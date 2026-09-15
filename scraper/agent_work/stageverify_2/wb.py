import json, math, sys, urllib.request, os, subprocess, time

S = os.path.dirname(os.path.abspath(__file__))
cfgp = S + '/wb.json'
cfg = json.load(open(cfgp))
rel = sorted([(v['itemTitle'].split('Wayback ')[-1].strip(')'), k, v['itemURL'], v['metadataLayerUrl']) for k, v in cfg.items()])


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=40).read()


def capdate(meta, lat, lng):
    u = (f"{meta}/identify?geometry={lng},{lat}&geometryType=esriGeometryPoint&sr=4326&layers=all&tolerance=1"
         f"&mapExtent={lng-0.01},{lat-0.01},{lng+0.01},{lat+0.01}&imageDisplay=800,800,96&returnGeometry=false&f=json")
    try:
        r = json.loads(get(u))['results']
        return r[0]['attributes'].get('SRC_DATE2', '?') if r else '?'
    except Exception as e:
        return 'err'


def pick(d):
    if d == 'latest':
        return rel[-1]
    return min(rel, key=lambda r: abs((int(r[0][:4]) * 12 + int(r[0][5:7])) - (int(d[:4]) * 12 + int(d[5:7]))))


name, lat, lng = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
z = int(sys.argv[4])
dates = sys.argv[5].split(',')
n = 2 ** z
lr = math.radians(lat)
X = (lng + 180) / 360 * n
Y = (1 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * n
x0 = int(X - 0.5)
y0 = int(Y - 0.5)
px, py = int((X - x0) * 256), int((Y - y0) * 256)
panels = []
for d in dates:
    c = pick(d)
    cd = capdate(c[3], lat, lng)
    tiles = []
    for dy in (0, 1):
        for dx in (0, 1):
            url = c[2].replace('{level}', str(z)).replace('{row}', str(y0 + dy)).replace('{col}', str(x0 + dx))
            fn = f'{S}/t_{c[1]}_{z}_{y0+dy}_{x0+dx}.jpg'
            if not os.path.exists(fn):
                open(fn, 'wb').write(get(url))
                time.sleep(0.2)
            tiles.append(fn)
    out = f'{S}/p_{name}_{c[0]}.png'
    subprocess.run(['magick', '(', tiles[0], tiles[1], '+append', ')', '(', tiles[2], tiles[3], '+append', ')', '-append', out], check=True)
    subprocess.run(['magick', out, '-fill', 'none', '-stroke', 'red', '-strokewidth', '3', '-draw',
                    f'circle {px},{py} {px+14},{py}', '-bordercolor', 'white', '-border', '4', out], check=True)
    panels.append(out)
    print(c[0], 'capture', cd)
final = f'{S}/{name}_z{z}.png'
subprocess.run(['magick', *panels, '+append', final], check=True)
print(final)
