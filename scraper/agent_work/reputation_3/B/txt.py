import sys,re,html,hashlib,subprocess,os,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
u=sys.argv[1]; a=int(sys.argv[2]) if len(sys.argv)>2 else 0; b=int(sys.argv[3]) if len(sys.argv)>3 else 3000
fn='pg_'+hashlib.md5(u.encode()).hexdigest()[:10]+'.html'
if not os.path.exists(fn): subprocess.run(['curl','-sL','-m','25','-A',UA,u,'-o',fn]); time.sleep(0.5)
t=open(fn,errors='ignore').read()
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
print(t[a:b])
