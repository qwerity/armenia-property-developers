"""usage: news.py "query" "key1|key2" -- lists search-result anchors whose text matches keys."""
import sys, re, html, urllib.parse
from f import fetch

ENGINES = ["https://www.aravot.am/?s={q}", "https://factor.am/?s={q}", "https://armlur.am/?s={q}",
           "https://168.am/?s={q}", "https://www.azatutyun.am/s?k={q}", "https://hetq.am/hy/search?q={q}"]

q, keys = sys.argv[1], re.compile(sys.argv[2], re.I)
seen = set()
for e in ENGINES:
    url = e.format(q=urllib.parse.quote(q))
    h = fetch(url)
    base = re.match(r"https://[^/]+", url).group(0)
    for m in re.finditer(r'<a[^>]+href="([^"#]+)"[^>]*>(.*?)</a>', h, re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        u = m.group(1) if m.group(1).startswith("http") else base + m.group(1)
        if len(t) > 25 and keys.search(t) and "?s=" not in u and "search" not in u and u not in seen:
            seen.add(u)
            print("-", u, "|", t[:220])
