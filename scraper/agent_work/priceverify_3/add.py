import json,sys,os
OUT='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/price_verified_3.json'
cur=json.load(open(OUT)) if os.path.exists(OUT) else []
keys=["id","title","verdict","usd_m2","amd_m2","currency_shown","apartment_from_total","apartment_from_area_m2","evidence_url","evidence_text","sold_out","wrong_merge_urls","notes"]
for e in json.load(sys.stdin):
    e={k:e.get(k, [] if k=='wrong_merge_urls' else None) for k in keys}
    assert e['verdict'] in ('confirmed','corrected','unverifiable'), e
    assert len(e['evidence_text'] or '')<=120, e['id']
    cur=[c for c in cur if c['id']!=e['id']]+[e]
json.dump(cur,open(OUT,'w'),ensure_ascii=False,indent=1)
print(len(cur))
