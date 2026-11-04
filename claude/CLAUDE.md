# Claude Code setup (kept in git, not published)

Not an Atlas topic: not in `topics.json`, not in the banner, never deployed, no site. Unlike `workstation/` and `vscode/` it has no JSON data
model or build: `README.md` is the guide and the research, `setup/` is what installs it. The site-wide content rules in the root
`CLAUDE.md` still apply (public sources only, no secrets, every claim linked, version and check date shown, "unconfirmed" when unverified).
Run commands from `claude/` (or `make claude-<target>` from the root).

## Files

- `README.md`: for people. Every tool that was looked at, the verdict, where to use it, the sources, what was verified and what was not.
- `setup/profile.json`: what is on or off. `global` is installed for the account that runs `setup.sh`; `project` is installed into one project by `project.sh`.
- `setup/setup.sh`, `setup/project.sh`, `setup/lib.sh`: read the profile and do it. `--dry-run`, `--list`, `--only <id>`.
- `setup/global-rules.md`: the working rules put in `~/.claude/CLAUDE.md`. `setup/project-rules.md`: the UI rules put in a project's `CLAUDE.md`.
  Both are written between `<!-- atlas claude setup: ... -->` markers, so the rest of the file is kept and a re-run replaces only the block.
- The status line is not copied here: `setup.sh` installs `../workstation/setup/claude-statusline.py`. Change it there.

## Rules

- A plugin enters the profile only after its repo, license, install command and version were read from the source, not from a blog.
  Install in a throwaway home first: `HOME=<scratch dir> setup/setup.sh` (the plugin commands use `$HOME/.claude`), never on the real account.
- `claude plugin details <plugin>@<marketplace>` prints the projected token cost. Record "always-on" in the README table, and re-measure on update.
  A plugin that adds more than a few hundred tokens to every session needs a reason; it is `on: false` otherwise.
- Pro plan constraint: no paid API keys, no extra subscriptions. A tool that routes to other providers is a fallback to use on purpose,
  never the default (see "Later" in the README).
- The scripts must stay idempotent (check, then act), never overwrite `settings.json` keys they do not own, and back up a file before the
  first write (unless git tracks it: git is the backup). Plugin installs go through `claude plugin ...`; never edit `enabledPlugins` by hand.
- The repository is public: the profile and the rules blocks hold no secrets, paths or private names.
- Plugins are cloned over SSH by the Claude CLI; the account needs a GitHub key or the clone fails.

## Refreshing

Versions move weekly. For each row of the README table: read the repo's latest release or `plugin.json`, run `claude plugin details`, update the
version, the always-on cost and the check date together. Re-read the README of a tool only when its major version changed.
