import json,sys,os
OUT='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_3/web_B.json'
new=json.load(open(sys.argv[1]))
if isinstance(new,dict): new=[new]
cur=json.load(open(OUT)) if os.path.exists(OUT) else []
idx={d['developer']:i for i,d in enumerate(cur)}
for n in new:
    if n['developer'] in idx: cur[idx[n['developer']]]=n
    else: cur.append(n)
json.dump(cur,open(OUT,'w'),ensure_ascii=False,indent=1)
print(len(cur),[d['developer'] for d in cur])
