import sys,subprocess,json,urllib.parse,time
q=sys.argv[1]
r=subprocess.run(["curl","-s","-m","90","-A","armenia-new-builds-map/1.0","--data-urlencode","data="+q,"https://overpass-api.de/api/interpreter"],capture_output=True,text=True).stdout
try:
    d=json.loads(r)
except: print(r[:500]); sys.exit()
for e in d["elements"]:
    t=e.get("tags",{}); c=e.get("center") or ({"lat":e.get("lat"),"lon":e.get("lon")})
    print(e["type"],e["id"],c.get("lat"),c.get("lon"),"|",t.get("name"),t.get("addr:street"),t.get("addr:housenumber"),t.get("building"),t.get("landuse"),t.get("place"))
