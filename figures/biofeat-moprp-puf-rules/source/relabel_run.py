"""Run a plotting script unchanged and replace the historical PCA basin labels in its figures at save time.

Every Figure.savefig call first draws the figure, then (with RELABEL_MAP) rewrites each text artist and each fixed or
categorical tick formatter through the map, so data, layout code and numbers are those of the original script.
RELABEL_MAP: JSON list of [kind, old, new], kind "exact" (whole text equal to old) or "sub" (substring), applied in order,
exact matches first. RELABEL_INVENTORY: file to which every non-empty text of every saved figure is appended (JSON lines).

Usage: relabel_run.py <script.py> [script args ...]"""
import json, os, runpy, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.category as mcat
import matplotlib.figure as mfig
import matplotlib.patheffects as pe
from matplotlib.colors import to_rgb
import matplotlib.ticker as mtick
from matplotlib.text import Text

MAP = json.load(open(os.environ["RELABEL_MAP"])) if os.environ.get("RELABEL_MAP") else None
INV = os.environ.get("RELABEL_INVENTORY")
_save = mfig.Figure.savefig


def rep(s):
    for kind, a, b in MAP:
        if kind == "exact" and s == a:
            return b
    for kind, a, b in MAP:
        if kind == "sub":
            s = s.replace(a, b)
    return s


def savefig(self, fname, *args, **kw):
    self.canvas.draw()
    texts = [t for t in self.findobj(Text) if t.get_text().strip()]
    if INV:
        with open(INV, "a") as fh:
            for t in texts:
                fh.write(json.dumps([os.path.basename(str(fname)), t.get_text()], ensure_ascii=False) + "\n")
    if MAP:
        for ax in self.axes:
            for axis in (ax.xaxis, ax.yaxis):
                f = axis.get_major_formatter()
                if isinstance(f, mtick.FixedFormatter):
                    f.seq = [rep(x) for x in f.seq]
                elif isinstance(f, mcat.StrCategoryFormatter):
                    f._units = {rep(k): v for k, v in f._units.items()}
                elif isinstance(f, mtick.FuncFormatter) and not getattr(f, "_relabelled", False):
                    # set_ticklabels stores fixed labels as a FuncFormatter in recent matplotlib
                    f.func = (lambda g: lambda x, pos=None: rep(str(g(x, pos))))(f.func); f._relabelled = True
        for t in texts:
            new = rep(t.get_text())
            if new != t.get_text():
                t.set_text(new)
                # white labels on maps: the longer names reach empty (white) bins, so give them a thin dark outline
                if to_rgb(t.get_color()) == (1.0, 1.0, 1.0):
                    t.set_path_effects([pe.withStroke(linewidth=1.6, foreground="0.25")])
        # the names are longer than the old labels and layouts were fixed before the swap, so let the canvas grow to fit
        kw.setdefault("bbox_inches", "tight")
    return _save(self, fname, *args, **kw)


mfig.Figure.savefig = savefig
script, *args = sys.argv[1:]
sys.argv = [script] + args
sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
runpy.run_path(script, run_name="__main__")
