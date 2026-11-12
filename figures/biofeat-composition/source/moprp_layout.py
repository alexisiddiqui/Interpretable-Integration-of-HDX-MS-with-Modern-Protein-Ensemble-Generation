"""Page-scale layout helpers for revised MoPrP panels; basin composition is unchanged."""
from regions import IDS,COLORS
KEY=['Folded, pH 4 seed','β1-detached arm, near','β1-detached arm, far','Folded, pH 7 seed','Core-distorted lobe','Detached β1–α1 set']
def region_key(fig,y=.02,size=9):
 for k,(code,name,c) in enumerate(zip(IDS,KEY,COLORS)):
  col,row=k%3,k//3
  fig.text(.09+col*.30,y+(1-row)*.026,f'{code}  {name}',fontsize=size,color=c,ha='left',va='bottom')
def enlarge_regions(ax,size=9):
 for text in ax.texts:
  if text.get_text() in IDS:text.set_fontsize(size)
def clear_titles(ax):
 for loc in ['center','left','right']:ax.set_title('',loc=loc)
