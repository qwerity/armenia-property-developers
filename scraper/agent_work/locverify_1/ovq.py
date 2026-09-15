import sys, subprocess, time, json

out, q = sys.argv[1], sys.argv[2]
for attempt in range(6):
    r = subprocess.run(["curl", "-s", "-m", "150", "-A", "armenia-new-builds-map/1.0",
                        "--data-urlencode", "data=" + q, "https://overpass-api.de/api/interpreter"],
                       capture_output=True, text=True).stdout
    if r.lstrip().startswith("{"):
        open(out, "w").write(r)
        d = json.loads(r)
        rows = set()
        for e in d["elements"]:
            c = e.get("center") or {"lat": e.get("lat"), "lon": e.get("lon")}
            t = e.get("tags", {})
            rows.add((t.get("name") or "", round(c["lat"], 5), round(c["lon"], 5),
                      t.get("highway") or t.get("building") or t.get("landuse") or "",
                      t.get("addr:street", ""), t.get("addr:housenumber", "")))
        for row in sorted(rows):
            print(*row)
        sys.exit(0)
    time.sleep(25)
print("FAILED")
