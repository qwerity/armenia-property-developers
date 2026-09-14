"""Merge scraped sources into web/data/projects.json with derived analytics.

Adds: normalized USD/AMD prices, inferred developer groups, status, deduplication
across sources, and a per-district price benchmark used for "opportunity" ranking.
"""
import json
import math
import re
import statistics
import sys
import urllib.request
from collections import defaultdict
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

from geo_admin import locate, mentioned_place, normalize_town, province_hint
from geocode import geocode, geocode_display
from price_audit import implied_observation, observation, reconcile

ROOT = Path(__file__).resolve().parent.parent
KP = ROOT / "web" / "data" / "karucapatoxic.json"
EXTRA_FILES = [ROOT / "scraper" / "extra_sources.json", *sorted((ROOT / "scraper").glob("developer_projects*.json"))]
ENRICH = ROOT / "scraper" / "website_enrichment.json"
DEVELOPERS = ROOT / "scraper" / "developers_master.json"
GEO_OVERRIDES_FILE = ROOT / "scraper" / "geo_overrides.json"
GEO_OVERRIDES = json.loads(GEO_OVERRIDES_FILE.read_text(encoding="utf-8")) if GEO_OVERRIDES_FILE.exists() else {}
OUT = ROOT / "web" / "data" / "projects.json"
FALLBACK_AMD_PER_USD = 385.0
GENERIC_DOMAINS = {
    "facebook.com", "instagram.com", "t.me", "gmail.com", "mail.ru", "yandex.ru", "yahoo.com",
    "dignisi.am", "norakaruyc.info", "hsbc.am", "list.am", "google.com", "company-name",
}
SOURCE_NAMES = {"dignisi": "dignisi.am", "geoln": "geoln.com", "ac-box": "ac-box.com", "etagi": "yerevan.etagi.com"}
TYPE_LABELS = {"1": "Apartments", "2": "Houses / townhouses"}


def amd_per_usd() -> tuple[float, str]:
    try:
        with urllib.request.urlopen("https://open.er-api.com/v6/latest/USD", timeout=15) as r:
            d = json.load(r)
        return float(d["rates"]["AMD"]), d.get("time_last_update_utc", "")
    except Exception as e:
        print(f"rate fetch failed ({e}); using fallback", file=sys.stderr)
        return FALLBACK_AMD_PER_USD, "fallback"


def num(v) -> float | None:
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v) if v > 0 and math.isfinite(v) else None
    m = re.search(r"\d[\d\s,]*\.?\d*", str(v))
    if not m:
        return None
    try:
        f = float(m.group(0).replace(" ", "").replace(",", ""))
    except ValueError:
        return None
    return f if f > 0 else None


def registrable_domain(url: str | None) -> str | None:
    if not url:
        return None
    host = urlparse(url if "://" in url else "http://" + url).netloc.lower().removeprefix("www.")
    parts = host.split(".")
    return ".".join(parts[-2:]) if len(parts) >= 2 else None


def humanize(key: str) -> str:
    key = re.sub(r"\.(am|com|ru|net|org|info)$", "", key)
    key = re.sub(r"\d+$", "", key)
    key = re.sub(r"(llc|ltd)$", "", key)
    return " ".join(w.capitalize() for w in re.split(r"[._\-]+", key) if w) or key


def infer_developer(p: dict) -> tuple[str, bool]:
    """Group projects without a named developer by website/email/facebook identity."""
    if p.get("developer"):
        return p["developer"], False
    dom = registrable_domain(p.get("website"))
    if dom and dom not in GENERIC_DOMAINS:
        return humanize(dom.split(".")[0]), True
    email = (p.get("email") or "").lower().strip()
    if "@" in email:
        local, edom = email.split("@", 1)
        if edom not in GENERIC_DOMAINS and not edom.startswith("company-name"):
            return humanize(edom.split(".")[0]), True
        if local not in {"company-name", "info", "sales"}:
            return humanize(local), True
    fb = (p.get("social") or {}).get("facebook") or ""
    m = re.search(r"facebook\.com/(?!profile\.php|groups|p/)([A-Za-z0-9.\-]+)", fb)
    if m:
        return humanize(m.group(1)), True
    return "Unknown developer", True


def to_usd_amd(value: float | None, currency: str | None, rate: float) -> tuple[float | None, float | None]:
    if value is None:
        return None, None
    cur = (currency or "").upper()
    if cur == "USD" or (not cur and value < 20000):
        return round(value), round(value * rate)
    return round(value / rate), round(value)


ROMAN_Q = {"i": 1, "ii": 2, "iii": 3, "iv": 4}


def parse_completion(v) -> str | None:
    """Normalize '2027', '2027-06', 'IV 2028', 'III квартал 2022', 'Q3 2027' to an ISO end-of-period date."""
    if not isinstance(v, str) or not v.strip():
        return None
    t = v.strip().lower()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}.*", t):
        return t[:10]
    if re.fullmatch(r"\d{4}-\d{2}", t):
        return t + "-28"
    year = re.search(r"(20[1-4]\d)", t)
    if not year:
        return None
    q = re.search(r"\b(iv|iii|ii|i)\b", t) or re.search(r"q\s*([1-4])|([1-4])\s*(?:кв|quarter|եռամսյակ)", t)
    if q:
        n = ROMAN_Q.get(q.group(1)) if q.group(1) in ROMAN_Q else int(next(g for g in q.groups() if g))
        return f"{year.group(1)}-{n * 3:02d}-28"
    return f"{year.group(1)}-12-31"


START_RE = re.compile(
    r"(?:start(?:ed)?(?:\s+of)?(?:\s+the)?(?:\s+construction)?|construction\s+(?:began|started)|launch(?:ed)?|groundbreaking|начало\s+строительства|շինարարության\s+մեկնարկ)"
    r"[^0-9]{0,25}(?:(\d{1,2})[./](\d{4}|\d{2})\b|(20[12]\d))", re.I)
TYPICAL_BUILD_MONTHS = 36


def start_from_text(*texts: str | None) -> str | None:
    """Construction start date mentioned in free text, e.g. 'Start of the construction 06/21'."""
    for t in texts:
        m = START_RE.search(t or "")
        if not m:
            continue
        if m.group(3):
            return f"{m.group(3)}-01-01"
        month, year = int(m.group(1)), m.group(2)
        year = int(year) + 2000 if len(year) == 2 else int(year)
        if 1 <= month <= 12 and 2010 <= year <= 2035:
            return f"{year}-{month:02d}-01"
    return None


def months_between(a: date, b: date) -> float:
    return (b.year - a.year) * 12 + (b.month - a.month) + (b.day - a.day) / 30


def construction_stage(p: dict, today: date | None = None) -> None:
    """
    Classify build progress into finished / in progress / just started / not started / unknown.

    Uses start and completion dates when both are known (progress = elapsed / total). Without a start
    date it assumes a typical ~3-year build before completion and marks the stage as estimated.
    """
    today = today or date.today()
    status = p.get("status")
    start = p.get("start") or start_from_text(p.get("description"), p.get("description_site"), p.get("completion_text"))
    p["start"] = start
    try:
        end = date.fromisoformat(p["completion"][:10]) if p.get("completion") else None
        begin = date.fromisoformat(start[:10]) if start else None
    except ValueError:
        end = begin = None
    estimated = False
    if status == "planned" or (begin and begin > today):
        stage = "not started"
    elif status == "completed" or (end and end <= today):
        stage = "finished"
    elif end:
        if not begin:
            estimated = True
            months_left = months_between(today, end)
            stage = "not started" if months_left > TYPICAL_BUILD_MONTHS + 12 else "just started" if months_left > TYPICAL_BUILD_MONTHS * 0.75 else "in progress"
        else:
            total = max(months_between(begin, end), 1)
            progress = months_between(begin, today) / total
            stage = "just started" if progress < 0.25 else "in progress"
            p["progress_pct"] = round(min(max(progress, 0), 1) * 100)
    elif status == "under construction":
        stage, estimated = "in progress", True
    else:
        stage = "unknown"
    p["stage"], p["stage_estimated"] = stage, estimated


def status_of(completion: str | None) -> str:
    if not completion:
        return "unknown"
    try:
        return "completed" if date.fromisoformat(completion[:10]) <= date.today() else "under construction"
    except ValueError:
        return "unknown"


def from_karucapatoxic(p: dict, rate: float) -> dict:
    cur = p.get("currency") or None
    lo_usd, lo_amd = to_usd_amd(num(p.get("price_m2_min")), cur, rate)
    hi_usd, hi_amd = to_usd_amd(num(p.get("price_m2_max")), cur, rate)
    apt_usd, apt_amd = to_usd_amd(num(p.get("min_apartment_price")), cur, rate)
    if lo_usd and apt_usd and apt_usd < lo_usd:  # apartment price mis-entered per m²
        apt_usd = apt_amd = None
    return {
        **{k: p.get(k) for k in (
            "id", "source", "source_url", "title", "title_am", "title_ru", "developer", "developer_slug",
            "region", "district", "address", "sales_address", "lat", "lng", "completion", "floors",
            "phones", "email", "website", "social", "working_hours", "images", "videos", "description",
            "popularity", "price_updated", "developer_website", "developer_logo", "developer_about",
            "income_tax_refund",
        )},
        "phones": [s.strip() for s in p.get("phones") or [] if s and s.strip()],
        "kind": TYPE_LABELS.get(p.get("type"), "Apartments"),
        "currency_raw": cur,
        "usd_m2_min": lo_usd, "usd_m2_max": hi_usd or lo_usd,
        "amd_m2_min": lo_amd, "amd_m2_max": hi_amd or lo_amd,
        "usd_from": apt_usd, "amd_from": apt_amd,
        "min_area_m2": num(p.get("min_area_m2")),
        "start": p.get("start"),
        "sold_out": bool(p.get("sold_out")),
        "address_am": p.get("address_am"),
        "prices_by_floor": [
            {"floors": x.get("floors"), "rooms": x.get("rooms"),
             "usd_m2": to_usd_amd(num(x.get("price")), cur, rate)[0], "amd_m2": to_usd_amd(num(x.get("price")), cur, rate)[1]}
            for x in p.get("prices_by_floor") or [] if num(x.get("price"))
        ],
        "prices_by_rooms": [
            {"rooms": x.get("room"), "area_min": num(x.get("minArea")), "area_max": num(x.get("maxArea")),
             "usd_from": to_usd_amd(num(x.get("minPrice")), cur, rate)[0], "amd_from": to_usd_amd(num(x.get("minPrice")), cur, rate)[1],
             "usd_to": to_usd_amd(num(x.get("maxPrice")), cur, rate)[0], "amd_to": to_usd_amd(num(x.get("maxPrice")), cur, rate)[1]}
            for x in p.get("prices_by_rooms") or []
        ],
        "geo_precision": "exact",
        "price_obs": [o for o in (
            observation("karucapatoxic.am", **({"usd": num(p.get("price_m2_min"))} if lo_usd == num(p.get("price_m2_min")) else {"amd": num(p.get("price_m2_min"))}),
                        raw=f"{p.get('price_m2_min')} {cur or ''}/m²") if num(p.get("price_m2_min")) else None,
            implied_observation("karucapatoxic.am", p.get("min_apartment_price"), p.get("min_area_m2"), cur,
                                raw=f"apartment {p.get('min_apartment_price')} {cur or ''} / {p.get('min_area_m2')} m²"),
        ) if o],
        "sources": [{"name": "karucapatoxic.am", "url": p.get("source_url")}],
    }


def rooms_from_extra(rows, rate: float) -> list[dict]:
    out = []
    for r in rows if isinstance(rows, list) else []:
        if not isinstance(r, dict):
            continue
        usd, amd = to_usd_amd(num(r.get("price_from")), r.get("currency"), rate)
        area_min, area_max = num(r.get("area_min")), num(r.get("area_max"))
        if usd or area_min:
            out.append({"rooms": str(r.get("rooms") or "") or None, "area_min": area_min, "area_max": area_max,
                        "usd_from": usd, "amd_from": amd, "usd_to": None, "amd_to": None})
    return out


PLACE_TYPES = {"city", "town", "village", "hamlet", "suburb", "neighbourhood", "quarter", "administrative", "isolated_dwelling", "locality"}


def in_province(hit: dict, province: str) -> bool:
    """Geocode hit lies in (or Nominatim names) the expected province."""
    return locate(hit["lat"], hit["lng"])[0] == province or f"{province} Province" in (hit.get("display") or "")


def fix_inconsistent_locations(projects: list[dict]) -> None:
    """
    Re-geocode projects whose coordinates contradict the district/town named in their address,
    and distrust coordinates shared by several unrelated projects (source placeholders).
    """
    shared = defaultdict(set)
    for p in projects:
        shared[(round(p["lat"], 4), round(p["lng"], 4))].add(dev_key(p.get("developer")) or norm_title(p["title"]))
    for p in projects:
        placeholder = len(shared[(round(p["lat"], 4), round(p["lng"], 4))]) >= 3
        province, place = mentioned_place(p.get("address") or "")
        actual_province, actual_area = locate(p["lat"], p["lng"])
        if province is None and place and not (actual_area or "").startswith(place):
            center = geocode(None, place, None)  # town centre (towns without an OSM polygon)
            town_ok = bool(center) and haversine_m(p, center) < 4000
        else:
            town_ok = True
        mismatch = bool(place) and not (
            (province == "Yerevan" and actual_province == "Yerevan" and actual_area == place)
            or (province is None and town_ok)
        )
        says_yerevan = re.match(r"(?i)\s*yerevan", str(p.get("region") or "")) and actual_province not in (None, "Yerevan")
        if says_yerevan and not mismatch and not any(
            locate(p["lat"] + dy, p["lng"] + dx)[0] == "Yerevan" for dy in (-0.03, 0, 0.03) for dx in (-0.03, 0, 0.03)
        ):
            mismatch, place, province = True, None, "Yerevan"  # source says Yerevan but pin is >3 km outside
        if not (placeholder or mismatch):
            continue
        near_edge = mismatch and not placeholder and any(
            locate(p["lat"] + dy, p["lng"] + dx)[1] == place for dy in (-0.006, 0, 0.006) for dx in (-0.006, 0, 0.006)
        )
        if near_edge:
            continue  # within ~600 m of the named district: boundary ambiguity, keep source pin
        def matches(hit, pl=place, pr=province):
            if not pl:
                return True
            hp, ha = locate(hit["lat"], hit["lng"])
            return ha == pl if pr == "Yerevan" else (ha or "").startswith(pl) or pl.lower() in (hit.get("display") or "").lower()
        if not place and province == "Yerevan":
            matches = lambda hit: locate(hit["lat"], hit["lng"])[0] == "Yerevan"  # noqa: E731
        city = "Yerevan" if province == "Yerevan" else place
        hit = geocode(p.get("address"), city, None, accept=matches)
        reason = "shared placeholder coordinates" if placeholder else f"pin not in {place or province}"
        if hit and hit["precision"] in ("address", "street"):
            p["location_note"] = f"re-geocoded from address ({reason})"
            p["lat"], p["lng"], p["geo_precision"] = hit["lat"], hit["lng"], hit["precision"]
        else:
            p["location_note"] = f"location uncertain ({reason})"
            p["geo_precision"] = "district" if p.get("geo_precision") == "exact" else p.get("geo_precision")


def classify_kind(p: dict) -> str:
    """Separate offices/hotels and detached houses from apartment buildings so they don't skew $/m² benchmarks."""
    text = f"{p.get('title') or ''} {p.get('title_full') or ''}"
    if re.search(r"(?i)business\s*cent|technopark|office|hotel|guest\s*house|mall|plaza business", text):
        return "Commercial"
    if re.search(r"(?i)town\s*house|villa|cottage|private house|detached|\bhaus\b|houses\b", text):
        return "Houses / townhouses"
    return p.get("kind") or "Apartments"


def clean_company(name: str | None, description: str | None = None) -> str | None:
    n = re.sub(r"[«»\"“”„']", "", name or "")
    n = re.sub(r"\b(LLC|CJSC|OJSC|Ltd\.?|ООО|ՍՊԸ|ФБ?Ը)\b", "", n, flags=re.I).strip(" ,.-")
    if len(n) < 3 and description:
        m = re.search(r"Developer[:\s]+[«\"“]?([^»\"”\n.;]{3,60})", description)
        n = re.sub(r"\b(LLC|CJSC)\b", "", m.group(1)).strip() if m else n
    return n or None


def short_title(p: dict) -> str | None:
    """Catalogs often name buildings by full address; build a readable name instead."""
    title = (p.get("title") or "").strip()
    addr = (p.get("address") or "").strip()
    looks_address = bool(title) and (
        (addr and (title in addr or addr in title))
        or re.match(r"^(region|community|\w+ region|\w+ community)\b", title, re.I)
    )
    if title and not looks_address:
        return re.split(r"\s[-–|]\s|- Buy ", title)[0].strip()
    street = re.sub(r"^(.*?(region|community|village)\s+\S+\s*,?\s*)+", "", addr or title, flags=re.I)
    street = re.split(r",", street)[0].strip()
    dev = clean_company(p.get("developer"))
    return " · ".join(x for x in (dev, street) if x) or title or None


def from_extra(p: dict, idx: int, rate: float) -> dict:
    usd = num(p.get("price_min_usd_m2"))
    amd = num(p.get("price_min_amd_m2"))
    if amd and amd < 20000:  # a USD figure placed in the AMD field
        usd, amd = usd or amd, None
    if usd and usd > 20000:  # an AMD figure placed in the USD field
        usd, amd = None, amd or usd
    if usd and not amd:
        amd = usd * rate
    elif amd and not usd:
        usd = amd / rate
    completion = parse_completion(p.get("completion"))
    return {
        "id": f"{re.sub(r'[^a-z0-9]+', '', (p.get('source') or 'x').lower())}-{idx}",
        "source": p.get("source"), "source_url": p.get("source_url"),
        "title": short_title(p) or "Untitled project",
        "title_full": (p.get("title") or "").strip() or None,
        "developer": clean_company(p.get("developer"), p.get("description")),
        "region": p.get("city") or None, "district": p.get("district") or p.get("city") or None,
        "address": p.get("address") or None, "lat": p.get("lat"), "lng": p.get("lng"),
        "completion": completion, "floors": p.get("floors") or None,
        "phones": p.get("phones") or [], "email": p.get("email") or None,
        "website": p.get("website") or p.get("developer_url") or None, "social": p.get("social") or {},
        "images": p.get("images") or [], "videos": p.get("videos") or [],
        "description": p.get("description") or None,
        "kind": {"commercial": "Commercial", "mixed": "Mixed use"}.get(p.get("type"), "Apartments"),
        "usd_m2_min": round(usd) if usd else None, "usd_m2_max": round(usd) if usd else None,
        "amd_m2_min": round(amd) if amd else None, "amd_m2_max": round(amd) if amd else None,
        "usd_from": None, "amd_from": None, "min_area_m2": None,
        "prices_by_rooms": rooms_from_extra(p.get("apartments"), rate),
        "price_obs": [o for o in [
            observation(SOURCE_NAMES.get(p.get("source"), p.get("source")), usd=p.get("price_min_usd_m2"), amd=p.get("price_min_amd_m2"), raw=p.get("price_currency_raw") or None),
            *(implied_observation(SOURCE_NAMES.get(p.get("source"), p.get("source")), r.get("price_from"), r.get("area_min"), r.get("currency"),
                                  raw=f"{str(r.get('rooms')) + '-room ' if r.get('rooms') else ''}apartment from {r.get('price_from'):,} {r.get('currency') or ''} / {r.get('area_min')} m²" if isinstance(r.get('price_from'), (int, float)) else None)
              for r in (p.get("apartments") or []) if isinstance(r, dict)),
        ] if o],
        "status_hint": p.get("status"),
        "completion_text": p.get("completion") if isinstance(p.get("completion"), str) else None,
        "geo_precision": "exact" if p.get("lat") is not None else None,
        "developer_website": p.get("developer_url") or None,
        "sources": [{"name": SOURCE_NAMES.get(p.get("source"), p.get("source")), "url": p.get("source_url")}] + [
            {"name": urlparse(u).netloc.removeprefix("www."), "url": u}
            for u in p.get("alt_source_urls") or [] if isinstance(u, str) and u.startswith("http")
        ],
    }


ARMENIAN = re.compile(r"[\u0531-\u0587]")


def sentence_case_hy(t: str) -> str:
    """ALL-CAPS Armenian → 'Սենտենս case' (each word capitalized)."""
    return " ".join(w[:1].upper() + w[1:].lower() for w in t.split(" ")) if t == t.upper() else t


def latin_name(t: str) -> str:
    out = translit(t)
    return " ".join(w[:1].upper() + w[1:] for w in out.split(" "))


def latinize_names(p: dict) -> None:
    """Show Armenian-script names in Latin transliteration, keeping the original as *_am."""
    title = re.sub(r"(?i)^\s*բնակելի\s+համալիր\s*[«\"]?\s*|[»\"]\s*$", "", p.get("title") or "").strip() or (p.get("title") or "")
    if title != p.get("title") and not ARMENIAN.search(title):
        p["title_am"], p["title"] = p.get("title_am") or p.get("title"), title
    if len(ARMENIAN.findall(title)) > len(title) / 3:
        p["title_am"] = p.get("title_am") or sentence_case_hy(title)
        p["title"] = latin_name(title)
    elif ARMENIAN.search(title):
        p["title_am"] = p.get("title_am") or title
        t = re.sub(r"(?i)մասնաշենք(եր)?|մսն[․.]?", "bldg", title)
        t = re.sub(r"(?i)բնակելի\s+համալիր", "", t)
        t = re.sub(r"(?i)համալիր", "complex", t)
        t = re.sub(r"\s(և|ԵՎ)\s", " & ", t)
        t = re.sub(r"-?րդ\b", "", t)
        p["title"] = re.sub(r"\s+", " ", re.sub(r"[\u0531-\u0587]+", lambda m: translit(m.group(0)).upper() if len(m.group(0)) <= 2 else latin_name(m.group(0)), t)).strip(" ·")
    dev = p.get("developer") or ""
    if len(ARMENIAN.findall(dev)) > len(dev) / 3:
        p["developer_am"] = sentence_case_hy(dev)
        p["developer"] = latin_name(dev)


def haversine_m(a: dict, b: dict) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371000 * 2 * math.asin(math.sqrt(h))


HY = dict(zip("աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ",
              ["a","b","g","d","e","z","e","y","t","zh","i","l","kh","ts","k","h","dz","gh","ch","m","y","n","sh","o","ch","p","j","r","s","v","t","r","ts","v","p","k","o","f"]))
RU = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
              ["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","kh","ts","ch","sh","sch","","y","","e","yu","ya"]))
GENERIC_WORDS = r"residential|complex|district|residence|residences|building|buildings|house|new|the|llc|bnakeli|hamalir|zhiloy|kompleks|tower|towers|park"


def translit(t: str) -> str:
    return "".join(HY.get(ch, RU.get(ch, ch)) for ch in t.lower().replace("ու", "u").replace("և", "ev"))


def norm_title(t: str) -> str:
    t = translit(t or "")
    t = t.split(" · ")[-1] if " · " in t else t
    t = re.sub(r"\b(%s)\b" % GENERIC_WORDS, " ", t)
    t = t.replace("kh", "k").replace("gh", "g").replace("q", "k").replace("ts", "c").replace("y", "i")
    return re.sub(r"[^a-z0-9]+", "", t)


def house_numbers(p: dict) -> set[str]:
    text = " ".join(x for x in (p.get("title"), p.get("address"), p.get("title_full")) if x)
    return set(re.findall(r"\b\d{1,3}(?:/\d{1,3})+\b|\b\d{1,3}[a-zա-ֆ]?\b(?=\s*(?:$|,|\)))", text.lower()))


def is_duplicate(a: dict, b: dict) -> bool:
    if a["lat"] is None or b["lat"] is None:
        return False
    d = haversine_m(a, b)
    if d > 5000:
        return False
    ta, tb = norm_title(a["title"]), norm_title(b["title"])
    sim = SequenceMatcher(None, ta, tb).ratio() if ta and tb else 0
    contains = len(ta) >= 5 and len(tb) >= 5 and (ta in tb or tb in ta)
    approx = a.get("geo_precision") != "exact" or b.get("geo_precision") != "exact"
    na, nb = ({n for n in house_numbers(x) if "/" in n} for x in (a, b))
    shared_no = bool(na & nb)
    if na and nb and not shared_no and sim < 0.9:
        return False  # different building numbers on the same street
    if a.get("source") and a.get("source") == b.get("source"):
        return False  # sources already dedupe themselves
    return (
        (d < 60 and (sim > 0.5 or contains or not ta or not tb))
        or (d < 400 and (sim > 0.7 or contains or shared_no))
        or (approx and (sim > 0.85 or (contains and shared_no)))
    )


def merge_into(base: dict, other: dict) -> None:
    base["sources"].extend(other["sources"])
    base["price_obs"] = (base.get("price_obs") or []) + (other.get("price_obs") or [])
    other_desc = other.get("description")
    if other_desc and (not base.get("description") or GENERIC_DESC.match(base["description"])) and not base.get("description_site"):
        base["description_site"] = other_desc
    for k, v in other.items():
        if k in ("id", "sources"):
            continue
        if base.get(k) in (None, "", [], {}) and v not in (None, "", [], {}):
            base[k] = v
    base["images"] = list(dict.fromkeys((base.get("images") or []) + (other.get("images") or [])))
    base["videos"] = list(dict.fromkeys((base.get("videos") or []) + (other.get("videos") or [])))


def load_price_verifications() -> dict:
    """Manual re-checks of flagged prices (scraper/price_verified_*.json), keyed by project id and title."""
    out = {}
    for f in sorted((ROOT / "scraper").glob("price_verified_*.json")):
        for v in json.loads(f.read_text(encoding="utf-8")):
            if isinstance(v, dict) and v.get("id"):
                out[v["id"]] = v
    return out


def drop_wrong_merges(p: dict, v: dict) -> None:
    wrong = {u for u in v.get("wrong_merge_urls") or [] if isinstance(u, str)}
    if not wrong:
        return
    hosts = {urlparse(u).netloc.removeprefix("www.") for u in wrong}
    p["sources"] = [s for s in p["sources"] if s.get("url") not in wrong]
    keep_hosts = {urlparse(s.get("url") or "").netloc.removeprefix("www.") for s in p["sources"]}
    p["price_obs"] = [o for o in p.get("price_obs") or [] if o["source"] not in hosts - keep_hosts]


def apply_price_verification(p: dict, v: dict, rate: float) -> None:
    verdict = v.get("verdict")
    p["price_verification"] = {k: v.get(k) for k in ("verdict", "evidence_url", "evidence_text", "notes") if v.get(k)}
    if v.get("sold_out") is True:
        p["sold_out"] = True
    if verdict == "corrected":
        usd, amd = num(v.get("usd_m2")), num(v.get("amd_m2"))
        if usd or amd:
            usd = usd or amd / rate
            amd = amd or usd * rate
            p["usd_m2_min"], p["amd_m2_min"] = round(usd), round(amd)
            if not p.get("usd_m2_max") or p["usd_m2_max"] < p["usd_m2_min"]:
                p["usd_m2_max"], p["amd_m2_max"] = p["usd_m2_min"], p["amd_m2_min"]
            p["price_confidence"] = "verified"
        total, area = num(v.get("apartment_from_total")), num(v.get("apartment_from_area_m2"))
        if total:
            shown_usd = (v.get("currency_shown") or "").upper() == "USD"
            p["usd_from"], p["amd_from"] = (round(total), round(total * rate)) if shown_usd else (round(total / rate), round(total))
            p["min_area_m2"] = area or p.get("min_area_m2")
    elif verdict == "confirmed":
        p["price_confidence"] = "verified"
    elif verdict == "unverifiable" and p.get("price_confidence") in ("low", "rejected"):
        p["usd_m2_min"] = p["amd_m2_min"] = p["usd_m2_max"] = p["amd_m2_max"] = None
        p["price_confidence"] = "none"


def sanity_check_numbers(p: dict) -> None:
    """Drop starting apartment prices / areas that contradict the reconciled price per m²."""
    notes = p.setdefault("price_flags", [])
    if not p.get("usd_from") and p.get("prices_by_rooms"):
        cheapest = min((r for r in p["prices_by_rooms"] if r.get("usd_from")), key=lambda r: r["usd_from"], default=None)
        if cheapest:
            p["usd_from"], p["amd_from"] = cheapest["usd_from"], cheapest["amd_from"]
            p["min_area_m2"] = p.get("min_area_m2") or cheapest.get("area_min")
    if p.get("usd_from") and p.get("usd_m2_min"):
        implied_area = p["usd_from"] / p["usd_m2_min"]
        if not 15 <= implied_area <= 600:
            notes.append(f"starting price ${p['usd_from']:,} implies {implied_area:.0f} m² — dropped")
            p["usd_from"] = p["amd_from"] = None
    if p.get("min_area_m2") and not 12 <= p["min_area_m2"] <= 1000:
        notes.append(f"min area {p['min_area_m2']} m² implausible — dropped")
        p["min_area_m2"] = None
    floors = [int(x) for x in re.findall(r"\d+", str(p.get("floors") or ""))]
    if floors and max(floors) > 80:
        notes.append(f"floors '{p['floors']}' implausible — dropped")
        p["floors"] = None


def add_benchmarks(projects: list[dict]) -> None:
    """Discount vs. median $/m² of OTHER apartment projects in the same district (region fallback)."""
    by_district, by_region = defaultdict(list), defaultdict(list)
    for p in projects:
        if p["usd_m2_min"] and p["kind"] == "Apartments" and p.get("price_confidence") not in ("low", "rejected"):
            by_district[p.get("district")].append((p["id"], p["usd_m2_min"]))
            by_region[p.get("region")].append((p["id"], p["usd_m2_min"]))
    for p in projects:
        others = lambda rows: [v for pid, v in rows if pid != p["id"]]
        pool, scope = others(by_district.get(p.get("district"), [])), "district"
        if len(pool) < 3:
            pool, scope = others(by_region.get(p.get("region"), [])), "region"
        if p["usd_m2_min"] and p["kind"] == "Apartments" and len(pool) >= 3:
            med = statistics.median(pool)
            p["bench_usd_m2"] = round(med)
            p["bench_scope"] = scope
            p["bench_n"] = len(pool)
            p["discount_pct"] = round((med - p["usd_m2_min"]) / med * 100, 1)
        else:
            p["bench_usd_m2"] = p["bench_scope"] = p["bench_n"] = p["discount_pct"] = None


GENERIC_DESC = re.compile(r"^New apartments in [^.]+\.( Prices from [^.]+\.)?( completion [^.]+\.)?$", re.I)


def dev_key(name: str | None) -> str:
    n = (name or "").lower()
    n = re.sub(r"\b(llc|ltd|cjsc|ojsc|group|construction|development|developments|company|shin|սպը|փբը|ооо)\b", " ", n)
    return re.sub(r"[^a-z0-9ա-ֆа-я]+", "", n)


def load_developers() -> dict:
    if not DEVELOPERS.exists():
        return {}
    index = {}
    for d in json.loads(DEVELOPERS.read_text(encoding="utf-8")):
        for key in {dev_key(d.get("name")), registrable_domain(d.get("website")) or ""}:
            if key and len(key) >= 3:
                index.setdefault(key, d)
    return index


def fill_from_developer(p: dict, devs: dict) -> None:
    """Use the developer directory to add contacts/website when a project has none."""
    d = devs.get(dev_key(p.get("developer"))) or devs.get(registrable_domain(p.get("website")) or "") \
        or devs.get(registrable_domain(p.get("developer_website")) or "")
    if not d:
        return
    if not p.get("developer_website") and d.get("website"):
        p["developer_website"] = d["website"]
    if not p.get("phones") and d.get("phones"):
        p["phones"], p["contacts_via_developer"] = d["phones"][:4], True
    if not p.get("email") and d.get("email"):
        p["email"], p["contacts_via_developer"] = d["email"], True
    for k in ("facebook", "instagram"):
        if d.get(k):
            p.setdefault("social", {}).setdefault(k, d[k])


def enrich(p: dict, sites: dict) -> None:
    """Fill description/videos/contacts/social from the project's (or developer's) official website."""
    for url in (p.get("website"), p.get("developer_website")):
        info = sites.get((url or "").split("#")[0]) if url else None
        if not info:
            continue
        own = url == p.get("website")
        text = next((t for t in (info.get("text"), info.get("description")) if t and len(t) >= 150), None)
        if own and text and (not p.get("description") or GENERIC_DESC.match(p["description"] or "")):
            p["description_site"] = text
        elif not own and text and not p.get("developer_about"):
            p["developer_about"] = text
        if own:
            p["videos"] = list(dict.fromkeys((p.get("videos") or []) + info.get("videos", [])))
            if info.get("image") and not p.get("images"):
                p["images"] = [info["image"]]
        for k, v in (info.get("social") or {}).items():
            p.setdefault("social", {}).setdefault(k, v)
        if not p.get("phones") and info.get("phones"):
            p["phones"] = info["phones"]
        if not p.get("email") and info.get("emails"):
            p["email"] = info["emails"][0]


COMPLETENESS = [
    ("price", lambda p: p.get("usd_m2_min") or p.get("usd_from")),
    ("developer", lambda p: not p.get("developer_inferred") or not str(p.get("developer_group", "")).endswith("(developer n/a)")),
    ("contacts", lambda p: p.get("phones") or p.get("email")),
    ("website/social", lambda p: p.get("website") or p.get("social")),
    ("completion date", lambda p: p.get("completion")),
    ("images", lambda p: p.get("images")),
    ("description", lambda p: p.get("description_site") or (p.get("description") and not GENERIC_DESC.match(p["description"]))),
    ("address", lambda p: p.get("address")),
    ("floors", lambda p: p.get("floors")),
    ("precise location", lambda p: p.get("geo_precision") in ("exact", "address")),
]


def score_completeness(p: dict) -> None:
    missing = [name for name, test in COMPLETENESS if not test(p)]
    p["info_missing"] = missing
    p["info_score"] = round(100 * (len(COMPLETENESS) - len(missing)) / len(COMPLETENESS))


def main() -> int:
    rate, rate_time = amd_per_usd()
    projects = [from_karucapatoxic(p, rate) for p in json.loads(KP.read_text(encoding="utf-8"))]
    extras = [e for f in EXTRA_FILES if f.exists() for e in json.loads(f.read_text(encoding="utf-8"))]
    added = merged = skipped = geocoded = 0
    for i, e in enumerate(extras):
        cand = from_extra(e, i, rate)
        override = GEO_OVERRIDES.get(e.get("source_url") or "")
        if override:
            cand["lat"], cand["lng"], cand["geo_precision"] = override["lat"], override["lng"], override["precision"]
        if cand["lat"] is None or cand["lng"] is None:
            hint = province_hint(" ".join(str(e.get(k) or "") for k in ("address", "city", "district", "description")))
            hit = geocode(cand.get("address"), e.get("city"), e.get("district"),
                          accept=(lambda hit, h=hint: in_province(hit, h)) if hint else None)
            if hit and hit["precision"] in ("district", "city"):
                place = hit["query"].split(",")[0]
                if SequenceMatcher(None, norm_title(place), norm_title((geocode_display(hit) or "").split(",")[0])).ratio() < 0.6:
                    hit = None  # matched a differently named place
            if not hit and hint:
                for part in re.split(r"[,\-–]| համայնք| community", cand.get("address") or ""):
                    part = part.strip()
                    if len(part) >= 3 and not province_hint(part):
                        hit = geocode(None, None, f"{part}, {hint}", accept=lambda hit, h=hint: in_province(hit, h) and hit.get("type") in PLACE_TYPES)
                        if hit and SequenceMatcher(None, norm_title(part), norm_title((geocode_display(hit) or "").split(",")[0])).ratio() < 0.6:
                            hit = None  # Nominatim matched some other place in the province
                        if hit:
                            break
            if not hit or hit["precision"] == "city" and not cand.get("address"):
                skipped += 1
                continue
            cand["lat"], cand["lng"], cand["geo_precision"] = hit["lat"], hit["lng"], hit["precision"]
            geocoded += 1
        if not (38.8 <= cand["lat"] <= 41.35 and 43.4 <= cand["lng"] <= 46.7):
            skipped += 1
            continue
        dup = next((p for p in projects if is_duplicate(p, cand)), None)
        if dup:
            merge_into(dup, cand)
            merged += 1
        else:
            projects.append(cand)
            added += 1
    fix_inconsistent_locations(projects)
    for p in projects:
        fallback = next((normalize_town(t) for t in (p.get("district"), p.get("region")) if normalize_town(t)), None)
        province, area = locate(p["lat"], p["lng"], fallback)
        if province:
            p["source_region"], p["source_district"] = p.get("region"), p.get("district")
            p["region"], p["district"] = province, area or province
            if p["district"] and ARMENIAN.search(p["district"]):
                p["district"] = latin_name(p["district"])
    for p in projects:
        p["title"] = p.get("title") or p.get("title_ru") or p.get("title_am") or p.get("address") or "Untitled project"
        latinize_names(p)
        p["kind"] = classify_kind(p)
        p["developer_group"], p["developer_inferred"] = infer_developer(p)
    group_sizes = defaultdict(int)
    for p in projects:
        group_sizes[p["developer_group"]] += 1
    for p in projects:
        if p["developer_inferred"] and group_sizes[p["developer_group"]] == 1:
            p["developer_group"] = f"{p['title']} (developer n/a)"
    for p in projects:
        hint = p.pop("status_hint", None)
        p["status"] = status_of(p.get("completion")) if p.get("completion") else (hint or "unknown")
        p["completion_year"] = int(p["completion"][:4]) if p.get("completion") else None
        construction_stage(p)
        if re.search(r"company-name|example\.|yourmail|email@", p.get("email") or "", re.I):
            p["email"] = None
        p["social"] = {k: v.strip() for k, v in (p.get("social") or {}).items() if isinstance(v, str) and v.strip()}
    sites = json.loads(ENRICH.read_text(encoding="utf-8")) if ENRICH.exists() else {}
    devs = load_developers()
    for p in projects:
        fill_from_developer(p, devs)
        enrich(p, sites)
        score_completeness(p)
    verified = load_price_verifications()
    for p in projects:
        v = verified.get(p["id"])
        if v:
            drop_wrong_merges(p, v)
        reconcile(p, rate)
        if v:
            apply_price_verification(p, v, rate)
        sanity_check_numbers(p)
    add_benchmarks(projects)
    meta = {
        "generated": date.today().isoformat(), "amd_per_usd": round(rate, 2), "rate_time": rate_time,
        "count": len(projects), "extra_added": added, "extra_merged": merged, "extra_skipped": skipped, "geocoded": geocoded,
        "sources": sorted({s["name"] for p in projects for s in p["sources"] if s.get("name")}),
    }
    OUT.write_text(json.dumps({"meta": meta, "projects": projects}, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, indent=1), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
