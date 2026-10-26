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

## Publish

Cloudflare Pages connected to this repo: no build command, output directory `dist`. `dist/` is committed, so a merge to
`main` is the deploy. The daily GitHub Action (`.github/workflows/daily-check.yml`) refreshes the Azure topic and commits.
