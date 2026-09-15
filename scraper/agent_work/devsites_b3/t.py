"""Compact page view: t.py url [maxlines] [linefilter-regex-for-LINK]"""
import sys, io, re, contextlib, urllib3
urllib3.disable_warnings()
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from f import info

url = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 80
lf = sys.argv[3] if len(sys.argv) > 3 else None
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    info(url, 20000, bool(lf), False)
seen, out = set(), []
for l in buf.getvalue().splitlines():
    if l.startswith(("SOCIAL", "EMAILS", "PHONES", "META og:title")):
        continue
    if l.startswith("LINK") and not re.search(lf, l):
        continue
    if l in seen:
        continue
    seen.add(l)
    out.append(l[:700])
print("\n".join(out[:n]))
