import sys,re,subprocess,html,urllib.parse,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
cl=lambda x: html.unescape(re.sub(r'<[^>]+>','',x)).strip()
for q in sys.argv[1:]:
    u='https://www.bing.com/search?setlang=en&cc=US&q='+urllib.parse.quote(q)
    r=subprocess.run(['curl','-sL','-m','25','-A',UA,'-H','Accept-Language: en-US,en;q=0.9',u],capture_output=True).stdout.decode('utf8','ignore')
    print('##',q)
    if 'captcha' in r.lower() and 'b_algo' not in r: print('  BLOCKED'); continue
    for blk in re.findall(r'<li class="b_algo".*?</li>',r,re.S)[:10]:
        a=re.search(r'<h2[^>]*><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',blk,re.S)
        s=re.search(r'<p[^>]*>(.*?)</p>',blk,re.S)
        if a:
            href=a.group(1)
            m=re.search(r'[?&]u=a1([^&]+)',href)
            if m:
                import base64
                try: href=base64.urlsafe_b64decode(m.group(1)+'==').decode()
                except Exception: pass
            print('  -',cl(a.group(2))[:100],'|',html.unescape(href)); print('     ',cl(s.group(1))[:250] if s else '')
    time.sleep(2)
