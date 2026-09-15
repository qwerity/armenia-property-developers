import sys, json, time, urllib.parse, urllib.request, os, hashlib, math
S=os.path.dirname(os.path.abspath(__file__))+'/'
LOCK=S+'nom.last'
def q(query, extra=''):
  key=hashlib.md5((query+extra).encode()).hexdigest()
  cf=S+'nomcache/'+key+'.json'; os.makedirs(S+'nomcache',exist_ok=True)
  if os.path.exists(cf): return json.load(open(cf))
  try: last=float(open(LOCK).read())
  except: last=0
  w=4.2-(time.time()-last)
  if w>0: time.sleep(w)
  url='https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode({'q':query,'format':'jsonv2','countrycodes':'am','addressdetails':1,'limit':6})+extra
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'armenia-new-builds-map/1.0'}),timeout=30).read()
  open(LOCK,'w').write(str(time.time()))
  res=json.loads(r); json.dump(res,open(cf,'w')); return res
if __name__=='__main__':
  ref=None
  args=sys.argv[1:]
  if args and args[0].startswith('@'):
    a,b=args[0][1:].split(','); ref=(float(a),float(b)); args=args[1:]
  for query in args:
    print('#',query)
    for x in q(query):
      la,ln=float(x['lat']),float(x['lon'])
      dd=''
      if ref: dd=' d=%dm'%(6371000*math.hypot(math.radians(la-ref[0]),math.radians(ln-ref[1])*math.cos(math.radians(la))))
      print('  %.6f,%.6f %s %s |%s%s'%(la,ln,x['category'],x['type'],x['display_name'][:120],dd))
