import json, hashlib, os, time, subprocess, urllib.parse, collections, threading
S='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/locverify_4/'
d=json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.loc_verify_4.json'))
urls=sorted({u.split('#')[0] for x in d for u in x['sources']})
byhost=collections.defaultdict(list)
for u in urls: byhost[urllib.parse.urlparse(u).netloc].append(u)
def fn(u): return S+'pages/'+hashlib.md5(u.encode()).hexdigest()+'.html'
def run(host):
  for u in byhost[host]:
    f=fn(u)
    if os.path.exists(f) and os.path.getsize(f)>500: continue
    subprocess.run(['curl','-sL','--compressed','-m','40','-o',f,'-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36','-H','Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','-H','Accept-Language: en',u])
    time.sleep(0.7)
ts=[threading.Thread(target=run,args=(h,)) for h in byhost]
[t.start() for t in ts];[t.join() for t in ts]
json.dump({u:fn(u) for u in urls},open(S+'urlmap.json','w'),indent=1)
for u in urls: print(os.path.getsize(fn(u)) if os.path.exists(fn(u)) else -1, u)
