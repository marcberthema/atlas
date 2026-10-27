"""Build dist/gitops/index.html from data/gitops.json and templates/index.html."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent / "shared"))
import atlas  # noqa: E402

DATA = ROOT / "data" / "gitops.json"
EXAMPLES = ROOT / "data" / "examples.json"
JOIN = {"yaml": "\n---\n", "shell": "\n", "text": "\n"}


def fill_examples(data):
    """Put the fetched text of each code example in place. The cache is written by scripts/examples.py, never by hand."""
    cache = json.loads(EXAMPLES.read_text(encoding="utf-8")) if EXAMPLES.exists() else {}
    for e in data["entries"]:
        for sec in e["sections"]:
            for it in sec["items"]:
                if isinstance(it, dict) and it.get("type") == "code" and it.get("match"):
                    ms = it["match"] if isinstance(it["match"], list) else [it["match"]]
                    got = [cache.get(it["source"]["url"] + " | " + m) for m in ms]
                    assert all(got), f"{e['id']}: example not in data/examples.json, run make examples ({it['title']})"
                    it["body"] = JOIN[it["lang"]].join(g["body"] for g in got)
                    it["fetched"] = min(g["fetched"] for g in got)
                    it["count"] = len(got)
TEMPLATE = ROOT / "templates" / "index.html"
DIST = atlas.DIST / "gitops"


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert data.get("title") and isinstance(data.get("entries"), list), "gitops.json needs a title and an entries list"
    fill_examples(data)
    DIST.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/"
    assert page.count(marker) == 1, "template needs exactly one data marker"
    # "</" would end the script element early
    page = atlas.apply(page.replace(marker, json.dumps(data, ensure_ascii=False).replace("</", "<\\/")), "gitops")
    (DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"built dist/gitops/index.html ({len(data['entries'])} entries)")


if __name__ == "__main__":
    main()
