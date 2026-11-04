# Claude Code setup

Skills, plugins and rules that make Claude Code more efficient, collected from videos and checked against their repositories. One
command installs the global part for your account, another installs the per-project part into a project.

Not published; see the [root README](../README.md). The rules for working on this folder are in [CLAUDE.md](CLAUDE.md).
Checked **2026-11-03** (versions below are the ones read that day). Constraint behind every choice: **one Claude Pro subscription, no extra
money**. Pro limits are a usage window, so the cost that matters is the context a tool adds to every session, not the price.

## Use it

```bash
# 1. Global, for the account that runs it (status line, working rules, plugins). Needs claude and python3, and a GitHub ssh key.
make setup-dry-run         # what would happen
make setup                 # do it; ARGS="--only superpowers" turns on one more item
# 2. One project: the UI skill (Impeccable) and a UI rules block in its CLAUDE.md
make project-dry-run PROJECT=~/work/my-app
make project PROJECT=~/work/my-app
```

From the repository root the same targets are `make claude-setup`, `make claude-project PROJECT=<path>`. `make list` and `make project-list`
show what the profile ([setup/profile.json](setup/profile.json)) turns on. Both scripts are safe to run again.

What `make setup` does: installs the status line (the script from [../workstation/setup/](../workstation/setup/claude-statusline.py)),
puts the [working rules](setup/global-rules.md) in `~/.claude/CLAUDE.md` between markers (the rest of the file is kept, a backup is made the
first time), and installs the plugins at user scope. What `make project` does: installs the plugins at project scope (they are written to
`<project>/.claude/settings.json`, so they follow the repository) and puts the [UI rules](setup/project-rules.md) in `<project>/CLAUDE.md`.
After either, start a new Claude Code session. Plugins that run hooks ask you to approve them.

## What is installed

Always-on is the context the plugin adds to **every** session, measured with `claude plugin details <plugin>` (an estimate). On-invoke is paid
only when a skill runs.

| Item | Where | Default | Version | Always-on | Source |
|---|---|---|---|---|---|
| Status line | global | on | n/a (our script) | 0 | [workstation](../workstation/setup/claude-statusline.py) |
| Working rules | global | on | n/a | ~150 (CLAUDE.md) | [global-rules.md](setup/global-rules.md) |
| **ponytail** | global | on | 5.3.3 | ~430, plus ~1.2k injected at session start (estimate) | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| **claude-code-setup** | global | on | 1.0.0 | ~100 | [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) |
| **context7** | global | on | commit a2e251d9b97b (no version) | ~0 measured; its 2 tool schemas load at run time and were not counted | [Upstash, official marketplace](https://github.com/upstash/context7) |
| **document-skills** (docx, pdf, pptx, xlsx) | global | on | no version | ~760 | [anthropics/skills](https://github.com/anthropics/skills) |
| example-skills (12 skills incl. skill-creator) | global | off | no version | ~940 | [anthropics/skills](https://github.com/anthropics/skills) |
| superpowers | global | off | 7.0.1 (plugin.json 7.0.0) | ~710 | [obra/superpowers](https://github.com/obra/superpowers) |
| graphify (CLI) | global | off | 0.9.101 | 0 until used | [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) |
| playwright-cli (CLI) | global | off | not found | 0 until used | [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli) |
| taste-skill | project | off | 2.1.5 | ~250 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) |
| **impeccable** | project | on | 4.8.0 | ~310 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) |

Global total with the defaults: about 2.6k tokens at the start of a session, plus Context7's tool definitions (not measured) (Ponytail's start-of-session text is an estimate from reading its hook code, see its row; each subagent adds ~700 more). A project with Impeccable adds about 0.3k. Turn an item off in the profile,
or install it for one run with `--only <id>`. The plugin and marketplace names above were confirmed by installing them (in a throwaway home).

## The full list, by family

Verdict: **every project** (global, cheap), **per project** (install where it pays off), **skip**, **later**. "Verified" means the repository
README or manifest was read on the check date; "unverified" means it comes from third-party articles or could not be identified.

### 1. Token optimisation

| Tool | What it does | Verdict | Notes |
|---|---|---|---|
| **Ponytail** | Makes the agent justify every line and prefer the smallest solution (YAGNI, standard library first). Adds `/ponytail`, `-review`, `-audit`, `-debt`, `-gain`, `-help`, and a band above the prompt (cost, tokens, tests). MIT. | **Every project** (installed) | Small but real gain: the best independent figure found is about 10% per task (JetBrains test, [summarised here](https://news.creeta.com/en/ponytail-claude-code-token-benchmark-2026/); the article itself was not read). The author's 47-94% figures are a per-task ceiling; "-54%" is lines of code, not tokens. Little gain on sessions that write little code. It runs three hooks (needs `node` on the PATH). `claude plugin details` shows only ~430 tokens (skill descriptions); the SessionStart hook also injects its ruleset (~700 tokens) and a codebase map (~500) once per session start, resume, `/clear` and compaction, and each subagent gets the ruleset again (~700). Ordinary prompts inject nothing on Claude Code (read from `hooks/*.js`; token counts are estimates). Its status line script only shows a `[PONYTAIL]` mode badge: the cost, tokens, reuse and tests are in a separate "band" UI above the prompt. `/ponytail off` or `lite` turns it down; `ledger` writes a local csv under `~/.config/ponytail/`, a webhook is optional and empty by default. It can offer its own status line: decline, ours is already set. Remove with `node scripts/uninstall.js` from the plugin, then `/plugin remove ponytail`. |
| Caveman | Terse replies. | **Skip** | Claims 65-75% fewer output tokens; independent tests found 12-23%, and output is only about 1-3% of a session's billed tokens, so the real saving is tiny. It does the same job as Ponytail's short replies. Pick one: Ponytail. [Measurements](https://www.implicator.ai/caveman-claude-code-skill-cuts-output-20-your-bill-barely-notices-2/). `/caveman-compress` (rewrites CLAUDE.md smaller) is a separate feature, unverified. |
| Headroom | Compresses tool output, logs and files before the model sees them; the original can be retrieved. | **Later** (trial on a log-heavy project) | Targets the input side, which is the real cost. Self-reported 60-95%. Several repositories carry the same README and the canonical one was not confirmed (one article names `chopratejas/headroom`): confirm before installing. [Overview](https://silenceper.com/en/article/2026-06-14-headroom-ai-agent-context-compression/). |
| claude-mem | Records sessions in a local database and re-injects context. | **Skip** | Duplicates Claude Code's built-in memory; two systems to keep. Needs Bun. [Overview](https://www.augmentcode.com/learn/claude-mem-persistent-memory-claude-code). |
| freeLLMApi / OmniRoute | Self-hosted proxies that put many providers' free tiers behind one endpoint. | **Later** (fallback, see below) | Not part of the install: Claude Code support is unverified for both. |

### 2. General workflow

| Tool | What it does | Verdict | Notes |
|---|---|---|---|
| **Working rules** (the "Karpathy" style rules) | Think before coding, smallest change, surgical edits, a checkable "done", honest reports. | **Every project** (installed) | Written in our own words in [global-rules.md](setup/global-rules.md); the exact rules attributed to Karpathy in videos were not read, so they are not copied. |
| **claude-code-setup** | Reads a repository and recommends hooks, subagents, skills, plugins and MCP servers. This is the "read my repo and propose skills" plugin. | **Every project** (installed, run once per new project) | Official Anthropic plugin; its skill `claude-automation-recommender` is read-only. Costs tokens only when run (~2.6k). Ask Claude "recommend Claude Code automations for this repo". |
| **/code-review, /security-review** | Built in. | **Every project** | Use `low` or `medium` effort on Pro; the higher levels start many reviewers. |
| **anthropics/skills** | Anthropic's example skills in two plugins: `document-skills` (docx, pdf, pptx, xlsx) and `example-skills` (skill-creator, mcp-builder, webapp-testing, frontend-design and more). | `document-skills` installed; `example-skills` **off** | `example-skills` costs ~940 tokens a session and includes `frontend-design`, a third UI skill that overlaps taste and Impeccable. Turn it on for a session of building skills: `make setup ARGS="--only example-skills"`. Licenses are mixed (see the repo). |
| **Superpowers** | A development method as skills: brainstorm, plan, subagent per task with review, test first, finish the branch. MIT, very active (v7.0.1, 2026-10-21). | **Per project** (off; trial on a new project) | Bootstrap ~700 tokens a session. The default flow dispatches a subagent per task and the README says runs can last "a couple hours": heavy on a usage window. Use `executing-plans` (inline, the cheaper mode). Savings claims are the maintainers' own. Behaviour changes between versions. Overlaps the working rules, /code-review and debugging. |
| Task Observer | Meta-skill that logs repeated workflows and friction into `skill-observations/log.md` and proposes skill updates on a schedule. CC BY 4.0, by Eoghan Henn. | **Skip** for now | Pays off only once you have a library of your own skills. The playbook version is a 994-line CLAUDE.md loaded every session; the modular version (`rebelytics/one-skill-to-rule-them-all`, not read) loads on demand. [Playbook](https://www.claudecodehq.com/playbooks/task-observer). |
| agent-skills (Addy Osmani) | 24 lifecycle skills plus a meta skill that routes work to the right one (spec, plan, build, test, review, ship), 9 slash commands and 4 agent personas. MIT, v0.6.15 (2026-10-31), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). | **Not installed**; a source of ideas (catalogue below) | Measured ~3,000 tokens added to every session (34 skills counting the commands, 4 agents), because the skills fire automatically. A spec-driven workflow of your own would then have a second spec, plan and ship method running beside it that triggers by itself, while your manual-only skills stay silent. Its `/review` also clashes with the built-in (needs `/agent-skills:review`). Decision: `interview-me` is written as an own skill in your own skills repository; other skills are imported the same way when one proves useful. |

### 3. Making agents better

| Tool | What it does | Verdict | Notes |
|---|---|---|---|
| **Graphify** | Turns a code base (and docs, PDFs) into a queryable graph: `graph.html`, `GRAPH_REPORT.md`, `graph.json`. Python, Apache-2.0 / MIT, v0.9.101, active (2026-11-02). | **Per project** (off): to understand a code base you have never opened | Install `uv tool install graphifyy` (two y; other `graphify*` packages are not official), then `/graphify .`. Code parsing is local and free; docs, PDFs and labelling use your session's model. `graphify claude install` adds hooks that intercept search and reads: skip it at first. 726 open issues. "80% fewer tokens" is the vendor's claim. |
| **Playwright CLI** | Drives a browser from the shell; saves page snapshots to disk and sends a summary. Apache-2.0. | **Per project** (off): testing your own web apps | Package `@playwright/cli` (the README never names `@anthropic-ai/playwright-cli`). `playwright-cli install --skills` adds its skills to a project. It starts its own browser: **no logins**. Latest release date not found. Cannot replace Claude in Chrome for anything behind your accounts; use both. |
| Claude in Chrome | Drives your real Chrome profile. | **Per project**, when logged-in pages are needed | Not installed by this repo (browser extension, paid plans). Does not work from WSL; the Windows setup in `workstation/` covers it. |
| ECC (Everything Claude Code) | A large bundle of agents, skills, rules and hooks. MIT, [affaan-m/ECC](https://github.com/affaan-m/ECC). | **Skip** as a whole | Too much context, and it encourages multi-agent runs. Take single pieces if one appeals. Mirrors exist; install from the official repo only. |
| agency-agents | About 230 persona files by division. MIT, [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents). | **Skip** (or one division) | Installing all of them lists every description in every session (the mechanism is from general knowledge, not the page). If you try it: `./scripts/install.sh --tool claude-code --division engineering`. Writing two or three agents of your own is cheaper and fits better. |
| Firecrawl | Web pages to clean markdown. | **Later** | Unverified. The built-in web search and fetch cover most needs. |
| **Context7** | Fetches current, version-specific library documentation into the session, so the agent stops guessing APIs from stale training data. Official plugin `context7@claude-plugins-official`, by Upstash; connects to their hosted server (no Node needed). | **Every project** (installed) | Works anonymously with default limits; a free key (`CONTEXT7_API_KEY`) raises them. Free allowance is about 1,000 requests a month per June 2026 sources, which disagree and are not an official page: check [context7.com/plans](https://context7.com/plans). Library names and questions go to Upstash. Helps most with fast-moving libraries (Terraform providers, web frameworks). [FAQ](https://context7mcp.pages.dev/faq). |
| Strix | Open-source AI pentester: agents run your app in a Docker sandbox (proxy, browser, shell), find weaknesses and confirm them with a working proof of concept. Apache-2.0, v1.7.0 (the page shows "05 Oct", no year), 73.6k stars, [usestrix/strix](https://github.com/usestrix/strix). Not a skill: a CLI. | **Later**, on an app of your own | Black-box (`strix --target https://your-app.com`), white-box (`--target ./app`) or both; `--scan-mode quick`, `standard` or `deep` (deep is the default and takes 1-4 hours per the docs). Needs Docker and an LLM: `STRIX_LLM` (LiteLLM names) plus `LLM_API_KEY`. **A paid API key unless the model is local**: Ollama or any OpenAI-compatible endpoint works (`LLM_API_BASE`), so a free proxy might, but that is unverified, and a weak model probably finds little. Frontier OpenAI, Anthropic and Gemini models require a cyber access program per the docs. Use `--max-budget <USD>` and `STRIX_TELEMETRY=0` (telemetry is on by default). **A local directory is mounted writable**: commit first; v1.7.0 adds read-only mounts. Install is `curl -sSL https://strix.ai/install \| bash`. Authorized use only (your own systems or written permission). Latest release year and per-scan token cost not found. [Docs](https://docs.strix.ai/usage/cli). |
| Shannon | Autonomous AI pentester (Keygraph), built on the Anthropic Agent SDK. [KeygraphHQ/shannon](https://github.com/KeygraphHQ/shannon) | **Skip** for now | The free edition is white-box (needs your source); black-box is in the paid Pro edition. Needs Docker and an API key or OAuth token. Strix does both modes for free software. Many look-alike repos. |
| 21st Magic MCP | Generates UI components from a prompt, with an API key from 21st.dev. | **Skip** | Free allowance of 3 to 5 generations a month (sources disagree; official page uses a token model); paid beyond that. Impeccable or taste-skill cover the need without a key. [Pricing](https://21st.dev/pricing). |
| Perplexity, second-brain, prompt master | Research, notes, prompt tooling. | **Skip** | Could not be identified: unverified. They overlap built-in search and memory. |

### 4. UI

| Tool | What it does | Verdict | Notes |
|---|---|---|---|
| taste-skill | Art direction for websites, product pages, dashboards and app screens, with a library of design directions, pictures from open collections and a browser inspector. MIT, v2.1.5 (2026-10-25). The one skill is `design-taste-frontend`. | **Optional** (off): for a fresh visual direction, `make project PROJECT=<path> ARGS="--only taste-skill"` | About 9.6k tokens each time it fires. Needs Node 22+ and Chrome, Edge or Chromium for its tools (the project script warns). Older variants live in a separate repo (`taste-skill-classics`) and run only when called by name. No dials in the current version. |
| **Impeccable** | A design vocabulary for the agent: one skill, 24 commands (`/impeccable critique`, `audit`, `polish`, `bolder`, `quieter`, `typeset`, `colorize`, ...), plus checks that run on UI edits. Apache-2.0, v4.8.0 (2026-10-26), by Paul Bakaus. | **Every UI project** (project install, the default) | Builds on Anthropic's `frontend-design`. The plugin runs hooks (session start, after edits, on stop): "scans every UI file your agent edits" per its README. Its README says the first edit can download its engine, and it fetches design directions from impeccable.style (disable: `npx impeccable telemetry off` or `DO_NOT_TRACK=1`). Whether the plugin route enables the edit-scan hook as the `npx impeccable install` route does is unconfirmed. |
| awesome-design-md | Turns a site's look into a reusable design file. | **Later** | Unverified (only a third-party mention). |
| Apple design skill | A reviewer grounded in Apple's Human Interface Guidelines (123 pages). [dickwu/apple-design-skill](https://github.com/dickwu/apple-design-skill) | **Per project**, mobile or Apple-style UI only | **No license stated**; unofficial; the snapshot goes stale. `npx skills add dickwu/apple-design-skill -a claude-code` (third-party installer). |
| lemo-opuscar | Writes code that renders short films (66 styles). | **Skip** | Not a UI skill. 30-60 minutes and many tokens per film; tuned for one model; needs ffmpeg 7+. |
| img2threejs | 3D from images. | **Skip** | Unverified; only for 3D work. |

### agent-skills catalogue (to pick from later)

Read 2026-11-03 from the README and `claude plugin details agent-skills@addy-agent-skills` (v0.6.15, MIT). The skill bodies were **not** read,
so the purposes below are the README's one-liners. Cost is the estimate from `claude plugin details`: always-on is paid every session if the
skill is installed, on-invoke each time it fires. Installed one at a time, a skill costs only its own always-on figure.

How to import one: write your own version in your skills repository, using the idea (cheapest, no licence question, fits your conventions), or copy
its folder (MIT: keep the copyright notice), or `npx skills add addyosmani/agent-skills --skill <name>` (third-party installer that runs code).
Pick one when a real task would have used it; the "Overlap" column says what you already have.

| Skill | Stage | Purpose (README) | Always-on / on-invoke | Overlap and fit |
|---|---|---|---|---|
| `interview-me` | Define | One question at a time to find out what you actually want | ~130 / ~3.6k | **Chosen**: write an own version. Nothing equivalent in the setup |
| `doubt-driven-development` | Build | Fresh-context adversarial review of a non-trivial decision (claim, extract, doubt, reconcile, stop) | ~130 / ~4k | Candidate. Not covered elsewhere here |
| `constraint-driven-development` | Define | A `CONSTRAINTS.md` quality bar; catches an agent skipping tests or silencing checks | ~230 / ~5.3k | Candidate. Costly always-on for its size |
| `source-driven-development` | Build | Ground framework decisions in the official docs, with citations | ~90 / ~2.4k | Candidate; pairs with Context7 |
| `idea-refine` | Define | Turn a vague idea into concrete proposals | ~90 / ~2.3k | Candidate before an epic is written |
| `using-agent-skills` | Meta | Maps incoming work to the right skill and sets shared rules | ~70 / ~2.4k | Only useful with the whole pack |
| `spec-driven-development` | Define | Writes a PRD (objectives, commands, structure, style, testing, boundaries) before code | ~120 / ~3.1k | Overlaps your own spec method: skip |
| `planning-and-task-breakdown` | Plan | Splits a spec into small, verifiable tasks with acceptance criteria | ~70 / ~2.6k | Overlaps your own epics and specs: skip |
| `incremental-implementation` | Build | Thin vertical slices: implement, test, verify, commit | ~100 / ~2.2k | Partly covered by the working rules |
| `test-driven-development` | Build | Red, green, refactor; test pyramid; browser testing | ~120 / ~4k | Overlaps Superpowers (off) |
| `context-engineering` | Build | Feed the agent the right information: rules files, context packing, MCP | ~60 / ~3.7k | Overlaps CLAUDE.md practice |
| `frontend-ui-engineering` | Build | Component architecture, design systems, state, responsive design, WCAG 2.1 AA | ~90 / ~2.9k | Overlaps Impeccable |
| `api-and-interface-design` | Build | Contract-first design, Hyrum's Law, error semantics, boundary validation | ~70 / ~3.6k | Possible fit for the SaaS apps |
| `browser-testing-with-devtools` | Verify | Chrome DevTools MCP: DOM, console, network, performance | ~90 / ~3.4k | Overlaps Playwright CLI and Claude in Chrome |
| `debugging-and-error-recovery` | Verify | Five steps: reproduce, localize, reduce, fix, guard | ~90 / ~2.5k | Overlaps Superpowers' debugging (off) |
| `code-review-and-quality` | Review | Five-axis review, about 100-line change size, severity labels | ~90 / ~5.2k | Overlaps the built-in `/code-review` |
| `code-simplification` | Review | Chesterton's Fence; reduce complexity, keep behaviour | ~110 / ~3.3k | Overlaps Ponytail |
| `security-and-hardening` | Review | OWASP Top 10, auth, secrets, dependency auditing | ~160 / ~4.2k | Overlaps `/security-review` and your own security skill |
| `performance-optimization` | Review | Measure first; Core Web Vitals, profiling, bundle analysis | ~80 / ~4.1k | Useful for web SaaS; nothing equivalent here |
| `git-workflow-and-versioning` | Ship | Trunk-based development, atomic commits | ~160 / ~3.4k | Overlaps your own release flow: skip |
| `ci-cd-and-automation` | Ship | Shift-left, quality-gate pipelines, feature flags | ~60 / ~2.7k | Overlaps your own project templates |
| `deprecation-and-migration` | Ship | Code as liability, migration patterns, zombie code removal | ~90 / ~3.1k | Occasional use |
| `documentation-and-adrs` | Ship | Architecture Decision Records and API docs | ~80 / ~2.7k | Overlaps your decisions log |
| `observability-and-instrumentation` | Ship | Structured logging, RED metrics, OpenTelemetry, alerting | ~90 / ~3.4k | Possible fit for deployed SaaS |
| `shipping-and-launch` | Ship | Pre-launch checklists, staged rollouts, rollback | ~80 / ~2.8k | Overlaps your own milestone closing |

Also in the pack: nine slash commands that are skills too (`/spec`, `/plan`, `/build`, `/test`, `/constraints`, `/review`, `/webperf`,
`/code-simplify`, `/ship`; ~20-30 always-on each) and four agents (`code-reviewer`, `test-engineer`, `security-auditor`,
`web-performance-auditor`; ~50-60 each). Not read: the hook files and the evals.

### Impeccable or taste-skill: one per project

Decision: **Impeccable is the only UI skill installed by default.** It has commands to review (`critique`, `audit`) and to fix (`polish`,
`typeset`, `layout`), which suits a review-first workflow, and it is cheaper when fired (~2.8k against ~9.6k). Add taste-skill to a project only
when you want a fresh visual direction (`--only taste-skill`), and then do not let both steer the same pass. What the sources say:

- taste-skill is a normal skill: Claude loads it when a design task matches its description (inferred; its `SKILL.md` header was not read). Its
  plugin is namespaced (`taste-skill:`), so names do not collide.
- Impeccable is explicit: its commands run when you type `/impeccable <command>`, and its hooks check UI files after edits.
- Neither README mentions the other, so the behaviour of the two together is **untested**.
- A third UI skill is `frontend-design` (inside `example-skills`, off by default); Impeccable started from it. Leave it off.
- Writing "/impeccable critique the pricing cards" is clearer than a general request, and costs nothing.

## Staying inside Pro

- The biggest costs are context size, tool output and subagents. Output wording is a small part.
- Start a fresh session per task (`/clear`), use `/compact` mid-task, and prefer the cheaper model for simple work.
- Install one thing at a time and compare your usage before and after. `claude plugin details <plugin>` shows the always-on cost first.
- Every installed plugin can run code on your machine (hooks, scripts). Read what you install; use the official repository, since mirrors
  and look-alike packages exist (Graphify, Ponytail and ECC all have them).
- Plugins are cloned over SSH, so the account needs a GitHub key.

## Fallback when the Pro window is used up: FreeLLMAPI or OmniRoute

Not installed by the scripts yet. Both are free, MIT, self-hosted proxies that put many providers' free tiers behind one endpoint, and both
document Claude Code (`ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`). Neither uses your Claude login. Read 2026-11-03 from their repositories
and docs; pages that were truncated are marked in the notes below.

| | FreeLLMAPI | OmniRoute |
|---|---|---|
| Repo | [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) | [diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) (the page served was `cheaper-inference/OmniRoute`: confirm the canonical org before `npm install -g omniroute`) |
| Size and activity | 46.9k stars, 23 open issues, 1,045 commits; release date not found | 84.2k stars, 204 open issues, 357 open PRs; v3.8.52 on 2026-10-19 |
| Install | Docker one-liner `curl -fsSL https://freellmapi.co/install.sh \| bash`, or Node 20+ with `npm run dev`; binds to 127.0.0.1 | `npm install -g omniroute` then `omniroute` (Node 22/24; native build step may be blocked), or Docker; dashboard on :20128 |
| Claude Code | Documented: `ANTHROPIC_BASE_URL=http://localhost:3001`, `ANTHROPIC_AUTH_TOKEN=<unified key>` (not `ANTHROPIC_API_KEY`). `npx freellmapi setup-claude` / `launch` | Documented: `ANTHROPIC_BASE_URL` (no `/v1`), `ANTHROPIC_AUTH_TOKEN`. `omniroute setup-claude` writes a separate profile under `~/.claude/profiles/`; `omniroute launch --profile` |
| Anthropic API | `/v1/messages` and `count_tokens`; streaming and tool use "translate across the same router" | Docs target `/v1/messages`; tool calling support is not stated in general terms (only for some providers) |
| Free tiers | 34 providers claimed (Google, Groq, Cerebras, Mistral, OpenRouter, Cloudflare, NVIDIA ...); per-provider limits not read (on freellmapi.co/models) | Bring your own accounts; ~1.62B tokens/month is an estimate across providers, "not an allowance supplied by OmniRoute"; some need a card or KYC (Cerebras, Vertex, LongCat) |
| Routing | `auto`, `auto:smart/fast/cheap/reliable/balanced`; retries up to 20 models, cooldown on 429, counters per key | `auto`, `auto/cheap`, combos; many strategies (20 is from a summary of truncated text) |
| Terms and privacy | Self-assessed terms table (Cohere avoid; Gemini, NVIDIA, Z.ai caution). "Personal experimentation only", "no SLA", "don't expose it to the internet" | 12 providers flagged "avoid" (excluded from auto-routing by default); unofficial web-session and cookie providers exist; one free provider logs every request; nothing found on Claude OAuth terms |
| Money | $0. Optional Premium catalog at $19/yr (free installs get the model list 30 days late) | $0 |
| Surface | One job, small | Large: dashboards, many strategies, OAuth providers, desktop app |

What neither fixes (my reading of the above, not a measurement): free models are weaker than Claude at agent work; Claude Code's own prompt
and tool list are large, so a free tier's per-minute token cap is reached fast; limits and terms change without notice; free providers may
log or train on prompts, so never send private code or secrets; Claude Code assumes a 200K window for unknown models (set
`CLAUDE_CODE_AUTO_COMPACT_WINDOW`).

Recommendation: **FreeLLMAPI first**. Smaller, narrower, Claude Code documented with a launcher, local-only by default. Use OmniRoute only if
it falls short. Run the fallback in its own profile (`CLAUDE_CONFIG_DIR=~/.claude-free`, a `claude-free` alias) so the Pro profile, its
plugins and its login are never touched, and switch on purpose.

## Not verified

Could not be identified or read, so nothing about them is in the install: Strix's release year, token cost per scan and whether a free proxy works as its model, Context7's real always-on cost (tool schemas), the bodies of the agent-skills skills, the per-provider free-tier limits of FreeLLMAPI, whether OmniRoute passes tool calls through reliably, OmniRoute's canonical organisation,
the "Anthropic core pack" (taken to be `anthropics/skills`), Firecrawl, Perplexity, second-brain, prompt master, awesome-design-md,
img2threejs, the canonical Headroom repository, the exact rules attributed to Karpathy, the Task Observer source repository, and the
JetBrains article on Ponytail. Star counts quoted in articles are third-party and change daily; they are not used here.
