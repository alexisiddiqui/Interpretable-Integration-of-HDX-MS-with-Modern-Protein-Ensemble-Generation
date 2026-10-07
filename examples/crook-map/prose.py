import sys,re
a,b=int(sys.argv[1]),int(sys.argv[2])
cur=''
for i,l in enumerate(open('tagged.txt'),1):
    if i<a: continue
    if i>b: break
    m=re.match(r'=====\[PDF (\d+) \| p\. (\w+)\]',l)
    if m: print(f'\n[p. {m.group(2)}]'); continue
    s=l.rstrip()
    if len(s)>70 or re.match(r'^(Fig\.|\d+\.\d|[A-C]\.\d)',s.strip()): print(s.strip())
