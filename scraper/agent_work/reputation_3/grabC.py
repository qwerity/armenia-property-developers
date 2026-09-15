import sys, re, html, time, subprocess

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
PATS = r'ՍՊԸ|ՓԲԸ|ԲԲԸ|ՀՎՀՀ|ՀՎՀ|ՍՊ ընկեր|LLC|ООО|CJSC|OJSC|Ltd|LTD|ИНН|[Tt]ax ID|TIN|\b\d{8}\b|©|[Կկ]առուցապատող|Застройщик|[Dd]eveloper'
extra = None
urls = []
for a in sys.argv[1:]:
    if a.startswith('--pat='):
        extra = a[6:]
    else:
        urls.append(a)
pats = PATS + ('|' + extra if extra else '')
for u in urls:
    print('===', u)
    try:
        t = subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u], capture_output=True, timeout=40).stdout.decode('utf-8', 'ignore')
    except Exception as e:
        print('  ERR', e); continue
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'\s+', ' ', t)
    print('  len', len(t))
    seen = set(); n = 0
    for m in re.finditer(pats, t):
        s = t[max(0, m.start() - 90):m.end() + 90]
        k = t[max(0, m.start() - 20):m.end() + 20]
        if k in seen:
            continue
        seen.add(k); print('  ..', s); n += 1
        if n > 30:
            break
    time.sleep(0.6)
