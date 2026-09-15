import json,sys,os,math
OUT='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/geo_verified_3.json'
S=os.path.dirname(os.path.abspath(__file__))+'/res.json'
inp={x['id']:x for x in json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.loc_verify_3.json'))}
res=json.load(open(S)) if os.path.exists(S) else {}
# args: id verdict lat lng precision address evidence_url evidence notes
a=sys.argv[1:]
id,v,lat,lng,p,addr,eu,ev=a[:8]; notes=a[8] if len(a)>8 else ''
x=inp[id]
lat=float(lat) if lat not in ('','null') else None; lng=float(lng) if lng not in ('','null') else None
if v=='correct' and lat is None: lat,lng=x['lat'],x['lng']
if not addr: addr=x['address']
res[id]={"id":id,"title":x['title'],"verdict":v,"lat":lat,"lng":lng,"precision":(p if p not in ('','null') else None),"address":addr,"evidence_url":eu,"evidence":ev,"notes":notes}
json.dump(res,open(S,'w'),ensure_ascii=False,indent=1)
order=[k for k in inp if k in res]
json.dump([res[k] for k in order],open(OUT,'w'),ensure_ascii=False,indent=1)
if lat is not None:
    R=6371000;r=math.radians
    d=2*R*math.asin(math.sqrt(math.sin(r(lat-x['lat'])/2)**2+math.cos(r(lat))*math.cos(r(x['lat']))*math.sin(r(lng-x['lng'])/2)**2))
    print(id,v,'move',round(d),'m; total',len(res))
else: print(id,v,'total',len(res))
