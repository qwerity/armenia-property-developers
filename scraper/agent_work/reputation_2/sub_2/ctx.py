"""ctx.py URL REGEX [before] [after] -> print lines around matches (uses f.py cache)."""
import sys, re, html, os, hashlib

D = os.path.dirname(os.path.abspath(__file__))
u, pat = sys.argv[1], re.compile(sys.argv[2], re.I)
b = int(sys.argv[3]) if len(sys.argv) > 3 else 3
a = int(sys.argv[4]) if len(sys.argv) > 4 else 6
fn = os.path.join(D, re.sub(r'[^A-Za-z0-9._-]', '_', u)[:120] + hashlib.md5(u.encode()).hexdigest()[:6] + '.html')
t = open(fn, errors='ignore').read()
t = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', t)
L = [l.strip() for l in html.unescape(re.sub(r'<[^>]+>', '\n', t)).split('\n') if l.strip()]
for i, l in enumerate(L):
    if pat.search(l):
        print(i, ' / '.join(x[:150] for x in L[max(0, i - b):i + a]))
