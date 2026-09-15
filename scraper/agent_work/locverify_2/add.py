import sys,json,math,os
IN="/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.loc_verify_2.json"
OUT="/Users/ksh/agents/news-agent/armenia-new-builds/scraper/geo_verified_2.json"
src={x["id"]:x for x in json.load(open(IN))}
res=json.load(open(OUT)) if os.path.exists(OUT) else []
def hav(a,b,c,d):
    R=6371000;p=math.radians
    return 2*R*math.asin(math.sqrt(math.sin(p(c-a)/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(p(d-b)/2)**2))
for arg in sys.argv[1:]:
    r=json.loads(arg); s=src[r["id"]]
    o={"id":r["id"],"title":s["title"],"verdict":r["verdict"],"lat":r.get("lat"),"lng":r.get("lng"),"precision":r.get("precision"),
       "address":r.get("address",s["address"]),"evidence_url":r.get("evidence_url",""),"evidence":r.get("evidence",""),"notes":r.get("notes","")}
    if o["verdict"]=="correct" and o["lat"] is None: o["lat"],o["lng"]=s["lat"],s["lng"]
    if o["lat"] is not None: print(r["id"],o["verdict"],"move_m=",round(hav(s["lat"],s["lng"],o["lat"],o["lng"])))
    res=[x for x in res if x["id"]!=o["id"]]+[o]
order=list(src)
res.sort(key=lambda x:order.index(x["id"]))
json.dump(res,open(OUT,"w"),ensure_ascii=False,indent=1)
print("total",len(res))
