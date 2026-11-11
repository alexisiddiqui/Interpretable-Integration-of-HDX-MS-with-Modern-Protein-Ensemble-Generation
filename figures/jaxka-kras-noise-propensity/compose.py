from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,Normalize
from matplotlib.cm import ScalarMappable
r=Path(__file__).resolve().parent
p=json.loads((r/'render-provenance.json').read_text())
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],'font.size':9,'pdf.fonttype':42,'svg.fonttype':'none'})
red=LinearSegmentedColormap.from_list('response',['white','#8c0a1f'])
div=LinearSegmentedColormap.from_list('difference',['#1959b2','white','#b20a1f'])
fig,ax=plt.subplots(2,3,figsize=(9.4,6.9))
for col,(name,title) in enumerate(zip(['g12d','wt','empty'],['G12D pMHC','WT pMHC','Peptide-free MHC'])):
 for row,view in enumerate(['whole','groove']):
  a=ax[row,col];a.imshow(plt.imread(r/f'{name}-{view}.png'));a.axis('off');a.set_title(f'{"ABCDEF"[row*3+col]}   {title}',loc='left',fontsize=11,pad=3)
fig.subplots_adjust(left=.025,right=.975,bottom=.12,top=.95,hspace=.12,wspace=.035)
cax=fig.add_axes([.3,.065,.4,.018]);fig.colorbar(ScalarMappable(norm=Normalize(*p['score_limits']),cmap=red),cax=cax,orientation='horizontal',label='Noise-averaged hmask contact-head response')
for ext in ['png','pdf','svg']:fig.savefig(r/f'fig.{ext}',dpi=300,facecolor='white')
plt.close(fig)
fig,ax=plt.subplots(1,3,figsize=(10,5.1))
for a,n,t in zip(ax,['g12d','wt','empty'],['G12D · Asp6','WT · Gly6','Peptide-free MHC']):
 a.imshow(plt.imread(r/f'{n}-groove.png'));a.axis('off');a.set_title(t,loc='left',fontsize=11)
fig.subplots_adjust(left=.015,right=.985,top=.84,bottom=.43,wspace=.02)
fig.text(.5,.95,'Peptide sticks and HLA surface share one scale · P6 labelled · N → C left to right',ha='center',fontsize=9)
for col,n in enumerate(['g12d','wt']):
 with (r/f'{n}.csv').open() as f:rows=[v for v in csv.DictReader(f) if v['chain']=='C']
 rows.sort(key=lambda v:int(v['number']));values=np.array([float(v['score']) for v in rows])
 strip=fig.add_axes([.04+col*.33,.30,.28,.045])
 strip.imshow(values[None,:],aspect='auto',cmap=red,vmin=p['score_limits'][0],vmax=p['score_limits'][1])
 strip.set_xticks(range(10),[f'{i+1}\n{aa}' for i,aa in enumerate('VVVGADGVGK' if n=='g12d' else 'VVVGAGGVGK')],fontsize=7)
 strip.set_yticks([]);strip.set_title('Peptide residue response',fontsize=8,loc='left',pad=4)
 for i,v in enumerate(values):strip.text(i,0,f'{v:.2f}',ha='center',va='center',fontsize=6,color='white' if v>.22 else 'black')
cax=fig.add_axes([.3,.14,.4,.022]);fig.colorbar(ScalarMappable(norm=Normalize(*p['score_limits']),cmap=red),cax=cax,orientation='horizontal',label='Noise-averaged hmask contact-head response')
for ext in ['png','pdf','svg']:fig.savefig(r/f'groove.{ext}',dpi=300,facecolor='white')
plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(8,3.8))
for a,n,title in zip(ax,['wt','empty'],['G12D − WT','G12D − peptide-free']):
 a.imshow(plt.imread(r/f'delta-{n}.png'));a.axis('off');a.set_title(title,loc='left',fontsize=11)
fig.subplots_adjust(left=.02,right=.98,top=.9,bottom=.24,wspace=.04)
cax=fig.add_axes([.3,.14,.4,.025]);fig.colorbar(ScalarMappable(norm=Normalize(*p['difference_limits']),cmap=div),cax=cax,orientation='horizontal',ticks=np.linspace(*p['difference_limits'],5),format='%.2f',label='Change in noise-averaged response')
for ext in ['png','pdf','svg']:fig.savefig(r/f'differences.{ext}',dpi=300,facecolor='white')
# Paired differences, finite-sample stability and exposure comparison.
from types import SimpleNamespace
def spearmanr(a,b):
 def ranks(x):
  _, inverse, counts=np.unique(x,return_inverse=True,return_counts=True)
  return (np.cumsum(counts)-0.5*(counts-1))[inverse]
 return SimpleNamespace(statistic=np.corrcoef(ranks(a),ranks(b))[0,1])
stats={};ds={}
for n in ['g12d','wt','empty']:
 d=np.load(r/f'{n}.npz');ds[n]=d
 stats[n]={'exposure_spearman':float(spearmanr(d['mean'],d['exposure']).statistic),'uniform_spearman':float(spearmanr(d['mean'],d['uniform']).statistic),'min_pairwise_seed_spearman':min(float(spearmanr(a,b).statistic) for i,a in enumerate(d['replicates']) for b in d['replicates'][i+1:])}
keys={}
for n in ds:
 with (r/f'{n}.csv').open() as f:keys[n]=[(x['chain'],x['number'],x['insertion']) for x in csv.DictReader(f)]
for n in ['wt','empty']:
 idx=[keys['g12d'].index(k) for k in keys[n]]
 delta=ds['g12d']['mean'][idx]-ds[n]['mean'];rep=ds['g12d']['replicates'][:,idx]-ds[n]['replicates']
 stats['delta_'+n]={'max_abs':float(abs(delta).max()),'rms':float(np.sqrt(np.mean(delta**2))),'max_paired_seed_sd':float(rep.std(0,ddof=1).max())}
 with (r/f'delta-{n}.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['chain','number','insertion','g12d_minus_control','paired_seed_sd'])
  for k,v,s in zip(keys[n],delta,rep.std(0,ddof=1)):w.writerow([*k,v,s])
(r/'comparison.json').write_text(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2))
