"""Compose TeaA evidence from archived per-structure scores; no refitting or new PCA.
Usage: python teaa_main.py <figure-folder> <output-folder> [log-folder]
All state bars use blind theta thresholds (-5,+5 degrees), not RMSD state assignments.
"""
from pathlib import Path
import csv,json,re,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
src,out=map(Path,sys.argv[1:3]);out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((src/'per_structure.csv').open()))
D={}
for e in sorted({r['ensemble'] for r in rows}):
 rr=[r for r in rows if r['ensemble']==e]
 D[e]={k:np.array([float(r[k]) if r[k] else np.nan for r in rr]) for k in rr[0] if k not in ('path','ensemble')}
 D[e]['path']=[r['path'] for r in rr]
def vals(e,k,weighted=False):
 d=D[e];v=d[k];w=d['weight_l1000'].copy() if weighted else np.ones(len(v));w/=w.sum();return v,w
def md(k):
 a,wa=vals('md_open',k);b,wb=vals('md_closed',k);return np.r_[a,b],np.r_[wa*.4,wb*.6]
def kde(v,w,g,s=1.5):return (np.exp(-.5*((g[:,None]-v)/s)**2)@w)/(s*np.sqrt(2*np.pi))
C={'unguided':'#858585','metad_union':'#d69f21','refined_a025':'#00796b','control':'#9452a1'}
plt.rcParams.update({'font.size':9,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
fig=plt.figure(figsize=(12.4,10.1));gs=fig.add_gridspec(3,3,hspace=.53,wspace=.37)
ax=fig.add_subplot(gs[0,0]);bx=fig.add_subplot(gs[0,1]);cx=fig.add_subplot(gs[0,2])
dx=fig.add_subplot(gs[1,0]);ex=fig.add_subplot(gs[1,1:]);fx=fig.add_subplot(gs[2,:2]);gx=fig.add_subplot(gs[2,2])
for axis,k,title,curves in [(ax,'theta','A  Hinge coverage, uniform weights',[('unguided',False,'Unguided (150)'),('metad_union',False,'Bias union (550)'),('refined_a025',False,'Refined (236)')]),(bx,'theta','B  Refinement and fitted weights',[('metad_union',True,'Union + MaxEnt'),('refined_a025',True,'Refined + MaxEnt'),('control',True,'Control + MaxEnt')]),(dx,'PC1','D  Geometry beyond the hinge',[('unguided',False,'Unguided'),('metad_union',False,'Union, uniform'),('refined_a025',True,'Refined + MaxEnt')])]:
 grid=np.linspace(-55,40,500) if k=='theta' else np.linspace(-85,85,600)
 axis.plot(grid,kde(*md(k),grid),color='#222222',lw=1.8,ls='--',label='MD target, 40:60')
 for e,w,l in curves:axis.plot(grid,kde(*vals(e,k,w),grid),color=C[e],lw=1.6,label=l)
 if k=='theta':
  for x,c in [(-18.4,'#d95f02'),(9.7,'#1f78b4')]:axis.axvline(x,color=c,lw=.8,ls=':')
 axis.set(title=title,xlabel='Hinge angle θ (°)' if k=='theta' else 'MD-fitted PC1 (Å)',ylabel='Probability density')
 axis.legend(fontsize=7,frameon=False,loc='upper left');axis.set_xlim(grid[0],grid[-1])
# state bars from exact archived weights
states=[];labels=['Target','Union','Refined','Control'];states.append([.4,0,.6]);audit={}
for e in ['metad_union','refined_a025','control']:
 v,w=vals(e,'theta',True);p=np.array([w[v < -5].sum(),w[(v>=-5)&(v<=5)].sum(),w[v>5].sum()]);states.append(p.tolist())
 audit[e]={'state_weights':p.tolist(),'ESS':float(1/(w@w)),'MD95_weight':[float(w@D[e]['in_md_open_95']),float(w@D[e]['in_md_closed_95'])]}
p=np.array(states);assert np.allclose(p.sum(1),1);assert np.allclose(p[2],[.419,.155,.426],atol=.0006);assert np.allclose(p[3],[.357,.408,.235],atol=.0006);left=np.zeros(4)
for j,(lab,col) in enumerate([('Open','#d95f02'),('Intermediate','#c8c8c8'),('Closed','#1f78b4')]):
 cx.barh(np.arange(4),p[:,j],left=left,color=col,label=lab,height=.62)
 for i in range(4):
  if p[i,j]>.08:cx.text(left[i]+p[i,j]/2,i,f'{p[i,j]:.3f}',ha='center',va='center',fontsize=8,color='white' if j!=1 else '#222222')
 left+=p[:,j]
cx.set(yticks=np.arange(4),yticklabels=labels,xlim=(0,1),xlabel='State weight',title='C  Population recovery (λ = 1000)');cx.invert_yaxis();cx.legend(fontsize=7,frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.4,-.22));cx.text(0,-.38,'Open θ < −5°; closed θ > +5°',transform=cx.transAxes,fontsize=7)
# Reconstruct the original density grid and HPD regions, using the same source parameters.
allpc=np.concatenate([np.c_[d['PC1'],d['PC2']] for d in D.values()]);lo=allpc.min(0);hi=allpc.max(0);pad=.08*(hi-lo);lo-=pad;hi+=pad
xe=np.linspace(lo[0],hi[0],241);ye=np.linspace(lo[1],hi[1],241);area=(xe[1]-xe[0])*(ye[1]-ye[0]);sig=(1.5/(xe[1]-xe[0]),1.5/(ye[1]-ye[0]))
def dens(e,weighted=False):
 x,w=vals(e,'PC1',weighted);y=D[e]['PC2'];h=np.histogram2d(x,y,bins=(xe,ye),weights=w)[0];h=gaussian_filter(h,sig,mode="constant");return h/(h.sum()*area)
def hpd(h):
 s=np.sort(h.ravel())[::-1];return s[np.searchsorted(np.cumsum(s)*area,.95)]
h=dens('refined_a025',True)
im=ex.pcolormesh(xe,ye,np.ma.masked_where(h.T<=0,np.log10(np.maximum(h.T,1e-20))),vmin=-5,vmax=-1.5,cmap='viridis',rasterized=True)
for e,c,l in [('md_open','#d95f02','MD open 95% region'),('md_closed','#1f78b4','MD closed 95% region')]:
 h0=dens(e);ex.contour((xe[:-1]+xe[1:])/2,(ye[:-1]+ye[1:])/2,h0.T,levels=[hpd(h0)],colors=[c],linestyles='--',linewidths=1.5);ex.plot([],[],color=c,ls='--',label=l)
ex.set(xlabel='MD-fitted PC1 (Å)',ylabel='MD-fitted PC2 (Å)',title='E  Refined + MaxEnt outside the MD regions');ex.legend(fontsize=8,frameon=True,facecolor='white',framealpha=.9,loc='upper right');fig.colorbar(im,ax=ex,label='log₁₀ probability density (Å⁻²)',pad=.02)
ex.text(.02,.03,'Weight inside open / closed MD regions: 9.8% / 7.7%\nMD target: 40.0% / 59.5%',transform=ex.transAxes,fontsize=8,bbox=dict(fc='white',ec='none',alpha=.9))
# Exact archived scoring log, required (never approximate the curve from prose values).
logs=Path(sys.argv[3]) if len(sys.argv)>3 else src/'source'
def log_text(name):
 p=logs/name
 if not p.exists():p=p.with_suffix('.txt')
 return p.read_text()
txt=log_text('F_bins_8050284.out');line=next(l for l in txt.splitlines() if l.strip().startswith('grid:'));pts=[(float(a),float(b)) for a,b in re.findall(r'([0-9.]+):([0-9.]+)',line)]
best=re.search(r'simplex fit: f in_open ([0-9.]+), in_closed [0-9.]+, MSE ([0-9.]+)',txt);fbest,mbest=map(float,best.groups())
fx.plot(*np.array(pts).T,'o-',color='#225f92',ms=3,label='20 open + 20 closed Boltz in-state structures')
for e,job in [('refined_a025','F_blind_8050281.out'),('metad_union','F_metad_8049979.out'),('control','F_ctl_8050283.out')]:
 floor=float(re.search(r'lambda 1000: floor ([0-9.]+)',log_text(job)).group(1));audit[e]['floor']=floor;fx.axhline(floor,color=C[e],ls={'refined_a025':'--','metad_union':'-.','control':':'}[e],label=f"{'Refined' if e=='refined_a025' else 'Union' if e=='metad_union' else 'Control'} floor {floor:.4f}")
fx.axvline(.4,color='#777777',ls=':',lw=1);fx.scatter([.4,fbest],[dict(pts)[.4],mbest],color='#222222',zorder=5)
fx.annotate(f'Target 0.40: {dict(pts)[.4]:.5f}\nMinimum {fbest:.3f}: {mbest:.5f}',(.45,mbest),xytext=(.12,.0076),arrowprops={'arrowstyle':'-','lw':.7},fontsize=8)
fx.set(xlim=(0,1),ylim=(0,.0125),xlabel='Open fraction within the in-state mixture',ylabel='Uptake MSE against target',title='F  Uptake weakly distinguishes reference-like mixtures');fx.legend(fontsize=7,frameon=False,loc='upper center',bbox_to_anchor=(.5,-.24),ncol=2)
gx.axis('off');gx.set_title('G  Closed-state geometry',loc='left');inset=src/'closed_overlay.png'
if inset.exists():gx.imshow(plt.imread(inset));gx.text(0,-.05,'Blue: MD closed reference\nGreen: weighted medoid of refined closed states\nFitted on Fiedler lobe I; lobe II remains displaced',transform=gx.transAxes,fontsize=8)
else:gx.text(0,.75,'Structural overlay pending source structures.',fontsize=9)
fig.subplots_adjust(top=.95,bottom=.10,left=.07,right=.96)
for ext in ['png','pdf']:fig.savefig(out/f'teaa_main.{ext}',dpi=220)
(out/'teaa_audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
# Two thesis-width compositions keep labels readable when included at text width.
all_axes=list(fig.axes)
for a in all_axes:
 for loc in ("left","center","right"):a.set_title("",loc=loc)
for a in all_axes:a.set_visible(False)
fig.set_size_inches(8.2,7.4)
for a,pos in [(ax,[.09,.59,.37,.31]),(bx,[.59,.59,.37,.31]),(cx,[.12,.16,.34,.28]),(dx,[.59,.16,.37,.28])]:a.set_visible(True);a.set_position(pos)
ax.set_title('A  Uniform hinge coverage',loc='left',fontsize=10);bx.set_title('B  Fitted hinge distributions',loc='left',fontsize=10);cx.set_title('C  State weights, λ = 1000',loc='left',fontsize=10);dx.set_title('D  Independent PC1 comparison',loc='left',fontsize=10)
for ext in ['png','pdf']:fig.savefig(out/f'teaa_coverage_main.{ext}',dpi=240)
# Restore the original, directly interpretable PC1/theta distribution comparison.
# Fresh axes avoid retained titles and colourbars from the other compositions.
plt.close(fig)
fig, axes=plt.subplots(1,2,figsize=(8.2,3.8))
colours=['#8177ba','#e52b90','#6ba518','#e5a000']
curves=[('unguided',False,'Unguided Boltz'),('metad_union',False,'Bias union'),('refined_a025',False,'Refined, uniform'),('refined_a025',True,'Refined + MaxEnt')]
for axis,k,title in zip(axes,['PC1','theta'],['A  Structural displacement','B  Hinge angle']):
 grid=np.linspace(-70,55,600) if k=='PC1' else np.linspace(-50,35,600)
 axis.plot(grid,kde(*md(k),grid),color='#222222',lw=1.9,label='MD target (40:60)')
 for (e,weighted,label),colour in zip(curves,colours):
  axis.plot(grid,kde(*vals(e,k,weighted),grid),color=colour,lw=1.5,ls='--' if weighted else '-',label=label)
 refs=[(-29.87,'#d95f02','Open reference'),(24.46,'#1f78b4','Closed reference')] if k=='PC1' else [(-18.4,'#d95f02','Open reference'),(9.7,'#1f78b4','Closed reference')]
 for x,colour,label in refs:axis.axvline(x,color=colour,lw=1,ls=':',label=label)
 axis.set(xlim=(grid[0],grid[-1]),ylim=(1e-4,.3),yscale='log',xlabel='MD-fitted PC1 (Å)' if k=='PC1' else 'Hinge angle θ (°)',ylabel='Probability density')
 axis.set_title(title,loc='left',fontsize=11,pad=10)
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='lower center',bbox_to_anchor=(.5,.005),ncol=3,frameon=False,fontsize=8)
fig.subplots_adjust(left=.09,right=.98,top=.88,bottom=.28,wspace=.30)
for ext in ['png','pdf']:
 fig.savefig(out/f'teaa_geometry_main.{ext}',dpi=240)
 fig.savefig(out/f'teaa_main.{ext}',dpi=240)
# The mixture fit remains a standalone supporting comparison.
plt.close(fig)
fig,axis=plt.subplots(figsize=(6.8,4.2))
axis.plot(*np.array(pts).T,'o-',color='#225f92',ms=4,label='Reference-like mixtures')
for e,label,ls in [('refined_a025','Refined + MaxEnt','--'),('metad_union','Union + MaxEnt','-.'),('control','Control + MaxEnt',':')]:
 axis.axhline(audit[e]['floor'],color=C[e],ls=ls,label=label)
axis.axvline(.4,color='#777777',ls=':',lw=1)
axis.scatter([.4,fbest],[dict(pts)[.4],mbest],color='#222222',zorder=5)
axis.annotate(f'Target: 0.40\nMinimum: {fbest:.3f}',(.45,mbest),xytext=(.13,.0078),arrowprops={'arrowstyle':'-','lw':.7},fontsize=9)
axis.set(xlim=(0,1),ylim=(0,.0125),xlabel='Open fraction',ylabel='Uptake MSE')
axis.set_title('Uptake agreement across mixtures',loc='left',fontsize=11,pad=10)
axis.legend(loc='lower center',bbox_to_anchor=(.5,-.39),ncol=2,frameon=False,fontsize=8)
fig.subplots_adjust(left=.13,right=.97,top=.90,bottom=.30)
for ext in ['png','pdf']:fig.savefig(out/f'teaa_fit_support.{ext}',dpi=240)
