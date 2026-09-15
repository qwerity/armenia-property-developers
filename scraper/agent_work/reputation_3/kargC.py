import sys, re, html, time, json, subprocess, urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def get(u):
    time.sleep(0.6)
    return subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u], capture_output=True, timeout=40).stdout.decode('utf-8', 'ignore')


def card(tid):
    t = get(f'https://karg.am/company/{tid}?lang=hy')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
    out = {}
    for k, p in [('status', r'Կարգավիճակ (\S+)'), ('reg', r'Գրանցման ամսաթիվ (\d\d\.\d\d\.\d{4})'),
                 ('form', r'Կազմակերպաիրավական ձև (.*?) Իրավաբանական'), ('addr', r'Իրավաբանական հասցե (.*?) (?:Հարկման|Ղեկավար|Գործունեության)'),
                 ('head', r'Ղեկավար (.*?) (?:Հարկման|Գործունեության|Իրավաբանական)'), ('cases', r'Դատական գործեր (\d+)')]:
        m = re.search(p, t)
        out[k] = m.group(1)[:120] if m else None
    m = re.search(r'Հիմնադիրներ Աղբյուր՝ \S+ \(BOR\) (.*?) (?:Նման ընկերություններ|Մարզերի)', t)
    out['founders'] = m.group(1)[:300] if m else None
    return out


for q in sys.argv[1:]:
    detail = q.startswith('!')
    q = q.lstrip('!')
    if re.fullmatch(r'\d{8}', q):
        print(q, card(q)); continue
    try:
        j = json.loads(get('https://karg.am/api/autocomplete.php?q=' + urllib.parse.quote(q)))
    except Exception as e:
        print('ERR', q, e); continue
    print('##', q)
    for g in j.get('groups', []):
        for it in g['items'][:8]:
            if it.get('type') == 'company':
                line = f"  {it['text']} {it['tax_id']}"
                if detail:
                    line += ' ' + json.dumps(card(it['tax_id']), ensure_ascii=False)
                print(line)
            else:
                print('   P:', it['text'], '|', it.get('role'))
