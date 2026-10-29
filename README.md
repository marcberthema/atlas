# Atlas

A personal knowledge base: references to look things up in, collected over time. Each topic is JSON data turned into a
static page. Public at marcberthelette.com (Cloudflare Pages, only `dist/` is published).

```
sources  ->  topics/<id>/data/*.json  ->  dist/<id>/index.html     (AI-assisted content, Python builds)
                  topics.json + shared/  ->  top banner + dist/index.html
```

| Topic | What | Docs |
|---|---|---|
| Azure with Terraform | What an Azure service provides, needs, costs, and how to build it with Terraform | [topics/azure](topics/azure/README.md) |
| GitOps | Argo CD and GitOps (just started) | [topics/gitops](topics/gitops/CLAUDE.md) |

## Not published

[Workstation setup](workstation/CLAUDE.md): from a new Windows PC to a working Linux setup in WSL 2 (Ubuntu LTS, zsh, uv,
fnm, kubectl, Terraform, Azure CLI, Docker, Claude Code). Same format and look as a topic, but it lives in `workstation/`, builds
into `workstation/site/index.html` and is never deployed. Open that file in a browser, or `make workstation-build` to rebuild it.
`workstation/setup/` has a script that installs and configures everything from a JSON profile.

## Use it

```bash
make help       # all targets
make build      # validate and build every topic and the landing page into dist/
make serve      # build and serve dist/ on http://localhost:8000
make azure-check   # any topic target: make <topic>-<target>
```

Python 3 standard library only. Every page works from `file://`.

## Drafting ideas

Add an entry to `topics.json` with `"draft": true` to note a topic idea (`id`, `label`, and any notes you like). Drafts are
skipped by the banner, the landing page and the build, so they never reach `dist/`. Remove `draft` once the topic exists
under `topics/<id>/`.

## Publish

A Cloudflare Worker with static assets named `atlas` serves `dist/` at atlas.marcberthelette.com (`wrangler.jsonc`). It is
not connected to git. `.github/workflows/deploy.yml` runs `wrangler deploy` when a commit on `main` changes `dist/` (and after the
daily check commits one). It needs the repo secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. `make deploy` does the same by hand. The daily GitHub Action (`.github/workflows/daily-check.yml`) refreshes the Azure topic and commits.
