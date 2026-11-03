# Views

A view is a generated page that cuts across topics: it is built from metadata on the topics, never from its own content. A new topic that
declares the metadata appears in the view without editing a diagram. Views live in `topics.json` under `views` and are built into
`dist/<view id>/index.html` by `shared/build_views.py`. In the banner they form a last family, Views.

## Registry

```
"views": [{"id": "devops-loop", "label": "DevOps loop", "description": "..."}]
```

`make validate` checks the id, label and description, that the id does not clash with a topic, and that every stage a topic names exists.

## The DevOps loop (`devops-loop`)

- **Stages.** `stages` at the top of `topics.json`: `id`, `label`, `about` (one line, general knowledge). Eight, in loop order: plan, code, build,
  test, release, deploy, operate, monitor.
- **Placement.** A topic or draft lists the `stages` it belongs to. A topic may belong to several. The assignment is a judgement, recorded in
  the topic's spec (Decisions), not something a source states.
- **Page.** An infinity loop with the eight stages on it (plan to test on the left lobe, release to monitor on the right), then one card per
  stage listing its published topics as links. A stage with no topic says so. Published topics with no stage are listed under the loop.
  Drafts are never shown, like everywhere else.
- **Scope.** The loop is a map of where topics fit, not a claim about how anyone works.

## Planned: the Azure estate and the application views

Same mechanism, with `areas` instead of `stages` and a diagram of areas (for the estate: identity, network, governance, platform, workloads;
for an application: web, API, data, messaging, identity, observability). A topic would declare `placements` (view id, area id). Not built yet:
the areas have to be agreed first, and they must come from public reference architectures.
