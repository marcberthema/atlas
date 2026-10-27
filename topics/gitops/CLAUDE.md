# GitOps (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/gitops/`.

Same shape as the other topics: `data/gitops.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/gitops/index.html` with `templates/index.html`. Python 3 standard library only.

`data/gitops.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md` for the format. `scripts/validate.py` (`make validate`)
checks it. Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: open source or free tools only. Argo CD is the main subject, then Flux, then short references for other operators
(name, start date, status). Helm and Kustomize are covered in depth, with short references for alternatives. A paid product
is left out unless it is an alternative that is a CNCF project.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. `started` is only `confirmed` when an announcement or release gives the date, not when it is a
repository creation date.

Refreshing: `make check` lists what changed (releases, archived repositories, CNCF levels; `LINKS=1` for source links) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every new entry.

Paid products: the group `paid` (Other tools tab) lists a few commercial products so the reader knows they exist. Each is a `ref` entry that says what the vendor's own
page says, nothing more, and names its closest open source alternative in `compare` (an entry id in this topic). No prices unless the page shows them, and say they change.
