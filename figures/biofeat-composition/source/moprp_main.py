"""Recompose archived MoPrP trajectories and stationary weights without fitting models.
Usage: python moprp_main.py <input-directory> <output-directory>
"""
import sys,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
from regions import decorate,NAMES,IDS,COLORS
from moprp_layout import region_key,enlarge_regions,clear_titles
root,out=map(Path,sys.argv[1:3]);out.mkdir(parents=True,exist_ok=True)
basins=json.load(open(root/'seeded/basins_seed.json'));scores=np.load(root/'basins/pca101_scores.npz')
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
sets=[]
for tag in ['half1_20ns','ext100_100ns','ext100b_100ns','ext100c_100ns']:
 q=np.load(root/f'seeded/qc/task_list_{tag}.npz');sets.extend((r,q,j) for j,r in enumerate(json.loads(str(q['runs']))) if tag!='half1_20ns' or r['basin'] in ['ph4_1','ph7_1'])
# Extensions replace their own 20 ns prefix, so each trajectory appears once.
sets=list({r['entry']:(r,q,j) for r,q,j in sets}.values())
# All folded-start trajectories, and all extended lobe/set trajectories. The appendix retains the full grid.
fig,axes=plt.subplots(2,3,figsize=(8.8,7.6),sharex=True,sharey=True)
columns=[(['ph4_1','ph7_1'],'Folded starts\nOrigins 4.1 and 7.1'),(['ph7_2'],'Core-distorted lobe\nOrigin 7.2'),(['ph7_3'],'Detached β1–α1 set\nOrigin 7.3')]
counts={}
for row,ph in enumerate(['ph4','ph7']):
 for col,(tags,title) in enumerate(columns):
  ax=axes[row,col];u=scores[f'{ph}_u'];ax.scatter(u[::10,0],u[::10,1],s=.7,color='#bbbbbb',alpha=.22,rasterized=True)
  chosen=[(r,q,j) for r,q,j in sets if r['basin'] in tags and r['target_ph']==ph];counts[f'{ph}_{col}']=len(chosen)
  for r,q,j in chosen:
   x=q[f'r{j:03d}_pc'];t=q[f'r{j:03d}_time_ps']/1000;win=max(1,round(1/np.median(np.diff(t))));x=uniform_filter1d(x.astype(float),win,axis=0,mode='nearest')
   idx=['ph4_1','ph4_2','ph4_3','ph7_1','ph7_2','ph7_3'].index(r['basin']);c=COLORS[idx]
   if col==0:c='#2166ac' if r['basin']=='ph4_1' else '#b2182b'
   ax.plot(x[:,0],x[:,1],color=c,lw=.6,alpha=.7,rasterized=True);ax.scatter(*x[0],s=17,facecolor='white',edgecolor=c,lw=.9,zorder=6);ax.scatter(*x[-1],s=16,marker='s',color=c,zorder=6)
  decorate(ax,basins);enlarge_regions(ax);ax.tick_params(labelsize=9);ax.set(xlim=(-40,135),ylim=(-100,65),xlabel='PC1' if row==1 else '',ylabel=f'Run at pH {ph[-1]}\nPC2' if col==0 else '')
  clear_titles(ax)
  if row==0:ax.set_title(title,fontsize=10,loc='left',pad=10)
  ax.text(.02,.02,('24 runs\n12 × 20 + 12 × 100 ns' if col==0 else '12 runs × 100 ns'),transform=ax.transAxes,fontsize=8.5,bbox={'facecolor':'white','edgecolor':'none','alpha':.85})
assert counts == {'ph4_0':24,'ph4_1':12,'ph4_2':12,'ph7_0':24,'ph7_1':12,'ph7_2':12},counts
fig.text(.09,.105,'○ Start   ■ End   Lines: 1 ns mean   Grey: unbiased MD',fontsize=9)
fig.text(.09,.08,'Folded-start colours: blue, origin pH 4; red, origin pH 7.',fontsize=9)
region_key(fig,size=8.5);fig.subplots_adjust(left=.09,right=.98,top=.91,bottom=.20,wspace=.12,hspace=.16)
for ext in ['png','pdf']:fig.savefig(out/f'moprp_paths_main.{ext}',dpi=220)
# The stored segment-model prior is identical to the original main model maximum-likelihood populations.
W=np.load(root/'msm_weights.npz');report=json.load(open(root/'msm_report.json'));kt=report['kT_kcal'];audit={'trajectory_counts':counts,'kT_kcal':kt,'arm_bin':{}}
fig,axes=plt.subplots(2,2,figsize=(8.6,8.6));ranges=[[[-50,140],[-100,70]],[[np.log10(.42),np.log10(1.6)],[np.log10(7),np.log10(120)]]]
for row,ph in enumerate(['ph4','ph7']):
 x=W[f'{ph}_x'];w=W[f'{ph}_w_prior']
 for col in [0,1]:
  ax=axes[row,col];h,xe,ye=np.histogram2d(x[:,col*2],x[:,col*2+1],bins=60,range=ranges[col],weights=w)
  with np.errstate(divide='ignore'):g=-kt*np.log(h/h.sum())
  g-=np.min(g[np.isfinite(g)]);im=ax.pcolormesh(xe,ye,np.ma.masked_invalid(g.T),cmap='viridis',vmin=0,vmax=6,rasterized=True)
  if col==0:
   decorate(ax,basins,white=True);enlarge_regions(ax);ix=np.searchsorted(xe,87.5)-1;iy=np.searchsorted(ye,17.5)-1;audit['arm_bin'][ph]={'xedges':xe[ix:ix+2].tolist(),'yedges':ye[iy:iy+2].tolist(),'G':float(g[ix,iy])}
   ax.scatter(87.5,17.5,marker='*',s=140,facecolor='white',edgecolor='#222222',zorder=10)
   ax.annotate('Arm state\n(87.5, 17.5)',(87.5,17.5),xytext=(-35,46),color='#222222',fontsize=9,bbox={'facecolor':'white','edgecolor':'none','alpha':.9},arrowprops={'arrowstyle':'-','color':'#222222'},zorder=10)
   ax.set(xlabel='PC1',ylabel='PC2')
  else:
   xt=[.5,.6,.8,1,1.5];yt=[10,20,40,60,100];ax.set_xticks(np.log10(xt),labels=xt);ax.set_yticks(np.log10(yt),labels=yt);ax.set(xlabel='dRMSD to 2L39 (rad, log)',ylabel='β1 deviation (°, log)')
  clear_titles(ax);ax.set_title(f"{'ABCD'[row*2+col]}  pH {ph[-1]}",loc='left',fontsize=11);ax.tick_params(labelsize=9)
fig.subplots_adjust(left=.10,right=.88,bottom=.29,top=.94,hspace=.28,wspace=.32)
cax=fig.add_axes([.92,.31,.02,.57]);fig.colorbar(im,cax=cax,label='Projected free energy (kcal/mol)')
fig.text(.10,.175,'Each map is zeroed at its own minimum. Candidate opening ΔG\nintegrates structural-state weights, rather than projected bins.',fontsize=9)
fig.text(.10,.115,'pH 4 opening ΔG (kcal/mol)     Candidate       HDX\nPUF1                                           2.60          2.2 ± 0.2\nPUF2                                           3.35          3.1 ± 0.5',fontsize=9,linespacing=1.45)
region_key(fig,size=8.5)
for ext in ['png','pdf']:fig.savefig(out/f'moprp_msm_main.{ext}',dpi=220)
(out/'moprp_audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2))
