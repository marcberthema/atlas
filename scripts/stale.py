"""List what needs review and write a prompt for an AI agent to do the review.

  stale.py [--all] [--only ID ...] [--limit N]

Default scope: services whose Learn pages changed or failed, and Terraform resources that disappeared.
--all also includes services never reviewed (everything is "unreviewed" until the first pass).
Writes review/PROMPT.md (git-ignored). No network access and no AI: it only reads data/.
"""
import argparse
import difflib
import sys
from datetime import date

import check_updates as cu
import model

OUT = model.ROOT / "review"
DIFF_LINES = 120

PROMPT = """# Review task: Azure Services Map ({today})

You are reviewing entries in this repo against their current Microsoft Learn pages. Read `CLAUDE.md` and
`docs/data-model.md` first and follow them. {count} service(s) need review, listed below with their current
entry ("Entry") and what changed on the page ("Now").

## How to work

1. Make sure the working tree is clean, then create the branch `{branch}` from `main`.
2. Go through the services below **one at a time, in order**. For each one:
   1. Read **Entry** and **Now**. If the diff is cut off or missing, read the snapshot files named there. You may
      also open the live Learn URL.
   2. Tell the user in a few lines what is still right, what is outdated or wrong, and what is new.
   3. Propose the exact edits. **Ask the user** (use AskUserQuestion when available) before changing anything you
      are not sure of, and always for: renames, retirements and dates, an edge whose type is debatable, whether
      Terraform support is `full`, `partial` (and the gaps), and anything that needs context only they have.
      Offer "skip this service" as a choice. Never guess: write "unconfirmed" in the note if it can't be verified.
   4. Apply the approved edits to `data/services.json`:
      - Verified content goes in `fetched` (`purpose`, `facts`). If the same key currently sits in `manual` only
        because it was imported (`review.note` says so), move it: delete the `manual` key and write `fetched`.
        Keep a `manual` value only when the user says it is a deliberate override.
      - Terraform judgement goes in `manual.terraform`: `status` (`full` or `partial`), `gaps` (`what`,
        `alternative` such as the azapi ARM type), `note`. Fix `tracking.terraform` if a resource was renamed
        or removed.
      - Edges: update `note`, `type`, add or remove edges. Set `origin` to `learn` and `status` to `verified` only
        for edges you checked against the page.
      - Set `review` to `{{"status": "verified", "note": "Verified against Learn on {today}."}}` only when the
        whole entry was checked; otherwise keep `unconfirmed` and say what is unchecked.
      - Do not edit `freshness`, `fetched.terraform` or anything in `data/snapshots/` by hand.
   5. Run `make ack SERVICE=<id>` (records the page as reviewed), then `make build` (must pass validation).
   6. Commit that service alone: `Review <service name>: <what changed>`.
3. Keep going until every service is done or skipped. Run `make validate` and `make build` one last time.
4. Show the user the summary (per service: changed, skipped, open questions). **Ask for confirmation**, then
   `git push -u origin {branch}` and open a pull request to `main` with `gh pr create --base main`. The PR body
   lists each service with its decisions and anything left unconfirmed. If there is no `origin` remote, stop after
   the commits and say so.

Rules that always apply: Microsoft Learn is the source of truth; no employer or client details; keep text short and
plain; "service" means a type and "resource" means an instance; edge `A requires B` reads left to right.

## Services to review

{overview}
{sections}"""


def reasons(svc, resolved, include_unreviewed):
    out = []
    status = svc["freshness"]["status"]
    if status in ("stale", "error"):
        out.append("docs " + ("changed since last review" if status == "stale" else "could not be fetched"))
    if status == "unreviewed" and include_unreviewed:
        out.append("never reviewed")
    missing = [r["type"] for r in resolved["terraform"]["resources"] if r["exists"] is False]
    if missing:
        out.append("Terraform resource(s) not found: " + ", ".join(missing))
    return out


def read(path):
    return path.read_text(encoding="utf-8") if path.exists() else None


def source_block(svc, url, src):
    rel = lambda p: p.relative_to(model.ROOT)
    latest_p, reviewed_p = cu.snapshot_path(svc["id"], url, "latest"), cu.snapshot_path(svc["id"], url, "reviewed")
    head = f"- {url}\n  - status: {cu.source_status(src)}, HTTP {src.get('http_status')}, ms.date {src.get('ms_date')}, " \
           f"updated {src.get('updated_at')}\n  - now: `{rel(latest_p)}`"
    latest, reviewed = read(latest_p), read(reviewed_p)
    if cu.source_status(src) == "error":
        return head + "\n  - the page could not be fetched: check whether it moved or was retired"
    if reviewed is None:
        return head + "\n  - no reviewed baseline: verify the entry against the whole current page"
    lines = list(difflib.unified_diff(reviewed.splitlines(), latest.splitlines(), "reviewed", "now", n=2, lineterm=""))
    if not lines:
        return head + "\n  - text unchanged since review"
    shown = "\n".join(lines[:DIFF_LINES])
    cut = f"\n... {len(lines) - DIFF_LINES} more diff lines; compare `{rel(reviewed_p)}` with `{rel(latest_p)}`" \
        if len(lines) > DIFF_LINES else ""
    return head + f"\n  - before: `{rel(reviewed_p)}`\n\n```diff\n{shown}{cut}\n```"


def entry_block(svc, resolved, names, edges):
    r = resolved
    t = r["terraform"]
    lines = [f"**Entry** (review status: {svc['review']['status']}; {svc['review']['note']})", "",
             f"- purpose: {r['purpose']}"]
    lines += [f"- fact: {f}" for f in r["facts"]]
    where = [k for k in ("purpose", "facts") if k in svc["manual"]]
    lines.append(f"- layers: `manual` holds {', '.join(where) or 'nothing'}; `fetched` holds "
                 f"{', '.join(k for k in svc['fetched'] if k != 'terraform') or 'nothing'}")
    lines.append(f"- terraform: {t['status']}; first supported {t['first_supported']}; "
                 f"resources: {', '.join(x['type'] + ('' if x['exists'] is not False else ' (NOT FOUND)') for x in t['resources']) or 'none'}")
    if t["gaps"]:
        lines.append("- terraform gaps: " + "; ".join(f"{g['what']} -> {g.get('alternative', '')}" for g in t["gaps"]))
    if t["note"]:
        lines.append(f"- terraform note: {t['note']}")
    if t["fallback"]:
        lines.append("- azapi ARM types: " + ", ".join(a["type"] for a in t["fallback"]["arm_types"]))
    mine = [e for e in edges if svc["id"] in (e["from"], e["to"])]
    lines.append(f"- relationships ({len(mine)}):")
    lines += [f"  - {names[e['from']]} {e['type']} {names[e['to']]}" + (f" ({e['note']})" if e["note"] else "") +
              f" [{e['status']}]" for e in mine]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="include services that were never reviewed")
    ap.add_argument("--only", nargs="+", metavar="ID")
    ap.add_argument("--limit", type=int, help="at most N services in the prompt")
    args = ap.parse_args()

    data = model.load()
    resolved = {r["id"]: r for r in model.resolve(data)["services"]}
    names = {s["id"]: s["name"] for s in data["services"] + data["stubs"]}
    if args.only:
        unknown = set(args.only) - set(resolved)
        if unknown:
            sys.exit("no such service: " + ", ".join(sorted(unknown)))

    todo = []
    for svc in data["services"]:
        if args.only and svc["id"] not in args.only:
            continue
        why = reasons(svc, resolved[svc["id"]], args.all or bool(args.only))
        if why:
            todo.append((svc, why))

    print(f"{len(todo)} service(s) need review" + ("" if args.all or args.only else " (add --all to include never-reviewed)"))
    for svc, why in todo:
        print(f"  {svc['id']:42} {'; '.join(why)}")
    if not todo:
        return 0
    shown = todo[:args.limit] if args.limit else todo
    if len(shown) < len(todo):
        print(f"prompt covers the first {len(shown)}")

    sections = []
    for svc, why in shown:
        urls = svc["freshness"]["sources"]
        body = [f"### {svc['name']} (`{svc['id']}`, {resolved[svc['id']]['tier_label'].lower()}, {svc['category']})", "",
                "**Why:** " + "; ".join(why), "", entry_block(svc, resolved[svc["id"]], names, data["edges"]), "",
                "**Now** (Microsoft Learn):"]
        body += [source_block(svc, u, urls.get(u, {})) for u in svc["tracking"]["learn_urls"]]
        sections.append("\n".join(body))

    overview = "\n".join(f"{i}. `{s['id']}`: {'; '.join(w)}" for i, (s, w) in enumerate(shown, 1)) + "\n"
    today = date.today().isoformat()
    OUT.mkdir(exist_ok=True)
    (OUT / "PROMPT.md").write_text(PROMPT.format(today=today, branch=f"review/{today}", count=len(shown),
                                                 overview=overview, sections="\n\n".join(sections) + "\n"),
                                   encoding="utf-8")
    print(f"wrote review/PROMPT.md ({len(shown)} service(s)). Run it with: claude \"$(cat review/PROMPT.md)\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
