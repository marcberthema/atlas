# GitHub Actions: spec

Status: published on the branch `topic-github-actions`, not yet reviewed or merged. Data checked 2026-11-03. Format: `docs/topic-spec.md`.
Approval: written and approved by the assistant alone, overnight, because the owner was asleep. Review the scope, layout and decisions first.

## Purpose and audience

A day-to-day reference for writing and running GitHub Actions workflows: every workflow key, the triggers, expressions and contexts, reuse,
runners, security, and the CLI to drive it. For someone who writes workflows and needs the exact key, rule or limit without reading the
documentation. It is the first topic in the CI/CD family.

## Scope

- In: GitHub Actions as a service (workflow syntax, events, expressions, contexts, default variables, workflow commands, reusable workflows,
  composite actions, runners, secrets, OIDC, environments, caching, artifacts, limits), the `gh` commands for workflows and runs, and
  companion tools (actionlint, act, the runner application, Actions Runner Controller).
- Out: writing JavaScript or Docker container actions in depth (only their metadata keys), GitHub Packages, Pages, Dependabot and code
  scanning beyond a mention, the Actions importer and migrations from other CI systems, agentic workflows, billing, and GitHub Enterprise Server differences.
- Rule that decides: what the official reference pages (docs.github.com, Actions section) say. Nothing about third-party actions beyond the
  security guidance.
- Version: the service has no version, so the version shown is "GitHub Docs, read on 2026-11-03". Tools carry their release versions.

## Layout

Archetype: tool with a language (see `docs/topic-spec.md`). Eight tabs:

| Tab | Holds |
|---|---|
| Start | `overview`: workflow, event, job, step, action and runner, a diagram, the smallest workflow |
| Syntax | A picker. `syntax-index` (every key on one page), then triggers, jobs, steps, matrix, permissions, concurrency |
| Expressions | A picker: expressions and functions, contexts, default variables, workflow commands |
| Reuse | `reuse`: reusable workflows and composite actions, and the action metadata keys |
| Platform | A picker: runners, security and secrets, environments, artifacts and cache, limits |
| CLI | `gh-cli`: the `gh workflow` and `gh run` commands |
| Ecosystem | The tools (the shared "others" list) |
| Compare | Reusable workflow or composite action; artifacts or cache; GitHub-hosted or self-hosted runners; `pull_request` or `pull_request_target` |

## Sources

The Actions reference pages on docs.github.com (workflow syntax, events that trigger workflows, expressions, contexts, variables, workflow
commands, metadata syntax, reusing workflow configurations, runners, secure use, secrets, OIDC, deployments and environments, dependency
caching, limits, the artifacts concept page) and the `gh` manual and `--help`. Tools: each project's repository.
Re-check: `GITHUB_TOKEN=$(gh auth token) make github-actions-check` compares tool releases; the docs pages carry no version or date, so
re-read the pages in each entry's `sources` when GitHub announces a change (the changelog), and update `checked`.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `overview` | done | Start tab |
| `syntax-index` | done | every key at workflow, job and step level |
| `triggers` | done | events, filters, schedule, dispatch, `workflow_call`, `workflow_run` |
| `jobs` | done | |
| `steps` | done | includes `background` steps |
| `matrix` | done | |
| `permissions` | done | all `GITHUB_TOKEN` scopes |
| `concurrency` | done | |
| `expressions` | done | literals, operators, functions, status functions |
| `contexts` | done | the context names and the main `github.*` keys; not every property |
| `env-vars` | done | default environment variables |
| `commands` | done | workflow commands and environment files |
| `reuse` | done | |
| `runners` | done | |
| `security` | done | secrets, `GITHUB_TOKEN`, OIDC, script injection, third-party actions |
| `environments` | done | |
| `artifacts-cache` | done | |
| `limits` | partial | the main limits; the page has more |
| `gh-cli` | done | |
| `actionlint` | done | tool |
| `act` | done | tool |
| `actions-runner` | done | tool |
| `actions-runner-controller` | done | tool |
| `matrix-context-properties` | dropped | every property of every context is on the contexts page; this topic lists the names and the keys used most |
| `agentic-workflows` | dropped | out of scope |
| `importer-migrations` | dropped | out of scope |
| `ghes-differences` | dropped | out of scope |

## Known gaps

- The docs pages carry no version or date. The version shown is the date they were read, so a change on GitHub's side is not detected by `make check`.
- Several entries are written from part of a long page (workflow syntax and events are very long). The tables hold what was read: where a
  table says "and more", the page has the rest.
- `contexts`, `env-vars` and `limits` are partial lists by design.
- Start dates are unconfirmed for every entry (no announcement was read).
- Single-source entries: see the validation warnings.
- Features that look new in the docs (`cache-mode`, `snapshot`, background steps) are described from the reference page only, and their
  availability by plan or version is not stated here: unconfirmed.

## Decisions

- Eight tabs with pickers rather than one tab per key group. Reason: the same layout as the Terraform topic, which the owner asked for after finding 23 tabs too many.
- A `syntax-index` page lists every key on one screen. Reason: the owner wants lookup first, and the keys are what is looked up most.
- No code is pasted: workflow snippets are fetched from the docs pages with `match` strings.
- The service has no release, so the version is the date the pages were read (the repo rule that a version is always visible).
- DevOps loop stages: build, test, release, deploy. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.
- Written and approved without the owner (overnight). Everything is on a branch, unpublished until the owner reviews.

## Updating

When GitHub changes Actions (see the GitHub changelog): re-read the affected reference page, update the entry, its `checked` and the version
text together, and `make github-actions-examples`. For tools: `GITHUB_TOKEN=$(gh auth token) make github-actions-check`. For a new key or event, add a row to
`syntax-index` or `triggers` and, if it deserves a page, a new entry listed here.
