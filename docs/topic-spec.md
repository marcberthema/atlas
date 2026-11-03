# Topic spec

Every topic keeps `docs/spec.md` next to its data. It is the plan the content is built from, and the record of what was left out. Write it
before the entries, get it approved, then generate the content. When the data changes, change the spec in the same commit.
`make validate` runs `shared/spec.py`, which checks the structure below and that the coverage table agrees with the data.

It applies to the published topics and to the unpublished `workstation/` and `vscode/`.

## Sections

The file starts with a title, a one-line status (`Status: ... Data checked YYYY-MM-DD`), then these sections in this order. Each is short.

| Section | What goes in it |
|---|---|
| `## Purpose and audience` | Who looks things up here, and for what. One paragraph. |
| `## Scope` | What is in, what is out, and the rule that decides. Name the exclusions. |
| `## Layout` | The archetype, the tabs and what each holds, and the groups. Say why the tabs are what they are. |
| `## Sources` | The primary pages the content is read from, and how to re-check them (the `track` fields, `make check`). |
| `## Coverage` | A table of what was planned: see below. |
| `## Known gaps` | Unconfirmed claims, single-source entries, things known to be wrong or thin. Nothing is hidden here. |
| `## Decisions` | Choices specific to this topic, each with its reason. A reason that cannot be verified says "reason unconfirmed". |
| `## Updating` | What to re-read when a new release appears, and which commands to run. |

## Coverage table

```
| Item | Status | Notes |
|---|---|---|
| `entry-id` | done | what it covers |
```

- `Item` is an entry id in backticks. A row without a backticked first cell is not read by the checker.
- `Status` is one of `done`, `partial`, `planned`, `dropped`. A dropped row says why in `Notes`.
- Every tab that opens one entry in full must be listed (the checker enforces it). Other entries are described by group in `Layout`; list one
  here when it is partial, planned or dropped, or when it carries a decision.
- An item that is not an entry (a tier, a comparison) is written `kind:name`, for example `tier:2`. The checker reads only its status.
- Rows marked `done` or `partial` must exist in the data. Rows marked `planned` or `dropped` that exist in the data produce a warning: update the status.

## Archetypes

A topic is built to one of these shapes, which decides its tabs. Add a new archetype here when a topic does not fit.

| Archetype | Shape | Example |
|---|---|---|
| Tool with a language | Workflow, CLI, one page per block, lookup pages for the language, state and operations, ecosystem, compare | `terraform` |
| Product family | One tab per main product (concepts first), a list of the others, compare | `gitops`, `identity`, `certificates` |
| Concepts | One tab per main idea, a list of the rest, compare | `patterns`, `topologies` |
| Cloud service map | Service entries with edges and a derived view, not the shared page | `azure` |
| Setup guide | Ordered steps, with a script that reads a profile | `workstation`, `vscode` |

## Writing rules

- Everything in a spec is general knowledge from public sources, like the rest of the repo. No employer, client or confidential material.
- A fact about the data comes from the data. A reason for a decision comes from git history or from the user. Otherwise write "reason unconfirmed".
- Keep it short. A spec that nobody reads is worse than none.
