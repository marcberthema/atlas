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
| `cloud_native_scale` | The levels (`native`, `partly`, `not`) with a label and the criteria for each. |
| `cost_scale` | The cost levels (`free`, `free-tier`, `trial`, `partial`, `paid`) with a label and description. |
| `comparisons` | Groups of services that solve the same problem: `id`, `title`, `question`, `status`, `note`, and `members` (`services`, `audience`, `choose_when`). |
| `terraform_providers` | Per provider: registry namespace and name, `latest_version`, `changed_at`, `docs_url`. `azapi` is the fallback. |
| `services` | Full entries (below). |
| `stubs` | Out-of-scope services (id, name, tier, category) that edges point at. No content. |
| `edges` | `from`, `type`, `to` (service or stub ids), `note`, `origin`, `status`. |

## A service

| Field | Written by | Meaning |
|---|---|---|
| `tracking` | human | Inputs to the check: `learn_urls`, `terraform` (provider, kind `resource`/`data_source`, type), `arm_types`. |
| `fetched` | pipeline or AI ingestion | Content from Microsoft or the registry: `purpose`, `facts`, `cost`, and `terraform.resources` (`type`, `exists`, `since`), `terraform.arm_types`. |
| `manual` | human | Overrides. Allowed keys: `purpose`, `facts`, `cost`, `cloud_native` (`level`, `note`), `terraform` (`gaps`, `note`, `status`). |
| `review` | human | `status` `unconfirmed` or `verified`, plus a note. |
| `freshness` | pipeline | `status`, `changed_at`, and per Learn URL: `http_status`, `ms_date`, `updated_at`, `latest_hash`, `reviewed_hash`. |

### Cloud native rating

`cloud_native.level` is one of the levels in `cloud_native_scale`, with a one-line `note`. It is a human judgement
against the scale's criteria, not a Microsoft label, so it lives in `manual` and is only set after the user confirms.
A service with no rating resolves to `unrated`.

### Cost

`cost` answers "can I try this without paying?" with a `level` from `cost_scale`, a one-line `note` (what is free and its
limits), `billed` (what still costs money), `sources` (https urls), `checked_at`, and `confirmed`. `confirmed` is `true` only when
the claim was read on the source page; otherwise it is `false` and the page shows a `?`. Pricing pages on azure.microsoft.com
are often not readable by the checker, so the free services page and Learn are the usual sources. Learn urls used for a cost
also go in `tracking.learn_urls`. Free offers change often: re-check `checked_at` before relying on a limit.

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

Snapshots are **local only** (git-ignored): they are verbatim Microsoft Learn text, which this repo doesn't redistribute. The
daily job still detects changes by hash. In a fresh clone run `make check` first to create the `latest` files; a service
without a local `reviewed` snapshot is reported as having no baseline, and the agent reads the whole current page instead.

### Terraform status (derived)

Versions are **provider** versions (azurerm, azuread, azuredevops, azapi), not Terraform core.

| Status | Rule |
|---|---|
| `full` | Set only by a human: `manual.terraform.status`. Shown as `full*` when `gaps` is non-empty. |
| `partial` | `manual.terraform.gaps` is non-empty, or some tracked resources do not exist in the latest docs. |
| `listed` | Every tracked resource exists, but nobody has confirmed the whole service is covered. |
| `azapi-only` | No tracked resource exists but an ARM type is tracked, so use `azapi_resource`. |
| `none` / `unknown` | Nothing tracked and no ARM type / nothing tracked at all. |
| `unchecked` | Not checked yet. |

`since` on a resource is the earliest provider version whose changelog lists it as a new resource or data source.
`null` means no such entry was found: it predates the changelogs, or was logged in another format. `first_supported`
and `fully_supported_since` are only set when every found resource has a `since`.

### How Terraform coverage is judged

Compare the configuration the Azure REST API accepts for the service (the OpenAPI spec in `Azure/azure-rest-api-specs`)
with what the provider resource accepts (its documented arguments):

- `full`: every configurable setting can be set through the provider.
- `full*`: `full` with a few `gaps`: the common uses are covered and the rest only through the API. The user decides when a gap is minor.
- `partial`: a meaningful part of the settings can only be set through the API; each goes in `gaps` with the azapi alternative.
- `none` / `azapi-only`: the provider has no resource for the service.

End-user actions (backup, restore, purge, recover, rotate now) are not configuration and never count as gaps.
Content you can manage in the service (secrets, keys, items in a store) is not a gap either: it goes in `content` as
"you can also manage this with ...". `compared` records the API version and provider version the judgement is based on.

`gaps` entries are `{ "what": "...", "alternative": "..." }`, for example a feature that needs `azapi_resource`.
