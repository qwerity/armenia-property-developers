"""Fetch URLs politely, save html + text, print price-ish lines.

usage: python3 fetch.py NAME=URL [NAME=URL ...] [--grep REGEX] [--all]
"""
import sys, re, html, os, time, subprocess, urllib.parse
from collections import defaultdict

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "pages")
os.makedirs(P, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PRICE = r"֏|AMD|\$|USD|դրամ|драм|м²|m2|m²|մ²|քմ|ք/մ|price|цена|стоим|արժ|sold|վաճառ"

args = [a for a in sys.argv[1:] if "=" in a and not a.startswith("--")]
grep = PRICE
show_all = "--all" in sys.argv
for i, a in enumerate(sys.argv):
    if a == "--grep":
        grep = sys.argv[i + 1]
last = defaultdict(float)
for a in args:
    name, url = a.split("=", 1)
    host = urllib.parse.urlparse(url).netloc
    wait = 0.6 - (time.time() - last[host])
    if wait > 0:
        time.sleep(wait)
    last[host] = time.time()
    hp = os.path.join(P, name + ".html")
    r = subprocess.run(["curl", "-sL", "--compressed", "-m", "40", "-o", hp, "-w", "%{http_code} %{size_download} %{url_effective}",
                        "-H", "User-Agent: " + UA, "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                        "-H", "Accept-Language: en", url], capture_output=True, text=True)
    print(f"===== {name} {r.stdout}")
    try:
        s = open(hp, encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        continue
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", "\n", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r\f\v\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    open(os.path.join(P, name + ".txt"), "w").write(s)
    lines = s.split("\n")
    if show_all:
        print(s[:6000])
    else:
        hits = [f"{j}: {l.strip()[:160]}" for j, l in enumerate(lines) if re.search(grep, l, re.I)]
        print("\n".join(hits[:40]))
