"""Retain the validated flow calculation, replacing only seed labels with the shared key.
Usage: python moprp_flow.py <original-flow-script> [original arguments...]
"""
import sys
from pathlib import Path
src=Path(sys.argv.pop(1));code=src.read_text();start=code.index('def draw_basins(');end=code.index('\n\n',code.index('path_effects=',start))
replacement='''def draw_basins(ax, plane, ph):
    from regions import decorate, IDS, COLORS
    if plane == "pca":
        decorate(ax, basins)
    else:
        for b, lab, colour in zip(basins, IDS, COLORS):
            tag=f"{b['ph'].replace(' ', '').lower()}_{b['id']}"
            seeds=[i for i,r in enumerate(runs) if r['basin']==tag and r['target_ph']==ph]
            cx=np.median([coords(i, plane)[0,0] for i in seeds]); cy=np.median([coords(i,plane)[0,1] for i in seeds])
            ax.scatter(cx,cy,s=60,facecolor='none',edgecolor=colour,lw=1.5,zorder=5)
            angle=np.radians(LABEL_ANGLE[plane][tag])
            ax.annotate(lab,(cx,cy),xytext=(14*np.cos(angle),14*np.sin(angle)),textcoords='offset points',fontsize=9,color=colour,fontweight='bold',path_effects=[pe.withStroke(linewidth=2.5,foreground=SURF)])
'''
code=code[:start]+replacement+code[end:]
code=code.replace('basin markers: dark green from pH 4 runs, mid green from pH 7 runs','seed-region identifiers are shared with basins, paths and MSM maps')
polish = """
from moprp_layout import region_key,clear_titles,enlarge_regions
fig.set_size_inches(8.9,10.4)
for text in list(fig.texts):text.remove()
for row in range(3):
    for col in range(2):
        ax=axes[row,col]
        clear_titles(ax)
        ax.set_title(('ABCDEF'[row*2+col])+'  '+['pH 4','pH 7','pH 7 − pH 4'][row],loc='left',fontsize=11)
        ax.set_xlabel('PC1' if col==0 else 'dRMSD to 2L39 (rad, log)',fontsize=10)
        ax.set_ylabel('PC2' if col==0 else 'β1 deviation (°, log)',fontsize=10)
        ax.tick_params(labelsize=9)
        enlarge_regions(ax)
        for other in fig.axes:
            if other is not ax and other.get_ylabel().startswith(('drift speed','|drift')):
                old=other.get_ylabel()
                unit='PC units ns⁻¹' if 'PC units' in old else 'log₁₀ units ns⁻¹'
                other.set_ylabel(('Δspeed' if '−' in old else 'Speed')+' ('+unit+')',fontsize=8)
                other.tick_params(labelsize=8)
fig.subplots_adjust(left=.09,right=.97,top=.96,bottom=.22,wspace=.30,hspace=.30)
fig.text(.09,.11,'PCA: speed contours and length-scaled arrows. Dihedrals: direction arrows.\\nBottom row: blue = faster at pH 4; red = faster at pH 7. Grey: unbiased MD.\\nLag 1 ns; ≥200 pairs from ≥3 runs per bin; 144 runs, 12.48 μs.',fontsize=9,linespacing=1.45)
region_key(fig,size=8.5)
assert len(runs)==144
assert abs(sum(TIME[i][-1] for i in range(len(runs)))-12480)<.1
"""
code=code.replace('fig.savefig(f"{prefix}.png", dpi=130)',polish+'\nfig.savefig(f"{prefix}.png", dpi=220)\nfig.savefig(f"{prefix}.pdf", dpi=220)')
exec(compile(code,str(src),'exec'))
