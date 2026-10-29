# Workstation setup (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/workstation/`.

Same shape as the Certificates topic: `data/workstation.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/workstation/index.html` with the shared page. Python 3 standard library only.

`data/workstation.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md` for the format. `scripts/validate.py` (`make validate`)
checks it. Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: the baseline to take a new Windows PC to a working state. Windows keeps the browser and Windows-only apps; development happens in WSL 2
with the latest Ubuntu LTS. In order: WSL, Windows Terminal, the shell (zsh), Python (uv), Node (fnm, pnpm), Kubernetes tools, Terraform,
the Azure CLI, containers, git and Claude Code. Each step says how to install, how to update and what to check. Free to use tools first; a tool
with a paid plan or a non open source licence says so and names the free alternative.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. A tool installed from Ubuntu's archive records the Ubuntu 26.04 package version and the upstream release in `docs`.
`started` is only `confirmed` when an announcement or release gives the date, not when it is a repository creation date.

The page has one tab per main entry (`templates/view.json`, ids must be entry ids), then Other tools and Compare.

Refreshing: `make check` lists what changed (releases, archived repositories, CNCF levels; `LINKS=1` for source and link urls) and writes nothing.
Several tools release weekly (uv, pnpm, mise, Claude Code, kubectl patches): update `version` and `checked`, and re-read the page only when
a minor or major version changed. When Ubuntu ships a new LTS, re-check every apt-based step (repository lines name the release codename).

Page: this topic uses the shared page (`shared/topic.html`). Tab entries use the learning layout (parts, steps, tables, callouts, cards,
checklists, fetched code examples: see `topics/gitops/docs/data-model.md`); short entries are flat. Examples are fetched by reference
(`make examples`), never pasted: install scripts change, so the page shows the vendor's current command.
