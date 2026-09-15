import sys,json,time,os,urllib.parse,urllib.request,hashlib
S=os.path.dirname(os.path.abspath(__file__))+'/'
os.makedirs(S+'nom',exist_ok=True)
lock=S+'nom/.last'
for q in sys.argv[1:]:
    f=S+'nom/'+hashlib.md5(q.encode()).hexdigest()+'.json'
    if os.path.exists(f): r=json.load(open(f))
    else:
        try: dt=time.time()-float(open(lock).read())
        except: dt=99
        if dt<4.2: time.sleep(4.2-dt)
        url='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':q,'format':'jsonv2','countrycodes':'am','addressdetails':1,'limit':5})
        r=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'armenia-new-builds-map/1.0'}),timeout=30))
        open(lock,'w').write(str(time.time())); json.dump(r,open(f,'w'))
    print('#',q)
    for x in r: print('  ',x['lat'],x['lon'],x.get('type'),'|',x['display_name'][:140])
