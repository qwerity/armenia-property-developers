import json,sys,os
SP=os.path.dirname(os.path.abspath(__file__))
IN='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.price_verify_2.json'
OUT='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/price_verified_2.json'
RATE=363.5
keys=["id","title","verdict","usd_m2","amd_m2","currency_shown","apartment_from_total","apartment_from_area_m2","evidence_url","evidence_text","sold_out","wrong_merge_urls","notes"]
for e in json.loads(sys.stdin.read()) if not sys.stdin.isatty() else []:
    src={x['id']:x for x in json.load(open(IN))}[e['id']]
    e.setdefault('title',src['title'])
    if e.get('usd_m2') is None and e.get('amd_m2'): e['usd_m2']=round(e['amd_m2']/RATE)
    if e.get('amd_m2') is None and e.get('usd_m2'): e['amd_m2']=round(e['usd_m2']*RATE/1000)*1000
    for k in keys: e.setdefault(k,None if k not in('wrong_merge_urls','notes') else ([] if k=='wrong_merge_urls' else ''))
    assert e['verdict'] in('confirmed','corrected','unverifiable')
    assert len(e['evidence_text'] or '')<=120, e['id']
    json.dump({k:e[k] for k in keys},open(f"{SP}/res/{e['id']}.json",'w'),ensure_ascii=False)
order=[x['id'] for x in json.load(open(IN))]
out=[json.load(open(f"{SP}/res/{i}.json")) for i in order if os.path.exists(f"{SP}/res/{i}.json")]
json.dump(out,open(OUT,'w'),ensure_ascii=False,indent=1)
print(len(out),'written')
