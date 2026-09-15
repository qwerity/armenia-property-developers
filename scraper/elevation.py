"""Ground elevation (metres above sea level) for project coordinates via Open-Meteo (Copernicus DEM), cached."""
import json
import sys
import time
import urllib.request
from pathlib import Path

CACHE_FILE = Path(__file__).resolve().parent / ".elevation_cache.json"
ENDPOINT = "https://api.open-meteo.com/v1/elevation"
BATCH = 100


def _key(lat: float, lng: float) -> str:
    return f"{lat:.4f},{lng:.4f}"


def add_elevations(projects: list[dict]) -> None:
    """Set p["elevation_m"] for every project; network failures leave the field unset."""
    cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}
    missing = sorted({_key(p["lat"], p["lng"]) for p in projects} - cache.keys())
    for i in range(0, len(missing), BATCH):
        chunk = missing[i:i + BATCH]
        lats = ",".join(k.split(",")[0] for k in chunk)
        lngs = ",".join(k.split(",")[1] for k in chunk)
        values = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(f"{ENDPOINT}?latitude={lats}&longitude={lngs}", timeout=30) as r:
                    values = json.load(r).get("elevation") or []
                break
            except Exception as e:  # 429 rate limit or network: back off, then give up for this run
                print(f"elevation lookup failed ({e}), retrying", file=sys.stderr)
                time.sleep(10 * (attempt + 1))
        if values is None:
            break
        cache.update({k: v for k, v in zip(chunk, values) if isinstance(v, (int, float))})
        time.sleep(3)
    CACHE_FILE.write_text(json.dumps(cache), encoding="utf-8")
    for p in projects:
        v = cache.get(_key(p["lat"], p["lng"]))
        if v is not None:
            p["elevation_m"] = round(v)
