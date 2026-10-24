"""Daily freshness check. No AI: it fetches public pages and records facts in data/services.json.

  check_updates.py check [--only ID] [--skip-learn] [--skip-terraform] [--strict]
  check_updates.py ack ID|all      mark the current Learn page contents as reviewed

Learn pages: store a hash of the main content plus ms.date. A service is "stale" when the latest hash
differs from the hash a human last reviewed. Terraform: which tracked resources exist in the latest
provider docs, and the first provider version that added each (from the provider changelogs).
"""
import argparse
import hashlib
import html
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import model

UA = {"User-Agent": "azure-services-map-check (https://github.com)"}
RAW = "https://raw.githubusercontent.com/{}/main/{}"
CHANGELOGS = {
    "azurerm": [RAW.format("hashicorp/terraform-provider-azurerm", f) for f in
                ("CHANGELOG.md", "CHANGELOG-v4.md", "CHANGELOG-v3.md", "CHANGELOG-v2.md", "CHANGELOG-v1.md")],
    "azuread": [RAW.format("hashicorp/terraform-provider-azuread", "CHANGELOG.md")],
    "azuredevops": [RAW.format("microsoft/terraform-provider-azuredevops", "CHANGELOG.md")],
    "azapi": [RAW.format("Azure/terraform-provider-azapi", "CHANGELOG.md")],
}
STATUS_ORDER = ["error", "stale", "unreviewed", "current"]  # worst first


def today():
    return datetime.now(timezone.utc).date().isoformat()


def fetch(url, tries=3):
    last = None
    for n in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return e.code, ""
            last = e.code
        except (urllib.error.URLError, TimeoutError) as e:
            last = str(e)
        time.sleep(2 * (n + 1))
    return last, ""


# ---- Microsoft Learn ------------------------------------------------------------------------

def meta(page, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % re.escape(name), page)
    return html.unescape(m.group(1)) if m else None


def content_hash(page):
    m = re.search(r"<main\b.*?</main>", page, re.S)
    text = m.group(0) if m else page
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return "sha256:" + hashlib.sha256(re.sub(r"\s+", " ", text).strip().encode()).hexdigest()


def check_source(url, prev):
    code, page = fetch(url)
    src = dict(prev)
    src["checked_at"] = today()
    src["http_status"] = code
    if code == 200:
        src["ms_date"] = meta(page, "ms.date")
        src["updated_at"] = meta(page, "updated_at")
        src["latest_hash"] = content_hash(page)
    return src


def source_status(src):
    if src.get("http_status") != 200:
        return "error"
    if not src.get("reviewed_hash"):
        return "unreviewed"
    return "current" if src["reviewed_hash"] == src["latest_hash"] else "stale"


def service_status(sources):
    states = {source_status(s) for s in sources.values()} or {"unreviewed"}
    return next(s for s in STATUS_ORDER if s in states)


def check_learn(services):
    jobs = [(svc, u) for svc in services for u in svc["tracking"]["learn_urls"]]
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(lambda j: check_source(j[1], j[0]["freshness"]["sources"].get(j[1], {})), jobs))
    for (svc, u), src in zip(jobs, results):
        svc["freshness"]["sources"][u] = src
    for svc in services:
        fr = svc["freshness"]
        fr["sources"] = {u: fr["sources"][u] for u in svc["tracking"]["learn_urls"]}
        fr["status"] = service_status(fr["sources"])
        fr["checked_at"] = today()


def ack(data, which):
    hit = 0
    for svc in data["services"]:
        if which not in ("all", svc["id"]):
            continue
        hit += 1
        for src in svc["freshness"]["sources"].values():
            if src.get("latest_hash"):
                src["reviewed_hash"] = src["latest_hash"]
        svc["freshness"]["status"] = service_status(svc["freshness"]["sources"])
    return hit


# ---- Terraform ------------------------------------------------------------------------------

def get_json(url):
    code, body = fetch(url)
    if code != 200:
        raise RuntimeError(f"{url}: {code}")
    import json
    return json.loads(body)


def registry_docs(ns, name):
    """Return (latest_version, {'resources': set, 'data_source': set}) from the Terraform Registry."""
    base = "https://registry.terraform.io"
    latest = get_json(f"{base}/v1/providers/{ns}/{name}")["version"]
    versions = get_json(f"{base}/v2/providers/{ns}/{name}?include=provider-versions")["included"]
    vid = next(v["id"] for v in versions if v["attributes"]["version"] == latest)
    found = {"resource": set(), "data_source": set()}
    for category, kind in (("resources", "resource"), ("data-sources", "data_source")):
        page = 1
        while True:
            q = urllib.parse.urlencode({"filter[provider-version]": vid, "filter[category]": category,
                                        "page[size]": 100, "page[number]": page})
            rows = get_json(f"{base}/v2/provider-docs?{q}")["data"]
            found[kind] |= {f"{name}_{r['attributes']['slug']}" for r in rows}
            if len(rows) < 100:
                break
            page += 1
    return latest, found


def changelog_since(provider):
    """Map (kind, type) -> earliest provider version whose changelog lists it as new."""
    since = {}
    for url in CHANGELOGS.get(provider, []):
        code, text = fetch(url)
        if code != 200:
            continue
        version = None
        for line in text.splitlines():
            h = re.match(r"##\s+v?(\d+\.\d+\.\d+)", line)
            if h:
                version = h.group(1)
                continue
            m = re.search(r"New (Data Source|Resource)\W", line)
            n = re.search(r"`(\w+)`", line)
            if version and m and n:
                key = ("data_source" if m.group(1) == "Data Source" else "resource", n.group(1))
                if key not in since or model.version_key(version) < model.version_key(since[key]):
                    since[key] = version
    return since


def check_terraform(data, services):
    used = sorted({t["provider"] for s in services for t in s["tracking"]["terraform"]} | {"azapi"})
    docs, since, errors = {}, {}, []
    for p in used:
        meta_p = data["terraform_providers"][p]
        try:
            latest, docs[p] = registry_docs(meta_p["namespace"], meta_p["name"])
            since[p] = changelog_since(p)
            meta_p["latest_version"], meta_p["checked_at"] = latest, today()
        except Exception as e:  # keep earlier results for this provider
            errors.append(f"{p}: {e}")
    for svc in services:
        prev = {r["type"]: r for r in svc["fetched"].get("terraform", {}).get("resources", [])}
        out = []
        for t in svc["tracking"]["terraform"]:
            if t["provider"] in docs:
                out.append({"type": t["type"], "exists": t["type"] in docs[t["provider"]][t["kind"]],
                            "since": since[t["provider"]].get((t["kind"], t["type"]))})
            elif t["type"] in prev:
                out.append(prev[t["type"]])
        entry = {"resources": out, "checked_at": today()}
        if svc["tracking"]["arm_types"]:
            # azapi has a typed page per ARM type; types without one still work through azapi_resource
            typed = docs.get("azapi", {}).get("resource")
            entry["arm_types"] = [{"type": a, "documented": "azapi_" + a.replace("/", "_") in typed}
                                  for a in svc["tracking"]["arm_types"]] if typed is not None else \
                svc["fetched"].get("terraform", {}).get("arm_types", [])
        svc["fetched"]["terraform"] = entry
    return errors


# ---- CLI ------------------------------------------------------------------------------------

def report(data, services, errors):
    counts = {}
    for s in services:
        counts[s["freshness"]["status"]] = counts.get(s["freshness"]["status"], 0) + 1
    print("learn freshness:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for s in services:
        if s["freshness"]["status"] in ("stale", "error"):
            print(f"  {s['freshness']['status']:5} {s['id']}")
    tf = {}
    for r in model.resolve(data)["services"]:
        if r["id"] in {s["id"] for s in services}:
            tf.setdefault(r["terraform"]["status"], []).append(r["id"])
    print("terraform status:", ", ".join(f"{k} {len(v)}" for k, v in sorted(tf.items())))
    for e in errors:
        print("  terraform check failed for", e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--only")
    c.add_argument("--skip-learn", action="store_true")
    c.add_argument("--skip-terraform", action="store_true")
    c.add_argument("--strict", action="store_true", help="exit 1 if any service is stale or errored")
    a = sub.add_parser("ack")
    a.add_argument("which")
    args = ap.parse_args()

    data = model.load()
    if args.cmd == "ack":
        n = ack(data, args.which)
        if not n:
            sys.exit(f"no such service: {args.which}")
        model.save(data)
        print("acknowledged", n, "service(s)")
        return 0

    services = [s for s in data["services"] if args.only in (None, s["id"])]
    if not services:
        sys.exit(f"no such service: {args.only}")
    errors = []
    if not args.skip_learn:
        check_learn(services)
    if not args.skip_terraform:
        errors = check_terraform(data, services)
    model.save(data)
    report(data, services, errors)
    bad = any(s["freshness"]["status"] in ("stale", "error") for s in services)
    return 1 if args.strict and (bad or errors) else 0


if __name__ == "__main__":
    sys.exit(main())
