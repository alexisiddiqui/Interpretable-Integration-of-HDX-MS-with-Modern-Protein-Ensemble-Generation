"""Compose both property comparisons without recalculating or rescaling maps."""
from pathlib import Path
import copy
import subprocess
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
NS='http://www.w3.org/2000/svg'
ET.register_namespace('',NS)
def el(tag,attrs=None,text=None):
 n=ET.Element('{'+NS+'}'+tag,attrs or {})
 if text is not None:n.text=text
 return n
def text(x,y,s,size=17,weight='normal'):
 return el('text',dict(x=str(x),y=str(y),fill='#20242c',**{'font-family':'DejaVu Sans,Arial,sans-serif','font-size':str(size),'font-weight':weight}),s)
out=el('svg',dict(width='1840',height='1125',viewBox='0 0 1840 1125'))
out.append(el('rect',dict(width='1840',height='1125',fill='white')))
for i,(title,subtitle) in enumerate([('Crystal · G12D','7OW6'),('Crystal · WT','7OW5'),('Screened hit · G12D','ID_1457932'),('Screened hit · WT','ID_1457932')]):
 out.append(text(i*460+38,30,title,22,'bold'));out.append(text(i*460+38,55,subtitle,15))
for row,name in enumerate(['electrostatics','hydrophobicity']):
 source=ET.parse(ROOT/(name+'.svg')).getroot()
 groups=[n for n in source if n.tag.endswith('}g')]
 y=90+row*500
 out.append(text(25,y, name.capitalize(),22,'bold'))
 for i,group in enumerate(groups):
  # The inner group contains exactly the dashboard map at its original scale.
  panel=copy.deepcopy(list(group)[-1]); panel.set('transform',f'translate({i*460},{y+5})')
  raw=ET.tostring(panel,encoding='unicode').replace('map-',name+'-map-')
  out.append(ET.fromstring(raw));out.append(text(i*460+18,y+38,chr(65+row*4+i),20,'bold'))
 defs=copy.deepcopy(next(n for n in source if n.tag.endswith('}defs')))
 for n in defs.iter():
  if n.get('id')=='scale':n.set('id',name+'-scale')
 out.append(defs)
 out.append(el('rect',dict(x='1290',y=str(y-13),width='220',height='10',fill=f'url(#{name}-scale)')))
 lo,hi,unit=('-5','+5','Potential (kT/e)') if row==0 else ('-4.5','+4.5','Kyte–Doolittle index')
 out.append(text(1250,y,lo,14));out.append(text(1522,y,hi,14));out.append(text(1580,y,unit,14))
out.append(text(30,1100,'25 Å radius · 5 Å rings     Peptide trace in teal · mutation site in pink · original screened patch outlined in gold',16))
ET.ElementTree(out).write(ROOT/'fig.svg',encoding='unicode',xml_declaration=True)
subprocess.run(['rsvg-convert','-f','pdf','-o',str(ROOT/'fig.pdf'),str(ROOT/'fig.svg')],check=True)
subprocess.run(['rsvg-convert','-w','2200','-o',str(ROOT/'fig.png'),str(ROOT/'fig.svg')],check=True)
