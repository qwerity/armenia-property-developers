"""Summarise myhome.am primary apartments API for building ids: python3 mh.py 257 57 ..."""
import sys, json, subprocess, time, collections

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for bid in sys.argv[1:]:
    out = subprocess.run(["curl", "-s", "--compressed", "-m", "30", "-H", "User-Agent: " + UA, "-H", "Accept: application/json",
                          "-H", "Accept-Language: en", f"https://myhome.am/API/v1/apartments/primary/{bid}"], capture_output=True, text=True).stdout
    time.sleep(0.6)
    try:
        floors = json.loads(out)
    except Exception:
        print(bid, "bad json", out[:200]); continue
    apts = [a for f in floors for a in f.get("apartments", [])]
    st = collections.Counter(a["globalAccessibilityState"] for a in apts)
    print(f"== building {bid}: {len(apts)} units, states {dict(st)}")
    for s in sorted(st):
        g = [a for a in apts if a["globalAccessibilityState"] == s]
        pr = [a for a in g if a.get("minAreaPrice")]
        if not pr:
            print(f"  state {s}: no prices"); continue
        m2 = min(pr, key=lambda a: a["minAreaPrice"])
        tot = min(pr, key=lambda a: a["minApartmentPrice"] or 9e18)
        print(f"  state {s}: n={len(g)} priced={len(pr)} min m2={m2['minAreaPrice']:,.0f} ({m2['area']} m2, total {m2['minApartmentPrice']:,.0f}) | cheapest total={tot['minApartmentPrice']:,.0f} area {tot['area']} m2price {tot['minAreaPrice']:,.0f}")
