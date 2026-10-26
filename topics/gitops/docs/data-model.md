# Data model

`data/gitops.json` is the only place content lives. `make validate` (`scripts/validate.py`) checks it.

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
| `started` | `date` (or `unconfirmed`), `basis` (what the date is: first release, repository created, ...), `confirmed`. Repository creation dates are not announcements, so they stay `confirmed: false`. |
| `cncf` | `level` (`graduated`, `incubating`, `sandbox`, `none`) and `text` with the dates from cncf.io. |
| `license`, `maintainer` | SPDX id as GitHub reports it. `maintainer` is optional. |
| `version` | Required, and shown in the dialog: `name`, `analysed` (the version the content was written against), `released` (its date), `docs` (what the text was read from), `checked` (date). |
| `sections` | `title` and `items` (plain text lines). |
| `compare`, `related` | `with` / entry ids that must exist. |
| `notes` | Unconfirmed claims and caveats, shown in a separate block. |
| `sources` | Every page the entry was written from: `label`, `url` (https), optional `date` when the page shows one. The page prints "no date on page" otherwise. |

## Rules

- Versions: `analysed` is the latest release when the page was checked. Docs pages that show no version are read from "stable" or "latest"; say so in `docs` or `notes`.
- Only open source or free tools. A paid product appears only as an alternative that is a CNCF project.
- Dates, CNCF status and versions come from the project's site, cncf.io or the GitHub release. Anything else goes in `notes` as unconfirmed.
