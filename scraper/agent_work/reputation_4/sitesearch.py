import sys,urllib.parse,urllib.request,re,html,time
from txt import txt
SITES={
 'azatutyun':'https://www.azatutyun.am/s?k={q}',
 'armlur':'https://armlur.am/?s={q}',
 'aravot':'https://www.aravot.am/?s={q}',
 '168':'https://168.am/?s={q}',
 'factor':'https://factor.am/?s={q}',
 'shamshyan':'https://shamshyan.com/hy/search?q={q}',
 'hraparak':'https://hraparak.am/?s={q}',
 'infocom':'https://infocom.am/?s={q}',
 'mediamax':'https://mediamax.am/am/search/?q={q}',
}
def fetch(u):
    req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124 Safari/537.36'})
    return urllib.request.urlopen(req,timeout=30).read().decode('utf8','ignore')
def run(term,sites):
    for s in sites:
        u=SITES[s].format(q=urllib.parse.quote(term))
        try: t=fetch(u)
        except Exception as e: print(f'  [{s}] ERR {e}'); continue
        links=set()
        for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',t,re.S):
            a=html.unescape(re.sub(r'<[^>]+>',' ',m.group(2)))
            a=re.sub(r'\s+',' ',a).strip()
            if term.lower() in a.lower() or any(w.lower() in a.lower() for w in term.split() if len(w)>4):
                links.add((a[:160],m.group(1)))
        
        body=txt('/tmp/_x.html') if False else re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S))))
        n=body.lower().count(term.lower())
        print(f'  [{s}] hits={n}')
        for a,l in list(links)[:8]: print('     -',a,'|',l)
        time.sleep(1)
if __name__=='__main__':
    sites=sys.argv[1].split(',') if sys.argv[1]!='all' else list(SITES)
    for term in sys.argv[2:]:
        print('####',term); run(term,sites)
