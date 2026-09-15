#!/usr/bin/env python3
"""usage: sp.py QUERY [...] -- spyur.am search; for each company hit print legal name, executive, address, activity snippet."""
import sys, re, html, urllib.parse, subprocess, time, os, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def get(u):
    fn = os.path.join(D, hashlib.md5(u.encode()).hexdigest()[:12] + ".html")
    if not (os.path.exists(fn) and os.path.getsize(fn) > 500):
        subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, u, "-o", fn]); time.sleep(0.7)
    return open(fn, errors="ignore").read() if os.path.exists(fn) else ""


def text(t):
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


for q in sys.argv[1:]:
    print("####", q)
    t = get("https://www.spyur.am/en/home/search/?addres=&company_name=" + urllib.parse.quote(q))
    links = list(dict.fromkeys(re.findall(r'href="(/en/companies/[^"]+)"', t)))[:4]
    if not links:
        print("  (no hits)")
    for l in links:
        x = text(get("https://www.spyur.am" + l.replace("/en/", "/am/", 1)))
        i = x.find("դիմելով «Սփյուռ» :")
        seg = x[i + 19:i + 700] if i >= 0 else x[:700]
        print("-", "https://www.spyur.am" + l, "|", seg)
