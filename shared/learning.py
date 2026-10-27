"""Checks for the learning layout (parts, items, diagrams) shared by the topics that use shared/topic.html."""

PARTS = ("overview", "use", "run", "reference")
CALLOUTS = {"gotcha", "default", "prod", "tip"}


def item_problems(it):
    """A section item is a string (a bullet) or an object with a type. Returns what is wrong with it."""
    if isinstance(it, str):
        return [] if it.strip() else ["empty item"]
    t = it.get("type")
    if t is None:
        return [] if it.get("text") else ["an object item needs a type or a text"]
    if t == "code":
        # Atlas points to the docs: an example is fetched by `match` (scripts/examples.py). Text written here needs a note saying why.
        m = it.get("match")
        ok_match = isinstance(m, str) and m or isinstance(m, list) and m and all(isinstance(x, str) and x for x in m)
        if ok_match and it.get("body"):
            out = ["code has both a match and a body: drop the body, it is fetched"]
        elif not ok_match and not (it.get("body") and it.get("note")):
            out = ["code needs a match (fetched from the source page), or a body with a note saying why it is not fetched"]
        else:
            out = []
        if it.get("lang") not in ("yaml", "shell", "text"):
            out.append("code needs lang yaml, shell or text")
        src = it.get("source") or {}
        if not src.get("label") or not src.get("url", "").startswith("https://"):
            out.append("code needs a source with a label and an https url")
        return out
    if t == "table":
        cols = it.get("columns") or []
        return [] if cols and it.get("rows") and all(len(r) == len(cols) for r in it["rows"]) else ["table rows must match its columns"]
    if t == "callout":
        return [] if it.get("kind") in CALLOUTS and it.get("text") else [f"callout needs a kind ({', '.join(sorted(CALLOUTS))}) and a text"]
    if t == "cards":
        return [] if it.get("cards") and all(c.get("title") and c.get("text") for c in it["cards"]) else ["cards need a title and a text each"]
    if t == "checklist":
        return [] if it.get("items") else ["checklist needs items"]
    if t == "diagram":
        ids = [n.get("id") for n in it.get("nodes", [])]
        out = [] if it.get("alt") and it.get("w") and it.get("h") and len(ids) == len(set(ids)) else ["diagram needs alt, w, h and unique node ids"]
        for n in it.get("nodes", []):
            if not all(isinstance(n.get(k), (int, float)) for k in ("x", "y", "w", "h")) or not n.get("label"):
                out.append("diagram node needs x, y, w, h and a label")
            elif n["x"] - n["w"] / 2 < 0 or n["y"] - n["h"] / 2 < 0 or n["x"] + n["w"] / 2 > it["w"] or n["y"] + n["h"] / 2 > it["h"]:
                out.append(f"diagram node {n['id']} is outside the canvas")
        out += ["diagram link names an unknown node" for l in it.get("links", []) if l.get("from") not in ids or l.get("to") not in ids]
        return out
    return [f"unknown item type {t}"]


def section_problems(e):
    """What is wrong with an entry's sections: parts, items, and that parts are all or nothing."""
    i, out = e["id"], []
    for sec in e.get("sections", []):
        if not sec.get("title") or not sec.get("items"):
            out.append(f"section needs a title and items: {i}")
        if sec.get("part") not in (None, *PARTS):
            out.append(f"section part must be one of {', '.join(PARTS)}: {i}")
        out += [f"{m}: {i} / {sec.get('title')}" for it in sec.get("items", []) for m in item_problems(it)]
    if any(s.get("part") for s in e.get("sections", [])) and not all(s.get("part") for s in e.get("sections", [])):
        out.append(f"either every section has a part or none does: {i}")
    return out
