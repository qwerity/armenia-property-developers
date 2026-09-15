import sys,re,subprocess,html,urllib.parse,time
for q in sys.argv[1:]:
    u='https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q='+urllib.parse.quote(q)
    r=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0',u],capture_output=True).stdout.decode('utf8','ignore')
    items=re.findall(r'<item>(.*?)</item>',r,re.S)
    print('##',q,len(items))
    for it in items[:12]:
        g=lambda k: html.unescape((re.search(r'<%s[^>]*>(.*?)</%s>'%(k,k),it,re.S) or [None,''])[1])
        print('  -',g('pubDate')[5:16],'|',g('title')[:140],'|',g('link')[:200])
    time.sleep(1.5)
