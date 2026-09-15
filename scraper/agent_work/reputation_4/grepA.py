import sys,re,html
pat=sys.argv[1]
for f in sys.argv[2:]:
    t=open(f,encoding='utf-8',errors='ignore').read().replace('\\"','"')
    t=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',t,flags=re.S)
    s=html.unescape(re.sub(r'<[^>]+>',' ',t)); s=re.sub(r'\s+',' ',s)
    seen=set()
    for m in re.finditer(pat,s,flags=re.I):
        x=s[max(0,m.start()-100):m.end()+120]
        if x[80:140] in seen: continue
        seen.add(x[80:140]); print(f,'::',x)
