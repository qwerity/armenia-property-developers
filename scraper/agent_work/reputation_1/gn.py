import sys,re,html,subprocess,time,urllib.parse
from gdec import dec
import os
DEC=os.environ.get('DEC','0')=='1'
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def get(u):
    time.sleep(1.0)
    return subprocess.run(['curl','-sL','-m','30','-A',UA,u],capture_output=True,text=True,errors='ignore').stdout
hl={'hy':'hl=hy&gl=AM&ceid=AM:hy','hx':'hl=en-US&gl=US&ceid=US:en','ru':'hl=ru&gl=AM&ceid=AM:ru','en':'hl=en-US&gl=US&ceid=US:en'}
lang=sys.argv[1]
for q in sys.argv[2:]:
    x=get('https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&'+hl[lang])
    items=re.findall(r'<item>(.*?)</item>',x,re.S)
    print('###',q,len(items))
    for it in items[:12]:
        t=html.unescape(re.search(r'<title>(.*?)</title>',it,re.S).group(1))
        l=re.search(r'<link>(.*?)</link>',it,re.S).group(1)
        d=(re.search(r'<pubDate>(.*?)</pubDate>',it) or [None,''])[1]
        print(' -',d[5:16],'|',t,'|',(dec(l) if DEC else l[-30:]))
