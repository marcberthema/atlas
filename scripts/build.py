"""Build dist/ from data/services.json and templates/index.html.

dist/services.resolved.json  layers merged, Terraform status derived: the stable contract for other front ends
dist/index.html              the template with that JSON embedded
"""
import json

import model

TEMPLATE = model.ROOT / "templates" / "index.html"
DIST = model.ROOT / "dist"


def main():
    resolved = model.resolve(model.load())
    DIST.mkdir(exist_ok=True)
    payload = json.dumps(resolved, indent=2, ensure_ascii=False)
    (DIST / "services.resolved.json").write_text(payload + "\n", encoding="utf-8")
    page = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/"
    assert page.count(marker) == 1, "template needs exactly one data marker"
    # "</" would end the script element early
    (DIST / "index.html").write_text(page.replace(marker, payload.replace("</", "<\\/")), encoding="utf-8")
    print(f"built dist/index.html and dist/services.resolved.json ({len(resolved['services'])} services)")


if __name__ == "__main__":
    main()
