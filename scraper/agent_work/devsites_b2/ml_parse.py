import re,sys,json;sys.path.insert(0,'.')
from f import get,text
h=get('https://mlmining.am/en/construction')
cards=[]
for c in re.findall(r'<div class="icon-box">(.*?)<!-- End Icon Box -->',h,re.S):
    g=lambda p: (re.search(p,c,re.S).group(1).strip() if re.search(p,c,re.S) else "")
    pt=g(r'pt=([\d.]+,[\d.]+)')
    cards.append(dict(img="https://mlmining.am"+g(r'<img src="([^"?]+)'),title=text(g(r'<h4>(.*?)</h4>')),site=g(r'<h4><a[^>]*href="([^"]+)"'),address=text(g(r'class="address">(.*?)</p>')),region=text(g(r'class="region">(.*?)</p>')),details=text(g(r'class="details">(.*?)</p>')),view=g(r'href="(https://charagayt[^"]+)"'),lng=float(pt.split(',')[0]) if pt else None,lat=float(pt.split(',')[1]) if pt else None))
json.dump(cards,open('ml_cards.json','w'),ensure_ascii=False,indent=1)
for c in cards: print(c)
