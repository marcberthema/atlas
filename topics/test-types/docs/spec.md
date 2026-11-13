# Test types: spec

Status: published (Test family). 25 entries. Data checked 2026-11-13. Format: `docs/topic-spec.md`.

## Purpose and audience

A reference for the kinds of automated test and where each one sits in the test pyramid: what it checks, what it costs, when to use it.
For someone who has to decide which tests a project needs. Each kind comes with a worked example for a typical Python application and for
Terraform code, so the same idea can be seen in both worlds. For the other main languages, one page per language names the tools that
fill each layer: unit tests, coverage, integration and end-to-end tests.

## Scope

- In: the pyramid and its layers (unit, contract, integration, end-to-end), the kinds that sit beside it (static analysis, smoke,
  regression, acceptance, performance, security, property-based, coverage) and the alternative shapes (testing trophy, honeycomb, ice-cream cone).
  For each kind: a short definition, what it checks, speed and cost, who owns it, common mistakes, and a Python and a Terraform example.
- In: one entry per language with the tools for unit tests, test doubles, coverage, integration tests and end-to-end tests, each with a link
  and the version analysed, and one unit test example fetched from the official documentation. Languages: Java and Kotlin (with Maven and
  Gradle), JavaScript and TypeScript (Node.js), C#, Go, C++, Rust, PHP, Ruby, Swift, plus Python and Terraform as a summary of the worked examples.
- Out: manual and exploratory testing, test management tools, and CI pipeline syntax (see the `github-actions` and `azure-devops` topics).
  Tool-by-tool reference pages: the tools appear only as the example of a kind or as a row of a language, with a link to their own documentation.
  A worked example in every layer for every language: the layer tabs stay Python and Terraform only.
  Other IaC tools. C, Scala, Dart, R and languages no longer maintained (VB6 and the like).
  Commercial tools: free and open source tools only, and what ships with the language's own toolchain.
- The rule: a kind is in when a page of a known project or a well known article defines it. A tool is in a language's table when the
  language's own documentation names it, or when it is the project's own documented way to do that job. At most three tools per cell.
  Nothing is written from experience.

## Layout

Archetype: concepts. Eight tabs (`templates/view.json`):

| Tab | Holds |
|---|---|
| Pyramid | `pyramid`: the shape, the layers side by side (cost, speed, count, scope), how to pick, the usual mistakes |
| Unit | `unit` |
| Contract | `contract` |
| Integration | `integration` |
| End-to-end | `e2e` |
| Languages | Group `languages`, with a picker: one entry per language |
| Other kinds | The shared entry list, opened in a window: the kinds beside the pyramid (static analysis, smoke, regression, acceptance, performance, security, property-based, coverage) and `shapes` (pyramid, trophy, honeycomb) |
| Compare | Four tables: the tools per language, the layers in Python and in Terraform, pyramid, trophy and honeycomb, solitary or sociable unit tests |

Each layer entry opens the same way: one sentence, what it checks and what it does not, then two parts, Python and Terraform, each with a
short explanation, a fetched code example and the tool it uses. Terraform has no unit tests in the strict sense (a plan needs the
provider schema), so that part says what stands in for the layer.

Each language entry opens the same way: one sentence on how testing is organised in that language (built in or by library, where test
files live, the command that runs them), a table of tools (rows: unit, test doubles, coverage, integration, end-to-end; columns: tool,
what it is, version analysed, link), then one fetched unit test example. The Java entry adds a part for Maven (Surefire, Failsafe, the
JaCoCo plugin) and one for Gradle (the `test` task, the JaCoCo plugin). A cell with no established tool says so.

Groups: `layers`, `languages`, `beside`, `shapes`.

## Sources

Python: the pytest, unittest and unittest.mock documentation, the Pact documentation (Python guide), Testcontainers for Python, Playwright for
Python, Hypothesis and Locust. Terraform: the `terraform test` documentation and tutorial, `terraform validate` and `terraform plan`, Terratest,
TFLint and Checkov. Pyramid concepts: Martin Fowler, "The Practical Test Pyramid" and "TestPyramid". Every entry lists the pages it was
written from. Re-check: `track` fields compare the latest GitHub releases with `version.analysed` (`make test-types-check`);
`make test-types-examples` re-fetches the code examples.

Languages: each tool's own documentation and release page, and the language's own testing page where it has one (the Go `testing` package,
the Node.js test runner, the Rust book and Cargo book, Microsoft Learn for .NET testing, the Maven Surefire and Failsafe plugins, the Gradle
user manual, Swift Testing). The table below was the starting list; each tool kept was checked against its documentation on 2026-11-13.

| Language | Starting list |
|---|---|
| Java and Kotlin | JUnit, Mockito, JaCoCo, Testcontainers, Selenium, Playwright for Java |
| JavaScript and TypeScript | the Node.js test runner, Jest, Vitest, c8 and Istanbul, Playwright, Cypress |
| C# | xUnit.net, NUnit, MSTest, NSubstitute, Coverlet, ASP.NET Core integration tests, Playwright for .NET |
| Go | the `testing` package and `go test -cover`, `httptest`, Testify, Testcontainers for Go |
| C++ | GoogleTest, Catch2, CTest, gcov and lcov, llvm-cov |
| Rust | `cargo test` (unit and `tests/`), cargo-llvm-cov |
| PHP | PHPUnit, Pest, coverage through Xdebug or PCOV |
| Ruby | RSpec, Minitest, SimpleCov, Capybara |
| Swift | Swift Testing, XCTest, the coverage of the Swift toolchain |
| Python | pytest, coverage.py and pytest-cov, Testcontainers, Playwright |
| Terraform | `terraform test`, Terratest; coverage: no tool known |

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
| `coverage` | done | What it measures (line, branch), what it does not prove; coverage.py for Python; Terraform: none known |
| `lang-java` | done | Java and Kotlin, with a Maven part and a Gradle part |
| `lang-javascript` | done | JavaScript and TypeScript on Node.js |
| `lang-csharp` | done | C# and .NET |
| `lang-go` | done | Go: mostly the standard toolchain |
| `lang-cpp` | done | C++: no language-specific end-to-end tool expected |
| `lang-rust` | done | Rust: mostly Cargo |
| `lang-php` | done | PHP |
| `lang-ruby` | done | Ruby |
| `lang-swift` | done | Swift |
| `lang-python` | done | Summary table; the worked examples stay in the layer tabs |
| `lang-terraform` | done | Summary table; the worked examples stay in the layer tabs |
| `kind:compare` | done | four tables: `mapping`, `shape-compare`, `doubles`, `languages` (one row per language: unit, coverage, integration, end-to-end) |

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
- Languages: which tools are "the main ones" is a judgement. No public source ranks them, so the table follows the rule in Scope and does not claim popularity.
- Languages: a coverage tool for Terraform is not known; the cell will say "none found" unless a documented one turns up.
- Languages: a language entry lists several tools but can `track` only one repository, so the other versions are re-read by hand.

## Decisions

- New family `test`, drawn in the purple of the Test stage of the DevOps loop (`--tst` in `shared/transit.py`). Stage: test.
- Worked examples in the layer tabs are Python (pytest) and Terraform only, as requested.
- Other languages get a tools page each, not a worked example in every layer: nine more languages in four layer tabs would make each tab too long to look things up in. Requested on 2026-11-13; this replaces the earlier decision to leave other languages out.
- Language list: Java (Maven and Gradle), C++, C#, Node.js and Go were requested; TypeScript, Kotlin, Rust, PHP, Ruby and Swift were added as other languages in wide use. Kotlin shares the Java entry and TypeScript the JavaScript entry, because the tools are the same.
- A language entry's `version.analysed` is the version of its first unit test tool, and its `track` follows that tool's repository. Every other tool's version is shown in its table row.
- Coverage is a kind beside the pyramid, not a layer: it measures the tests, it is not a test.
- Code examples are fetched unchanged from official pages; where a layer has no official snippet, the part is prose with a link.
- Archetype is concepts, with one tab per layer of the pyramid because those are what people look up; the rest go in a picker.
- The Terraform version analysed is the latest release found at the check (v1.17.2 on 2026-11-11); the `terraform` topic is at v1.17.1 and is not changed here.
- Tool versions at the check (2026-11-12): pytest 9.2.0, Pact Python 4.2.0, Testcontainers for Python 4.15.0, Playwright for Python 1.65.1, Terratest 1.0.1, Checkov 3.4.4, TFLint 0.66.0, Locust 2.47.0, Hypothesis 6.170.15, mypy 2.4.1 (from its docs page).
- The Terraform tab uses the shared "others" list rather than a picker, so the kinds beside the pyramid open in a window, as in the patterns topic.
- DevOps loop stages: test. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.

## Updating

When a tool releases, run `make test-types-check`, read the release notes for changed behaviour of the examples, update `version`, `checked`
and the facts together, then `make test-types-examples` and `make build`. Re-read the Fowler articles only if their date changes.
For a language entry, `make test-types-check` reports only the tracked tool: open the other tools' release pages and update their rows too.

## Language entries: what differs from the plan

- Go and Ruby have no `track`: neither publishes GitHub releases, so their versions come from go.dev and RubyGems and `make test-types-check` skips them.
- TestNG, Spock, Mocha, Selenium for other languages, Behat and Kotest were not looked at; the starting list was kept to the tools named there.
- NUnit and MSTest are in the C# table next to xUnit.net, because Microsoft Learn names all three (and TUnit, which is not in the table).
- Swift's end-to-end tool, XCUIAutomation, is Apple's and not open source; the entry says so.
- The Java examples are Testcontainers and Mockito: the JUnit site failed the certificate check of the script that fetches examples (expired at the time), so the JUnit example is a link.
- The Vitest site failed the same way, so Vitest has no example.
