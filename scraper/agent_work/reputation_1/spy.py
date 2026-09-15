import re,sys,subprocess,urllib.parse,time,html
def get(u):
    time.sleep(0.6)
    return subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0',u],capture_output=True,text=True).stdout
def search(q):
    h=get("https://www.spyur.am/am/home/search/?company_name="+urllib.parse.quote_plus(q))
    out=[]
    for m in re.finditer(r'href="(/am/companies/[^"]+)"[^>]*>(.*?)</a>',h,re.S):
        out.append((m.group(1), html.unescape(re.sub(r'<[^>]+>|\s+',' ',m.group(2)))[:160]))
    return out
def page(p):
    h=get("https://www.spyur.am"+p)
    t=html.unescape(re.sub(r'<script.*?</script>|<style.*?</style>','',h,flags=re.S))
    t=re.sub(r'<[^>]+>',' ',t); t=re.sub(r'\s+',' ',t)
    return t
if __name__=="__main__" and sys.argv[1]=="s":
    for q in sys.argv[2:]:
        print('##',q)
        for r in search(q): print(' ',*r)
elif __name__=="__main__":
    for p in sys.argv[2:]:
        t=page(p); i=t.find('ՀՎՀՀ')
        print('##',p); print(t[max(0,i-1500):i+400] if i>=0 else t[:2000])
