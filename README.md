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
not connected to git: after a merge to `main`, run `make deploy` (validate, build, `wrangler deploy`). `dist/` is committed. The daily GitHub Action (`.github/workflows/daily-check.yml`) refreshes the Azure topic and commits.
