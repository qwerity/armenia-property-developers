import sys,json,os,time,urllib.request,urllib.parse,hashlib
D=os.path.dirname(os.path.abspath(__file__)); C=D+"/nomcache"; os.makedirs(C,exist_ok=True); L=D+"/nom.lock"
def q(s,extra=""):
    url="https://nominatim.openstreetmap.org/search?"+urllib.parse.urlencode({"q":s,"format":"jsonv2","countrycodes":"am","addressdetails":1,"limit":5})+extra
    fn=C+"/"+hashlib.md5(url.encode()).hexdigest()+".json"
    if os.path.exists(fn): return json.load(open(fn))
    try: last=float(open(L).read())
    except: last=0
    w=4.2-(time.time()-last)
    if w>0: time.sleep(w)
    r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"armenia-new-builds-map/1.0"}),timeout=30).read()
    open(L,"w").write(str(time.time()))
    d=json.loads(r); json.dump(d,open(fn,"w")); return d
if __name__=="__main__":
    for s in sys.argv[1:]:
        print("Q:",s)
        for x in q(s): print("  ",x["lat"],x["lon"],x.get("addresstype"),"|",x["display_name"][:140])
def rev(lat,lon,zoom=18):
    url="https://nominatim.openstreetmap.org/reverse?"+urllib.parse.urlencode({"lat":lat,"lon":lon,"format":"jsonv2","zoom":zoom,"addressdetails":1})
    fn=C+"/"+hashlib.md5(url.encode()).hexdigest()+".json"
    if os.path.exists(fn): return json.load(open(fn))
    try: last=float(open(L).read())
    except: last=0
    w=4.2-(time.time()-last)
    if w>0: time.sleep(w)
    r=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"armenia-new-builds-map/1.0"}),timeout=30).read()
    open(L,"w").write(str(time.time()))
    d=json.loads(r); json.dump(d,open(fn,"w")); return d
