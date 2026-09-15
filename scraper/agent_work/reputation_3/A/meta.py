import sys,re,subprocess,html,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
kw=[k for k in sys.argv[1:] if not k.startswith('http')]
for u in [a for a in sys.argv[1:] if a.startswith('http')]:
    t=subprocess.run(['curl','-sL','-m','25','-A',UA,u],capture_output=True).stdout.decode('utf8','ignore')
    ti=re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]*)"',t) or re.search(r'<title>(.*?)</title>',t,re.S)
    d=re.search(r'(?:datePublished|article:published_time|pubdate|dateCreated)["\']?\s*(?:content=|:)\s*["\']([0-9T:\-\.+ ]{10,})',t)
    print('==',u); print('  T:',html.unescape(ti.group(1)).strip()[:200] if ti else None,'| D:',d.group(1)[:10] if d else None)
    b=re.sub(r'<script.*?</script>|<style.*?</style>',' ',t,flags=re.S);b=html.unescape(re.sub(r'<[^>]+>',' ',b));b=re.sub(r'\s+',' ',b)
    for k in kw:
        for m in list(re.finditer(re.escape(k),b))[:3]:
            print('  ['+k+']',b[max(0,m.start()-150):m.end()+150])
    time.sleep(0.5)
