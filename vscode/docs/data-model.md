# Data model

The format is the one of the other topics (see `topics/gitops/docs/data-model.md` for sections, parts and item types). This page lists what is
specific to the VS Code setup: one entry per extension, tracked on the Marketplace, and a profile that must agree with the entries.

`data/vscode.json` is the only place content lives. `make validate` (`scripts/validate.py`) checks it.

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
| `started` | `date` (or `unconfirmed`), `basis` (what the date is: first release, repository created, ...), `confirmed`. Repository creation dates are not announcements, so they stay `confirmed: false`. A confirmed `date` may be `YYYY-MM` or `YYYY` when the source gives no day. |
| `cncf` | Required by the shared page, always `{"level": "none", "text": "Not a CNCF project."}` here. |
| `license`, `maintainer` | The licence as the extension's own licence file or repository states it (for an extension with parts under other terms, say so). `maintainer` is the Marketplace publisher. |
| `version` | Required, and shown in the dialog: `name`, `analysed` (the version the content was written against), `released` (its date), `docs` (what the text was read from), `checked` (date). For an extension: the newest **stable** Marketplace version and its date, never a pre-release. |
| `track` | Input to `make check`: `marketplace` (`publisher.name`, an extension tracked on the Marketplace), and/or `github` (owner/repo) with an optional `tag` regex. `cncf` is not used here. |
| `extension` | Required with `track.marketplace`: `id` (same as the track), `engine` (the oldest VS Code the stable build runs on, as the Marketplace writes it, for example `^1.104.0`), and, only if `setup/setup.sh` installs it, `where` (`wsl` or `windows`) and `default` (true or false). |
| `links` | Where to go next, required: `label` and `url` (https). Project page, documentation, install guide, CLI and API references, repository, releases, whichever exist. Unlike `sources` these are not what the text was written from, so they carry no date. |
| `sections` | `title` and `items` (plain text lines). |
| `compare`, `related` | `with` / entry ids that must exist. |
| `notes` | Unconfirmed claims and caveats, shown in a separate block. |
| `sources` | Every page the entry was written from: `label`, `url` (https), optional `date` when the page shows one. The page prints "no date on page" otherwise. |

## Rules

- Versions: `analysed` is the newest stable Marketplace version when the page was checked. The Marketplace lists a pre-release first when there is
  one: skip it (a version property `PreRelease` is `true`). Say in the entry when a pre-release exists beside the stable build.
- Facts come from the extension's README, the VS Code docs or the Marketplace listing. Anything else goes in `notes` as unconfirmed.
- Groups: a group whose id is a tab in `templates/view.json` shows all its entries in full. Entries in `g-more` are the extensions looked at and
  not installed, listed under Not installed; they carry `extension.id` and `engine` but no `where`.
- `started` of an extension is the Marketplace's first published date, so it is never `confirmed`.

## Profile consistency

`scripts/validate.py` reads `setup/profile.json`: every entry with `extension.where` must be in `profile.extensions` with the same `on` (`default`) and
`where`, every extension in the profile must have an entry, and every settings group's `needs` must name an extension in the profile.

## Update check

`make check` (`scripts/check_updates.py`) reads, and never writes, the data. For each entry with `track.marketplace` it compares the newest stable
Marketplace version with `version.analysed` and its minimum VS Code with `extension.engine`; for `track.github` it compares the latest release and
the archived flag. `LINKS=1` also fetches every source and link url, `ONLY=<id>` limits it to one entry, `STRICT=1` exits 1 on any difference.
Set `GITHUB_TOKEN` to avoid GitHub's 60 requests an hour limit (the Marketplace needs none).
