from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from opig027_replacements import build
build(Path(__file__).resolve().parent)
