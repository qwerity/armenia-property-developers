import sys,json,re; sys.path.insert(0,'.')
from mk import *
from f import text
m=json.load(open('metrum.json')); m2=json.load(open('metrum2.json'))
dev="Metrum Invest"; du="https://metruminvest.am/"; ph=["+37411886886","+37455886886"]; em="info@metruminvest.am"
so={"facebook":"https://www.facebook.com/metrum.am/","instagram":"https://www.instagram.com/metrum_invest/"}
def dd(s):
    mm=re.match(r'(\d\d)/(\d\d)/(\d{4})',s or ""); return f"{mm.group(3)}-{mm.group(1)}" if mm else None
def gal(p):
    return [g['urls']['original'] for g in (p.get('attachments_gallery') or []) if g.get('urls',{}).get('original')]
meta={"tsaghkadzor-park":dict(city="Tsaghkadzor",district="Kotayk",address="17 M. Mkrtchyan St, Tsaghkadzor",floors="5,7,9,11",type="resort"),
 "renet":dict(city="Yerevan",district="Kentron",address="136/2 Verin Antarayin St, Yerevan",floors="6",type="residential"),
 "antarainn":dict(city="Yerevan",district="Kentron",address="4/1 L. Azgaldyan St, Verin Antarain, Yerevan",floors="6",type="residential"),
 "emin-6":dict(city="Yerevan",district="Kentron",address="6 Gevorg Emin St, Yerevan",floors="6",type="residential"),
 "toon-27":dict(city="Zovuni",district="Kotayk",address="27 Zovuni 30th St, 2nd lane, Kotayk (near Davtashen)",floors="18",type="residential"),
 "rubinyants-complex":dict(city="Yerevan",district="Avan",address="27/16 Rubinyants St, Yerevan",floors="16",type="residential"),
 "EdenPark":dict(city="Arinj",district="Kotayk",address="Arinj, M. Mkrtchyan St / Artashat highway, Abovyan community",floors="5-9",type="residential"),
 "antarayin7-1":dict(city="Yerevan",district="Kentron",address="7/1 Verin Antarayin St, Yerevan",floors="4",type="residential"),
 "masis-central":dict(city="Masis",district="Ararat",address="5 Araratyan St, Masis",floors="9",type="residential")}
now="2026-09"
P=[]
for s,d in m.items():
    p=d['project']; l=d['list']; mt=meta[s]
    comp=dd(p.get('delivery_date'))
    sold=l.get('sold_out')==1
    status="completed" if comp and comp<now else "under construction"
    rows=m2['rows'].get(s,[])
    avail=[pr for a,pr,st,r in rows if pr and 100<pr<5000]
    ppm_k=min(avail) if avail else None
    about=text(p.get('about_project_en') or '')
    facts=f"{p.get('number_residences')} apartments of {p.get('size_apartments_min')}-{p.get('size_apartments_max')} m2; site {p.get('common_area_en')} m2, green area {p.get('green_area_en')} m2, parking {p.get('parking_lot_en')}, lifts {p.get('elevators_en')}. Delivery {p.get('delivery_date')}." if s!="EdenPark" else ""
    if s=="EdenPark":
        sched={}
        for c in m2['children'].values(): sched.setdefault(dd(c['delivery']),[]).append(c['title'].replace('Eden Park','').strip())
        facts="~2,500 apartments of 30-125 m2 in 5-9 storey buildings; 13 ha site (75,000 m2 green), 1,800 parking spaces. Building delivery schedule: "+"; ".join(f"{k}: {', '.join(v)}" for k,v in sorted(sched.items()))+"."
        status="under construction"; comp="2030-06"
    P.append(rec(source_url=f"https://metruminvest.am/en/project/{s}",title=l['title_en'],developer=dev,developer_url=du,
        price_min_amd_m2=int(ppm_k*1000) if ppm_k else None,price_currency_raw=(f"from {int(ppm_k)} thousand AMD/m2 (unit list)" if ppm_k else (f"price {p.get('price')}-{p.get('price_max')} (site field, unit unspecified)" if str(p.get('price')) not in ('0','X','None') else ""))+("; sold out" if sold else ""),
        completion=comp,status=status,phones=ph,email=em,social=so,images=gal(p),videos=(["https://youtu.be/-qqJHnc3-8c"] if s=="EdenPark" else []),
        description=(facts+" "+about) if s=="EdenPark" else (about[:420]+" "+facts),**mt))
save("45_metrum",P,{"note":"Eden Park children (21 buildings) summarised in one record"})
for r in P: print(r['title'],r['completion'],r['status'],r['price_min_amd_m2'],len(r['images']),r['description'][:120])
