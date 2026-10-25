"""Check data/services.json is internally consistent. Usage: python3 scripts/validate.py [path]"""
import sys
from collections import Counter

import model

FRESHNESS = {"unreviewed", "current", "stale", "error"}
REVIEW = {"unconfirmed", "verified"}
EDGE_STATUS = {"unconfirmed", "verified"}
TF_KINDS = set(model.TF_KINDS)
MANUAL_KEYS = {"purpose", "facts", "cloud_native", "terraform"}


def main():
    data = model.load(*sys.argv[1:2])
    bad, warn = [], []
    cats = set(data["categories"])
    tiers = {t["tier"] for t in data["tiers"]}
    types = {t["type"] for t in data["edge_types"]}
    providers = data["terraform_providers"]
    if "azapi" not in providers:
        bad.append("terraform_providers: azapi is required (fallback)")

    ids = [s["id"] for s in data["services"]] + [s["id"] for s in data["stubs"]]
    bad += [f"duplicate id: {i}" for i, n in Counter(ids).items() if n > 1]
    known = set(ids)
    scope = set(data["scope"]["tiers"])

    for s in data["services"]:
        i = s["id"]
        if s["category"] not in cats:
            bad.append(f"category: {i}")
        if s["tier"] not in scope:
            bad.append(f"tier outside scope: {i}")
        if s["review"]["status"] not in REVIEW:
            bad.append(f"review status: {i}")
        if s["freshness"]["status"] not in FRESHNESS:
            bad.append(f"freshness status: {i}")
        for k in s["manual"]:
            if k not in MANUAL_KEYS:
                bad.append(f"unknown manual key {k}: {i}")
        if not model.deep_merge(s["fetched"], s["manual"]).get("purpose"):
            bad.append(f"no purpose: {i}")
        for t in s["tracking"]["terraform"]:
            if t["provider"] not in providers or t["kind"] not in TF_KINDS or not t["type"].startswith(t["provider"] + "_"):
                bad.append(f"terraform entry {t['type']}: {i}")
        for r in s["fetched"].get("terraform", {}).get("resources", []):
            if r["exists"] is False:
                warn.append(f"terraform resource not found: {r['type']} ({i})")
    for s in data["services"]:
        extra = set(s["manual"].get("terraform", {})) - {"status", "gaps", "content", "compared", "note"}
        if extra:
            bad.append(f"unknown manual.terraform key {sorted(extra)}: {s['id']}")
    levels = {c["level"] for c in data["cloud_native_scale"]}
    for s in data["services"]:
        cn = model.deep_merge(s["fetched"], s["manual"]).get("cloud_native")
        if cn and (cn.get("level") not in levels or not cn.get("note")):
            bad.append(f"cloud_native needs a level from the scale and a note: {s['id']}")
    service_ids = {s["id"] for s in data["services"]}
    for c in data["comparisons"]:
        for m in c["members"]:
            bad += [f"comparison {c['id']}: unknown service {i}" for i in m["services"] if i not in service_ids]
            if not m.get("audience") or not m.get("choose_when"):
                bad.append(f"comparison {c['id']}: member needs audience and choose_when")
    for s in data["stubs"]:
        if s["tier"] in scope or s["category"] not in cats:
            bad.append(f"stub: {s['id']}")

    seen = set()
    for e in data["edges"]:
        key = (e["from"], e["type"], e["to"])
        if key in seen:
            bad.append(f"duplicate edge: {key}")
        seen.add(key)
        for end in ("from", "to"):
            if e[end] not in known:
                bad.append(f"edge {end}: {e[end]}")
        if e["type"] not in types:
            bad.append(f"edge type: {e['type']}")
        if e["status"] not in EDGE_STATUS:
            bad.append(f"edge status: {key}")
    for g in data["edge_group_order"]:
        if g["type"] not in types or g["direction"] not in ("in", "out"):
            bad.append(f"edge_group_order: {g}")

    by_tier = Counter(s["tier"] for s in data["services"])
    print(f"services {len(data['services'])} tiers {dict(sorted(by_tier.items()))} "
          f"stubs {len(data['stubs'])} edges {len(data['edges'])} bad {len(bad)} warnings {len(warn)}")
    for b in bad:
        print("  BAD", b)
    for w in warn:
        print("  warn", w)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
