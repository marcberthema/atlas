---
name: refresh-topic
description: Refresh an existing Atlas topic against its sources: find what changed upstream (releases, archived repositories, example blocks, links), re-read the affected pages, and update the data and the spec together. Use when the user says "refresh topic X" or asks whether a topic is out of date.
---

# Refresh a topic

Read `topics/<id>/docs/spec.md` and `topics/<id>/CLAUDE.md` first. The result is a branch for review. Never push, open a PR, merge or deploy
without being asked.

1. **Branch.** `git checkout -b refresh-<id>-<date>` from an up to date `main`.
2. **Find the differences.** `GITHUB_TOKEN=$(gh auth token) make <id>-check` (without a token GitHub allows 60 requests an hour and the check fails). It reads and never
   writes: new releases, archived repositories, CNCF levels, and code examples that changed upstream or can no longer be found. Add `LINKS=1` to also
   fetch every source and link url (slow). `ONLY=<entry id>` limits it to one entry.
3. **Review each difference.** For a new release read the release notes or changelog for that version and the pages named in the entry's `sources`.
   Change only what the sources say. A fact you cannot verify becomes "unconfirmed" in `notes`. Update `version.analysed`, `version.released`, the facts that
   changed and `checked` together, never one without the others.
4. **Examples.** `make <id>-examples` re-fetches them. If one cannot be found, fix its `match`; do not paste code.
5. **Coverage.** Compare the spec's coverage table with what the sources now describe: new features or pages that deserve an entry go in the table as
   `planned`; things removed upstream are marked `dropped` with the reason. Update Known gaps.
6. **Validate and build.** `make <id>-validate`, `python3 shared/spec.py`, `make build`, and look at the changed pages in a browser.
7. **Commit** with `dist/`, one coherent change per commit, and report what changed, what you could not verify, and what you left alone.

A topic with no GitHub repository (a specification, a concept) has no releases to compare: re-read the source page when its date changes.
