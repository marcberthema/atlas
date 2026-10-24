# Azure Services Map

A quick reference for what an Azure service provides, what it needs, and how to build it with Terraform.
Tiers 0 (always there) and 1 (core) only for now: 42 services.

Two steps, joined by one JSON file:

```
Microsoft Learn + Terraform Registry  ->  data/services.json  ->  dist/index.html
      (AI-assisted or scripted)           (source of truth)        (scripts/build.py)
```

## Use it

```bash
make help       # all targets
make build      # validate, then generate dist/index.html and dist/services.resolved.json
make check      # daily freshness check (Learn pages, Terraform support); writes data/services.json
make ack SERVICE=key-vault   # mark a service's docs as reviewed after you updated it
make serve      # build and serve dist/ on http://localhost:8000
```

Python 3 standard library only. `dist/index.html` works from `file://`.

## Change the look or the stack

Everything the page shows comes from `dist/services.resolved.json`. Edit `templates/index.html` for a new look,
or write your own front end against that file. The format is in [docs/data-model.md](docs/data-model.md).

## Pipeline

`.github/workflows/daily-check.yml` runs `make check` and `make build` every day and commits the result.
It uses no AI. It only records whether each Learn page changed since it was last reviewed, and which Terraform
resources exist. Content in `manual` is never touched by it.

`azure-services.html` is the original hand-built single page, kept as a reference only.
