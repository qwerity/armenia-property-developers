"""Address geocoding for Armenia via OpenStreetMap Nominatim (cached, rate-limited to 1 req/s)."""
import json
import re
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_FILE = Path(__file__).resolve().parent / ".geocode_cache.json"
ENDPOINT = "https://nominatim.openstreetmap.org/search"
UA = "armenia-new-builds-map/1.0 (research prototype)"
ARMENIA_BBOX = (38.8, 43.4, 41.35, 46.7)  # south, west, north, east
_lock = threading.Lock()
_last_call = 0.0
_cache: dict | None = None


def _load() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}
    return _cache


def _save() -> None:
    CACHE_FILE.write_text(json.dumps(_load(), ensure_ascii=False, indent=0), encoding="utf-8")


def _query(q: str) -> dict | None:
    global _last_call
    cache = _load()
    if q in cache:
        return cache[q]
    with _lock:
        wait = 1.1 - (time.monotonic() - _last_call)
        if wait > 0:
            time.sleep(wait)
        params = urllib.parse.urlencode({"q": q, "format": "jsonv2", "countrycodes": "am", "limit": 1, "addressdetails": 0})
        req = urllib.request.Request(f"{ENDPOINT}?{params}", headers={"User-Agent": UA, "Accept-Language": "en"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                rows = json.load(r)
        except Exception:
            _last_call = time.monotonic()
            return None  # transient failure: don't cache
        _last_call = time.monotonic()
    hit = None
    if rows:
        lat, lng = float(rows[0]["lat"]), float(rows[0]["lon"])
        s, w, n, e = ARMENIA_BBOX
        if s <= lat <= n and w <= lng <= e:
            hit = {"lat": lat, "lng": lng, "type": rows[0].get("addresstype") or rows[0].get("type"), "display": rows[0].get("display_name")}
    cache[q] = hit
    _save()
    return hit


def geocode_display(hit: dict) -> str | None:
    """Nominatim display name for a geocode() result (from cache)."""
    cached = _load().get(hit.get("query") or "")
    return cached.get("display") if cached else None


def geocode(address: str | None, city: str | None = None, district: str | None = None, accept=None) -> dict | None:
    """
    Geocode an Armenian address, progressively relaxing the query.

    Args:
        address: street address, e.g. "Aivazovsky 5".
        city: city/town, e.g. "Yerevan".
        district: optional district/community.
        accept: optional callable(hit) -> bool (hit has lat, lng, type, display) used to reject wrong matches.
    Returns:
        {"lat", "lng", "precision": "address"|"street"|"district"|"city", "query"} or None.
    """
    city = (city or "").strip() or None
    district = (district or "").strip() or None
    addr = re.sub(r"\s+", " ", (address or "")).strip() or None
    attempts = []
    if addr and re.search(r"[\u0530-\u058F\u0400-\u04FF]", addr):
        attempts.append((addr, "address"))
    if addr:
        attempts.append((", ".join(x for x in (addr, city or district, "Armenia") if x), "address"))
        street = re.sub(r"\s*\d+[\w/\-]*\s*$", "", re.sub(r"^\s*\d+[\w/\-]*\s+", "", addr)).strip()
        if street and street != addr:
            attempts.append((", ".join(x for x in (street, city or district, "Armenia") if x), "street"))
    if addr and "," in addr:
        head = addr.split(",")[0].strip()
        head_street = re.sub(r"\s*\d+[\w/\-]*\s*$", "", head).strip()
        for q in (head, head_street):
            if q and len(q) >= 4:
                attempts.append((", ".join(x for x in (q, city or district, "Armenia") if x), "address" if q == head else "street"))
    if district:
        attempts.append((", ".join(dict.fromkeys(x for x in (district, city, "Armenia") if x)), "district"))
    if city:
        attempts.append((f"{city}, Armenia", "city"))
    seen = set()
    for q, precision in attempts:
        if q in seen:
            continue
        seen.add(q)
        hit = _query(q)
        if hit and (accept is None or accept(hit)):
            return {"lat": hit["lat"], "lng": hit["lng"], "precision": precision, "query": q}
    return None
