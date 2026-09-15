#!/usr/bin/env python3
"""usage: s.py "query" [...] -- web search via DuckDuckGo html / Bing fallback; prints title | url | snippet."""
import sys, re, html, urllib.parse, subprocess, time, os, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def get(url, data=None):
    fn = os.path.join(D, "q_" + hashlib.md5((url + (data or "")).encode()).hexdigest()[:12] + ".html")
    if os.path.exists(fn) and os.path.getsize(fn) > 2000:
        return open(fn, errors="ignore").read()
    cmd = ["curl", "-sL", "-m", "25", "-A", UA, "-H", "Accept-Language: hy,ru;q=0.8,en;q=0.6", url, "-o", fn]
    if data:
        cmd[1:1] = ["--data", data]
    subprocess.run(cmd)
    time.sleep(1.2)
    return open(fn, errors="ignore").read() if os.path.exists(fn) else ""


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


for q in sys.argv[1:]:
    print("#### ", q)
    t = get("https://html.duckduckgo.com/html/", "q=" + urllib.parse.quote(q))
    items = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)">(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>', t, re.S)
    if items:
        for u, ti, sn in items[:10]:
            m = re.search(r"uddg=([^&]+)", u)
            u = urllib.parse.unquote(m.group(1)) if m else u
            print("-", clean(ti), "|", u, "|", clean(sn)[:220])
        continue
    t = get("https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&setlang=hy")
    items = re.findall(r'<li class="b_algo".*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?(?:<p[^>]*>(.*?)</p>|</li>)', t, re.S)
    if not items:
        print("  (no results; ddg/bing blocked?)", len(t))
    for u, ti, sn in items[:10]:
        print("-", clean(ti), "|", u, "|", clean(sn or "")[:220])
