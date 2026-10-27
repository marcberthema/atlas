# Enterprise topologies (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/topologies/`.

Same shape as the GitOps topic: `data/topologies.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/topologies/index.html` with `templates/index.html`. Python 3 standard library only.

`data/topologies.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md` for the format. `scripts/validate.py` (`make validate`)
checks it. Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: How systems talk to each other (hub-and-spoke, mesh, tree, bus, ring), where each shows up in networks, services, messaging and data, and the products that implement them. Open source tools are tracked with versions. The Azure and AWS network services are references because the shapes are most visible there.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. For a concept the version is the page it was read from and that page's date. `license` is `n/a` for a concept,
and the validator then does not ask for a `track`. `started` is only `confirmed` when the source gives the date.

The page has one tab per main entry (the `TABS` list in `templates/index.html`, ids must be entry ids), then the rest and Compare.

Refreshing: `make check` lists what changed for the entries that have a `track` (releases, archived repositories, CNCF levels; `LINKS=1` for source and link urls) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every entry that has a GitHub repository and releases.

The last tab, Standard topologies, shows every entry of the group `reference` in full (the template's `group` option on a tab). They are reference designs taken from vendor or project docs, so each says whose docs it comes from and which shapes it uses. Do not call one a standard unless a source does.

Diagrams: an entry may have `diagrams` (see docs/data-model.md). The page draws them as inline SVG from the spec, so there is no image file and no script from outside. A diagram only restates what the entry's text and sources say. Keep labels short enough to fit their node, and check the page in a browser after changing one.
