# Cloudflare: spec

Status: published (SaaS family). Data checked 2026-11-04. Format: `docs/topic-spec.md`. The owner asked for a summary of what is available and the API, so the topic is kept lean.

## Purpose and audience

A reference for someone building on or putting a site behind Cloudflare: what each product is for, how the pieces fit (DNS and proxy in front, Workers and storage behind, Zero Trust for internal access), the tools that manage it (Wrangler, Terraform, the API) and where the limits and pricing pages are. It points to the official documentation and does not replace it.

## Scope

- In: the products documented at developers.cloudflare.com that a developer or platform engineer configures. Workers and its bindings (KV, R2, D1, Durable Objects, Queues, Hyperdrive, Workflows), DNS, Cache, SSL/TLS, Rules, WAF, DDoS, Bots, Turnstile, Tunnel, Cloudflare One (Access, Gateway, WARP), and the tooling (Wrangler, Terraform provider, API, `cloudflared`).
- Out: the consumer services (1.1.1.1, Radar), billing and support pages, network products for carriers and enterprises (Magic Transit, BYOIP, Network Interconnect), media (Stream, Images, Realtime) and the AI products (Workers AI, AI Gateway, Vectorize, Agents). Each of these gets one line in the `others` list with a link, so the reader knows it exists. Reason: the rule is "what you configure to run an app", and the docs list well over a hundred products.
- Plans and prices: not recorded. They change often and Cloudflare publishes them. Entries link to the pricing and limits pages and say which plan a feature needs only when the docs page says so.
- Versions: Wrangler, `cloudflared`, workerd and the Terraform provider have releases. Other products are services: the version is the docs page date, or "no date on page".

## Layout

Archetype: product family, kept lean. Eight tabs: Start (`platform`), API (`api`), Workers (`workers`), and pickers for Data (KV, R2, D1, Durable Objects, Queues, Hyperdrive, Workflows), Edge (DNS, Cache, SSL/TLS), Security (WAF), Zero Trust (Tunnel, Cloudflare One) and Tooling (Wrangler, Terraform provider, cloudflared). Each product entry has a short description and a table of where to look in the docs. No comparisons. Reason: the owner wants a summary of what is available and the API, not guides.

## Sources

developers.cloudflare.com, read from each product's `llms.txt` index and its pages. Repositories for `track`: `cloudflare/workers-sdk` (Wrangler, tag `wrangler@x.y.z`, Apache-2.0), `cloudflare/cloudflared` (Apache-2.0), `cloudflare/workerd` (Apache-2.0), `cloudflare/terraform-provider-cloudflare` (Apache-2.0, tag pattern to check: the release list shows several major lines). The docs repository `cloudflare/cloudflare-docs` is CC-BY-4.0. Re-check with `make cloudflare-check` and `make cloudflare-examples`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `platform` | done | product map, objects |
| `api` | partial | tokens and rate limits; endpoints not read |
| `workers` | done | plan limits from the limits page |
| `kv` | done |  |
| `r2` | done |  |
| `d1` | done |  |
| `durable-objects` | done |  |
| `queues` | done |  |
| `hyperdrive` | done |  |
| `workflows` | done |  |
| `dns` | done |  |
| `cache` | done |  |
| `ssl-tls` | partial | modes page not read |
| `waf` | partial | start page only |
| `tunnel` | done |  |
| `cloudflare-one` | partial | Access, Gateway and WARP not read separately |
| `wrangler` | partial | tracked; commands not read |
| `terraform` | done | v5 line tracked |
| `cloudflared` | done | tracked |

## Known gaps

- The API entry covers authentication and rate limits only. The base URL and endpoints were not read; the API reference is linked from the docs.
- Product entries are summaries from the docs index, the product's front page and its page list, not from the full guides. Their "Where to look" tables name docs sections, not fields or commands.
- Wrangler commands, Cloudflare One's Access, Gateway and WARP products, and the WAF rule types were not read.
- Pages is not an entry and its current status was not checked.
- Plans and prices are left out on purpose. Only the Workers plan limits are given, from the limits page.

## Decisions

- Cloudflare is a paid service with free tiers. It is included as a SaaS family topic because the owner asked for it. The open source tools (Wrangler, `cloudflared`, workerd, the provider) are tracked; the services are references with the docs page date.
- DevOps loop stages: deploy, operate. A judgement for the DevOps loop view, not a statement from a source.

## Updating

Run `make cloudflare-check` after a Wrangler, `cloudflared` or provider release, read the pages in `sources`, then update `version`, the facts and `checked` together. Re-read the product index (`llms.txt`) a few times a year: products are added and renamed often.
