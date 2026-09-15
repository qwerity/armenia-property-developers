#!/usr/bin/env python3
"""usage: ns.py [-t] "query" [...] -- search Armenian news sites' internal search; -t tests which sites work.
Prints article links whose anchor text/URL context contains the query words."""
import sys, re, html, urllib.parse, subprocess, time, os, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
SITES = {
    "aravot": "https://www.aravot.am/?s={q}",
    "hetq": "https://hetq.am/hy/search?q={q}",
    "168": "https://www.168.am/?s={q}",
    "factor": "https://factor.am/?s={q}",
    "newsam": "https://news.am/arm/search/?q={q}",
    "civilnet": "https://www.civilnet.am/?s={q}",
    "armlur": "https://armlur.am/?s={q}",
    "azatutyun": "https://www.azatutyun.am/s?k={q}",
    "hraparak": "https://hraparak.am/?s={q}",
    "infocom": "https://infocom.am/?s={q}",
    "armtimes": "https://www.armtimes.com/hy/search?q={q}",
    "shamshyan": "https://shamshyan.com/hy/search?q={q}",
}


def get(url):
    fn = os.path.join(D, "n_" + hashlib.md5(url.encode()).hexdigest()[:12] + ".html")
    if not (os.path.exists(fn) and os.path.getsize(fn) > 500):
        subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, url, "-o", fn])
        time.sleep(0.5)
    return open(fn, errors="ignore").read() if os.path.exists(fn) else ""


args = sys.argv[1:]
test = args and args[0] == "-t"
if test:
    args = args[1:]
only = None
if args and args[0].startswith("--sites="):
    only = args[0][8:].split(","); args = args[1:]
for q in args:
    words = [w.lower() for w in re.findall(r"\w+", q) if len(w) > 2]
    print("#### ", q)
    for name, pat in SITES.items():
        if only and name not in only:
            continue
        t = get(pat.format(q=urllib.parse.quote(q)))
        if test:
            print(name, len(t), t.lower().count(words[0]) if words else 0)
            continue
        out = set()
        for href, a in re.findall(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', t, re.S):
            txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", a))).strip()
            if len(txt) < 25:
                continue
            if all(w in txt.lower() for w in words[:2]) or (words and words[0] in txt.lower()):
                key = (txt[:150], href)
                if key not in out:
                    out.add(key)
                    print(f"- [{name}] {txt[:170]} | {href[:160]}")
