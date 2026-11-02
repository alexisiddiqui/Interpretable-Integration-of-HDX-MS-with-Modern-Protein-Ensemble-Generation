"""Build experiment 027 figures from the checksum-verified local snapshot.

Each figure directory has a make.py entrypoint. No remote computation is run.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/opig027-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import scipy
from scipy.stats import beta

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / ".experiments/opig-adaptyv-027"
INPUTS = STAGE / "inputs"
ARMS = ["vanilla", "acid", "alk", "gibbs0", "pka_gqt_acid", "pka_pkai_acid", "pka_gqt_alk", "pka_pkai_alk"]
LABELS = ["Vanilla", "Acid FT", "Alk FT", "Gibbs", "GQT acid", "pKAI acid", "GQT alk", "pKAI alk"]
COLORS = dict(zip(ARMS, ["#777777", "#D97732", "#B45170", "#363D49", "#3C9B91", "#6A9FD1", "#087E75", "#346BA3"]))
METHODS = ["#D97732", "#087E75", "#346BA3"]
AA = list("DEKRHQNSTAGPVMILFYW C".replace(" ", ""))
CHALLENGES = {1: "o", 2: "s", 3: "^", 5: "D"}


def load(name):
    manifest = json.loads((STAGE / "access-audit.json").read_text())
    record = next(f for f in manifest["files"] if Path(f["source"]).name == name)
    raw = (INPUTS / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == record["sha256"], name
    return json.loads(raw)


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
        "axes.titlesize": 10, "axes.labelsize": 9, "xtick.labelsize": 8,
        "ytick.labelsize": 8, "axes.spines.top": False, "axes.spines.right": False,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "axes.linewidth": .7, "savefig.facecolor": "white"})


def panel(ax, letter, title):
    ax.set_title(title, loc="left", pad=13)
    ax.text(-.10, 1.055, letter, transform=ax.transAxes, fontsize=13, fontweight="bold", va="bottom")


def weighted(rows, key):
    groups = defaultdict(list)
    for r in rows:
        groups[r["challenge"]].append(key(r))
    return float(np.mean([np.mean(v) for v in groups.values()]))


def points(ax, x, values, color, center="mean", marker="o"):
    values = np.asarray(values, dtype=float)
    if not len(values):
        return
    jitter = np.linspace(-.17, .17, len(values)) if len(values) > 1 else [0]
    ax.scatter(x + np.asarray(jitter), values, s=24, c=color, alpha=.8,
               edgecolor="white", linewidth=.4, marker=marker, zorder=3)
    mid = np.mean(values) if center == "mean" else np.median(values)
    ax.plot([x-.23, x+.23], [mid, mid], color="#20242C", lw=1.7, zorder=4)


def finish(fig, out, tables, names, caption):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for fmt in ["pdf", "svg", "png"]:
        fig.savefig(out / f"fig.{fmt}", dpi=220, bbox_inches="tight", pad_inches=.14)
    for name, rows in tables.items():
        with (out / f"{name}.csv").open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    audit = json.loads((STAGE / "access-audit.json").read_text())
    manifest = {"source_repository": audit["source_repository"], "source_commit": audit["source_commit"],
        "inputs": [f for f in audit["files"] if Path(f["source"]).name in names],
        "dependencies": {"matplotlib": matplotlib.__version__, "numpy": np.__version__, "scipy": scipy.__version__},
        "plotting_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "build_command": f"python figures/{out.name}/make.py",
        "output_sha256": {f"fig.{fmt}": hashlib.sha256((out / f"fig.{fmt}").read_bytes()).hexdigest() for fmt in ["pdf", "svg", "png"]}}
    (out / "provenance.json").write_text(json.dumps(manifest, indent=2)+"\n")
    (out / "caption.md").write_text(caption.strip()+"\n")
    plt.close(fig)
    print(out.relative_to(ROOT))


def chemistry(out):
    style()
    data = load("analysis.json")
    freq = data["readouts"]["2_position_frequencies"]["per_arm"]
    records = []
    by_arm = {}
    for direction in ["acid", "alk"]:
        for arm in [direction, f"pka_gqt_{direction}", f"pka_pkai_{direction}"]:
            rows = [r for r in freq[arm]["per_backbone"] if r["backbone_tier"] == "matched" and r["tier"] in ["matched", "reference_arm"]]
            assert len(rows) == (5 if arm == "pka_pkai_alk" else 6)
            by_arm[arm] = rows
            for r in rows:
                for aa, v in r["residues_written_on_the_surface"]["frequency_delta_over_all_surface_positions"].items():
                    records.append({"arm": arm, "backbone": r["backbone"], "challenge": r["challenge"], "residue": aa, "delta_percentage_points": v*100})
    delta = lambda r, aa: r["residues_written_on_the_surface"]["frequency_delta_over_all_surface_positions"][aa]*100
    fig = plt.figure(figsize=(12.4, 9.8))
    gs = fig.add_gridspec(3, 2, height_ratios=[.85, 1.3, 1.15], hspace=.72, wspace=.36)
    fig.suptitle("Different surface chemistry at matched charge changes", x=.05, ha="left", fontsize=15, fontweight="bold", y=.99)
    heat_axes = []
    for j, direction in enumerate(["acid", "alk"]):
        arms = [direction, f"pka_gqt_{direction}", f"pka_pkai_{direction}"]
        ax = fig.add_subplot(gs[0, j]); heat_axes.append(ax)
        matrix = np.array([[weighted(by_arm[a], lambda r, aa=aa: delta(r, aa)) for aa in AA] for a in arms])
        im = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-20, vmax=20)
        ax.set_xticks(range(20), AA); ax.set_yticks(range(3), ["Fine-tune (6)", "GQT (6)", "pKAI (5)" if direction == "alk" else "pKAI (6)"])
        ax.tick_params(length=0)
        ax.set_xlabel("Surface residue")
        panel(ax, "AB"[j], f"{direction.capitalize()} direction")
        for row, col in zip(*np.where(np.abs(matrix) >= 4.0)):
            ax.text(col, row, f"{matrix[row,col]:+.0f}", ha="center", va="center", fontsize=7,
                    color="white" if abs(matrix[row,col]) > 11 else "#242424")
        ax = fig.add_subplot(gs[1, j])
        selected = list("EKQA") if direction == "acid" else list("EDKPS")
        for x, aa in enumerate(selected):
            for k, a in enumerate(arms):
                xx = x + (k-1)*.24
                rows = by_arm[a]
                for q, r in enumerate(rows):
                    ax.scatter(xx+(q-(len(rows)-1)/2)*.018, delta(r, aa), s=27,
                               marker=CHALLENGES[r["challenge"]], color=METHODS[k], alpha=.7, edgecolor="white", lw=.3)
                avg = weighted(rows, lambda r: delta(r, aa))
                ax.plot([xx-.075, xx+.075], [avg, avg], color="#222222", lw=1.8)
        ax.axhline(0, color="#888888", lw=.7); ax.set_xticks(range(len(selected)), selected)
        ax.set_ylabel("Surface frequency change (pp)"); ax.set_ylim(-24, 35)
        ax.grid(axis="y", alpha=.15)
        panel(ax, "CD"[j], "Acid depletion versus basic enrichment" if j == 0 else "Different routes to acidic enrichment")
        if j == 0:
            ax.legend(handles=[Line2D([], [], marker="o", color=c, linestyle="", label=l) for c,l in zip(METHODS,["Fine-tune", "GQT", "pKAI"])], frameon=False, fontsize=8, ncol=3, loc="upper left")
    cb = fig.colorbar(im, ax=heat_axes, fraction=.03, pad=.025)
    cb.set_label("Frequency change (pp)")
    pairs = [r for r in data["readouts"]["3_position_agreement"]["pairs"] if r["tier"] == "matched"]
    order = ["pka_gqt_acid", "pka_pkai_acid", "pka_gqt_alk", "pka_pkai_alk"]
    pair_table = []
    ax1 = fig.add_subplot(gs[2, 0]); ax2 = fig.add_subplot(gs[2, 1])
    for x, arm in enumerate(order):
        rows = [r for r in pairs if r["arm"] == arm]
        for k, r in enumerate(rows):
            v = r["jaccard_surface"] - r["jaccard_chance_surface"]
            v2 = r["substitution_profile_correlation_off_diagonal"] - r["substitution_profile_permutation_null"]["mean"]
            xx = x + (k-(len(rows)-1)/2)*.045
            for ax, value in [(ax1,v),(ax2,v2)]:
                ax.scatter(xx, value, marker=CHALLENGES[r["challenge"]], s=35, color=COLORS[arm], alpha=.8)
            pair_table.append({"arm":arm,"backbone":r["backbone"],"challenge":r["challenge"],"jaccard":r["jaccard_surface"],"chance_jaccard":r["jaccard_chance_surface"],"jaccard_excess":v,"chemistry_excess_over_permutation_mean":v2,"permutation_upper_tail_p":r["substitution_profile_permutation_null"]["p_value"]})
        for ax, calc in [(ax1, lambda r:r["jaccard_surface"]-r["jaccard_chance_surface"]), (ax2, lambda r:r["substitution_profile_correlation_off_diagonal"]-r["substitution_profile_permutation_null"]["mean"])]:
            avg = weighted(rows,calc);ax.plot([x-.23,x+.23],[avg,avg],color="#222222",lw=1.8)
    for ax in [ax1,ax2]:
        ax.axhline(0, color="#777777", lw=.8, ls="--");ax.grid(axis="y",alpha=.15)
        ax.set_xticks(range(4),["GQT\nacid","pKAI\nacid","GQT\nalk","pKAI\nalk"])
    ax1.set_ylabel("Jaccard minus chance"); ax2.set_ylabel("Class-substitution correlation\nminus permutation mean")
    panel(ax1,"E","Surface positions overlap above chance");panel(ax2,"F","Chemical agreement depends on direction")
    fig.text(.05,.005,"Points are backbones; symbols identify challenges 1 (circle), 2 (square), 3 (triangle) and 5 (diamond). Black bars are challenge-weighted means.",fontsize=8)
    finish(fig,out,{"surface_deltas":records,"overlap_and_chemistry":pair_table},["analysis.json"],"""
Matched charge changes arise through different surface chemistry. (A, B) Changes in amino-acid frequency at surface positions, in percentage points relative to each arm's own unsteered reference. Fine-tunes use vanilla autoregressive ProteinMPNN; GQT and pKAI steering use unsteered Gibbs sampling. Means weight each challenge equally. The acidophile comparison uses six matched backbones per arm; pKAI alk uses five and the other alk arms use six. (C, D) Diagnostic residue changes for individual backbones, with challenge-weighted means shown as black bars. Symbols identify challenges 1, 2, 3 and 5. (E) Surface mutation-position Jaccard above its set-size-matched chance expectation. (F) Off-diagonal class-substitution correlation above the mean of 2,000 position permutations per pair. Positive values in F describe chemistry agreement beyond this null; location is measured separately in E. The signed change in formal surface charge was matched by fitting steering strength and is therefore not an independent result. Composition alone does not establish stability or adaptation at extreme pH.
""")


def complex_confidence(out):
    style(); name="fold-check-complexcheck-target-2026-10-28.json"; rows=load(name)["rows"]
    grouped=defaultdict(list)
    for r in rows:
        assert r["backbone"].endswith("+target")
        grouped[(r["backbone"],r["arm"],r["key"])].append(r)
    table=[]
    for (bb,arm,key),rs in sorted(grouped.items()):
        assert len(rs)==8
        table.append({"backbone":bb,"arm":arm,"key":key,"n_refolds":8,
            **{f:float(np.mean([r[f] for r in rs])) for f in ["binder_iptm","reproduced","binder_sctm_in_complex","plddt"]}})
    fig,axs=plt.subplots(2,3,figsize=(13.6,8.2),gridspec_kw={"hspace":.65,"wspace":.26})
    fig.subplots_adjust(top=.86,bottom=.12)
    fig.suptitle("Complex confidence after design with target context",x=.05,ha="left",fontsize=15,fontweight="bold",y=.98)
    fig.text(.05,.928,"Each point is one design, averaged over four ESMFold2 critics and two fold seeds. Native references use the same eight refolds.",fontsize=9)
    for i,prefix in enumerate(["ch2-","ch5-"]):
        for j,(field,title,ylim) in enumerate([("binder_iptm","Binder interface confidence",(0,1.03)),("reproduced","Binding-pose recovery",(-.04,1.13)),("binder_sctm_in_complex","Binder fold retention",(.74,1.015))]):
            ax=axs[i,j]
            for x,arm in enumerate(ARMS+["native"]):
                rs=[r for r in table if r["backbone"].startswith(prefix) and r["arm"]==arm]
                points(ax,x,[r[field] for r in rs],COLORS.get(arm,"#111111"),marker="D" if arm=="native" else "o")
                if field=="reproduced":
                    total=len(rs)*8; passed=round(sum(r[field]*8 for r in rs))
                    ax.text(x,1.065,f"{passed}/{total}",ha="center",va="center",fontsize=6.7)
            ax.set_xticks(range(9),LABELS+["Native"],rotation=50,ha="right")
            ax.set_ylim(*ylim);ax.set_xlim(-.5,8.5);ax.grid(axis="y",alpha=.15)
            if field=="binder_iptm":ax.axhline(.5,color="#888888",lw=.7,ls="--")
            if field=="reproduced":ax.set_yticks([0,.25,.5,.75,1],["0","2/8","4/8","6/8","8/8"])
            if j==0:ax.set_ylabel(("TNF" if i==0 else "TCR/pMHC")+"\nBinder ipTM",fontweight="normal")
            if j==1:ax.set_ylabel("Passing refolds per design")
            if j==2:ax.set_ylabel("Binder scTM in complex")
            panel(ax,"ABCDEF"[i*3+j],title if i==0 else title+" (TCR)")
    fig.text(.05,.015,"Pose criterion: target-aligned binder C-alpha RMSD <= 5 A and binder ipTM >= 0.5. Black bars are means across designs.",fontsize=8)
    finish(fig,out,{"design_level_metrics":table},[name],"""
Complex confidence after sequence design with the target present. TNF (A-C) and TCR/pMHC (D-F) are shown separately. Each point represents one of eight designs per arm, averaged over four ESMFold2 critics and two fold seeds; native sequences each contribute one point. Black bars show means across designs. (A, D) Binder ipTM; the dashed line marks the 0.5 confidence component of the pose criterion. (B, E) Fraction of eight refolds passing both binder ipTM >= 0.5 and target-aligned binder C-alpha RMSD <= 5 angstrom. Counts above each group give passing/total refolds and are not independent-design sample sizes. (C, F) Binder scTM within the predicted complex. AlkSecMPNN preserves the TNF binder fold while losing interface confidence and the source pose. Both fine-tunes reduce TCR binder scTM, although pose recovery is poor across TCR designs. The fine-tunes also alter more residues and more buried positions, so these comparisons do not isolate checkpoint identity from mutation load.
""")


def linkage(out):
    style()
    names=["selectivity-sweep-select-2026-10-29.json","selectivity-sweep-select-yield-2026-10-29.json","fold-check-selectcheck-2026-10-29.json","fold-check-selectcheck-yield-2026-10-30.json","binding-ph-bindingph-select-2026-10-29.json","binding-ph-bindingph-yield-2026-10-30.json"]
    sweep,yield_summary,folds,yield_folds,binding,yield_binding=[load(n) for n in names]
    summaries={r["lam"]:r for r in sweep["rows"] if r["arm"]=="pka_gqt_select"}
    summaries.update({r["lam"]:r for r in yield_summary["rows"]})
    fs=[r for r in folds["rows"] if r["arm"]!="native" and r.get("lam")!=.2]+yield_folds["rows"]
    grouped=defaultdict(list)
    for r in fs:grouped[r["lam"]].append(r)
    stats=[]
    for lam,rs in sorted(grouped.items()):
        assert len({r['key'] for r in rs})==len(rs)
        n=len(rs);k=int(sum(r["reproduced"] for r in rs))
        lo=0 if k==0 else float(beta.ppf(.025,k,n-k+1))
        hi=1 if k==n else float(beta.ppf(.975,k+1,n-k))
        stats.append({"lambda":lam,"n_designs":n,"n_pose_passing":k,"fraction":k/n,"ci95_low":lo,"ci95_high":hi,"median_J_binder_sites":summaries.get(lam,{}).get("median_J_binder_sites"),"median_his":summaries.get(lam,{}).get("median_his",1)})
    assert [(r['n_designs'],r['n_pose_passing']) for r in stats if r['lambda'] in [.15,.2]]==[(24,12),(24,4)]
    fig=plt.figure(figsize=(13.5,10.4));fig.subplots_adjust(top=.89,bottom=.16,left=.07,right=.98)
    gs=fig.add_gridspec(2,1,height_ratios=[1,1.15],hspace=.47)
    top=gs[0].subgridspec(2,2,height_ratios=[2.3,1],hspace=.12,wspace=.3)
    axj=fig.add_subplot(top[0,0]);axh=fig.add_subplot(top[1,0],sharex=axj);axy=fig.add_subplot(top[:,1])
    fig.suptitle("Complex-aware steering increases predicted pH selectivity",x=.05,ha="left",fontsize=15,fontweight="bold",y=.98)
    fig.text(.05,.937,"TNF designs with target context; linkage and structural yield are evaluated separately.",fontsize=9)
    lams=sorted(summaries)
    axj.plot(lams,[summaries[x]['median_J_binder_sites'] for x in lams],'-o',color='#74549A',lw=1.5,ms=5)
    axj.axhline(sweep['native_J_binder_sites'],color='#777777',ls='--',lw=.8,label='Native GQT score')
    axj.legend(frameon=False,fontsize=8,loc='upper left');axj.set_ylabel('Median GQT linkage score');axj.tick_params(labelbottom=False)
    axh.plot(lams,[summaries[x]['median_his'] for x in lams],'-o',color='#74549A',lw=1.1,ms=4)
    axh.set_ylabel('Median His');axh.set_xlabel('Steering strength, lambda')
    for r in stats:
        x=r['lambda'];c='#087E75' if x==.15 else '#346BA3' if x==.2 else '#74549A'
        axy.errorbar(x,r['fraction'],yerr=[[r['fraction']-r['ci95_low']],[r['ci95_high']-r['fraction']]],fmt='o',color=c,capsize=3,ms=6,lw=1)
        axy.annotate(f"{r['n_pose_passing']}/{r['n_designs']}",(x,r['ci95_high']),xytext=(0,8),textcoords='offset points',ha='center',fontsize=8)
    axy.set_ylabel('Fraction of designs retaining pose');axy.set_ylim(-.04,1.17);axy.set_xlabel('Steering strength, lambda')
    for ax in [axj,axh,axy]:
        ax.set_xscale('symlog',linthresh=.03,linscale=.65)
        ax.set_xlim(-.005,.95);ax.set_xticks([0,.025,.05,.1,.15,.2,.4,.8],['0','.025','.05','.1','.15','.2','.4','.8'])
        ax.grid(axis='y',alpha=.15);ax.axvspan(.135,.165,color='#087E75',alpha=.08);ax.axvspan(.18,.22,color='#346BA3',alpha=.06)
    panel(axj,'A','The objective responds to stronger steering');panel(axy,'B','Pose retention declines beyond the intermediate region')
    bottom=gs[1].subgridspec(1,3,wspace=.18)
    configs=[('visible',a,None,l) for a,l in zip(ARMS,LABELS)]+[('select_yield','pka_gqt_select',.15,'Linkage .15'),('select_yield','pka_gqt_select',.2,'Linkage .20')]
    all_binding=binding['rows']+yield_binding['rows']
    table=[]
    for j,predictor in enumerate(['propka','pkai','pkai_plus']):
        ax=fig.add_subplot(bottom[0,j]); native=next(r for r in yield_binding['rows'] if r['condition']=='source')['profile'][predictor]['6.0']['binder']
        ax.axhline(0,color='#AAAAAA',lw=.7);ax.axhline(native,color='#444444',ls='--',lw=.9)
        tick_labels=[]
        for x,(cond,arm,lam,label) in enumerate(configs):
            rs=[r for r in all_binding if r['condition']==cond and r['arm']==arm and (lam is None or r.get('lam')==lam)]
            by_design=defaultdict(list)
            for r in rs:by_design[r['key']].append(r['profile'][predictor]['6.0']['binder'])
            vals=[]
            for key,v in sorted(by_design.items()):
                mean=float(np.mean(v));vals.append(mean)
                table.append({'predictor':predictor,'condition':cond,'arm':arm,'lambda':lam,'key':key,'n_passing_refolds':len(v),'binder_log10_KD_ratio_pH6':mean})
            color=COLORS.get(arm,'#087E75' if lam==.15 else '#346BA3')
            points(ax,x,vals,color,center='median')
            denominator=24 if cond=='select_yield' else 8
            tick_labels.append(f'{label}\n{len(vals)}/{denominator}')
            if not vals:ax.text(x,.05,'NA',transform=ax.get_xaxis_transform(),ha='center',fontsize=7,color='#777777')
        ax.set_xticks(range(len(configs)),tick_labels,rotation=65,ha='right')
        ax.set_xlim(-.65,len(configs)-.35);ax.set_ylim(-.95,2.5);ax.grid(axis='y',alpha=.15)
        if j==0:ax.set_ylabel('Binder-site contribution to log10 KD(6.0)/KD(7.4)')
        else:ax.tick_params(labelleft=False)
        panel(ax,'CDE'[j],['PROPKA','pKAI','pKAI+'][j])
    fig.text(.05,.045,'C-E: points are designs with a retained pose; black bars are medians; dashed lines mark the source complex. Labels give scored/total designs.',fontsize=8)
    fig.text(.05,.02,'Surface arms use eight refolds per design; linkage arms use one. Predictions are binder-site linkage contributions, not measured affinities.',fontsize=8)
    finish(fig,out,{'steering_response':stats,'binding_per_design':table},names,"""
Complex-aware linkage steering produces predicted pH selectivity within a limited pose-retention window. All designs use the TNF target as context. (A) Median GQT binder-site linkage objective and histidine count across steering strengths. The native GQT linkage score is dashed. (B) Fraction of designs retaining the pose, with exact 95% binomial intervals and passing/total design counts. Each linkage design has one ESMFold2 critic and fold seed. The 24-design yield runs replace the eight-design sweep population at strength 0.20, avoiding eight repeated sequences; strength 0.15 also has 24 designs. (C-E) Binder-site contributions to predicted log10 KD(6.0)/KD(7.4), calculated after minimisation with PROPKA, pKAI and pKAI+. Positive values indicate a contribution towards weaker binding at pH 6. Each point is a design, averaged over its passing refolds; black bars are medians. Dashed lines show the source complex rescored in the yield run. Labels show the number of scored designs over the number generated, and NA marks the absence of a passing pose. Surface-charge arms use the target-context comparison's eight refolds per design, whereas linkage arms use one; their yields are therefore protocol-specific. Scores are shown only for retained poses. The checking predictors corroborate a computational proof of concept on one backbone, not an experimental affinity measurement. Larger GQT objective values alone do not validate selectivity.
""")


def monomer(out):
    style();name='fold-check-foldcheck-2026-10-28.json';rows=load(name)['rows'];analysis=load('analysis.json')
    matched={r['backbone'] for r in analysis['readouts']['3_position_agreement']['pairs'] if r['tier']=='matched'}
    rows=[r for r in rows if r['backbone'] in matched and r.get('tier')!='weakly_determined']
    table=[]
    for bb in sorted(matched):
        for arm in ARMS+['native']:
            rs=[r for r in rows if r['backbone']==bb and r['arm']==arm]
            if not rs:continue
            challenge=int(bb[2]);table.append({'backbone':bb,'challenge':challenge,'arm':arm,'n_designs':len(rs),'sctm':float(np.mean([r['sctm'] for r in rs])),'plddt':float(np.mean([r['plddt'] for r in rs]))})
    fig,axs=plt.subplots(1,2,figsize=(12,4.9));fig.subplots_adjust(top=.78,bottom=.23,wspace=.25)
    fig.suptitle('Monomer refolding supports compatibility with the design backbone',x=.05,ha='left',fontsize=14,fontweight='bold',y=.98)
    fig.text(.05,.89,'Matched backbones only; each point averages designs within one backbone. This comparison does not test binding.',fontsize=9)
    for j,field in enumerate(['sctm','plddt']):
        ax=axs[j]
        for x,arm in enumerate(ARMS+['native']):
            rs=[r for r in table if r['arm']==arm]
            for k,r in enumerate(rs):ax.scatter(x+(k-(len(rs)-1)/2)*.045,r[field],s=30,marker=CHALLENGES[r['challenge']],color=COLORS.get(arm,'#111111'),alpha=.8)
            mid=weighted(rs,lambda r:r[field]);ax.plot([x-.23,x+.23],[mid,mid],color='#222222',lw=1.8)
        ax.set_xticks(range(9),LABELS+['Native'],rotation=45,ha='right');ax.grid(axis='y',alpha=.15)
        ax.set_ylabel('Monomer scTM' if j==0 else 'Monomer pLDDT')
        ax.set_ylim(.74,1.005) if j==0 else ax.set_ylim(.60,.96)
        panel(ax,'AB'[j],'Fold retention' if j==0 else 'Predicted structural confidence')
    fig.text(.05,.025,'Black bars are challenge-weighted means. Symbols identify challenges 1 (circle), 2 (square), 3 (triangle) and 5 (diamond).',fontsize=8)
    finish(fig,out,{'backbone_level_metrics':table},[name,'analysis.json'],"""
Monomer refolding supports compatibility with the design backbone. (A) Self-consistency TM-score of binder-only ESMFold2 refolds against the design backbone. (B) Mean monomer pLDDT. Points average designs within each of six matched backbones, with five backbones for pKAI alk; symbols identify challenges 1, 2, 3 and 5. Native sequences provide one reference refold per backbone. Black bars weight each challenge equally. These measurements use one ESMFold2 critic and one fold seed per sequence. The fine-tunes alter more positions and more buried residues, so their confidence penalty is confounded by mutation load. Monomer self-consistency does not establish stability, expression or binding-pose retention.
""")


BUILDERS={'chemistry':chemistry,'complex':complex_confidence,'linkage':linkage,'monomer':monomer}


def build(kind,out):
    BUILDERS[kind](Path(out))
