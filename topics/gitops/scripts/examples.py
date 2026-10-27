"""Fetch the code examples the data points to, instead of copying them by hand.

  examples.py            check: fetch every example and report what changed upstream or can no longer be found (writes nothing)
  examples.py --refresh  fetch every example and save it to data/examples.json, the cache the build reads

A code item in data/gitops.json has a `source` (label, url) and a `match`: a string, or a list of strings for several examples
from the same page, shown in that order. Each string selects the code block on the page that contains it; when several blocks
contain it, the shortest one is used. The cache is generated, never edited by hand: Atlas points to the docs, it does not keep its own copy.
"""
import argparse
import datetime
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "gitops.json"
CACHE = ROOT / "data" / "examples.json"
UA = {"User-Agent": "atlas-check (https://github.com)"}


def key(url, match):
    return url + " | " + match


def refs(data):
    """Every (url, match) the data points to."""
    out = []
    for e in data["entries"]:
        for sec in e["sections"]:
            for it in sec["items"]:
                if isinstance(it, dict) and it.get("type") == "code" and it.get("match"):
                    ms = it["match"] if isinstance(it["match"], list) else [it["match"]]
                    out += [(it["source"]["url"], m) for m in ms]
    return out


def blocks(url, pages):
    """The code blocks of a page, as plain text, fetched once per run."""
    if url not in pages:
        for n in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                    page = r.read().decode("utf-8", "replace")
                break
            except (urllib.error.URLError, TimeoutError):
                if n == 2:
                    raise
                time.sleep(2 * (n + 1))
        pages[url] = [html.unescape(re.sub(r"<[^>]+>", "", b)).strip("\n") for b in re.findall(r"<pre[^>]*>(.*?)</pre>", page, flags=re.S)]
    return pages[url]


def find(url, match, pages):
    hits = [b for b in blocks(url, pages) if match in b]
    return min(hits, key=len) if hits else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    today = datetime.date.today().isoformat()
    pages, found, problems = {}, {}, []
    for url, match in refs(data):
        try:
            body = find(url, match, pages)
        except (urllib.error.URLError, TimeoutError) as e:
            problems.append(f"cannot fetch {url}: {e}")
            continue
        k = key(url, match)
        if body is None:
            problems.append(f"not found upstream: '{match}' on {url}")
        elif k not in cache:
            problems.append(f"not cached yet: '{match}' on {url}")
        elif cache[k]["body"] != body:
            problems.append(f"changed upstream: '{match}' on {url}")
        if body is not None:
            found[k] = {"body": body, "fetched": today if k not in cache or cache[k]["body"] != body else cache[k]["fetched"], "checked": today}
    for p in problems:
        print(p)
    if args.refresh:
        missing = [p for p in problems if p.startswith(("not found", "cannot fetch"))]
        if missing:
            print("nothing written: fix the match strings above first")
            return 1
        CACHE.write_text(json.dumps(dict(sorted(found.items())), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {len(found)} examples to data/examples.json")
        return 0
    print(f"checked {len(found)} examples, {len(problems)} differences")
    if problems:
        print("review each one, then run make examples to refresh the cache")
    return 0


if __name__ == "__main__":
    sys.exit(main())
