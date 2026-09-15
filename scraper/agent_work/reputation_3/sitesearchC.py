import sys, re, html, time, subprocess, urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
SITES = {
    'azatutyun': ('https://www.azatutyun.am/s?k={q}&tab=all', r'href="(/a/[^"]+\.html)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{8,200})'),
    'hetq': ('https://hetq.am/hy/search?q={q}', r'href="(https://hetq\.am/hy/article/[^"]+)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{8,200})'),
    'civilnet': ('https://www.civilnet.am/?s={q}', r'href="(https://www\.civilnet\.am/news/[^"]+)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{8,200})'),
    'news.am': ('https://news.am/arm/search/?q={q}', r'href="((?:https://news\.am)?/arm/news/\d+\.html)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{8,200})'),
    'armtimes': ('https://www.armtimes.com/hy/search?q={q}', r'href="(https://www\.armtimes\.com/hy/article/\d+)"[^>]*>\s*(?:<[^>]+>\s*)*([^<]{8,200})'),
}
args = sys.argv[1:]
sites = list(SITES)
if args and args[0].startswith('--sites='):
    sites = args[0][8:].split(','); args = args[1:]
for q in args:
    for s in sites:
        url, pat = SITES[s]
        u = url.format(q=urllib.parse.quote(q))
        t = subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u], capture_output=True).stdout.decode('utf-8', 'ignore')
        hits = []
        seen = set()
        for m in re.finditer(pat, t, flags=re.S):
            if m.group(1) in seen:
                continue
            seen.add(m.group(1))
            hits.append((m.group(1), re.sub(r'\s+', ' ', html.unescape(m.group(2))).strip()))
        print(f'## {s} [{q}] len={len(t)} hits={len(hits)}')
        for h in hits[:10]:
            print('   ', h[1][:150], '|', h[0])
        time.sleep(0.8)
