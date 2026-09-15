import sys,re,html,hashlib
url=sys.argv[1]; kw=sys.argv[2:]
t=open("pages/"+hashlib.md5(url.encode()).hexdigest()+".html",encoding="utf-8",errors="ignore").read()
t=re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>"," ",t)
t=html.unescape(re.sub(r"<[^>]+>"," ",t)); t=re.sub(r"\s+"," ",t)
for k in kw:
    for m in re.finditer(k,t,re.I):
        print("..",t[max(0,m.start()-150):m.end()+150])
