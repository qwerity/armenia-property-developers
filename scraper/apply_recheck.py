"""Split full re-check results (scraper/recheck_<date>_<i>.json) into price/geo/stage verification files the build applies.

Usage: python3 scraper/apply_recheck.py 20260915
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main(stamp: str) -> int:
    files = sorted(HERE.glob(f"recheck_{stamp}_*.json"))
    if not files:
        print(f"no recheck_{stamp}_*.json files", file=sys.stderr)
        return 1
    prices, geos, stages = [], [], []
    for f in files:
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except ValueError as e:
            print(f"skip {f.name}: {e}", file=sys.stderr)
            continue
        for r in rows if isinstance(rows, list) else []:
            if not isinstance(r, dict) or not r.get("id"):
                continue
            base = {"id": r["id"], "title": r.get("title")}
            if isinstance(r.get("price"), dict) and r["price"].get("verdict"):
                prices.append({**base, **r["price"]})
            loc = r.get("location") if isinstance(r.get("location"), dict) else {}
            # an "unlocatable" verdict without coordinates would drop the project from the map; keep the current pin instead
            if loc.get("verdict") and not (loc["verdict"] == "unlocatable" and loc.get("lat") is None):
                geos.append({**base, **loc})
            n = r.get("numbers") if isinstance(r.get("numbers"), dict) else {}
            if n.get("floors") or n.get("completion"):
                stages.append({**base, "stage": None, "floors": n.get("floors"), "completion": n.get("completion"),
                               "evidence_url": n.get("evidence_url"), "notes": n.get("notes")})
    for name, rows in (("price", prices), ("geo", geos), ("stage", stages)):
        (HERE / f"{name}_verified_{stamp}_full.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{name}: {len(rows)} records", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
