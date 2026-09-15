import sys,urllib.request,urllib.parse,re,html,time
q=' '.join(sys.argv[1:])
req=urllib.request.Request('https://html.duckduckgo.com/html/',data=urllib.parse.urlencode({'q':q}).encode(),headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'})
t=urllib.request.urlopen(req,timeout=25).read().decode('utf8','ignore')
for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',t,re.S):
    u=m.group(1)
    if 'uddg=' in u: u=urllib.parse.unquote(u.split('uddg=')[1].split('&')[0])
    print('-',html.unescape(re.sub('<[^>]+>','',m.group(2))),'|',u); print('   ',html.unescape(re.sub('<[^>]+>','',m.group(3)))[:300])
