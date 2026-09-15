import sys,re,json,html
S='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/locverify_4/'
um=json.load(open(S+'urlmap.json'))
u=sys.argv[1]; pat=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 200
t=open(um.get(u,u),errors='ignore').read()
if len(sys.argv)>4: t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
n=0
for m in re.finditer(pat,t,flags=re.I):
  print('...',t[max(0,m.start()-w):m.end()+w].replace('\n',' '),'\n'); n+=1
  if n>8: break
