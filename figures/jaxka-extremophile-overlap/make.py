from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import opig027 as base
from opig027_replacements import overlap
base.style()
overlap(base.load("analysis.json"), Path(__file__).resolve().parent)
