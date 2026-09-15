"""Site-internal news search: news.py "QUERY" [match-regex]. Prints article links whose anchor text or nearby snippet matches."""
import sys, re, html, urllib.parse, os, subprocess, time, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
SITES = ['https://factor.am/?s={q}', 'https://armlur.am/?s={q}', 'https://www.azatutyun.am/s?k={q}', 'https://168.am/?s={q}']


def fetch(u):
    fn = os.path.join(D, 'news_' + hashlib.md5(u.encode()).hexdigest() + '.html')
    if not (os.path.exists(fn) and os.path.getsize(fn) > 0):
        subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u, '-o', fn])
        time.sleep(0.8)
    return open(fn, errors='ignore').read() if os.path.exists(fn) else ''


def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()


def main():
    q = sys.argv[1]
    pat = re.compile(sys.argv[2] if len(sys.argv) > 2 else re.escape(q), re.I)
    for tpl in SITES:
        u = tpl.format(q=urllib.parse.quote(q))
        t = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', fetch(u))
        host = urllib.parse.urlparse(u).netloc
        seen = {}
        for m in re.finditer(r'(?s)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', t):
            href, txt = m.group(1), clean(m.group(2))
            ctx = clean(t[max(0, m.start() - 400):m.end() + 600])
            if len(txt) < 15 or '?s=' in href:
                continue
            if pat.search(txt):
                full = urllib.parse.urljoin(u, href)
                if host.replace('www.', '') in full and full not in seen:
                    seen[full] = txt
        print('==', host, len(seen))
        for k, v in list(seen.items())[:12]:
            print('  -', v[:160], '|', k)


main()
