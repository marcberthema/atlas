"""Build dist/github-actions/index.html: the shared page (shared/topic.html) with this topic's data/github-actions.json and templates/view.json."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "shared"))
import build_topic  # noqa: E402

if __name__ == "__main__":
    build_topic.build("github-actions")
