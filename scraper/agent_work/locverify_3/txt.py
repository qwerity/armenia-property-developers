import sys,re,html,hashlib,os,subprocess
S=os.path.dirname(os.path.abspath(__file__))+'/'
u=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else None; w=int(sys.argv[3]) if len(sys.argv)>3 else 200
f=S+'html/'+hashlib.md5(u.split('#')[0].encode()).hexdigest()+'.html'
if not os.path.exists(f) or os.path.getsize(f)==0:
    subprocess.run(['curl','-sL','-m','40','--compressed','-A',"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",'-H','Accept: text/html','-H','Accept-Language: en','-o',f,u.split('#')[0]])
raw=open(f,errors='ignore').read()
if len(sys.argv)>4 and sys.argv[4]=='raw': t=raw
else:
    t=re.sub(r'<script.*?</script>|<style.*?</style>',' ',raw,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
if not pat: print(t[:w]); sys.exit()
for m in list(re.finditer(pat,t,flags=re.I))[:15]:
    print('>>',t[max(0,m.start()-w):m.end()+w])
