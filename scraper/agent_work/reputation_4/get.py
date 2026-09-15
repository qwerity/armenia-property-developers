import sys, re, html, time, urllib.request, os, ssl

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cacheC")
os.makedirs(OUT, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

args = sys.argv[1:]
for name, url in zip(args[::2], args[1::2]):
    try:
        raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30, context=ctx).read().decode("utf8", "ignore")
        t = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
        open(os.path.join(OUT, name + ".txt"), "w").write(t)
        open(os.path.join(OUT, name + ".html"), "w").write(raw)
        print(name, len(t))
    except Exception as e:
        print(name, "ERR", e)
    time.sleep(0.6)
