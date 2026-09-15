import re,html,sys
keys=sys.argv[1].split('|')
for f in sys.argv[2:]:
  t=open(f,encoding='utf8',errors='ignore').read()
  t=' '.join(html.unescape(re.sub(r'<[^>]+>',' ',re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S))).split())
  for k in keys:
    for m in re.finditer(re.escape(k),t,re.I):
      print(f.split('/')[-1],'[',k,']',t[max(0,m.start()-200):m.start()+250]);break
