from pathlib import Path
import urllib.request,urllib.parse,json
r=Path(__file__).resolve().parent
for name,seq in [('g12d','VVVGADGVGK'),('wt','VVVGAGGVGK')]:
 q={'query':{'type':'group','logical_operator':'and','nodes':[{'type':'terminal','service':'seqmotif','parameters':{'value':seq,'pattern_type':'simple','sequence_type':'protein'}},{'type':'group','logical_operator':'or','nodes':[{'type':'terminal','service':'full_text','parameters':{'value':v}} for v in ['HLA','MHC']]}]},'return_type':'entry','request_options':{'paginate':{'start':0,'rows':1000}}}
 url='https://search.rcsb.org/rcsbsearch/v2/query?json='+urllib.parse.quote(json.dumps(q))
 with urllib.request.urlopen(url,timeout=60) as f:d=json.load(f)
 (r/f'{name}-broad-query.json').write_text(json.dumps(q,indent=2));(r/f'{name}-broad-results.json').write_text(json.dumps(d,indent=2));print(name,[x['identifier'] for x in d.get('result_set',[])])
