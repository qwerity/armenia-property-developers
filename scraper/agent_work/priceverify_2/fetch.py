import json,sys,os,re,time,hashlib,subprocess,html
from urllib.parse import urlparse
SP=os.path.dirname(os.path.abspath(__file__))
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def fname(u): return os.path.join(SP,'pages',re.sub(r'[^a-zA-Z0-9]+','_',u.split('#')[0])[:150])
def fetch(u,force=False):
    os.makedirs(os.path.join(SP,'pages'),exist_ok=True)
    f=fname(u)
    if os.path.exists(f+'.html') and not force: return f
    r=subprocess.run(['curl','-sL','--compressed','-m','40','-A',UA,'-H','Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','-H','Accept-Language: en-US,en;q=0.9','-o',f+'.html','-w','%{http_code} %{size_download}',u.split('#')[0]],capture_output=True,text=True)
    print(r.stdout,u,file=sys.stderr)
    t=open(f+'.html',errors='ignore').read()
    t=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',t)
    t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'[ \t\r\f]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    open(f+'.txt','w').write(t)
    return f
if __name__=='__main__':
    last={}
    for u in sys.argv[1:]:
        h=urlparse(u).netloc
        if h in last and time.time()-last[h]<1.0: time.sleep(1.0)
        fetch(u); last[h]=time.time()
