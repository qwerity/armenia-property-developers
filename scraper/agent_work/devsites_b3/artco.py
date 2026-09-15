import re,sys,json
sys.path.insert(0,'.')
from f import get
from bs4 import BeautifulSoup
L=[("district",12,1),("district",6,1),("district",13,1),("district",10,1),("building",11,1),("district",3,2),("building",4,2),("district",7,2),("building",2,2),("district",5,2),("building",8,2),("building",9,2),("district",1,2)]
for pg,pid,ps in L:
    url=f"https://artco.am/?app=AppProject&page={pg}&project_id={pid}&project_status_id={ps}"
    st,u,tx=get(url)
    s=BeautifulSoup(tx,"html.parser")
    fl=sorted(set(re.findall(r'"floor_count":"(\d+)"',tx)),key=int)
    ll=re.findall(r'"latitude":"([\d.]+)","longitude":"([\d.]+)"',tx)[:1]
    cnt=re.findall(r'"appartment_count":(\d+),"sold_appartment_count":(\d+)',tx)
    yt=sorted(set(re.findall(r"youtube\.com/embed/([\w-]+)",tx)))
    imgs=[i.get("src") for i in s.find_all("img") if "file.php" in (i.get("src") or "")]
    for t in s(["script","style"]): t.decompose()
    t=s.get_text("\n",strip=True)
    i=t.find("Նախագծեր\n"); t=t[i+9:]
    j=t.find("Փաստաթղթեր\n",200)
    print("=====",url,"floors",fl,"ll",ll,"counts",cnt[:12],"yt",yt)
    print("IMGS",imgs[:10])
    print(re.sub(r"\n(\d{4}[.-]\d{2}(-\d{2})?)(?=\n)","",t[:3500]))
