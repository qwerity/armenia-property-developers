import sys,json,os,time,urllib.request,urllib.parse,hashlib
D=os.path.dirname(os.path.abspath(__file__)); C=D+"/ovpcache"; os.makedirs(C,exist_ok=True)
BB="(38.8,43.4,41.3,46.7)"
def run(q):
    fn=C+"/"+hashlib.md5(q.encode()).hexdigest()+".json"
    if os.path.exists(fn): return json.load(open(fn))
    for ep in ["https://maps.mail.ru/osm/tools/overpass/api/interpreter","https://overpass-api.de/api/interpreter"]:
        try:
            r=urllib.request.urlopen(urllib.request.Request(ep,data=urllib.parse.urlencode({"data":q}).encode(),headers={"User-Agent":"armenia-new-builds-map/1.0"}),timeout=45).read()
            d=json.loads(r); json.dump(d,open(fn,"w")); time.sleep(1); return d
        except Exception as e: print("ERR",ep,e); time.sleep(2)
    return {"elements":[]}
def addr(street,hn=None,bbox=BB):
    h=f'["addr:housenumber"~"^{hn}"]' if hn else ""
    q=f'[out:json][timeout:60];(nwr{h}["addr:street"~"{street}",i]{bbox};);out center tags 200;'
    return run(q)["elements"]
def road(street,bbox=BB):
    q=f'[out:json][timeout:60];way["highway"]["name"~"{street}",i]{bbox};out center tags 60;'
    return run(q)["elements"]
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="addr": els=addr(sys.argv[2], sys.argv[3] if len(sys.argv)>3 and sys.argv[3] else None, sys.argv[4] if len(sys.argv)>4 else BB)
    else: els=road(sys.argv[2], sys.argv[3] if len(sys.argv)>3 else BB)
    for e in els:
        c=e.get("center") or {"lat":e.get("lat"),"lon":e.get("lon")}; t=e.get("tags",{})
        print(round(c["lat"],6),round(c["lon"],6),t.get("addr:street",t.get("name")),t.get("addr:housenumber",""),t.get("addr:city",""),t.get("building",""),t.get("name","") if "addr:street" in t else "")
