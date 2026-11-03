# Architecture and design patterns: spec

Status: published (Development family). Data checked 2026-10-26. Reconstructed from the data and git history, not written before the content:
reasons that the history does not record are marked "reason unconfirmed". Format: `docs/topic-spec.md`.

## Purpose and audience

Reference cards for how software is split by structure and responsibility: application structure, distributed styles, resilience and cloud
patterns, and the classic 1994 patterns. For someone who needs the name, the idea and the trade-off of a pattern quickly.

## Scope

- In: patterns as ideas, in short cards with no code. Sources that are free to read.
- Out: code, and any release tracking. A pattern has no release, so the version shown is the date of the page the card was read from, and
  `license` is `n/a`, which exempts the entry from needing a `track`.

## Layout

Archetype: concepts. Seven tabs: Layered, MVC, Hexagonal, Microservices, Event-driven (the five main entries), All patterns, Compare.
Groups: application structure, distributed systems, resilience and cloud, and the classic patterns (creational, structural, behavioral).
Comparisons (5): presentation patterns; layered, hexagonal and clean; monolith, microservices and serverless; resilience patterns and when to use
which; and one more, see the data.

## Sources

Martin Fowler's articles, Microsoft's Azure Architecture Center pattern pages and the original hexagonal and clean architecture articles, plus
the pages the classic patterns were read from (two sources per card, read 2026-10-26). Each entry lists its pages and their dates.
There is nothing to release-check: re-read a page when its date changes (`make patterns-check` with `LINKS=1` checks that the links still resolve).

## Coverage

| Item | Status | Notes |
|---|---|---|
| `layered` | done | one source |
| `mvc` | done | one source |
| `hexagonal` | done | one source |
| `microservices` | done | |
| `event-driven` | done | |
| `mvp` | done | overview |
| `mvvm` | done | overview |
| `clean` | done | overview |
| `monolith` | done | overview |
| `serverless` | done | overview |
| `cqrs` | done | overview |
| `event-sourcing` | done | overview |
| `saga` | done | overview |
| `api-gateway` | done | overview |
| `bff` | done | overview |
| `strangler-fig` | done | overview |
| `circuit-breaker` | done | |
| `bulkhead` | done | |
| `retry` | done | |
| `sidecar` | done | |
| `cache-aside` | done | |
| `throttling` | done | |
| `queue-based-load-leveling` | done | |
| `competing-consumers` | done | |
| `singleton` | done | all 23 classic patterns are `ref` cards, listed by group in the data |

## Known gaps

- `layered`, `mvc` and `hexagonal` cite one source each (validation warns).
- Start dates: 24 of 46 entries are `started` unconfirmed.
- Not covered: other cloud patterns beyond the nine in the resilience group, domain-driven design, and data-management patterns.

## Decisions

- No code in the cards. Reason: a pattern is an idea, and code would be a copy of someone else's page.
- The version shown is the page date. Reason: the repo rule that a version is always visible, applied to a thing with no release.
- The classic patterns are short `ref` cards in groups, not tabs. Reason unconfirmed.
- DevOps loop stages: plan, code. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.

## Updating

Re-read a page when its date changes, then update `version`, the facts and `checked` together. A new pattern is a card in the matching group with
its sources; add it to a comparison if it competes with an existing one.
