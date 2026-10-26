# Atlas

A personal knowledge base: a collection of references to look things up in, not Q&A. Each topic is a set of facts kept in
JSON, generated into static HTML. Published on Cloudflare Pages under marcberthelette.com; only `dist/` is exposed.
Built with AI assistance. Topics now: Azure with Terraform, GitOps.

---

## Architecture: data in, view out, per topic

```
sources (docs, registries) -> topics/<id>/data/*.json -> topics/<id>/scripts/build.py -> dist/<id>/index.html
topics.json + shared/ -> the top banner on every page and the landing page, dist/index.html
```

- Each topic owns its `data/`, `scripts/`, `templates/`, `docs/` and its own `CLAUDE.md` with the topic's rules. Read it
  before working in a topic.
- `topics.json` is the topic registry (name, tagline, topics). The banner and the landing page are built from it.
- `shared/atlas.py` renders the banner. A template carries `<!--__BANNER__-->` after `<body>` and `/*__BANNER_CSS__*/` in
  its style block; the topic build fills both. `shared/build_site.py` builds `dist/index.html`.
- AI generates content into the JSON files. Python checks for updates and builds the pages. Neither the look nor the stack
  of a page may require changing the data.
- `dist/` is generated and committed. Cloudflare Pages has no build command and `dist` as its output directory.
- Adding a topic: create `topics/<id>/` (data, scripts/build.py, templates/index.html, Makefile, CLAUDE.md), add it to
  `topics.json` and to `TOPICS` and the pattern rules in the root `Makefile`.

Do not add dependencies, a framework or external scripts or fonts without asking. Python 3 standard library only. Pages must
work from `file://`: relative links that name `index.html`, no absolute paths, no fetch of local files.

---

## Rules for every topic

- **Everything is public, for everyone.** Atlas exists so that I and anyone else can find centralized information in one place.
  Write only from public sources, and write it as general knowledge. Nothing is ever based on, drawn from or shaped by a
  company I work or worked for, a client, or any confidential material: no internal names, architectures, region counts,
  team structures, tools choices, incidents or conventions, not even rephrased or "anonymised". If something would only be
  known from that experience, it does not go in. No credentials, tokens, account or subscription ids either.
- **Every source is linked.** An entry links to each page it was written from, so a reader can check it. The footer disclaimer
  (`shared/atlas.py`) is on every page; a template must keep its `<!--__FOOTER__-->` marker.
- **The version analysed is always visible.** Every documented thing records which version of it was analysed, and the page
  shows it next to the content: the product, API or provider version when there is one (for example `azurerm 5.11.0`, API
  `2026-08-01`), and the date of the source page and of the check. If the source has no version, show the page's date.
  A topic's data model must have a place for it, its validator must flag entries without it, and a template must not hide it.
- **Accuracy over completeness.** Do not add a fact from memory when unsure. Verify against the official source and say
  "unconfirmed" in the note if it can't be verified. Dates and versions change often; check the announcement.
- **Keep text short and plain.** Facts only where a common confusion exists.
- **Style:** match the existing code: same naming, same comment density.
- Never push, open a PR, rename the GitHub repo or change Cloudflare settings without asking.

## Commands

```bash
make help        # all targets
make validate    # every topic
make build       # every topic and the landing page into dist/
make serve       # build and serve dist/ on http://localhost:8000
make azure-check # run any target of a topic: make <topic>-<target>
```

## Workflow

1. Describe the change. Claude edits the topic's data (or template), runs `make build`, and checks the page in a browser.
2. Commit after each coherent change, with a message saying what was added or corrected. Commit `dist/` with it.
3. Branch and PR to `main` after the user confirms.

## Feedback Style

Be direct. If a claim, relationship or date is uncertain, say so plainly rather than guessing. Flag errors in existing entries
when you notice them.
