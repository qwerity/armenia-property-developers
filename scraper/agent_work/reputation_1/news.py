"""Bing News RSS lookup: python3 news.py '<query>' ['<query>' ...] -> prints date | title | url."""
import html, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
CACHE = Path(__file__).resolve().parent / "news_cache"; CACHE.mkdir(exist_ok=True)
def rss(q):
    cf = CACHE / (re.sub(r"[^\w]+", "_", q)[:120] + ".xml")
    if cf.exists(): return cf.read_text()
    time.sleep(1.2)
    u = "https://www.bing.com/news/search?" + urllib.parse.urlencode({"q": q, "format": "rss"})
    t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "replace")
    cf.write_text(t); return t
for q in sys.argv[1:]:
    print("##", q)
    for it in re.findall(r"<item>(.*?)</item>", rss(q), re.S):
        g = lambda tag: html.unescape((re.search(rf"<{tag}>(.*?)</{tag}>", it, re.S) or [None, ""])[1])
        link = g("link"); m = re.search(r"url=([^&]+)", link)
        url = urllib.parse.unquote(m.group(1)) if m else link
        print(" ", g("pubDate")[5:16], "|", g("title")[:140], "|", url, "|", re.sub(r"<[^>]+>", "", g("description"))[:160])
