import sys, re, html, urllib.parse, subprocess, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def ddg(q):
    r = subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, "--data-urlencode", f"q={q}",
                        "https://html.duckduckgo.com/html/"], capture_output=True, text=True).stdout
    out = []
    for m in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>', r, re.S):
        u = m.group(1)
        if "uddg=" in u:
            u = urllib.parse.unquote(re.search(r"uddg=([^&]+)", u).group(1))
        strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
        out.append((strip(m.group(2)), u, strip(m.group(3))))
    return out, len(r)


for q in sys.argv[1:]:
    res, n = ddg(q)
    print("###", q, "bytes", n, "results", len(res))
    for t, u, s in res[:10]:
        print("-", t, "|", u, "|", s[:250])
    time.sleep(1.5)
