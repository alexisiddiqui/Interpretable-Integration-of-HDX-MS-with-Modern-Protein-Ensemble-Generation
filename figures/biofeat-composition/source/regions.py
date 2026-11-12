"""Common seed-region identifiers; geometry is distinct from candidate signatures."""
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
NAMES=['Folded (pH 4 seed)','β1-detached arm, near','β1-detached arm, far','Folded (pH 7 seed)','Core-distorted lobe','Detached β1–α1 set']
IDS=['4.1','4.2','4.3','7.1','7.2','7.3']
COLORS=['#555555','#e29425','#bf6d10','#555555','#8a4fad','#007f79']
def decorate(ax,basins,white=False):
 for b,i,c in zip(basins,IDS,COLORS):
  x,y=b['centre'];ax.add_patch(plt.Circle((x,y),b['radius'],fill=False,ec='white' if white else c,ls='--',lw=1.1,zorder=8))
  dx,dy=(-13,-11) if i=='4.1' else (10,8)
  ax.annotate(i,(x,y),xytext=(dx,dy),textcoords='offset points',color='white' if white else c,fontsize=8,fontweight='bold',zorder=9,path_effects=[pe.withStroke(linewidth=2,foreground='#333333' if white else 'white')])
def key(fig,y=.015):
 fig.text(.5,y,'   '.join(f'{i}  {n}' for i,n in zip(IDS[:3],NAMES[:3]))+'\n'+'   '.join(f'{i}  {n}' for i,n in zip(IDS[3:],NAMES[3:])),ha='center',va='bottom',fontsize=8,linespacing=1.7)
