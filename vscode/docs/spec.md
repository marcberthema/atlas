# Visual Studio Code setup: spec

Status: kept in git, not published (`vscode/site/index.html`). Data checked 2026-10-29. Reconstructed from the data, the `CLAUDE.md` of this folder
and git history, not written before the content: reasons that the history does not record are marked "reason unconfirmed". Format:
`docs/topic-spec.md`.

## Purpose and audience

VS Code on Windows working in WSL Ubuntu: the extensions that fit the toolchain of the Workstation guide, how each is configured where it needs
it, and a script that installs and configures them from a profile. An evolving document: add an extension when a tool is added to the workstation.

## Scope

- In: extensions for Claude Code, Python with uv, Node with pnpm, Kubernetes, Terraform, Azure, Docker, GitHub and shell scripts, and the settings the
  profile merges into the user `settings.json`. Free extensions first; a paid tier or a proprietary licence is stated.
- Out: extensions that were looked at and left out are `ref` entries in the group `g-more` (Copilot, the Azure CLI tools, the old Docker extension,
  the Microsoft Terraform on Azure preview), each saying why.
- Versions are the newest stable Marketplace build, never a pre-release.

## Layout

Archetype: setup guide. Thirteen tabs: Start here, WSL, Claude Code, six group tabs (Python, JavaScript, Kubernetes, Terraform and Azure, containers,
git, files: group tabs show every extension of the group in full), Settings, Other tools, Compare. Comparisons: where a setting can live, what
happens when a file is saved. `setup/profile.json` says which extensions are on and where they install (`wsl` or `windows`) and the settings
groups with the extensions they need. `setup/setup.sh` reads it; `--dry-run` and `--list` change nothing.

## Sources

Each extension's Marketplace listing and README, and the VS Code documentation. `make vscode-check` compares the stable version and the minimum
VS Code engine with the Marketplace; `LINKS=1` also checks every source link.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `start` | done | VS Code on Windows, the WSL extension |
| `wsl` | done | the only extension installed on the Windows side |
| `claude-code` | done | |
| `settings` | done | what the profile merges into `settings.json`, with the source of each setting |
| `python` | done | in group `g-python` with `ruff` |
| `eslint` | done | in group `g-node` with `prettier` |
| `kubernetes-tools` | done | in group `g-k8s` with `yaml` and `aks-tools` |
| `terraform` | done | in group `g-iac` with `azure-resources` |
| `containers` | done | in group `g-containers` with `dev-containers` |
| `github-pr` | done | in group `g-git` with `github-actions` and `gitlens` (off by default) |
| `shellcheck` | done | in group `g-files` with `toml` and `editorconfig` |
| `copilot` | done | reference: left out, not installed. VS Code's own AI features: Claude is the assistant here |
| `azure-cli-tools` | done | reference: left out, not installed. The last release was old (see its entry) |
| `docker-extension` | done | reference: left out, not installed. Replaced by Container Tools |
| `azure-terraform` | done | reference: left out, not installed. Preview on the Marketplace |

## Known gaps

- The guide and the profile must agree (`make vscode-validate` fails when an extension is in one and not the other, or when the default or place
  differs). Anything not covered by that check is not verified.
- A setting that is a preference of the author, not a recommendation of the extension, says so in its entry.
- The setup script was tested against a stand-in for VS Code, not on every machine.

## Decisions

- An install counts as done only when the CLI says "successfully installed" or "is already installed". Reason: grepping for "error" marked every
  extension failed once, because Node's deprecation warnings contain the word (PR #22).
- The script never rewrites a settings file that has comments, and backs up before it writes.
- Pick a working Python in the setup script (PR #24). Reason unconfirmed beyond the commit title.
- Versions are stable Marketplace builds: the Marketplace lists a pre-release first.

## Updating

To add an extension: look it up on the Marketplace (id, newest stable version and date, minimum VS Code, pack and dependencies, licence), read its
README, add an entry with `extension` and `track.marketplace`, add it to `setup/profile.json` with the same `on` and `where`, add a settings group if
it needs one, then `make vscode-build` and `setup/setup.sh --dry-run` and `--list`. Refresh with `make vscode-check`.
