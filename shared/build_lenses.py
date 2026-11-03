"""Build the lenses view (views/lenses/, spec in views/lenses/docs/spec.md) into dist/lenses/index.html.

The data is embedded in the page as JSON and drawn in the browser, so the page works from file:// and needs no fetch.
Unlike the other views it has a catalogue of its own: views/lenses/data/lenses.json, checked by shared/lenses_check.py.
"""
import html
import json
import sys

import atlas
import lenses_check

VIEW_ID = "lenses"


def main():
    bad, warn = lenses_check.check()
    for line in bad:
        print("bad:", line)
    if bad:
        sys.exit(1)
    reg = atlas.load()
    v = next(x for x in reg.get("views", []) if x["id"] == VIEW_ID)
    data = lenses_check.load()
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (atlas.SITE / "shared" / "lenses.html").read_text(encoding="utf-8")
    page = (atlas.themed(template).replace("__TITLE__", html.escape(v["label"])).replace("__NAME__", html.escape(reg["name"]))
            .replace("__CHECKED__", html.escape(data["checked"])).replace("__DATA__", blob)
            .replace(atlas.BANNER_MARK, atlas.banner(VIEW_ID, "../")).replace(atlas.CSS_MARK, atlas.CSS).replace(atlas.FOOTER_MARK, atlas.FOOTER))
    out = atlas.DIST / VIEW_ID
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    print(f"built dist/{VIEW_ID}/index.html")


if __name__ == "__main__":
    main()
