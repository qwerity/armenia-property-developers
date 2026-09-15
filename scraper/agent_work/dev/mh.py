import json, subprocess, time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def get(u, data=None):
    cmd=["curl","-s","-m","20","-A",UA,"-H","Accept: application/json"]
    if data is not None: cmd+=["-X","POST","-H","Content-Type: application/json","-d",json.dumps(data)]
    time.sleep(0.5)
    r=subprocess.run(cmd+[u],capture_output=True,text=True).stdout
    try: return json.loads(r)
    except Exception: return r[:200]
ids=[b['id'] for b in json.load(open('mh_builders.json'))]
out=[]
for i in ids:
    d=get(f"https://myhome.am/API/v1/builders/{i}")
    if isinstance(d,dict):
        b=get("https://myhome.am/API/v1/buildings/published",{"builderId":i,"pageNumber":1,"pageSize":100})
        d['buildings']=b
    out.append(d)
    print(i, d.get('builderBrandName',{}).get('eng') if isinstance(d,dict) else d, d.get('webSite') if isinstance(d,dict) else '', str(d.get('buildings'))[:150] if isinstance(d,dict) else '')
json.dump(out,open('mh_details.json','w'),ensure_ascii=False,indent=1)
