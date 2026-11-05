"""Regenerate the PINDER figures from the checked-in audit reports.

No training or inference. Run either figure directory's make.py.
"""
from pathlib import Path
import csv
import hashlib
import json
import os

os.environ.setdefault('MPLCONFIGDIR', '/private/tmp/jaxka-pinder-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

ROOT = Path(__file__).resolve().parent
SUPPORT = ROOT / 'jaxka-pinder-ablations'
INPUT = SUPPORT / 'inputs'
BLUE, ORANGE, TEAL, GREY = '#346BA3', '#D97732', '#087E75', '#66717D'
INK = '#20242C'
SEEDS = [17, 29, 43]


def read(name):
    return json.loads((INPUT / name).read_text())


def md_rows(name):
    return [[c.strip() for c in line.strip('|').split('|')]
            for line in (INPUT / name).read_text().splitlines()
            if line.startswith('|')]


def load():
    for source in json.loads((SUPPORT / 'source.json').read_text())['files']:
        assert hashlib.sha256((SUPPORT / source['input']).read_bytes()).hexdigest() == source['sha256']
    summary = read('recipe-summary.json')
    negatives = read('negatives.json')['runs']
    rows = []

    def add(group, recipe, seed, metric, value, source, field, **extra):
        rows.append(dict(group=group, recipe=recipe, seed=seed, metric=metric,
                         value=float(value), source=source, field=field, **extra))

    r4 = negatives['run 4 w64']
    for metric, value, source, field in [
        ('edge_AP', r4['edges_10A_free']['ap'], 'negatives.json', 'runs/run 4 w64/edges_10A_free/ap'),
        ('AbAg_accuracy', r4['swap_same_stratum']['Ab/Ag']['accuracy'], 'negatives.json', 'runs/run 4 w64/swap_same_stratum/Ab/Ag/accuracy'),
        ('binding_MAE', read('run4-residue.json')['run 4 w64']['pka']['paired_all_no_bonded'], 'run4-residue.json', 'run 4 w64/pka/paired_all_no_bonded')]:
        add('recipe', 'run4', 17, metric, value, source, field)
    for seed in SEEDS:
        for arm, recipe in [('control', 'hmask'), ('drsa', 'dRSA')]:
            b = summary['binding']['per_seed'][str(seed)][arm]
            for metric, key in [('edge_AP', 'edge_AP'), ('AbAg_accuracy', 'swap_AbAg_accuracy')]:
                add('recipe', recipe, seed, metric, b[key], 'recipe-summary.json', f'binding/per_seed/{seed}/{arm}/{key}')
            shift = summary['binding_shifts']['results'][str(seed)][arm]['metrics']['overall']
            assert shift['sites'] == 29305
            add('recipe', recipe, seed, 'binding_MAE', shift['MAE'], 'recipe-summary.json', f'binding_shifts/results/{seed}/{arm}/metrics/overall/MAE')
    for arm in ['run 4 w64', 'decoy both w64', 'within 0.1 s17', 'within 0.3 s17', 'within 1.0 s17']:
        for metric, key in [('all_accuracy', 'all'), ('AbAg_accuracy', 'Ab/Ag')]:
            add('negatives', arm, 17, metric, negatives[arm]['swap_same_stratum'][key]['accuracy'], 'negatives.json', f'runs/{arm}/swap_same_stratum/{key}/accuracy')
    for cells in md_rows('anm.md'):
        if not cells[0].startswith(('ctrl s', 'anmcons s')):
            continue
        arm, seed = cells[0].split(' s')
        if cells[1] == 'a2':
            assert int(cells[2]) == 793
            add('anm', arm, int(seed), 'perturbation_penalty', cells[7], 'anm.md', f'Robustness/{cells[0]}/pKa alt - crystal')
        else:
            for metric, column in [('AbAg_accuracy', 1), ('all_accuracy', 2)]:
                add('anm', arm, int(seed), metric, cells[column], 'anm.md', f'Crystal/{cells[0]}/{metric}')
    for seed in SEEDS:
        b = summary['binding']['per_seed'][str(seed)]['drsa']
        for metric, key in [('edge_AP', 'edge_AP'), ('AbAg_accuracy', 'swap_AbAg_accuracy')]:
            add('capacity', 'w064', seed, metric, b[key], 'recipe-summary.json', f'binding/per_seed/{seed}/drsa/{key}')
    for arm in ['w096', 'w128', 'rel61', 'rel66']:
        for seed in ([17] if arm == 'w096' else SEEDS):
            name = f'{arm}-s{seed}.md'
            cells = next(x for x in md_rows(name) if x[0] == 'unmasked')
            for metric, column in [('edge_AP', 5), ('AbAg_accuracy', 7)]:
                add('capacity', arm, seed, metric, cells[column], name, f'unmasked/{metric}')
    audit = []
    for arm in ['w064', 'w128', 'e40-w064', 'e40-w128']:
        name = f'audits/datascale-v1/{arm}/masked2/report.json'
        report = read(name)
        record = report['runs'][arm]
        m = record['modes']['unmasked']
        assert report['validation']['complexes'] == 800
        assert m['swap_same_stratum']['Ab/Ag']['n'] == 645
        assert m['swap_same_stratum']['all']['n'] == 4000
        assert m['edges_10A_free']['pairs'] == 18956558
        run_dir = f'training/gqt-production-v2/runs/{record["run"]}'
        protocol, selection = read(run_dir + '/protocol.json'), read(run_dir + '/selection.json')
        history = [json.loads(x) for x in (INPUT / run_dir / 'history.jsonl').read_text().splitlines()]
        resource = read(f'audits/datascale-v1/{arm}/train_resources.json')
        assert resource['exit'] == 0 and protocol['fraction'] == 1 and not protocol['test_data_included']
        assert selection['selected_epoch'] == record['selected_epoch']
        assert selection['epochs_run'] == len(history)
        assert protocol['manifests'] == read('drsa-model.json')['protocol']['manifests']
        assert all(h['train_loss']['pinder_mask_fallbacks'] == 0 for h in history)
        assert protocol['hotspot_mask']['store_records'] == 28733
        residue_name = f'audits/datascale-v1/{arm}/residue/report.json'
        pka = read(residue_name)[arm]['pka']
        assert pka['epoch'] == record['selected_epoch']
        for metric, value, source, field in [
            ('edge_AP', m['edges_10A_free']['ap'], name, 'modes/unmasked/edges_10A_free/ap'),
            ('AbAg_accuracy', m['swap_same_stratum']['Ab/Ag']['accuracy'], name, 'modes/unmasked/swap_same_stratum/Ab/Ag/accuracy'),
            ('all_accuracy', m['swap_same_stratum']['all']['accuracy'], name, 'modes/unmasked/swap_same_stratum/all/accuracy'),
            ('selection_MAE_clean', pka['selection_no_bonded'], residue_name, 'pka/selection_no_bonded'),
            ('binding_MAE', pka['paired_all_no_bonded'], residue_name, 'pka/paired_all_no_bonded')]:
            add('data', arm, 17, metric, value, source, field, selected_epoch=record['selected_epoch'], epochs_run=len(history))
        audit.append(dict(arm=arm, run=record['run'], selected_epoch=record['selected_epoch'],
                          epochs_run=len(history), exit=resource['exit'], hotspot_fallbacks=0,
                          hotspot_records=28733, schedule=protocol['schedule'],
                          validation=report['validation'], manifests=protocol['manifests']))
    assert len({json.dumps(a['manifests'], sort_keys=True) for a in audit}) == 1
    (SUPPORT / 'scaling-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    return rows


def values(rows, group, recipe, metric):
    return sorted([r for r in rows if (r['group'], r['recipe'], r['metric']) == (group, recipe, metric)], key=lambda r: r['seed'])


def style():
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
        'axes.titlesize': 10.5, 'axes.labelsize': 9, 'xtick.labelsize': 8.5,
        'ytick.labelsize': 8.5, 'axes.spines.top': False, 'axes.spines.right': False,
        'axes.linewidth': .7, 'axes.edgecolor': '#B0B5BB', 'text.color': INK,
        'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK,
        'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'svg.fonttype': 'none'})


def panel(ax, title, ylabel):
    ax.set_title(title, loc='left', fontweight='bold', pad=15)
    ax.set_ylabel(ylabel, labelpad=7)
    ax.set_axisbelow(True)
    ax.grid(axis='y', color='#E8EBEE', linewidth=.65)
    ax.tick_params(length=3, width=.65)
    ax.tick_params(axis='x', length=0, pad=8)


def seed_points(ax, rows, group, recipes, metric, colors, connect=True, annotate=False):
    seed_x = {17: -.085, 29: 0, 43: .085}
    if connect:
        for seed in SEEDS:
            xy = [(x + (seed_x[seed] if len(values(rows, group, arm, metric)) > 1 else 0), r['value']) for x, arm in enumerate(recipes)
                  for r in values(rows, group, arm, metric) if r['seed'] == seed]
            if len(xy) > 1:
                ax.plot(*zip(*xy), color='#CCD2D8', lw=.8, zorder=1)
    for x, (arm, color) in enumerate(zip(recipes, colors)):
        rr = values(rows, group, arm, metric)
        yy = [r['value'] for r in rr]
        ax.scatter([x + (seed_x[r['seed']] if len(rr) > 1 else 0) for r in rr], yy,
                   color=color, s=37, edgecolor='white', linewidth=.65, zorder=4)
        mean = np.mean(yy)
        if len(rr) > 1:
            ax.plot([x-.16, x+.16], [mean, mean], color=color, lw=2.5, solid_capstyle='round', zorder=5)
        if annotate:
            ax.annotate(f'{mean:.4f}', (x, max(yy)), xytext=(0, 10), textcoords='offset points',
                        ha='center', fontsize=9, color=color)
    ax.set_xlim(-.4, len(recipes)-.6)


def save(fig, directory, rows):
    directory.mkdir(exist_ok=True)
    for ext in ['pdf', 'svg', 'png']:
        fig.savefig(directory / f'fig.{ext}', dpi=220)
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (directory / 'plotted-data.csv').open('w') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    plt.close(fig)


def recipe():
    rows = load(); style()
    fig, axs = plt.subplots(1, 3, figsize=(10.6, 3.65))
    fig.subplots_adjust(left=.075, right=.985, bottom=.23, top=.82, wspace=.43)
    specs = [('A  Contact prediction', 'Contact-edge AP ↑', 'edge_AP', (.024, .052)),
             ('B  Partner discrimination', 'Antibody/antigen swap accuracy ↑', 'AbAg_accuracy', (.61, .735)),
             ('C  Binding-shift prediction', 'Binding ΔpKa MAE ↓', 'binding_MAE', (.0615, .069))]
    for ax, (title, ylabel, metric, ylim) in zip(axs, specs):
        panel(ax, title, ylabel)
        seed_points(ax, rows, 'recipe', ['run4', 'hmask', 'dRSA'], metric, [GREY, BLUE, TEAL], annotate=True)
        ax.set_xticks(range(3), ['Run4\n1 seed', 'Hmask\n3 seeds', 'dRSA\n3 seeds'])
        ax.set_ylim(ylim)
    axs[2].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    fig.text(.075, .04, 'PINDER development validation · 50% training pool · points show seeds; bars show means', fontsize=8.5, color=GREY)
    save(fig, ROOT / 'jaxka-pinder-recipe-comparison', [r for r in rows if r['group'] == 'recipe'])


def ablations():
    rows = load(); style()
    fig, axs = plt.subplots(2, 3, figsize=(11.6, 7.35))
    fig.subplots_adjust(left=.075, right=.985, bottom=.16, top=.91, wspace=.40, hspace=.68)
    ax = axs[0, 0]
    panel(ax, 'A  Negative construction', 'Swapped-partner accuracy ↑')
    arms = ['run 4 w64', 'decoy both w64', 'within 0.1 s17', 'within 0.3 s17', 'within 1.0 s17']
    for metric, color, label in [('all_accuracy', BLUE, 'All strata'), ('AbAg_accuracy', ORANGE, 'Antibody/antigen')]:
        yy = [values(rows, 'negatives', arm, metric)[0]['value'] for arm in arms]
        ax.plot(range(5), yy, 'o-', color=color, ms=5, lw=1.1, markeredgecolor='white', markeredgewidth=.6, label=label)
    ax.set_xticks(range(5), ['Run4', 'Decoy\nboth', 'Within\n0.1', 'Within\n0.3', 'Within\n1.0'])
    ax.set_ylim(.53, .91); ax.legend(loc='upper left', frameon=False, fontsize=8, handlelength=1.3)
    ax = axs[0, 1]
    panel(ax, 'B  ANM and discrimination', 'Swapped-partner accuracy ↑')
    for metric, color, label in [('all_accuracy', BLUE, 'All strata'), ('AbAg_accuracy', ORANGE, 'Antibody/antigen')]:
        seed_points(ax, rows, 'anm', ['ctrl', 'anmcons'], metric, [color]*2)
        ax.plot([], [], 'o-', color=color, lw=1, ms=4, label=label)
    ax.set_xticks([0, 1], ['Hmask', '+ ANM\nconsistency']); ax.set_ylim(.64, .805)
    ax.legend(loc='upper left', frameon=False, fontsize=8, handlelength=1.3)
    ax = axs[0, 2]
    panel(ax, 'C  ANM perturbation tolerance', 'Increase in state + interface MAE ↓')
    seed_points(ax, rows, 'anm', ['ctrl', 'anmcons'], 'perturbation_penalty', [GREY, TEAL], annotate=True)
    ax.set_xticks([0, 1], ['Hmask', '+ ANM\nconsistency']); ax.set_ylim(.015, .047)
    ax.text(.98, .95, '≈2 Å views · 793 complexes', transform=ax.transAxes, ha='right', va='top', color=GREY, fontsize=8)
    ax = axs[1, 0]
    panel(ax, 'D  Width and relation maps', 'Antibody/antigen swap accuracy ↑')
    arms = ['w064', 'w096', 'w128', 'rel61', 'rel66']
    seed_points(ax, rows, 'capacity', arms, 'AbAg_accuracy', [TEAL, BLUE, BLUE, ORANGE, ORANGE], connect=False)
    baseline = np.mean([r['value'] for r in values(rows, 'capacity', 'w064', 'AbAg_accuracy')])
    ax.axhline(baseline, color=TEAL, lw=.8, ls=(0,(3,3)), zorder=1)
    ax.set_xticks(range(5), ['w64\n4/1', 'w96\n4/1', 'w128\n4/1', 'w64\n6/1', 'w64\n6/6'])
    ax.set_ylim(.66, .72)
    ax.text(.98, .95, '50% training pool', transform=ax.transAxes, ha='right', va='top', color=GREY, fontsize=8)
    for ax, metric, title, ylabel, ylim in [
        (axs[1, 1], 'edge_AP', 'E  Data scaling and contacts', 'Contact-edge AP ↑', (.042, .069)),
        (axs[1, 2], 'AbAg_accuracy', 'F  Data scaling and partners', 'Antibody/antigen swap accuracy ↑', (.665, .735))]:
        panel(ax, title, ylabel)
        for width, color, marker in [('w064', BLUE, 'o'), ('w128', ORANGE, 'D')]:
            yy = [values(rows, 'capacity', width, metric)[0]['value'],
                  values(rows, 'data', width, metric)[0]['value'],
                  values(rows, 'data', 'e40-'+width, metric)[0]['value']]
            ax.plot(range(3), yy, color=color, marker=marker, ms=5.5, lw=1.4,
                    markeredgecolor='white', markeredgewidth=.7, label=f'Width {int(width[1:])}')
        ax.set_xticks(range(3), ['50%\n20 epochs', '100%\n20 epochs', '100%\n40 epochs'])
        ax.set_xlabel('Training pool / epoch budget', labelpad=8)
        ax.set_xlim(-.25, 2.25); ax.set_ylim(ylim)
        ax.legend(loc='upper left', frameon=False, fontsize=8, handlelength=1.3, ncol=2, columnspacing=1)
    fig.text(.075, .035, 'PINDER development validation · A, E, F: seed 17 · B–D: seeds 17, 29, 43 (w96: seed 17 only)', color=GREY, fontsize=8.5)
    save(fig, SUPPORT, [r for r in rows if r['group'] != 'recipe'])
