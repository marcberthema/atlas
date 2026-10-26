"""Build dist/azure/ from data/services.json and templates/index.html.

dist/azure/services.resolved.json  layers merged, Terraform status derived: the stable contract for other front ends
dist/azure/index.html              the template with that JSON embedded and the Atlas banner
"""
import json
import sys

import model

sys.path.insert(0, str(model.SITE / "shared"))
import atlas  # noqa: E402

TEMPLATE = model.ROOT / "templates" / "index.html"
DIST = atlas.DIST / "azure"


def main():
    resolved = model.resolve(model.load())
    DIST.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(resolved, indent=2, ensure_ascii=False)
    (DIST / "services.resolved.json").write_text(payload + "\n", encoding="utf-8")
    page = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/"
    assert page.count(marker) == 1, "template needs exactly one data marker"
    # "</" would end the script element early
    page = atlas.apply(page.replace(marker, payload.replace("</", "<\\/")), "azure")
    (DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"built dist/azure/index.html and dist/azure/services.resolved.json ({len(resolved['services'])} services)")


if __name__ == "__main__":
    main()
