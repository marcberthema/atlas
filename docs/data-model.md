# Data model

`data/services.json` is the single source of truth. Nothing else holds content. The page is one
possible view of it; to use a different look or stack, read `dist/services.resolved.json` (same data,
layers already merged, Terraform status derived) or merge the layers yourself with the rules below.

## Top level

| Key | Meaning |
|---|---|
| `schema_version` | Integer, bump on breaking changes. |
| `scope` | Which tiers have full entries (`tiers: [0, 1]`). |
| `tiers`, `categories` | Labels and display order. |
| `edge_types` | `type`, `out` and `in` wording, `meaning`. Edge `[A, requires, B]` reads "A requires B". |
| `edge_group_order` | Order of relationship groups on a card. |
| `terraform_providers` | Per provider: registry namespace and name, `latest_version`, `changed_at`, `docs_url`. `azapi` is the fallback. |
| `services` | Full entries (below). |
| `stubs` | Out-of-scope services (id, name, tier, category) that edges point at. No content. |
| `edges` | `from`, `type`, `to` (service or stub ids), `note`, `origin`, `status`. |

## A service

| Field | Written by | Meaning |
|---|---|---|
| `tracking` | human | Inputs to the check: `learn_urls`, `terraform` (provider, kind `resource`/`data_source`, type), `arm_types`. |
| `fetched` | pipeline or AI ingestion | Content from Microsoft or the registry: `purpose`, `facts`, and `terraform.resources` (`type`, `exists`, `since`), `terraform.arm_types`. |
| `manual` | human | Overrides. Allowed keys: `purpose`, `facts`, `terraform` (`gaps`, `note`, `status`). |
| `review` | human | `status` `unconfirmed` or `verified`, plus a note. |
| `freshness` | pipeline | `status`, `changed_at`, and per Learn URL: `http_status`, `ms_date`, `updated_at`, `latest_hash`, `reviewed_hash`. |

### Merge rule

`resolved = deep_merge(fetched, manual)`: dicts merge key by key, anything else (strings, lists) in
`manual` replaces the `fetched` value. A re-fetch never touches `manual`.

### Freshness

Each Learn source has `latest_hash` (what the pipeline saw last) and `reviewed_hash` (what a human last
accepted). Service status is the worst of its sources:

- `error`: the page could not be fetched (not HTTP 200).
- `stale`: `latest_hash` differs from `reviewed_hash`, so the docs changed since review.
- `unreviewed`: no `reviewed_hash` yet.
- `current`: hashes match.

`make ack SERVICE=<id>` copies `latest_hash` to `reviewed_hash` after you have re-read the page and updated the entry.

Dates called `changed_at` move only when the recorded values change, so an unchanged day leaves the file untouched
(no daily commit noise, and review branches don't conflict with the daily job).

### Snapshots

`data/snapshots/<service-id>/<page>.latest.txt` is the page text the pipeline last saw; `.reviewed.txt` is the text
at the last `make ack`. `make stale` diffs the two to show what changed.

### Terraform status (derived)

Versions are **provider** versions (azurerm, azuread, azuredevops, azapi), not Terraform core.

| Status | Rule |
|---|---|
| `full` | Set only by a human: `manual.terraform.status`. |
| `partial` | `manual.terraform.gaps` is non-empty, or some tracked resources do not exist in the latest docs. |
| `listed` | Every tracked resource exists, but nobody has confirmed the whole service is covered. |
| `azapi-only` | No tracked resource exists but an ARM type is tracked, so use `azapi_resource`. |
| `none` / `unknown` | Nothing tracked and no ARM type / nothing tracked at all. |
| `unchecked` | Not checked yet. |

`since` on a resource is the earliest provider version whose changelog lists it as a new resource or data source.
`null` means no such entry was found: it predates the changelogs, or was logged in another format. `first_supported`
and `fully_supported_since` are only set when every found resource has a `since`.

`gaps` entries are `{ "what": "...", "alternative": "..." }`, for example a feature that needs `azapi_resource`.
