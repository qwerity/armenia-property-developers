import sys,re,html,subprocess,time
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
u=sys.argv[1]; pats=sys.argv[2:]
time.sleep(0.6)
h=subprocess.run(['curl','-sL','-m','30','-A',UA,u],capture_output=True,text=True,errors='ignore').stdout
t=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
print('##',u,len(t)); 
m=re.search(r'<title>(.*?)</title>',h,re.S); print('TITLE:',html.unescape(m.group(1)).strip() if m else '')
seen=0
for p in pats:
    for k in re.finditer(p,t,re.I):
        if k.start()<seen: continue
        print('  ..',t[max(0,k.start()-350):k.start()+450]); seen=k.start()+450
