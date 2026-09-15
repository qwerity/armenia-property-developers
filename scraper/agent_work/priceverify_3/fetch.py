import json,subprocess,hashlib,os,sys,time,re,html
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
SP=os.path.dirname(os.path.abspath(__file__))
d=json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.price_verify_3.json'))
urls=sys.argv[1:] or sorted({u for x in d for u in x['source_urls']})
byhost={}
for u in urls: byhost.setdefault(urlparse(u).netloc,[]).append(u)
def fn(u): return os.path.join(SP,'pages',hashlib.md5(u.encode()).hexdigest()[:10])
os.makedirs(SP+'/pages',exist_ok=True)
def text(h):
    h=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>',' ',h)
    h=re.sub(r'(?s)<[^>]+>',' ',h); h=html.unescape(h)
    return re.sub(r'\s+',' ',h)
def run(host):
    for u in byhost[host]:
        f=fn(u)
        r=subprocess.run(['curl','-sL','--compressed','-m','40','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36','-H','Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','-H','Accept-Language: en','-o',f+'.html','-w','%{http_code} %{url_effective}',u],capture_output=True,text=True)
        try: h=open(f+'.html',errors='ignore').read()
        except: h=''
        open(f+'.txt','w').write(text(h))
        print(r.stdout, len(h), u, os.path.basename(f), flush=True)
        time.sleep(0.7)
with ThreadPoolExecutor(12) as ex: list(ex.map(run,byhost))
