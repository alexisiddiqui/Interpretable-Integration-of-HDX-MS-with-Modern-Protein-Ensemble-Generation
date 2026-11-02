"""Residue replacement preferences between independent matched design ensembles."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import csv
import opig027 as base
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D

AA = list('DEQNKRHSTAPGVMILFYW C'.replace(' ', ''))

def reconstruct():
    manifest_path = base.STAGE / 'replacement-records-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    groups = defaultdict(list)
    for entry in manifest['files']:
        raw = (base.STAGE / entry['local']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == entry['sha256']
        d = json.loads(raw)
        groups[d['backbone'], d['arm']].append(d)
    assert len(manifest['files']) == 376
    analysis = base.load('analysis.json')
    freq = analysis['readouts']['2_position_frequencies']['per_arm']
    output, checks = [], []
    matrices = {}
    for (backbone, arm), ds in sorted(groups.items()):
        if arm in ['vanilla', 'gibbs0']:
            continue
        ref = groups[backbone, ds[0]['reference_arm']]
        idx = ds[0]['surface_idx']
        assert len(ds) == len(ref) == 8
        assert {d['seed'] for d in ds} == set(range(8))
        assert all(d['surface_idx'] == idx for d in ds + ref)
        def frequencies(draws):
            return np.array([[sum(d['sequence'][i] == aa for d in draws)/len(draws)
                              for aa in AA] for i in idx])
        r, a = frequencies(ref), frequencies(ds)
        assert np.allclose(r.sum(axis=1), 1) and np.allclose(a.sum(axis=1), 1)
        # Cross-ensemble replacement mass, with every independent draw pair equally weighted.
        mass = 100 * r.T @ a / len(idx)
        net = mass - mass.T
        expected = next(x for x in freq[arm]['per_backbone'] if x['backbone'] == backbone)
        expected = expected['residues_written_on_the_surface']['frequency_delta_over_all_surface_positions']
        assert np.array_equal(np.round(net.sum(axis=0)/100, 6), [expected[aa] for aa in AA]), (backbone, arm)
        matrices[backbone, arm] = net
        checks.append({'backbone': backbone, 'arm': arm, 'n_surface': len(idx),
                       'max_composition_error': float(np.max(np.abs(net.sum(axis=0)-np.array([100*expected[aa] for aa in AA]))))})
        for i, source in enumerate(AA):
            for j, destination in enumerate(AA):
                output.append(dict(backbone=backbone, challenge=ds[0]['challenge'], arm=arm,
                    reference_arm=ds[0]['reference_arm'], source=source, destination=destination,
                    replacement_mass_pp=float(mass[i,j]), reverse_mass_pp=float(mass[j,i]),
                    net_replacement_pp=float(net[i,j])))
    # Reproduce the saved four-class counts to verify source selection and orientation.
    classes = ['DE', 'HKR', 'CNQSTY', 'AFGILMPVW']
    class_checks = 0
    for pair in analysis['readouts']['3_position_agreement']['pairs']:
        if pair['tier'] != 'matched':
            continue
        for arm, key in [(pair['arm'], 'substitution_matrix_arm'),
                         (pair['fine_tune_arm'], 'substitution_matrix_fine_tune')]:
            ds = groups[pair['backbone'], arm]
            ref = groups[pair['backbone'], ds[0]['reference_arm']]
            idx = ds[0]['surface_idx']
            def counts(draws):
                return np.array([[sum(d['sequence'][i] in c for d in draws)
                                  for c in classes] for i in idx])
            assert np.array_equal(counts(ref).T @ counts(ds), pair[key])
            class_checks += 1
    checks_path = base.STAGE / 'qa/replacement-checks.json'
    checks_path.write_text(json.dumps({'n_records':len(manifest['files']), 'n_arm_backbone_comparisons':len(checks),
        'n_residue_pairs':len(output), 'original_class_matrix_checks':class_checks, 'composition_checks':checks}, indent=2)+'\n')
    return output, manifest, analysis


def aggregate(rows):
    g = defaultdict(list)
    for r in rows:
        g[r['challenge']].append(r['net_replacement_pp'])
    return float(np.mean([np.mean(x) for x in g.values()]))


def build(out):
    base.style()
    out = Path(out)
    rows, manifest, analysis = reconstruct()
    table = defaultdict(list)
    for r in rows:
        table[r['arm'], r['source'], r['destination']].append(r)
    fig = plt.figure(figsize=(14.2, 12.3))
    grid = fig.add_gridspec(3, 6, height_ratios=[1, 1, .85], hspace=.48, wspace=.75)
    fig.subplots_adjust(left=.065, right=.91, top=.90, bottom=.10)
    fig.suptitle('Residue replacement preferences at matched surface charge changes',
                 x=.045, y=.985, ha='left', fontsize=16, weight='bold')
    fig.text(.045,.951,'Rows = control residue; columns = design residue. Colour shows the preferred direction after subtracting the reverse exchange.',fontsize=9)
    fig.text(.045,.929,'Fine-tunes are compared with vanilla ProteinMPNN; GQT and pKAI are compared with unsteered Gibbs sampling.',fontsize=9)
    heat_axes=[]
    means=[]
    norm = LogNorm(vmin=.05, vmax=8)
    cmap=plt.get_cmap('magma_r').copy(); cmap.set_bad('#f5f5f5')
    for direction_idx, direction in enumerate(['acid', 'alk']):
        arms=[direction, f'pka_gqt_{direction}', f'pka_pkai_{direction}']
        for method_idx, arm in enumerate(arms):
            ax=fig.add_subplot(grid[direction_idx,method_idx*2:method_idx*2+2]);heat_axes.append(ax)
            matrix=np.array([[aggregate(table[arm,s,d]) for d in AA] for s in AA])
            for i,s in enumerate(AA):
                for j,d in enumerate(AA):
                    means.append(dict(arm=arm,source=s,destination=d,net_replacement_pp=matrix[i,j]))
            im=ax.imshow(np.ma.masked_where(matrix < .05,matrix),cmap=cmap,norm=norm,aspect='equal',interpolation='nearest')
            ax.set_xticks(range(20),AA);ax.set_yticks(range(20),AA);ax.tick_params(length=0,labelsize=8)
            ax.set_xlabel('Design residue',fontsize=9);ax.set_ylabel('Control residue',fontsize=9)
            ax.set_xticks(np.arange(-.5,20,1),minor=True);ax.set_yticks(np.arange(-.5,20,1),minor=True)
            ax.grid(which='minor',color='white',linewidth=.3);ax.tick_params(which='minor',length=0)
            for i,j in zip(*np.where(matrix>=1.5)):
                ax.text(j,i,f'{matrix[i,j]:.1f}',ha='center',va='center',fontsize=5.2,color='white')
            label=['Fine-tune','GQT','pKAI'][method_idx]
            n=5 if arm=='pka_pkai_alk' else 6
            ax.set_title(f'{direction.capitalize()} direction  |  {label}  (n = {n})',loc='left',pad=10)
            ax.text(-.13,1.04,'ABCDEF'[direction_idx*3+method_idx],transform=ax.transAxes,weight='bold',fontsize=13)
        ax=fig.add_subplot(grid[2,direction_idx*3:direction_idx*3+3])
        selected=[('E','Q'),('D','N'),('P','A'),('P','E'),('A','K'),('A','E'),('G','M'),('S','M'),('P','M')]
        for x,(s,d) in enumerate(selected):
            for method_idx,arm in enumerate(arms):
                rr=table[arm,s,d];xx=x+(method_idx-1)*.23
                for k,r in enumerate(rr):
                    ax.scatter(xx+(k-(len(rr)-1)/2)*.016,r['net_replacement_pp'],
                        marker=base.CHALLENGES[r['challenge']],s=23,color=base.METHODS[method_idx],
                        alpha=.75,edgecolor='white',linewidth=.3,zorder=3)
                mean=aggregate(rr);ax.plot([xx-.08,xx+.08],[mean,mean],color='#20242C',lw=1.6,zorder=4)
        ax.axhline(0,color='#666666',lw=.8)
        ax.axvspan(-.5,1.5,color='#dce8f2',alpha=.35,zorder=0)
        ax.axvspan(5.5,8.5,color='#eee5d3',alpha=.35,zorder=0)
        ax.set_xticks(range(len(selected)),[f'{s}→{d}' for s,d in selected],rotation=45,ha='right')
        ax.set_xlim(-.6,8.6);ax.grid(axis='y',alpha=.15)
        ax.set_ylabel('Net replacement\n(per 100 surface positions)')
        ax.set_title(f'{direction.capitalize()} direction  |  Selected replacement preferences',loc='left',pad=11)
        ax.text(-.10,1.04,'GH'[direction_idx],transform=ax.transAxes,weight='bold',fontsize=13)
    cax=fig.add_axes([.935,.46,.012,.38]);cb=fig.colorbar(im,cax=cax)
    cb.set_ticks([.05,.1,.25,.5,1,2,4,8],labels=['0.05','0.1','0.25','0.5','1','2','4','8'])
    cb.set_label('Net replacement per 100 surface positions (log scale)',fontsize=9)
    fig.legend(handles=[Line2D([],[],marker='o',linestyle='',color=c,label=l) for c,l in zip(base.METHODS,['Fine-tune','GQT','pKAI'])],
               loc='lower left',bbox_to_anchor=(.045,.035),frameon=False,ncol=3)
    fig.text(.045,.025,'G-H: blue shading marks E/Q and D/N scaffold-preserving candidates; tan shading marks methionine enrichment routes.',fontsize=8.5)
    fig.text(.045,.009,'Points = backbones; symbols = challenges 1 (circle), 2 (square), 3 (triangle), 5 (diamond). Black bars = equal-challenge means.',fontsize=8.5)
    caption='''Residue replacement preferences distinguish extremophile fine-tuning from surface-charge steering. (A-F) Each matrix compares position-resolved residue frequencies in a design ensemble with its own unsteered control. For residues a and b, the plotted quantity is 100 times the surface-average of p_control(a) p_design(b) minus p_control(b) p_design(a). Rows identify the control residue and columns the design residue. Positive values indicate a preference for the row-to-column exchange over its reverse. Means first average backbones within each challenge and then weight the four challenges equally. Only positive means at least 0.05 per 100 surface positions are coloured, on a logarithmic scale shared by all six panels. Pale cells include reverse preferences, zero and positive values below this display threshold; the full signed matrices are supplied as CSV files. Numbers label means of at least 1.5. Acid comparisons and the alk fine-tune and GQT use six backbones each; pKAI alk uses five. Each arm and control contains eight independently sampled designs per backbone.

(G, H) Signed preferences for selected exchanges retain individual backbones and show challenge-weighted means as black bars. Blue shading identifies E/Q and D/N pairs, chosen to examine changes in terminal chemistry on similar side-chain scaffolds. Tan shading identifies the principal methionine enrichment routes in the fine-tunes. The remaining pairs resolve the prominent proline and alanine changes. These pairs were selected descriptively after examining the full matrices and are not independent hypothesis tests. Acid fine-tuning favours E-to-Q and P-to-A preferences, while acid steering favours A-to-K. Alk fine-tuning shows a large P-to-E preference. Fine-tune methionine enrichment arises mainly from positions occupied by S, G and P in the controls.

These quantities compare independent sequence ensembles at corresponding positions, rather than observed mutation trajectories. Subtracting reverse exchange removes symmetric sampling variation but does not make a replacement causal or establish structural isosterism. Column sums of each signed matrix reproduce the original residue-frequency changes to their reported precision. The matched quantity is the change in formal surface charge relative to each sampler's control. Replacement preferences alone do not establish adaptation, stability or activity at extreme pH.'''
    base.finish(fig,out,{'residue_replacements':rows,'mean_residue_replacements':means},['analysis.json'],caption)
    prov=json.loads((out/'provenance.json').read_text())
    prov['replacement_records']=manifest
    prov['replacement_plotting_code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (out/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
    overlap(analysis,out.parent/'jaxka-extremophile-overlap')


def overlap(data,out):
    pairs=[r for r in data['readouts']['3_position_agreement']['pairs'] if r['tier']=='matched']
    fig,axes=plt.subplots(1,2,figsize=(10,3.8));fig.subplots_adjust(wspace=.38,bottom=.22,top=.82)
    order=['pka_gqt_acid','pka_pkai_acid','pka_gqt_alk','pka_pkai_alk'];export=[]
    for x,arm in enumerate(order):
        rows=[r for r in pairs if r['arm']==arm]
        funcs=[lambda r:r['jaccard_surface']-r['jaccard_chance_surface'],lambda r:r['substitution_profile_correlation_off_diagonal']-r['substitution_profile_permutation_null']['mean']]
        for ax,func in zip(axes,funcs):
            for k,r in enumerate(rows):
                ax.scatter(x+(k-(len(rows)-1)/2)*.045,func(r),marker=base.CHALLENGES[r['challenge']],s=32,color=base.COLORS[arm],alpha=.8)
            mean=base.weighted(rows,func);ax.plot([x-.23,x+.23],[mean,mean],color='#222222',lw=1.8)
        for r in rows:export.append(dict(arm=arm,backbone=r['backbone'],challenge=r['challenge'],jaccard_excess=funcs[0](r),chemistry_excess=funcs[1](r)))
    for ax in axes:
        ax.axhline(0,color='#777777',ls='--',lw=.8);ax.grid(axis='y',alpha=.15)
        ax.set_xticks(range(4),['GQT\nacid','pKAI\nacid','GQT\nalk','pKAI\nalk'])
    axes[0].set_ylabel('Jaccard minus chance');axes[1].set_ylabel('Class-substitution correlation\nminus permutation mean')
    base.panel(axes[0],'A','Surface positions overlap above chance');base.panel(axes[1],'B','Chemical agreement depends on direction')
    fig.text(.06,.02,'Points = backbones; symbols = challenges 1 (circle), 2 (square), 3 (triangle), 5 (diamond). Black bars = equal-challenge means.',fontsize=8)
    base.finish(fig,out,{'overlap_and_chemistry':export},['analysis.json'],'''Position overlap and class-level chemistry provide separate comparisons. (A) Surface-position Jaccard above its set-size-matched chance expectation. (B) Off-diagonal class-substitution correlation above the mean of 2,000 position permutations per pair. Positive values in B describe class-level chemistry agreement beyond this null; location is measured separately in A. Points are matched backbones, with six in each comparison except pKAI alk, which has five. Black bars first average within challenge and then weight challenges equally. These panels were separated from the main chemistry figure to allow its residue-level replacement preferences to be shown in full.''')
    prov=json.loads((out/'provenance.json').read_text());prov['replacement_plotting_code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (out/'provenance.json').write_text(json.dumps(prov,indent=2)+'\n')

if __name__=='__main__':
    build(base.ROOT/'figures/jaxka-extremophile-chemistry')
