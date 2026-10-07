import json
d=json.load(open('thesis.json'))
# drop bulky fields not used by the page
j=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/').replace('<!--','<\\!--')
t=open('map_template.html',encoding='utf-8').read()
assert '/*DATA*/' in t
open('map.html','w',encoding='utf-8').write(t.replace('/*DATA*/',j))
import os;print(os.path.getsize('map.html')//1024,'KB')
