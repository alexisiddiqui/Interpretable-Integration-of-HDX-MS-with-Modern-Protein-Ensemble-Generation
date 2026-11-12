"""Compose existing basin evidence with common region identifiers and newly labelled renders."""
from pathlib import Path
import json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap,Normalize
from regions import decorate,key,NAMES,IDS
root,renders,out=map(Path,sys.argv[1:]);bs=json.load(open(root/'basins/frames101_trim/basins.json'));seed=json.load(open(root/'seeded/basins_seed.json'));S=np.load(root/'basins/pca101_scores.npz')
fig=plt.figure(figsize=(14,8.8));gs=fig.add_gridspec(2,4,width_ratios=[1.1,1,1,1],wspace=.08,hspace=.35)
for row,ph in enumerate(['ph4','ph7']):
 ax=fig.add_subplot(gs[row,0]);x=np.concatenate([S[f'{ph}_mi'],S[f'{ph}_mmpb']]);edges=np.linspace(-120,150,70);h,_,_=np.histogram2d(x[:,0],x[:,1],bins=(edges,edges));ax.pcolormesh(edges,edges,np.ma.masked_where(h.T==0,np.log10(np.maximum(h.T,1))),cmap='Greys',vmin=-.5,vmax=4.2,rasterized=True)
 ref=S[f'{ph}_reference'];ax.scatter(ref[:,0],ref[:,1],s=8,color='black',label='2L39');ax.scatter(*S[f'{ph}_af3'],s=100,marker='*',color='#e34948',edgecolor='white',label='AF3 start');decorate(ax,seed);ax.set(xlim=(-50,140),ylim=(-100,70),xlabel='PC1',ylabel='PC2');ax.set_title(f'pH {ph[-1]}: restrained frame counts',fontsize=10,loc='left');ax.legend(frameon=False,fontsize=7,loc='upper left')
 for col in range(3):
  idx=row*3+col;b=bs[idx];ax=fig.add_subplot(gs[row,col+1]);ax.imshow(plt.imread(renders/(Path(b['file']).stem+'.png')));ax.axis('off');ax.set_title(f'{IDS[idx]}  {NAMES[idx]}',fontsize=9,loc='left')
  ax.text(0,-.04,f"{b['frames_in_basin']:,} frames in circle; {len(b['frames'])} shown\nMI+PB seed origin pH {ph[-1]} #{b['id']}",transform=ax.transAxes,fontsize=8)
cmap=LinearSegmentedColormap.from_list('pymol',[(1,1,.5),(1,.5,0),(1,.65,.85),(1,0,0),(0,0,0)])
cax=fig.add_axes([.38,.085,.4,.013]);fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(.5,8),cmap=cmap),cax=cax,orientation='horizontal',label='Per-residue backbone RMSD from minimised AF3 start (Å)')
fig.suptitle('Restrained basin coverage and segment displacement',x=.06,ha='left',fontsize=14);fig.subplots_adjust(left=.06,right=.98,top=.9,bottom=.2)
fig.text(.5,.145,'All structures share a core-aligned camera; grey tube: minimised reference. Labels mark reference segments.\nCircles and identifiers denote seed geometry; they do not assign experimental PUF states.',ha='center',fontsize=9)
for ext in ['png','pdf']:fig.savefig(out/f'moprp_basins_main.{ext}',dpi=220)
