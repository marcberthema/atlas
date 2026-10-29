#!/usr/bin/env bash
# Install and configure the Workstation setup baseline (../site/index.html) in WSL Ubuntu, from a JSON profile.
#
#   setup.sh                      run every component the profile turns on
#   setup.sh --profile my.json    another profile (copy profile.json and edit it)
#   setup.sh --only kubectl,helm  run these components, whatever the profile says
#   setup.sh --dry-run            show what would run and what is already installed
#   setup.sh --list               list the components and whether the profile turns them on
#
# Run as your normal user, not root: it asks for sudo once. Safe to run again: a component that is
# already installed is skipped (apt ones are upgraded by apt_upgrade). Needs python3 (Ubuntu has it) to read the profile.
# The commands follow each vendor's install page, linked in the guide. When a vendor page changes, update the step here too.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="$HERE/profile.json"
ONLY=""
DRY=0
LIST=0
ARCH="$(dpkg --print-architecture)"   # amd64 or arm64
MARK="# Managed by atlas workstation/setup/setup.sh. Edits are replaced on the next run: put your own lines in ~/.zshrc.local"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --list) LIST=1; shift ;;
    -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

# --- Output -----------------------------------------------------------------
if [[ -t 1 ]]; then B=$'\e[1m'; G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; N=$'\e[0m'; else B=""; G=""; Y=""; R=""; N=""; fi
say()  { printf '%s\n' "$*"; }
step() { printf '\n%s==> %s%s\n' "$B" "$*" "$N"; }
warn() { printf '%s!   %s%s\n' "$Y" "$*" "$N"; }
have() { command -v "$1" >/dev/null 2>&1; }
apt_install() { sudo DEBIAN_FRONTEND=noninteractive apt-get install -y "$@"; }

# --- Profile ----------------------------------------------------------------
[[ -f "$PROFILE" ]] || { echo "profile not found: $PROFILE" >&2; exit 2; }
# The profile becomes shell variables: ON_<component>=0|1 and S_<setting>=value, quoted by python.
eval "$(python3 -I - "$PROFILE" <<'EOF'
import json, shlex, sys
p = json.load(open(sys.argv[1]))
for k, v in p["components"].items():
    print(f"ON_{k}={1 if v else 0}")
s = p.get("settings", {})
g = s.get("git", {})
for k, v in (("git_name", g.get("name", "")), ("git_email", g.get("email", "")), ("git_branch", g.get("default_branch", "")),
             ("python", s.get("python", "")), ("node", s.get("node", "lts")), ("kubectl_minor", s.get("kubectl_minor", "")),
             ("docker_group", "1" if s.get("docker_group", True) else "0"), ("starship_k8s", "1" if s.get("starship_kubernetes", True) else "0")):
    print(f"S_{k}={shlex.quote(str(v))}")
print("ALIASES=" + shlex.quote("\n".join(f"alias {k}={shlex.quote(v)}" for k, v in s.get("aliases", {}).items())))
print("COMPONENTS=" + shlex.quote(" ".join(p["components"])))
EOF
)"

# --- Components: one function each, in the guide's order ------------------------
# DESC is shown by --list and --dry-run; CHECK is a command that succeeds when the component is already done.
declare -A DESC CHECK
ORDER=(apt_upgrade wsl_conf git gh zsh zsh_plugins fzf zoxide starship uv fnm pnpm kubectl kubectx helm k9s kind kubelogin krew
       terraform opentofu tflint azure_cli docker claude_code zshrc)

in_wsl() { grep -qi microsoft /proc/version; }
systemd_running() { [[ "$(ps -p 1 -o comm=)" == systemd ]]; }

DESC[apt_upgrade]="apt update and upgrade (also upgrades every tool installed from an apt repository)"
CHECK[apt_upgrade]="false"
c_apt_upgrade() { sudo apt-get update && sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y; }

DESC[wsl_conf]="/etc/wsl.conf: [boot] systemd=true and [user] default=\$USER"
CHECK[wsl_conf]="grep -qx 'systemd=true' /etc/wsl.conf 2>/dev/null && grep -qx \"default=$USER\" /etc/wsl.conf"
c_wsl_conf() {
  in_wsl || { warn "not WSL: skipped"; return 0; }
  # Set the two keys and keep everything else in the file
  sudo python3 -I - "$USER" <<'EOF'
import sys
from pathlib import Path
p = Path("/etc/wsl.conf")
lines = p.read_text().splitlines() if p.exists() else []
def put(section, key, value):
    head = f"[{section}]"
    if head not in [l.strip() for l in lines]:
        lines.extend(["", head, f"{key}={value}"] if lines else [head, f"{key}={value}"])
        return
    i = [l.strip() for l in lines].index(head) + 1
    j = i
    while j < len(lines) and not lines[j].strip().startswith("["):
        if lines[j].split("=")[0].strip() == key:
            lines[j] = f"{key}={value}"
            return
        j += 1
    lines.insert(j if j == len(lines) or lines[j - 1].strip() else j - 1, f"{key}={value}")
put("boot", "systemd", "true")
put("user", "default", sys.argv[1])
p.write_text("\n".join(lines) + "\n")
EOF
  warn "wsl.conf changed: run 'wsl --shutdown' in PowerShell, reopen Ubuntu, then run this script again for docker"
}

DESC[git]="git identity (name, email, default branch) when not set yet"
CHECK[git]="git config --global user.name >/dev/null && git config --global user.email >/dev/null"
c_git() {
  have git || apt_install git
  local name="$S_git_name" email="$S_git_email"
  if ! git config --global user.name >/dev/null; then
    [[ -n "$name" ]] || { [[ -t 0 ]] && read -rp "git user.name: " name; } || true
    [[ -n "$name" ]] && git config --global user.name "$name" || warn "git user.name not set: commits will fail until it is"
  fi
  if ! git config --global user.email >/dev/null; then
    [[ -n "$email" ]] || { [[ -t 0 ]] && read -rp "git user.email: " email; } || true
    [[ -n "$email" ]] && git config --global user.email "$email" || warn "git user.email not set: commits will fail until it is"
  fi
  [[ -z "$S_git_branch" ]] || git config --global init.defaultBranch "$S_git_branch"
}

DESC[gh]="GitHub CLI from GitHub's apt repository (then run: gh auth login)"
CHECK[gh]="have gh && grep -rqs cli.github.com/packages /etc/apt/sources.list.d/"
c_gh() {
  sudo mkdir -p -m 755 /etc/apt/keyrings
  local out; out="$(mktemp)"
  wget -nv -O"$out" https://cli.github.com/packages/githubcli-archive-keyring.gpg
  sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg <"$out" >/dev/null
  sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$ARCH signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null
  sudo apt-get update && apt_install gh
  gh auth status >/dev/null 2>&1 || warn "sign in with: gh auth login"
}

DESC[zsh]="zsh from apt, made your login shell"
CHECK[zsh]="have zsh && [[ \"\$(getent passwd $USER | cut -d: -f7)\" == */zsh ]]"
c_zsh() {
  have zsh || apt_install zsh
  [[ "$(getent passwd "$USER" | cut -d: -f7)" == */zsh ]] || sudo chsh -s "$(command -v zsh)" "$USER"
  say "login shell: $(getent passwd "$USER" | cut -d: -f7) (new tabs use it)"
}

DESC[zsh_plugins]="zsh-autosuggestions and zsh-syntax-highlighting from apt"
CHECK[zsh_plugins]="[[ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh && -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]"
c_zsh_plugins() { apt_install zsh-autosuggestions zsh-syntax-highlighting; }

DESC[fzf]="fzf from apt (Ctrl+R history, Ctrl+T files, Alt+C directories)"
CHECK[fzf]="have fzf"
c_fzf() { apt_install fzf; }

DESC[zoxide]="zoxide from apt (z <dir>)"
CHECK[zoxide]="have zoxide"
c_zoxide() { apt_install zoxide; }

DESC[starship]="Starship prompt (install script) and ~/.config/starship.toml"
CHECK[starship]="have starship && [[ -f ~/.config/starship.toml ]]"
c_starship() {
  have starship || curl -sS https://starship.rs/install.sh | sh -s -- -y
  mkdir -p ~/.config
  if [[ -f ~/.config/starship.toml ]] && ! grep -qF "$MARK" ~/.config/starship.toml; then
    say "~/.config/starship.toml exists and is yours: left as is"; return 0
  fi
  cat >~/.config/starship.toml <<EOF
$MARK
# Starship prompt: https://starship.rs/config/
add_newline = true

[directory]
truncation_length = 4        # parent folders shown (default 3)
truncate_to_repo = true      # inside a repo, start at the repo root

[cmd_duration]
min_time = 2_000             # show how long commands over 2 s took

[kubernetes]
disabled = $([[ "$S_starship_k8s" == 1 ]] && echo false || echo true)             # off by default in Starship: kubectl context and namespace

[time]
disabled = true              # false for a clock
EOF
}

DESC[uv]="uv (Astral installer) and a Python from uv (settings.python)"
CHECK[uv]="[[ -x ~/.local/bin/uv ]]"
c_uv() {
  # The managed ~/.zshrc puts ~/.local/bin on PATH, so the installer must not edit shell files
  [[ -x ~/.local/bin/uv ]] || curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh
  case "$S_python" in
    "") ;;
    latest) ~/.local/bin/uv python install ;;
    *) ~/.local/bin/uv python install "$S_python" ;;
  esac
}

DESC[fnm]="fnm (installer, --skip-shell) and Node (settings.node: lts or a version), set as default"
CHECK[fnm]="[[ -x ~/.local/share/fnm/fnm ]]"
c_fnm() {
  have unzip || apt_install unzip
  [[ -x ~/.local/share/fnm/fnm ]] || curl -fsSL https://fnm.vercel.app/install | bash -s -- --skip-shell
  local fnm="$HOME/.local/share/fnm/fnm"
  eval "$("$fnm" env --shell bash)"
  if [[ "$S_node" == lts ]]; then
    "$fnm" install --lts && "$fnm" default lts-latest
  elif [[ -n "$S_node" ]]; then
    "$fnm" install "$S_node" && "$fnm" default "$S_node"
  fi
  "$fnm" list
}

DESC[pnpm]="pnpm (standalone installer, no shell edits)"
CHECK[pnpm]="[[ -x ~/.local/share/pnpm/pnpm || -x ~/.local/share/pnpm/bin/pnpm ]]"
c_pnpm() { curl -fsSL https://get.pnpm.io/install.sh | env PNPM_NO_MODIFY_PATH=1 sh -; }

DESC[kubectl]="kubectl from pkgs.k8s.io (settings.kubectl_minor; changing it upgrades kubectl)"
CHECK[kubectl]="have kubectl && grep -q \"/$S_kubectl_minor/\" /etc/apt/sources.list.d/kubernetes.list 2>/dev/null"
c_kubectl() {
  apt_install apt-transport-https ca-certificates curl gnupg
  sudo mkdir -p -m 755 /etc/apt/keyrings
  curl -fsSL "https://pkgs.k8s.io/core:/stable:/$S_kubectl_minor/deb/Release.key" | sudo gpg --dearmor --yes -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
  sudo chmod 644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
  echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/$S_kubectl_minor/deb/ /" \
    | sudo tee /etc/apt/sources.list.d/kubernetes.list >/dev/null
  sudo chmod 644 /etc/apt/sources.list.d/kubernetes.list
  sudo apt-get update && apt_install kubectl
  kubectl version --client
}

DESC[kubectx]="kubectx and kubens from apt"
CHECK[kubectx]="have kubectx"
c_kubectx() { apt_install kubectx; }

DESC[helm]="Helm 4 (get-helm-4 script; rerun the component to upgrade)"
CHECK[helm]="have helm"
c_helm() {
  local s; s="$(mktemp)"
  curl -fsSL -o "$s" https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
  bash "$s"
}

DESC[k9s]="k9s .deb from the latest GitHub release"
CHECK[k9s]="have k9s"
c_k9s() {
  local d; d="$(mktemp -d)"
  curl -fsSL -o "$d/k9s.deb" "https://github.com/derailed/k9s/releases/latest/download/k9s_linux_$ARCH.deb"
  apt_install "$d/k9s.deb"
}

latest_tag() { curl -fsSLI -o /dev/null -w '%{url_effective}' "https://github.com/$1/releases/latest" | sed 's|.*/tag/||'; }

DESC[kind]="kind binary, latest release, into /usr/local/bin (needs docker)"
CHECK[kind]="have kind"
c_kind() {
  local v; v="$(latest_tag kubernetes-sigs/kind)"
  curl -fsSLo /tmp/kind "https://kind.sigs.k8s.io/dl/$v/kind-linux-$ARCH"
  sudo install -m 0755 /tmp/kind /usr/local/bin/kind && rm /tmp/kind
  kind version
}

DESC[kubelogin]="Azure kubelogin, latest release zip, into /usr/local/bin"
CHECK[kubelogin]="have kubelogin"
c_kubelogin() {
  have unzip || apt_install unzip
  local d; d="$(mktemp -d)"
  curl -fsSL -o "$d/k.zip" "https://github.com/Azure/kubelogin/releases/latest/download/kubelogin-linux-$ARCH.zip"
  unzip -q "$d/k.zip" -d "$d"
  sudo install -m 0755 "$(find "$d" -type f -name kubelogin | head -1)" /usr/local/bin/kubelogin
  kubelogin --version
}

DESC[krew]="krew, the kubectl plugin manager (krew's install snippet)"
CHECK[krew]="[[ -x ~/.krew/bin/kubectl-krew ]]"
c_krew() {
  cd "$(mktemp -d)"
  local os arch krew
  os="$(uname | tr '[:upper:]' '[:lower:]')"
  arch="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')"
  krew="krew-${os}_${arch}"
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/${krew}.tar.gz"
  tar zxf "${krew}.tar.gz"
  ./"${krew}" install krew
}

DESC[terraform]="Terraform from HashiCorp's apt repository"
CHECK[terraform]="have terraform"
c_terraform() {
  wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor --yes -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
  echo "deb [arch=$ARCH signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" \
    | sudo tee /etc/apt/sources.list.d/hashicorp.list >/dev/null
  sudo apt-get update && apt_install terraform
  terraform version
}

DESC[opentofu]="OpenTofu (installer script, --install-method deb)"
CHECK[opentofu]="have tofu"
c_opentofu() {
  local s; s="$(mktemp)"
  curl --proto '=https' --tlsv1.2 -fsSL https://get.opentofu.org/install-opentofu.sh -o "$s"
  chmod +x "$s" && "$s" --install-method deb && rm -f "$s"
}

DESC[tflint]="TFLint, latest release zip, into /usr/local/bin"
CHECK[tflint]="have tflint"
c_tflint() {
  have unzip || apt_install unzip
  local d; d="$(mktemp -d)"
  curl -fsSL -o "$d/t.zip" "https://github.com/terraform-linters/tflint/releases/latest/download/tflint_linux_$ARCH.zip"
  unzip -q "$d/t.zip" -d "$d"
  sudo install -m 0755 "$d/tflint" /usr/local/bin/tflint
  tflint --version
}

DESC[azure_cli]="Azure CLI (Microsoft's one-command script, adds its apt repository)"
CHECK[azure_cli]="have az"
c_azure_cli() { curl -fsSL 'https://azurecliprod.blob.core.windows.net/$root/deb_install.sh' | sudo bash; }

DESC[docker]="Docker Engine from Docker's apt repository, docker group (settings.docker_group), enabled in systemd"
CHECK[docker]="have docker && [[ -f /etc/apt/sources.list.d/docker.sources ]]"
c_docker() {
  if [[ -e /mnt/wsl/docker-desktop ]] || { have docker && [[ "$(readlink -f "$(command -v docker)")" == /mnt/* ]]; }; then
    warn "Docker Desktop's WSL integration is present: running both conflicts. Skipped."; return 0
  fi
  systemd_running || { warn "systemd is not running (wsl_conf, then wsl --shutdown): skipped"; return 0; }
  apt_install ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc
  sudo tee /etc/apt/sources.list.d/docker.sources >/dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $ARCH
Signed-By: /etc/apt/keyrings/docker.asc
EOF
  sudo apt-get update
  apt_install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  sudo systemctl enable --now docker.service containerd.service
  if [[ "$S_docker_group" == 1 ]] && ! id -nG "$USER" | grep -qw docker; then
    sudo usermod -aG docker "$USER"
    warn "added to the docker group (root-level access). It applies after: wsl --terminate <distro>, or a new login"
  fi
}

DESC[claude_code]="Claude Code (native installer; it updates itself)"
CHECK[claude_code]="[[ -x ~/.local/bin/claude ]]"
c_claude_code() { curl -fsSL https://claude.ai/install.sh | bash; }

DESC[zshrc]="~/.zshrc and its completions for the tools above (the previous file is backed up once)"
CHECK[zshrc]="grep -qF \"$MARK\" ~/.zshrc 2>/dev/null"
c_zshrc() {
  if [[ -f ~/.zshrc ]] && ! grep -qF "$MARK" ~/.zshrc; then
    cp ~/.zshrc ~/.zshrc.bak-"$(date +%Y%m%d-%H%M%S)"
    say "previous ~/.zshrc backed up next to it"
  fi
  mkdir -p ~/.zsh/completions
  cat >~/.zshrc <<EOF
$MARK

# --- PATH: per-user tools (uv, claude, starship, fnm, pnpm, krew) ---------------
export PATH="\$HOME/.local/bin:\$HOME/.local/share/fnm:\$PATH"
export PNPM_HOME="\$HOME/.local/share/pnpm"
export PATH="\$PNPM_HOME/bin:\$PNPM_HOME:\$PATH"
[[ -d "\${KREW_ROOT:-\$HOME/.krew}/bin" ]] && export PATH="\${KREW_ROOT:-\$HOME/.krew}/bin:\$PATH"

# --- History ----------------------------------------------------------------
HISTFILE=~/.zsh_history
HISTSIZE=50000
SAVEHIST=50000
setopt SHARE_HISTORY HIST_IGNORE_ALL_DUPS HIST_IGNORE_SPACE HIST_REDUCE_BLANKS

# --- Behaviour --------------------------------------------------------------
setopt AUTO_CD INTERACTIVE_COMMENTS
bindkey -e

# --- Completion -------------------------------------------------------------
fpath=(~/.zsh/completions \$fpath)
autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' menu select

command -v fnm      >/dev/null && eval "\$(fnm env --use-on-cd --shell zsh)"
command -v uv       >/dev/null && eval "\$(uv generate-shell-completion zsh)"
command -v uvx      >/dev/null && eval "\$(uvx --generate-shell-completion zsh)"
command -v kubectl  >/dev/null && source <(kubectl completion zsh)
command -v gh       >/dev/null && [[ ! -f ~/.zsh/completions/_gh ]] && gh completion -s zsh > ~/.zsh/completions/_gh

# --- Aliases (settings.aliases in the profile) ----------------------------------
$ALIASES

# --- Plugins and prompt -----------------------------------------------------
[[ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
command -v fzf      >/dev/null && source <(fzf --zsh)
command -v zoxide   >/dev/null && eval "\$(zoxide init zsh)"
command -v starship >/dev/null && eval "\$(starship init zsh)"

# Your own lines
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local

# Must stay last
[[ -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
EOF
  if have zsh; then zsh -n ~/.zshrc; fi
  say "~/.zshrc written: open a new tab or run 'exec zsh'"
}

# --- Run --------------------------------------------------------------------
selected() {   # 0 when the component runs: in --only, or on in the profile
  local c="$1" on="ON_$1"
  if [[ -n "$ONLY" ]]; then [[ ",$ONLY," == *",$c,"* ]]; else [[ "${!on:-0}" == 1 ]]; fi
}

for c in $COMPONENTS; do [[ -n "${DESC[$c]:-}" ]] || { echo "profile names an unknown component: $c" >&2; exit 2; }; done
if [[ -n "$ONLY" ]]; then
  for c in ${ONLY//,/ }; do [[ -n "${DESC[$c]:-}" ]] || { echo "unknown component in --only: $c" >&2; exit 2; }; done
fi

if [[ $LIST == 1 || $DRY == 1 ]]; then
  say "${B}profile:${N} $PROFILE"
  for c in "${ORDER[@]}"; do
    if ! selected "$c"; then
      [[ $LIST == 1 ]] && printf '  %s%-12s off%s  %s\n' "$Y" "$c" "$N" "${DESC[$c]}"
      continue
    fi
    if [[ $DRY == 1 ]] && eval "${CHECK[$c]}" 2>/dev/null; then state="${G}done${N}"; else state="${B}run ${N}"; fi
    [[ $LIST == 1 ]] && state="${G}on ${N}"
    printf '  %-12s %s  %s\n' "$c" "$state" "${DESC[$c]}"
  done
  exit 0
fi

[[ $EUID -ne 0 ]] || { echo "run as your normal user, not root: tools install into your home" >&2; exit 1; }
grep -q '^ID=ubuntu' /etc/os-release || warn "not Ubuntu: the apt steps assume Ubuntu"
in_wsl || warn "not running in WSL: wsl_conf is skipped"

say "${B}profile:${N} $PROFILE"
sudo -v
while true; do sudo -n true; sleep 50; kill -0 "$$" 2>/dev/null || exit; done 2>/dev/null &
KEEPALIVE=$!
trap 'kill $KEEPALIVE 2>/dev/null || true' EXIT

step "base packages"
sudo apt-get update
apt_install ca-certificates curl wget gpg unzip git

declare -a DONE SKIPPED FAILED
for c in "${ORDER[@]}"; do
  selected "$c" || continue
  if [[ "$c" != apt_upgrade && "$c" != zshrc && "$c" != git ]] && eval "${CHECK[$c]}" 2>/dev/null; then
    SKIPPED+=("$c"); continue
  fi
  step "$c: ${DESC[$c]}"
  set +e
  ( set -e; "c_$c" )
  rc=$?
  set -e
  if [[ $rc -eq 0 ]]; then DONE+=("$c"); else FAILED+=("$c"); printf '%s!   %s failed (exit %s), carrying on%s\n' "$R" "$c" "$rc" "$N"; fi
done

step "summary"
say "${G}done:${N}    ${DONE[*]:-none}"
say "already: ${SKIPPED[*]:-none}"
[[ ${#FAILED[@]} -eq 0 ]] || say "${R}failed:${N}  ${FAILED[*]} (rerun with --only ${FAILED[*]// /,})"
say "Open a new Ubuntu tab (or 'exec zsh') to load the shell setup."
[[ ${#FAILED[@]} -eq 0 ]]
