# Architecture and design patterns (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/patterns/`.

Same shape as the GitOps topic: `data/patterns.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/patterns/index.html` with `templates/index.html`. Python 3 standard library only.

`data/patterns.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md` for the format. `scripts/validate.py` (`make validate`)
checks it. Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: Reference cards for how software is split by structure and responsibility: application structure, distributed styles, resilience and cloud patterns and the classic 1994 patterns. No code. A pattern is an idea, so there is no release to check: the version shown is the date of the page the card was written from.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. For a concept the version is the page it was read from and that page's date. `license` is `n/a` for a concept,
and the validator then does not ask for a `track`. `started` is only `confirmed` when the source gives the date.

The page has one tab per main entry (the `TABS` list in `templates/index.html`, ids must be entry ids), then the rest and Compare.

Refreshing: `make check` lists what changed for the entries that have a `track` (releases, archived repositories, CNCF levels; `LINKS=1` for source and link urls) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every entry that has a GitHub repository and releases.
