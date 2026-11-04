# Workstation setup: spec

Status: kept in git, not published (not in `topics.json`, built to `workstation/site/index.html`). Data checked 2026-10-31. Reconstructed from the
data, the `CLAUDE.md` of this folder and git history, not written before the content: reasons that the history does not record are marked "reason
unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

The baseline to take a new Windows PC to a working development setup: WSL 2 with the latest Ubuntu LTS, and the tools that fit the author's toolchain.
Each step says how to install, how to update and what to check. A setup script does the same from a profile.

## Scope

- In: WSL, Windows Terminal, the shell (zsh), Python (uv), Node (fnm, pnpm), Kubernetes tools, Terraform, the Azure CLI, containers, git and Claude Code.
  Free tools first. A tool with a paid plan or a licence that is not open source says so and names the free alternative.
- Out: the browser and Windows-only apps, and anything that needs admin on the Windows script (Docker included).
- Not an Atlas topic: it does not appear in the banner or the landing page and is never deployed. It keeps the same data model, checks and shared
  page, with a banner that names only itself.

## Layout

Archetype: setup guide. Thirteen tabs: Start here, WSL and Ubuntu, Terminal, Shell, Python, Node, Kubernetes, Terraform, Azure CLI, Docker,
Claude Code, Other tools, Compare. Groups: start here, Windows side, shell, Python and Node, Kubernetes, Terraform and cloud, containers, development.
Comparisons: shells; Python and Node side by side; a Kubernetes cluster on the workstation. The setup scripts are in `setup/`: `setup.sh` with
`profile.json` for WSL Ubuntu (and `profile-ubuntu.json` for native Ubuntu, same script), and `setup-windows.sh` with `profile-windows.json` for Git Bash on Windows (Scoop, no admin).

## Sources

Each vendor's install page and repository, Ubuntu's package archive for apt-installed tools (the Ubuntu 26.04 package version and the upstream
release are both recorded), and the Microsoft Learn WSL pages. Re-check with `make workstation-check`. Several tools release weekly: update
`version` and `checked` and re-read the page only when a minor or major version changed. When Ubuntu ships a new LTS, re-check every apt step.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `baseline` | done | |
| `wsl` | done | |
| `windows-terminal` | done | |
| `zsh` | done | |
| `uv` | done | |
| `node` | done | fnm; pnpm is a reference |
| `kubectl` | done | with Helm, k9s, kubectx and kubens, kubelogin |
| `terraform` | done | the tool's install; the language is the `terraform` Atlas topic |
| `azure-cli` | done | |
| `docker` | done | Docker Engine inside Ubuntu |
| `claude-code` | done | with git identity and the GitHub CLI |
| `windows-script` | planned | the guide does not describe the Windows setup script yet |

## Known gaps

- The Windows setup script was tested from WSL with `--list`, `--dry-run` and local repositories, and the owner has run it on Windows and reported it works. No run log or date is kept.
- The `winget` line and the installer choices in the README are unverified: confirm against git-scm.com before relying on them.
- The guide (`data/workstation.json`) does not describe the Windows script.
- The Claude Code status line on Windows was not checked separately from the script run.

## Decisions

- Development happens in WSL 2; Windows keeps the browser and Windows-only apps. Reason unconfirmed beyond the scope text.
- `setup.sh` is the one place commands are written out rather than fetched, so a step changed in the data needs the matching `c_<component>`
  function changed too. It must stay idempotent: each component has a check and is skipped when done.
- The repository is public: committed profiles keep `repos` empty and git name and email empty. Private URLs go in `setup/*.local.json`.
- Unpublished on purpose (PR #17, "Unpublish Workstation setup"). Reason unconfirmed beyond the commit title.

## Updating

Run `make workstation-check`, update `version` and `checked`, and change the matching `c_<component>` function when a vendor's install command or a
repository line changes. Test the scripts with `--dry-run` and `--list`, and `bash -n` for syntax. Update the README when a component, a profile key
or a prerequisite changes.
