"""Build the Atlas landing page, dist/index.html, from topics.json and shared/landing.html."""
import html
import json

import atlas


def entries(topic):
    """[(entry id, name, summary)] of a topic, for the landing search. Azure reads its resolved services, the others their data file."""
    if topic == "azure":
        path = atlas.DIST / "azure" / "services.resolved.json"
        return [(s["id"], s["name"], s["purpose"]) for s in json.loads(path.read_text(encoding="utf-8"))["services"]]
    path = atlas.SITE / "topics" / topic / "data" / f"{topic}.json"
    return [(e["id"], e["name"], e.get("summary", "")) for e in json.loads(path.read_text(encoding="utf-8"))["entries"]]


def main():
    reg = atlas.load()
    topics = atlas.published()
    page = (atlas.SITE / "shared" / "landing.html").read_text(encoding="utf-8")
    found = {t["id"]: entries(t["id"]) for t in topics}
    index = [[t["id"], t["label"], *e] for t in topics for e in found[t["id"]]]
    cards = "".join(
        '<section data-fam="{id}"><h2>{fam}</h2>{fdesc}<div class="topics">{cards}</div></section>'.format(
            id=f["id"], fam=html.escape(f["label"]),
            fdesc='<p class="fdesc">' + html.escape(f["description"]) + "</p>" if f.get("description") else "",
            cards="".join(
                '<a class="topic" href="{id}/index.html"><b>{label}</b><span>{desc}</span><small>{n}</small></a>'.format(
                    id=t["id"], label=html.escape(t["label"]), desc=html.escape(t["description"]),
                    n="view" if f["id"] == "views" else f"{len(found[t['id']])} entries")
                for t in ts))
        for f, ts in atlas.by_family())
    page = (atlas.themed(page).replace("__NAME__", html.escape(reg["name"])).replace("__TAGLINE__", html.escape(reg["tagline"]))
                .replace("<!--__TOPICS__-->", cards)
                .replace("/*__INDEX__*/", json.dumps(index, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
                .replace(atlas.BANNER_MARK, atlas.banner(None, "")).replace(atlas.CSS_MARK, atlas.CSS).replace(atlas.FOOTER_MARK, atlas.FOOTER))
    atlas.DIST.mkdir(exist_ok=True)
    (atlas.DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"built dist/index.html ({len(topics)} topics, {len(index)} entries searchable)")


if __name__ == "__main__":
    main()
