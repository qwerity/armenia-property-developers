import sys,re,html,urllib.request
for u in sys.argv[1:]:
    try:
        t=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30).read().decode('utf-8','replace')
    except Exception as e: print(u,e); continue
    t=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>',' ',t); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
    kw=sys.argv[0]
    ps=[m.start() for m in re.finditer(r'ՍՊԸ|ՓԲԸ|բնակիչ|դատարան|հայց',t)]
    i=ps[0] if ps else 0
    print('==',u,'\n',t[max(0,i-600):i+1400],'\n')
