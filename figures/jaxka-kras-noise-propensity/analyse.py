"""Run on Pegasus with the POISK JAX environment; intact bound graph, noise-only partner tokens."""
from pathlib import Path
import os,json,hashlib,csv
import numpy as np
import jax,jax.numpy as jnp
from pkanet.allres import AllResiduePredictor
from pkanet.features import prepare_file
from pkanet.model import norm,linear
root=Path(__file__).resolve().parent
model=Path(os.environ['NOISE_MODEL'])
p=AllResiduePredictor(model,device=os.environ.get('NOISE_DEVICE','gpu'),backend='jax',batch_size=1,compilation_cache=False)
names=['g12d','wt','empty']; outputs={}; metadata={}
for name in names:
 rec=prepare_file(root/'structures'/f'{name}.pdb',root/'cache',gap_policy='cap')
 _,o=next(p.predict([rec],states=('bound',)))
 outputs[name]=o['bound'];metadata[name]=rec[1]
 print('embedded',name,len(o['bound']['edge_embedding']),flush=True)
e=p.params['aux_redge']
@jax.jit
def scores(z,raw):
 r=norm(e['norm'],raw)
 features=jnp.concatenate((z[:,None,:]*r[None,:,:],jnp.abs(z[:,None,:]-r[None,:,:])),axis=-1)
 return jax.nn.sigmoid(linear(e['out'],jax.nn.gelu(linear(e['hidden'],features)))[...,0]).mean(1)
results={}; audits={}
# Four independent 8192-vector replicates; nested half-sample convergence; alternate uniform noise.
for name in names:
 z=jnp.asarray(outputs[name]['edge_embedding']); runs=[]; halves=[]
 for seed in [17,29,43,71]:
  rng=np.random.default_rng(seed); chunks=[]
  for b in range(32):
   chunks.append(np.asarray(scores(z,jnp.asarray(rng.standard_normal((256,z.shape[1])).astype('float32')))))
  runs.append(np.mean(chunks,axis=0));halves.append(np.mean(chunks[:16],axis=0))
 rng=np.random.default_rng(17); alt=[]
 for b in range(32):alt.append(np.asarray(scores(z,jnp.asarray(rng.uniform(-np.sqrt(3),np.sqrt(3),(256,z.shape[1])).astype('float32')))))
 runs=np.array(runs);mean=runs.mean(0);uniform=np.mean(alt,axis=0)
 results[name]=dict(mean=mean,replicates=runs,half=np.array(halves),uniform=uniform,z=np.asarray(z),exposure=1-jax.nn.sigmoid(outputs[name]['burial_logit']))
 audits[name]={'n':len(mean),'range':[float(mean.min()),float(mean.max())],'max_seed_sd':float(runs.std(0,ddof=1).max()),'max_half_full_difference':float(np.max(np.abs(np.mean(halves,0)-mean))),'uniform_pearson':float(np.corrcoef(mean,uniform)[0,1]),'uniform_max_abs':float(np.max(abs(mean-uniform)))}
 np.savez_compressed(root/f'{name}.npz',**results[name])
 with (root/f'{name}.csv').open('w') as f:
  w=csv.writer(f);w.writerow(['chain','number','insertion','score','seed_sd','uniform_score','exposure'])
  for i,r in enumerate(metadata[name]['residues']):w.writerow([r['chain'],r['number'],r.get('insertion',''),mean[i],runs[:,i].std(ddof=1),uniform[i],float(results[name]['exposure'][i])])
 print(name,audits[name],flush=True)
receipt={'model':str(model),'params_sha256':hashlib.sha256((model/'params.npz').read_bytes()).hexdigest(),'state':'bound: intact assembly, no external partner','seeds':[17,29,43,71],'vectors_per_seed':8192,'noise':'iid Gaussian N(0,1) before learned edge layer norm','sensitivity':'variance-one iid uniform before same norm','jax':jax.__version__,'devices':str(jax.devices()),'audit':audits,'structures':{n:hashlib.sha256((root/'structures'/f'{n}.pdb').read_bytes()).hexdigest() for n in names}}
(root/'provenance.json').write_text(json.dumps(receipt,indent=2))
