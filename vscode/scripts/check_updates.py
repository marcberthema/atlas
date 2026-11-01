"""Check data/vscode.json against public sources. No AI, and it never writes the data: it prints what changed.

  check_updates.py [--only ID] [--links] [--strict]

For each entry with a `track`: with `marketplace` (publisher.name), the newest stable (not pre-release) Marketplace version
against version.analysed and its minimum VS Code (engine) against extension.engine; with `github`, the latest GitHub release
against version.analysed and the archived flag against status; with `cncf`, the CNCF maturity level against cncf.level. --links also fetches every source and link url. Set GITHUB_TOKEN to avoid
the unauthenticated GitHub rate limit (60 requests an hour). --strict exits 1 when anything differs.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "vscode.json"
UA = {"User-Agent": "atlas-check (https://github.com)"}
API = "https://api.github.com/repos/{}"
CNCF = "https://www.cncf.io/projects/{}/"
LEVELS = {"sandbox": "sandbox", "incubating": "incubating", "graduated": "graduated"}


def fetch(url, headers=None, tries=3):
    """(status, body). A 4xx is returned at once, 5xx and network errors are retried."""
    last = None
    for n in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **(headers or {})}), timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return e.code, ""
            last = e.code
        except (urllib.error.URLError, TimeoutError) as e:
            last = str(e)
        time.sleep(2 * (n + 1))
    return last, ""


def gh(path):
    token = os.environ.get("GITHUB_TOKEN")
    status, body = fetch(API.format(path), {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {token}"} if token else {})})
    if status == 403:
        sys.exit("GitHub refused the request (rate limit?). Set GITHUB_TOKEN and run again.")
    return status, json.loads(body) if status == 200 else None


def latest_release(repo, pattern):
    """Highest version among the recent releases that are not drafts or prereleases and whose tag matches `pattern`.
    The list is ordered by date, and a patch for an older minor version can be newer than the latest release."""
    status, rels = gh(f"{repo}/releases?per_page=50")
    if rels is None:
        return None, f"releases: HTTP {status}"
    ok = [r for r in rels if not r["draft"] and not r["prerelease"] and re.search(pattern, r["tag_name"])
          and not re.search(r"-(alpha|beta|rc)", r["tag_name"])]  # some projects do not flag these
    if not ok:
        return None, "no matching release"
    return max(ok, key=lambda r: [int(n) for n in re.findall(r"\d+", r["tag_name"])]), None


def cncf_level(slug):
    """The level the project page names last, for example 'moved to the Graduated maturity level'."""
    status, page = fetch(CNCF.format(slug))
    if status != 200:
        return None, f"cncf.io: HTTP {status}"
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))
    m = re.search(r"accepted to CNCF on [^.]*\.", text)  # one sentence, and the dates in it have no period
    found = re.findall(r"(Sandbox|Incubating|Graduated) maturity level", m.group(0)) if m else []
    return (found[-1].lower(), None) if found else (None, "cncf.io: level not found on the page")


MARKET = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"


def marketplace_stable(ext):
    """(version, date, engine) of the newest version of publisher.name that is not a pre-release, or (None, error, None).
    Flags: versions, version properties, statistics. `code --install-extension` installs this version, not a pre-release."""
    body = json.dumps({"filters": [{"criteria": [{"filterType": 7, "value": ext}], "pageSize": 1}], "flags": 0x1 | 0x10 | 0x100}).encode()
    headers = {**UA, "Content-Type": "application/json", "Accept": "application/json;api-version=7.1-preview.1"}
    for n in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(MARKET, data=body, headers=headers), timeout=30) as r:
                found = json.load(r)["results"][0]["extensions"]
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            if n == 2:
                return None, f"marketplace: {e}", None
            time.sleep(2 * (n + 1))
    if not found:
        return None, f"marketplace: {ext} not found", None
    for v in found[0]["versions"]:
        props = {x["key"].split(".")[-1]: x["value"] for x in v.get("properties", [])}
        if props.get("PreRelease", "false") != "true":
            return v["version"], v["lastUpdated"][:10], props.get("Engine")
    return None, f"marketplace: {ext} has no stable version", None


def check_marketplace(entry):
    i, ext = entry["id"], entry["track"]["marketplace"]
    version, date, engine = marketplace_stable(ext)
    if version is None:
        return [f"{i}: {date}"]
    out = []
    if version != entry["version"]["analysed"]:
        out.append(f"{i}: analysed {entry['version']['analysed']}, latest stable {version} ({date})")
    if engine != entry["extension"].get("engine"):
        out.append(f"{i}: needs VS Code {entry['extension'].get('engine')} in the data, Marketplace says {engine}")
    return out


def check(entry):
    """Differences for one entry, as strings."""
    out = check_marketplace(entry) if entry["track"].get("marketplace") else []
    return out + (check_github(entry) if entry["track"].get("github") else [])


def check_github(entry):
    i, t, out = entry["id"], entry["track"], []
    repo = t["github"]
    status, info = gh(repo)
    if info is None:
        return [f"{i}: repository {repo}: HTTP {status}"]
    if info["archived"] and entry["status"] != "archived":
        out.append(f"{i}: {repo} is archived on GitHub, status is {entry['status']}")
    if not info["archived"] and entry["status"] == "archived":
        out.append(f"{i}: status is archived, {repo} is not archived on GitHub")
    rel, err = latest_release(repo, t.get("tag", ".*"))
    if err:
        out.append(f"{i}: {err}")
    elif rel["tag_name"] != entry["version"]["analysed"]:
        out.append(f"{i}: analysed {entry['version']['analysed']}, latest {rel['tag_name']} ({rel['published_at'][:10]})")
    if t.get("cncf"):
        level, err = cncf_level(t["cncf"])
        if err:
            out.append(f"{i}: {err}")
        elif level != entry["cncf"]["level"]:
            out.append(f"{i}: cncf level is {entry['cncf']['level']}, cncf.io says {level}")
    return out


def broken_links(entry):
    out = []
    for s in entry["sources"] + entry.get("links", []):
        status, _ = fetch(s["url"])
        # 403 and 429 are usually bot protection, not a dead link
        if not isinstance(status, int) or (status >= 400 and status not in (403, 429)):
            out.append(f"{entry['id']}: source {s['url']}: {status}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--links", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = [e for e in data["entries"] if not args.only or e["id"] == args.only]
    tracked = [e for e in entries if e.get("track")]
    with ThreadPoolExecutor(max_workers=6) as ex:
        found = [line for lines in ex.map(check, tracked) for line in lines]
        if args.links:
            found += [line for lines in ex.map(broken_links, entries) for line in lines]
    for line in found:
        print(line)
    print(f"checked {len(tracked)} entries, {len(found)} differences (data checked {data['checked']})")
    if found:
        print("review each one, then update version, facts and `checked` together")
    return 1 if args.strict and found else 0


if __name__ == "__main__":
    sys.exit(main())
