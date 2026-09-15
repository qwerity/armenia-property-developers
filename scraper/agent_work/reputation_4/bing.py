import sys,urllib.parse,urllib.request,re,html,time
def search(q):
    url='https://www.bing.com/search?q='+urllib.parse.quote(q)+'&setlang=en&cc=AM'
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36','Accept-Language':'en-US,en;q=0.8'})
    t=urllib.request.urlopen(req,timeout=30).read().decode('utf8','ignore')
    out=[]
    for m in re.finditer(r'<li class="b_algo".*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>(.*?)</li>',t,re.S):
        sn=re.search(r'<p[^>]*>(.*?)</p>',m.group(3),re.S)
        out.append((html.unescape(m.group(1)),html.unescape(re.sub('<[^>]+>','',m.group(2))),html.unescape(re.sub('<[^>]+>','',sn.group(1))) if sn else ''))
    if not out: print('NO RESULTS len',len(t),'captcha' if 'captcha' in t.lower() else '')
    return out
for q in sys.argv[1:]:
    print('#####',q)
    for u,ti,sn in search(q)[:8]: print(' -',ti,'|',u,'\n    ',sn[:300])
    time.sleep(2.5)
