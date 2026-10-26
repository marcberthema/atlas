"""What every Atlas page shares: the topic registry, the top banner and the footer disclaimer.

Templates carry two markers, filled in at build time so the page stays plain static HTML:
  <!--__BANNER__-->      right after <body>
  /*__BANNER_CSS__*/     inside <style>
  <!--__FOOTER__-->      just before </body>
Links are relative and name index.html, so they also work from file://.
"""
import html
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DIST = SITE / "dist"
BANNER_MARK = "<!--__BANNER__-->"
CSS_MARK = "/*__BANNER_CSS__*/"
FOOTER_MARK = "<!--__FOOTER__-->"

CSS = """
.atlas{display:flex;gap:6px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:0 0 8px;margin:0 0 12px}
.atlas a{color:var(--fg);text-decoration:none;padding:4px 12px;border-radius:8px;border:1px solid transparent}
.atlas a:hover{border-color:var(--rule)}
.atlas a:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.atlas-foot{border-top:1px solid var(--rule);margin-top:28px;padding-top:10px;color:var(--mut);font-size:.85rem}
.atlas-foot p{margin:0 0 4px}
.atlas .home{font-weight:700;color:var(--acc);margin-right:6px}
.atlas a[aria-current=page]{background:var(--acc);color:var(--bg);font-weight:600}
"""


FOOTER = (
    '<footer class="atlas-foot"><p>Everything here is collected with AI assistance from public sources, and it changes. '
    'Always check the real source (the links and dates on each entry) before relying on it. '
    'Entries marked <b>?</b> or "unconfirmed" haven\'t been verified yet.</p>'
    '<p>This is a personal project, not an official resource of Microsoft, HashiCorp, Argo CD or any other product named here.</p></footer>')


def load():
    return json.loads((SITE / "topics.json").read_text(encoding="utf-8"))


def published():
    """Topics that are built and shown. An entry with "draft": true is an idea: it never reaches dist/."""
    return [t for t in load()["topics"] if not t.get("draft")]


def check():
    """Exit 1 when topics.json is inconsistent: ids, published topics need a folder, drafts must not leak into dist/."""
    bad, seen = [], set()
    for t in load()["topics"]:
        i = t.get("id", "")
        if not i or not t.get("label"):
            bad.append(f"topic needs an id and a label: {t}")
        if i in seen:
            bad.append(f"duplicate topic id: {i}")
        seen.add(i)
        if t.get("draft"):
            if (DIST / i).exists():
                bad.append(f"draft topic {i} has a dist/{i} folder: remove it")
        elif not (SITE / "topics" / i / "Makefile").exists() or not t.get("description"):
            bad.append(f"published topic {i} needs topics/{i}/Makefile and a description (or set \"draft\": true)")
    for line in bad:
        print("bad:", line)
    print(f"topics {len(seen)} published {len(published())} drafts {len(seen) - len(published())} bad {len(bad)}")
    return 1 if bad else 0


def banner(current, prefix):
    """`current` is a topic id or None for the landing page; `prefix` is "../" from a topic page, "" from the landing."""
    reg = load()
    links = "".join(
        '<a href="{p}{id}/index.html"{cur}>{label}</a>'.format(
            p=prefix, id=t["id"], label=html.escape(t["label"]), cur=' aria-current="page"' if t["id"] == current else "")
        for t in published())
    return '<nav class="atlas" aria-label="Topics"><a class="home" href="{}index.html">{}</a>{}</nav>'.format(
        prefix, html.escape(reg["name"]), links)


def apply(page, current):
    """Fill the banner markers of a topic page."""
    assert all(page.count(m) == 1 for m in (BANNER_MARK, CSS_MARK, FOOTER_MARK)), "template needs one banner, one banner css and one footer marker"
    return page.replace(BANNER_MARK, banner(current, "../")).replace(CSS_MARK, CSS).replace(FOOTER_MARK, FOOTER)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["ids"]:
        print(" ".join(t["id"] for t in published()))
    elif sys.argv[1:] == ["check"]:
        sys.exit(check())
    else:
        sys.exit("usage: atlas.py ids|check")
