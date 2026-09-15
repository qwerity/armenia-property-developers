import re,sys,subprocess,urllib.parse,time,html
def get(u):
    time.sleep(0.6)
    return subprocess.run(['curl','-sL','-m','30','-A','Mozilla/5.0',u],capture_output=True,text=True).stdout
def search(s):
    h=get("https://www.e-register.am/hy/search/companies?query="+urllib.parse.quote(s))
    n=re.search(r'քանակը՝ \((\d+)\)',h)
    return (n.group(1) if n else '0'), re.findall(r'href="/hy/companies/(\d+)">\s*<h4>(.*?)</h4>',h,re.S)
def detail(cid):
    t=get("https://www.e-register.am/hy/companies/"+cid)
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    t=html.unescape(re.sub(r'<[^>]+>','|',t)); t=re.sub(r'(\s*\|\s*)+','|',t)
    g=lambda k: (re.search(k+r'\|([^|]+)',t) or [None,None])[1]
    st='ok' if 'գրառված չեն' in t else 'STATUS:'+ (g('Կարգավիճակ') or '?')
    return f"tax={g('ՀՎՀՀ')} reg={g('Գրանցման ամսաթիվ')} addr={g('Գտնվելու վայր')} {st}"
maxd=int(sys.argv[1])
for s in sys.argv[2:]:
    n,res=search(s)
    print('##',s,'count',n)
    for k,(cid,name) in enumerate(res):
        name=html.unescape(name.strip())
        print('  ',name, detail(cid) if k<maxd else cid)
