# GitOps (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/gitops/`.

Same shape as the other topics: `data/gitops.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/gitops/index.html` with `templates/index.html`. Python 3 standard library only.

The data format is a placeholder (`title`, `intro`, `sections`). Design the real one with the user when the first content
is collected, and write it down in a `docs/data-model.md` here. Content collected with AI help goes into the JSON with
its source URL. Say "unconfirmed" when it can't be verified.

Every entry must record the version of the tool analysed (Argo CD version, for example) and the page must show it. See the
root `CLAUDE.md`.
