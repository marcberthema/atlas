# Visual Studio Code setup (kept in git, not published)

Not an Atlas topic, like `workstation/`: it is not in `topics.json`, not in the banner or the landing page, and never deployed. It keeps the
same data model, checks and shared page so it looks the same. The site-wide content rules in the repo root `CLAUDE.md` still apply.
Run commands from `vscode/` (or `make vscode-<target>` from the root).

`data/vscode.json` is the only place content lives, `scripts/build.py` turns it into `site/index.html` (outside `dist/`) with the shared page
and a banner that names only this page. Links to Atlas topics and to the Workstation guide are written as they resolve from `site/`.
Python 3 standard library only.

Scope: VS Code on Windows, working in WSL Ubuntu: the extensions that fit the toolchain of the Workstation guide (Claude Code, Python with uv,
Node with pnpm, Kubernetes, Terraform, Azure, Docker, GitHub, shell scripts), how each is configured where it needs it, and a script that
does both from a profile. It is an evolving document: add an extension when a tool is added to the workstation.

## What the files are

- `data/vscode.json`: one entry per extension (`level: deep`, in a group that is a tab), plus entries for the guide itself (`start`, `wsl`,
  `claude-code`, `settings`) and `ref` entries in the group `g-more` for what was looked at and left out. See `docs/data-model.md`.
- `setup/profile.json`: which extensions are on and where they install (`wsl` or `windows`), and the settings groups merged into the user
  `settings.json`, each with the extensions it `needs`.
- `setup/setup.sh`: reads the profile and does it. It is the one place commands are written out, rather than fetched. `--dry-run` and `--list`
  change nothing.

The guide and the profile must agree: `make validate` fails when an extension is in one and not the other, or the default or place differs.

## Rules

- Versions are the newest **stable** Marketplace build, never a pre-release (the Marketplace lists a pre-release first). `version.analysed` is
  that version and `extension.engine` is the oldest VS Code it runs on. `make check` compares both with the Marketplace and writes nothing.
- Every setting in the profile comes from the extension's own README or the VS Code docs. Say where in the entry. A setting that is a
  preference of ours, not a recommendation of the extension, says so.
- Facts about an extension come from its README, the VS Code docs or the Marketplace listing, with the page linked in `sources`. Say
  "unconfirmed" in `notes` when it can't be verified. Do not describe what an extension does from memory.
- Code examples are fetched, not pasted (`make examples`): give the page and a match string, and check the fetched block is the one you meant.
  A match string that is too loose picks a smaller block: check the result in `data/examples.json`.
- The setup script must stay idempotent, must never rewrite a settings file that has comments, and must back up before it writes.
  Test it against a stand-in for VS Code before a real run: see the cases in the commit that added it.

## Adding an extension

1. Look it up on the Marketplace: id, newest stable version and date, minimum VS Code, pack and dependencies, licence. Read its README.
2. Add an entry to `data/vscode.json` with `extension` (`id`, `engine`, and `where`, `default` if the script installs it) and
   `track.marketplace`. Put it in a group that is a tab, or in `g-more` if it is not installed.
3. Add it to `setup/profile.json` with the same `on` and `where`.
4. If it needs configuring, add a settings group with `needs`, using the README's own settings.
5. `make vscode-build`, then `setup/setup.sh --dry-run` and `--list`.

## Refreshing

`make check` lists the extensions whose stable version or minimum VS Code changed (`LINKS=1` also checks every source and link).
Update `version`, `extension.engine`, and the facts that changed together, and re-read the README when a major version changed.
The Marketplace metadata is read from its public query API; nothing needs an account.
