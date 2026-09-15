import sys,re,html,subprocess,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for q in sys.argv[1:]:
    u='https://news.google.com/rss/search?q='+urllib.parse.quote(q)+'&hl=hy&gl=AM&ceid=AM:hy'
    r=subprocess.run(['curl','-s','-m','20','-A',UA,u],capture_output=True,text=True).stdout
    items=re.findall(r'<item>(.*?)</item>',r,re.S)
    print('>>>',q,len(items))
    for it in items[:12]:
        t=html.unescape(re.search(r'<title>(.*?)</title>',it,re.S).group(1))
        l=re.search(r'<link>(.*?)</link>',it,re.S).group(1)
        d=re.search(r'<pubDate>(.*?)</pubDate>',it,re.S); d=d.group(1)[5:16] if d else ''
        print(' -',d,'|',t,'|',l[:120])
    time.sleep(1.5)
