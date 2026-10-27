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
| `track` | Input to `make check`: `github` (owner/repo), optional `tag` (regex a release tag must match, for repositories that also publish API or chart tags) and `cncf` (slug in cncf.io/projects/<slug>). |
| `links` | Where to go next, required: `label` and `url` (https). Project page, documentation, install guide, CLI and API references, repository, releases, whichever exist. Unlike `sources` these are not what the text was written from, so they carry no date. |
| `sections` | `title` and `items`. An item is a plain text line (a bullet), or an object (see Learning layout below). |
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

An entry whose sections all have a `part` is drawn as a page to learn from: a jump bar, then Overview, Use it, Run it and a collapsed Reference. The five tab
entries use it. A short entry (an overview or a reference card) has no `part`: it gets the same header and the same item types, with its sections one
after another and no jump bar. Either every section of an entry has a `part` or none does.

| Section field | Meaning |
|---|---|
| `part` | `overview` (what it is), `use` (typical use, step by step), `run` (owning and operating it) or `reference` (lookup tables, collapsed). |
| `step` | Optional number shown as a step badge (used in `use`). |
| `icon` | Optional icon name from the sprite in the template (book, play, server, list, box, sync, layers, clock, grid, bell, key, users, globe, up, eye, wrench, shield, file, scale, download, login, check). |
| `intro` | Optional lead sentence. |

| Item | Fields |
|---|---|
| text | A string, or `{text, unconfirmed}` to show an unconfirmed badge with the reason next to the claim. |
| `code` | `title`, `lang` (yaml, shell, text), `source` (`label`, https `url`) and `match`: a string, or a list for several examples from the same page in order. `make examples` fetches the code block that contains each string (the shortest if several do) into `data/examples.json`, which the build reads; never edit that file. `make check` reports examples that changed upstream or can no longer be found. Text written in the data (`body`) is only allowed with a `note` saying why it cannot be fetched. |
| `table` | `columns`, `rows` (same length as columns), optional `caption`. |
| `callout` | `kind`: gotcha, default, prod or tip; `text`; optional `title`, `unconfirmed`. |
| `cards` | `cards`: `icon`, `title`, `text`. |
| `checklist` | `items`. |
| `diagram` | Same spec as the topologies diagrams: `alt`, `caption`, `w`, `h`, `boxes`, `nodes`, `links`. |

Text can use `code` in backticks and links as [label](url), where the url is https or a relative page of this site.
`make check` also checks the code examples (scripts/examples.py). `make check LINKS=1` fetches every source url.
