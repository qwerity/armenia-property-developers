import sys, re, html, os, subprocess, time, hashlib

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
DEFAULT = r'ՍՊԸ|ՓԲԸ|ՀՎՀՀ|ООО|ЗАО|ОАО|ИНН|LLC|CJSC|L\.L\.C|Ltd|\b\d{8}\b|©|tax'


def fetch(u):
    fn = os.path.join(D, re.sub(r'[^A-Za-z0-9._-]', '_', u)[:120] + hashlib.md5(u.encode()).hexdigest()[:6] + '.html')
    if not (os.path.exists(fn) and os.path.getsize(fn) > 0):
        subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u, '-o', fn])
        time.sleep(0.6)
    return open(fn, errors='ignore').read() if os.path.exists(fn) else ''


def main():
    u = sys.argv[1]
    pat = re.compile(sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else DEFAULT, re.I)
    t = fetch(u)
    t = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', t)
    t = html.unescape(re.sub(r'<[^>]+>', '\n', t))
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    out = list(dict.fromkeys(l[:300] for l in lines if pat.search(l)))
    print(u, len(lines), 'lines')
    print('\n'.join(out[:40]))


main()
