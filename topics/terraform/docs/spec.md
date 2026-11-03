# Terraform: spec

Status: published (IaC family). Terraform v1.17.1 analysed. Data checked 2026-11-02. Format: `docs/topic-spec.md`.

## Purpose and audience

A day-to-day reference for the Terraform CLI and language only: the workflow, the commands, every block type, the language lookups (types,
references, expressions, functions), state, testing and debugging, and the tools around it. For someone who writes Terraform and needs the
exact syntax, flag or rule without reading the documentation.

## Scope

- In: the Terraform CLI and the configuration language, kept general. Companion tools (linters, doc generators, scanners, wrappers, PR
  automation, version managers, the language server) and OpenTofu as the open source alternative.
- Out: cloud-specific resources and provider pages (see the `azure` topic for Azure), Terraform Stacks and query configuration, and HCP Terraform
  and Terraform Enterprise beyond the `cloud` block and the workflow differences the docs mention.
- Licence: Terraform 1.6.0 and later is under the Business Source License 1.1, so it is not open source. The topic says so, and lists OpenTofu.

## Layout

Archetype: tool with a language. Seven tabs (`templates/view.json`):

| Tab | Holds |
|---|---|
| Start | `workflow`: write, init, plan, apply, destroy, automation, what is new |
| Blocks | A picker. `blocks-index` first (every block with its shape and when to use it), then one page per block in three rows: Everyday, Refactoring, Specialised |
| Language | A picker. `language-index` first, then the lookup pages, then providers and versions |
| CLI | `commands`: a cheat sheet by stage, then the commands grouped by task |
| State & ops | A picker: state and backends, check and test, debug and recover |
| Ecosystem | The companion tools and OpenTofu (the shared "others" list) |
| Compare | Refactoring in the configuration or on the command line; workspaces or separate configurations |

Block pages open the same way: one sentence, the fetched syntax skeleton, then arguments, examples and the rules. The lookup pages have no
parts: short tables, one section after another.

## Sources

The official documentation at developer.hashicorp.com/terraform (version 1.17.x "latest"), the v1.17 CHANGELOG and the LICENSE on GitHub for
Terraform. Each companion tool is read from its own site and GitHub repository. Every entry lists the pages it was written from.
Re-check: `make terraform-check` compares the latest releases with `version.analysed`; `make terraform-examples` re-fetches the code examples.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `workflow` | done | Start tab |
| `commands` | done | CLI tab, with the cheat sheet |
| `blocks-index` | done | Judged tiers: everyday, refactoring, specialised |
| `terraform` | done | block |
| `provider` | done | block |
| `resource` | done | block; `lifecycle`, `provisioner` and `connection` are covered inside it |
| `data` | done | block |
| `variable` | done | block |
| `output` | done | block |
| `locals` | done | block; one source |
| `module` | done | block |
| `import` | done | block |
| `moved` | done | block |
| `removed` | partial | which `destroy` value keeps the real object is not stated: see Known gaps |
| `check` | done | block; one source |
| `action` | done | block |
| `ephemeral` | done | block |
| `language-index` | done | files, structure and style |
| `types` | done | all type constraints, conversion rules, `optional()` |
| `setting-values` | done | ways to set a value, precedence, sensitive and ephemeral |
| `meta-arguments` | done | `count`, `for_each`, `depends_on`, `lifecycle`, `provider`, `providers` |
| `references` | done | named values and how to read instances |
| `expressions` | done | conditionals, `for`, splat, `dynamic`, templates, operators |
| `functions` | done | the ones used most, and every built-in by category |
| `dependencies` | done | providers, modules, version constraints, lock file |
| `state` | done | state, backends, locking, workspaces |
| `testing` | done | formatting and validation, `terraform test`, the linters and scanners people add |
| `troubleshooting` | done | logs, a locked state, a failed apply, drift, a plan that wants to destroy the wrong thing |
| `opentofu` | done | alternative |
| `tflint` | done | tool |
| `terraform-docs` | done | tool |
| `terragrunt` | done | tool |
| `trivy` | done | tool; whether it scans Terraform is unconfirmed |
| `checkov` | done | tool |
| `atlantis` | done | tool |
| `terraform-ls` | done | tool |
| `tenv` | done | tool |
| `lifecycle` | dropped | not a block: it is a nested block, covered in `resource` and `meta-arguments` |
| `provisioner` | dropped | not a top-level block, covered in `resource` |
| `stacks` | dropped | out of scope: Terraform Stacks |
| `hcp-terraform` | dropped | out of scope beyond the `cloud` block |

## Known gaps

- `removed`: the page does not say clearly which `destroy` setting keeps the real object, so the entry points to the page instead of stating it.
- `locals` and `check` cite one source each (validation warns).
- Unconfirmed in the data: when Terraform started (the first tag has no dated release), the licence before 1.6.0, how OpenTofu was forked and how
  it differs, and whether Trivy scans Terraform code.
- The grouping of blocks into tiers, and which functions are "used most", are judgements for this page, not from the docs.
- Whether the 14 blocks are every top-level block type is unconfirmed: the list follows the block reference pages read.
- `make terraform-check` makes one GitHub request per entry that has a `track`. Terraform's entries share one repository, so without a
  `GITHUB_TOKEN` it can hit the 60 requests an hour limit. Set the token before running it.

## Decisions

- Terraform only, no cloud-specific content. Reason: the owner asked for a topic "100% for terraform only"; Azure has its own topic.
- One page per block, then collapsed into a single Blocks tab with a picker. Reason: the owner found 23 tabs too many, and wanted the common blocks
  easier to find than the rare ones.
- Tabs are organised by task (start, blocks, language, CLI, state and operations) rather than by documentation section. Reason: the owner found
  the earlier layout "all over the place", and reference lookup is by question.
- Lookup tables, not articles, for the language. Reason: the owner kept missing lists such as the variable types.
- Code examples are fetched from the official pages and shown unchanged, never pasted. HCL uses `lang: text` because the shared page only
  knows yaml, shell and text.
- The version shown is the Terraform CLI's, v1.17.1, for every Terraform entry. Companion tools carry their own versions.
- DevOps loop stages: code, deploy. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.

## Updating

When a new Terraform release appears: run `GITHUB_TOKEN=... make terraform-check`, read the CHANGELOG for that minor version and the pages named
in each affected entry's `sources`, then update `version`, the facts that changed and `checked` together, and run `make terraform-examples`.
For a new block type: add a page in the Blocks group and a row in `blocks-index`, and list it here. Regenerate nothing by hand in
`data/examples.json`.
