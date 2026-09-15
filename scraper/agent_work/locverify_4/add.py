import json,sys,os,math
S=os.path.dirname(os.path.abspath(__file__))+'/'
OUT='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/geo_verified_4.json'
d={x['id']:x for x in json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.loc_verify_4.json'))}
res=json.load(open(OUT)) if os.path.exists(OUT) else []
idx={r['id']:i for i,r in enumerate(res)}
for line in sys.stdin:
  line=line.strip()
  if not line: continue
  r=json.loads(line); x=d[r['id']]
  rec={'id':r['id'],'title':x['title'],'verdict':r['v'],'lat':r.get('lat'),'lng':r.get('lng'),'precision':r.get('p'),
       'address':r.get('addr',x['address']),'evidence_url':r.get('url',''),'evidence':r.get('ev',''),'notes':r.get('n','')}
  if r['v']=='correct' and rec['lat'] is None: rec['lat'],rec['lng']=x['lat'],x['lng']; rec['precision']=rec['precision'] or x.get('geo_precision')
  if r['id'] in idx: res[idx[r['id']]]=rec
  else: idx[r['id']]=len(res); res.append(rec)
json.dump(res,open(OUT,'w'),ensure_ascii=False,indent=1)
print(len(res),'records')
