"""Web search via DuckDuckGo html endpoint: s.py QUERY -> title | url | snippet"""
import sys, re, html, urllib.parse, os, subprocess, time, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def main(q):
    u = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    fn = os.path.join(D, 'ddg_' + hashlib.md5(q.encode()).hexdigest() + '.html')
    if not (os.path.exists(fn) and os.path.getsize(fn) > 2000):
        subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u, '-o', fn])
        time.sleep(1.5)
    t = open(fn, errors='ignore').read()
    if 'anomaly' in t.lower() or 'captcha' in t.lower():
        print('BLOCKED (bot check) - stop')
        return
    blocks = re.findall(r'(?s)class="result__a" href="([^"]+)">(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>', t)
    if not blocks:
        print('no results', len(t))
    for href, title, snip in blocks[:10]:
        m = re.search(r'uddg=([^&]+)', href)
        url = urllib.parse.unquote(m.group(1)) if m else href
        clean = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
        print('-', clean(title), '|', url, '|', clean(snip)[:250])


main(sys.argv[1])
