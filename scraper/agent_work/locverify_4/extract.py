import json, re, math, html
S='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/locverify_4/'
d=json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.loc_verify_4.json'))
um=json.load(open(S+'urlmap.json'))
LAT=r'(3[89]\.\d{3,}|4[01]\.\d{3,})'; LNG=r'(4[3-6]\.\d{3,})'
pats=[('3d2d',r'!3d'+LAT+r'!(?:2d|4d)'+LNG,0),('2d3d',r'!2d'+LNG+r'!3d'+LAT,1),('@',r'@'+LAT+r','+LNG,0),
('q=',r'[?&;](?:q|ll|center|daddr|destination|query)=(?:loc:)?'+LAT+r'(?:,|%2C)\s*'+LNG,0),
('yll',r'(?:ll|pt)=(?:%5B)?'+LNG+r'(?:,|%2C)'+LAT,1),
('pair',LAT+r'["\']?\s*[,;]\s*["\']?(?:lng|lon|longitude)?["\']?\s*:?\s*'+LNG,0),
('lat:',r'lat(?:itude)?["\']?\s*[:=]\s*["\']?'+LAT+r'["\']?\s*[,;]\s*["\']?(?:lng|lon|long|longitude)["\']?\s*[:=]\s*["\']?'+LNG,0),
('rev',LNG+r'\s*,\s*'+LAT,1)]
def dist(a,b,c,e): return 6371000*math.hypot(math.radians(c-a),math.radians(e-b)*math.cos(math.radians(a)))
import sys
ids=sys.argv[1:]
for x in d:
  if ids and x['id'] not in ids: continue
  print('=====',x['id'],x['title'],'|',x['address'],'| pin',x['lat'],x['lng'])
  for u in x['sources']:
    t=open(um[u.split('#')[0]],errors='ignore').read()
    found={}
    for name,p,rev in pats:
      for m in re.finditer(p,t):
        la,ln=(m.group(2),m.group(1)) if rev else (m.group(1),m.group(2))
        k=(round(float(la),5),round(float(ln),5))
        if name=='rev' and k in found: continue
        found.setdefault(k,name)
    cnt={}
    items=sorted(found.items())
    print('  ',u[:100],len(items),'cands')
    for k,v in items[:12]: print('     ',v,k,int(dist(x['lat'],x['lng'],*k)),'m')
