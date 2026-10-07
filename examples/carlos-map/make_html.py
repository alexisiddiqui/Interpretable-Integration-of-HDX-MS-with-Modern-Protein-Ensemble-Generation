import json
d = json.load(open('thesis.json'))
s = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
t = open('map.template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in t
open('map.html', 'w', encoding='utf-8').write(t.replace('/*__DATA__*/', s))
import os
print('map.html', os.path.getsize('map.html') // 1024, 'KB')
