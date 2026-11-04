"""Build the dashboard-derived KRAS radial comparisons. Requires Node and librsvg."""
from pathlib import Path
import subprocess
import shutil
import json
import hashlib

root = Path(__file__).resolve().parent
subprocess.run(['node', str(root / 'make.mjs')], check=True)
subprocess.run(['python3', str(root / 'combine.py')], check=True)

receipt = json.loads((root / 'provenance.json').read_text())
receipt['command'] = 'python3 figures/jaxka-kras-pmhc-radial/make.py'
for name in ('make.py', 'combine.py', 'fig.pdf', 'fig.svg', 'fig.png'):
    receipt['hashes'][name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
(root / 'provenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
