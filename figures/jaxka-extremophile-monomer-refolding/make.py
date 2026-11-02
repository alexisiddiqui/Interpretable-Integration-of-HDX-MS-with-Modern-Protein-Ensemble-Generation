from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from opig027 import build
build("monomer", Path(__file__).resolve().parent)
