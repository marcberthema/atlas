# Azure with Terraform: spec

Status: published (IaC family). Data checked by the daily pipeline. Reconstructed from the data, the topic's `CLAUDE.md` and git history, not written
before the content: reasons that the history does not record are marked "reason unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

A day-to-day reference for what an Azure service provides, what it requires, how it relates to other services, what it costs to try, and how to
build it with Terraform. A personal study project built with AI assistance.

## Scope

- In: tier 0 ("always there") and tier 1 ("core") services: 42 services in 9 categories, plus 23 stubs for the tier 2 and 3 services that an edge
  points at.
- Out: tier 2 and 3 services (adjacent, long tail), Marketplace and third-party offerings, Microsoft 365 and Dynamics.
- Services, not products: a service is a type (Virtual Machines), a resource is an instance. Keep the distinction in all copy.
- Terraform here means provider versions (azurerm, azuread, azuredevops, azapi), never Terraform core. The Terraform CLI has its own topic.

## Layout

Archetype: cloud service map. This topic does not use the shared page: `templates/index.html` reads `dist/azure/services.resolved.json`, the stable
contract for any front end. Two views of the same data, Simple (default) and Full, plus a Compare tab. Data lives in `data/services.json`:
services, stubs, 173 edges (typed relationships: contains, requires, optional, access, network, sends, protects, enforces), tiers,
categories, a cloud-native scale, a cost scale and two comparisons (which monitoring service fits, where a workload should run).
`azure-services.html` is the original single-file page, kept as a frozen reference.

## Sources

Microsoft Learn for each service (URLs in each service's `tracking.learn_urls`) and the Terraform Registry for provider resources. A daily GitHub
workflow runs `make check` and `make build` with no AI: it records whether each Learn page changed since it was last reviewed and which Terraform
resources exist, and commits the result. Learn text is never committed (`data/snapshots/` is git-ignored).

## Coverage

| Item | Status | Notes |
|---|---|---|
| `tier:0` | done | 10 "always there" services |
| `tier:1` | done | 32 "core" services |
| `tier:2` | planned | adjacent services appear only as stubs when an edge points at them |
| `tier:3` | planned | long tail: stubs only |
| `comparison:observability` | done | which monitoring service fits (status unconfirmed) |
| `comparison:compute` | done | where a workload should run (status unconfirmed) |
| `rating:cloud-native` | partial | a judgement stored in `manual.cloud_native`; never set without the owner's answer; the filter is parked until the data is more complete |

## Known gaps

- Every one of the 42 services has `review.status` unconfirmed: the content was imported from the first hand-drafted page and has not been
  verified against Learn. Of the 173 edges, 92 are verified and 81 unconfirmed (origin `learn` or `legacy-import`).
- Terraform status: 37 full, 1 partial, 1 none, 3 unset. `full` is a human judgement; the pipeline can only prove a resource exists.
- Cost claims are set `confirmed` only when read on the source page. Free offers change often, so nothing is added from memory.
- This topic does not use the shared page, so the About window's details switch does not apply, and the Atlas page layout changes (details hidden
  by default, picker tabs) are not available here. Bringing Azure onto the shared page is not scheduled.

## Decisions

- Data in, view out: `services.json` is the only source of content; the page reads only the resolved JSON, so the look or stack can change without
  touching the data (`CLAUDE.md` of this topic).
- Four data layers per service: `tracking`, `fetched`, `manual` (always wins), `review`, plus the pipeline's `freshness`. The pipeline never
  writes `manual`, `review`, `reviewed_hash` or `tracking`.
- Edges name the real relationship (`enforces`, not `requires`, for Azure Policy). `make validate` checks that every edge names an existing service or
  stub.
- Tiers 0 and 1 only. Reason unconfirmed beyond "scope for now".

## Updating

The daily pipeline detects changes; it does not update content. To bring entries up to date: `make stale` lists what needs review and writes
`review/PROMPT.md`, an AI agent updates the service from its Learn page, then `make ack SERVICE=<id>` marks it reviewed. Set `review.status` to
`verified` only for facts actually checked against Learn. Run commands from `topics/azure/` or as `make azure-<target>`.
