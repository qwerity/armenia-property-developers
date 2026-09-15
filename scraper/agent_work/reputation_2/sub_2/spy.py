"""spyur.am name search: spy.py NAME -> company links, then legal form / year / director from each."""
import sys, re, html, urllib.parse, os, subprocess, time, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"


def fetch(u):
    fn = os.path.join(D, 'spy_' + hashlib.md5(u.encode()).hexdigest() + '.html')
    if not (os.path.exists(fn) and os.path.getsize(fn) > 0):
        subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u, '-o', fn])
        time.sleep(0.8)
    return open(fn, errors='ignore').read() if os.path.exists(fn) else ''


def lines(t):
    t = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', t)
    return [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if l.strip()]


name = sys.argv[1]
u = 'https://www.spyur.am/' + os.environ.get('SL','en') + '/home/search/?company_name=' + urllib.parse.quote(name) + '&addres='
t = fetch(u)
links = list(dict.fromkeys(re.findall(r'href="(/(?:en|am)/companies/[^"]+/\d+)/?"', t)))
print('search', name, '->', links[:8])
for l in links[:5]:
    L = lines(fetch("https://www.spyur.am" + l + "/"))
    keep = [x for i, x in enumerate(L) if re.search(r'\((LLC|CJSC|OJSC|SP|PE)\)|Director|Year established|^\d\d\.\d\d\.\d{4}$|Activit', x)]
    idx = [i for i, x in enumerate(L) if x == 'Year established']
    extra = L[idx[0]:idx[0] + 2] if idx else []
    print('  ', l, '|', ' / '.join(dict.fromkeys(keep[:8] + extra)))
