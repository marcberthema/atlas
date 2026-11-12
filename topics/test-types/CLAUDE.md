# Test types (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/test-types/`.

Same shape as the Terraform, GitOps and Certificates topics: `data/test-types.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/test-types/index.html` with the shared page (`shared/topic.html`) and `templates/view.json`. Python 3 standard library only.

`data/test-types.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md`. `scripts/validate.py` (`make validate`) checks it.
Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: see `docs/spec.md`, the plan this topic is built from. Read it first and change it in the same commit as the data. Format: `docs/topic-spec.md`.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. `started` is only `confirmed` when an announcement or release gives the date, not when it is a repository creation date.

Refreshing: `make check` lists what changed (releases, archived repositories, CNCF levels; `LINKS=1` for source links) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every entry that has a GitHub repository.

Code examples are fetched, never pasted: give the source page and a `match` string, run `make examples`, and check the result on the page.
HCL, workflow files and other non-shell code use `lang: text` when the shared page does not know the language (it knows yaml, shell and text).
