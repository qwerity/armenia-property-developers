import re,urllib.request,html,ssl,sys
ctx=ssl._create_unverified_context()
def get(u):
  t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Macintosh) Chrome/126','Accept-Language':'hy,en'}),timeout=25,context=ctx).read().decode('utf8','ignore')
  t=html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)); return ' '.join(re.sub(r'<[^>]+>',' ',t).split())
keys=sys.argv[1].split('|'); w=int(sys.argv[2])
for u in sys.argv[3:]:
  print('==',u)
  try: t=get(u)
  except Exception as e: print(e); continue
  n=0
  for k in keys:
    for m in re.finditer(re.escape(k),t):
      print('  ['+k+']',t[max(0,m.start()-w):m.start()+w]); n+=1; break
  if not n: print(' NOKEY',t[:600])
