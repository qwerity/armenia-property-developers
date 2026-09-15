import sys, re, json, subprocess, urllib.parse, time

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def curl(args):
    return subprocess.run(['curl', '-sL', '-m', '25', '-A', UA] + args, capture_output=True).stdout.decode('utf-8', 'ignore')


def decode(link):
    gid = re.search(r'articles/([^?]+)', link).group(1)
    page = curl([f'https://news.google.com/articles/{gid}'])
    sg = re.search(r'data-n-a-sg="([^"]+)"', page)
    ts = re.search(r'data-n-a-ts="([^"]+)"', page)
    if not sg or not ts:
        return None
    inner = ["garturlreq", [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1], "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0], gid, int(ts.group(1)), sg.group(1)]
    freq = json.dumps([[["Fbv4je", json.dumps(inner), None, "generic"]]])
    r = curl(['-X', 'POST', 'https://news.google.com/_/DotsSplashUi/data/batchexecute',
              '-H', 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8',
              '--data', 'f.req=' + urllib.parse.quote(freq)])
    m = re.search(r'garturlres\\",\\"(.*?)\\"', r)
    return m.group(1) if m else r[:200]


for l in sys.argv[1:]:
    print(decode(l))
    time.sleep(1)
