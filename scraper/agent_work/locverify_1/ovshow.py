import json,sys
d=json.load(open(sys.argv[1]))
rows=set()
for e in d['elements']:
    c=e.get('center') or {'lat':e.get('lat'),'lon':e.get('lon')}
    t=e.get('tags',{})
    rows.add((t.get('name') or '', round(c['lat'],5),round(c['lon'],5),t.get('highway') or t.get('building') or '', t.get('addr:street',''),t.get('addr:housenumber','')))
for r in sorted(rows): print(*r)
