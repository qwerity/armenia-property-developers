# usage: gn2.py lang "query" "title-regex-to-decode"
import sys,re,html,subprocess,time,urllib.parse
from gdec import dec
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
hl={'ru':'hl=ru&gl=AM&ceid=AM:ru','en':'hl=en-US&gl=US&ceid=US:en'}
lang,q=sys.argv[1],sys.argv[2]; pat=sys.argv[3] if len(sys.argv)>3 else None
time.sleep(1)
x=subprocess.run(['curl','-sL','-m','30','-A',UA,'https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&'+hl[lang]],capture_output=True,text=True).stdout
items=re.findall(r'<item>(.*?)</item>',x,re.S)
print('###',q,len(items))
for it in items[:25]:
    t=html.unescape(re.search(r'<title>(.*?)</title>',it,re.S).group(1))
    l=re.search(r'<link>(.*?)</link>',it,re.S).group(1)
    d=(re.search(r'<pubDate>(.*?)</pubDate>',it) or [None,''])[1]
    u=dec(l) if pat and re.search(pat,t,re.I) else ''
    print(' -',d[5:16],'|',t,'|',u)
