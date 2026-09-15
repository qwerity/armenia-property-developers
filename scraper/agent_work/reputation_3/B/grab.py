import sys,re,html,subprocess,time,hashlib,os
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PAT=r'.{0,90}(?:ՍՊԸ|ՓԲԸ|ԲԲԸ|ՀՎՀՀ|Հ\.Վ\.Հ\.Հ|LLC|L\.L\.C|CJSC|ООО|ЗАО|ИНН|[Tt]ax ID|TIN|«[^»]{2,40}»|\b\d{8}\b).{0,90}'
for u in sys.argv[1:]:
    fn='pg_'+hashlib.md5(u.encode()).hexdigest()[:10]+'.html'
    if not os.path.exists(fn):
        subprocess.run(['curl','-sL','-m','25','-A',UA,u,'-o',fn]); time.sleep(0.6)
    try: t=open(fn,errors='ignore').read()
    except: print('##',u,'FAIL'); continue
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
    print('##',u,len(t))
    seen=set()
    for m in re.finditer(PAT,t):
        s=m.group(0).strip()
        if s in seen: continue
        seen.add(s); print('   ',s)
        if len(seen)>15: break
