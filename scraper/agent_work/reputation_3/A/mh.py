import sys,re,subprocess,html,time
for bid in sys.argv[1:]:
    t=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0','https://myhome.am/hy/building/'+bid],capture_output=True).stdout.decode('utf8','ignore')
    t=html.unescape(t).replace('\\"','"')
    m=re.search(r'"builder":\{(.*?)"translitUrl":"([^"]*)"\}',t)
    ti=re.search(r'"title","0",\{"children":"([^"]*)"',t)
    print(bid, ti.group(1) if ti else '', '|', (m.group(1)[:600]+' slug='+m.group(2)) if m else 'NO BUILDER')
    time.sleep(0.6)
