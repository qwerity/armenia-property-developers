"""Location consensus across sources and reverse-geocode street checks."""
import json
import re
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_FILE = Path(__file__).resolve().parent / ".reverse_cache.json"
UA = "armenia-new-builds-map/1.0 (research prototype)"
CLUSTER_M = 150
DISAGREE_M = 300
GEO_WEIGHT = {
    "myhome.am": 3, "redgroup.am": 2.5, "redinvest.am": 2.5, "karucapatoxic.am": 2, "construction.am": 1.5,
    "ar-go.am": 1.5, "dignisi.am": 1, "ac-box.com": 1, "yerevan.etagi.com": 1, "novostroiki-yerevan.com": 0.5, "geoln.com": 0.5,
}
DEVELOPER_SITE_WEIGHT = 3
_lock = threading.Lock()
_last = 0.0
_cache: dict | None = None


def _haversine(a, b) -> float:
    from math import asin, cos, radians, sin, sqrt
    la1, lo1, la2, lo2 = map(radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = sin((la2 - la1) / 2) ** 2 + cos(la1) * cos(la2) * sin((lo2 - lo1) / 2) ** 2
    return 12742000 * asin(sqrt(h))


def location_consensus(obs: list[dict]) -> dict | None:
    """
    Pick the best-supported coordinate among per-source observations.

    Identical coordinates copied between aggregators count once. Returns
    {"lat","lng","spread_m","support","sources"} or None when there are no observations.
    """
    uniq = {}
    for o in obs:
        if not (38.8 <= o["lat"] <= 41.4 and 43.3 <= o["lng"] <= 46.7):
            continue
        key = (round(o["lat"], 5), round(o["lng"], 5))
        w = GEO_WEIGHT.get(o["source"], DEVELOPER_SITE_WEIGHT)
        if key not in uniq or w > uniq[key]["w"]:
            uniq[key] = {**o, "w": w}
    pts = list(uniq.values())
    if not pts:
        return None
    best, best_w = [], 0.0
    for c in pts:
        group = [q for q in pts if _haversine(c, q) <= CLUSTER_M]
        w = sum(q["w"] for q in group)
        if w > best_w:
            best, best_w = group, w
    total_w = sum(q["w"] for q in best)
    lat = sum(q["lat"] * q["w"] for q in best) / total_w
    lng = sum(q["lng"] * q["w"] for q in best) / total_w
    spread = max((_haversine(a, b) for a in pts for b in pts), default=0)
    return {"lat": lat, "lng": lng, "spread_m": round(spread), "support": [q["source"] for q in best],
            "outliers": [q["source"] for q in pts if q not in best]}


def _load() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}
    return _cache


def reverse(lat: float, lng: float) -> dict | None:
    """Nominatim reverse geocode (cached, 1 req/s): {"road","suburb","city","display"}."""
    global _last
    key = f"{lat:.5f},{lng:.5f}"
    cache = _load()
    if key in cache:
        return cache[key]
    with _lock:
        wait = 1.1 - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        q = urllib.parse.urlencode({"lat": lat, "lon": lng, "format": "jsonv2", "zoom": 17, "addressdetails": 1})
        req = urllib.request.Request(f"https://nominatim.openstreetmap.org/reverse?{q}", headers={"User-Agent": UA, "Accept-Language": "en"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
        except Exception:
            _last = time.monotonic()
            return None
        _last = time.monotonic()
    a = d.get("address") or {}
    out = {"road": a.get("road") or a.get("pedestrian") or a.get("residential"), "suburb": a.get("suburb") or a.get("quarter"),
           "city": a.get("city") or a.get("town") or a.get("village"), "display": d.get("display_name")}
    cache[key] = out
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    return out


STREET_STOP = r"street|str|st|avenue|ave|pogh|poghots|lane|nrbants|district|block|thaghamas|village|city|yerevan|armenia|kotayk|the|of|and|residential|complex|building"


def street_tokens(text: str, translit) -> set[str]:
    t = translit(text or "")
    t = re.sub(r"\d+[\w/.-]*", " ", t)
    words = re.findall(r"[a-z]{4,}", t)
    norm = lambda w: w.replace("kh", "k").replace("gh", "g").replace("y", "i").replace("ts", "c").replace("q", "k")[:6]  # noqa: E731
    return {norm(w) for w in words if not re.fullmatch(STREET_STOP, w)}


def street_matches(address: str, rev: dict, translit) -> bool | None:
    """True/False when the address names a street we can compare with the pin's reverse-geocoded road; None if unknown."""
    if not rev or not address:
        return None
    addr = street_tokens(address, translit)
    road = street_tokens(" ".join(x for x in (rev.get("road"), rev.get("suburb")) if x), translit)
    if not addr or not road:
        return None
    return bool(addr & road)


STREET_CACHE = Path(__file__).resolve().parent / ".street_cache.json"
_street_cache: dict | None = None


def _street_name(address: str) -> str | None:
    """Street part of an address: prefer the chunk carrying a house number or a street keyword."""
    from geo_admin import DISTRICT_PATTERNS, TOWN_PATTERNS, PROVINCE_NAMES
    a = re.sub(r"\([^)]*\)", " ", address or "")
    a = re.sub(r"(?i)^\s*between\s+", "", a)
    parts = [x.strip() for x in re.split(r"[,;]", a) if x.strip()]
    places = "|".join(list(DISTRICT_PATTERNS.values()) + list(TOWN_PATTERNS.values()) + list(PROVINCE_NAMES.values()))
    scored = []
    for idx, part in enumerate(parts):
        has_no = bool(re.search(r"\d", part))
        has_kw = bool(re.search(r"(?i)street|\bst\b\.?|avenue|ave\b|lane|փ\.|փողոց|պող|ул\.|улица|пр\.", part))
        name = re.sub(r"\b\d+[\w/.\-]*\b|\d+", " ", part)
        name = re.sub(r"(?i)\b(h\.|house|building|bldg|block|lot|plot|apt\.?|no\.?|street|st\.?|ave\.?|avenue|lane|th|rd|nd)\b|ք\.|փ\.|գ\.|փողոց|թաղամաս|համայնք|մարզ", " ", name)
        name = re.sub(r"(?<!\w)[A-ZԱ-Ֆ]\.\s*", " ", name)
        name = re.sub(r"\s+", " ", name).strip(" .-")
        letters = re.sub(r"[^A-Za-zԱ-ևЀ-ӿ]", "", name)
        if len(letters) < 4 or re.fullmatch(r"(?i)(%s)" % places, name.strip()) or re.search(r"(?i)region|community|village|complex|residential|district", name):
            continue
        scored.append((has_no * 2 + has_kw, -idx, name))
    return max(scored)[2] if scored else None


def _nominatim_lines(query: str) -> list[list[tuple[float, float]]]:
    global _last, _street_cache
    if _street_cache is None:
        _street_cache = json.loads(STREET_CACHE.read_text(encoding="utf-8")) if STREET_CACHE.exists() else {}
    if query in _street_cache:
        return _street_cache[query]
    with _lock:
        wait = 1.1 - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        q = urllib.parse.urlencode({"q": query, "format": "jsonv2", "countrycodes": "am", "limit": 5, "polygon_geojson": 1, "polygon_threshold": 0.00005})
        req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?{q}", headers={"User-Agent": UA, "Accept-Language": "en"})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                rows = json.load(r)
        except Exception:
            _last = time.monotonic()
            return []
        _last = time.monotonic()
    lines = []
    for row in rows:
        g = row.get("geojson") or {}
        coords = g.get("coordinates")
        if g.get("type") == "LineString":
            lines.append([(c[1], c[0]) for c in coords])
        elif g.get("type") == "MultiLineString":
            lines += [[(c[1], c[0]) for c in ln] for ln in coords]
        elif g.get("type") == "Point":
            lines.append([(coords[1], coords[0])])
    _street_cache[query] = lines
    STREET_CACHE.write_text(json.dumps(_street_cache), encoding="utf-8")
    return lines


def distance_to_street(lat: float, lng: float, address: str, city: str | None) -> tuple[float | None, str | None]:
    """Metres from the pin to the nearest vertex/segment of the street named in the address (None if street not found)."""
    name = _street_name(address)
    if not name:
        return None, None
    lines = _nominatim_lines(", ".join(x for x in (name, city, "Armenia") if x))
    if not lines:
        return None, name
    pin = {"lat": lat, "lng": lng}
    best = None
    for ln in lines:
        for i, (la, lo) in enumerate(ln):
            d = _haversine(pin, {"lat": la, "lng": lo})
            if i:
                pla, plo = ln[i - 1]
                for t in (0.25, 0.5, 0.75):
                    d = min(d, _haversine(pin, {"lat": pla + (la - pla) * t, "lng": plo + (lo - plo) * t}))
            best = d if best is None else min(best, d)
    return best, name
