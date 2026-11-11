from pathlib import Path
import json,urllib.request,urllib.parse,concurrent.futures
r=Path(__file__).resolve().parent

def get(url):
 with urllib.request.urlopen(url,timeout=60) as f:return json.load(f)
q={'query':{'type':'group','logical_operator':'and','nodes':[{'type':'terminal','service':'text','parameters':{'attribute':'struct.title','operator':'contains_words','value':v}} for v in ['KRAS','HLA']]},'return_type':'entry','request_options':{'paginate':{'start':0,'rows':1000}}}
d=get('https://search.rcsb.org/rcsbsearch/v2/query?json='+urllib.parse.quote(json.dumps(q)));(r/'title-query.json').write_text(json.dumps(q,indent=2));(r/'title-results.json').write_text(json.dumps(d,indent=2))
ids=set(v['identifier'] for v in d.get('result_set',[]))
for n in ['g12d','wt']:ids.update(v['identifier'] for v in json.loads((r/f'{n}-results.json').read_text())['result_set'])
def entry(pdb):
 d=get(f'https://data.rcsb.org/rest/v1/core/entry/{pdb}');(r/f'{pdb}-entry.json').write_text(json.dumps(d,indent=2));entities=[]
 for eid in d['rcsb_entry_container_identifiers']['polymer_entity_ids']:
  e=get(f'https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb}/{eid}');(r/f'{pdb}-entity-{eid}.json').write_text(json.dumps(e,indent=2))
  entities.append({'id':eid,'description':e['rcsb_polymer_entity'].get('pdbx_description'),'sequence':e['entity_poly'].get('pdbx_seq_one_letter_code_can'),'chains':e['rcsb_polymer_entity_container_identifiers'].get('auth_asym_ids')})
 return {'pdb':pdb,'title':d['struct']['title'],'method':d.get('exptl'),'entities':entities}
with concurrent.futures.ThreadPoolExecutor(6) as pool:results=list(pool.map(entry,sorted(ids)))
(r/'inventory.json').write_text(json.dumps(results,indent=2))
for e in results:print(e['pdb'],e['title'],[(p['description'],len(p['sequence']),p['sequence'] if len(p['sequence'])<30 else '') for p in e['entities']],flush=True)
