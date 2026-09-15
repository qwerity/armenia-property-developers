#!/usr/bin/env python3
"""usage: f.py [-x EXTRA_REGEX] URL [URL...] -- fetch (cached) and print legal-entity snippets."""
import sys, re, html, hashlib, os, subprocess, time

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
args = sys.argv[1:]
extra = ""
if args and args[0] == "-x":
    extra = args[1]; args = args[2:]
full = False
if args and args[0] == "-f":
    full = True; args = args[1:]
for u in args:
    fn = os.path.join(D, hashlib.md5(u.encode()).hexdigest()[:12] + ".html")
    if not os.path.exists(fn) or os.path.getsize(fn) == 0:
        subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, u, "-o", fn])
        time.sleep(0.6)
    t = open(fn, errors="ignore").read() if os.path.exists(fn) else ""
    print(f"## {u} {len(t)}")
    t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', t)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t)); t = re.sub(r'\s+', ' ', t)
    if full:
        print(t[:6000]); continue
    pat = r'ՍՊԸ|ՓԲԸ|ՀՎՀՀ|LLC|ООО|CJSC|ИНН|\b\d{8}\b|Ltd|[Tt]ax ID|հարկ վճար' + ('|' + extra if extra else '')
    seen = set(); n = 0
    for m in re.finditer(pat, t):
        s = t[max(0, m.start() - 90):m.end() + 90]
        k = t[max(0, m.start() - 20):m.end() + 20]
        if k in seen: continue
        seen.add(k); print('..', s); n += 1
        if n > 20: break
