#!/usr/bin/env python3
"""usage: gn.py "query" [...] -- Google News RSS search (hy/ru/en editions); prints date | title | link."""
import sys, re, html, urllib.parse, subprocess, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
EDS = [("hy", "AM", "AM:hy"), ("ru", "AM", "AM:ru"), ("en-US", "US", "US:en")]

for q in sys.argv[1:]:
    seen = set()
    print("#### ", q)
    for hl, gl, ceid in EDS:
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl={hl}&gl={gl}&ceid={ceid}"
        t = subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, url], capture_output=True, text=True).stdout
        time.sleep(0.8)
        for it in re.findall(r"<item>(.*?)</item>", t, re.S):
            g = lambda k: html.unescape((re.search(r"<%s[^>]*>(.*?)</%s>" % (k, k), it, re.S) or [None, ""])[1])
            ti = g("title")
            if ti in seen:
                continue
            seen.add(ti)
            print("-", g("pubDate")[5:16], "|", ti, "|", g("link")[:200])
        if len(seen) >= 15:
            break
    if not seen:
        print("  (no results)")
