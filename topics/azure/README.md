# Azure with Terraform (Atlas topic)

A quick reference for what an Azure service provides, what it needs, and how to build it with Terraform.
Tiers 0 (always there) and 1 (core) only for now: 42 services.

Two steps, joined by one JSON file:

```
Microsoft Learn + Terraform Registry  ->  data/services.json  ->  dist/azure/index.html
      (AI-assisted or scripted)           (source of truth)        (scripts/build.py)
```

## Use it

Run from `topics/azure/` (or from the repo root as `make azure-<target>`):

```bash
make help       # all targets
make build      # validate, then generate ../../dist/azure/ (index.html and services.resolved.json)
make check      # daily freshness check (Learn pages, Terraform support); writes data/services.json
make ack SERVICE=key-vault   # mark a service's docs as reviewed after you updated it
make stale      # list what needs review, write review/PROMPT.md for an AI agent (ALL=1, LIMIT=5)
```

Python 3 standard library only. `dist/azure/index.html` works from `file://`. To preview the whole site, run `make serve` in the repo root.

## Change the look or the stack

Everything the page shows comes from `dist/azure/services.resolved.json`. Edit `templates/index.html` for a new look,
or write your own front end against that file.

The page has two views of the same data, switched with the Simple / Full button (the choice is remembered). Simple is the
default: tier chips, search, purpose, requires and required by, Learn links. Full adds Terraform status, freshness and review
badges, the cloud native rating (the filter is parked until the data is more complete), and the Compare tab. The format is in [docs/data-model.md](docs/data-model.md).

## Pipeline

`.github/workflows/daily-check.yml` runs `make check` and `make build` every day and commits the result.
It uses no AI. It only records whether each Learn page changed since it was last reviewed, and which Terraform
resources exist. Content in `manual` is never touched by it.

## Review loop

The daily check only detects. To bring entries up to date:

```bash
make stale                      # which services need review, and why
claude "$(cat review/PROMPT.md)"  # the prompt written by make stale; run both from topics/azure/
```

The prompt gives the agent, per service, the current entry and a diff of the Learn page against the text last
reviewed (`data/snapshots/`, kept locally and git-ignored; run `make check` first in a fresh clone). The agent asks you for decisions, edits `data/services.json`, runs `make ack`,
commits per service on a `review/<date>` branch, and opens a PR to `main` once you confirm. The first pass over
never-reviewed services is `make stale ALL=1 LIMIT=5`.

`azure-services.html` is the original hand-built single page, kept as a reference only.
