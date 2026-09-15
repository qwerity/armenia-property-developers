import re, json
from fetch import fetch, links, text
slugs=[]
for off in range(0,150,10):
    st,fu,t=fetch(f"https://www.construction.am/arm/developers.php?offset_pagination={off}")
    for l in links(t):
        m=re.match(r"https://www.construction.am/arm/companies/([^/]+)/$",l)
        if m and m.group(1) not in slugs and m.group(1) not in ('green-line','midea-store'): slugs.append(m.group(1))
print(len(slugs))
out=[]
for s in slugs:
    st,fu,t=fetch(f"https://www.construction.am/companies/{s}/")
    title=re.search(r"<title>(.*?)</title>",t,re.S)
    ext=[l for l in links(t) if l.startswith('http') and 'construction.am' not in l and 'building.am' not in l and not re.search(r'fonts.goog|yandex|liveinternet|mail.ru|rambler|citadeli|construction_portal',l)]
    emails=sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+",t)))
    phones=sorted(set(re.findall(r'tel:([+\d]+)',t)))
    out.append(dict(slug=s,status=st,title=title.group(1).strip() if title else '',ext=list(dict.fromkeys(ext)),emails=emails,phones=phones))
json.dump(out,open('ca.json','w'),ensure_ascii=False,indent=1)
for o in out: print(o['slug'],o['status'],o['title'][:60],o['ext'][:4],o['emails'][:2])
