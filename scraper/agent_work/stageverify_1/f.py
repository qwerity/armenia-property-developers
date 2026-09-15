import sys, re, html, subprocess, math, json, os

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
D = os.path.dirname(os.path.abspath(__file__))


def get(url, raw=False):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, "-H", "Accept: text/html,*/*",
                        "-H", "Accept-Language: en", url], capture_output=True)
    t = r.stdout.decode("utf-8", "replace")
    if raw:
        return t
    t = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)


def tile(lat, lng, z, rel, name):
    n = 2 ** z
    x = int((lng + 180) / 360 * n)
    lr = math.radians(lat)
    y = int((1 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * n)
    url = f"https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{rel}/{z}/{y}/{x}"
    out = os.path.join(D, name)
    subprocess.run(["curl", "-s", "--max-time", "40", "-A", UA, "-o", out, url])
    # pin pixel position within tile
    fx = ((lng + 180) / 360 * n - x) * 256
    fy = ((1 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * n - y) * 256
    return out, int(fx), int(fy)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "get":
        t = get(sys.argv[2])
        pat = sys.argv[3] if len(sys.argv) > 3 else None
        if pat:
            c = int(sys.argv[4]) if len(sys.argv) > 4 else 200
            last = -10**9
            for m in re.finditer(pat, t, re.I):
                if m.start() - last < c:
                    continue
                last = m.start()
                print("...", t[max(0, m.start() - c):m.end() + c])
        else:
            print(t[: int(sys.argv[4]) if len(sys.argv) > 4 else 6000])
    elif cmd == "raw":
        print(get(sys.argv[2], raw=True)[:int(sys.argv[3]) if len(sys.argv) > 3 else 20000])
    elif cmd == "tile":
        lat, lng, z, rel, name = float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
        print(tile(lat, lng, z, rel, name))
