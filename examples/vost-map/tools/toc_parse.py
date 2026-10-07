import re, json, sys
S='/private/tmp/claude-501/-Users-alexi-Library-CloudStorage-OneDrive-Nexus365-Rotation-Projects-Rotation-3-Thesis-OPIG-theses/1a78a980-eb77-4848-9ee3-90f80bd30341/scratchpad/'
pages=open(S+'thesis.txt').read().split('\f')[:177]   # pages[i-1] = PDF index i
def norm(l): return re.sub(r'\s+',' ',l).strip()
# TOC lives on PDF idx 11..14 (printed ix..xii)
lines=[]
for i in range(11,15):
    for l in pages[i-1].split('\n'):
        l=norm(l)
        if l and not re.fullmatch(r'(ix|x|xi|xii)|(x|xi|xii) Contents|Contents (xi)|Contents',l): lines.append(l)
# join wrapped titles: a line without a trailing page number is continued by next line
joined=[];buf=''
for l in lines:
    buf=(buf+' '+l).strip() if buf else l
    if re.search(r'(\. ){2,}\.? ?\d+$',buf) or re.search(r'^\d+ .*\s\d+$',buf) or buf in('Appendices',) or re.match(r'^(References|List of Figures)\s',buf):
        joined.append(buf);buf=''
if buf: joined.append(buf)
out=[]
for j in joined:
    j=re.sub(r'(\w)- (\w)',r'\1\2',j) if False else j
    m=re.match(r'^(?:(\d+(?:\.\d+)*|[A-Z](?:\.\d+)?)\s+)?(.*?)\s*(?:(?:\. ){2,}\.?\s*)?(\d+|[ivx]+)$',j)
    out.append((j,m.groups() if m else None))
for o in out: print(o)
