import re, json
from fetch import *
slugs=[]
for p in range(1,7):
    u="https://www.pages.am/en/real-estate-developers/"+("" if p==1 else f"?page={p}")
    st,fu,t=fetch(u)
    for s in re.findall(r'https://www.pages.am/en/pages/([a-z0-9-]+)/',t):
        if s not in slugs: slugs.append(s)
print(len(slugs))
out=[]
for s in slugs:
    st,fu,t=fetch(f"https://www.pages.am/en/pages/{s}/")
    title=re.search(r"<title>(.*?)</title>",t,re.S)
    ext=[l for l in links(t) if l.startswith('http') and 'pages.am' not in l and not re.search(r'google|apple.com|yandex|w3.org|schema.org|gstatic|cloudflare|jsdelivr',l)]
    out.append(dict(slug=s,title=title.group(1).strip() if title else '',ext=list(dict.fromkeys(ext))[:12]))
    print(out[-1]['title'][:70],'|',[e for e in out[-1]['ext'] if 'facebook' not in e and 'instagram' not in e][:4])
json.dump(out,open('pages.json','w'),ensure_ascii=False,indent=1)
