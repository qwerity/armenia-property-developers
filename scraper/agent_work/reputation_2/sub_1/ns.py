import sys, re, html, urllib.parse
from f import fetch

SITES = {
    "hetq": ("https://hetq.am/hy/search?q={q}", r'href="(https://hetq\.am/hy/article/\d+)"[^>]*>(.*?)</a>'),
    "factor": ("https://factor.am/?s={q}", r'href="(https://factor\.am/\d+\.html)"[^>]*>(.*?)</a>'),
    "a1plus": ("https://a1plus.am/hy/search?q={q}", r'href="(/hy/article/\d+)"[^>]*>(.*?)</a>'),
    "newsam": ("https://news.am/arm/search/?q={q}", r'href="((?:https://news\.am)?/arm/news/\d+\.html)"[^>]*>(.*?)</a>'),
    "shamshyan": ("https://shamshyan.com/hy/search?q={q}", r'href="((?:https://shamshyan\.com)?/hy/article/[^"]+)"[^>]*>(.*?)</a>'),
}


def run(site, q):
    url, pat = SITES[site]
    h = fetch(url.format(q=urllib.parse.quote(q)))
    seen = {}
    for m in re.finditer(pat, h, re.S):
        title = html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
        title = re.sub(r"\s+", " ", title).strip()
        if title and m.group(1) not in seen:
            seen[m.group(1)] = title
    return len(h), seen


if __name__ == "__main__":
    sites = sys.argv[1].split(",")
    for q in sys.argv[2:]:
        for s in sites:
            n, res = run(s, q)
            print(f"### {s} «{q}» bytes={n} hits={len(res)}")
            for u, t in list(res.items())[:10]:
                print("-", u, "|", t[:160])
