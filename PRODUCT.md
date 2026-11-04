# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Engineers looking something up in the middle of a task (the author first, then anyone): what a service provides and requires, how two things relate, which version was analysed, how to build it with Terraform or a pipeline. They also browse more slowly to learn how topics and services connect.

## Product Purpose

Atlas is a public knowledge base of references: a set of facts per topic (Azure with Terraform, Terraform, GitOps, GitHub Actions, identity providers, certificates, enterprise topologies, architecture patterns), kept in JSON and generated into static pages. It centralises knowledge and points to where it lives; it is not Q&A. Success is finding one fact, its source and its version in seconds, and understanding how topics relate when browsing.

## Positioning

Every entry links its sources and shows the version analysed and the check date, and a daily check flags when upstream changes. Cross-cutting views (lenses, the DevOps loop) show relationships between topics that no single vendor's documentation shows.

## Operating Context

Pages are generated from JSON by Python and committed to `dist/`, then published as static assets on Cloudflare. Topics are grouped in four families (IaC, CI/CD, Development, Enterprise) plus cross-topic views. Search covers every entry. A banner with two sticky rows (families, then topics) sits on every page.

## Capabilities and Constraints

- Today: static pages, no server, must work from `file://`. The redesign exploration lifts this: new fonts, frameworks, dependencies and build steps are all open for the mocks. Whether any of it ships is a later decision.
- Everything is public and general knowledge; no employer or client material.
- Terminology: "service" is a type, "resource" an instance; "entry" is the unit of a topic.

## Brand Commitments

Name "Atlas". Nothing else is binding for this exploration: information architecture, navigation and page structure are open (user, 2026-11-03).

## Evidence on Hand

Real content exists for all topics in `topics/*/data/*.json`, the Lenses catalogue in `views/lenses/data/lenses.json`, and the current pages in `dist/`. No testimonials, usage numbers or customers exist; none may be invented.

## Product Principles

- Lookup first, learning second: the fastest path to one fact never gets longer.
- Every claim shows its source and version.
- Relationships between topics are the thing only Atlas shows; make them visible.
- Public and general: nothing personal, nothing proprietary.

## Accessibility & Inclusion

Keyboard operable throughout, visible focus, screen-reader state announcements, respects reduced motion and light/dark preference. Required standard not formally set; assume WCAG 2.2 AA.
