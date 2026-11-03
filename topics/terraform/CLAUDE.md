# Terraform (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/terraform/`.

Same shape as the GitOps and Certificates topics: `data/terraform.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/terraform/index.html` with the shared page (`shared/topic.html`) and `templates/view.json`. Python 3 standard library only.

`data/terraform.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md`. `scripts/validate.py` (`make validate`) checks it.
Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: the Terraform CLI and language only, kept general: workflow, commands, blocks, language lookups, state, providers and modules, testing, debugging.
No cloud-specific resources (those belong to the Azure topic or a future one). Terraform 1.6.0 and later is under the Business Source
License 1.1, so it is not open source; say so (the `license` field is `BUSL-1.1`). The companion tools are open source, and OpenTofu is
listed as an alternative. Paid products (HCP Terraform and others) are left out unless asked for as a reference.

Every entry records the version analysed. The tab entries share Terraform's version (`version.analysed` is the latest stable
release when the docs were read, tracked by `make check`). Docs pages are read from developer.hashicorp.com `latest`; when a new minor
release appears, re-read the pages named in `sources` and the CHANGELOG, then update `version`, the facts and `checked` together.

Tabs (`templates/view.json`): Start and CLI are single entries; Blocks, Language and State & ops are group tabs with `pick`, which show a row of
buttons and one entry at a time (`sets` split the buttons into labelled rows). The first entry of a pick group is its overview. Blocks are grouped by
how often they are used, a judgement for this page. Then Ecosystem (the tools) and Compare. Lookup pages (types, references, functions...) have no
`part`: short tables, one section after another. Learning-layout entries use parts, steps,
tables, callouts, cards, diagrams, fetched code examples: see `topics/gitops/docs/data-model.md`). Code examples are fetched, never pasted:
give the source page and a `match` string, run `make examples`. HCL examples use `lang: text` because the page only knows yaml, shell and text.
Check diagrams in a browser after editing one.
