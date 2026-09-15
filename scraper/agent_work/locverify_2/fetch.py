import sys,re,hashlib,os,subprocess,time,html
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D=os.path.dirname(os.path.abspath(__file__))+"/pages"
def get(url):
    fn=D+"/"+hashlib.md5(url.encode()).hexdigest()+".html"
    if not os.path.exists(fn):
        subprocess.run(["curl","-sL","-m","30","--compressed","-A",UA,"-H","Accept: text/html,application/xhtml+xml","-H","Accept-Language: en","-o",fn,url])
        time.sleep(0.6)
    try: return open(fn,encoding="utf-8",errors="ignore").read()
    except: return ""
PAT=[r"!3d(-?\d+\.\d+)!2d(-?\d+\.\d+)",r"@(4\d\.\d{3,}),(4\d\.\d{3,})",r"[?&;](?:q|ll|center|daddr|destination|query)=(4\d\.\d{3,})(?:,|%2C|\s)+(4\d\.\d{3,})",
 r"(?:ll|pt)=(4\d\.\d{3,})(?:,|%2C)(3\d\.\d{3,}|4\d\.\d{3,})",r"lat(?:itude)?\W{1,6}(4\d\.\d{3,})\W{1,40}l(?:ng|on|ong|ongitude)\W{1,6}(4\d\.\d{3,})",
 r"\[\s*(3\d\.\d{4,}|4[0-1]\.\d{4,})\s*,\s*(4[3-6]\.\d{4,})\s*\]",r"(4[0-1]\.\d{4,})\s*,\s*(4[3-6]\.\d{4,})"]
if __name__=="__main__":
    kw=sys.argv[2:] 
    url=sys.argv[1]; t=get(url); t2=html.unescape(t).replace("\\/","/")
    print("LEN",len(t))
    seen=set()
    for p in PAT:
        for m in re.finditer(p,t2):
            s=t2[max(0,m.start()-60):m.end()+20].replace("\n"," ")
            if m.group(0) in seen: continue
            seen.add(m.group(0)); print("COORD",m.group(1),m.group(2),"|",s[:160])
    for m in re.finditer(r"(maps\.google|google\.[a-z.]+/maps|yandex\.[a-z]+/map|goo\.gl/maps|maps\.app\.goo)[^\"'<> ]{0,300}",t2):
        print("MAPURL",m.group(0)[:300])
    txt=re.sub(r"<script.*?</script>|<style.*?</style>"," ",t2,flags=re.S); txt=re.sub(r"<[^>]+>"," ",txt); txt=re.sub(r"\s+"," ",txt)
    for k in kw:
        for m in list(re.finditer(k,txt,flags=re.I))[:6]:
            print("KW",k,"|",txt[max(0,m.start()-120):m.end()+120])
