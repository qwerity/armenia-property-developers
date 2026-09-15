#!/usr/bin/env python3
"""usage: art.py [-k KEYWORD_REGEX] URL [...] -- print article title/date, keyword snippets from <p> text, else first paragraphs."""
import sys, re, html, hashlib, os, subprocess, time

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
args = sys.argv[1:]
kw = None
if args and args[0] == "-k":
    kw = args[1]; args = args[2:]
for u in args:
    fn = os.path.join(D, hashlib.md5(u.encode()).hexdigest()[:12] + ".html")
    if not os.path.exists(fn) or os.path.getsize(fn) == 0:
        subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, u, "-o", fn]); time.sleep(0.6)
    t = open(fn, errors="ignore").read()
    g = lambda p: (re.search(p, t, re.S | re.I) or [None, ""])[1]
    title = g(r'<meta property="og:title" content="([^"]*)"') or g(r"<title>(.*?)</title>")
    date = g(r'"datePublished"\s*:\s*"([^"]+)"') or g(r'article:published_time" content="([^"]+)"')
    print("##", u, "|", html.unescape(title).strip(), "|", date)
    ps = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", p))).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", t, re.S)]
    ps = [p for p in ps if len(p) > 40]
    body = " ".join(ps)
    if kw:
        hits = [m for m in re.finditer(kw, body)]
        for m in hits[:8]:
            print("..", body[max(0, m.start() - 300):m.end() + 300])
        if not hits:
            print("(no keyword hit) ", body[:800])
    else:
        print(body[:1800])
