# Azure DevOps: spec

Status: published (CI/CD family). Azure DevOps Services docs read 2026-11-08 (YAML schema pages dated 2026-09-23). Data checked 2026-11-08. Format: `docs/topic-spec.md`.

## Purpose and audience

A reference for people who use Azure DevOps day to day: what each service does and where its settings live, and above all the YAML pipeline language,
with every keyword and many official snippets, so the exact syntax can be found without reading the documentation. It is a lookup, not a tutorial.

## Scope

- In: the five services (Boards, Repos, Pipelines, Test Plans, Artifacts), the things around them (organization and projects, security, agents, environments and
  service connections, dashboards and analytics, extensions, CLI) and the complete YAML pipeline language: schema keys, template expressions, functions,
  predefined variables, logging commands and conditions.
- Out: classic (designer) pipelines and classic release pipelines beyond a mention, Azure DevOps Server installation and administration, the REST API reference,
  every individual task (the task reference is linked, not copied), extension development, and prices (the free tier is stated, paid access is linked).
- Rule: Azure DevOps Services is the subject. Where Azure DevOps Server differs, the source page says so and the entry says "Services" or "Server" only when the page does.
- Not Azure itself: Terraform and Azure resources belong to the `terraform` and `azure` topics.

## Layout

Archetype: product family, with one very large lookup group. Five tabs (`templates/view.json`):

| Tab | Holds |
|---|---|
| Start | `overview`: the services, how they fit together, organization and project, hosting options, free tier |
| Services | A picker, one entry per service and per supporting area, in two rows: the five core services, then the areas around them. `services-index` first |
| YAML pipelines | A picker with one entry per part of the language, in rows: Start, Triggers, Structure, Data, Reuse and logic, Run. `yaml-index` first lists every keyword and where it lives |
| Ecosystem | The shared "others" list: agent, tasks, CLI, MCP server |
| Compare | Variable syntaxes, parameters against variables, trigger types |

Service entries open with what the service is, then where things live and the limits worth knowing. The YAML pages open the same way: one sentence,
the fetched syntax blocks (every key of that part, unchanged), the official examples, then a table of the traps. The YAML section has one entry per
schema area so that every schema page is reachable from `yaml-index`.

## Sources

learn.microsoft.com/azure/devops (Azure DevOps Services; pages show "Azure DevOps Services | Server" and a last-updated date). The YAML schema is
read from the YAML schema reference (`pipelines/yaml-schema/`, 75 pages from its table of contents), expressions, templates, variables, conditions, resources and
logging commands from the Pipelines process pages. Repositories read for release tracking: microsoft/azure-pipelines-agent, microsoft/azure-pipelines-tasks,
Azure/azure-devops-cli-extension, microsoft/azure-devops-mcp (all MIT). Azure DevOps Services itself is a hosted product with no version: each entry shows the
date of its page. Re-check: `make azure-devops-check` compares the tracked releases and `make azure-devops-examples` re-fetches every code block.

## Coverage

| Item | Status | Notes |
|---|---|---|
| `overview` | done | Start tab |
| `services-index` | done | Services tab, first |
| `boards` | done | service |
| `repos` | done | service |
| `pipelines` | done | service |
| `test-plans` | done | service |
| `artifacts` | done | service |
| `organization` | done | projects, teams, access levels, billing |
| `security` | done | permissions, authentication, tokens, auditing, pipeline security |
| `agents` | done | Microsoft-hosted, self-hosted, scale sets, pools |
| `connections` | done | environments, service connections, variable groups, secure files |
| `reporting` | done | dashboards, Analytics, wiki, notifications |
| `extend` | done | extensions, service hooks, CLI |
| `yaml-index` | done | every keyword, with its entry |
| `yaml-pipeline` | done | top level keys |
| `yaml-trigger` | done | trigger, pr, schedules, resource triggers, filters |
| `yaml-stages` | done | stages |
| `yaml-jobs` | done | jobs, strategy, container, workspace |
| `yaml-deployment` | done | deployment jobs, strategies, hooks, environment |
| `yaml-steps` | done | every step type |
| `yaml-tasks` | done | task step, versions, catalogue by category |
| `yaml-pool` | done | pool, demands, hosted images |
| `yaml-variables` | done | variables and the three syntaxes |
| `yaml-parameters` | done | parameters and their types |
| `yaml-predefined` | done | predefined variable names |
| `yaml-resources` | done | resources |
| `yaml-templates` | done | templates and extends |
| `yaml-expressions` | done | template expressions, functions |
| `yaml-conditions` | done | conditions and status functions |
| `yaml-artifacts` | done | publish, download, cache |
| `yaml-logging` | done | logging commands |
| `azure-pipelines-agent` | done | tool |
| `azure-pipelines-tasks` | done | tool |
| `azure-devops-cli` | done | tool |
| `azure-devops-mcp` | done | tool |

## Known gaps

- Azure DevOps Services has no release: the "version" is the docs page date, and entries read from several pages show the newest one.
- Task inputs are not covered: the task reference has one page per task and is linked, not copied.
- The code blocks of the process pages were chosen by hand (the schema pages are included whole); some long pages (variables, templates) are shown in part.
- Descriptions of the predefined variables are written here from the variable names on the page and a spot check of the enumerated values; the page itself is the authority.
- `yaml-tasks` lists the six task categories, not every task name.
- The azure-devops-mcp entry does not list the tools of the server (not read).
- Wiki, classic release pipelines and the REST API are not covered. The wiki page was not reachable when the topic was written.
- Azure DevOps Server differences are noted only where a page states them.

## Decisions

- Decided without a review step: the request asked for a branch and a pull request when finished, so the owner reviews the spec together with the data in the pull request.
- DevOps loop stages: plan, code, build, test, release, deploy. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.
- One entry per schema area, not one per keyword page: 75 schema pages would make a picker nobody scans. Every keyword is listed in `yaml-index` with the entry that holds it.
- Syntax is the fetched block from the schema page, which lists every key of the part with Microsoft's own comments. The tables written here only cover traps and defaults.
- Azure DevOps Services is a hosted product, so there is no release to analyse: `version.analysed` is the docs page date, as in the Cloudflare topic.
- Paid features (Basic + Test Plans, paid parallel jobs, extra Artifacts storage) are stated as a fact with a link, never as a subject.

## Updating

Re-read the YAML schema table of contents (`pipelines/yaml-schema/toc.json`) for new or removed pages and the "last updated" dates; `make azure-devops-examples` reports
changed or missing code blocks; `make azure-devops-check` reports new releases of the tracked repositories. Then update `version`, the facts and `checked` together.
