import re,sys,subprocess,urllib.parse,time,html
def az(q):
    time.sleep(1.0)
    t=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0',"https://www.azatutyun.am/s?k="+urllib.parse.quote(q)],capture_output=True,text=True).stdout
    c=re.search(r'search_results_count:"(\d+)"',t)
    seen=[]
    for m in re.finditer(r'<a href="(/a/[^"]+)"[^>]*title="([^"]+)"',t):
        if m.group(1) not in [s[0] for s in seen]: seen.append((m.group(1),html.unescape(m.group(2))))
    return (c.group(1) if c else '?'),seen
for q in sys.argv[1:]:
    c,s=az(q); print('##',q,c)
    for u,ti in s[:6]: print('   https://www.azatutyun.am'+u,'|',ti[:120])
