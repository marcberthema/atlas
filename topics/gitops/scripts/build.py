"""Build dist/gitops/index.html from data/gitops.json and templates/index.html."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent.parent / "shared"))
import atlas  # noqa: E402

DATA = ROOT / "data" / "gitops.json"
TEMPLATE = ROOT / "templates" / "index.html"
DIST = atlas.DIST / "gitops"


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    assert data.get("title") and isinstance(data.get("sections"), list), "gitops.json needs a title and a sections list"
    DIST.mkdir(parents=True, exist_ok=True)
    page = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/"
    assert page.count(marker) == 1, "template needs exactly one data marker"
    # "</" would end the script element early
    page = atlas.apply(page.replace(marker, json.dumps(data, ensure_ascii=False).replace("</", "<\\/")), "gitops")
    (DIST / "index.html").write_text(page, encoding="utf-8")
    print(f"built dist/gitops/index.html ({len(data['sections'])} sections)")


if __name__ == "__main__":
    main()
