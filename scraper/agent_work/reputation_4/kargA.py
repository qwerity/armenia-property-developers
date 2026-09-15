import sys,re,html,json,time,urllib.request,os
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/124'
out={}
for tin in sys.argv[1:]:
    fn=f'cacheA/karg_{tin}.html'
    if not os.path.exists(fn):
        time.sleep(0.8)
        d=urllib.request.urlopen(urllib.request.Request(f'https://karg.am/company/{tin}?lang=hy',headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','replace')
        open(fn,'w').write(d)
    d=open(fn).read()
    t=re.sub(r'<(script|style)[^>]*>.*?</\1>','',d,flags=re.S)
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',t)))
    g=lambda p: (re.search(p,t).group(1).strip() if re.search(p,t) else None)
    r={'name':g(r'^\s*(.*?) \(ՀՎՀՀ'),'status':g(r'Կարգավիճակ (\S+)'),'reg':g(r'Գրանցման ամսաթիվ (\d\d\.\d\d\.\d{4})'),
       'form':g(r'Կազմակերպաիրավական ձև (.*?) NACE'),'addr':g(r'Իրավաբանական հասցե (.*?) Հարկման'),
       'courts':g(r'Դատական գործեր (\d+) Տվյալների աղբյուր'),'cesa':g(r'Կատարողական վարույթներ (\d+)'),
       'director':g(r'(?:Տնօրեն|Ղեկավար) ([^✓✗]{3,60}?) (?:Հիմնադիրներ|Պաշտոն)'),
       'founders':g(r'Հիմնադիրներ Աղբյուր՝ e-register\.moj\.am \(BOR\) (.*?) Կապված')}
    out[tin]=r; print(tin,json.dumps(r,ensure_ascii=False))
json.dump(out,open('cacheA/karg_summary.json','w'),ensure_ascii=False,indent=1)
