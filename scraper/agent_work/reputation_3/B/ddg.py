import sys,re,html,subprocess,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for q in sys.argv[1:]:
    r=subprocess.run(['curl','-s','-m','20','-A',UA,'https://html.duckduckgo.com/html/?q='+urllib.parse.quote(q)],capture_output=True,text=True).stdout
    print('>>>',q, len(r))
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',r,re.S):
        u=m.group(1)
        if 'uddg=' in u: u=urllib.parse.unquote(u.split('uddg=')[1].split('&')[0])
        print(' -',html.unescape(re.sub('<[^>]+>','',m.group(2))),'|',u); print('    ',html.unescape(re.sub('<[^>]+>','',m.group(3)))[:250])
    time.sleep(2)
