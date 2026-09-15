import sys,re,html,subprocess,time,urllib.parse
UA='Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124 Safari/537.36'
for q in sys.argv[1:]:
    time.sleep(1.1)
    x=subprocess.run(['curl','-s','-m','30','-A',UA,'https://www.bing.com/news/search?q='+urllib.parse.quote(q)+'&format=rss'],capture_output=True,text=True,errors='ignore').stdout
    items=re.findall(r'<item>(.*?)</item>',x,re.S)
    print('###',q,len(items))
    for it in items[:10]:
        g=lambda tag:html.unescape((re.search(rf'<{tag}>(.*?)</{tag}>',it,re.S) or [None,''])[1])
        l=g('link'); m=re.search(r'[?&]url=([^&]+)',l); l=urllib.parse.unquote(m.group(1)) if m else l
        print(' -',g('pubDate')[5:16],'|',g('title')[:130],'|',l)
