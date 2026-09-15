import sys, hashlib, os, time, re, json, subprocess
from urllib.parse import urljoin
H={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.9,hy;q=0.8,ru;q=0.7"}
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"cache")
def get(url, refresh=False):
    fn=os.path.join(D,hashlib.md5(url.encode()).hexdigest())
    if os.path.exists(fn) and not refresh:
        return open(fn,encoding="utf-8",errors="replace").read()
    time.sleep(0.5)
    cmd=["curl","-sSL","-k","--compressed","-m","40","-w","\n__STATUS__%{http_code}"]
    for k,v in H.items(): cmd+=["-H",f"{k}: {v}"]
    p=subprocess.run(cmd+[url],capture_output=True)
    out=p.stdout.decode("utf-8","replace")
    m=re.search(r"\n__STATUS__(\d+)$",out)
    code=int(m.group(1)) if m else 0
    body=out[:m.start()] if m else out
    t=body if 0<code<400 else f"__HTTP_{code}__ {p.stderr.decode()[:300]} "+body[:2000]
    open(fn,"w",encoding="utf-8").write(t)
    return t
def text(html):
    html=re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>"," ",html)
    t=re.sub(r"(?s)<[^>]+>"," ",html)
    import html as h
    return re.sub(r"\s+"," ",h.unescape(t)).strip()
def links(html,base):
    return sorted(set(urljoin(base,m) for m in re.findall(r'href=["\']([^"\'#]+)',html)))
if __name__=="__main__":
    mode=sys.argv[1]; url=sys.argv[2]
    h=get(url)
    if mode=="raw": print(h[:int(sys.argv[3]) if len(sys.argv)>3 else 100000])
    elif mode=="text": print(text(h)[:int(sys.argv[3]) if len(sys.argv)>3 else 20000])
    elif mode=="links":
        pat=sys.argv[3] if len(sys.argv)>3 else ""
        for l in links(h,url):
            if re.search(pat,l) and len(l)<200 and not re.search(r'\.(css|js|png|jpe?g|webp|svg|ico|woff2?)(\?|$)|wp-json|xmlrpc|/feed/|parastorage|googleapis|gstatic',l): print(l)
    elif mode=="grep":
        for m in re.finditer(sys.argv[3],h): print(h[max(0,m.start()-150):m.end()+150].replace("\n"," ")); print("--")
