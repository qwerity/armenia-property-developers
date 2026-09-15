import re, json
from fetch import *
st,fu,t=fetch("https://novostroiki-yerevan.com/en/d/")
slugs=list(dict.fromkeys(re.findall(r'href="/en/d/([^/"]+)/"',t)))
out={}
for s in slugs:
    st,fu,t=fetch(f"https://novostroiki-yerevan.com/en/d/{s}/")
    name=re.search(r"<h1[^>]*>(.*?)</h1>",t,re.S)
    ps=list(dict.fromkeys(re.findall(r'href="/en/p/([^/"]+)/"',t)))
    out[s]=dict(h1=text(name.group(1)).strip() if name else s, projects=ps)
    print(s,out[s])
json.dump(out,open('nov.json','w'),ensure_ascii=False,indent=1)
