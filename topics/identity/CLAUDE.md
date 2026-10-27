# Identity providers (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/identity/`.

Same shape as the GitOps topic: `data/identity.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/identity/index.html` with `templates/index.html`. Python 3 standard library only.

`data/identity.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md` for the format. `scripts/validate.py` (`make validate`)
checks it. Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: Identity providers are the OIDC, SAML and LDAP side of sign-in. Single sign-on and the protocols (OIDC, OAuth 2.0, SAML, LDAP, Kerberos, SCIM) are covered in depth, with open source identity providers (Keycloak in depth, Dex, authentik, Authelia, ZITADEL and others), directories, three cloud services as references, and how Argo CD and Kubernetes use an identity provider. Open source or free tools only. Paid products are left out unless they are a CNCF alternative, or the user asked for them as a reference.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. For a specification the version is the document (for example an RFC) and its month. For a managed service it is the
docs page date. `started` is only `confirmed` when an announcement, RFC or release gives the date, not when it is a repository creation date.

The page has one tab per main entry (the `TABS` list in `templates/index.html`, ids must be entry ids), then Other tools and Compare.

Refreshing: `make check` lists what changed (releases, archived repositories, CNCF levels; `LINKS=1` for source and link urls) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every entry that has a GitHub repository and releases.

Paid products: the group `paid` (Other tools tab) lists a few commercial products so the reader knows they exist. Each is a `ref` entry that says what the vendor's own
page says, nothing more, and names its closest open source alternative in `compare` (an entry id in this topic). No prices unless the page shows them, and say they change.
