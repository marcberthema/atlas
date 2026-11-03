"""Scaffold a new topic: the folder, the scripts, an empty data file, a spec to fill in, and the registry entries.

  new_topic.py <id> "<Label>" <family> [--stages plan,code] [--description "..."]   create topics/<id>/ and register it as a draft
  new_topic.py --publish <id>                                                       remove "draft": the topic is built, shown and checked

The scripts are copies of the Terraform topic's with the id replaced. The topic stays a draft (never built or shown) until it is published.
Python 3 standard library only. Run from anywhere; it works on the repository this file is in.
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
MODEL = SITE / "topics" / "terraform"  # the topic the scripts are copied from
COPY = ["Makefile", "scripts/build.py", "scripts/check_updates.py", "scripts/validate.py"]

CLAUDE = """# {label} (Atlas topic)

Rules for this topic. The site-wide rules are in the repo root `CLAUDE.md`. Run commands from `topics/{id}/`.

Same shape as the Terraform, GitOps and Certificates topics: `data/{id}.json` is the only place content lives, `scripts/build.py` turns it into
`../../dist/{id}/index.html` with the shared page (`shared/topic.html`) and `templates/view.json`. Python 3 standard library only.

`data/{id}.json` holds `groups`, `entries` and `comparisons`. See `docs/data-model.md`. `scripts/validate.py` (`make validate`) checks it.
Content collected with AI help goes into the JSON with its source URLs. Say "unconfirmed" in `notes` when it can't be verified.

Scope: see `docs/spec.md`, the plan this topic is built from. Read it first and change it in the same commit as the data. Format: `docs/topic-spec.md`.

Every entry must record the version analysed (`version.analysed`, its release date and the check date) and the page shows it.
See the root `CLAUDE.md`. `started` is only `confirmed` when an announcement or release gives the date, not when it is a repository creation date.

Refreshing: `make check` lists what changed (releases, archived repositories, CNCF levels; `LINKS=1` for source links) and writes nothing.
Review each difference, then update `checked`, `version` and the facts that changed together. Add a `track` to every entry that has a GitHub repository.

Code examples are fetched, never pasted: give the source page and a `match` string, run `make examples`, and check the result on the page.
HCL, workflow files and other non-shell code use `lang: text` when the shared page does not know the language (it knows yaml, shell and text).
"""

SPEC = """# {label}: spec

Status: draft (not published). Data checked {today}. Format: `docs/topic-spec.md`. Fill in every section before writing entries, and get it approved.

## Purpose and audience

TODO: who looks things up here, and for what. One paragraph.

## Scope

TODO: what is in, what is out, and the rule that decides. Name the exclusions.

## Layout

TODO: the archetype (see `docs/topic-spec.md`), the tabs and what each holds, the groups, and why.

## Sources

TODO: the primary pages the content is read from, and how to re-check them (`track` fields, `make check`).

## Coverage

| Item | Status | Notes |
|---|---|---|
| `entry-id` | planned | what it covers |

## Known gaps

TODO: unconfirmed claims, single-source entries, anything thin. Nothing is hidden here.

## Decisions

- TODO: choices specific to this topic, each with its reason. A reason that cannot be verified says "reason unconfirmed".
- DevOps loop stages: {stages}. A judgement made for the DevOps loop view (`docs/views.md`), not a statement from a source.

## Updating

TODO: what to re-read when a new release appears, and which commands to run.
"""


def sub(text, id_, label):
    return text.replace("terraform", id_).replace("Terraform", label)


def register(id_, label, family, stages, description):
    """Add the draft entry to topics.json (text edit, so its one-line layout stays) and the pattern rule to the root Makefile."""
    reg = json.loads((SITE / "topics.json").read_text(encoding="utf-8"))
    if family not in [f["id"] for f in reg["families"]]:
        sys.exit(f"unknown family {family!r}: use one of {[f['id'] for f in reg['families']]}")
    path = SITE / "topics.json"
    text = path.read_text(encoding="utf-8")
    if not any(t["id"] == id_ for t in reg["topics"]):
        entry = {"id": id_, "family": family, "label": label, "draft": True}
        if stages:
            entry["stages"] = stages
        entry["description"] = description
        line = "    " + json.dumps(entry, ensure_ascii=False).replace('{"', '{"', 1).replace('", "', '", "') + ",\n"
        text = text.replace('  "topics": [\n', '  "topics": [\n' + line, 1)
        path.write_text(text, encoding="utf-8")
    mk = SITE / "Makefile"
    rule = f"{id_}-%:\n\t$(MAKE) -C topics/{id_} $*\n"
    body = mk.read_text(encoding="utf-8")
    if rule not in body:
        mk.write_text(body.rstrip("\n") + "\n" + rule, encoding="utf-8")


def create(id_, label, family, stages, description):
    if not re.fullmatch(r"[a-z][a-z0-9-]*", id_):
        sys.exit("the id is lowercase letters, digits and hyphens")
    folder = SITE / "topics" / id_
    if folder.exists():
        sys.exit(f"{folder} already exists")
    for rel in COPY:
        dest = folder / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(sub((MODEL / rel).read_text(encoding="utf-8"), id_, label), encoding="utf-8")
    (folder / "templates").mkdir()
    (folder / "templates" / "view.json").write_text(json.dumps({"title": label, "tabs": [{"id": "others", "label": "Ecosystem"}, {"id": "compare", "label": "Compare"}]}, indent=2) + "\n", encoding="utf-8")
    today = datetime.date.today().isoformat()
    (folder / "data").mkdir()
    (folder / "data" / f"{id_}.json").write_text(json.dumps(
        {"title": label, "intro": "", "checked": today, "scope": "", "groups": [], "entries": [], "comparisons": []}, indent=2) + "\n", encoding="utf-8")
    (folder / "docs").mkdir()
    (folder / "docs" / "data-model.md").write_text(
        f"# Data model\n\n`data/{id_}.json` follows the same format as the GitOps topic: see `topics/gitops/docs/data-model.md` for entries,\nthe learning layout, tables, callouts, code examples and diagrams.\n", encoding="utf-8")
    (folder / "docs" / "spec.md").write_text(SPEC.format(label=label, today=today, stages=", ".join(stages) or "none yet"), encoding="utf-8")
    (folder / "CLAUDE.md").write_text(CLAUDE.format(id=id_, label=label), encoding="utf-8")
    register(id_, label, family, stages, description or f"TODO: one line for the landing page.")
    print(f"created topics/{id_}/ and registered it as a draft in topics.json and the Makefile")
    print("next: fill in docs/spec.md and get it approved, then write data/%s.json, set tabs in templates/view.json," % id_)
    print(f"      run `make {id_}-validate`, `make {id_}-examples`, `python3 shared/new_topic.py --publish {id_}`, `make build`")


def publish(id_):
    path = SITE / "topics.json"
    text = path.read_text(encoding="utf-8")
    new, n = re.subn(r'(\{"id": "%s",[^\n]*?) "draft": true,' % re.escape(id_), r"\1", text, count=1)
    if not n:
        sys.exit(f"{id_} is not a draft in topics.json")
    reg = json.loads(new)
    t = next(t for t in reg["topics"] if t["id"] == id_)
    if not t.get("description") or t["description"].startswith("TODO"):
        sys.exit("write a description in topics.json first: it is shown on the landing page")
    path.write_text(new, encoding="utf-8")
    print(f"published {id_}: run `make validate` and `make build`")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("id")
    ap.add_argument("label", nargs="?")
    ap.add_argument("family", nargs="?")
    ap.add_argument("--stages", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    if a.publish:
        return publish(a.id)
    if not a.label or not a.family:
        ap.error("a new topic needs an id, a label and a family")
    create(a.id, a.label, a.family, [s for s in a.stages.split(",") if s], a.description)


if __name__ == "__main__":
    main()
