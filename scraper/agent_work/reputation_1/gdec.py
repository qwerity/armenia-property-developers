import re,subprocess,json,urllib.parse,time
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
def dec(link):
    gid=re.search(r'articles/([^?]+)',link).group(1)
    time.sleep(0.6)
    h=subprocess.run(['curl','-sL','-m','30','-A',UA,'https://news.google.com/rss/articles/'+gid],capture_output=True,text=True).stdout
    sg=re.search(r'data-n-a-sg="([^"]+)"',h); ts=re.search(r'data-n-a-ts="([^"]+)"',h)
    if not sg: return None
    req=[["Fbv4je",json.dumps(["garturlreq",[["X","X",["X","X"],None,None,1,1,"US:en",None,1,None,None,None,None,None,0,1],"X","X",1,[1,1,1],1,1,None,0,0,None,0],gid,int(ts.group(1)),sg.group(1)])]]
    body='f.req='+urllib.parse.quote(json.dumps([req]))
    time.sleep(0.6)
    r=subprocess.run(['curl','-s','-m','30','-A',UA,'-H','Content-Type: application/x-www-form-urlencoded;charset=UTF-8','--data',body,'https://news.google.com/_/DotsSplashUi/data/batchexecute'],capture_output=True,text=True).stdout
    m=re.search(r'\\"(https?://[^\\"]+)\\"',r)
    return m.group(1) if m else None
if __name__=='__main__':
    import sys
    for l in sys.argv[1:]: print(dec(l))
