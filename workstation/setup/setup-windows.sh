#!/usr/bin/env bash
# Install and configure the Workstation baseline on Windows, from Git Bash, with no admin rights, from a JSON profile.
# Tools are installed with Scoop under <root>/tools/scoop; repositories are cloned into <root>/git.
#
#   setup-windows.sh                    install the packages the profile turns on, then clone the repos
#   setup-windows.sh --profile my.json  another profile (copy profile-windows.json to profile-windows.local.json and edit it)
#   setup-windows.sh --only kubectl,jq  only these packages (upgrades them), whatever the profile says; no repos, no bashrc
#   setup-windows.sh --dry-run          show what would run and what is already there
#   setup-windows.sh --list             list the profile
#   setup-windows.sh --no-repos         skip the git clones         --no-tools   repos and bashrc only
#
# Run in Git Bash as your normal user. Needs Git for Windows and the root folder (default C:/work); PowerShell is called only for
# Scoop and to read the profile. Safe to run again: an installed package is skipped, a repo folder that exists is skipped.
# Repos are cloned over ssh with the key you already set up (ssh-agent or ~/.ssh): nothing is asked, a failed clone is reported at the end.
# Not covered, they need admin: Docker engine or Desktop, WSL itself. See ../site/index.html.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILE="$HERE/profile-windows.json"
ONLY=""; DRY=0; LIST=0; DO_TOOLS=1; DO_REPOS=1
MARK="# Managed by atlas workstation/setup/setup-windows.sh. Edits are replaced on the next run: put your own lines in ~/.bashrc.local"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile) PROFILE="$2"; shift 2 ;;
    --only) ONLY="$2"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    --list) LIST=1; shift ;;
    --no-repos) DO_REPOS=0; shift ;;
    --no-tools) DO_TOOLS=0; shift ;;
    -h|--help) sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1 (see --help)" >&2; exit 2 ;;
  esac
done

if [[ -t 1 ]]; then B=$'\e[1m'; G=$'\e[32m'; Y=$'\e[33m'; R=$'\e[31m'; N=$'\e[0m'; else B=""; G=""; Y=""; R=""; N=""; fi
say()  { printf '%s\n' "$*"; }
step() { printf '\n%s==> %s%s\n' "$B" "$*" "$N"; }
warn() { printf '%s!   %s%s\n' "$Y" "$*" "$N"; }
have() { command -v "$1" >/dev/null 2>&1; }
# Git Bash has cygpath, WSL has wslpath (only used to test this script from Linux)
winpath() { if have cygpath; then cygpath -w "$1"; else wslpath -w "$1"; fi; }
unixpath() { if have cygpath; then cygpath -u "$1"; else wslpath -u "$1"; fi; }
ps() { powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$1" | tr -d '\r'; }

have powershell.exe || { echo "powershell.exe not found: run this in Git Bash on Windows" >&2; exit 2; }
[[ -f "$PROFILE" ]] || { echo "profile not found: $PROFILE" >&2; exit 2; }

# --- Profile ----------------------------------------------------------------
# PowerShell reads the JSON (Git Bash has no python or jq yet). One line per item, tab separated: kind, key, value.
mapfile -t LINES < <(ps "\$p = Get-Content -Raw -LiteralPath '$(winpath "$PROFILE")' | ConvertFrom-Json
\$p.packages.PSObject.Properties | ForEach-Object { 'pkg' + [char]9 + \$_.Name + [char]9 + [int][bool]\$_.Value }
foreach (\$r in @(\$p.repos)) { if (\$r -is [string]) { 'repo' + [char]9 + \$r + [char]9 } elseif (\$r) { 'repo' + [char]9 + \$r.url + [char]9 + \$r.dir } }
'root' + [char]9 + \$p.root + [char]9
'git' + [char]9 + [string]\$p.settings.git.name + [char]9 + [string]\$p.settings.git.email + [char]9 + [string]\$p.settings.git.default_branch
'bashrc' + [char]9 + [int][bool]\$p.settings.bashrc + [char]9
'python' + [char]9 + [string]\$p.settings.python + [char]9
'node' + [char]9 + [string]\$p.settings.node + [char]9
'statusline' + [char]9 + [int][bool]\$p.settings.claude_statusline + [char]9
\$p.settings.aliases.PSObject.Properties | ForEach-Object { 'alias' + [char]9 + \$_.Name + [char]9 + \$_.Value }")

PKGS=(); declare -A PKG_ON; REPOS=(); REPO_DIRS=(); ALIASES=(); ROOT=""; G_NAME=""; G_EMAIL=""; G_BRANCH=""; BASHRC=0; STATUSLINE=0; S_PYTHON=""; S_NODE=""
for l in "${LINES[@]}"; do
  IFS=$'\t' read -r kind a b c <<<"$l"
  case "$kind" in
    pkg) PKGS+=("$a"); PKG_ON["$a"]="$b" ;;
    repo) [[ -n "$a" ]] && { REPOS+=("$a"); REPO_DIRS+=("$b"); } ;;
    root) ROOT="$a" ;;
    git) G_NAME="$a"; G_EMAIL="$b"; G_BRANCH="$c" ;;
    bashrc) BASHRC="$a" ;;
    statusline) STATUSLINE="$a" ;;
    python) S_PYTHON="$a" ;;
    node) S_NODE="$a" ;;
    alias) ALIASES+=("alias $a='$b'") ;;
  esac
done
[[ -n "$ROOT" ]] || { echo "profile has no \"root\"" >&2; exit 2; }
ROOT_U="$(unixpath "$ROOT")"; ROOT_W="$(winpath "$ROOT_U")"
GIT_DIR_U="$ROOT_U/git"; SCOOP_W="$ROOT_W\\tools\\scoop"; SCOOP_U="$ROOT_U/tools/scoop"

repo_name() { local n="${1##*/}"; n="${n##*:}"; echo "${n%.git}"; }   # git@github.com:me/x.git -> x

# --- List -------------------------------------------------------------------
if [[ $LIST -eq 1 ]]; then
  say "profile: $PROFILE"; say "root: $ROOT_W (tools in tools\\scoop, repos in git)"
  for k in "${PKGS[@]}"; do printf '  %-4s %s\n' "$([[ ${PKG_ON[$k]} -eq 1 ]] && echo on || echo off)" "$k"; done
  say "repos: ${#REPOS[@]}"
  for i in "${!REPOS[@]}"; do printf '  %s -> git/%s\n' "${REPOS[$i]}" "${REPO_DIRS[$i]:-$(repo_name "${REPOS[$i]}")}"; done
  exit 0
fi

[[ -d "$ROOT_U" ]] || { echo "root folder not found: $ROOT_W (create it first)" >&2; exit 2; }
have git || { echo "git not found: install Git for Windows first" >&2; exit 2; }
[[ $DRY -eq 1 ]] && say "${B}dry run: nothing is changed${N}"
FAILED=()
export PATH="$SCOOP_U/shims:$PATH"   # tools installed in this run are usable at once

# --- Scoop ------------------------------------------------------------------
scoop() { ps "\$env:SCOOP='$SCOOP_W'; & '$SCOOP_W\\shims\\scoop.ps1' $*"; }
scoop_have() { [[ -f "$SCOOP_U/shims/scoop.ps1" ]]; }
installed_pkgs() { scoop_have && scoop list 2>/dev/null | awk 'NR>1 {print $1}' | tr 'A-Z' 'a-z' || true; }

install_tools() {
  step "scoop (installs under $SCOOP_W, no admin)"
  if scoop_have; then say "scoop: installed"
  elif [[ $DRY -eq 1 ]]; then say "scoop: would be installed"
  else
    mkdir -p "$ROOT_U/tools"
    ps "\$env:SCOOP='$SCOOP_W'; [Environment]::SetEnvironmentVariable('SCOOP','$SCOOP_W','User'); Invoke-RestMethod https://get.scoop.sh | Invoke-Expression"
    scoop_have || { warn "scoop did not install; stopping the tools"; return 1; }
  fi
  if scoop_have; then
    scoop bucket list 2>/dev/null | grep -qw extras && say "bucket extras: added" || {
      [[ $DRY -eq 1 ]] && say "bucket extras: would be added (needed for kubelogin)" || scoop bucket add extras; }
  fi
  local have_list want=() k
  have_list="$(installed_pkgs)"
  if [[ -n "$ONLY" ]]; then IFS=, read -ra want <<<"$ONLY"
  else for k in "${PKGS[@]}"; do [[ ${PKG_ON[$k]} -eq 1 ]] && want+=("$k"); done; fi
  step "packages"
  for k in "${want[@]}"; do
    if grep -qx "$k" <<<"$have_list"; then
      if [[ -n "$ONLY" && $DRY -eq 0 ]]; then say "$k: updating"; scoop update "$k" || FAILED+=("package $k")
      else say "$k: installed, skipped"; fi
    elif [[ $DRY -eq 1 ]]; then say "$k: would be installed"
    else say "$k: installing"; scoop install "$k" || FAILED+=("package $k"); fi
  done
}

# uv and fnm are only managers: they still have to fetch a Python and a Node (settings.python: latest or a version, settings.node: lts or a version)
install_runtimes() {
  step "Python (uv) and Node (fnm)"
  if ! have uv; then warn "uv not found: Python skipped"
  elif [[ -z "$S_PYTHON" ]]; then say "python: off in the profile"
  elif [[ $DRY -eq 1 ]]; then say "python: would run uv python install ${S_PYTHON/latest/}"
  else uv python install $([[ "$S_PYTHON" == latest ]] || echo "$S_PYTHON") || FAILED+=("python"); fi
  if ! have fnm; then warn "fnm not found: Node skipped"
  elif [[ -z "$S_NODE" ]]; then say "node: off in the profile"
  elif [[ $DRY -eq 1 ]]; then say "node: would run fnm install and set it as default ($S_NODE)"
  else
    eval "$(fnm env --shell bash)"
    if [[ "$S_NODE" == lts ]]; then fnm install --lts && fnm default lts-latest || FAILED+=("node")
    else fnm install "$S_NODE" && fnm default "$S_NODE" || FAILED+=("node"); fi
    fnm list
  fi
}

# --- Git identity and shell -------------------------------------------------
configure_git() {
  step "git identity"
  [[ $DRY -eq 1 ]] && { say "would set name, email and default branch when empty"; return; }
  [[ -z "$G_BRANCH" ]] || git config --global init.defaultBranch "$G_BRANCH"
  git config --global user.name >/dev/null || { [[ -n "$G_NAME" ]] && git config --global user.name "$G_NAME" || warn "git user.name not set: commits will fail until it is"; }
  git config --global user.email >/dev/null || { [[ -n "$G_EMAIL" ]] && git config --global user.email "$G_EMAIL" || warn "git user.email not set: commits will fail until it is"; }
}

configure_bashrc() {
  step "~/.bashrc"
  [[ "$BASHRC" -eq 1 ]] || { say "off in the profile"; return; }
  local f="$HOME/.bashrc" begin="# >>> atlas windows >>>" end="# <<< atlas windows <<<" block
  block="$begin
$MARK
command -v fzf >/dev/null && eval \"\$(fzf --bash 2>/dev/null)\"
command -v zoxide >/dev/null && eval \"\$(zoxide init bash)\"
command -v starship >/dev/null && eval \"\$(starship init bash)\"
command -v fnm >/dev/null && eval \"\$(fnm env --use-on-cd --shell bash)\"
$(printf '%s\n' "${ALIASES[@]}")
[ -f ~/.bashrc.local ] && . ~/.bashrc.local
$end"
  if [[ -f "$f" ]] && grep -qF "$begin" "$f" && [[ "$(sed -n "/$begin/,/$end/p" "$f")" == "$block" ]]; then say "already up to date"; return; fi
  [[ $DRY -eq 1 ]] && { say "would write the managed block to $f"; return; }
  [[ -f "$f" ]] && cp "$f" "$f.bak" && sed -i "/$begin/,/$end/d" "$f"
  printf '\n%s\n' "$block" >>"$f"
  [[ -f ~/.bash_profile ]] || printf '[ -f ~/.bashrc ] && . ~/.bashrc\n' >~/.bash_profile
  say "written (backup: $f.bak); open a new Git Bash window"
}

# Claude Code status line: the same script as in WSL, run with uv (Python comes from uv, no admin). Needs uv and claude-code installed.
configure_statusline() {
  step "Claude Code status line"
  [[ "$STATUSLINE" -eq 1 ]] || { say "off in the profile"; return; }
  [[ $DRY -eq 1 ]] && { say "would copy claude-statusline.py to ~/.claude/statusline.py and set statusLine in ~/.claude/settings.json"; return; }
  have uv || { warn "uv not found: install the uv package first (open a new Git Bash if it was just installed)"; FAILED+=("statusline"); return; }
  mkdir -p ~/.claude
  cp "$HERE/claude-statusline.py" ~/.claude/statusline.py
  uv python install >/dev/null 2>&1 || warn "uv could not install Python; the status line needs one"
  # Set statusLine and keep every other setting
  uv run --quiet python -I - <<'PY' || { FAILED+=("statusline"); return; }
import json
from pathlib import Path
p = Path.home() / ".claude" / "settings.json"
s = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
s["statusLine"] = {"type": "command", "command": "uv run --quiet --script ~/.claude/statusline.py", "refreshInterval": 60}
p.write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
PY
  say "status line set: it shows in the next Claude Code session"
}

# --- Repositories -----------------------------------------------------------
clone_repos() {
  step "repositories into $ROOT_W\\git"
  [[ ${#REPOS[@]} -gt 0 ]] || { say "none in the profile"; return; }
  [[ $DRY -eq 1 ]] || mkdir -p "$GIT_DIR_U"
  local i url dir
  for i in "${!REPOS[@]}"; do
    url="${REPOS[$i]}"; dir="${REPO_DIRS[$i]:-$(repo_name "$url")}"
    if [[ -e "$GIT_DIR_U/$dir" ]]; then say "$dir: exists, skipped"
    elif [[ $DRY -eq 1 ]]; then say "$dir: would be cloned from $url"
    else
      say "$dir: cloning"
      # BatchMode: never wait for a password; accept-new: trust a host seen for the first time, still fail if its key changes
      GIT_SSH_COMMAND="ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new" git clone "$url" "$GIT_DIR_U/$dir" || FAILED+=("repo $dir")
    fi
  done
}

if [[ $DO_TOOLS -eq 1 ]]; then install_tools || FAILED+=("scoop"); fi
if [[ -z "$ONLY" && $DO_TOOLS -eq 1 ]]; then install_runtimes; configure_git; configure_bashrc; configure_statusline; fi
if [[ -z "$ONLY" && $DO_REPOS -eq 1 ]]; then clone_repos; fi

step "summary"
if [[ ${#FAILED[@]} -gt 0 ]]; then printf '%sfailed: %s%s\n' "$R" "${FAILED[*]}" "$N"; exit 1; fi
say "${G}done${N}. Open a new Git Bash window so the PATH and ~/.bashrc apply."
