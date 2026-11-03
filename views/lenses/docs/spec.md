# Lenses and the organization level: spec

Status: spec drafted, waiting for the owner's approval. No data and no page yet. The visual reference is the mockup `docs/mockups/lenses.html`
(sample text, not verified). Format: `docs/topic-spec.md`, adapted for a view that has its own catalogue.

## Purpose and audience

Answers "where does this service go?" for someone who meets a service they do not know (Kafka, Redis, a bastion, a load balancer) or who wants
the high-level picture of how an application and its surroundings connect. It files every product under a role ("message broker", "cache"),
and shows the role on one base picture of an application. A lens changes what is highlighted, a stack changes the labels, and the picture
never moves. A second view shows what sits above the resource group: tenant, management groups, subscriptions and the services tied to each.

## Scope

- In: roles (what a thing is for), where a role usually sits and what it talks to, products per stack (generic, Azure, open source), five lenses
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
Re-check: each role and organization item carries `sources` (urls) and `checked`. `make lenses-check` (to be written) reports products
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
              "products": {"azure":[{"name","service":"<azure service id>","note"}], "oss":[{"name","note"}]},
              "aliases": ["kafka", ...],
              "topics": ["<topic id>", ...],           // Atlas topics that document it: empty means "no page yet"
              "sources": [url, ...], "basis": "<url or judgement>", "status": "verified|unconfirmed", "checked"}],
  "edges":  [{"from","to","label","style":"solid|dash|dot","lenses":[...],"badge":"<role id>"}],
  "levels": [{"id","generic","azure","about","scope"}],   // tenant, management group, subscription, resource group
  "org":    [{"id","generic","azure","level","kind":"scope|span|outside","inherits":false,"what","why","sources","status","checked"}] }
```

- Positions are in the data (a lane and a column). An automatic layout is not worth its cost for twenty boxes.
- The page embeds the data as JSON and draws it in the browser, so it works from `file://` and needs no fetch.
- A role links to the topics that document it. A role with no topic is listed as "no page yet": that list is the backlog for the add-topic skill.
- Validator (`make validate`): ids unique; every lens, lane, stack, topic and Azure service id exists; every box has a free cell; every edge
  joins two roles; every role is in at least one lens; every role has `what`, `where`, `why`, `sources` and `checked`; `status` is
  `verified` only with a source. Warnings: a role with no topic, a product with no source.

## Coverage

Twenty roles, seventeen organization-level items. All are `planned`: the mockup text is sample content and has to be read against the sources
before it is data.

| Item | Status | Notes |
|---|---|---|
| `users` | planned | users and clients, the start of the request path |
| `waf` | planned | edge protection and cache (CDN, WAF) |
| `lb` | planned | load balancer, layer 4 and layer 7 |
| `web` | planned | web server or reverse proxy |
| `app` | planned | application service |
| `db` | planned | relational database |
| `dns` | planned | name resolution |
| `secrets` | planned | secrets store |
| `identity` | planned | identity provider |
| `broker` | planned | message broker; Kafka is an event streaming platform that often fills this role (to confirm) |
| `cache` | planned | cache; the network-cost claim varies by provider and stays "check your provider" until sourced |
| `search` | planned | search index |
| `worker` | planned | background worker |
| `vpn` | planned | private connectivity |
| `bastion` | planned | admin access to private servers |
| `firewall` | planned | central firewall service at a network boundary |
| `filter` | planned | traffic filter rules, a setting shown as a shield |
| `collector` | planned | telemetry collector or agent |
| `store` | planned | telemetry store |
| `dash` | planned | dashboards and alerts |
| `tenant` | planned | the directory, top of the hierarchy |
| `mg` | planned | management groups |
| `sub` | planned | subscription |
| `rg` | planned | resource group |
| `entra` | planned | Entra ID, tenant level |
| `condacc` | planned | Conditional Access, tenant level |
| `pim` | planned | Privileged Identity Management, tenant level |
| `policy` | planned | Azure Policy, assigned at a scope and inherited |
| `rbac` | planned | role assignments, any scope, inherited |
| `cost` | planned | Cost Management, several scopes |
| `defender` | planned | Defender for Cloud, subscription |
| `actlog` | planned | activity log, subscription |
| `advisor` | planned | Advisor, subscription |
| `arm` | planned | Azure Resource Manager, spans every level |
| `graph` | planned | Resource Graph, spans subscriptions |
| `monitor` | planned | Azure Monitor platform; its workspaces are resources in a resource group |
| `devops` | planned | Azure DevOps, outside the subscriptions, linked to the tenant (to confirm) |
| `stack:aws` | planned | another stack, after generic and Azure are checked |
| `stack:vsphere` | planned | on-premises stack |
| `stack:dynatrace` | planned | a monitoring product stack |

## Known gaps

- Nothing is verified yet: the mockup is sample text. Every role and organization item starts `unconfirmed`.
- The scope of each organization-level service (tenant, management group, subscription) is from general knowledge, to be read against Learn.
  Azure DevOps's relation to the tenant, and the current name of Azure's managed Redis service, are unconfirmed.
- Where filtering happens (shield on the load balancer to servers hop and on the bastion to servers hop) is a pattern, to be checked against the
  hub-and-spoke reference architecture.
- The Generic names for the organization levels are a mapping, not a standard.
- One base picture shows one common shape of application. Applications that do not look like it (event-driven, data pipelines, single page
  apps with no web tier) fit it only roughly.
- There is no security information (SIEM) role yet, and no storage role (object, file, disk). Add them when a lens needs them.

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
- Written by the assistant and approved by the owner on this date: not yet. The roles and the organization items came from the mockup that
  the owner reviewed; the text did not.

## Updating

Add a role: a row in `roles` (and its place in `at`), its edges, its aliases, sources, and a row in Coverage. Add a product: under the
role's `products`, with a source. Add a stack: declare it under `stacks`, fill the `products` key of each role, mark the stack `planned` until
every role has been read. When the Azure topic gains or drops a service, `make lenses-check` flags a dangling `service` id.
