"""Build site/index.html: the shared page (shared/topic.html) with data/vscode.json and templates/view.json.
Not part of the published Atlas: the output stays in this folder, outside dist/."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent / "shared"))
import build_topic  # noqa: E402

if __name__ == "__main__":
    build_topic.build("vscode", root=ROOT, out=ROOT / "site")
