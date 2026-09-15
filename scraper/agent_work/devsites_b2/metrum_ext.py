import re,sys,json,html;sys.path.insert(0,'.')
from f import get,text
def props(url):
    h=get(url); out={}
    for a,v in re.findall(r'\s:([\w-]+)="(\[?\{&quot;.*?)"(?=\s|>)',h,re.S):
        try: out.setdefault(a,json.loads(html.unescape(v)))
        except: pass
    return out
lst=props('https://metruminvest.am/en/project/renet')['projects']
res={}
for p in lst:
    print(p['slug'],p['title_en'],'sold_out',p['sold_out'],'children',[(c.get('slug'),c.get('title_en')) for c in p.get('child_projects',[])][:30])
    pr=props('https://metruminvest.am/en/project/'+p['slug']).get('project',{})
    res[p['slug']]={'list':p,'project':pr}
json.dump(res,open('metrum.json','w'),ensure_ascii=False)
pr=res['renet']['project']; print([k for k in pr.keys()])
