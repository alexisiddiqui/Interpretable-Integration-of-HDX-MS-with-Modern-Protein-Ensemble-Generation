from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # tools/kb-lint
sys.path.insert(0, str(Path(__file__).resolve().parent))      # tests/helpers.py

from helpers import build_repo  # noqa: E402


@pytest.fixture
def repo(tmp_path):
    """A fixture repository that passes every check; tests break one thing at a time."""
    root = tmp_path / "repo"
    build_repo(root)
    return root
