# GitOps: spec

Status: published (IaC family). Data checked 2026-10-26. Reconstructed from the data and git history, not written before the content: reasons
that the history does not record are marked "reason unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

A reference for GitOps on Kubernetes: the principles, Argo CD in depth, Flux, the other operators, and the tools that produce the manifests
(Helm, Kustomize and alternatives), plus how secrets are handled. For someone choosing, installing or operating a GitOps setup.

## Scope

- In: open source or free tools. Argo CD is the main subject, then Flux, then short references for other operators (name, start date, status).
  Helm and Kustomize in depth, with short references for alternatives. Secrets tools.
- Out: paid products, except a few listed for awareness in the `paid` group, each a short reference that says only what the vendor page says and
  names its closest open source alternative. No prices.
- The rule that decides: open source or free (`CLAUDE.md`).

## Layout

Archetype: product family. Seven tabs (`templates/view.json`): GitOps principles, Argo CD, Flux, Helm, Kustomize, Other tools, Compare.
Groups: principles, GitOps operators, around the operator (progressive delivery and promotion), Helm, Kustomize and alternatives, secrets, paid
products. Argo CD, Helm and Kustomize and the principles use the learning layout (parts, steps, tables, fetched examples, diagrams).
Comparisons: Argo CD and Flux; Helm, Kustomize and alternatives; secrets in GitOps.

## Sources

The project sites and documentation of each tool, opengitops.dev for the principles, and each tool's GitHub repository for releases. The Argo
CD docs pages show no version: they are the stable docs read on 2026-10-26 (v3.5.6). Re-check with `make gitops-check` (`LINKS=1` also fetches every
source link) and `make gitops-examples`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `opengitops` | done | the four principles, v1.0.0 |
| `argo-cd` | done | main subject: install, dev and production setups, API, CLI, UI |
| `flux` | partial | overview level: the controllers; whether Flux core has a web UI is unconfirmed |
| `helm` | done | Helm 4 |
| `kustomize` | done | |
| `fleet` | done | reference |
| `flux-v1` | done | end of life, reference |
| `weave-gitops` | done | inactive is a judgement |
| `config-sync` | done | reference |
| `kubevela` | done | reference |
| `flux-operator` | done | reference |
| `argo-rollouts` | done | overview |
| `flagger` | partial | how it treats the Deployment was not on the page read |
| `kargo` | done | overview |
| `argocd-image-updater` | done | reference |
| `sealed-secrets` | done | overview |
| `external-secrets` | done | overview |
| `sops` | done | overview |
| `secrets-store-csi` | done | overview |
| `argocd-vault-plugin` | done | reference; inactive is a judgement |
| `akuity-platform` | done | paid reference |
| `harness-gitops` | done | paid reference |
| `openshift-gitops` | done | paid reference |
| `codefresh-gitops` | done | paid reference, discontinued |
| `argo-api-vs-cli-vs-ui` | planned | compare the API (`/swagger-ui` on the server) with the CLI commands and the web UI, to list what only one of them can do. Waits for a running test Argo CD |

## Known gaps

- The API, CLI and UI comparison for Argo CD is a recorded to-do (above).
- Start dates: 30 of 33 entries are `started` unconfirmed, because repository creation dates are not announcements.
- Unconfirmed in the data: Flux core's web UI, whether the Flux Helm controller uses the Helm SDK, the exact Flux v1 retirement date, whether
  argoproj-labs projects are covered by the Argo CD CNCF graduation, and several details of the paid references (their notes say which).
- "Inactive" for `weave-gitops` and `argocd-vault-plugin` is a judgement from release history, not a statement from the projects.
- Four paid references have no `track`, so the update check skips them.

## Decisions

- Tabs per product, with Argo CD, Helm and Kustomize in depth (PR #11); links per entry (PR #12). Reasons unconfirmed beyond the commit titles.
- Paid products are listed for awareness only, as short references. Reason: the repo's open source or free rule, with an exception so the reader
  knows the closest commercial options exist (`CLAUDE.md` of this topic).
- Code examples are fetched, not copied (PR #15, the learning layout). Reason: the repo rule "centralise, don't copy".
- `started` is `confirmed` only when an announcement or release gives the date. Reason: repository creation dates are not announcements.

## Updating

Run `make gitops-check` after a release of Argo CD, Flux, Helm or Kustomize, read the release notes and the pages named in `sources`, then update
`version`, the facts and `checked` together. Add a `track` to every new entry that has a GitHub repository.
