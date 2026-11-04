# Cloudflare: spec

Status: draft (not published). Data checked 2026-11-04. Format: `docs/topic-spec.md`. Proposed for approval: no entry is written yet.

## Purpose and audience

A reference for someone building on or putting a site behind Cloudflare: what each product is for, how the pieces fit (DNS and proxy in front, Workers and storage behind, Zero Trust for internal access), the tools that manage it (Wrangler, Terraform, the API) and where the limits and pricing pages are. It points to the official documentation and does not replace it.

## Scope

- In: the products documented at developers.cloudflare.com that a developer or platform engineer configures. Workers and its bindings (KV, R2, D1, Durable Objects, Queues, Hyperdrive, Workflows), DNS, Cache, SSL/TLS, Rules, WAF, DDoS, Bots, Turnstile, Tunnel, Cloudflare One (Access, Gateway, WARP), and the tooling (Wrangler, Terraform provider, API, `cloudflared`).
- Out: the consumer services (1.1.1.1, Radar), billing and support pages, network products for carriers and enterprises (Magic Transit, BYOIP, Network Interconnect), media (Stream, Images, Realtime) and the AI products (Workers AI, AI Gateway, Vectorize, Agents). Each of these gets one line in the `others` list with a link, so the reader knows it exists. Reason: the rule is "what you configure to run an app", and the docs list well over a hundred products.
- Plans and prices: not recorded. They change often and Cloudflare publishes them. Entries link to the pricing and limits pages and say which plan a feature needs only when the docs page says so.
- Versions: Wrangler, `cloudflared`, workerd and the Terraform provider have releases. Other products are services: the version is the docs page date, or "no date on page".

## Layout

Archetype: product family. Eight tabs, concepts first.

| Tab | Holds |
|---|---|
| Start (`platform`) | How the pieces fit: zone, proxy, account, Workers, bindings. Which product to look at for which need. |
| Workers (`workers`) | Workers, the runtime and limits, bindings, Pages (status), deploy with Wrangler. |
| Data (`data`, group with picker) | KV, R2, D1, Durable Objects, Queues, Hyperdrive, Workflows: what each is for and when to choose it. |
| Edge (`edge`, group with picker) | DNS, Cache, SSL/TLS, Rules, Load Balancing. |
| Security (`security`, group with picker) | WAF, DDoS, Bots, Turnstile, API Shield. |
| Zero Trust (`zerotrust`, group with picker) | Cloudflare One, Access, Gateway, Tunnel, WARP. |
| Tooling (`tooling`) | Wrangler, API and tokens, Terraform provider, Pulumi, `cloudflared`. |
| Compare | Storage options, Workers vs Pages, Tunnel vs Access vs WARP. |

Groups: platform, compute, data, edge, security, zero trust, tooling, other products. Comparisons: the three above.

## Sources

developers.cloudflare.com, read from each product's `llms.txt` index and its pages. Repositories for `track`: `cloudflare/workers-sdk` (Wrangler, tag `wrangler@x.y.z`, Apache-2.0), `cloudflare/cloudflared` (Apache-2.0), `cloudflare/workerd` (Apache-2.0), `cloudflare/terraform-provider-cloudflare` (Apache-2.0, tag pattern to check: the release list shows several major lines). The docs repository `cloudflare/cloudflare-docs` is CC-BY-4.0. Re-check with `make cloudflare-check` and `make cloudflare-examples`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `platform` | planned | concepts and a product map |
| `workers` | planned | runtime, limits, bindings |
| `wrangler` | planned | CLI and config file, tracked |
| `kv` | planned | |
| `r2` | planned | |
| `d1` | planned | |
| `durable-objects` | planned | |
| `queues` | planned | |
| `dns` | planned | |
| `cache` | planned | |
| `ssl-tls` | planned | |
| `waf` | planned | |
| `tunnel` | planned | tracked through `cloudflared` |
| `cloudflare-one` | planned | Access, Gateway, WARP |
| `terraform` | planned | provider, tracked |

## Known gaps

- Nothing is written yet. Product limits and plan availability are not recorded on purpose (see Scope).
- The Terraform provider release tags need checking before `track` is set: the release list shows v3, v4 and later lines side by side.

## Decisions

- Cloudflare is a paid service with free tiers. It is included as a SaaS family topic because the owner asked for it. The open source tools (Wrangler, `cloudflared`, workerd, the provider) are tracked; the services are references with the docs page date.
- The Pages status is read from the docs when the entry is written (unconfirmed now: the docs may point new projects to Workers).
- DevOps loop stages: deploy, operate. A judgement for the DevOps loop view, not a statement from a source.

## Updating

Run `make cloudflare-check` after a Wrangler, `cloudflared` or provider release, read the pages in `sources`, then update `version`, the facts and `checked` together. Re-read the product index (`llms.txt`) a few times a year: products are added and renamed often.
