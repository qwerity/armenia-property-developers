import re, json
from fetch import *
st,fu,t=fetch("https://ar-go.am/en/projects")
slugs=sorted(set(re.findall(r'https://ar-go.am/en/project/([a-z0-9-]+)"',t)))
# check pagination
for p in range(2,6):
    s2,f2,t2=fetch(f"https://ar-go.am/en/projects?page={p}")
    new=set(re.findall(r'https://ar-go.am/en/project/([a-z0-9-]+)"',t2))-set(slugs)
    print('page',p,len(new)); 
    if not new: break
    slugs+=sorted(new)
out=[]
for s in slugs:
    st,fu,t=fetch(f"https://ar-go.am/en/project/{s}")
    x=text(t)
    title=re.search(r"<title>(.*?)</title>",t,re.S)
    dev=re.search(r"Developer:?\s*(.{3,60}?)\s+(?:Total area|Construction Company|Bank|Address)",x)
    out.append(dict(slug=s,title=title.group(1).strip() if title else '',developer=dev.group(1) if dev else None))
    print(out[-1])
json.dump(out,open('argo.json','w'),ensure_ascii=False,indent=1)
