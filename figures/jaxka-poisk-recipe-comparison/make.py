"""Extend experiment 028's original connected-point figure to three recipes."""
from __future__ import annotations
import csv
import hashlib
import json
import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/jaxka-poisk-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
SURFACE, INK, INK2, GRID = '#fcfcfb', '#0b0b0b', '#52514e', '#e4e3df'
MODES = (
    ('apo', '', 'Free monomers, apo refolds (ABB2 / ESMFold)', '#2a78d6', 0.22),
    ('bound_conformers', 'bc_', 'Free monomers, bound conformers (split from the complex)', '#eb6834', 0.0),
    ('complex', 'cx_', 'Complex (Protenix-v2 pose), not blind', '#1baf7a', -0.22),
)
MODELS = ('run4', 'hmask', 'drsa')
READOUTS = (
    ('edge_all', 'Edges, Σp (whole Fv)', 'abc'),
    ('edge_cdr', 'Edges, Σp (CDRs)', 'abc'),
    ('bur_all', 'Edges × free exposure, Σp·x·y (whole Fv)', 'ab'),
    ('bur_cdr', 'Edges × free exposure, Σp·x·y (CDRs)', 'ab'),
    ('bur_cdr_share', 'CDR share of Σp·x·y', 'ab'),
    ('edge_max_cdr', 'Max contact probability (CDRs)', 'abc'),
    ('edge_top50_cdr', 'Top-50 mean contact probability (CDRs)', 'abc'),
    ('contacts', 'Contacts p > 0.5 (whole Fv)', 'c'),
    ('dbur_total', 'Burial change Δb (predicted dRSA), Fv + antigen', 'abc'),
    ('dbur_fv', 'Burial change Δb (predicted dRSA), whole Fv', 'abc'),
    ('dbur_cdr', 'Burial change Δb (predicted dRSA), CDRs', 'abc'),
    ('dbur_cdr_frac', 'CDR share of Fv Δb', 'abc'),
    ('dbur_ag', 'Burial change Δb (predicted dRSA), antigen', 'abc'),
    ('edge_x_dbur', 'dRSA-weighted edges, Σp·Δb·Δb (whole Fv)', 'abc'),
    ('edge_x_dbur_cdr', 'dRSA-weighted edges, Σp·Δb·Δb (CDRs)', 'abc'),
)

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    with (HERE / 'pairwise_accuracy.csv').open(newline='') as handle:
        rows = {row['']: row for row in csv.DictReader(handle)}
    with (HERE / 'paper_baselines.csv').open(newline='') as handle:
        baselines = {row['score']: row for row in csv.DictReader(handle)}
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'pdf.fonttype': 42, 'svg.fonttype': 'none'})
    n_rows = len(READOUTS)
    fig, ax = plt.subplots(figsize=(9.5, 2.7 + 0.47 * n_rows), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.spines['bottom'].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=0)
    ax.axvline(0.5, color=INK2, lw=1, ls=(0, (3, 3)))
    ax.text(0.5, n_rows - 0.35, 'chance', color=INK2, fontsize=8.5, ha='center', va='bottom')
    for key, label, linestyle in (
        ('ipsae_boltz2', 'Boltz-2 ipSAE', (0, (1, 2))),
        ('ipsae_protenixv2', 'Protenix-v2 ipSAE', '-'),
    ):
        value = float(baselines[key]['pairwise'])
        ax.axvline(value, color=INK2, lw=1, ls=linestyle)
        ax.text(value, n_rows - 0.35, label, color=INK2, fontsize=8.5, ha='center', va='bottom')
    plotted = []
    for mode_index, (mode, prefix, label, colour, offset) in enumerate(MODES):
        letter = 'abc'[mode_index]
        for row_index, (key, readout, enabled) in enumerate(READOUTS):
            if letter not in enabled:
                continue
            source_key = prefix + key
            row = rows[source_key]
            y = n_rows - 1 - row_index + offset
            values = [float(row[model]) for model in MODELS]
            n_pairs = int(row['n_pairs'])
            if n_pairs != (11111 if mode == 'apo' else 11115) or any(not 0 <= v <= 1 for v in values):
                raise ValueError(source_key)
            ax.plot(values[:2], [y, y], color=colour, lw=2, alpha=0.43, solid_capstyle='round', zorder=2)
            ax.plot(values[1:], [y, y], color=colour, lw=2, alpha=0.72, solid_capstyle='round', zorder=2)
            ax.plot(values[0], y, 'o', ms=8, mfc=SURFACE, mec=colour, mew=2, zorder=3)
            ax.plot(values[1], y, 'D', ms=7.6, mfc=SURFACE, mec=colour, mew=1.8, zorder=4)
            ax.plot(values[2], y, 'o', ms=7.6, mfc=colour, mec=SURFACE, mew=1.5, zorder=5)
            for model, accuracy in zip(MODELS, values):
                plotted.append(dict(mode=mode, readout=key, readout_label=readout, model=model,
                                    pairwise_accuracy=accuracy, n_pairs=n_pairs, source_row=source_key))
    handles = [Line2D([], [], marker='o', linestyle='none', color=colour, markersize=7, label=label)
               for _, _, label, colour, _ in MODES]
    handles += [
        Line2D([], [], marker='o', linestyle='none', ms=8, mfc=SURFACE, mec=INK2, mew=2, label='hollow circle: run 4'),
        Line2D([], [], marker='D', linestyle='none', ms=7, mfc=SURFACE, mec=INK2, mew=1.8, label='hollow diamond: hmask'),
        Line2D([], [], marker='o', linestyle='none', ms=8, mfc=INK2, mec=SURFACE, mew=1.5, label='filled circle: dRSA'),
    ]
    ax.set_yticks(list(range(n_rows))[::-1], [label for _, label, _ in READOUTS], color=INK, fontsize=9.5)
    ax.set_xlim(0.33, 0.78)
    ax.set_ylim(-0.7, n_rows - 0.1)
    ax.set_xlabel('Pairwise accuracy: share of pairs where the binder outscores its decoy', color=INK2, fontsize=9.5)
    ax.grid(axis='x', color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title('GQT by mode:\nrun 4 → hmask → dRSA', color=INK, fontsize=12, loc='left', pad=128)
    ax.legend(handles=handles, loc='lower left', bbox_to_anchor=(0, 1.04), frameon=False, fontsize=9, labelcolor=INK)
    fig.tight_layout()
    for suffix in ('pdf', 'svg', 'png'):
        fig.savefig(HERE / f'fig.{suffix}', dpi=190, facecolor=SURFACE)
    plt.close(fig)
    with (HERE / 'plotted_data.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(plotted[0]))
        writer.writeheader()
        writer.writerows(plotted)
    provenance = json.loads((HERE / 'source.json').read_text())
    provenance.update({
        'figure_id': HERE.name,
        'inputs': {name: sha256(HERE / name) for name in ('pairwise_accuracy.csv', 'paper_baselines.csv')},
        'plotting_code_sha256': sha256(Path(__file__)),
        'build_command': f'python figures/{HERE.name}/make.py',
        'dependencies': {'matplotlib': matplotlib.__version__},
        'selection': 'Original general contact/burial readouts plus top-50 CDR contact probability; no hotspot-specific readouts.',
        'visual_source': 'Experiment 028 figures.py accuracy_chart; original mode colours, background, layout and reference lines.',
        'values_plotted': len(plotted),
        'output_sha256': {f'fig.{ext}': sha256(HERE / f'fig.{ext}') for ext in ('pdf', 'svg', 'png')},
    })
    (HERE / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Built {HERE.name}: {len(plotted)} values, PDF / SVG / PNG.')

if __name__ == '__main__':
    main()
