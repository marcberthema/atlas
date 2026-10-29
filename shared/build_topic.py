"""Build dist/<topic>/index.html from a topic's data and view, with the shared page (shared/topic.html).

A topic keeps: data/<topic>.json (the content), data/examples.json (code examples fetched by shared/examples.py, never edited by hand)
and templates/view.json (the page title and its tabs). The look and the script of the page are shared by every topic that uses it.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import atlas  # noqa: E402

JOIN = {"yaml": "\n---\n", "shell": "\n", "text": "\n"}


def fill_examples(data, cache, topic):
    """Put the fetched text of each code example in place. The cache is written by shared/examples.py, never by hand."""
    for e in data["entries"]:
        for sec in e["sections"]:
            for it in sec["items"]:
                if isinstance(it, dict) and it.get("type") == "code" and it.get("match"):
                    ms = it["match"] if isinstance(it["match"], list) else [it["match"]]
                    got = [cache.get(it["source"]["url"] + " | " + m) for m in ms]
                    assert all(got), f"{topic}/{e['id']}: example not in data/examples.json, run make examples ({it['title']})"
                    it["body"] = JOIN[it["lang"]].join(g["body"] for g in got)
                    it["fetched"] = min(g["fetched"] for g in got)
                    it["count"] = len(got)


def build(topic, root=None, out=None):
    """A published topic lives in topics/<topic> and builds into dist/<topic>. A resource kept in git but not published passes
    its own `root` and `out` folder: its banner then names only itself (atlas.apply_standalone)."""
    standalone = root is not None
    root = Path(root) if standalone else atlas.SITE / "topics" / topic
    data = json.loads((root / "data" / f"{topic}.json").read_text(encoding="utf-8"))
    view = json.loads((root / "templates" / "view.json").read_text(encoding="utf-8"))
    assert data.get("title") and isinstance(data.get("entries"), list), f"{topic}.json needs a title and an entries list"
    cache_file = root / "data" / "examples.json"
    fill_examples(data, json.loads(cache_file.read_text(encoding="utf-8")) if cache_file.exists() else {}, topic)
    ids = {e["id"] for e in data["entries"]}
    for t in view["tabs"]:
        assert t["id"] in ids or t["id"] in ("others", "compare") or t.get("group"), f"{topic}: tab {t['id']} is not an entry id"
    page = (atlas.SITE / "shared" / "topic.html").read_text(encoding="utf-8")
    for marker, value in (("/*__TITLE__*/", view["title"]), ("/*__TABS__*/[]", json.dumps(view["tabs"], ensure_ascii=False))):
        assert page.count(marker) == 1, f"shared/topic.html needs exactly one {marker}"
        page = page.replace(marker, value)
    marker = "/*__DATA__*/"
    assert page.count(marker) == 1, "template needs exactly one data marker"
    # "</" would end the script element early
    page = page.replace(marker, json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = atlas.apply_standalone(page, view["title"]) if standalone else atlas.apply(page, topic)
    out = Path(out) if out else atlas.DIST / topic
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"built {(out / 'index.html').relative_to(atlas.SITE)} ({len(data['entries'])} entries)")


if __name__ == "__main__":
    build(sys.argv[1])
