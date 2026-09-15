import json,subprocess,sys,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def units(bid):
    out=[];p=1
    while True:
        r=subprocess.run(['curl','-s','-m','40','-A',UA,'-H','Content-Type: application/json','-H','Accept: application/json','-D','/dev/stderr','-d',json.dumps({"buildingId":bid,"pageNumber":p,"pageSize":100}),'https://myhome.am/API/v1/apartments/filter'],capture_output=True,text=True)
        a=json.loads(r.stdout).get('apartments') or []; out+=a
        if '"HasNext":true' not in r.stderr: break
        p+=1; time.sleep(1)
    return out
for bid in sys.argv[1:]:
    a=units(int(bid)); print('== building',bid,len(a),'units; booked',sum(x['isBooked'] for x in a))
    a.sort(key=lambda x:x['minAreaPrice'] or 9e9)
    for x in a[:5]: print('  m2 %s total %s area %s rooms %s floor %s booked %s studio %s free %s'%(x['minAreaPrice'],x['minApartmentPrice'],x['area'],x['roomsCount'],x['floor'],x['isBooked'],x['isStudio'],x['isFreePlaning']))
    c=min(a,key=lambda x:x['minApartmentPrice'] or 9e12) if a else None
    if c: print('  cheapest total',c['minApartmentPrice'],c['area'],c['minAreaPrice'])
    nb=[x for x in a if not x['isBooked']]
    if nb: print('  min non-booked m2',min(x['minAreaPrice'] for x in nb))
    time.sleep(1)
