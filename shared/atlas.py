"""What every Atlas page shares: the topic registry and the top banner.

Templates carry two markers, filled in at build time so the page stays plain static HTML:
  <!--__BANNER__-->      right after <body>
  /*__BANNER_CSS__*/     inside <style>
Links are relative and name index.html, so they also work from file://.
"""
import html
import json
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DIST = SITE / "dist"
BANNER_MARK = "<!--__BANNER__-->"
CSS_MARK = "/*__BANNER_CSS__*/"

CSS = """
.atlas{display:flex;gap:6px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--rule);padding:0 0 8px;margin:0 0 12px}
.atlas a{color:var(--fg);text-decoration:none;padding:4px 12px;border-radius:8px;border:1px solid transparent}
.atlas a:hover{border-color:var(--rule)}
.atlas a:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.atlas .home{font-weight:700;color:var(--acc);margin-right:6px}
.atlas a[aria-current=page]{background:var(--acc);color:var(--bg);font-weight:600}
"""


def load():
    return json.loads((SITE / "topics.json").read_text(encoding="utf-8"))


def banner(current, prefix):
    """`current` is a topic id or None for the landing page; `prefix` is "../" from a topic page, "" from the landing."""
    reg = load()
    links = "".join(
        '<a href="{p}{id}/index.html"{cur}>{label}</a>'.format(
            p=prefix, id=t["id"], label=html.escape(t["label"]), cur=' aria-current="page"' if t["id"] == current else "")
        for t in reg["topics"])
    return '<nav class="atlas" aria-label="Topics"><a class="home" href="{}index.html">{}</a>{}</nav>'.format(
        prefix, html.escape(reg["name"]), links)


def apply(page, current):
    """Fill the banner markers of a topic page."""
    assert page.count(BANNER_MARK) == 1 and page.count(CSS_MARK) == 1, "template needs one banner marker and one banner css marker"
    return page.replace(BANNER_MARK, banner(current, "../")).replace(CSS_MARK, CSS)
