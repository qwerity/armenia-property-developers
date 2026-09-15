import re,sys
for f in sys.argv[2:]:
  t=open(f,errors='ignore').read(); t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
  import html; t=html.unescape(t); t=re.sub(r'\s+',' ',t)
  for m in re.finditer(r'.{0,120}('+sys.argv[1]+').{0,120}',t): print(f[:40],':',m.group(0))
