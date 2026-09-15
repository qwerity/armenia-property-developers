import sys,re,html,subprocess,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for q in sys.argv[1:]:
    u='https://www.bing.com/search?format=rss&count=20&q='+urllib.parse.quote(q)
    r=subprocess.run(['curl','-s','-m','20','-A',UA,u],capture_output=True,text=True).stdout
    items=re.findall(r'<item>(.*?)</item>',r,re.S)
    print('>>>',q,len(items))
    for it in items[:15]:
        g=lambda k:(html.unescape(re.search(f'<{k}>(.*?)</{k}>',it,re.S).group(1)) if re.search(f'<{k}>',it) else '')
        print(' -',g('title'),'|',g('link')); print('     ',g('description')[:260])
    time.sleep(2)
