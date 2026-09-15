import sys,re,html,subprocess,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
WP=['armlur.am','www.aravot.am','168.am','fip.am','factor.am']
def get(u): return subprocess.run(['curl','-sL','-m','20','-A',UA,u],capture_output=True,text=True).stdout
for q in sys.argv[1:]:
    qq=urllib.parse.quote(q)
    print('>>>',q)
    for s in WP:
        r=get(f'https://{s}/?s={qq}&sentence=1&feed=rss2')
        for it in re.findall(r'<item>(.*?)</item>',r,re.S)[:8]:
            g=lambda k:(html.unescape(re.sub(r'<!\[CDATA\[|\]\]>','',re.search(f'<{k}>(.*?)</{k}>',it,re.S).group(1))) if re.search(f'<{k}>',it) else '')
            desc=re.sub('<[^>]+>','',g('description'))
            if q.lower() not in (g('title')+desc+g('content:encoded')).lower(): continue
            print('  [%s] %s | %s | %s'%(s,g('pubDate')[5:16],g('title'),g('link')))
            i=(desc).lower().find(q.lower()); print('       ',desc[max(0,i-120):i+160].replace('\n',' '))
        time.sleep(0.5)
    r=get(f'https://www.azatutyun.am/s?k={qq}')
    for m in re.finditer(r'<a href="(/a/[^"]+)"[^>]*title="([^"]+)"',r):
        print('  [azatutyun]',html.unescape(m.group(2)),'| https://www.azatutyun.am'+m.group(1))
    time.sleep(0.5)
