# Test types: spec

Status: published (Test family). 13 entries. Data checked 2026-11-12. Format: `docs/topic-spec.md`.

## Purpose and audience

A reference for the kinds of automated test and where each one sits in the test pyramid: what it checks, what it costs, when to use it.
For someone who has to decide which tests a project needs. Each kind comes with a worked example for a typical Python application and for
Terraform code, so the same idea can be seen in both worlds.

## Scope

- In: the pyramid and its layers (unit, contract, integration, end-to-end), the kinds that sit beside it (static analysis, smoke,
  regression, acceptance, performance, security, property-based) and the alternative shapes (testing trophy, honeycomb, ice-cream cone).
  For each kind: a short definition, what it checks, speed and cost, who owns it, common mistakes, and a Python and a Terraform example.
- Out: manual and exploratory testing, test management tools, and CI pipeline syntax (see the `github-actions` and `azure-devops` topics).
  Tool-by-tool reference pages: the tools appear only as the example of a kind, with a link to their own documentation.
  Other languages and other IaC tools: the examples are Python and Terraform only, by decision.
- The rule: a kind is in when a page of a known project or a well known article defines it. Nothing is written from experience.

## Layout

Archetype: concepts. Seven tabs (`templates/view.json`):

| Tab | Holds |
|---|---|
| Pyramid | `pyramid`: the shape, the layers side by side (cost, speed, count, scope), how to pick, the usual mistakes |
| Unit | `unit` |
| Contract | `contract` |
| Integration | `integration` |
| End-to-end | `e2e` |
| Other kinds | The shared entry list, opened in a window: the kinds beside the pyramid (static analysis, smoke, regression, acceptance, performance, security, property-based) and `shapes` (pyramid, trophy, honeycomb) |
| Compare | Three tables: the layers in Python and in Terraform, pyramid, trophy and honeycomb, solitary or sociable unit tests |

Each layer entry opens the same way: one sentence, what it checks and what it does not, then two parts, Python and Terraform, each with a
short explanation, a fetched code example and the tool it uses. Terraform has no unit tests in the strict sense (a plan needs the
provider schema), so that part says what stands in for the layer.

## Sources

Python: the pytest, unittest and unittest.mock documentation, the Pact documentation (Python guide), Testcontainers for Python, Playwright for
Python, Hypothesis and Locust. Terraform: the `terraform test` documentation and tutorial, `terraform validate` and `terraform plan`, Terratest,
TFLint and Checkov. Pyramid concepts: Martin Fowler, "The Practical Test Pyramid" and "TestPyramid". Every entry lists the pages it was
written from. Re-check: `track` fields compare the latest GitHub releases with `version.analysed` (`make test-types-check`);
`make test-types-examples` re-fetches the code examples.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `pyramid` | done | Pyramid tab: the shape, the layers compared, how to start, mistakes |
| `unit` | done | pytest and unittest.mock; `terraform test` with `command = plan` and `mock_provider` |
| `contract` | done | Pact consumer and provider; Terraform: variable validation and `expect_failures` (this topic's mapping) |
| `integration` | done | Testcontainers; `terraform test` with the default apply; Terratest as prose |
| `e2e` | done | Playwright for Python; Terraform: a `check` block probing a deployed endpoint |
| `static-analysis` | done | mypy; `terraform fmt`, `validate`, TFLint, Checkov |
| `smoke` | done | one source (ISTQB glossary) |
| `regression` | done | one source (ISTQB glossary) |
| `acceptance` | done | Fowler and the ISTQB glossary; the examples are suggestions |
| `performance` | done | Locust |
| `security` | done | OWASP WSTG only points to the guide |
| `property-based` | done | Hypothesis; no Terraform tool found |
| `shapes` | done | Dodds and Spotify; the year of the Spotify article is from its URL |
| `kind:compare` | done | three tables: `mapping`, `shape-compare`, `doubles` |

## Known gaps

- "Contract test" for Terraform is not an established term in the Terraform documentation. The entry says it is this topic's mapping, and `notes` marks it unconfirmed. The same applies to using a `check` block as an end-to-end probe.
- The Terraform documentation does separate integration and unit testing by the `command` of a run block (apply or plan), so those two entries rest on its own words.
- Terratest has no fetched example: its code samples are loaded by script, not present in the page. The entries describe it in prose and link its quick start.
- Tool versions (pytest, Pact Python, Testcontainers, Playwright, Terraform, Terratest, mypy, Checkov, TFLint, Locust, Hypothesis) are recorded in the text and in `version.docs`, but no entry has a `track`, because each entry is a concept, not a tool. `make test-types-check` checks the code examples only.
- `smoke`, `regression`, `static-analysis`, `performance` and `acceptance` rest on the ISTQB glossary's one-line definitions (no date on the pages) plus one tool each. `security` is only a pointer to OWASP's guide.
- Dodds's article gives the trophy's history; the Spotify page has no date (year from its URL, unconfirmed).
- The Python snippets from the unittest.mock and Testcontainers pages are doctests (`>>>`), shown as on the page.
- Pact's own site (docs.pact.io) had an expired certificate for some clients when checked, so the Pact Python site is the source.
- Not covered: exploratory and manual testing, mutation testing, snapshot tests, test data management.

## Decisions

- New family `test`, drawn in the purple of the Test stage of the DevOps loop (`--tst` in `shared/transit.py`). Stage: test.
- Examples are Python (pytest) and Terraform only, as requested.
- Code examples are fetched unchanged from official pages; where a layer has no official snippet, the part is prose with a link.
- Archetype is concepts, with one tab per layer of the pyramid because those are what people look up; the rest go in a picker.
- The Terraform version analysed is the latest release found at the check (v1.17.2 on 2026-11-11); the `terraform` topic is at v1.17.1 and is not changed here.
- Tool versions at the check (2026-11-12): pytest 9.2.0, Pact Python 4.2.0, Testcontainers for Python 4.15.0, Playwright for Python 1.65.1, Terratest 1.0.1, Checkov 3.4.4, TFLint 0.66.0, Locust 2.47.0, Hypothesis 6.170.15, mypy 2.4.1 (from its docs page).
- The Terraform tab uses the shared "others" list rather than a picker, so the kinds beside the pyramid open in a window, as in the patterns topic.
- DevOps loop stages: test. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.

## Updating

When a tool releases, run `make test-types-check`, read the release notes for changed behaviour of the examples, update `version`, `checked`
and the facts together, then `make test-types-examples` and `make build`. Re-read the Fowler articles only if their date changes.
