import json,sys,re,collections
from pathlib import Path
C=Path('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.cache_datalex')
for w in sys.argv[1:]:
    k=re.sub(r"[^\w]+","_",w)
    c=collections.Counter()
    tot=[]
    for role in ('claimant','respondant'):
        f=C/f"civil_{role}_{k}_1.json"
        if not f.exists(): print(w,'not yet'); continue
        r=json.loads(f.read_text()).get('result') or {}
        tot.append(r.get('totalCount'))
        for x in r.get('data') or []:
            for p in re.split(r",\s*", x.get(role+'_full_name') or ''):
                if re.search(w, p, re.I): c[re.sub(r'[«»"<>\s]+',' ',p).strip().upper()]+=1
    print(w, tot, c.most_common(25))
