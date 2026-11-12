# Test types: spec

Status: draft (not published). Data checked 2026-11-12. Format: `docs/topic-spec.md`.

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
| Others | A picker of the kinds beside the pyramid: static analysis, smoke, regression, acceptance, performance, security, property-based |
| Compare | Pyramid, trophy and honeycomb; unit or integration first; mocks or real dependencies |

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
| `pyramid` | planned | Pyramid tab: the shape, the layers compared, how to pick |
| `unit` | planned | pytest and unittest.mock; Terraform `terraform test` with `command = plan` and mocked providers |
| `contract` | planned | Pact consumer and provider; Terraform: the module interface (variable validation, outputs) tested with `expect_failures` |
| `integration` | planned | pytest with Testcontainers; Terraform: `terraform test` with `command = apply`, Terratest |
| `e2e` | planned | Playwright for Python; Terraform: apply the root configuration in a sandbox and probe the result |
| `others` | planned | Static analysis, smoke, regression, acceptance, performance, security, property-based |
| `compare` | planned | Pyramid or trophy or honeycomb; mocks or real dependencies |

## Known gaps

- Nothing is written yet. This spec is the plan.
- "Contract test" for Terraform is not an established term in the Terraform documentation. The part will say that it is this topic's mapping
  (a module's variables and outputs are its interface), marked unconfirmed in `notes`.
- Terraform "unit" and "integration" both use `terraform test`; the documentation separates them by the `command` (`plan` or `apply`), not by those names.
  The part will say so.
- Python examples fetched from documentation are small. A complete pyramid for one application is not available from a single official page,
  so the examples are separate snippets and are not stitched together.

## Decisions

- New family `test`, drawn in the purple of the Test stage of the DevOps loop (`--tst` in `shared/transit.py`). Stage: test.
- Examples are Python (pytest) and Terraform only, as requested.
- Code examples are fetched unchanged from official pages; where a layer has no official snippet, the part is prose with a link.
- Archetype is concepts, with one tab per layer of the pyramid because those are what people look up; the rest go in a picker.
- The Terraform version analysed is the latest release found at the check (v1.17.2 on 2026-11-11); the `terraform` topic is at v1.17.1 and is not changed here.
- Tool versions at the check: pytest 9.2.0, Playwright for Python v1.65.1, Testcontainers for Python 4.15.0, Checkov 3.4.4, TFLint v0.66.0, Terratest
  (modules/core v2.0.0). Pact for Python and Hypothesis: release tags not read yet, to confirm before the entries.
- DevOps loop stages: test. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.

## Updating

When a tool releases, run `make test-types-check`, read the release notes for changed behaviour of the examples, update `version`, `checked`
and the facts together, then `make test-types-examples` and `make build`. Re-read the Fowler articles only if their date changes.
