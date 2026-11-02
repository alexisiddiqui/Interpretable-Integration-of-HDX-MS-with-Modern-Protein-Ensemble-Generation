"""Project matched-start BPTI ensembles onto the archived Anton PCA, without refitting."""
import os,json,hashlib,csv,re
from pathlib import Path
import numpy as np
from biotite.structure.io import load_structure
from biotite.structure.io.xtc import XTCFile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(os.environ['CAMPAIGN_ROOT']); OUT=ROOT/'analysis/pca-comparison';OUT.mkdir(parents=True,exist_ok=True)
OLD=Path('/bitbucket/hussain/BioFeaturisers-production/BPTI/variance-scaled-mi/20260911T215808Z')
ARCH=OLD/'analysis/9abdde1511481f3b'; pca=np.load(ARCH/'pca_cartesian_ca_reference.npz',allow_pickle=True)
REFERENCE=Path('/opig-shared/projects/hussian-simulation_hdx/_runtime/BioFeaturisers/worktrees/cartesian-pca/biofeaturisers/examples/PLUMED/systems/bpti_solution/derived/bpti_5pti_curated.pdb')
EXPECTED=json.loads((ARCH/'analysis_summary.json').read_text())['cartesian_pca']['alignment_reference_sha256']
assert hashlib.sha256(REFERENCE.read_bytes()).hexdigest()==EXPECTED
identities=pca['atom_identities'].astype(str); residues=[int(v.split(':')[1]) for v in identities]
ref=load_structure(REFERENCE);ref=ref[~ref.hetero]
def ca_indices(atoms):
 out=[]
 for res in residues:
  hits=np.flatnonzero((atoms.res_id==res)&(atoms.atom_name=='CA'));assert len(hits)==1,(res,hits);out.append(int(hits[0]))
 return np.asarray(out,dtype=int)
ref_nm=np.asarray(ref.coord,float)[ca_indices(ref)]/10

def project(coords):
 center=ref_nm.mean(0); target=ref_nm-center
 a=coords-coords.mean(axis=1,keepdims=True);cov=np.einsum('fai,aj->fij',a,target)
 u,_,vt=np.linalg.svd(cov);fix=np.ones((len(a),3));fix[:,-1]=np.linalg.det(u@vt)
 rotated=a@((u*fix[:,None,:])@vt)+center
 return (rotated.reshape(len(a),-1)-pca['pca_center'])@pca['loadings']

def read_ca(path,indices,unwrap=False):
 x=XTCFile.read(path,atom_i=indices)
 coords=np.asarray(x.get_coord(),dtype=float)/10
 if unwrap:
  box=np.asarray(x.get_box(),dtype=float)/10
  delta=np.diff(coords,axis=1);frac=np.einsum('fai,fij->faj',delta,np.linalg.inv(box));frac-=np.round(frac)
  delta=np.einsum('faj,fjk->fak',frac,box)
  coords=np.concatenate([coords[:,:1],coords[:,:1]+np.cumsum(delta,axis=1)],axis=1)
  assert np.max(np.linalg.norm(np.diff(coords,axis=1),axis=2))<.8,'CA chain failed PBC reconstruction'
 return np.asarray(x.get_time(),float),project(coords)

summary={'pca_source':str(ARCH/'pca_cartesian_ca_reference.npz'),'refitted':False,'alignment_reference_sha256':EXPECTED,'basin_definition':'Anton C-alpha PC1 < -0.55','threshold_pc1':-.55,'weights':'uniform frame weights for all ensembles; MI weights do not remove PB bias','conditions':{},'validation':{}}
# Validate the fixed projection against every archived corrected source trajectory.
old_template=load_structure(OLD/'mipb-250ns/build/generated_gromacs/protein.gro');ca=ca_indices(old_template)
oldmask=np.char.startswith(pca['segment_label'].astype(str),'mmpb/')
old_scores=pca['analysis_scores'][oldmask];old_time=pca['time'][oldmask];old_reps=pca['replica'][oldmask]
max_error=0.
for r in range(1,5):
 t,s=read_ca(ARCH/f'mmpb/replica_{r}/mmpb_cuda/corrected.xtc',ca)
 m=old_reps==r;assert len(t)==m.sum() and np.allclose(t,old_time[m],atol=.001)
 err=float(np.max(abs(s-old_scores[m])));max_error=max(err,max_error)
assert max_error<1e-8,max_error
summary['validation']['max_abs_source_reprojection_error']=max_error
print('Archived source projection reproduced:',max_error,flush=True)
starts=json.loads((ROOT/'prepared/starts.json').read_text())['records']
for r in starts:
 t,s=read_ca(r['trajectory'],ca,unwrap=True)
 i=np.flatnonzero(abs(t-r['time_ps'])<.001);assert len(i)==1
 err=float(np.max(abs(s[i[0]]-[r['pc1'],r['pc2']])));assert err<.015,err
 summary['validation'][f'raw_selected_start_{r["number"]}_max_pc_error']=err
 print('Raw PBC projection validated for approved start',r['number'],err,flush=True)

THRESH=-.55
WINDOWS=[(0,10),(10,25),(25,50),(50,100),(100,150),(150,200),(200,250)]
def first_sustained_exit(t,inside,dwell=1.):
 if not inside[0]:return None
 outside=~inside
 edges=np.diff(np.r_[False,outside,False].astype(int));beg=np.flatnonzero(edges==1);end=np.flatnonzero(edges==-1)
 for a,b in zip(beg,end):
  dt=np.median(np.diff(t))
  if t[b-1]-t[a]+dt>=dwell-1e-6:return float(t[a])
 return None

def metrics(t,s,r):
 inside=s[:,0]<THRESH
 row={'replica':r,'frames':len(t),'start_pc1':float(s[0,0]),'end_pc1':float(s[-1,0]),'initial_second_basin':bool(inside[0]),'second_basin_fraction':float(inside.mean()),'late_200_250ns_fraction':float(inside[t>=200].mean()),'final_10ns_fraction':float(inside[t>=240].mean()),'first_sustained_exit_ns':first_sustained_exit(t,inside),'windows':[]}
 for lo,hi in WINDOWS:
  m=(t>=lo)&(t<(hi if hi<250 else hi+1e-6));row['windows'].append({'start_ns':lo,'stop_ns':hi,'fraction':float(inside[m].mean()),'frames':int(m.sum())})
 return row

datasets={};all_rows=[]
for c,sub,stage,label in [('mmpb','mmpb_cuda','8mmpb_reweighted_mi_pbmetad','±2 MI+PB'),('mi','mi_cuda','8mi_replica_average','±2 MI'),('u','u','8u_unbiased','Unbiased')]:
 items=[];rows=[]
 for r in range(1,5):
  path=ROOT/f'runs/{c}/build/branches/matched-seq0-starts-250ns/{sub}/replica_{r}'
  if c=='u':path=path/'production_block_0001'
  template=load_structure(ROOT/f'runs/{c}/build/generated_gromacs/protein.gro')
  t,s=read_ca(path/f'{stage}.xtc',ca_indices(template),unwrap=True);t=(t-t[0])/1000
  assert len(t)==25001 and abs(t[-1]-250)<1e-6,(c,r,len(t),t[-1]);assert np.allclose(np.diff(t),.01,atol=1e-6)
  assert (s[0,0]<THRESH)==(starts[r-1]['pc1']<THRESH),'Starting basin mismatch'
  items.append({'time_ns':t,'scores':s,'replica':r});row=metrics(t,s,r);rows.append(row);all_rows.append({'condition':label,**{k:v for k,v in row.items() if k!='windows'}})
  np.savez_compressed(OUT/f'{c}-replica-{r}-projection.npz',time_ns=t,scores=s,replica=r)
  print(c,'replica',r,'second basin',row['second_basin_fraction'],'late',row['late_200_250ns_fraction'],flush=True)
 datasets[c]=items
 pooled=np.concatenate([x['scores'] for x in items]);times=np.concatenate([x['time_ns'] for x in items])
 left=np.concatenate([x['scores'] for x in items if x['replica'] in [1,2]])
 late=np.concatenate([x['scores'][x['time_ns']>=200] for x in items])
 lateleft=np.concatenate([x['scores'][x['time_ns']>=200] for x in items if x['replica'] in [1,2]])
 summary['conditions'][c]={'label':label,'replicas':rows,'second_basin_fraction':float(np.mean(pooled[:,0]<THRESH)),'late_200_250ns_fraction':float(np.mean(late[:,0]<THRESH)),'initial_left_replicas':[1,2],'initial_left_replicas_late_fraction':float(np.mean(lateleft[:,0]<THRESH)),'threshold_sensitivity_late':{str(v):float(np.mean(late[:,0]<v)) for v in [-.65,-.55,-.45]}}
summary['source_seq0']={'second_basin_fraction':float(np.mean(old_scores[:,0]<THRESH)),'late_200_250ns_fraction':float(np.mean(old_scores[old_time>=200000,0]<THRESH))}
reference=pca['reference_scores'];summary['anton_second_basin_fraction']=float(np.mean(reference[:,0]<THRESH))
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
with (OUT/'replica-basin-summary.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(all_rows[0]));w.writeheader();w.writerows(all_rows)
# Preserve original histogram cells, expanding outward only if new frames require it.
joined=np.concatenate([pca['analysis_scores'],reference,*[x['scores'] for c in datasets.values() for x in c]])
orig=np.concatenate([pca['analysis_scores'],reference]);lo=orig.min(0);hi=orig.max(0);width=(hi-lo)/36
edges=[]
for j in range(2):
 before=max(0,int(np.ceil((lo[j]-joined[:,j].min())/width[j])));after=max(0,int(np.ceil((joined[:,j].max()-hi[j])/width[j])))
 edges.append(lo[j]+np.arange(-before,37+after)*width[j])
summary['histogram']={'edges':[v.tolist() for v in edges],'original_bin_widths':width.tolist(),'expanded_extents':bool(any(len(v)!=37 for v in edges))}
variance=pca['explained_variance_ratio'];xlabel=f'Anton reference Cα PC1 ({100*variance[0]:.1f}%)';ylabel=f'Anton reference Cα PC2 ({100*variance[1]:.1f}%)'
def density(ax,s,title):
 h=np.histogram2d(s[:,0],s[:,1],bins=edges)[0];assert int(h.sum())==len(s)
 occupied=h>0;v=np.zeros_like(h);v[occupied]=-np.log(h[occupied]/h.max());v=np.ma.masked_where(~occupied,v)
 im=ax.pcolormesh(*edges,v.T,cmap='viridis',shading='auto',vmin=0,vmax=float(v.max()))
 ax.axvline(THRESH,color='#b33b2e',ls='--',lw=1.15)
 ax.set(xlabel=xlabel,ylabel=ylabel,title=title,xlim=(edges[0][0],edges[0][-1]),ylim=(edges[1][0],edges[1][-1]))
 return im
fig,axes=plt.subplots(2,3,figsize=(16,9),constrained_layout=True)
panels=[('±0 MI+PB source',old_scores),('±2 MI+PB',np.concatenate([x['scores'] for x in datasets['mmpb']])),('±2 MI',np.concatenate([x['scores'] for x in datasets['mi']])),('Unbiased',np.concatenate([x['scores'] for x in datasets['u']])),('Anton reference (1.03 ms)',reference)]
for ax,(label,s) in zip(axes.flat,panels):
 im=density(ax,s,label);fig.colorbar(im,ax=ax,shrink=.83,label='−ln(p/pmax)')
ax=axes.flat[5]
colors={'mmpb':'#7a3db8','mi':'#df7928','u':'#2679b9'}
for c,items in datasets.items():
 centers=np.arange(5,250,10);occ=[]
 for lo2 in np.arange(0,250,10):
  s=np.concatenate([x['scores'][(x['time_ns']>=lo2)&(x['time_ns']<(lo2+10 if lo2<240 else 250.00001))] for x in items]);occ.append(100*np.mean(s[:,0]<THRESH))
 ax.plot(centers,occ,'o-',ms=3,lw=1.8,color=colors[c],label=summary['conditions'][c]['label'])
ax.axhline(100*summary['source_seq0']['second_basin_fraction'],color='#777',ls='--',lw=1,label='±0 source, full-run fraction')
ax.set(xlabel='Time after restart (ns)',ylabel='Frames in second basin (%)',ylim=(-2,102),xlim=(0,250),title='Second-basin occupancy · 10 ns windows');ax.legend(fontsize=8);ax.grid(alpha=.2)
fig.suptitle('BPTI matched-start comparison · fixed Anton PCA basis\nUniform-frame log sampling densities; independent colour scales; dashed boundary PC1 < −0.55',fontsize=14)
fig.savefig(OUT/'bpti-five-ensemble-log-density-pca.png',dpi=190);plt.close(fig)
# Per-replica fate: retain the four start numbers used in the review figure.
fig,axes=plt.subplots(3,1,figsize=(13,10),sharex=True,sharey=True,constrained_layout=True)
repcolors=['#3574bc','#d45b36','#24976a','#a76ab9']
for ax,(c,items) in zip(axes,datasets.items()):
 for x in items:
  t=x['time_ns'];s=x['scores'];v=[]
  for k in range(250):
   m=(t>=k)&(t<(k+1 if k<249 else 250.00001));v.append(float(s[m,0].mean()))
  row=summary['conditions'][c]['replicas'][x['replica']-1]
  ax.plot(np.arange(250)+.5,v,color=repcolors[x['replica']-1],lw=1,label=f'Start {x["replica"]} · late left {100*row["late_200_250ns_fraction"]:.1f}%')
  ax.scatter([0],[s[0,0]],color=repcolors[x['replica']-1],s=30,zorder=4)
 ax.axhline(THRESH,color='#b33b2e',ls='--',lw=1.3);ax.axvspan(200,250,color='#999',alpha=.09)
 ax.set(title=summary['conditions'][c]['label'],ylabel='PC1 · 1 ns mean',xlim=(0,250));ax.grid(alpha=.2);ax.legend(loc='lower right',ncol=2,fontsize=8)
axes[-1].set_xlabel('Time after restart (ns)');fig.suptitle('Do the approved starts remain in the second basin?\nStarts 1 and 2 begin in the left basin; shaded region is the final 50 ns',fontsize=14)
fig.savefig(OUT/'bpti-second-basin-replica-traces.png',dpi=190);plt.close(fig)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('COMPLETE',json.dumps({c:{k:v for k,v in s.items() if k!='replicas'} for c,s in summary['conditions'].items()}),flush=True)
