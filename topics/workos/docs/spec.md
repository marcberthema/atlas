# WorkOS: spec

Status: published (SaaS family). Data checked 2026-11-04. Format: `docs/topic-spec.md`. The owner asked for a summary of what is available and the API, so the topic is kept lean.

## Purpose and audience

A reference for a developer adding enterprise features to a SaaS application with WorkOS: sign-in (AuthKit), single sign-on and directory sync for customers' identity providers, roles and permissions, audit logs and events. It says what each feature is for, the objects and flows involved, and where the SDKs and API reference are. It points to the official documentation and does not replace it.

## Scope

- In: the products in the WorkOS docs that a developer integrates. AuthKit, Single Sign-On, Directory Sync, Admin Portal, RBAC, Fine-Grained Authorization, Feature Flags, Audit Logs, Events and webhooks, Vault, Pipes, MFA; the API objects (organization, user, connection, directory); the SDKs, CLI and MCP server.
- Out: pricing (WorkOS publishes it; entries link the pricing page), the Widgets GraphQL API reference (one line), on-prem deployment and the migration guides (one line each), and Radar and other pages that the docs index lists without a guide. The rule: what you integrate, not what you buy.
- Not a replacement for the Identity providers topic: protocols (OIDC, SAML, SCIM) and open source providers stay there. WorkOS entries link to them.
- Versions: the SDKs and the CLI have releases. The service itself has no version, so its entries show the docs page date, or "no date on page".

## Layout

Archetype: product family, kept lean. Four tabs: Start (`platform`), API (`api`, conventions and rate limits), Products (a picker over the features, each with a short description and an API surface table) and Tooling (SDKs and CLI). No comparisons. Reason: the owner wants a summary of what is available and the API, not guides.

## Sources

workos.com/docs, read from `workos.com/docs/llms.txt` and the page of each feature. Repositories for `track`: `workos/workos-node` (MIT, v12.1.0 on 2026-10-30), `workos/workos-python` (MIT), `workos/workos-go` (MIT), `workos/authkit-nextjs` (MIT) and `workos/cli` (GitHub reports no SPDX licence, so the licence is unconfirmed). Re-check with `make workos-check` and `make workos-examples`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `platform` | done | objects and a feature map |
| `api` | done | base URL, auth, rate limits |
| `authkit` | done |  |
| `sso` | done |  |
| `directory-sync` | done |  |
| `admin-portal` | done |  |
| `rbac` | done | roles, permissions, groups |
| `fga` | done |  |
| `feature-flags` | partial | operations not read in full |
| `audit-logs` | done |  |
| `events` | done | events list and webhook endpoints |
| `mfa` | partial | operations not read in full |
| `vault` | partial | reference; operations not read |
| `pipes` | partial | reference; operations not read |
| `sdks` | done | Node tracked |
| `cli` | done | tracked, licence unconfirmed |

## Known gaps

- No docs page shows a date or a version, so each entry uses the check date as its release date and says so in `notes`.
- The API surface tables name objects and operations from the reference index (`llms.txt` paths), not endpoint paths or fields. Feature flags, MFA, Vault and Pipes operations were not read in full.
- Only `workos-node` and the CLI are tracked. The other SDKs were seen on GitHub (MIT) but are not entries.
- The `magic-link`, Radar, WorkOS Connect, Widgets, Agents and Platform API sections of the reference are not covered.
- Pricing and plan limits are left out on purpose.

## Decisions

- WorkOS is a paid service with a free tier for some products. It is a SaaS family topic because the owner asked for it. The SDKs are open source and tracked; the services are references with the docs page date.
- The Widgets API and the other long reference sections are one-line links, not entries. Reason: they are lookup material that the official reference does better.
- DevOps loop stages: code, deploy. A judgement for the DevOps loop view, not a statement from a source.
- This branch is based on `topic-cloudflare` because the SaaS family is registered there.
- Entries have no code examples: the docs examples are per language and customised with keys, so none is fetched.

## Updating

Run `make workos-check` after an SDK or CLI release, read the pages in `sources`, then update `version`, the facts and `checked` together. Re-read `llms.txt` a few times a year: products are added and renamed.
