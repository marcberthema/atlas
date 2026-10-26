# Azure with Terraform (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run the commands below from `topics/azure/`.

A day-to-day reference for what an Azure service provides, what it requires, how it relates to other
services, and how to build it with Terraform. Personal study project, built with AI assistance.
Scope for now: tier 0 ("always there") and tier 1 ("core") services only.

---

## Architecture: data in, view out

```
Learn + Terraform Registry  ->  data/services.json  ->  scripts/build.py  ->  dist/azure/
```

- `data/services.json` is the only place content lives. See `docs/data-model.md` for the format.
- `dist/azure/services.resolved.json` is the stable contract for any front end (layers merged, Terraform status derived).
- `templates/index.html` is the view. It reads only the resolved JSON. Changing the look or the tech stack must
  never require touching the data or the scripts.
  It holds two views of the same data, Simple (default) and Full, toggled in the page. Elements only the Full view
  needs carry the `full` class.
- `scripts/` is Python 3, standard library only. No pip dependencies.
- `azure-services.html` is the original single-file page. Frozen reference: do not edit or build on it.

```
topics/azure/
  CLAUDE.md  README.md  Makefile
  data/services.json            source of truth
  docs/data-model.md            schema and merge rules
  scripts/model.py              load/save, merge, Terraform status
  scripts/validate.py           consistency checks
  scripts/check_updates.py      daily check (no AI) and `ack`
  scripts/build.py              JSON -> ../../dist/azure/ (adds the Atlas banner via ../../shared/atlas.py)
  templates/index.html          the view
  azure-services.html           frozen reference
```

Do not add dependencies, a framework or external scripts or fonts without asking. The generated page must work from `file://`.

---

## Data layers

Per service: `tracking` (inputs the check uses), `fetched` (from Microsoft or the registry), `manual` (human
overrides, always win), `review`, `freshness` (written by the pipeline). Rules:

- The pipeline never writes `manual`, `review`, `reviewed_hash` or `tracking`.
- Content from AI ingestion goes into `fetched`, with its Learn URL in `tracking.learn_urls`.
- `data/snapshots/` is local only and git-ignored (verbatim Learn text must not be committed). Do not hand-edit `freshness`, `data/snapshots/` or `fetched.terraform`; `make check` and `make ack` own them.
- After updating a service from its Learn page, run `make ack SERVICE=<id>`, and set `review.status` to
  `verified` only for facts actually checked against Learn.
- Currently every entry is `unconfirmed`: it was imported from the first hand-drafted page.

---

## Conventions

- **Services, not products.** "Service" is Microsoft's term and means a type (Virtual Machines).
  A "resource" is an instance (`myvm`). Keep the distinction in all copy. Marketplace and third-party
  offerings, Microsoft 365 and Dynamics are out of scope.
- **Every edge must name an existing service or stub id.** `make validate` checks it.
- **Edge direction reads left to right:** `from requires to` means "from requires to". Pick the
  type by the real relationship, not by convenience:
  - `contains`: B lives inside A (resource group contains a VM).
  - `requires`: A cannot exist without B (VM requires a NIC).
  - `optional`: A can use B but does not need it.
  - `access`: A authenticates or authorizes against B.
  - `network`: A is reached or connected through B.
  - `sends`: A sends data (logs, metrics, events) to B.
  - `protects`: A secures or backs up B.
  - `enforces`: A checks or enforces B (Azure Resource Manager enforces Azure Policy). Do not use
    `requires` for this; it reads backwards.
- **Cloud native:** a 3-level judgement (`native`, `partly`, `not`) against the criteria in `cloud_native_scale`, stored in
  `manual.cloud_native` with a note. It is not a Microsoft label: never set it without the user's answer. Services that
  solve the same problem are grouped in `comparisons` (first one: observability) and shown on the Compare tab.
- **Terraform:** versions mean *provider* versions (azurerm, azuread, azuredevops, azapi), never Terraform core.
  `full` is a human judgement set in `manual.terraform.status`; the pipeline can only prove a resource exists
  (`listed`). Record real gaps in `manual.terraform.gaps` with the azapi alternative; `full` with gaps shows as `full*` (common uses covered). Judge by comparing the API spec with the azurerm docs (see `docs/data-model.md`); secrets, keys and other content go in `content`, not `gaps`. Name resource types
  exactly as in the registry.
- **Cost:** `fetched.cost` says whether a service can be tried for free (`cost_scale` in the data). Set `confirmed` to `true`
  only for claims read on the source page. Free offers change often, so never add a limit from memory.
- **Accuracy over completeness.** Do not add a fact or edge from memory when unsure. Verify against
  Microsoft Learn (learn.microsoft.com) and say "unconfirmed" in the note if it can't be verified.
  Retirement dates change often; always check the official retirement announcement before adding one.
- **Keep text short and plain.** One line per service purpose. Facts only where a common confusion exists
  (RBAC versus Policy, Key Vault access policy versus RBAC, and so on).
- **Public and general only.** See the root `CLAUDE.md`: nothing is ever based on a current or past employer or client, only public Azure knowledge.
- **Version visible.** Each detail panel has a "Based on" section: the Learn pages with their dates and the Terraform provider
  and API versions. Keep `tracking.learn_urls` and `manual.terraform.compared` accurate so it stays true.
- **Style:** match the existing code. Same naming, same comment density.

---

## Commands

```bash
make validate   # must report bad 0
make build      # validate + generate ../../dist/azure/
make check      # network: Learn hashes + Terraform registry/changelogs; writes data/services.json
make ack SERVICE=<id>
make stale      # what needs review; writes review/PROMPT.md (git-ignored) for an agent
make update     # check + build
```

From the repo root use `make azure-<target>`, and `make serve` there to preview the whole site.

```bash
```

## Workflow

1. Describe the change (add a service, fix a relationship, refresh a stale service).
2. Claude edits `data/services.json` (or the template), runs `make build`, and checks `dist/azure/index.html` in a browser (`make serve` at the repo root).
3. Commit after each coherent change, with a message saying what was added or corrected. Commit `dist/` with it.
4. The daily GitHub Action (`.github/workflows/daily-check.yml` at the repo root) commits freshness, snapshots and Terraform status updates itself.
5. Reviews run from `review/PROMPT.md` (`make stale`): one branch `review/<date>`, one commit per service, a PR to
   `main` after the user confirms. Never push or open a PR without asking.

Onboarding tier 2 and 3 later: add the service entries, remove the matching stub, and extend `scope.tiers`.

---

## Feedback Style

Be direct. If a relationship, claim or retirement date is uncertain, say so plainly rather than
guessing. Flag errors in existing entries when you notice them.
