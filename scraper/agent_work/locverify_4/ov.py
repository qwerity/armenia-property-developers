import sys,json,time,urllib.request,urllib.parse
q=sys.argv[1]
for ep in ['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter']:
  try:
    r=urllib.request.urlopen(urllib.request.Request(ep,data=urllib.parse.urlencode({'data':'[out:json][timeout:40];'+q}).encode(),headers={'User-Agent':'armenia-new-builds-map/1.0'}),timeout=60).read()
    for e in json.loads(r)['elements']:
      t=e.get('tags',{}); c=e.get('center') or {'lat':e.get('lat'),'lon':e.get('lon')}
      print(e['type'],t.get('name'),t.get('addr:street'),t.get('addr:housenumber'),t.get('building'),round(c['lat'],6),round(c['lon'],6))
    break
  except Exception as ex: print('ERR',ep,ex); time.sleep(3)
