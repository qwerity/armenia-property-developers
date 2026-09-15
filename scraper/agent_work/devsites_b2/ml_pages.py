import re,sys,json;sys.path.insert(0,'.')
from f import get,text
cards=json.load(open('ml_cards.json'))
for c in cards:
    if not c['view']: continue
    h=get(c['view']); t=text(h)
    sold=sum(int(x) for x in re.findall(r'(\d+) վաճ\. է',t)); avail=sum(int(x) for x in re.findall(r'(\d+) առկա է',t))
    i=max(t.find('Թաղամասի մասին'),t.find('Համալիրի մասին'),t.find('Շենքի մասին'))
    j=t.find('Այստեղ դուք կարող եք տեսնել')
    seg=t[i:j if j>i else i+1500]
    seg=re.sub(r'Բնակարանները կհանձնվեն՝.*','',seg)
    vids=sorted(set(re.findall(r'youtube\.com/embed/([\w-]+)',h)))
    imgs=[m for m in re.findall(r'(?:src|href)="([^"]+\.(?:jpe?g|png|webp))"',h,re.I) if 'key.png' not in m and 'logo' not in m.lower()][:6]
    c.update(sold=sold,avail=avail,seg=seg[:1100],vids=vids,imgs=imgs)
    print('=====',c['title'],'| sold',sold,'avail',avail,'| vids',vids); print(seg[:1100]); print('IMGS',imgs[:4])
json.dump(cards,open('ml_cards.json','w'),ensure_ascii=False,indent=1)
