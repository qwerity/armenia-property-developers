import json, re, hashlib, os, time, subprocess, sys
from urllib.parse import urlparse, unquote
S='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/locverify_3/'
d=json.load(open('/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.loc_verify_3.json'))
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
last={}
def fn(u): return S+'html/'+hashlib.md5(u.split('#')[0].encode()).hexdigest()+'.html'
def get(u):
    f=fn(u)
    if os.path.exists(f) and os.path.getsize(f)>0: return open(f,errors='ignore').read()
    h=urlparse(u).netloc
    dt=time.time()-last.get(h,0)
    if dt<0.6: time.sleep(0.6-dt)
    last[h]=time.time()
    subprocess.run(['curl','-sL','-m','40','--compressed','-A',UA,'-H','Accept: text/html,application/xhtml+xml','-H','Accept-Language: en','-o',f,u.split('#')[0]])
    return open(f,errors='ignore').read() if os.path.exists(f) else ''
pats=[r'!3d(-?\d+\.\d+)!2d(-?\d+\.\d+)',r'@(4\d\.\d{4,}),(4\d\.\d{4,})',r'[?&;]q=(4\d\.\d+)(?:,|%2C)\s*(4\d\.\d+)',r'll=(4\d\.\d+)(?:,|%2C)(4\d\.\d+)',r'pt=(4\d\.\d+)(?:,|%2C)(4\d\.\d+)',
 r'lat["\']?\s*[:=]\s*["\']?(4\d\.\d{3,})["\']?\s*,\s*["\']?(?:lng|lon|long|longitude)["\']?\s*[:=]\s*["\']?(4\d\.\d{3,})',
 r'latitude["\']?\s*[:=]\s*["\']?(4\d\.\d{3,}).{0,40}?longitude["\']?\s*[:=]\s*["\']?(4\d\.\d{3,})',
 r'\[\s*(4\d\.\d{4,})\s*,\s*(4\d\.\d{4,})\s*\]',r'(4[01]\.\d{4,})\s*,\s*(4[3-6]\.\d{4,})',r'(4[3-6]\.\d{4,})\s*,\s*(4[01]\.\d{4,})']
sel=sys.argv[1:] 
for x in d:
    if sel and x['id'] not in sel: continue
    print('=====',x['id'],x['title'],'|',x['lat'],x['lng'])
    for u in x['sources']:
        t=get(u)
        found=set()
        for p in pats:
            for m in re.finditer(p,unquote(t)):
                found.add((p[:6],m.group(1),m.group(2)))
        embeds=set(re.findall(r'(?:maps\.google|google\.[a-z.]+/maps|yandex\.[a-z]+/(?:map-widget|maps))[^"\'\s<>]{0,300}',t))
        print('  --',u,len(t))
        for f in list(found)[:12]: print('    ',f)
        for e in list(embeds)[:5]: print('     E',e[:250])
