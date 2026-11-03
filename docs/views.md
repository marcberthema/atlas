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

## The lenses view (`lenses`)

Where does a service go? One page, `/lenses/`: a base picture of an application (22 roles in five lanes), five lenses (application, network,
infrastructure, security, monitoring) that highlight roles, a stack filter that changes the labels (generic, Azure, open source; AWS is shown as
soon), an Organization view (tenant, management groups, subscriptions, resource groups and the services tied to each level) and an A-Z list.
A search finds a role, a product or an alias (kafka leads to Message broker). It has a catalogue of its own, so it is not built from topic
metadata like the DevOps loop: `views/lenses/data/lenses.json`, checked by `shared/lenses_check.py` (part of `make validate`), built by
`shared/build_lenses.py` from `shared/lenses.html` into `dist/lenses/index.html`, with the data embedded in the page. `make lenses-check` also
fetches every source link. The spec is `views/lenses/docs/spec.md`; the first visual agreement is `docs/mockups/lenses.html` (sample text).
