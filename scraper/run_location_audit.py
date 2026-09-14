"""Reverse-geocode every project pin and compare with its stated address -> scraper/location_audit.json."""
import json
import sys
from pathlib import Path

from build_dataset import translit
from geo_audit import distance_to_street, reverse, street_matches

ROOT = Path(__file__).resolve().parent


def main() -> int:
    projects = json.loads((ROOT.parent / "web" / "data" / "projects.json").read_text(encoding="utf-8"))["projects"]
    rows = []
    for i, p in enumerate(projects):
        rev = reverse(p["lat"], p["lng"])
        addrs = [o.get("address") for o in p.get("geo_obs") or [] if o.get("address")] + [p.get("address")]
        verdicts = [street_matches(a, rev, translit) for a in addrs if a]
        match = True if True in verdicts else (False if False in verdicts else None)
        city = "Yerevan" if p.get("region") == "Yerevan" else p.get("district")
        dists = [distance_to_street(p["lat"], p["lng"], a, city) for a in dict.fromkeys(addrs) if a]
        known = [(d, n) for d, n in dists if d is not None]
        street_dist, street_name = min(known) if known else (None, next((n for _, n in dists if n), None))
        rows.append({"street_dist_m": round(street_dist) if street_dist is not None else None, "street_name": street_name,"id": p["id"], "title": p["title"], "address": p.get("address"), "lat": p["lat"], "lng": p["lng"],
                     "geo_precision": p.get("geo_precision"), "pin_road": (rev or {}).get("road"), "pin_suburb": (rev or {}).get("suburb"),
                     "pin_city": (rev or {}).get("city"), "street_match": match, "spread_m": p.get("geo_spread_m"),
                     "location_note": p.get("location_note"), "district": p.get("district"), "region": p.get("region"),
                     "sources": [s["url"] for s in p["sources"] if s.get("url")]})
        if i % 50 == 0:
            print(f"{i}/{len(projects)}", file=sys.stderr, flush=True)
    (ROOT / "location_audit.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
