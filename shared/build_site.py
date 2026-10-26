"""Build the Atlas landing page, dist/index.html, from topics.json and shared/landing.html."""
import html

import atlas


def main():
    reg = atlas.load()
    page = (atlas.SITE / "shared" / "landing.html").read_text(encoding="utf-8")
    cards = "".join(
        '<a class="topic" href="{id}/index.html"><b>{label}</b><span>{desc}</span></a>'.format(
            id=t["id"], label=html.escape(t["label"]), desc=html.escape(t["description"]))
        for t in reg["topics"])
    page = (page.replace("__NAME__", html.escape(reg["name"])).replace("__TAGLINE__", html.escape(reg["tagline"]))
                .replace("<!--__TOPICS__-->", cards)
                .replace(atlas.BANNER_MARK, atlas.banner(None, "")).replace(atlas.CSS_MARK, atlas.CSS))
    atlas.DIST.mkdir(exist_ok=True)
    (atlas.DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"built dist/index.html ({len(reg['topics'])} topics)")


if __name__ == "__main__":
    main()
