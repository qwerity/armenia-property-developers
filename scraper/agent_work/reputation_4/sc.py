import sys,re,urllib.request,html,ssl
ctx=ssl.create_default_context();ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
for u in sys.argv[1:]:
    print("==",u)
    try:
        t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20,context=ctx).read().decode('utf8','ignore')
    except Exception as e: print(e); continue
    t=html.unescape(re.sub(r'<[^>]+>',' ',t))
    s=set()
    for m in re.finditer(r'.{0,50}(ՍՊԸ|ՓԲԸ|ԲԲԸ|\bLLC\b|CJSC|ՀՎՀՀ|ООО|ИНН|[Tt]ax ID|«[^»]{2,40}»|"[A-Z][A-Z \-]{3,40}"|©).{0,50}',t):
        x=' '.join(m.group(0).split())
        if x not in s: s.add(x); print(' ',x)
        if len(s)>12: break
