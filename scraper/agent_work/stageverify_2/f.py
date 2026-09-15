import sys, re, html, subprocess

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, "-H", "Accept: text/html,application/xhtml+xml",
                        "-H", "Accept-Language: en", url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def text(t):
    t = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t)


if __name__ == "__main__":
    url = sys.argv[1]
    raw = fetch(url)
    if len(sys.argv) > 2 and sys.argv[2] == "raw":
        print(raw)
    else:
        t = text(raw)
        if len(sys.argv) > 2:
            for kw in sys.argv[2:]:
                for m in re.finditer(kw, t, re.I):
                    print("...", t[max(0, m.start() - 200):m.end() + 200])
        else:
            print(t[:int(8000)])
