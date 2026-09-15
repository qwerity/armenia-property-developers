import sys,re,subprocess,html,time
pat=sys.argv[1]
for u in sys.argv[2:]:
    t=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36',u],capture_output=True).stdout.decode('utf8','ignore')
    t=html.unescape(t).replace('\\"','"')
    print('==',u,len(t)); s=set()
    for m in re.finditer(r'.{0,120}(%s).{0,140}'%pat,t):
        x=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',m.group(0))).strip()
        if x not in s: s.add(x); print('   ',x[:260])
        if len(s)>12: break
    time.sleep(0.6)
