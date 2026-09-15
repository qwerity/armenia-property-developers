import json,sys,os
OUT='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_3/web_A.json'
new=json.load(sys.stdin)
cur=json.load(open(OUT)) if os.path.exists(OUT) else []
for n in (new if isinstance(new,list) else [new]):
    cur=[c for c in cur if c['developer']!=n['developer']]+[n]
json.dump(cur,open(OUT,'w'),ensure_ascii=False,indent=1)
print(len(cur),[c['developer'] for c in cur])
