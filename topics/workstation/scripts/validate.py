"""Check data/workstation.json is internally consistent. Usage: python3 scripts/validate.py [path]"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "shared"))
import learning  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")  # an RFC is dated by month, a book by year
LEVELS = {"deep", "overview", "ref"}
STATUS = {"active", "inactive", "archived"}
CNCF = {"graduated", "incubating", "sandbox", "none"}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "workstation.json"
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
        if s.get("confirmed") and not MONTH.match(s.get("date", "")):
            bad.append(f"started is confirmed but not a date, a month or a year: {i}")
        t = e.get("track")
        if not t:
            if e.get("license") != "n/a":  # a concept has no release to check
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
        bad += learning.section_problems(e)
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
    print(f"workstation entries {len(data['entries'])} comparisons {len(data.get('comparisons', []))} warn {len(warn)} bad {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
