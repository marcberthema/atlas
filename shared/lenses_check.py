"""Check the data of the lenses view (views/lenses/data/lenses.json), and optionally its links.

  lenses_check.py          offline: ids, cells, edges, topics, Azure service ids, sources and statuses
  lenses_check.py links    also fetch every source url once and report the ones that no longer answer (needs the network)

The format is in views/lenses/docs/spec.md. Exit 1 on errors; warnings (a role with no topic, a product with no source) do not fail.
"""
import json
import sys
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = SITE / "views" / "lenses" / "data" / "lenses.json"
KINDS = {"scope", "span", "outside"}
STYLES = {"solid", "dash", "dot"}


def load():
    return json.loads(DATA.read_text(encoding="utf-8"))


def azure_services():
    d = json.loads((SITE / "topics" / "azure" / "data" / "services.json").read_text(encoding="utf-8"))
    return {s["id"] for s in d["services"]} | {s["id"] for s in d.get("stubs", [])}


def topic_ids():
    return {t["id"] for t in json.loads((SITE / "topics.json").read_text(encoding="utf-8"))["topics"] if not t.get("draft")}


def check(d=None):
    """(errors, warnings)."""
    d = d or load()
    bad, warn = [], []
    lens = [x["id"] for x in d["lenses"]]
    stack = [x["id"] for x in d["stacks"]]
    lane = [x["id"] for x in d["lanes"]]
    role = [r["id"] for r in d["roles"]]
    lvl = [x["id"] for x in d["levels"]]
    org = [o["id"] for o in d["org"]]
    for what, items in (("lens", lens), ("stack", stack), ("lane", lane), ("role", role), ("level", lvl), ("organization", org)):
        for i in sorted({x for x in items if items.count(x) > 1}):
            bad.append(f"duplicate {what} id: {i}")
    if len(set(role) | set(lvl) | set(org)) != len(role) + len(lvl) + len(org):
        bad.append("a role, a level and an organization item share an id")
    services, topics = azure_services(), topic_ids()
    cells = {}
    for r in d["roles"]:
        i = r["id"]
        for k in ("name", "full", "what", "where", "why", "checked"):
            if not r.get(k):
                bad.append(f"role {i} has no {k}")
        if not r.get("sources") and i != "users":
            bad.append(f"role {i} has no sources")
        if r.get("status") not in ("verified", "unconfirmed"):
            bad.append(f"role {i} has status {r.get('status')!r}")
        if r.get("status") == "verified" and not r.get("sources"):
            bad.append(f"role {i} is verified without a source")
        if not r["lenses"] or any(x not in lens for x in r["lenses"]):
            bad.append(f"role {i} names an unknown lens or none: {r['lenses']}")
        if r.get("setting"):
            if "at" in r:
                bad.append(f"role {i} is a setting and must have no cell")
        else:
            at = r.get("at")
            if not at or at["lane"] not in lane or not 0 <= at["col"] <= 5:
                bad.append(f"role {i} needs a lane and a column 0-5")
            elif (at["lane"], at["col"]) in cells:
                bad.append(f"role {i} and {cells[(at['lane'], at['col'])]} share a cell")
            else:
                cells[(at["lane"], at["col"])] = i
        for t in r.get("topics", []):
            if t not in topics:
                bad.append(f"role {i} names an unknown topic: {t}")
        if not r.get("topics"):
            warn.append(f"role {i} has no topic yet")
        for s, plist in r["products"].items():
            if s not in stack:
                bad.append(f"role {i} has products for an unknown stack: {s}")
            for p in plist:
                if not p.get("name"):
                    bad.append(f"role {i} has a product with no name")
                if p.get("service") and p["service"] not in services:
                    bad.append(f"role {i}: product {p['name']} names an unknown Azure service: {p['service']}")
                if not p.get("source"):
                    warn.append(f"role {i}: product {p.get('name')} has no source")
    settings = {r["id"] for r in d["roles"] if r.get("setting")}
    nodes = set(role) | {"@frame"}
    for e in d["edges"]:
        tag = f"edge {e['from']} -> {e['to']}"
        if e["from"] not in nodes or e["to"] not in nodes or e["from"] == e["to"]:
            bad.append(f"{tag} joins unknown nodes")
        if e["style"] not in STYLES:
            bad.append(f"{tag} has style {e['style']!r}")
        if not e["lenses"] or any(x not in lens for x in e["lenses"]):
            bad.append(f"{tag} names an unknown lens")
        if e.get("badge") and e["badge"] not in role:
            bad.append(f"{tag} names an unknown badge role")
        if e["from"] in settings or e["to"] in settings:
            bad.append(f"{tag} joins a setting, which has no box")
    for x in d["levels"]:
        if not (x.get("generic") and x.get("azure") and x.get("about") and x.get("source")):
            bad.append(f"level {x['id']} needs generic, azure, about and source")
    for o in d["org"]:
        i = o["id"]
        if o["kind"] not in KINDS:
            bad.append(f"organization item {i} has kind {o['kind']!r}")
        if any(x not in lvl for x in o["levels"]) or (o["kind"] == "scope" and not o["levels"]):
            bad.append(f"organization item {i} has bad levels: {o['levels']}")
        if o["kind"] == "scope" and o.get("place") not in lvl:
            bad.append(f"organization item {i} needs a place that is a level")
        if o.get("service") and o["service"] not in services:
            bad.append(f"organization item {i} names an unknown Azure service: {o['service']}")
        if not (o.get("sources") and o.get("what") and o.get("why") and o.get("checked")):
            bad.append(f"organization item {i} needs what, why, sources and checked")
        if o["status"] not in ("verified", "unconfirmed"):
            bad.append(f"organization item {i} has status {o['status']!r}")
        if o["status"] == "unconfirmed" and not o.get("note"):
            warn.append(f"organization item {i} is unconfirmed but has no note saying what")
    return bad, warn


def urls(d):
    out = {u for r in d["roles"] for u in r.get("sources", [])} | {u for o in d["org"] for u in o.get("sources", [])}
    out |= {x["source"] for x in d["levels"]}
    out |= {p["source"] for r in d["roles"] for plist in r["products"].values() for p in plist if p.get("source")}
    return sorted(out)


def links(d):
    """The source urls that do not answer 200 (redirects are followed), with the reason. A certificate error can come from this machine's trust store, and some sites refuse scripts (403): check by hand before dropping a source."""
    dead = []
    for u in urls(d):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "atlas-lenses-check"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status != 200:
                    dead.append((u, r.status))
        except Exception as e:  # network errors and http errors are both reported
            dead.append((u, getattr(e, "code", None) or str(getattr(e, "reason", e))[:90]))
    return dead


def main(args):
    d = load()
    bad, warn = check(d)
    for line in bad:
        print("bad:", line)
    for line in warn:
        print("warn:", line)
    print(f"roles {len(d['roles'])} edges {len(d['edges'])} organization {len(d['org'])} warn {len(warn)} bad {len(bad)}")
    if "links" in args:
        dead = links(d)
        for u, c in dead:
            print("dead:", c, u)
        print(f"links {len(urls(d))} dead {len(dead)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
