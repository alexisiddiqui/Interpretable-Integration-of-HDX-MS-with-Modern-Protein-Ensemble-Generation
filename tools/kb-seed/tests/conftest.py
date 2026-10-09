from pathlib import Path
import sys

import pytest

TOOLS = Path(__file__).resolve().parents[2]
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS / "kb-seed"))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # seed_helpers

from seed_helpers import make_repo, make_zotero  # noqa: E402


@pytest.fixture
def zotero_home(tmp_path):
    return make_zotero(tmp_path / "Zotero")


@pytest.fixture
def seed_repo(tmp_path):
    """Repository with the two introductions and bibs, using the real kb/_templates/."""
    return make_repo(tmp_path / "repo", REPO / "kb" / "_templates")
