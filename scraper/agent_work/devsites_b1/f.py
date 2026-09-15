#!/usr/bin/env python3
"""Cached fetch + extraction helper. Usage: f.py <cmd> <url> [arg]
cmds: get, links [regex], text [maxchars], meta, raw [regex]"""
import hashlib, os, re, subprocess, sys, time, html, json
from urllib.parse import urljoin, urlparse

D = os.path.dirname(os.path.abspath(__file__)) + "/cache"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def get(url, force=False):
    p = f"{D}/{hashlib.md5(url.encode()).hexdigest()}.html"
    if os.path.exists(p) and not force:
        return open(p, encoding="utf-8", errors="replace").read()
    time.sleep(0.5)
    r = subprocess.run(["curl", "-sSL", "-k", "--compressed", "-m", "40", "-A", UA,
                        "-H", "Accept: text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                        "-H", "Accept-Language: en-US,en;q=0.9,hy;q=0.8,ru;q=0.7",
                        "-w", "\n<!--STATUS %{http_code} %{url_effective}-->", url], capture_output=True)
    body = r.stdout.decode("utf-8", errors="replace")
    if r.returncode != 0:
        body += f"\n<!--CURLERR {r.returncode} {r.stderr.decode(errors='replace')[:200]}-->"
    open(p, "w", encoding="utf-8").write(body)
    return body


def text(h):
    h = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|section)>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def links(url, h):
    out = []
    for m in re.finditer(r'href=["\']([^"\'#]+)', h):
        u = urljoin(url, html.unescape(m.group(1)))
        if u not in out:
            out.append(u)
    return out


def meta(url, h):
    r = {}
    m = re.search(r"(?is)<title>(.*?)</title>", h); r["title"] = html.unescape(m.group(1).strip()) if m else ""
    for k in ["og:title", "og:description", "og:image", "description"]:
        m = re.search(r'<meta[^>]+(?:property|name)=["\']%s["\'][^>]+content=["\']([^"\']*)' % k, h)
        if m: r[k] = html.unescape(m.group(1))
    co = set()
    for pat in [r"!3d(-?\d+\.\d+)!2d(-?\d+\.\d+)", r"@(\d{2}\.\d{3,}),(\d{2}\.\d{3,})", r"[?&](?:q|ll|center|daddr)=(\d{2}\.\d{3,})(?:,|%2C)\s*(\d{2}\.\d{3,})",
                r"lat[\"']?\s*[:=]\s*[\"']?(\d{2}\.\d{3,})[\s\S]{0,40}?(?:lng|lon)[\"']?\s*[:=]\s*[\"']?(\d{2}\.\d{3,})"]:
        for a in re.findall(pat, h): co.add(a)
    for a in re.findall(r"!2d(-?\d+\.\d+)!3d(-?\d+\.\d+)", h): co.add((a[1], a[0]))
    for a in re.findall(r"(?:ll|pt)=(\d{2}\.\d{3,})(?:,|%2C)(\d{2}\.\d{3,})", h): co.add((a[1], a[0]) if float(a[0]) > 42 else a)
    r["coords"] = sorted(co)
    r["iframes"] = re.findall(r'<iframe[^>]+src=["\']([^"\']+)', h)
    r["videos"] = sorted(set(re.findall(r'(?:https?:)?//(?:www\.)?(?:youtube\.com/(?:embed/|watch\?v=|shorts/)|youtu\.be/|player\.vimeo\.com/video/|vimeo\.com/)[\w\-?=&]+', h)))
    r["phones"] = sorted(set(re.findall(r'tel:([+\d\s\-()]+)', h)))
    r["emails"] = sorted(set(re.findall(r'[\w.\-]+@[\w\-]+\.[a-z]{2,}', h)) - {"x@x.x"})
    r["social"] = sorted(set(re.findall(r'https?://(?:www\.)?(?:facebook\.com|instagram\.com|youtube\.com|t\.me)/[^"\'\s<>]+', h)))
    imgs = []
    for m in re.finditer(r'(?:src|data-src|href|data-bg|url\()=?["\']?([^"\'\s)>]+\.(?:jpe?g|png|webp))', h, re.I):
        u = urljoin(url, html.unescape(m.group(1)))
        if u not in imgs and not re.search(r"logo|icon|favicon|flag|cropped-|fav\d|-\d{2,3}x\d{2,3}\.|HEADER|placeholder|arrow", u, re.I): imgs.append(u)
    r["images"] = imgs[:40]
    return r


if __name__ == "__main__":
    cmd, url = sys.argv[1], sys.argv[2]
    arg = sys.argv[3] if len(sys.argv) > 3 else None
    h = get(url, force=(cmd == "reget"))
    st = re.search(r"<!--STATUS (\d+) (\S+)-->", h)
    print("#", st.group(1) if st else "?", st.group(2) if st else "", len(h), "bytes")
    if cmd in ("get", "reget"): pass
    elif cmd == "links":
        host = urlparse(url).netloc.replace("www.", "")
        for u in links(url, h):
            if (arg == "all" or host in u) and (not arg or arg == "all" or re.search(arg, u)) and not re.search(r"\.(css|js|png|jpe?g|svg|webp|ico|woff2?)(\?|$)", u):
                print(u)
    elif cmd == "text":
        print(text(h)[: int(arg or 6000)])
    elif cmd == "meta":
        print(json.dumps(meta(url, h), ensure_ascii=False, indent=1))
    elif cmd == "raw":
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 8; last = -1
        for m in re.finditer(arg, h):
            if m.start() < last: continue
            s = max(0, m.start() - 120); last = m.end() + 200; print("...", h[s:last].replace("\n", " "), "\n"); n -= 1
            if n <= 0: break
    elif cmd == "sm":
        for l in re.findall(r"<loc>\s*([^<\s]+)", h): print(html.unescape(l))
