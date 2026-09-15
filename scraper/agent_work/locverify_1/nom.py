import sys,json,subprocess,time,urllib.parse,os
last="nom_last"
for q in sys.argv[1:]:
    try:
        dt=time.time()-float(open(last).read())
        if dt<4.2: time.sleep(4.2-dt)
    except: pass
    url="https://nominatim.openstreetmap.org/search?"+urllib.parse.urlencode({"q":q,"format":"jsonv2","countrycodes":"am","addressdetails":1,"limit":5})
    r=subprocess.run(["curl","-s","-m","30","-A","armenia-new-builds-map/1.0",url],capture_output=True,text=True).stdout
    open(last,"w").write(str(time.time()))
    print("###",q)
    try:
        for x in json.loads(r): print("  ",x["lat"],x["lon"],x["type"],"|",x["display_name"][:150])
    except Exception as e: print("ERR",r[:200])
