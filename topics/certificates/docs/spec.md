# Certificates: spec

Status: published (Development family). Data checked 2026-10-26. Reconstructed from the data and git history, not written before the content:
reasons that the history does not record are marked "reason unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

A reference for working with X.509 certificates and TLS: the concepts and formats, ACME and automatic issuing, private CAs and workload identity,
cert-manager and Kubernetes, and the OpenSSL commands to inspect and troubleshoot a certificate. For someone who has to get, renew, inspect or
debug a certificate.

## Scope

- In: X.509 and TLS basics, ACME and Let's Encrypt, ACME clients, private CAs, cert-manager and trust-manager, Kubernetes TLS, OpenSSL. Open source
  or free tools.
- Out: paid products, except a few `paid` references for awareness. Two cloud services (Azure Key Vault certificates, AWS ACM) are references and are
  marked not open source.
- Versions: for a specification the version is the document (an RFC) and its month; for a managed service it is the docs page date; for a tool it is
  the release.

## Layout

Archetype: product family. Eight tabs: X.509 and PKI, TLS, ACME and Let's Encrypt, cert-manager, Kubernetes, Inspect and troubleshoot, Other
tools, Compare. Groups: concepts and formats, ACME and automatic issuing, private CAs and workload identity, Kubernetes, cloud services, tools and
troubleshooting, paid products. Comparisons: ACME challenge types, ACME clients, certificate authorities you can run, where certificates live.

## Sources

The RFCs (5280, 8446, 8555, 7468), the Let's Encrypt, cert-manager, Kubernetes and OpenSSL documentation, and each tool's repository. Re-check
with `make certificates-check` and `make certificates-examples`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `x509` | done | RFC 5280 |
| `tls` | done | RFC 8446, TLS 1.3 |
| `acme` | done | RFC 8555 |
| `cert-manager` | done | v1.21.3 |
| `kubernetes-tls` | done | |
| `troubleshooting` | done | OpenSSL commands and common errors |
| `formats` | done | PEM, DER, PKCS#12, CSRs |
| `certbot` | done | |
| `step-ca` | done | |
| `openbao` | done | PKI secrets engine |
| `spire` | done | workload identity |
| `openssl` | done | |
| `azure-key-vault-certs` | done | cloud reference, not open source |
| `aws-acm` | done | cloud reference, not open source |
| `digicert` | done | paid reference |
| `sectigo` | done | paid reference |
| `globalsign` | done | paid reference |
| `cyberark-certificate-manager` | done | paid reference |
| `keyfactor-command` | done | paid reference |

## Known gaps

- Start dates: 23 of 27 entries are `started` unconfirmed.
- Seven references have no `track` (the two cloud services and the five paid products), so the update check skips them.
- Several entries have notes that say what could not be confirmed (ACME, cert-manager and the OpenSSL entries carry the most): read each entry's
  notes before relying on a detail.

## Decisions

- ACME and cert-manager are separate tabs from the concepts. Reason unconfirmed.
- Cloud services are included as references although they are not open source, and are marked so. Reason: the owner asked for them (the scope
  text in the data records this).
- Paid products are references only, as in the GitOps topic.

## Updating

Run `make certificates-check` after a release of cert-manager, certbot, step-ca, SPIRE or OpenSSL, read the notes and the pages in `sources`, then
update `version`, the facts and `checked` together.
