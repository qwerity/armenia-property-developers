import json,sys,os
p="/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_3/web_E.json"
arr=json.load(open(p)) if os.path.exists(p) else []
new=json.load(open(sys.argv[1]))
if isinstance(new,dict): new=[new]
for n in new:
    arr=[a for a in arr if a["developer"]!=n["developer"]]+[n]
json.dump(arr,open(p,"w"),ensure_ascii=False,indent=1)
print(len(arr),[a["developer"] for a in arr])
