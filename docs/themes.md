# Two looks: classic and transit

Spec for building every Atlas page in two looks from the same data, and letting a visitor pick. Status: proposed, not approved.

## Decisions (from the owner, 2026-11-04)

- Both looks are built on every release (`make build`) and both are published.
- A first-time visitor sees **classic** (today's look). Transit is opt-in. Flipping the default later is one constant.
- The transit font (Red Hat Display, SIL Open Font License) is shipped as files inside `dist/transit/`, self-hosted, so pages work from `file://` and load nothing from outside. This is an exception to "no external fonts", for the transit look only.
- The switch is a button in the banner on every page ("Look: Classic / Transit"). It opens the same page, same entry and tab, in the other look and remembers the choice in `localStorage`.

## Layout of dist/

```
dist/index.html, dist/<topic>/index.html, dist/azure/, dist/lenses/, dist/devops-loop/    classic, unchanged URLs
dist/transit/index.html, dist/transit/<topic>/index.html, ...                              transit, same paths under /transit/
dist/transit/fonts/                                                                         font files and their licence
```

Every classic page has a transit twin at the same path. Links inside a tree stay relative and name `index.html`.

## How, without writing every renderer twice

Today each page is one template (`shared/topic.html`, `landing.html`, `lenses.html`, `view.html`, Azure's `index.html`) holding structure, script and CSS, with the data embedded as JSON. The pages draw their content with JavaScript from that JSON.

The plan keeps one structure and one script per page and makes the look a layer:

- Each template's CSS moves to a theme file: `shared/themes/classic/<page>.css` and `shared/themes/transit/<page>.css`. The build picks the theme's CSS, and adds the theme's banner, footer and switch.
- A new kind of content in the data is then drawn once, by the shared script, and appears in both looks.
- Where transit needs different structure (route landing page, Lenses lanes and gutter, the loop), the template gets a small hook that the classic CSS ignores. If a hook would bend the classic page, that page gets a second template file instead, called out in this spec.
- The mocks in `explorations/ui/` are the reference for the look. They are not shipped.

## Phases (one commit per phase, `dist/` regenerated with each)

1. Plumbing: theme argument in the build, the `dist/transit/` tree, the switch and redirect, font files, the transit banner and footer, the About window, dark mode. Landing page in transit.
2. Topic pages (the shared template, 7 topics): entries, tabs, compare, learning layout, code, tables, diagrams, details switch.
3. Azure: tiers, filters, details.
4. Lenses: icons, more spacing between boxes and lanes, lane titles in a gutter, arrows, the Organization view, A to Z, the stack filter and search, deselect.
5. DevOps loop.
6. Release: `make build` builds both, `make validate` checks both trees, docs and `CLAUDE.md` updated.

## Done means

- `make build` and `make validate` exit 0; every classic page has a transit twin; both trees carry the same entries and versions.
- Nothing loads from outside the site; pages open from `file://`; the transit tree contains the font files.
- The switch keeps the page, entry and tab; the saved choice is honoured on every page; no redirect loop.
- Keyboard, focus, `role=status` announcements, reduced motion and light/dark work in both looks (not just visually checked: scripts run, detector clean).
- The classic pages are byte-for-byte unchanged except the new banner button and the theme-file split (diff reviewed).

## Risks and open points

- Nobody can see a render in this setup (no browser tool): every phase ends with the owner looking at it.
- `dist/` is committed, so the repo grows by roughly one more copy of the pages.
- Transit is built to the mocks' three sample entries; real entries (tables, code, diagrams, learning layout) will show gaps in phase 2.
- A feature added to one look only (for example the Lenses Organization view in transit before classic) is not allowed: both read the same data and must offer the same content.
