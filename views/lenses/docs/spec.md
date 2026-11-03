# Lenses and the organization level: spec

Status: approved by the owner on 2026-11-03 (location accepted, security and storage roles added to the first batch). Data, validator and page are built; the data wording and the place of `siem` and `storage` are not yet reviewed by the owner. The visual reference is the mockup `docs/mockups/lenses.html`
(sample text, not verified). Format: `docs/topic-spec.md`, adapted for a view that has its own catalogue.

## Purpose and audience

Answers "where does this service go?" for someone who meets a service they do not know (Kafka, Redis, a bastion, a load balancer) or who wants
the high-level picture of how an application and its surroundings connect. It files every product under a role ("message broker", "cache"),
and shows the role on one base picture of an application. A lens changes what is highlighted, a stack changes the labels, and the picture
never moves. A second view shows what sits above the resource group: tenant, management groups, subscriptions and the services tied to each.

## Scope

- In: roles (what a thing is for, including a security information and event management role and a storage role), where a role usually sits and what it talks to, products per stack (generic, Azure, open source), five lenses
  (application, network, infrastructure, security, monitoring), the organization level for Azure, an A-Z list and a search over roles and products.
- Out: subnets, address ranges, sizing, cost, regions and high-availability layouts. Another stack (AWS, vSphere, Dynatrace, and so on) until the
  generic and Azure ones are checked: they are listed as planned. Step-by-step design for a specific product (that is a topic). Anything taken
  from a company, a client or a private architecture.
- Rule that decides: a role is in when it has inputs and outputs and a job of its own. What only defines or restricts another object (role
  assignments, resource groups, tags, route tables, policies) is a setting: it is not drawn, but is listed under the lens as "not drawn". One
  exception: traffic filter rules, shown as a shield on a hop, because the owner expects to see where filtering happens.
- Placements are general knowledge, taken from public reference architectures. Each carries a `basis`: a source page, or the word `judgement`.
- Version: roles and placements have no version. The version shown is the date the sources were read (`checked`). Products are named without
  versions. A product whose name or availability changes is `unconfirmed` until the page is re-read.

## Layout

Archetype: its own page, not the shared topic page. One page, `/lenses/`, in the Views family. Controls in a row: View (Lenses, Organization,
A-Z), Lens (disabled outside the Lenses view), Stack, and a search box.

| View | Holds |
|---|---|
| Lenses | The base picture: five bands (request path, supporting services, background work, network and access, operations). Roles are boxes with an icon. A lens highlights its roles and fades the others. A role opens a panel: what it is, where it sits, why, what it talks to, which lenses show it, and the products for the chosen stack |
| Organization | Nested boxes: tenant, management groups, subscription, resource groups. Services sit on the level they apply to, plus "spans every level" and "outside the subscriptions". A button leads from a resource group to the Lenses view |
| A-Z | Every role and organization-level service, grouped, with icon and lens chips |

Stacks: Generic (no products, the role names only), Azure, Open source; AWS is shown as "soon". The Organization view is Azure-shaped: Generic
shows the concept names ("Account", "Account groups"), which are a mapping and are `unconfirmed`.
Search matches role names, product names and organization-level names, and a product found under two roles lists both (Elasticsearch: search
index and telemetry store). Keyboard: every box and badge is a button with a visible focus ring; colour is never the only signal (a faded box is also dashed).

## Sources

Placement and roles: the Microsoft Cloud Adoption Framework and Azure Architecture Center (hub-and-spoke, landing zones, reference
architectures), the Azure Well-Architected Framework, and the product documentation of each open source product. Services and scopes: Microsoft
Learn (the Azure topic already tracks 42 services with their Learn pages, including the tier 0 "always there" services). Products are
checked against their own documentation.
Re-check: each role and organization item carries `sources` (urls) and `checked`. `make lenses-check` (`shared/lenses_check.py links`) reports products
whose page no longer resolves, and roles whose Azure service ids are missing from `topics/azure/data/services.json`.

## Data model

`views/lenses/data/lenses.json`, one file, `groups` kept out of it on purpose:

```
{ "title", "checked", "stacks": [{"id","label","status"}],
  "lenses": [{"id","label","about","not_drawn","frame"}],
  "lanes":  [{"id","label"}],
  "roles":  [{"id","name","full","category","setting":false,
              "at": {"lane":0-4,"col":0-5},            // absent for a setting
              "lenses": ["app", ...],
              "what","where","why",
              "products": {"az":[{"name","service":"<azure service id, optional>","note","source"}], "oss":[{"name","note","source"}]},
              "aliases": ["kafka", ...],
              "topics": ["<topic id>", ...],           // Atlas topics that document it: empty means "no page yet"
              "sources": [url, ...], "basis": "<url or judgement>", "status": "verified|unconfirmed", "checked"}],
  "edges":  [{"from","to","label","style":"solid|dash|dot","lenses":[...],"badge":"<role id>"}],
  "levels": [{"id","generic","azure","about","source"}],   // tenant, management group, subscription, resource group
  "org":    [{"id","generic","azure","levels":[...],"kind":"scope|span|outside","inherits":false,"what","why","sources","status","checked","service","note"}] }
```

- Positions are in the data (a lane and a column). An automatic layout is not worth its cost for twenty-two boxes.
- The page embeds the data as JSON and draws it in the browser, so it works from `file://` and needs no fetch.
- A role links to the topics that document it. A role with no topic is listed as "no page yet": that list is the backlog for the add-topic skill.
- Validator (`make validate`): ids unique; every lens, lane, stack, topic and Azure service id exists; every box has a free cell; every edge
  joins two roles; every role is in at least one lens; every role has `what`, `where`, `why` and `checked`, and `sources` unless it is a convention of the picture (`users`); `status` is
  `verified` only with a source. Warnings: a role with no topic, a product with no source.

## Coverage

Twenty-two roles, seventeen organization-level items. Text and products were read against Microsoft Learn and each product's own site on 2026-11-03: `done` means read and consistent, `partial` means a claim could not be confirmed (the note says which). `siem` and `storage` are new.

| Item | Status | Notes |
|---|---|---|
| `users` | partial | users and clients, the start of the request path. Read 2026-11-03: a convention of the picture, no source applies |
| `waf` | done | edge protection and cache (CDN, WAF). Read against sources 2026-11-03 |
| `lb` | done | load balancer, layer 4 and layer 7. Read against sources 2026-11-03 |
| `web` | done | web server or reverse proxy. Read against sources 2026-11-03 |
| `app` | done | application service. Read against sources 2026-11-03 |
| `db` | done | relational database. Read against sources 2026-11-03 |
| `dns` | done | name resolution. Read against sources 2026-11-03 |
| `secrets` | done | secrets store. Read against sources 2026-11-03 |
| `identity` | done | identity provider. Read against sources 2026-11-03 |
| `broker` | done | message broker; Kafka is an event streaming platform that often fills this role (to confirm). Read against sources 2026-11-03 |
| `cache` | partial | cache; the network-cost claim varies by provider and stays "check your provider" until sourced. Read 2026-11-03: name and retirement dates confirmed; the same-segment and network-cost advice is not on the Learn pages read |
| `search` | done | search index. Read against sources 2026-11-03 |
| `worker` | done | background worker. Read against sources 2026-11-03 |
| `vpn` | done | private connectivity. Read against sources 2026-11-03 |
| `bastion` | done | admin access to private servers. Read against sources 2026-11-03 |
| `firewall` | partial | central firewall service at a network boundary. Read 2026-11-03: Architecture Center: not on every hop; Bastion to firewall to server not shown |
| `filter` | partial | traffic filter rules, a setting shown as a shield. Read 2026-11-03: NSG confirmed; the iptables/nftables entry has no source |
| `collector` | done | telemetry collector or agent. Read against sources 2026-11-03 |
| `store` | done | telemetry store. Read against sources 2026-11-03 |
| `dash` | done | dashboards and alerts. Read against sources 2026-11-03 |
| `siem` | done | security events collected and analysed (SIEM); new, not in the mockup, to draw and place. Read against sources 2026-11-03 |
| `storage` | done | object and file storage for uploads, media and backups; new, not in the mockup, to draw and place. Disks belong to the server and are not drawn. Read against sources 2026-11-03 |
| `tenant` | done | the directory, top of the hierarchy. Read against sources 2026-11-03 |
| `mg` | done | management groups. Read against sources 2026-11-03 |
| `sub` | done | subscription. Read against sources 2026-11-03 |
| `rg` | done | resource group. Read against sources 2026-11-03 |
| `entra` | done | Entra ID, tenant level. Read against sources 2026-11-03 |
| `condacc` | partial | Conditional Access, tenant level. Read 2026-11-03: tenant-level wording not on the page |
| `pim` | done | Privileged Identity Management, tenant level. Read against sources 2026-11-03 |
| `policy` | done | Azure Policy, assigned at a scope and inherited. Read against sources 2026-11-03 |
| `rbac` | done | role assignments, any scope, inherited. Read against sources 2026-11-03 |
| `cost` | done | Cost Management, several scopes. Read against sources 2026-11-03 |
| `defender` | partial | Defender for Cloud, subscription. Read 2026-11-03: per-subscription plans and management group option not stated |
| `actlog` | done | activity log, subscription. Read against sources 2026-11-03 |
| `advisor` | partial | Advisor, subscription. Read 2026-11-03: resource and management group scope not stated |
| `arm` | done | Azure Resource Manager, spans every level. Read against sources 2026-11-03 |
| `graph` | done | Resource Graph, spans subscriptions. Read against sources 2026-11-03 |
| `monitor` | partial | Azure Monitor platform; its workspaces are resources in a resource group. Read 2026-11-03: workspace in a resource group is inferred from the Resource Manager rule |
| `devops` | partial | Azure DevOps, outside the subscriptions, linked to the tenant (to confirm). Read 2026-11-03: Entra connection confirmed; "outside the subscriptions" not stated |
| `stack:aws` | planned | another stack, after generic and Azure are checked |
| `stack:vsphere` | planned | on-premises stack |
| `stack:dynatrace` | planned | a monitoring product stack |

## Known gaps

- Roles and products were read once, on 2026-11-03, and not re-read since. Placement (lane, column, edges) is a judgement, not a sourced fact. Learn pages for Azure metrics, Ceph, Redis's self-description and OpenSearch Dashboards could not be read or do not say what was asked: unconfirmed.
- The scope of each organization-level service (tenant, management group, subscription) is from general knowledge, to be read against Learn.
  Azure DevOps's separation from the subscriptions is unconfirmed (its Entra link is confirmed). Azure Managed Redis is the current name (Azure Cache for Redis retires 2027-03-31 for Enterprise tiers, 2028-09-30 for the others).
- Where filtering happens: the Architecture Center shows a firewall in parallel with Application Gateway (not on the gateway to server hop) as a common design, and NSGs as less granular than a firewall. The shield on the load balancer and bastion hops is the filter-rules idea, not a claim that a firewall is there. Bastion to firewall to server is not shown on the hub-and-spoke page: unconfirmed.
- The Generic names for the organization levels are a mapping, not a standard.
- One base picture shows one common shape of application. Applications that do not look like it (event-driven, data pipelines, single page
  apps with no web tier) fit it only roughly.
- `siem` and `storage` are not in the mockup: their place on the picture and their edges are new and need the owner's eye once drawn.

## Decisions

- One page, one base picture, lenses and stacks as filters. Reason: the owner wants to see how everything connects, and a picture that moves
  between lenses hides that.
- Role first, product second. Reason: a new service is understood by its role; the same role is filled by different products in each stack.
- Generic first. Reason: the owner's call; products make the page stale faster than roles do.
- No subnets or address ranges. Reason: the owner's call; the view shows who talks to whom, not how it is deployed.
- Settings are not drawn, except filter rules as a shield. Reason: objects like role assignments belong to every role, so drawing them
  clutters the picture; but "where is traffic filtered" is a main question.
- Firewall is a central service at a boundary; filtering on each hop is the filter rules. Reason: a box on every hop would be wrong for how the
  cloud works, and the owner asked not to see it everywhere. The placement is to be checked against the reference architecture.
- The data lives in `views/lenses/`, not in `topics/`. Reason: it is not a topic about one product, and the registry keeps two layers
  (family, topic); the view is a page of the Views family with its own catalogue. Reason unconfirmed beyond that.
- Positions in the data, drawn in the browser from embedded JSON. Reason: no layout engine to maintain, and the page must work from `file://`.
- Written by the assistant; spec approved by the owner on 2026-11-03. The roles and the organization items came from the mockup that the
  owner reviewed; the text did not. Security (SIEM) and storage roles added at the owner's request.

## Updating

Add a role: a row in `roles` (and its place in `at`), its edges, its aliases, sources, and a row in Coverage. Add a product: under the
role's `products`, with a source. Add a stack: declare it under `stacks`, fill the `products` key of each role, mark the stack `planned` until
every role has been read. When the Azure topic gains or drops a service, `make lenses-check` flags a dangling `service` id.
