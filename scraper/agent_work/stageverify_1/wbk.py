import sys, math, subprocess, os, json, time

D = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
WB = json.load(open(os.path.join(D, "wb.json")))
TITLE = {k: v["itemTitle"].split("Wayback ")[1].rstrip(")") for k, v in WB.items()}


def frac(lat, lng, z):
    n = 2 ** z
    lr = math.radians(lat)
    return (lng + 180) / 360 * n, (1 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * n


def mosaic(name, lat, lng, rel, z=18):
    fx, fy = frac(lat, lng, z)
    x0 = int(fx) - (1 if fx - int(fx) < 0.5 else 0)
    y0 = int(fy) - (1 if fy - int(fy) < 0.5 else 0)
    parts = []
    for dy in (0, 1):
        for dx in (0, 1):
            p = os.path.join(D, f"u_{rel}_{z}_{x0+dx}_{y0+dy}.jpg")
            if not os.path.exists(p) or os.path.getsize(p) < 500:
                url = f"https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{rel}/{z}/{y0+dy}/{x0+dx}"
                r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, "-o", p, "-w", "%{url_effective}", url], capture_output=True, text=True)
                eff = r.stdout.split("/tile/")[1].split("/")[0] if "/tile/" in r.stdout else rel
                open(p + ".rel", "w").write(eff)
                time.sleep(0.3)
            parts.append(p)
    effs = sorted({open(q + ".rel").read() for q in parts if os.path.exists(q + ".rel")})
    print(name, "req", TITLE[rel], "-> effective", [TITLE.get(e, e) for e in effs])
    px, py = (fx - x0) * 256, (fy - y0) * 256
    out = os.path.join(D, f"m_{name}_{rel}.png")
    subprocess.run(["magick", "(", parts[0], parts[1], "+append", ")", "(", parts[2], parts[3], "+append", ")",
                    "-append", "-fill", "none", "-stroke", "red", "-strokewidth", "2",
                    "-draw", f"circle {px},{py} {px+12},{py}",
                    out])
    return out


if __name__ == "__main__":
    name, lat, lng = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    rels = sys.argv[4].split(",")
    z = int(sys.argv[5]) if len(sys.argv) > 5 else 18
    outs = [mosaic(name, lat, lng, r, z) for r in rels]
    final = os.path.join(D, f"cmp_{name}.png")
    subprocess.run(["magick"] + outs + ["+append", final])
    print(final)
