import re,sys,subprocess,urllib.parse,time,html
def ddg(q):
    time.sleep(1.2)
    h=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','--data-urlencode','q='+q,'https://html.duckduckgo.com/html/'],capture_output=True,text=True).stdout
    out=[]
    for m in re.finditer(r'class="result__a" href="([^"]+)">(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',h,re.S):
        u=m.group(1)
        if 'uddg=' in u: u=urllib.parse.unquote(re.search(r'uddg=([^&]+)',u).group(1))
        cl=lambda s: html.unescape(re.sub(r'<[^>]+>','',s)).strip()
        out.append((u,cl(m.group(2)),cl(m.group(3))))
    if not out: out=[('NO RESULTS',str(len(h)),h[:200])]
    return out
for q in sys.argv[1:]:
    print('##',q)
    for u,t,s in ddg(q)[:8]: print(' -',u,'|',t[:90],'|',s[:220])
