import re,json,glob
pages={}
for i in range(1,267):
    t=open(f'ocr/p{i:03d}.txt').read()
    lines=[l.strip() for l in t.splitlines() if l.strip()]
    cand=None
    if lines:
        # footer: lone number; header: ends/starts with number
        for l in [lines[-1],lines[0]]:
            m=re.fullmatch(r'(\d{1,3})',l)
            if m: cand=int(m.group(1));break
            m=re.search(r'(?:^|\s)(\d{1,3})$',l) if l is lines[0] else None
            m2=re.match(r'^(\d{1,3})\s+[A-Z]',l)
            if m and l is lines[0]: cand=int(m.group(1));break
            if m2 and l is lines[0]: cand=int(m2.group(1));break
    pages[i]=(cand,len(t.split()))
offs={}
for i,(c,w) in pages.items():
    if c: offs.setdefault(i-c,[]).append(i)
for o,v in sorted(offs.items()): print('offset',o,'n=',len(v),'range',min(v),max(v))
print([ (i,pages[i]) for i in range(1,267) if pages[i][0] is None][:80])
print('low-word pages',[i for i in pages if pages[i][1]<40])
