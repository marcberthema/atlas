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

## Planned: the lenses view

Replaces the earlier idea of an Azure estate view and an application view with areas. One page, `/lenses/`: a base picture of an application,
five lenses (application, network, infrastructure, security, monitoring) that highlight roles, a stack filter that changes the labels
(generic, Azure, open source), and a second view for the organization level (tenant, subscriptions, resource groups). It has its own
catalogue of roles and products, so it is not built from topic metadata like the DevOps loop. The spec is `views/lenses/docs/spec.md`; the
visual reference is `docs/mockups/lenses.html` (sample text, not verified). Not built yet: the spec has to be approved first.
