import sys,urllib.parse,urllib.request,re,html,time
def search(q):
    url='https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/124 Safari/537.36'})
    t=urllib.request.urlopen(req,timeout=30).read().decode('utf8','ignore')
    out=[]
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',t,re.S):
        u=m.group(1)
        if 'uddg=' in u: u=urllib.parse.unquote(u.split('uddg=')[1].split('&')[0])
        out.append((u,html.unescape(re.sub('<[^>]+>','',m.group(2))),html.unescape(re.sub('<[^>]+>','',m.group(3)))))
    if not out: print('NO RESULTS / len',len(t), 'captcha' if 'anomaly' in t or 'captcha' in t.lower() else '')
    return out
for q in sys.argv[1:]:
    print('#####',q)
    for u,ti,sn in search(q)[:8]: print(' -',ti,'|',u,'\n    ',sn[:300])
    time.sleep(2)
