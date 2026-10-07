import re,json
t=open('thesis.txt').read().split('\f')
lines=[]
for p in range(11,16):
    for l in t[p-1].split('\n'):
        s=re.sub(r'\s+',' ',l.strip())
        if not s: continue
        if re.match(r'^(Table of contents( [xvi]+)?|[xvi]+ Table of contents)$',s): continue
        lines.append(s)
ents=[];cur=None
start=re.compile(r'^((?:Appendix [A-C]|[A-C]\.\d+(?:\.\d+)*|\d+(?:\.\d+)*))\s+(.*)$')
for s in lines:
    m=start.match(s)
    if s.startswith('List of'): 
        mm=re.match(r'^(List of \w+) ([xvi]+)$',s); ents.append({'num':None,'title':mm.group(1),'page':mm.group(2),'done':True}); cur=None; continue
    if m and (cur is None or cur['done']):
        cur={'num':m.group(1),'title':m.group(2),'done':False}; ents.append(cur)
    elif cur and not cur['done']:
        cur['title']+=' '+s
    else:
        print('SKIP',s); continue
    mm=re.search(r'(?:\. ?){2,}\s*(\d+)$',cur['title']) or (re.search(r'(?<=[a-z\)])\s*(\d{1,3})$',cur['title']) if re.match(r'^[\d]+$',cur['num']) and '.' not in cur['num'] else None)
    if mm:
        cur['page']=int(mm.group(1)); cur['done']=True
        cur['title']=re.sub(r'(\. ?){2,}\s*\d+$','',cur['title']); cur['title']=re.sub(r'\s*\d{1,3}$','',cur['title']) if '. .' not in cur['title'] and True else cur['title']
        cur['title']=cur['title'].strip()
# refs
for e in ents: e.pop('done',None)
for e in ents: print(e)
json.dump(ents,open('toc.json','w'),indent=1)
print(len(ents))
