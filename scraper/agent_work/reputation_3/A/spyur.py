import sys,re,subprocess,html,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for q in sys.argv[1:]:
    u='https://www.spyur.am/en/home/search-17/?company_name='+urllib.parse.quote(q)
    r=subprocess.run(['curl','-sL','-m','25','-A',UA,u],capture_output=True).stdout.decode('utf8','ignore')
    print('##',q)
    seen=set()
    for h,t in re.findall(r'href="(/en/companies/[^"]+)"[^>]*>(.*?)</a>',r,re.S):
        t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t).strip()
        if h in seen: continue
        seen.add(h); print('  -',t[:150],'| https://www.spyur.am'+h)
    time.sleep(1)
