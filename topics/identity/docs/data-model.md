# Data model

`data/identity.json` is the only place content lives. `make validate` (`scripts/validate.py`) checks it.

## Top level

| Key | Meaning |
|---|---|
| `title`, `intro`, `scope` | Page heading, one line of what it covers, and the open source / free rule. |
| `checked` | Date of the last research pass (YYYY-MM-DD). No entry may be checked after it. |
| `groups` | `id`, `label`, `about`. Display order. |
| `entries` | One per tool or idea (below). |
| `comparisons` | Tables. `columns` are labels. A row has `cells` (one per column) and either `label` (free text) or `entry` (an entry id, shown as a link). |

## An entry

| Field | Meaning |
|---|---|
| `id`, `name`, `group`, `summary` | `group` is a group id. `summary` is one line. |
| `level` | `deep` (own sections, in depth), `overview`, `ref` (name, dates, status, a few lines). |
| `status` | `active`, `inactive` (a judgement, say why in `notes`) or `archived`. |
| `started` | `date` (or `unconfirmed`), `basis` (what the date is: first release, repository created, ...), `confirmed`. Repository creation dates are not announcements, so they stay `confirmed: false`. An RFC is dated by month, so a confirmed `date` may be `YYYY-MM`, or `YYYY` for a book. |
| `cncf` | `level` (`graduated`, `incubating`, `sandbox`, `none`) and `text` with the dates from cncf.io. |
| `license`, `maintainer` | SPDX id as GitHub reports it. `maintainer` is optional. |
| `version` | Required, and shown in the dialog: `name`, `analysed` (the version the content was written against), `released` (its date), `docs` (what the text was read from), `checked` (date). |
| `track` | Input to `make check`: `github` (owner/repo), optional `tag` (regex a release tag must match, for repositories that also publish API or chart tags) and `cncf` (slug in cncf.io/projects/<slug>). |
| `links` | Where to go next, required: `label` and `url` (https). Project page, documentation, install guide, CLI and API references, repository, releases, whichever exist. Unlike `sources` these are not what the text was written from, so they carry no date. |
| `sections` | `title` and `items` (plain text lines). |
| `compare`, `related` | `with` / entry ids that must exist. |
| `notes` | Unconfirmed claims and caveats, shown in a separate block. |
| `sources` | Every page the entry was written from: `label`, `url` (https), optional `date` when the page shows one. The page prints "no date on page" otherwise. |

## Rules

- Versions: `analysed` is the latest release when the page was checked. Docs pages that show no version are read from "stable" or "latest"; say so in `docs` or `notes`.
- Only open source or free tools. A paid product appears only as an alternative that is a CNCF project.
- Dates, CNCF status and versions come from the project's site, cncf.io or the GitHub release. Anything else goes in `notes` as unconfirmed.

## Update check

`make check` (`scripts/check_updates.py`) reads, and never writes, the data. For each entry with a `track` it compares the highest
non-prerelease GitHub release with `version.analysed`, the archived flag with `status`, and the CNCF level with `cncf.level`.
`LINKS=1` also fetches every source and link url, `ONLY=<id>` limits it to one entry, `STRICT=1` exits 1 on any difference. Set
`GITHUB_TOKEN` to avoid the 60 requests an hour limit. A difference is a prompt to review the entry: update `version`, the facts
that changed and `checked` together.

## Learning layout

Sections can carry a `part` (overview, use, run, reference) and items can be text, `code` (fetched by `match`, see `make examples`), `table`, `callout`, `cards`, `checklist` or `diagram`.
The page is shared with the other topics, so the full format is documented once, in `topics/gitops/docs/data-model.md`. A short entry has no `part`.
