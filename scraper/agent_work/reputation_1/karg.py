import sys,re,html,subprocess,time,urllib.parse
UA='Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124 Safari/537.36'
def get(u):
    time.sleep(0.8)
    return subprocess.run(['curl','-sL','-m','30','-A',UA,u],capture_output=True,text=True,errors='ignore').stdout
def txt(h):
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
mode=sys.argv[1]
for q in sys.argv[2:]:
    if mode=='s':
        h=get('https://karg.am/search?q='+urllib.parse.quote(q)+'&lang=hy')
        print('###',q)
        seen=set()
        for m in re.finditer(r'href="/company/(\d{8})[^"]*"[^>]*>(.*?)</a>',h,re.S):
            if m.group(1) in seen: continue
            seen.add(m.group(1)); print('  ',m.group(1),html.unescape(re.sub(r'<[^>]+>|\s+',' ',m.group(2))).strip()[:150])
        if not seen: print('   none', txt(h)[:300] if len(h)<3000 else '')
    else:
        t=txt(get('https://karg.am/company/'+q+'?lang=hy'))
        i=t.find(q); print('##',q, t[max(0,i-300):i+900])
