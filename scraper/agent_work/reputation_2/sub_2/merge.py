import json, os, glob

D = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.dirname(D)
order = [x['developer'] for x in json.load(open(os.path.join(TOP, 'chunk_2.json')))]
entries = {}
for fn in glob.glob(os.path.join(D, 'e', '*.json')):
    e = json.load(open(fn))
    assert e['developer'] in order, e['developer']
    entries[e['developer']] = e
out = [entries[n] for n in order if n in entries]
tmp = os.path.join(TOP, 'entities_2.json.tmp')
json.dump(out, open(tmp, 'w'), ensure_ascii=False, indent=1)
os.replace(tmp, os.path.join(TOP, 'entities_2.json'))
print(len(out), 'entries; missing:', [n for n in order if n not in entries])
