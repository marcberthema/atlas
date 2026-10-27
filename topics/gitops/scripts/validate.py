"""Check data/gitops.json is internally consistent. Usage: python3 scripts/validate.py [path]"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LEVELS = {"deep", "overview", "ref"}
STATUS = {"active", "inactive", "archived"}
CNCF = {"graduated", "incubating", "sandbox", "none"}


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


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "gitops.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    bad, warn = [], []
    if not DATE.match(data.get("checked", "")):
        bad.append("checked: a YYYY-MM-DD date is required")
    groups = {g["id"] for g in data["groups"]}
    ids = [e["id"] for e in data["entries"]]
    bad += [f"duplicate id: {i}" for i, n in Counter(ids).items() if n > 1]
    known = set(ids)

    for e in data["entries"]:
        i = e["id"]
        for k in ("name", "summary", "license", "version", "started", "cncf", "sources", "sections"):
            if not e.get(k):
                bad.append(f"{k} missing: {i}")
        if e.get("group") not in groups:
            bad.append(f"group: {i}")
        if e.get("level") not in LEVELS:
            bad.append(f"level: {i}")
        if e.get("status") not in STATUS:
            bad.append(f"status: {i}")
        if e.get("cncf", {}).get("level") not in CNCF:
            bad.append(f"cncf level: {i}")
        # the version analysed must be visible: the root CLAUDE.md requires it of every entry
        v = e.get("version", {})
        for k in ("name", "analysed", "released", "checked"):
            if not v.get(k):
                bad.append(f"version.{k} missing: {i}")
        for k in ("released", "checked"):
            if v.get(k) and not DATE.match(v[k]):
                bad.append(f"version.{k} is not a date: {i}")
        if v.get("checked", "") > data.get("checked", ""):
            bad.append(f"version.checked is after the topic's checked date: {i}")
        s = e.get("started", {})
        if not s.get("date") or not s.get("basis") or not isinstance(s.get("confirmed"), bool):
            bad.append(f"started needs date, basis and confirmed: {i}")
        if s.get("confirmed") and not DATE.match(s.get("date", "")):
            bad.append(f"started is confirmed but not a full date: {i}")
        t = e.get("track")
        if not t:
            warn.append(f"no track (the update check skips it): {i}")
        elif not re.match(r"^[\w.-]+/[\w.-]+$", t.get("github", "")):
            bad.append(f"track.github needs owner/repo: {i}")
        for src in e.get("sources", []):
            if not src.get("label") or not src.get("url", "").startswith("https://"):
                bad.append(f"source needs a label and an https url: {i}")
            if src.get("date") and not DATE.match(src["date"]):
                bad.append(f"source date is not a date: {i}")
        if len({s["url"] for s in e.get("sources", [])}) != len(e.get("sources", [])):
            bad.append(f"duplicate source url: {i}")
        links = e.get("links", [])
        if not links:
            bad.append(f"no links (project, docs or repository): {i}")
        for link in links:
            if not link.get("label") or not link.get("url", "").startswith("https://"):
                bad.append(f"link needs a label and an https url: {i}")
        if len({x["url"] for x in links}) != len(links):
            bad.append(f"duplicate link url: {i}")
        for sec in e.get("sections", []):
            if not sec.get("title") or not sec.get("items"):
                bad.append(f"section needs a title and items: {i}")
            if sec.get("part") not in (None, *PARTS):
                bad.append(f"section part must be one of {', '.join(PARTS)}: {i}")
            for it in sec.get("items", []):
                bad += [f"{m}: {i} / {sec.get('title')}" for m in item_problems(it)]
        if any(sec.get("part") for sec in e.get("sections", [])) and not all(sec.get("part") for sec in e.get("sections", [])):
            bad.append(f"either every section has a part or none does: {i}")
        for c in e.get("compare", []):
            if c["with"] not in known:
                bad.append(f"compare points at unknown entry {c['with']}: {i}")
        for r in e.get("related", []):
            if r not in known:
                bad.append(f"related points at unknown entry {r}: {i}")
        if e.get("level") == "deep" and len(e.get("sources", [])) < 2:
            warn.append(f"deep entry with fewer than 2 sources: {i}")

    for c in data.get("comparisons", []):
        n = len(c["columns"])
        for r in c["rows"]:
            if len(r["cells"]) != n:
                bad.append(f"comparison {c['id']}: row {r.get('label') or r.get('entry')} has {len(r['cells'])} cells, expected {n}")
            if bool(r.get("label")) == bool(r.get("entry")):
                bad.append(f"comparison {c['id']}: a row needs exactly one of label and entry")
            if r.get("entry") and r["entry"] not in known:
                bad.append(f"comparison {c['id']}: unknown entry {r['entry']}")

    for line in warn:
        print("warn:", line)
    for line in bad:
        print("bad:", line)
    print(f"gitops entries {len(data['entries'])} comparisons {len(data.get('comparisons', []))} warn {len(warn)} bad {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
