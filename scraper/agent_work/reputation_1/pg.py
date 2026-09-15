import sys,re,html,subprocess,time
def get(u):
    time.sleep(0.6)
    return subprocess.run(['curl','-sL','-m','30','-A','Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/120 Safari/537.36',u],capture_output=True,text=True,errors='ignore').stdout
for u in sys.argv[1:]:
    h=get(u)
    links=sorted(set(re.findall(r'href="([^"#]+)"',h)))
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
    print('##',u,len(h))
    for k in re.finditer(r'ՀՎՀՀ|ՀՎՀ|ИНН|TIN|Tax ID|ՍՊԸ|ФБЭ|ՓԲԸ|LLC|ООО|\b0\d{7}\b',t):
        print('  ..',t[max(0,k.start()-80):k.start()+80])
    if '-l' in sys.argv[0:1]: pass
    print('  LINKS:',[l for l in links if not l.startswith(('javascript','mailto','tel'))][:80])
