import sys,json,re; sys.path.insert(0,'.')
from mk import *
from f import text
det=json.load(open("red_det.json")); L=json.load(open("red_list.json"))
S3="https://redgroup-public.s3.eu-central-1.amazonaws.com/"
MON={m:i+1 for i,m in enumerate(["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"])}
SKIP={"79","289","400"}  # Smart City -> handled in Smart City developer section
def completion(vd):
    m=re.search(r'(?:completion|end)(.{0,70})',vd,re.I)
    if not m: return None
    s=m.group(1)
    for pat in [r'(\d{1,2})[.․/](\d{1,2})[.․/](\d{2,4})', r'(\d{1,2})/(20\d\d)', r'([A-Za-z]+)\s+(20\d\d)', r'(20\d\d)\.?\s*([A-Za-z]+)', r'(20\d\d)']:
        mm=re.search(pat,s)
        if not mm: continue
        g=mm.groups()
        if len(g)==3:
            y=g[2]; y="20"+y if len(y)==2 else y; return f"{y}-{int(g[1]):02d}"
        if len(g)==2 and g[0].isdigit() and g[1].isdigit(): return f"{g[1]}-{int(g[0]):02d}"
        if len(g)==2 and not g[0].isdigit():
            mo=MON.get(g[0][:3].lower()); return f"{g[1]}-{mo:02d}" if mo else g[1]
        if len(g)==2:
            mo=MON.get(g[1][:3].lower()); return f"{g[0]}-{mo:02d}" if mo else g[0]
        return g[0]
    return None
DEVO={"408":"Argavand Towers LLC","411":"House Construction LLC","302":"1SQ Estate Development","386":"1SQ Estate Development","405":"Life House LLC","311":"TM Mega Holding LLC","298":"S. S. Brothers LLC","133":"Ecology Construction LLC","57":"New Home LLC","54":"TM Mega Holding LLC","396":"Villa Town House LLC","344":"Villa Town House LLC","334":"Amikson Sapphire LLC"}
def developer(vd):
    m=re.search(r'(?:Project Manager and )?Developer[s]?\s*(?:of the complex is|is|[:—-])?\s*[«"“”]*\s*([A-Za-z0-9][^«»"“”]{1,40}?)\s*[»"“”]',vd,re.I) or re.search(r'Developer[s]?\s*[:—-]\s*([A-Z][\w .&-]{2,40}?)(?=\s+(?:Design|Contractor|Partner|Architect|Start|Construction|Builder)|$)',vd)
    return m.group(1).strip() if m else None
def district(addr):
    for k,v in [("Kentron","Kentron"),("Nork-Marash","Nork-Marash"),("Nork Marash","Nork-Marash"),("Nor Nork","Nor Nork"),("Nor-Nork","Nor Nork"),("Nor-Norq","Nor Nork"),("Avan","Avan"),("Ajapnyak","Ajapnyak"),("Davtashen","Davtashen"),("Arabkir","Arabkir"),("Erebuni","Erebuni"),("Noragyugh","Kentron"),("Mher Mkrtchyan","Avan"),("Nairi district","Davtashen")]:
        if re.search(r'\b'+re.escape(k.lower())+r'\b',addr.lower()): return v
    return ""
def city(addr,title):
    for k,v in [("Nor Hachn","Nor Hachn"),("Argavand","Argavand"),("Tsakhkadzor","Tsaghkadzor"),("Tsaghkadzor","Tsaghkadzor"),("Yeghvard","Yeghvard"),("Merdzavan","Merdzavan"),("Jrvej","Jrvezh")]:
        if k.lower() in (addr+title).lower(): return v
    return "Yerevan"
P=[]; now="2026-09"
for x in L:
    k=str(x["id"])
    if k in SKIP: continue
    d=det[k]; p=d["project"]; c=(p.get("content") or [{}])[0] or {}
    vd=text(c.get("videoDescList") or ""); desc=text(c.get("description") or "")
    title=re.split(r'\s*[—–]\s*|\s+-\s*|-\s*(?=[A-Z][a-z])|․\s|\.\s', p["title"])[0].strip()
    lat=lng=None
    if p.get("coordinates"):
        a,b=[float(v) for v in re.findall(r'[\d.]+',p["coordinates"])[:2]]; lat,lng=a,b
    prods=d.get("products") or []
    amd=[x_["price"]/x_["area"] for x_ in prods if x_.get("price") and x_.get("area") and x_["currency_id"]==1]
    usd=[x_["price"]/x_["area"] for x_ in prods if x_.get("price") and x_.get("area") and x_["currency_id"]==2]
    amd=[v for v in amd if 150000<v<5000000]; usd=[v for v in usd if 300<v<15000]
    comp=completion(vd); dev=DEVO.get(k) or developer(vd)
    past=bool(comp) and (comp[:7]<now if len(comp)>4 else comp<now[:4])
    st="completed" if past or (x["status"]=="sold" and not comp) else ("under construction" if comp else None)
    imgs=[p["image"]] if p.get("image") else []
    for f_ in d.get("files") or []:
        u=f_["url"]
        if f"projects/{k}/" not in u: continue
        u=u if u.startswith("http") else S3+u
        if u not in imgs: imgs.append(u)
    vids=[]
    if c.get("descriptionVideo"):
        m=re.search(r'embed/([\w-]+)',c["descriptionVideo"]); vids=["https://www.youtube.com/watch?v="+m.group(1)] if m else []
    rooms={}
    for x_ in prods:
        r=str(x_.get("rooms") or ""); 
        if not x_.get("area"): continue
        e=rooms.setdefault(r,{"rooms":r,"area_min":x_["area"],"area_max":x_["area"],"price_from":x_.get("price"),"currency":"AMD" if x_["currency_id"]==1 else "USD"})
        e["area_min"]=min(e["area_min"],x_["area"]); e["area_max"]=max(e["area_max"],x_["area"])
        if x_.get("price") and (not e["price_from"] or x_["price"]<e["price_from"]): e["price_from"]=x_["price"]
    addr=re.sub(r'^'+re.escape(title)+r'[^,]*,\s*','',p["address"]) if p["address"].lower().startswith(title.lower()[:8]) else p["address"]
    if addr.startswith("bnakarankarucapatoxic"): addr=""
    typ="commercial" if "Technopark –" in p["title"] else ("resort" if "Novotel" in title else "residential")
    dd=(f"Developer: {dev}. " if dev else "")+(f"Completion: {comp}. " if comp else "")+desc
    P.append(rec(source_url=f"https://www.redinvest.am/en/developers/{p['slug']}" if p.get("slug") else f"https://redgroup.am/api/projects/{k}",title=title,
        developer=(dev+" (sales: RED Invest Group)") if dev else "RED Invest Group (exclusive sales agent)",developer_url="https://www.redinvest.am/en",
        city=city(p["address"],title),district=district(p["address"]+" "+title),address=addr or title,lat=lat,lng=lng,
        price_min_amd_m2=int(min(amd)) if amd else None,price_min_usd_m2=int(min(usd)) if usd else None,
        price_currency_raw=("from %s AMD/m2 (computed from listed units)"%f"{int(min(amd)):,}" if amd else "")+("; " if amd and usd else "")+("from $%s/m2 (listed units)"%f"{int(min(usd)):,}" if usd else "")+("; sold out" if x["status"]=="sold" else ""),
        completion=comp,status=st,type=typ,phones=["+37498908908"],email="areg.khachatryan@redinvest.am",website=f"https://www.redinvest.am/en/developers/{p['slug']}",
        social={"facebook":"https://www.facebook.com/redinvestgroup","instagram":"https://www.instagram.com/redinvestgroup/"},
        images=imgs,videos=vids,description=dd,apartments=sorted(rooms.values(),key=lambda e:e["rooms"]) or None))
save("33_redinvest",P,{"note":"RED Invest is a sales agent; Smart City 1-3 moved to Smart City developer section"})
for r in P: print(r["title"][:35],"|",r["developer"][:40],"|",r["completion"],r["status"],"|",r["price_min_amd_m2"],r["price_min_usd_m2"],"|",r["district"],r["city"],"|",len(r["images"]),r["address"][:50])
