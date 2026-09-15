import re,sys,json,html;sys.path.insert(0,'.')
from metrum_ext import props
m=json.load(open('metrum.json'))
def price_stats(pp):
    ab=pp.get('all-building-apartments') or {}
    rows=[]
    for b,v in ab.items():
        items=v if isinstance(v,list) else (v.get('apartments') or v.get('data') or list(v.values()) if isinstance(v,dict) else [])
        for a in items:
            if isinstance(a,dict) and a.get('area') and a.get('price'):
                try: rows.append((float(a['area']),float(a['price']),a.get('sold_status'),a.get('room')))
                except: pass
    return rows
out={}
for s in list(m.keys()):
    pp=props('https://metruminvest.am/en/project/'+s)
    rows=price_stats(pp)
    ppm=[p/a for a,p,st,r in rows if p>1000]
    raw=[p for a,p,st,r in rows]
    print(s,len(rows),'ppm',(int(min(ppm)),int(max(ppm))) if ppm else None,'rawprice sample',raw[:4],'status',set(st for _,_,st,_ in rows))
    out[s]=rows
ch={}
for c in m['EdenPark']['list']['child_projects']:
    pr=props('https://metruminvest.am/en/project/'+c['slug']).get('project',{})
    rows=price_stats(props('https://metruminvest.am/en/project/'+c['slug']))
    ppm=[p/a for a,p,st,r in rows if p>1000]
    ch[c['slug']]=dict(title=c['title_en'],delivery=pr.get('delivery_date'),n=pr.get('number_residences'),smin=pr.get('size_apartments_min'),smax=pr.get('size_apartments_max'),floors=pr.get('flat_taxes_en'),sold=c.get('sold_out'),ppm=int(min(ppm)) if ppm else None)
    print(ch[c['slug']])
json.dump({'rows':out,'children':ch},open('metrum2.json','w'),ensure_ascii=False)
