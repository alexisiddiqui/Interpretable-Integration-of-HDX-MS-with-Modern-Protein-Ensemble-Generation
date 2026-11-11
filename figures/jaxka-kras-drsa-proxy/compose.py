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
red=LinearSegmentedColormap.from_list('response',['#ffffff','#deebf7','#c6dbef','#9ecae1','#6baed6','#3182bd','#08519c'])
div=LinearSegmentedColormap.from_list('difference',['#1959b2','white','#b20a1f'])
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
 strip.set_yticks([]);strip.set_title('Peptide burial-change proxy',fontsize=8,loc='left',pad=4)
 for i,v in enumerate(values):strip.text(i,0,f'{v:.3f}',ha='center',va='center',fontsize=6,color='white' if v>.18 else 'black')
cax=fig.add_axes([.3,.14,.4,.022]);fig.colorbar(ScalarMappable(norm=Normalize(*p['score_limits']),cmap=red),cax=cax,orientation='horizontal',label='hmask burial-change proxy (exposure × noise contact)')
for ext in ['png','pdf','svg']:fig.savefig(r/f'groove.{ext}',dpi=300,facecolor='white')
plt.close(fig)
