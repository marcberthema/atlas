"""Build the generated views (docs/views.md) into dist/<view id>/index.html from topics.json and shared/view.html.

A view has no content of its own: it is drawn from the metadata of the topics, so a new topic appears without editing a diagram.
"""
import html
import math

import atlas

W, H = 940, 330


def lemniscate(t, a=330):
    """A point of the figure eight at angle t, in svg coordinates (centre of the drawing is W/2, H/2)."""
    d = 1 + math.sin(t) ** 2
    return W / 2 + a * math.cos(t) / d, H / 2 - a * 0.95 * math.sin(t) * math.cos(t) / d


def loop_svg(stages):
    """The infinity loop: the first half of the stages on the left lobe, the rest on the right, each linking to its card."""
    n, half = len(stages), len(stages) // 2
    pts = [lemniscate(2 * math.pi * i / 240 + math.pi / 2) for i in range(241)]
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    nodes = []
    for i, s in enumerate(stages):
        lobe, k = divmod(i, half)
        t = math.pi / 2 + math.pi * lobe + (k + 0.5) * math.pi / half  # left lobe first, then the right one
        x, y = lemniscate(t)
        nodes.append('<a href="#stage-{id}"><g class="n"><circle cx="{x:.1f}" cy="{y:.1f}" r="27"/><text class="c" x="{x:.1f}" y="{cy:.1f}">{num}</text>'
                     '<text x="{x:.1f}" y="{ty:.1f}">{label}</text></g></a>'.format(
                         id=html.escape(s["id"]), x=x, y=y, cy=y - 5, ty=y + 11, num=i + 1, label=html.escape(s["label"])))
    labels = ('<text class="lobe" x="{l}" y="{y}">Dev</text><text class="lobe" x="{r}" y="{y}">Ops</text>').format(l=W * 0.25, r=W * 0.75, y=H / 2 + 4)
    return ('<svg class="loop" viewBox="0 0 {w} {h}" role="img" aria-label="The DevOps loop: {names}, then back to {first}">'
            '<title>The DevOps loop</title><path class="path" d="{p}"/><path class="flow" d="{p}"/>{labels}{nodes}</svg>').format(
        w=W, h=H, p=path, labels=labels, nodes="".join(nodes), first=html.escape(stages[0]["label"]),
        names=", ".join(html.escape(s["label"]) for s in stages))


def devops_loop(reg):
    stages = reg["stages"]
    topics = atlas.published()
    fam = {f["id"]: f["label"] for f in reg["families"]}
    cards = []
    for s in stages:
        mine = [t for t in topics if s["id"] in t.get("stages", [])]
        items = "".join(
            '<li><a href="../{id}/index.html"><b>{label}</b><span>{fam}</span></a></li>'.format(
                id=t["id"], label=html.escape(t["label"]), fam=html.escape(fam.get(t["family"], "")))
            for t in mine) or '<li class="none">No topic yet</li>'
        cards.append('<section class="stage" id="stage-{id}"><h3>{label}</h3><p>{about}</p><ul>{items}</ul></section>'.format(
            id=html.escape(s["id"]), label=html.escape(s["label"]), about=html.escape(s["about"]), items=items))
    unplaced = [t for t in topics if not t.get("stages")]
    rest = ('<h2>Not on the loop</h2><p class="unplaced">{}</p>'.format("".join(
        '<a href="../{id}/index.html">{label}</a>'.format(id=t["id"], label=html.escape(t["label"])) for t in unplaced)) if unplaced else "")
    return ('<h1>DevOps loop</h1><p class="sub">The eight stages, and where each topic fits. A topic can belong to several stages.</p>'
            '{svg}<h2>Stages</h2><div class="stages">{cards}</div>{rest}'
            '<p class="note">Which stages a topic belongs to is a judgement recorded in the topic\'s spec, not something a source states. '
            'This page is generated from <code>topics.json</code>; see <code>docs/views.md</code>.</p>').format(
        svg=loop_svg(stages), cards="".join(cards), rest=rest)


VIEWS = {"devops-loop": devops_loop}


def main():
    reg = atlas.load()
    template = (atlas.SITE / "shared" / "view.html").read_text(encoding="utf-8")
    for v in reg.get("views", []):
        body = VIEWS[v["id"]](reg)
        page = (atlas.themed(template).replace("__TITLE__", html.escape(v["label"])).replace("__NAME__", html.escape(reg["name"]))
                .replace("<!--__CONTENT__-->", body).replace(atlas.BANNER_MARK, atlas.banner(v["id"], "../"))
                .replace(atlas.CSS_MARK, atlas.CSS).replace(atlas.FOOTER_MARK, atlas.FOOTER))
        out = atlas.DIST / v["id"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(page, encoding="utf-8")
        print(f"built dist/{v['id']}/index.html")


if __name__ == "__main__":
    main()
