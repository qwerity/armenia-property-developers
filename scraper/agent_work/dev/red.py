import re, json, subprocess, time
from fetch import fetch, text
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
projs=[]
for p in range(1,8):
    time.sleep(0.6)
    r=subprocess.run(["curl","-s","-m","20","-A",UA,"-H","Accept: application/json",f"https://redgroup.am/api/projects?page={p}"],capture_output=True,text=True).stdout
    try: d=json.loads(r)
    except Exception: print('fail',p,r[:200]); break
    projs+=d['data']
    if not d['links']['next']: break
print(len(projs))
out=[]
for pr in projs:
    st,fu,t=fetch(f"https://www.redinvest.am/en/developers/{pr['id']}")
    x=text(t)
    dev=re.search(r"Developer:\s*(.{3,60}?)\s+(?:Designer|Contractor|Start|Exclusive|Partner|Builder|Sales|Construction|Details)",x)
    out.append(dict(id=pr['id'],title=pr['title'],address=pr.get('address'),developer=dev.group(1) if dev else None))
    print(out[-1])
json.dump(out,open('red.json','w'),ensure_ascii=False,indent=1)
