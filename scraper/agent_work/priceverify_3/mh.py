import json,sys,time,urllib.request,re
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def post(bid,page):
    req=urllib.request.Request("https://myhome.am/API/v1/apartments/filter",data=json.dumps({"buildingId":bid,"pageNumber":page,"pageSize":100}).encode(),headers={"User-Agent":UA,"Content-Type":"application/json","Accept":"application/json","Accept-Language":"en"},method="POST")
    with urllib.request.urlopen(req,timeout=60) as r: return json.loads(r.read()), r.headers.get('x-pagination','{}')
for bid in map(int,sys.argv[1:]):
    units=[];p=1
    while True:
        d,h=post(bid,p); time.sleep(0.6)
        units+=d.get('apartments') or []
        if not json.loads(h).get('HasNext'): break
        p+=1
    if units and p==1 and bid==int(sys.argv[1]): print('keys',sorted(units[0].keys()))
    rows=[]
    for a in units:
        pr=a.get('minApartmentPrice'); ar=a.get('area')
        if pr and ar: rows.append((pr/ar,pr,ar,a.get('roomsCount'),a.get('isStudio'),a.get('status') or a.get('apartmentStatus')))
    rows.sort()
    print(bid,'units',len(units),'priced',len(rows))
    for r in rows[:4]: print('   m2=%.0f total=%s area=%s rooms=%s studio=%s st=%s'%r)
    if rows: print('   cheapest total', min(rows,key=lambda r:r[1])[1:3])
