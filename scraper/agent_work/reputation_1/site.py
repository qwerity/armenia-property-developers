import sys,re,html,subprocess,time,urllib.parse
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
tmpl,pat=sys.argv[1],sys.argv[2]
for q in sys.argv[3:]:
    time.sleep(1)
    u=tmpl.replace('{q}',urllib.parse.quote(q))
    h=subprocess.run(['curl','-sL','-m','30','-A',UA,u],capture_output=True,text=True,errors='ignore').stdout
    print('###',u,len(h))
    seen=set()
    for m in re.finditer(r'<a[^>]+href="([^"]*'+pat+r'[^"]*)"[^>]*>(.*?)</a>',h,re.S):
        t=html.unescape(re.sub(r'<[^>]+>|\s+',' ',m.group(2))).strip()
        if m.group(1) in seen or len(t)<15: continue
        seen.add(m.group(1)); print(' -',t[:140],'|',m.group(1))
