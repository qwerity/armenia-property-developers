import sys, os, re, json, hashlib, time, argparse
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

D = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(D, "cache")
H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
     "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
     "Accept-Language": "en-US,en;q=0.9,hy;q=0.8,ru;q=0.7"}
_last = {}


def get(url, refresh=False):
    k = hashlib.md5(url.encode()).hexdigest()
    p = os.path.join(C, k)
    if os.path.exists(p) and not refresh:
        with open(p, encoding="utf-8", errors="replace") as fh:
            j = json.load(fh)
        return j["status"], j["url"], j["text"]
    host = urlparse(url).netloc
    dt = time.time() - _last.get(host, 0)
    if dt < 0.6:
        time.sleep(0.6 - dt)
    try:
        r = requests.get(url, headers=H, timeout=30, verify=False)
        try:
            body = r.content.decode("utf-8")
        except UnicodeDecodeError:
            body = r.content.decode(r.encoding or "cp1251", errors="replace")
        st, fu, tx = r.status_code, r.url, body
    except Exception as e:
        st, fu, tx = -1, url, "ERR " + str(e)[:300]
    _last[host] = time.time()
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"status": st, "url": fu, "text": tx}, fh)
    return st, fu, tx


COORD = [r"!2d(-?\d+\.\d+)!3d(-?\d+\.\d+)", r"@(\d{2}\.\d+),(\d{2}\.\d+)", r"[?&](?:q|ll|center|query)=(\d{2}\.\d+),\s*(\d{2}\.\d+)",
         r"(?:lat|latitude)[\"']?\s*[:=]\s*[\"']?(\d{2}\.\d{3,})", r"(?:lng|lon|longitude)[\"']?\s*[:=]\s*[\"']?(\d{2}\.\d{3,})",
         r"setView\(\[(\d{2}\.\d+),\s*(\d{2}\.\d+)", r"LatLng\((\d{2}\.\d+),\s*(\d{2}\.\d+)", r"ll=(\d{2}\.\d+)(?:,|%2C)(\d{2}\.\d+)", r"pt=(\d{2}\.\d+)(?:,|%2C)(\d{2}\.\d+)"]


def info(url, text=3000, links=True, allimgs=False, refresh=False):
    st, fu, tx = get(url, refresh)
    print("STATUS", st, fu, len(tx))
    if st != 200 and len(tx) < 500:
        print(tx[:500]); return
    s = BeautifulSoup(tx, "html.parser")
    print("TITLE", s.title.get_text(strip=True) if s.title else "")
    for m in s.find_all("meta"):
        if m.get("property") in ("og:image", "og:description", "og:title") or m.get("name") == "description":
            print("META", m.get("property") or m.get("name"), (m.get("content") or "")[:300])
    for pat in COORD:
        for mm in set(re.findall(pat, tx))[:5] if False else list(dict.fromkeys(re.findall(pat, tx)))[:5]:
            print("COORD", pat[:12], mm)
    print("PHONES", sorted(set(re.findall(r"tel:([+\d\s\-()]+)", tx)))[:8])
    print("EMAILS", sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", tx)) - {""})[:8])
    print("VIDEOS", sorted(set(re.findall(r"(?:youtube\.com/(?:embed/|watch\?v=)|youtu\.be/|vimeo\.com/(?:video/)?)[\w-]+", tx)))[:8])
    print("SOCIAL", sorted(set(re.findall(r"https?://(?:www\.)?(?:facebook|instagram|t\.me|youtube|tiktok)[^\s\"'<>]*", tx)))[:10])
    for i in s.find_all("iframe"):
        print("IFRAME", (i.get("src") or i.get("data-src") or "")[:300])
    imgs = []
    for i in s.find_all(["img", "source"]):
        u = i.get("data-src") or i.get("src") or i.get("data-lazy-src") or (i.get("srcset") or "").split(" ")[0]
        if u and not u.startswith("data:"):
            imgs.append(urljoin(fu, u))
    imgs += [urljoin(fu, u) for u in re.findall(r"url\(['\"]?([^'\")]+\.(?:jpe?g|png|webp))", tx)]
    imgs = list(dict.fromkeys(imgs))
    print("IMGS", len(imgs), imgs if allimgs else imgs[:25])
    if links:
        ls = []
        for a in s.find_all("a", href=True):
            u = urljoin(fu, a["href"]).split("#")[0]
            ls.append((u, a.get_text(" ", strip=True)[:50]))
        seen = set()
        for u, t in ls:
            if u in seen: continue
            seen.add(u); print("LINK", u, "|", t)
    for t in s(["script", "style", "noscript", "svg"]):
        t.decompose()
    body = re.sub(r"\s*\n\s*", "\n", s.get_text("\n", strip=True))
    print("TEXT", body[:text])


if __name__ == "__main__":
    import urllib3; urllib3.disable_warnings()
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("-t", type=int, default=3000); ap.add_argument("-n", action="store_true"); ap.add_argument("-i", action="store_true"); ap.add_argument("-r", action="store_true")
    ap.add_argument("-g")
    a = ap.parse_args()
    if a.g:
        st, fu, tx = get(a.url, a.r)
        print("STATUS", st, fu, len(tx))
        for m in re.finditer(a.g, tx):
            print("...", tx[max(0, m.start() - 150): m.end() + 250].replace("\n", " "))
    else:
        info(a.url, a.t, not a.n, a.i, a.r)
