import sys, subprocess, re, hashlib, os, time, html
from urllib.parse import urlparse
D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
_last = {}


def fetch(url, timeout=25):
    """Fetch url with browser headers; cache to pages/. Returns (status, final_url, text)."""
    os.makedirs(f"{D}/pages", exist_ok=True)
    fn = f"{D}/pages/" + hashlib.md5(url.encode()).hexdigest() + ".html"
    meta = fn + ".meta"
    if os.path.exists(fn) and os.path.exists(meta):
        st, fu = open(meta).read().split(" ", 1)
        return st, fu.strip(), open(fn, encoding="utf-8", errors="replace").read()
    host = urlparse(url).netloc
    dt = time.time() - _last.get(host, 0)
    if dt < 0.6:
        time.sleep(0.6 - dt)
    _last[host] = time.time()
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "--compressed", "-A", UA,
                        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "-H", "Accept-Language: en-US,en;q=0.9,hy;q=0.8,ru;q=0.7",
                        "-o", fn, "-w", "%{http_code} %{url_effective}", url], capture_output=True, text=True)
    out = r.stdout.strip() or "000 " + url
    open(meta, "w").write(out)
    st, fu = out.split(" ", 1)
    txt = open(fn, encoding="utf-8", errors="replace").read() if os.path.exists(fn) else ""
    return st, fu, txt


def links(txt):
    return re.findall(r'href=["\']([^"\']+)["\']', txt)


def text(txt):
    t = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", txt)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


if __name__ == "__main__":
    mode = sys.argv[1]
    for u in sys.argv[2:]:
        st, fu, t = fetch(u)
        print("==", st, fu, len(t))
        if mode == "links":
            seen = set()
            for l in links(t):
                if l not in seen:
                    seen.add(l); print("  ", l)
        elif mode == "text":
            print(text(t)[:6000])
