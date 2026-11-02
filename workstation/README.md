# Workstation setup

A new Windows PC to a working development setup, in two parts that can be used together:

- **WSL (Ubuntu)**: the main place for development. Every CLI tool for day-to-day work.
- **Windows (Git Bash)**: the same tools without admin rights, for repositories that need Windows apps, such as Claude in Chrome (it does
  not work from WSL).

Not published; see the [root README](../README.md). The full guide with sources and versions is `site/index.html` (`make build`, then open
it). For VS Code, see [../vscode/README.md](../vscode/README.md).

Both scripts read a JSON profile, are safe to run again (what is installed or cloned is skipped), and have `--dry-run` and `--list`.
To clone repositories, add them to `repos` in a profile; the committed profiles stay empty because this repo is public. Copy a profile to
`setup/<name>.local.json` (git-ignored), edit it and pass `--profile`.

## A. WSL (Ubuntu)

### Before you run it (done by hand, needs admin once)

1. Windows 10 22H2 or Windows 11, with virtualisation enabled in the BIOS/UEFI.
2. In an administrator PowerShell: `wsl --install -d Ubuntu`, then restart if asked. Open Ubuntu and create your user.
3. Your SSH key in `~/.ssh` (or an ssh-agent) if the profile lists repos to clone over ssh. The scripts never create keys.
4. Network access; the script asks for your sudo password once.

### Run it (in Ubuntu, as your normal user)

```bash
sudo apt-get update && sudo apt-get install -y git make     # if not there yet
git clone <this repo> ~/work/atlas && cd ~/work/atlas/workstation
make setup-dry-run     # what would happen
make setup             # do it (ARGS="--only helm" to run or upgrade one component)
```

`wsl.conf` changes (systemd, default user) need `wsl --shutdown` in PowerShell, then reopen Ubuntu and run `make setup` again for Docker.

### What it installs (`setup/profile.json`, each can be turned off)

apt update and upgrade, `wsl.conf`, git identity, GitHub CLI, zsh with autosuggestions and syntax highlighting, fzf, zoxide, jq, starship,
uv (Python), fnm and pnpm (Node), kubectl, kubectx, helm, k9s, kind, kubelogin, Terraform, tflint, Azure CLI, Docker Engine, Claude Code
and its status line, your `~/.zshrc`, and the repos in `~/git`. Off by default: krew, OpenTofu.

After it: `gh auth login`, `az login`, sign in to Claude Code.

## B. Windows (Git Bash, no admin)

### Before you run it

1. **Git for Windows** installed (it provides Git Bash). If it is not: download the installer from https://git-scm.com/download/win and
   keep "Git Bash" and "Git from the command line and also from 3rd-party software" selected, or run `winget install --id Git.Git` in
   PowerShell. Open **Git Bash** from the Start menu to check: `git --version`.
2. The folder **`C:\work`** exists. The script creates `tools\` (Scoop and every tool) and `git\` (clones) inside it.
3. A working SSH key for the repos, loaded in ssh-agent or in `~/.ssh` (Git Bash home).
4. PowerShell present (it is, on Windows); the script uses it only to install Scoop and read the profile.
5. Network access. Windows must allow running a downloaded user script for Scoop; the script passes `-ExecutionPolicy Bypass` for its own call only.

### Run it (in Git Bash)

```bash
cd /c/work/git && git clone <this repo> atlas && cd atlas/workstation
setup/setup-windows.sh --list        # the profile
setup/setup-windows.sh --dry-run     # what would be installed and cloned
setup/setup-windows.sh               # do it
```

Git Bash does not ship `make`, so the first run uses the script directly. It installs `make` (via Scoop), and in a new Git Bash window
`make workstation-win-setup` and its `win-list` and `win-dry-run` variants work from the repo root or `workstation/`. Open a new Git Bash
window after the run for the PATH.

### What it installs (`setup/profile-windows.json`)

Scoop under `C:\work\tools\scoop` (user environment variable `SCOOP`), then: make, Python (the real python.org build: `python` and `python3` work in Git Bash, ahead of the Microsoft Store stub), GitHub CLI, jq, fzf, zoxide, starship, uv, fnm, pnpm, kubectl,
kubectx, helm, k9s, kind, kubelogin, Terraform, tflint, Azure CLI, Claude Code. It then installs the Node LTS with fnm (set as default; `settings.node` in the profile; `settings.python` makes uv fetch a Python for projects that pin one; the Scoop `python` package is the one on the PATH). Off by default: OpenTofu. It also installs the Claude Code status line (`~/.claude/statusline.py`, run with uv, which also provides Python; turn off with `claude_statusline` in the profile), sets your git identity when
empty, writes a managed block in `~/.bashrc` (backed up first; your own lines go in `~/.bashrc.local`), and clones `repos` into `C:\work\git`.

### Not covered (needs admin)

Docker Engine or Docker Desktop, WSL itself, and any app that comes as an installer. After it: `gh auth login`, `az login`, sign in to
Claude Code. Claude Code needs Git Bash, which you already have; if it does not find it, set `CLAUDE_CODE_GIT_BASH_PATH`.
