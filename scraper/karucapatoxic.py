"""Scrape all new-building projects from karucapatoxic.am (Next.js RSC payloads).

Output: ../web/data/karucapatoxic.json — list of normalized project dicts.
"""
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = "https://karucapatoxic.am"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"
OUT = Path(__file__).resolve().parent.parent / "web" / "data" / "karucapatoxic.json"
CACHE = Path(__file__).resolve().parent / ".cache"
_DEC = json.JSONDecoder()


def fetch(path: str, retries: int = 3) -> str:
    """Fetch a page with on-disk caching and retry/backoff."""
    CACHE.mkdir(exist_ok=True)
    cf = CACHE / (re.sub(r"[^a-zA-Z0-9]+", "_", path).strip("_") + ".html")
    if cf.exists() and cf.stat().st_size > 1000:
        return cf.read_text(encoding="utf-8")
    for attempt in range(retries):
        try:
            req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                html = r.read().decode("utf-8")
            cf.write_text(html, encoding="utf-8")
            return html
        except Exception as e:  # network errors, 5xx
            if attempt == retries - 1:
                raise RuntimeError(f"fetch {path} failed: {e}") from e
            time.sleep(2 ** attempt)
    return ""


def rsc_text(html: str) -> str:
    """Concatenate the Next.js flight payload chunks embedded in the HTML."""
    parts = re.findall(r'self\.__next_f\.push\(\[1,(".*?")\]\)</script>', html, re.S)
    return "".join(json.loads(p) for p in parts)


def iter_objects(txt: str, anchor: str):
    """Yield JSON objects whose text starts at each occurrence of `anchor`."""
    for m in re.finditer(re.escape(anchor), txt):
        try:
            obj, _ = _DEC.raw_decode(txt[m.start():])
        except ValueError:
            continue
        if isinstance(obj, dict):
            yield obj


def list_buildings() -> list[dict]:
    txt = rsc_text(fetch("/en"))
    i = txt.find('"listBuildings":[')
    if i < 0:
        raise RuntimeError("listBuildings not found on /en")
    arr, _ = _DEC.raw_decode(txt[i + len('"listBuildings":'):])
    return arr


def marker_from_embed(url: str | None) -> tuple[float | None, float | None]:
    """Marker position from a Google Maps embed's base64 `!2z` DMS label (e.g. 40°14'52.6"N 44°30'56.8"E)."""
    import base64
    m = re.search(r"!2z([A-Za-z0-9+/_-]+=*)", url or "")
    if not m:
        return None, None
    try:
        label = base64.b64decode(m.group(1) + "=" * (-len(m.group(1)) % 4), altchars=b"-_").decode("utf-8", "replace")
    except ValueError:
        return None, None
    dms = re.findall(r"(\d+)°(\d+)'([\d.]+)\"([NSEW])", label)
    if len(dms) != 2:
        return None, None
    vals = {}
    for deg, mins, sec, hemi in dms:
        v = int(deg) + int(mins) / 60 + float(sec) / 3600
        vals["lat" if hemi in "NS" else "lng"] = -v if hemi in "SW" else v
    return vals.get("lat"), vals.get("lng")


def coords_from_embed(url: str | None) -> tuple[float | None, float | None]:
    """Viewport centre of a Google Maps embed (offset from the marker; use marker_from_embed first)."""
    if not url:
        return None, None
    lng = re.search(r"!2d(-?\d+\.\d+)", url)
    lat = re.search(r"!3d(-?\d+\.\d+)", url)
    return (float(lat.group(1)), float(lng.group(1))) if lat and lng else (None, None)


def building_detail(bid: str) -> dict:
    """Return the full building object, JSON-LD listing and breadcrumb for one project."""
    html = fetch(f"/en/{bid}")
    txt = rsc_text(html)
    detail: dict = {}
    for o in sorted(iter_objects(txt, '{"id":"%s"' % bid), key=len):
        detail.update({k: v for k, v in o.items() if v not in (None, "", [], {})})
    ld, crumbs = {}, []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            j = json.loads(raw)
        except ValueError:
            continue
        if j.get("@type") == "RealEstateListing":
            ld = j
        elif j.get("@type") == "BreadcrumbList":
            crumbs = [e.get("name") for e in j.get("itemListElement", [])]
    return {"detail": detail, "ld": ld, "crumbs": crumbs}


def developer_info(slug: str) -> dict:
    txt = rsc_text(fetch(f"/en/{slug}"))
    for o in iter_objects(txt, '{"id":'):
        if o.get("url") == slug and "name" in o:
            return o
    return {}


def clean(s):
    return s.strip() if isinstance(s, str) and s.strip() else None


def normalize(base: dict, extra: dict) -> dict:
    d, ld = extra["detail"], extra["ld"]
    about = ld.get("about", {})
    geo = about.get("geo") or {}
    embed = d.get("googleMap") or base.get("googleMap")
    lat, lng = marker_from_embed(embed)
    if lat is None:
        lat, lng = geo.get("latitude"), geo.get("longitude")
    if lat is None:
        lat, lng = coords_from_embed(embed)
    addr = about.get("address", {})
    provider = ld.get("provider", {})
    price = d.get("price") or base.get("price") or {}
    social = {k: clean(d.get(k)) for k in ("facebook", "instagram", "telegram", "youtube", "tiktok") if clean(d.get(k))}
    return {
        "id": f"kp-{base['id']}",
        "source": "karucapatoxic",
        "source_url": f"{BASE}/en/{base['id']}",
        "title": clean(base.get("title_en")) or clean(base.get("title_ru")) or clean(base.get("title_am")),
        "title_am": clean(base.get("title_am")),
        "title_ru": clean(base.get("title_ru")),
        "developer": clean(provider.get("name")),
        "developer_slug": (provider.get("url") or "").rstrip("/").rsplit("/", 1)[-1] or None,
        "region": clean(addr.get("addressRegion")),
        "district": clean(addr.get("addressLocality")) or (extra["crumbs"][1] if len(extra["crumbs"]) > 2 else None),
        "address": clean(d.get("address_en")) or clean(base.get("address_en")),
        "sales_address": clean(d.get("sales_address_en")),
        "lat": lat,
        "lng": lng,
        "price_m2_min": price.get("min"),
        "price_m2_max": price.get("max"),
        "currency": price.get("currency"),
        "min_apartment_price": d.get("minApartmentPrice") or base.get("minApartmentPrice"),
        "min_area_m2": base.get("minApartmentPriceSquare"),
        "completion": (d.get("endDate") or base.get("endDate") or "")[:10] or None,
        "start": (d.get("startDate") or "")[:10] or None,
        "sold_out": bool(d.get("soldOut")),
        "address_am": clean(d.get("address_am")),
        "property_condition": d.get("propertyCondition"),
        "prices_by_floor": [
            {"floors": clean(x.get("floors")), "rooms": clean(x.get("rooms")), "price": x.get("price")}
            for x in d.get("prices") or [] if isinstance(x, dict) and x.get("price")
        ],
        "prices_by_rooms": [x for x in d.get("pricesByType") or [] if isinstance(x, dict)],
        "floors": clean(d.get("floors")),
        "active": base.get("active"),
        "is_new": base.get("new"),
        "type": base.get("type"),
        "income_tax_refund": (d.get("incomeTaxRefund") or base.get("incomeTaxRefund")) == "yes",
        "renovation": clean(d.get("renovation")) if isinstance(d.get("renovation"), str) else d.get("renovation"),
        "phones": d.get("phones") or [],
        "email": clean(d.get("email")),
        "website": clean(d.get("link")),
        "social": social,
        "working_hours": d.get("workingHours") or [],
        "images": base.get("images") or d.get("images") or [],
        "videos": [v for v in (d.get("videos") or []) if isinstance(v, str)],
        "description": clean(ld.get("description")),
        "popularity": base.get("gaActiveUsers"),
        "price_updated": (d.get("priceUpdated") or "")[:10] or None,
    }


def main() -> int:
    buildings = list_buildings()
    print(f"{len(buildings)} buildings listed", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=4) as ex:
        extras = list(ex.map(lambda b: building_detail(b["id"]), buildings))
    projects = [normalize(b, e) for b, e in zip(buildings, extras)]
    slugs = sorted({p["developer_slug"] for p in projects if p["developer_slug"]})
    with ThreadPoolExecutor(max_workers=4) as ex:
        devs = dict(zip(slugs, ex.map(developer_info, slugs)))
    for p in projects:
        dev = devs.get(p["developer_slug"] or "", {})
        p["developer_website"] = clean(dev.get("link"))
        p["developer_logo"] = (BASE + dev["logo"]) if isinstance(dev.get("logo"), str) and dev["logo"].startswith("/") else dev.get("logo")
        p["developer_about"] = (dev.get("description") or {}).get("en") if isinstance(dev.get("description"), dict) else None
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(projects, ensure_ascii=False, indent=1), encoding="utf-8")
    missing = sum(1 for p in projects if p["lat"] is None)
    print(f"wrote {len(projects)} projects ({missing} without coords), {len(devs)} developers -> {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
