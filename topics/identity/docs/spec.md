# Identity providers: spec

Status: published (Enterprise family). Data checked 2026-10-26. Reconstructed from the data and git history, not written before the content:
reasons that the history does not record are marked "reason unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

A reference for single sign-on and the protocols behind it (OIDC, OAuth 2.0, SAML, LDAP, Kerberos, SCIM), the open source identity providers, and
how a platform such as Argo CD or Kubernetes trusts one. For someone choosing or integrating an identity provider.

## Scope

- In: the protocols, open source identity providers (Keycloak in depth; Dex, authentik, Authelia, ZITADEL and others), directories and
  Kerberos, and the GitOps and Kubernetes integration.
- Out: paid products, except a few `paid` references. Three cloud identity services are references and are marked not open source.
- Versions: for a protocol the version is the specification; for a product, the release; for a managed service, the docs page date.

## Layout

Archetype: product family. Eight tabs: SSO and federation, OIDC and OAuth 2.0, SAML 2.0, LDAP, Keycloak, Argo CD and Kubernetes, Other tools,
Compare. Groups: concepts and protocols, open source identity providers, directories and Kerberos, cloud identity services, GitOps and
Kubernetes, paid products. Comparisons: protocols, open source identity providers, cloud identity services.

## Sources

The specifications (OpenID Connect, RFC 6749 and 9700, RFC 7519, OASIS SAML 2.0, RFC 4511, RFC 7644), each product's documentation and repository,
and the Argo CD docs for the integration. Re-check with `make identity-check` and `make identity-examples`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `sso` | done | |
| `oidc` | done | OIDC 1.0 with errata set 2 |
| `saml` | partial | one source |
| `ldap` | done | RFC 4511 |
| `keycloak` | done | 26.8.1 |
| `argocd-k8s` | done | Argo CD with Dex or a direct OIDC provider |
| `oauth2` | done | overview |
| `jwt` | done | overview |
| `scim` | done | overview |
| `kerberos` | done | overview; no `track` |
| `dex` | done | |
| `authentik` | done | |
| `authelia` | done | |
| `zitadel` | done | |
| `entra-id` | done | cloud reference, not open source |
| `google-cloud-identity` | done | cloud reference, not open source |
| `aws-iam-identity-center` | done | cloud reference, not open source |
| `okta` | done | paid reference |
| `auth0` | done | paid reference |
| `ping-identity` | done | paid reference |

## Known gaps

- `saml` cites one source (validation warns).
- Start dates: 19 of 26 entries are `started` unconfirmed.
- Ten references have no `track`: Kerberos, OpenLDAP, FreeIPA, the three cloud services and the three paid products.

## Decisions

- Keycloak gets its own tab, the other providers are overviews or references. Reason unconfirmed.
- The Argo CD and Kubernetes integration is a tab of its own, because it is where identity providers meet the GitOps topic.
- Cloud services are references, marked not open source. Reason: the owner asked for them (the scope text in the data records this).

## Updating

Run `make identity-check` after a release of Keycloak, Dex, authentik or the other tracked products, read the notes and the pages in `sources`, then
update `version`, the facts and `checked` together. A specification changes rarely: re-read it when its owner publishes a new version.
