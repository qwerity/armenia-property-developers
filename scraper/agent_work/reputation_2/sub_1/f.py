import sys, re, html, hashlib, os, subprocess, time

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
DEFAULT = r"ՀՎՀՀ|ՍՊԸ|ՓԲԸ|LLC|CJSC|ООО|ЗАО|[Tt]ax ID|ИНН|\b\d{8}\b"


def fetch(url):
    f = os.path.join(D, hashlib.md5(url.encode()).hexdigest()[:12] + ".html")
    if not (os.path.exists(f) and os.path.getsize(f) > 0):
        subprocess.run(["curl", "-sL", "--max-time", "25", "-A", UA, url, "-o", f])
        time.sleep(0.6)
    return open(f, errors="ignore").read() if os.path.exists(f) else ""


def text(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


if __name__ == "__main__":
    t = text(fetch(sys.argv[1]))
    pat = sys.argv[2] if len(sys.argv) > 2 else DEFAULT
    print("LEN", len(t))
    if pat == "ALL":
        print(t[:6000])
    else:
        seen = 0
        for m in re.finditer(pat, t):
            print("..", t[max(0, m.start() - 160):m.end() + 160])
            seen += 1
            if seen > 25:
                break
