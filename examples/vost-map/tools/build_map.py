"""Stage 2: embed thesis.json into map_template.html -> ../map.html (single self-contained file)."""
import json
d=json.load(open('../thesis.json'))
d['quality'].pop('coverage_report',None)   # keep the page lean; report lives in coverage_report.txt
js=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
t=open('map_template.html').read()
assert '/*__DATA__*/' in t
open('../map.html','w').write(t.replace('/*__DATA__*/',js))
import os;print('map.html',os.path.getsize('../map.html'),'bytes')
