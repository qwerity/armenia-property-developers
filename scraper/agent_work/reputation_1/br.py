import sys,re,html,subprocess,time,urllib.parse
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def get(u):
    time.sleep(1.0)
    return subprocess.run(['curl','-sL','-m','30','-A',UA,u],capture_output=True,text=True,errors='ignore').stdout
for q in sys.argv[1:]:
    x=get('https://www.bing.com/search?format=rss&count=15&q='+urllib.parse.quote(q))
    items=re.findall(r'<item>(.*?)</item>',x,re.S)
    print('###',q,len(items))
    for it in items[:15]:
        g=lambda tag:html.unescape((re.search(rf'<{tag}>(.*?)</{tag}>',it,re.S) or [None,''])[1])
        print(' -',g('title'),'|',g('link'),'|',re.sub(r'<[^>]+>','',g('description'))[:200])
