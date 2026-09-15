import sys,json,html
from f import get
base,typ=sys.argv[1],sys.argv[2]
st,u,tx=get(f"{base}/wp-json/wp/v2/{typ}?per_page=100&_embed=1")
print(st)
try: j=json.loads(tx)
except Exception: print(tx[:300]); sys.exit()
for p in j:
    print(p["id"], html.unescape(p["title"]["rendered"]), p["link"], p.get("date"), p.get("project_category"))
