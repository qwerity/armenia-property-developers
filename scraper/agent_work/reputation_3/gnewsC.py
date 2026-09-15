import sys, re, html, time, subprocess, urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for q in sys.argv[1:]:
    hl = 'hl=ru&gl=RU&ceid=RU:ru' if re.search('[а-яА-Я]', q) else ('hl=hy&gl=AM&ceid=AM:hy' if re.search('[\u0531-\u0587]', q) else 'hl=en-US&gl=US&ceid=US:en')
    u = 'https://news.google.com/rss/search?q=' + urllib.parse.quote(q) + '&' + hl
    t = subprocess.run(['curl', '-sL', '-m', '25', '-A', UA, u], capture_output=True).stdout.decode('utf-8', 'ignore')
    items = re.findall(r'<item>(.*?)</item>', t, flags=re.S)
    print('##', q, len(items))
    for it in items[:12]:
        ti = html.unescape(re.search(r'<title>(.*?)</title>', it, re.S).group(1))
        d = re.search(r'<pubDate>(.*?)</pubDate>', it)
        src = re.search(r'<source url="([^"]+)"', it)
        lk = re.search(r'<link>(.*?)</link>', it)
        print('  ', (d.group(1)[5:16] if d else ''), '|', ti[:160], '|', src.group(1) if src else '', '|', lk.group(1) if lk else '')
    time.sleep(1.5)
