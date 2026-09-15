import sys,urllib.request,re,html,time
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124 Safari/537.36'})
    return urllib.request.urlopen(req,timeout=30).read().decode('utf8','ignore')
terms=sys.argv[1].split('|')
for u in sys.argv[2:]:
    try: t=fetch(u)
    except Exception as e: print('ERR',u,e); continue
    title=re.search(r'<title>(.*?)</title>',t,re.S)
    s=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S))))
    print('=====',u,'\n  T:',html.unescape(title.group(1)).strip() if title else '')
    last=-10**9
    for m in re.finditer('|'.join(map(re.escape,terms)),s):
        if m.start()-last<600: continue
        last=m.start(); print('  ..',s[max(0,m.start()-300):m.end()+500])
    time.sleep(1)
