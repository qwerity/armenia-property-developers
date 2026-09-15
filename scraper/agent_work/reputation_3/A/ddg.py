import sys,re,subprocess,html,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for q in sys.argv[1:]:
    r=subprocess.run(['curl','-sL','-m','25','-A',UA,'--data-urlencode','q='+q,'https://html.duckduckgo.com/html/'],capture_output=True).stdout.decode('utf8','ignore')
    print('##',q)
    if 'anomaly' in r or 'captcha' in r.lower(): print('  BLOCKED'); continue
    items=re.findall(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',r,re.S)
    for h,t,s in items[:10]:
        m=re.search(r'uddg=([^&]+)',h); u=urllib.parse.unquote(m.group(1)) if m else h
        cl=lambda x: html.unescape(re.sub(r'<[^>]+>','',x)).strip()
        print('  -',cl(t)[:100],'|',u); print('     ',cl(s)[:250])
    time.sleep(2)
