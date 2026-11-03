"""Check that every topic has a spec (docs/spec.md) and that its coverage table agrees with the data.

  spec.py            check every published topic, and workstation/ and vscode/
  spec.py <dir>...   check these topic folders only

The format is in docs/topic-spec.md. Errors: the spec is missing, a section is missing, a coverage row has an unknown status, a row marked
done or partial names an entry that does not exist, or a tab's main entry is not in the table. Warnings: a row marked planned or dropped
names an entry that now exists (update the status).
"""
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SECTIONS = ["Purpose and audience", "Scope", "Layout", "Sources", "Coverage", "Known gaps", "Decisions", "Updating"]
STATUS = {"done", "partial", "planned", "dropped"}
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([a-z]+)\s*\|")


def entry_ids(folder):
    """Ids of the entries (or Azure services) the topic's data holds, or None when the data has neither."""
    files = [f for f in sorted((folder / "data").glob("*.json")) if f.name != "examples.json"]
    if not files:
        return None
    data = json.loads(files[0].read_text(encoding="utf-8"))
    if "entries" in data:
        return {e["id"] for e in data["entries"]}
    if "services" in data:
        return {s["id"] for s in data["services"]} | {s["id"] for s in data.get("stubs", [])}
    return None


def tab_entries(folder, ids):
    """Tabs that open one entry in full: the main entries a spec must list."""
    view = folder / "templates" / "view.json"
    if not view.exists() or ids is None:
        return set()
    return {t["id"] for t in json.loads(view.read_text(encoding="utf-8"))["tabs"] if t["id"] in ids and not t.get("group")}


def check(folder):
    """(errors, warnings) for one topic folder."""
    bad, warn = [], []
    spec = folder / "docs" / "spec.md"
    if not spec.exists():
        return [f"{folder.name}: docs/spec.md is missing (format: docs/topic-spec.md)"], warn
    text = spec.read_text(encoding="utf-8")
    heads = re.findall(r"^## (.+?)\s*$", text, re.M)
    for s in SECTIONS:
        if s not in heads:
            bad.append(f"{folder.name}: spec has no '## {s}' section")
    ids = entry_ids(folder)
    listed = set()
    for line in text.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        eid, status = m[1], m[2]
        if status not in STATUS:
            bad.append(f"{folder.name}: coverage row `{eid}` has status '{status}' (use {sorted(STATUS)})")
            continue
        listed.add(eid)
        if ids is None or ":" in eid:  # `kind:name` is an item that is not an entry (a tier, a comparison): only its status is checked
            continue
        if status in ("done", "partial") and eid not in ids:
            bad.append(f"{folder.name}: coverage row `{eid}` is {status} but no such entry exists")
        if status in ("planned", "dropped") and eid in ids:
            warn.append(f"{folder.name}: coverage row `{eid}` is {status} but the entry exists: update the status")
    for eid in sorted(tab_entries(folder, ids) - listed):
        bad.append(f"{folder.name}: tab entry `{eid}` is not in the coverage table")
    return bad, warn


def folders():
    topics = json.loads((SITE / "topics.json").read_text(encoding="utf-8"))["topics"]
    out = [SITE / "topics" / t["id"] for t in topics if not t.get("draft")]
    return out + [SITE / "workstation", SITE / "vscode"]


def main(args):
    bad, warn = [], []
    targets = [Path(a).resolve() for a in args] if args else folders()
    for f in targets:
        b, w = check(f)
        bad += b
        warn += w
    for line in bad:
        print("bad:", line)
    for line in warn:
        print("warn:", line)
    print(f"specs {len(targets)} warn {len(warn)} bad {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
