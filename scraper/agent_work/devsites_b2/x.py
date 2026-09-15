import sys,re,html as H
from urllib.parse import urljoin
from f import get,text
def summ(url,n=6000):
    h=get(url)
    if h.startswith("__"): print("FAIL",h[:300]); return
    t=re.search(r"(?is)<title>(.*?)</title>",h); print("TITLE:",H.unescape(t.group(1)).strip() if t else "")
    og=re.findall(r'<meta[^>]+property="og:(title|description|image)"[^>]+content="([^"]*)"',h); print("OG:",og[:4])
    co=set()
    for p in [r'!2d(-?\d+\.\d+)!3d(-?\d+\.\d+)', r'@(\d{2}\.\d+),(\d{2}\.\d+)', r'[?&](?:q|ll|center|daddr)=(\d{2}\.\d+)(?:,|%2C)\s*(\d{2}\.\d+)', r'"?lat"?\s*[:=]\s*"?(\d{2}\.\d{3,})"?[,\s]+"?(?:lng|lon)"?\s*[:=]\s*"?(\d{2}\.\d{3,})',r'data-lat="([\d.]+)"[^>]*data-lng="([\d.]+)"',r'\[\s*(40\.\d{3,})\s*,\s*(4[3-6]\.\d{3,})\s*\]',r'pt=(4[3-6]\.\d+),(40\.\d+)']:
        for m in re.findall(p,h): co.add((p[:12],m))
    print("COORDS:",list(co)[:8])
    for m in re.findall(r'<iframe[^>]+src="([^"]+)"',h): print("IFRAME:",H.unescape(m)[:250])
    print("VIDEOS:",sorted(set(re.findall(r'(?:https?:)?//(?:www\.)?(?:youtube\.com/(?:embed/|watch\?v=)[\w-]+|youtu\.be/[\w-]+|player\.vimeo\.com/video/\d+|vimeo\.com/\d+)',h)))[:10])
    imgs=[]
    for m in re.findall(r'(?:src|data-src|href|data-bg|url\()\s*=?\s*["\']?([^"\'\s)]+\.(?:jpe?g|png|webp))',h,re.I):
        u=urljoin(url,H.unescape(m))
        if not re.search(r'logo|icon|favicon|flag|avatar|placeholder|-\d{2,3}x\d{2,3}\.',u,re.I) and u not in imgs: imgs.append(u)
    print("IMAGES(%d):"%len(imgs)); [print("  ",i) for i in imgs[:15]]
    print("PHONES:",sorted(set(re.findall(r'tel:([+\d\s()-]{7,})',h)))[:8]," EMAILS:",sorted(set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+',text(h))))[:5])
    print("SOCIAL:",sorted(set(re.findall(r'https?://(?:www\.)?(?:facebook\.com|instagram\.com|youtube\.com/(?:@|channel|c/|user)|t\.me)/[^"\'\s<>]*',h)))[:10])
    print("TEXT:",text(h)[:n])
if __name__=="__main__":
    summ(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 6000)
