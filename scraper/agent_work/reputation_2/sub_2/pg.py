"""pages.am lookup: pg.py search TERM [filter]  |  pg.py page URL"""
import sys, re, html, urllib.parse
sys.argv_backup = sys.argv
from importlib.machinery import SourceFileLoader
import os, subprocess, time, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def fetch(u):
    fn = os.path.join(D, re.sub(r'[^A-Za-z0-9._-]', '_', u)[:120] + hashlib.md5(u.encode()).hexdigest()[:6] + '.html')
    if not (os.path.exists(fn) and os.path.getsize(fn) > 0):
        subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u, '-o', fn])
        time.sleep(0.7)
    return open(fn, errors='ignore').read() if os.path.exists(fn) else ''


def lines(t):
    t = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', t)
    return [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if l.strip() and l.strip() not in ('">',)]


def page(u):
    L = lines(fetch(u))
    try:
        i = L.index('Organization')
        print(u, '|', ' / '.join(L[max(0, i - 12):i + 12]))
    except ValueError:
        print(u, '| no Organization block')


def search(term, flt=None):
    u = 'https://www.pages.am/en/search/?searchterm=' + urllib.parse.quote(term)
    if flt:
        u += '&search_filter%5B%5D=' + flt
    t = fetch(u)
    links = sorted(set(re.findall(r'href="(https://www.pages.am/en/pages/[^"#/]+/)"', t)))
    print('search', term, flt, '->', links)
    return links


if sys.argv[1] == 'search':
    for l in search(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)[:6]:
        page(l)
else:
    page(sys.argv[2])
