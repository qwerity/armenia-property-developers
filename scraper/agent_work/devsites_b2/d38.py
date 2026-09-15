import sys,json,re; sys.path.insert(0,'.')
from mk import *
det=json.load(open("red_det.json"))
S3="https://redgroup-public.s3.eu-central-1.amazonaws.com/"
def red(k):
    d=det[k]; p=d["project"]; imgs=[p["image"]]
    for f_ in d["files"]:
        u=f_["url"]
        if f"projects/{k}/" in u or f"announcements/" in u and int(k)<200:
            u=u if u.startswith("http") else S3+u
            if u not in imgs: imgs.append(u)
    amd=[x["price"]/x["area"] for x in d["products"] if x.get("price") and x.get("area") and x["currency_id"]==1 and 150000<x["price"]/x["area"]<5000000]
    usd=[x["price"]/x["area"] for x in d["products"] if x.get("price") and x.get("area") and x["currency_id"]==2 and 300<x["price"]/x["area"]<15000]
    lat,lng=[float(v) for v in re.findall(r'[\d.]+',p["coordinates"])[:2]]
    v=re.search(r'embed/([\w-]+)',p["content"][0].get("descriptionVideo") or "")
    return dict(images=imgs[:12],lat=lat,lng=lng,price_min_amd_m2=int(min(amd)) if amd else None,price_min_usd_m2=int(min(usd)) if usd else None,videos=["https://www.youtube.com/watch?v="+v.group(1)] if v else [],redurl="https://www.redinvest.am/en/developers/"+p["slug"])
dev="Smart City Developer (Global Real Estate)"; du="https://smart-city.am/"; ph=["+37460742222","+37441900255","+37498908908"]; em="info@smart-city.am"
B="https://smart-city.am/Community?communityId="
P=[]
for cid,k,title,desc,extra in [
 (1,"79","Smart City (Smart City 1)","Gated 'Smart City 1' quarter at Bagrevand 49 (Jrvezh), 9.1 km from Republic Square, 2.2 km from Mega Mall, 620 m from Engineering City: 12,537 m2 site (29% built), 24 townhouses and 4 multi-apartment buildings of 2-3 floors (with attic and basement; 60 apartments), monolithic structure, mineral wool insulation, 3 m ceilings, parking, 5,000 m2 roads/greenery/playgrounds, shop, bar-cafe, kids centre. Built 05/2020-05/2022 by Global Real Estate LLC (architect Suren Gavaryan / Tribeca Studio).",dict(completion="2022-05",status="completed")),
 (2,"289","Smart City 2","Gated innovative district at Bagrevand 49 on 15,044 m2 (29% built), 9.3 km from Republic Square: 10 townhouses and 6 four-storey apartment buildings with semi-basement parking (about 120 apartments), monolithic construction, 3 m ceilings, apartments optionally renovated; roads, greenery, playgrounds, supermarket, swimming pool, gym and cafe. Developer Smart City Developer LLC, builder Global Real Estate.",dict(status="under construction")),
 (3,"400","Smart City 3","Gated family district next to Smart City 2 at Bagrevand 49 on 5,868 m2 (31% built): two 5-storey buildings with semi-basement parking and two 3-storey buildings with semi-basement public spaces, 87 apartments, monolithic with external insulation, 3 m ceilings; supermarket, pool, gym and cafe planned; near Engineering City, Ministry of Defence and Mega Mall.",dict(status="under construction"))]:
    r=red(k)
    P.append(rec(source_url=B+str(cid),title=title,developer=dev,developer_url=du,city="Jrvezh",district="Kotayk",address="Bagrevand 49, Jrvezh (Kotayk)",lat=r["lat"],lng=r["lng"],
      price_min_amd_m2=r["price_min_amd_m2"],price_min_usd_m2=r["price_min_usd_m2"],price_currency_raw=("from %s AMD/m2 (RED Invest listing)"%f"{r['price_min_amd_m2']:,}" if r["price_min_amd_m2"] else ("from $%s/m2 (RED Invest listing)"%r["price_min_usd_m2"] if r["price_min_usd_m2"] else "")),
      floors={1:"2-3",2:"3-4",3:"3-5"}[cid],type="residential",phones=ph,email=em,website=r["redurl"],images=r["images"],videos=r["videos"],description=desc,**extra))
save("38_smartcity",P)
for p in P: print(p["title"],p["price_min_amd_m2"],p["price_min_usd_m2"],len(p["images"]))
