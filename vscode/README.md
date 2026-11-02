# Visual Studio Code setup

VS Code on Windows, working in WSL Ubuntu: the extensions that fit the Workstation toolchain, how each is configured, and a script that
installs and configures them from a profile. Not published; see the [root README](../README.md) for how it fits in Atlas.

## On a new workstation

Do the [Workstation setup](../workstation/README.md) first (WSL 2, Ubuntu, zsh, uv, fnm, kubectl, Terraform, Azure CLI, Docker): the extensions
and settings assume those tools exist in Ubuntu.

1. **Install VS Code on Windows**, with "Add to PATH" checked. From WSL: `winget.exe install Microsoft.VisualStudioCode`.
2. **Clone this repo in Ubuntu** (in the Linux filesystem, e.g. `~/work`, not under `/mnt/c`) and `cd atlas/vscode`.
3. **Preview**: `make setup-list` shows the profile, `make setup-dry-run` shows what would be installed and which settings would change.
4. **Run it**: `make setup` (same as `setup/setup.sh`). Run as your normal user, no sudo. It installs the WSL extension on Windows and the
   others inside Ubuntu, then merges the settings into the Windows user `settings.json` (a backup is made first).
5. **If it warns** that the VS Code server folder is missing, run `code .` once from Ubuntu, then run `make setup` again.
6. **Open projects from Ubuntu** with `code .`; the window title shows `[WSL: Ubuntu]`.
7. **Sign in** to what needs it (GitHub for the pull request extension, Claude Code, Azure). Nothing secret is in the profile.

Safe to run again: installed extensions are skipped and settings already at their value are left alone.

## Choose what is installed

Edit `setup/profile.json` (`on: true/false` per extension and settings group), or copy it and pass it:

```bash
setup/setup.sh --profile my.json
make setup ARGS="--only ruff,terraform"   # only these, even if the profile has them off
make setup ARGS="--no-settings"           # extensions only (or --no-extensions)
```

## Read the guide

`make build` generates `site/index.html`; open it in a browser. It lists every extension, its settings and sources.

## Makefile

Run `make` for the list of targets. `setup*` act on your machine; `validate`, `build`, `check` and `examples` maintain the guide.
`make check` needs network access.
