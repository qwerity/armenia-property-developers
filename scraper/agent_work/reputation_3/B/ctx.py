import sys,re,html,hashlib,subprocess,os,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
u=sys.argv[1]; keys=sys.argv[2:]
fn='pg_'+hashlib.md5(u.encode()).hexdigest()[:10]+'.html'
if not os.path.exists(fn): subprocess.run(['curl','-sL','-m','25','-A',UA,u,'-o',fn]); time.sleep(0.5)
t=open(fn,errors='ignore').read()
tm=re.search(r'<title>(.*?)</title>',t,re.S); dt=re.search(r'(?:datePublished|article:published_time)["\']?\s*(?:content=|:)\s*["\']([^"\']+)',t)
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
print('##',u,'|',html.unescape(tm.group(1).strip()) if tm else '','|',dt.group(1) if dt else '')
n=0
for k in keys:
    for m in re.finditer(re.escape(k),t,re.I):
        print('  ..',t[max(0,m.start()-300):m.start()+400]); n+=1
        if n>=4: break
