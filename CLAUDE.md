# Atlas

A personal knowledge base: a collection of references to look things up in, not Q&A. Each topic is a set of facts kept in
JSON, generated into static HTML. Published as a Cloudflare Worker with static assets at atlas.marcberthelette.com; only `dist/` is exposed.
Built with AI assistance. Topics now: Azure with Terraform, Terraform, GitOps, GitHub Actions, Azure DevOps, Identity providers, Certificates, Enterprise topologies, Architecture and design patterns, Test types.
Kept in git but not published: Workstation setup (`workstation/`), Visual Studio Code setup (`vscode/`) and Claude Code setup (`claude/`).

---

## Architecture: data in, view out, per topic

```
sources (docs, registries) -> topics/<id>/data/*.json -> topics/<id>/scripts/build.py -> dist/<id>/index.html
topics.json + shared/ -> the top banner on every page and the landing page, dist/index.html
```

- Each topic owns its `data/`, `scripts/`, `templates/`, `docs/` and its own `CLAUDE.md` with the topic's rules. Read it
  before working in a topic.
- `topics.json` is the topic registry (name, tagline, families, stages, topics). `stages` are the eight DevOps stages (plan, code, build, test, release, deploy, operate, monitor); a topic or draft may list the `stages` it belongs to, and `make validate` checks the ids. Two layers only: family, then topic. CI/CD covers application delivery pipelines and the services around them (artifact repositories, scanners, quality gates). Each published topic names its `family` (an id from `families`: IaC, CI/CD, Development, Enterprise, Test, SaaS). The banner (two rows: families, then the selected family's topics, sticky) and the landing page (a search over every entry, then one column per family) are built from it. A page's own sticky bars sit below the banner through `--atlash`.
  An entry with `"draft": true` is an idea, not a topic: it needs only `id` and `label`, may carry any extra keys
  (`description`, `notes`, ...), is never built or shown, and has no folder. To publish it, remove `draft`, add a
  `description`, create `topics/<id>/` and add its `<topic>-%` rule to the root `Makefile`. `make validate` checks all of this.
  The user writes ideas there to say what to work on next: read the drafts when asked what is next.
  The repo itself is public, so drafts are visible on GitHub even though they never reach `dist/`: keep them as general as the
  rest (no employer or client material).
- Every topic except Azure uses one shared page: `shared/topic.html` (look and script), `shared/build_topic.py`, `shared/learning.py` (checks)
  and `shared/examples.py` (code examples fetched from the docs). A topic keeps its data, its `templates/view.json` (title and tabs)
  and a three line `scripts/build.py`. See `topics/gitops/docs/data-model.md` for the entry format (parts, tables, callouts, code, diagrams).
- The banner has a `?` button that opens the About window: the disclaimer, the git ref and repository, and a switch (remembered in `localStorage`) that shows the low-value details of every entry. Those details (release and check dates, status, CNCF, licence, extra links, sources) carry the class `xd` in `shared/topic.html` and are hidden by default; each entry also has its own "details" button. The version analysed is never hidden. The version is the release tag in the `VERSION` file (or `ATLAS_REF` when set, as `make deploy` does), so committed pages change only when a release is cut.
- The `lenses` view (`/lenses/`) is not built from topic metadata: it has its own catalogue, `views/lenses/data/lenses.json`, with a spec at `views/lenses/docs/spec.md`. `shared/lenses_check.py` validates it (in `make validate`), `shared/build_lenses.py` builds it from `shared/lenses.html`, and `make lenses-check` also checks its source links. Read the spec before changing it.
- `shared/atlas.py` renders the banner. A template carries `<!--__BANNER__-->` after `<body>` and `/*__BANNER_CSS__*/` in
  its style block; the topic build fills both. `shared/build_site.py` builds `dist/index.html`.
- AI generates content into the JSON files. Python checks for updates and builds the pages. Neither the look nor the stack
  of a page may require changing the data.
- `dist/` is generated and committed. Deploy with `make deploy` (wrangler, one Worker named `atlas` serving `dist/`); there is no build on Cloudflare. The site is published only when a release is published, through `.github/workflows/deploy.yml` (wrangler, no build, the committed `dist/` at the release tag; it can also be run by hand). Merging a PR does not publish it.
- `workstation/` is not a topic: same data model, checks and shared page, but it builds into `workstation/site/index.html`
  (outside `dist/`, so never deployed) with a banner that names only itself. It is not in `topics.json`. Read `workstation/CLAUDE.md`.
- `vscode/` is the same kind of unpublished resource (`vscode/site/index.html`). Its entries are VS Code extensions, tracked against the
  Marketplace by `make vscode-check`, and its `setup/profile.json` must agree with them (`make vscode-validate` checks). Read `vscode/CLAUDE.md`.
- `claude/` is the same kind of unpublished resource, with no data model or site: a README (tools looked at, verdicts, sources) and `setup/` scripts that install the Claude Code
  setup globally (`make claude-setup`) or into one project (`make claude-project PROJECT=<path>`). Read `claude/CLAUDE.md`.
- Adding a topic: use the `add-topic` skill (or `python3 shared/new_topic.py <id> "<Label>" <family>`, which scaffolds a draft and a spec); `refresh-topic` updates one. Done by hand: create `topics/<id>/` (data, scripts/build.py, templates/index.html, Makefile, CLAUDE.md), add it to
  `topics.json` and to `TOPICS` and the pattern rules in the root `Makefile`.

Do not add dependencies, a framework or external scripts or fonts without asking. Python 3 standard library only. Pages must
work from `file://`: relative links that name `index.html`, no absolute paths, no fetch of local files.

---

## Rules for every topic

- **A spec per topic.** `topics/<id>/docs/spec.md` (also `workstation/` and `vscode/`) holds the purpose, scope, layout, sources, coverage, known gaps and decisions. Write it before the entries, get it approved, and change it in the same commit as the data. Format: `docs/topic-spec.md`. The product vision and the order of work are in `docs/vision.md` and `docs/roadmap.md`.
- **Everything is public, for everyone.** Atlas exists so that I and anyone else can find centralized information in one place.
  Write only from public sources, and write it as general knowledge. Nothing is ever based on, drawn from or shaped by a
  company I work or worked for, a client, or any confidential material: no internal names, architectures, region counts,
  team structures, tools choices, incidents or conventions, not even rephrased or "anonymised". If something would only be
  known from that experience, it does not go in. No credentials, tokens, account or subscription ids either.
- **Centralise, don't copy.** Atlas gathers knowledge in one place and points to where it lives. Summarise in short plain sentences and link
  the page. Code examples are not pasted into the data: a script fetches them from the source page by a match string into a generated cache
  (see `topics/gitops/scripts/examples.py`), shows them unchanged, and `make check` reports when they change upstream. Never stitch or edit an
  example: show the official snippets as they are, several from one page in their order at most.
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
make deploy      # validate, build, wrangler deploy to atlas.marcberthelette.com
make azure-check # run any target of a topic: make <topic>-<target>
```

## Workflow

1. Describe the change. Claude edits the topic's data (or template), runs `make build`, and checks the page in a browser.
2. Commit after each coherent change, with a message saying what was added or corrected. Commit `dist/` with it.
3. Branch and PR to `main` after the user confirms.
4. Release (only when the user asks): write the new tag in `VERSION`, `make build`, commit with `dist/`, PR and squash merge, then `gh release create <tag> --target main`; publishing the release deploys. The tag names the version the About window shows.

## Feedback Style

Be direct. If a claim, relationship or date is uncertain, say so plainly rather than guessing. Flag errors in existing entries
when you notice them.

<!-- atlas claude setup: ui-rules begin -->
## UI work

- Use `/impeccable` for UI: `critique` and `audit` to review a page, then `polish`, `typeset`, `layout` and its other commands to refine it. Run `/impeccable init` once per project (its README says to).
- This project's own rules (dependencies, fonts, scripts, file layout) win over the skill.
<!-- atlas claude setup: ui-rules end -->
