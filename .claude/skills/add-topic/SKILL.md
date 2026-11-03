---
name: add-topic
description: Add a new Atlas topic (a reference page set about one product or subject). Reads the official documentation, writes the spec first, then the entries, fetches the code examples, validates, builds and commits to a branch. Use when the user says "add topic X" or asks for a new reference topic.
---

# Add a topic

You are adding one topic to Atlas. Read `docs/vision.md`, `docs/topic-spec.md`, the root `CLAUDE.md` and the Terraform topic
(`topics/terraform/docs/spec.md`, `templates/view.json`, a few entries of `data/terraform.json`) first: Terraform is the worked example.
The result is a branch for the owner to review. Never push, open a PR, merge or deploy without being asked.

Input: the topic name, and if the user did not say, propose the family (`iac`, `cicd`, `development`, `enterprise`) and the DevOps
stages (`topics.json` `stages`) and say that they are your judgement.

## Steps

1. **Branch.** `git checkout -b topic-<id>` from an up to date `main`. If a draft with this id exists in `topics.json`, use it.
2. **Scaffold.** `python3 shared/new_topic.py <id> "<Label>" <family> --stages a,b --description "..."`. It creates `topics/<id>/` from the
   Terraform topic and registers a draft. The topic is not built or shown until it is published.
3. **Research the official source.** Use the project's own documentation and repository, not blogs. Note for every page: URL, the date it
   shows, and the version it describes. Find the GitHub repository and release tag pattern for `track`, and the licence (SPDX id as GitHub reports it).
   Anything you cannot verify goes in `notes` as "unconfirmed". Nothing is written from memory.
4. **Write `docs/spec.md` before any entry.** All eight sections (see `docs/topic-spec.md`): purpose, scope (with exclusions), layout
   (pick an archetype, name the tabs), sources, a coverage table of what you plan to write, known gaps, decisions, updating.
   **Stop and show the spec to the user for approval** unless they said to decide on their own. If they did, record that in Decisions.
5. **Write the data** in `data/<id>.json`, following `topics/gitops/docs/data-model.md` and the Terraform topic. Use a throwaway generator script in the
   scratchpad, not in the repo; the JSON is the source of truth. Rules that decide most reviews:
   - Short plain sentences. Summaries are plain text: no backticks. Link other entries as `[label](#entry-id)`.
   - Every entry: `version` (what was analysed, its release date, the check date), `track` when there is a GitHub repository, `links`, `sources`
     (each page it was written from, two or more for an entry that is a tab), `notes` for anything unconfirmed.
   - Code is never pasted: a `code` item names the source page and a `match` string, and `make <id>-examples` fetches it. A match must be exact,
     including whitespace. The page knows only the languages yaml, shell and text, so other languages use `text`.
   - Lookup pages (types, options, flags) are short tables, not articles. Put what people look up most first, and the rare things behind a picker.
   - More than about eight tabs is too many: use a group tab with `pick` (and `sets` to split the buttons into rows), with an overview entry first.
   - Facts that depend on the version (flags, defaults) say which version.
   - No employer, client or confidential material, no credentials or ids. General public knowledge only.
6. **Check.** `make <id>-examples`, `make <id>-validate` (0 bad; fix warnings you can), then `python3 shared/new_topic.py --publish <id>` once the
   description in `topics.json` is real, then `make build`. Open `dist/<id>/index.html` in a browser (serve `dist/`), click every tab, check the picker, the
   console for errors, and that links like `#entry-id` resolve. Run `GITHUB_TOKEN=$(gh auth token) make <id>-check`: 0 differences.
7. **Update the spec**: coverage statuses, known gaps (single-source entries, unconfirmed claims, what you left out and why). `python3 shared/spec.py` passes.
8. **Commit** with `dist/`: one commit for the spec, one for the data and build. Update `docs/roadmap.md` and the root `CLAUDE.md` topic list.
9. **Report** to the user: what was added, the decisions you made on your own, what is unconfirmed, and what to review first.

## Do not

- Copy documentation text. Summarise it and link it.
- Set `started` to confirmed from a repository creation date.
- Add paid products as subjects. They appear only as short references (see the GitOps `paid` group).
- Edit `data/examples.json` by hand.
