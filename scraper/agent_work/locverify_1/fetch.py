import sys,re,subprocess,hashlib,os,html,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def fetch(url):
    fn="pages/"+hashlib.md5(url.encode()).hexdigest()+".html"
    if not os.path.exists(fn) or os.path.getsize(fn)==0:
        subprocess.run(["curl","-sL","-m","40","-k","-A",UA,"-H","Accept: text/html,application/xhtml+xml","-H","Accept-Language: en","--compressed","-o",fn,url])
        time.sleep(0.6)
    try: return open(fn,encoding="utf-8",errors="ignore").read()
    except: return ""
pats=[r"!2d(-?\d+\.\d+)!3d(-?\d+\.\d+)",r"!3d(-?\d+\.\d+)!2d(-?\d+\.\d+)",r"@(4\d\.\d{3,}),(4\d\.\d{3,})",r"[?&;](?:q|ll|center|daddr|destination|query)=(4\d\.\d{3,})(?:,|%2C)\s*(4\d\.\d{3,})",
 r"(?:ll|pt)=(4\d\.\d{3,})(?:,|%2C)(4\d\.\d{3,})",r"lat\"?'?\s*[:=]\s*\"?'?(4\d\.\d{3,})[\s\S]{0,40}?(?:lng|lon)\w*\"?'?\s*[:=]\s*\"?'?(4\d\.\d{3,})",
 r"latitude\"?\s*[:=]\s*\"?(4\d\.\d{3,})[\s\S]{0,60}?longitude\"?\s*[:=]\s*\"?(4\d\.\d{3,})",r"\[\s*(4\d\.\d{4,})\s*,\s*(4\d\.\d{4,})\s*\]",r"LatLng\(\s*(4\d\.\d{3,})\s*,\s*(4\d\.\d{3,})"]
for url in sys.argv[1:]:
    t=fetch(url); u=html.unescape(urllib.parse.unquote(t))
    print("=====",url,len(t))
    seen=set()
    for p in pats:
        for m in re.finditer(p,u,re.I):
            s=u[max(0,m.start()-60):m.end()+20].replace("\n"," ")
            k=(m.group(1),m.group(2))
            if k in seen: continue
            seen.add(k); print("  COORD",k,"|",s[:200])
    for m in re.finditer(r"(maps\.google|google\.[a-z.]+/maps|goo\.gl/maps|maps\.app\.goo\.gl|yandex\.[a-z]+/map)[^\"'<> ]*",u):
        if m.group(0) not in seen: seen.add(m.group(0)); print("  MAPLINK",m.group(0)[:250])
