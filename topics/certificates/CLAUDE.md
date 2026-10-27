# Certificates (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/certificates/`.

Same shape as the GitOps topic: `data/certificates.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/certificates/index.html` with `templates/index.html`. Python 3 standard library only.

`data/certificates.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md` for the format. `scripts/validate.py` (`make validate`)
checks it. Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: X.509 and TLS basics, ACME and Let's Encrypt, private CAs, cert-manager and Kubernetes, and OpenSSL commands to inspect and troubleshoot a certificate. Open source or free tools only. Paid products are left out unless they are a CNCF alternative, or the user asked for them as a reference.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. For a specification the version is the document (for example an RFC) and its month. For a managed service it is the
docs page date. `started` is only `confirmed` when an announcement, RFC or release gives the date, not when it is a repository creation date.

The page has one tab per main entry (the `TABS` list in `templates/index.html`, ids must be entry ids), then Other tools and Compare.

Refreshing: `make check` lists what changed (releases, archived repositories, CNCF levels; `LINKS=1` for source and link urls) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every entry that has a GitHub repository and releases.
