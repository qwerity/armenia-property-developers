import sys,re,subprocess,html,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PAT=re.compile(r'.{0,60}(?:ՍՊԸ|ՓԲԸ|ԲԲԸ|ООО|ЗАО|LLC|L\.L\.C|CJSC|ՀՎՀՀ|ՀՎՀ|Tax ID|TIN|ИНН|ИНН|ՀՎՀՀ|\b\d{8}\b|Ա/Ձ|©).{0,60}')
for u in sys.argv[1:]:
    try:
        r=subprocess.run(['curl','-sL','-m','25','-A',UA,u],capture_output=True,timeout=30)
        t=r.stdout.decode('utf8','ignore')
    except Exception as e:
        print('ERR',u,e); continue
    t=re.sub(r'<script.*?</script>|<style.*?</style>',' ',t,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
    print('==',u,len(t))
    seen=set()
    for m in PAT.finditer(t):
        s=m.group(0)
        if re.search(r'\d{8}',s) and not re.search(r'ՀՎՀՀ|ՀՎՀ|Tax|TIN|ИНН|ՍՊԸ|LLC|ООО',s): continue
        if s not in seen: seen.add(s); print('  ',s)
        if len(seen)>25: break
    time.sleep(0.5)
