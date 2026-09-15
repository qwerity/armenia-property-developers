import json,os,re,glob
from urllib.parse import urlparse
OUT="/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developer_projects_b2.json"
D=os.path.dirname(os.path.abspath(__file__))
KEYS=["source","source_url","title","developer","developer_url","city","district","address","lat","lng","price_min_usd_m2","price_min_amd_m2","price_currency_raw","completion","status","floors","type","phones","email","website","social","images","videos","description","apartments"]
def rec(**kw):
    r={k:None for k in KEYS}
    r.update({"phones":[],"email":"","images":[],"videos":[],"social":{"facebook":"","instagram":"","youtube":"","telegram":""},"price_currency_raw":"","address":"","district":"","floors":None,"description":""})
    soc=kw.pop("social",None) or {}
    r["social"].update({k:v or "" for k,v in soc.items()})
    r.update(kw)
    if not r["source"] and r["source_url"]: r["source"]=urlparse(r["source_url"]).netloc.replace("www.","")
    if not r["website"]: r["website"]=r["source_url"]
    r["images"]=list(dict.fromkeys(r["images"]))[:12]
    r["videos"]=list(dict.fromkeys(r["videos"]))
    if r["description"] and len(r["description"])>700: r["description"]=r["description"][:697].rsplit(" ",1)[0]+"..."
    if r.get("apartments") is None: r.pop("apartments")
    if isinstance(r["floors"],int): r["floors"]=str(r["floors"])
    return r
def save(slug,recs,meta=None):
    json.dump({"projects":recs,"meta":meta or {}},open(os.path.join(D,"out",slug+".json"),"w"),ensure_ascii=False,indent=1)
    merge()
def merge():
    allr=[];seen=set()
    for fn in sorted(glob.glob(os.path.join(D,"out","*.json"))):
        for r in json.load(open(fn))["projects"]:
            k=(r["developer"],r["source_url"],r["title"])
            if k in seen: continue
            seen.add(k); allr.append(r)
    json.dump(allr,open(OUT,"w"),ensure_ascii=False,indent=1)
    print("saved",len(allr))
def tilda(u):
    m=re.match(r"https://thb\.tildacdn\.(?:one|com)/(tild[\w-]+)/-/(?:empty|resize/\w+)/(.+)",u)
    return f"https://static.tildacdn.one/{m.group(1)}/{m.group(2)}" if m else u
