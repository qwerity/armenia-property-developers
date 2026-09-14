"""Scrape Armenian new-building projects from multi-developer catalogs.

Sources:
  * myhome.am (Ameriabank)      — JSON API (buildings/filter_v2, buildings/{id}, apartments/filter, projects)
  * redgroup.am (RED Invest)    — JSON API (/api/projects?page=N, /api/projects/{id}); redinvest.am mirrors it
  * novostroiki-yerevan.com     — sitemap + per-project Markdown (.md) + JSON-LD on the HTML page
  * ar-go.am (ARGO Realty)      — /projects listing + server-rendered project pages
  * acba.am                     — "apartments from developers" page (Angular ng-state JSON)
  * evoca.am                    — partner construction companies accordion page
  * byblosbankarmenia.am        — partner developers cards

Output: ./developer_projects_catalogs.json (list of records in the schema of .agent_schema.md),
rewritten after every source so partial results survive.
Cache directory: $CATALOG_CACHE or ./.cache_catalogs
"""
import hashlib
import html as htmllib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
HERE = Path(__file__).resolve().parent
OUT = HERE / "developer_projects_catalogs.json"
CACHE = Path(os.environ.get("CATALOG_CACHE", HERE / ".cache_catalogs"))
DELAY = 0.6
MAX_IMAGES = 12
TODAY = time.strftime("%Y-%m")

YEREVAN_DISTRICTS = [
    ("Nor Nork", r"nor[\s-]*nor[kq]|նոր\s*նորք|нор[\s-]*норк"),
    ("Nork-Marash", r"nor[kq][\s-]*marash|նորք[\s-]*մարաշ|норк[\s-]*мараш"),
    ("Malatia-Sebastia", r"malatia|sebastia|մալաթիա|սեբաստիա|малатия|себастия"),
    ("Kanaker-Zeytun", r"[kq]ana[kq]er(?!avan)|zeytun|zeitun|քանաքեռ(?!ավան)|զեյթուն|канакер(?!аван)|зейтун"),
    ("Ajapnyak", r"ajapnyak|աջափնյակ|аджапняк|silikyan|սիլիկյան"),
    ("Arabkir", r"arabkir|արաբկիր|арабкир"),
    ("Avan", r"\bavan\b|ավան|\bаван\b"),
    ("Davtashen", r"davtashen|davitashen|դավթաշեն|давташен"),
    ("Erebuni", r"erebuni|էրեբունի|эребуни"),
    ("Kentron", r"kentron|center of yerevan|կենտրոն|кентрон|noragyugh|նորագյուղ"),
    ("Nubarashen", r"nubarashen|նուբարաշեն|нубарашен"),
    ("Shengavit", r"shengavit|շենգավիթ|шенгавит"),
]
TOWNS = [
    ("Kanakeravan", r"kanakeravan|քանաքեռավան|канакераван"), ("Dzoraghbyur", r"dzora[gk]h?byur|ձորաղբյուր|дзорагбюр"),
    ("Arinj", r"\barinj\b|առինջ|ариндж"), ("Zovuni", r"zovuni|զովունի|зовуни"), ("Mrgashen", r"mrgashen|մրգաշեն"),
    ("Argavand", r"argavand|արգավանդ"), ("Merdzavan", r"merdzavan|մերձավան"), ("Ptghni", r"ptghni|պտղնի"),
    ("Proshyan", r"proshyan|պռոշյան"), ("Talin", r"\btalin\b|թալին"), ("Aparan", r"aparan|ապարան"),
    ("Nairi", r"\bnairi (?:village|community)|նաիրի համայնք"),
    ("Tsaghkadzor", r"tsa[gk]h?kadzor|ծաղկաձոր|цахкадзор"), ("Dilijan", r"dilijan|դիլիջան|дилижан"),
    ("Abovyan", r"abovyan(?! st| city house|ի \d)|աբովյան քաղաք|ք[․.]\s*աբովյան|абовян"), ("Nor Hachn", r"nor\s*hachn|նոր\s*հաճն|нор\s*ачн"),
    ("Yeghvard", r"yeghvard|եղվարդ|егвард"), ("Ashtarak", r"ashtarak(?! str)|աշտարակ(?!ի)|аштарак"),
    ("Gyumri", r"gyumri|գյումրի|гюмри"), ("Vanadzor", r"vanadzor|վանաձոր|ванадзор"),
    ("Jermuk", r"jermuk|ջերմուկ|джермук"), ("Sevan", r"\bsevan\b|սևան|севан"),
    ("Vagharshapat", r"vagharshapat|echmiadzin|վաղարշապատ|էջմիածին|эчмиадзин"), ("Masis", r"\bmasis\b|մասիս"),
    ("Vedi", r"\bvedi\b|վեդի"), ("Artashat", r"artashat|արտաշատ"), ("Goris", r"\bgoris\b|գորիս"),
    ("Kapan", r"\bkapan\b|կապան"), ("Hrazdan", r"hrazdan(?! gorge)|հրազդան քաղաք"), ("Charentsavan", r"charentsavan|չարենցավան"),
    ("Jrvezh", r"jrve[jz]h?|ջրվեժ|джрвеж"),
]
YEREVAN_RE = r"yerevan(?!yan| highway| hwy)|երևան(?!յան)|երեւան(?!յան)|ереван(?!ское)"
YEREVAN_BBOX = (40.06, 40.25, 44.36, 44.62)  # lat_min, lat_max, lng_min, lng_max


# ----------------------------------------------------------------------------- fetching
def _cache_file(key: str, ext: str) -> Path:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", key).strip("_")[:120]
    return CACHE / f"{slug}_{hashlib.md5(key.encode()).hexdigest()[:8]}.{ext}"


def fetch(url: str, *, data: dict | None = None, headers: dict | None = None, retries: int = 4,
          want_headers: bool = False):
    """GET (or POST JSON when ``data`` is given) ``url`` with disk cache, delay and retry.

    Returns the body text ("" on failure). With ``want_headers`` returns ``(text, headers_dict)``.
    """
    CACHE.mkdir(parents=True, exist_ok=True)
    key = url + (json.dumps(data, sort_keys=True) if data is not None else "") + json.dumps(headers or {}, sort_keys=True)
    cf = _cache_file(key, "cache")
    if cf.exists() and cf.stat().st_size > 2:
        blob = json.loads(cf.read_text(encoding="utf-8"))
        return (blob["body"], blob["headers"]) if want_headers else blob["body"]
    hdrs = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/json",
            "Accept-Language": "en-US,en;q=0.9,hy;q=0.8,ru;q=0.7"}
    hdrs.update(headers or {})
    body = json.dumps(data).encode() if data is not None else None
    if body is not None:
        hdrs["Content-Type"] = "application/json"
    for attempt in range(retries):
        try:
            time.sleep(DELAY)
            req = urllib.request.Request(url, data=body, headers=hdrs, method="POST" if body else "GET")
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8", errors="replace")
                rh = {k.lower(): v for k, v in r.headers.items()}
            cf.write_text(json.dumps({"body": text, "headers": rh}), encoding="utf-8")
            return (text, rh) if want_headers else text
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 410) or attempt == retries - 1:
                print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
                break
            time.sleep((15 if e.code == 429 else 2) * 2 ** attempt)
        except Exception as e:  # network errors, timeouts
            if attempt == retries - 1:
                print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
                break
            time.sleep(2 ** attempt)
    return ("", {}) if want_headers else ""


def fetch_json(url: str, **kw):
    """Fetch and decode JSON; returns None when the body is missing or not JSON."""
    text = fetch(url, **kw)
    try:
        return json.loads(text) if text else None
    except json.JSONDecodeError:
        print(f"  ! bad JSON from {url}", file=sys.stderr)
        return None


# ----------------------------------------------------------------------------- normalisation helpers
def blank(source: str, url: str) -> dict:
    """Return an empty record in the output schema."""
    return {
        "source": source, "source_url": url, "title": "", "developer": "", "developer_url": "",
        "city": "", "district": "", "address": "", "lat": None, "lng": None,
        "price_min_usd_m2": None, "price_min_amd_m2": None, "price_currency_raw": "",
        "completion": None, "status": None, "floors": "", "type": None, "phones": [],
        "email": "", "website": "", "social": {"facebook": "", "instagram": "", "youtube": "", "telegram": ""},
        "images": [], "videos": [], "description": "", "apartments": [],
    }


def strip_tags(s: str) -> str:
    """HTML fragment -> collapsed plain text (block tags become newlines)."""
    s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s or "", flags=re.S)
    s = re.sub(r"<br\s*/?>|</(p|li|div|h\d|tr)>", "\n", s)
    s = htmllib.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()


def short(text: str, n: int = 700) -> str:
    """Single-line text truncated at a word boundary to at most ``n`` chars."""
    t = re.sub(r"\s+", " ", text or "").strip()
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


def to_num(s) -> float | None:
    """Parse '1 185', '400,000', '560.000', '1500.5' to a number; None if not parseable."""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    t = re.sub(r"[\s  ]", "", str(s)).replace("․", ".")
    m = re.search(r"\d[\d.,]*", t)
    if not m:
        return None
    t = m.group(0).rstrip(".,")
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", t):
        t = re.sub(r"[.,]", "", t)
    else:
        t = t.replace(",", "")
    try:
        return float(t)
    except ValueError:
        return None


def clean_coord(lat, lng) -> tuple[float | None, float | None]:
    """Validate a coordinate pair against Armenia's bounding box (swapping if reversed)."""
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return None, None
    if 43.4 <= lat <= 46.7 and 38.8 <= lng <= 41.35:
        lat, lng = lng, lat
    if 38.8 <= lat <= 41.35 and 43.4 <= lng <= 46.7:
        return round(lat, 7), round(lng, 7)
    return None, None


MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}
QUARTERS = {"first": "I", "1st": "I", "i": "I", "second": "II", "2nd": "II", "ii": "II",
            "third": "III", "3rd": "III", "iii": "III", "fourth": "IV", "4th": "IV", "iv": "IV"}


def norm_completion(text: str | None) -> str | None:
    """Normalise a free-text date to 'YYYY-MM', 'IV 2027' or 'YYYY'.

    Examples: '2027-10-01' -> '2027-10'; '05/12/2026թ.' -> '2026-12'; 'first quarter of 2029' -> 'I 2029'.
    """
    if not text:
        return None
    t = str(text).replace("․", ".").lower()
    nd, ndr = r"(?<!\d)", r"(?!\d)"
    if m := re.search(rf"{nd}(20\d\d)-(\d{{1,2}}){ndr}", t):
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    if m := re.search(rf"{nd}\d{{1,2}}[./](\d{{1,2}})[./](20\d\d|\d\d){ndr}", t):
        y = m.group(2) if len(m.group(2)) == 4 else "20" + m.group(2)
        if 1 <= int(m.group(1)) <= 12:
            return f"{y}-{int(m.group(1)):02d}"
    if m := re.search(rf"{nd}(\d{{1,2}})\s*[/.]\s*(20\d\d){ndr}", t):
        if 1 <= int(m.group(1)) <= 12:
            return f"{m.group(2)}-{int(m.group(1)):02d}"
    if m := re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*(?:of\s*)?(20\d\d)", t):
        return f"{m.group(2)}-{MONTHS[m.group(1)]:02d}"
    if m := re.search(r"(20\d\d)\.?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*", t):
        return f"{m.group(1)}-{MONTHS[m.group(2)]:02d}"
    if m := re.search(r"\b(first|second|third|fourth|1st|2nd|3rd|4th|iv|iii|ii|i)\s+quarter\s*(?:of\s*)?(20\d\d)", t):
        return f"{QUARTERS[m.group(1)]} {m.group(2)}"
    if m := re.search(rf"{nd}(\d{{1,2}})/(\d\d){ndr}", t):
        if 1 <= int(m.group(1)) <= 12:
            return f"20{m.group(2)}-{int(m.group(1)):02d}"
    if m := re.search(rf"{nd}(20\d\d){ndr}", t):
        return m.group(1)
    return None


def completion_is_past(c: str | None) -> bool:
    """True when a normalised completion value lies strictly before the current month."""
    if not c:
        return False
    m = re.search(r"(20\d\d)(?:-(\d\d))?", c)
    if not m:
        return False
    ym = f"{m.group(1)}-{m.group(2) or '12'}"
    return ym < TODAY


def guess_city_district(*texts: str) -> tuple[str, str]:
    """Infer (city, Yerevan district) from address-like text in English/Armenian/Russian."""
    t = " ".join(x for x in texts if x).lower()
    district = next((name for name, rx in YEREVAN_DISTRICTS if re.search(rx, t)), "")
    if re.search(YEREVAN_RE, t):
        return "Yerevan", district
    town = next((name for name, rx in TOWNS if re.search(rx, t)), "")
    if town:
        return town, ""
    return ("Yerevan", district) if district else ("", "")


def fill_city(rec: dict) -> None:
    """Default an empty city to Yerevan when the coordinates fall inside the Yerevan bounding box."""
    if not rec["city"] and rec["lat"] is not None:
        a, b, c, d = YEREVAN_BBOX
        if a <= rec["lat"] <= b and c <= rec["lng"] <= d:
            rec["city"] = "Yerevan"


def price_per_m2(text: str) -> float | None:
    """Smallest plausible per-m² amount in a raw price text ('1,2 մասնաշենք 700,000.00 - 880,000' -> 700000)."""
    t = (text or "").replace("․", ".")
    nums = [to_num(x) for x in re.findall(r"(?<![\d,.])\d{1,3}(?:[., ]\d{3})+(?:\.\d{1,2})?|(?<![\d,.])\d{3,}(?:\.\d{1,2})?", t)]
    nums = [n for n in nums if n and n >= 100]
    return min(nums) if nums else None


def sane_price(amd: float | None, usd: float | None) -> tuple[float | None, float | None]:
    """Drop implausible per-m² prices; move AMD values that are clearly USD-sized into USD."""
    if amd is not None and 150 <= amd <= 20000 and usd is None:
        amd, usd = None, amd
    if amd is not None and not 50000 <= amd <= 10000000:
        amd = None
    if usd is not None and not 150 <= usd <= 20000:
        usd = None
    return amd, usd


def split_social(urls: list[str], rec: dict) -> None:
    """Distribute URLs into ``rec['social']`` / ``rec['videos']`` / ``rec['website']``."""
    for u in urls:
        lu = u.lower()
        for net in ("facebook", "instagram", "telegram"):
            if net in lu or (net == "telegram" and "t.me/" in lu):
                rec["social"][net] = rec["social"][net] or u
                break
        else:
            if "youtube" in lu or "youtu.be" in lu:
                rec["social"]["youtube"] = rec["social"]["youtube"] or u
            elif not rec["website"]:
                rec["website"] = u


def phones_from(text: str) -> list[str]:
    """Extract Armenian phone numbers from text, normalised to '+374 XX XXXXXX'."""
    out = []
    for m in re.finditer(r"(?:\+?\s*374|\b0)[\s\-()]*(\d{2})[\s\-()]*(\d{2,3})[\s\-]*(\d{2,3})[\s\-]*(\d{0,3})", text or ""):
        digits = "".join(m.groups())
        if len(digits) == 8:
            p = f"+374 {digits[:2]} {digits[2:]}"
            if p not in out:
                out.append(p)
    return out


def apartments_summary(units: list[tuple]) -> list[dict]:
    """Group (rooms, area, price, currency) tuples by room count into schema ``apartments`` rows."""
    groups = defaultdict(list)
    for rooms, area, price, cur in units:
        if area:
            groups[(str(rooms) if rooms not in (None, "") else "", cur)].append((area, price))
    rows = []
    for (rooms, cur), vals in sorted(groups.items()):
        prices = [p for _, p in vals if p]
        rows.append({"rooms": rooms, "area_min": min(a for a, _ in vals), "area_max": max(a for a, _ in vals),
                     "price_from": min(prices) if prices else None, "currency": cur})
    return rows


# ----------------------------------------------------------------------------- myhome.am
MYHOME_API = "https://myhome.am/API/v1"


def _en(d) -> str:
    """Pick the English (fallback Russian/Armenian) value of a myhome i18n dict."""
    if not isinstance(d, dict):
        return d or ""
    return (d.get("eng") or d.get("rus") or d.get("arm") or "").strip()


def myhome_apartments(building_id: int) -> list[dict]:
    """Fetch every available apartment of a myhome building and summarise by rooms."""
    units, page = [], 1
    while page <= 20:
        text, hdr = fetch(f"{MYHOME_API}/apartments/filter",
                          data={"buildingId": building_id, "pageNumber": page, "pageSize": 100}, want_headers=True)
        try:
            items = json.loads(text).get("apartments") or []
        except (json.JSONDecodeError, AttributeError):
            break
        for a in items:
            rooms = "studio" if a.get("isStudio") else ("free layout" if a.get("isFreePlaning") or not a.get("roomsCount") else a.get("roomsCount"))
            units.append((rooms, a.get("area"), a.get("minApartmentPrice"), "AMD"))
        try:
            has_next = json.loads(hdr.get("x-pagination", "{}")).get("HasNext")
        except json.JSONDecodeError:
            has_next = False
        if not has_next:
            break
        page += 1
    return apartments_summary(units)


def myhome_address(addr: dict) -> tuple[str, str, str]:
    """Return (address, city, district) strings from a myhome address object."""
    street = _en(addr.get("street"))
    num = addr.get("buildingNumber") or ""
    city = _en(addr.get("city")) or (_en((addr.get("city") or {}).get("name")) if isinstance(addr.get("city"), dict) else "")
    district = _en(addr.get("district"))
    region = _en(addr.get("region"))
    parts = [p for p in [f"{street} {num}".strip(), district, city, region] if p]
    return ", ".join(parts), city, district


def myhome_building(b: dict, listing: dict) -> dict:
    """Convert a myhome building detail JSON (plus its filter_v2 ``listing`` item) into a schema record."""
    rec = blank("myhome.am", f"https://myhome.am/en/building/{b['id']}")
    addr = b.get("address") or {}
    rec["address"], rec["city"], rec["district"] = myhome_address(addr)
    builder = b.get("builder") or {}
    name = _en(b.get("name")) or _en(listing.get("name"))
    rec["title"] = name or rec["address"]
    rec["developer"] = _en(builder.get("builderBrandName"))
    rec["developer_url"] = builder.get("builderWebSite") or ""
    rec["lat"], rec["lng"] = clean_coord(b.get("latitude") or addr.get("lat"), b.get("longitude") or addr.get("lng"))
    price = b.get("areaPriceStartingAt")
    rec["price_min_amd_m2"] = price or None
    if price:
        rec["price_currency_raw"] = f"from {price:,.0f} AMD/m²; apartment from {b.get('apartmentPriceStartingAt') or 0:,.0f} AMD"
    rec["completion"] = norm_completion(b.get("exploitationDate") or b.get("completionDate"))
    rec["status"] = "completed" if b.get("isBuilt") else "under construction"
    rec["floors"] = str(b.get("floorsCount") or "")
    rec["type"] = "residential"
    rec["phones"] = phones_from(" ".join(filter(None, [builder.get("builderMobilePhoneNumber"), builder.get("builderPhoneNumber")])))
    rec["email"] = builder.get("builderEmail") or ""
    rec["website"] = builder.get("builderWebSite") or ""
    rec["images"] = list(dict.fromkeys([u for u in [b.get("mainImage"), *(b.get("images") or [])] if u]))[:MAX_IMAGES]
    extra = [f"{b.get('apartmentsCount')} apartments ({b.get('availableForSale')} for sale)" if b.get("apartmentsCount") else "",
             f"areas {b.get('minAreaOfApartments')}-{b.get('maxAreaOfApartments')} m²" if b.get("minAreaOfApartments") else "",
             f"wall type: {_en(b.get('typeOfWall'))}" if b.get("typeOfWall") else "",
             f"exploitation {b.get('exploitationDate')}, completion {b.get('completionDate')}",
             "townhouse" if b.get("isTownHouse") else ""]
    rec["description"] = short("; ".join(x for x in extra if x) + ". " + strip_tags(_en(b.get("description"))))
    return rec


def myhome_project(p: dict) -> dict:
    """Convert a myhome project (complex) detail JSON into a schema record."""
    rec = blank("myhome.am", f"https://myhome.am/en/project/{p['id']}")
    addr = p.get("address") or {}
    rec["address"], rec["city"], rec["district"] = myhome_address(addr)
    builder = p.get("builder") or {}
    rec["title"] = _en(p.get("projectName"))
    rec["developer"] = _en(builder.get("builderBrandName"))
    rec["developer_url"] = rec["website"] = builder.get("builderWebSite") or ""
    rec["lat"], rec["lng"] = clean_coord(addr.get("lat"), addr.get("lng"))
    if p.get("areaPriceStartingAt"):
        rec["price_min_amd_m2"] = p["areaPriceStartingAt"]
        rec["price_currency_raw"] = f"from {p['areaPriceStartingAt']:,.0f} AMD/m²"
    rec["completion"] = norm_completion(p.get("exploitationDate"))
    rec["status"] = "under construction"
    rec["type"] = "residential"
    rec["phones"] = phones_from(" ".join(filter(None, [builder.get("builderMobilePhoneNumber"), builder.get("builderPhoneNumber")])))
    rec["email"] = builder.get("builderEmail") or ""
    rec["images"] = list(dict.fromkeys([u for u in [p.get("mainImage"), *(p.get("images") or [])] if u]))[:MAX_IMAGES]
    rec["description"] = short(strip_tags(_en(p.get("description"))))
    return rec


def scrape_myhome() -> list[dict]:
    """All buildings from myhome.am filter_v2 plus projects whose buildings are not listed."""
    text = fetch(f"{MYHOME_API}/buildings/filter_v2", data={"pageNumber": 1, "pageSize": 500})
    try:
        items = json.loads(text)["items"]
    except (json.JSONDecodeError, KeyError, TypeError):
        print("  ! myhome filter_v2 failed", file=sys.stderr)
        return []
    out, ids = [], set()
    for it in items:
        det = fetch_json(f"{MYHOME_API}/buildings/{it['id']}", headers={"Accept": "application/json"})
        if not det:
            continue
        ids.add(it["id"])
        rec = myhome_building(det, it)
        rec["apartments"] = myhome_apartments(it["id"])
        out.append(rec)
    projects = fetch_json(f"{MYHOME_API}/projects/filter", data={"pageNumber": 1, "pageSize": 100}) or {}
    for pr in projects.get("items") or []:
        det = fetch_json(f"{MYHOME_API}/projects/{pr['id']}")
        if det and not any(b.get("id") in ids for b in det.get("buildings") or []):
            out.append(myhome_project(det))
    return out


# ----------------------------------------------------------------------------- redgroup.am
RED = "https://redgroup.am"


def red_developer(lines: list[str]) -> str:
    """Find the developer company in RED 'videoDescList' bullet lines."""
    text = "\n".join(lines).replace("u055d", ": ")
    for pref in (r"developer(?: of the complex is| company)?", r"builder", r"construction company", r"constructor"):
        for m in re.finditer(rf"\b{pref}\b\s*(?:u055d)?\s*[:\-—–՝]?\s*([^\n]+)", text, re.I):
            if re.search(r"design|development management", text[max(0, m.start() - 25):m.start()], re.I):
                continue
            v = re.split(r"\s+(?:Design(?:er| company)|Architectural Company|Construction Company|Contractor|Partner banks?|"
                         r"Builder|Main partner|Start|Construction start|The construction|Exclusive)\b\s*[:—\-–]?", m.group(1), flags=re.I)[0]
            v = re.sub(r"^(?:company|of the complex is)\s*[:—\-–]?\s*", "", v.strip(" .;"), flags=re.I).strip(" .;")
            if v and not re.match(r"(?:management|is carried)", v, re.I):
                return v
    return ""


def red_completion(lines: list[str]) -> str | None:
    """Completion date from RED bullet lines (end/completion keywords)."""
    for ln in lines:
        if re.search(r"end|complet", ln, re.I):
            seg = re.split(r"end date|end of (?:the )?construction|completion(?: of construction| date)?|construction completion", ln, flags=re.I)
            c = norm_completion(seg[-1] if len(seg) > 1 else ln)
            if c:
                return c
    return None


def red_title(p: dict) -> str:
    """Human project name: prefer the address's leading segment when short_name is a slug/teaser."""
    name = (p.get("short_name") or p.get("title") or "").strip()
    first = (p.get("address") or "").split(",")[0].strip(" «»")
    slug_like = bool(re.fullmatch(r"[a-z0-9_\-]+", name)) and "-" in name
    if slug_like or re.search(r"\s-\s|-\s", name) or (first.lower().startswith(name.lower()[:6]) and len(first) > len(name) and len(first) < 70):
        return first if first and not re.fullmatch(r"[a-z0-9_\-]+", first) else name
    return name


def red_record(d: dict) -> dict:
    """Convert a RED project detail JSON into a schema record."""
    p = d["project"]
    rec = blank("redgroup.am", f"{RED}/projects/{p['slug']}")
    content = (p.get("content") or [{}])[0] or {}
    lines = [strip_tags(x) for x in re.split(r"</li>|<br\s*/?>|</p>", content.get("videoDescList") or "") if strip_tags(x)]
    rec["title"] = red_title(p)
    rec["developer"] = red_developer(lines)
    addr = p.get("address") or ""
    rec["address"] = rec["title"] if re.fullmatch(r"[a-z0-9_\-]+", addr) else addr
    rec["city"], rec["district"] = guess_city_district(rec["address"])
    if p.get("coordinates"):
        parts = re.split(r"[,\s]+", p["coordinates"].strip())
        if len(parts) >= 2:
            rec["lat"], rec["lng"] = clean_coord(parts[0], parts[1])
    rec["completion"] = red_completion(lines)
    fill_city(rec)
    if completion_is_past(rec["completion"]) or (p.get("status") == "sold" and not rec["completion"]):
        rec["status"] = "completed"
    elif any(re.search(r"start", ln, re.I) and re.search(r"planned|scheduled", ln, re.I)
             and int((re.findall(r"20\d\d", ln) or ["0"])[0]) >= int(TODAY[:4]) for ln in lines):
        rec["status"] = "planned"
    else:
        rec["status"] = "under construction"
    products = d.get("products") or []
    floors = [f for f in d.get("floors") or [] if isinstance(f, int) and 0 < f <= 60]
    rec["floors"] = str(max(floors)) if floors else ""
    ptypes = {x.get("property_type_id") for x in products}
    rec["type"] = "commercial" if ptypes == {3} else ("mixed" if 3 in ptypes else "residential")
    if re.search(r"novotel|tsakhkadzor|tsaghkadzor", rec["title"] + rec["address"], re.I):
        rec["type"] = "resort"
    cur_map = {1: "AMD", 2: "USD", 3: "EUR", 4: "RUB"}
    units = [(x.get("rooms"), x.get("area"), x.get("price"),
              "USD" if x.get("currency_id") == 1 and (x.get("price") or 0) < 1000000 else cur_map.get(x.get("currency_id"), ""))
             for x in products if str(x.get("status") or "").lower() not in {"sold", "reserved", "booked", "sold_out"}]
    per_m2 = defaultdict(list)
    for _, area, price, cur in units:
        if area and price:
            per_m2[cur].append(price / area)
    rec["price_min_amd_m2"], rec["price_min_usd_m2"] = sane_price(
        round(min(per_m2["AMD"])) if per_m2.get("AMD") else None, round(min(per_m2["USD"])) if per_m2.get("USD") else None)
    if per_m2:
        rec["price_currency_raw"] = "; ".join(f"from {min(v):,.0f} {c}/m² (computed from {len(v)} listed units of {d.get('all_products_count')})"
                                             for c, v in per_m2.items())
    rec["apartments"] = apartments_summary([u for u in units if u[0]])
    rec["phones"] = phones_from((p.get("phone") or "") + " " + " ".join(lines))
    rec["website"] = rec["source_url"]
    if p.get("telegram_link"):
        rec["social"]["telegram"] = p["telegram_link"]
    imgs = [p.get("image")] + [f.get("url") for f in d.get("files") or []]
    rec["images"] = list(dict.fromkeys(u for u in imgs if u and u.startswith("http")))[:MAX_IMAGES]
    desc = strip_tags(content.get("description") or "")
    area = f"Apartments {d.get('min_area')}-{d.get('max_area')} m², {d.get('min_rooms')}-{d.get('max_rooms')} rooms. " if d.get("min_area") else ""
    rec["description"] = short(area + " ".join(lines) + " " + desc)
    return rec


def scrape_redgroup() -> list[dict]:
    """All RED Invest Group projects via its paginated JSON API (English)."""
    ids, page, last = [], 1, 1
    while page <= last and page <= 50:
        d = fetch_json(f"{RED}/api/projects?page={page}", headers={"Accept": "application/json"})
        if not d:
            break
        ids += [x["id"] for x in d.get("data") or []]
        last = (d.get("meta") or {}).get("last_page") or 1
        page += 1
    out = []
    for pid in dict.fromkeys(ids):
        d = fetch_json(f"{RED}/api/projects/{pid}", headers={"Accept": "application/json", "Accept-Language": "en"})
        if d and d.get("project"):
            out.append(red_record(d))
    return out


# ----------------------------------------------------------------------------- novostroiki-yerevan.com
NOVO = "https://novostroiki-yerevan.com"
NOVO_STATUS = {"under construction": "under construction", "completed": "completed", "built": "completed",
               "commissioned": "completed", "planned": "planned", "project": "planned"}


def md_field(md: str, label: str) -> str:
    """Value of a '- Label: value' bullet in novostroiki Markdown (links flattened)."""
    m = re.search(rf"^- {re.escape(label)}:\s*(.+)$", md, re.M)
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", m.group(1)).strip() if m else ""


def novo_record(url: str) -> dict | None:
    """Build a record from a novostroiki project page (.md + JSON-LD)."""
    md = fetch(url.rstrip("/") + ".md")
    if not md.startswith("#"):
        return None
    page = fetch(url)
    rec = blank("novostroiki-yerevan.com", url)
    rec["title"] = md.splitlines()[0].lstrip("# ").strip()
    rec["address"] = md_field(md, "Address")
    rec["district"] = md_field(md, "District")
    rec["city"] = "Yerevan"
    rec["developer"] = md_field(md, "Developer")
    status = md_field(md, "Status").lower()
    rec["status"] = next((v for k, v in NOVO_STATUS.items() if k in status), None)
    t = md_field(md, "Type").lower()
    rec["type"] = "mixed" if "multifunction" in t else ("commercial" if "commercial" in t or "business" in t else ("residential" if t else None))
    ppm = md_field(md, "Price per m²")
    rec["price_currency_raw"] = "; ".join(x for x in [ppm, md_field(md, "Price")] if x)
    if "$" in ppm:
        rec["price_min_usd_m2"] = to_num(ppm)
    elif ppm and re.search(r"֏|amd|dram", ppm, re.I):
        rec["price_min_amd_m2"] = to_num(ppm)
    rec["completion"] = norm_completion(md_field(md, "Completion"))
    if rec["status"] is None and completion_is_past(rec["completion"]):
        rec["status"] = "completed"
    rec["floors"] = md_field(md, "Floors")
    if m := re.search(r"Coordinates:\s*([\d.]+),\s*([\d.]+)", md):
        rec["lat"], rec["lng"] = clean_coord(m.group(1), m.group(2))
    rec["images"] = list(dict.fromkeys(re.findall(r"!\[[^\]]*\]\((https?://[^)]+)\)", md)))[:MAX_IMAGES]
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            ld = json.loads(block)
        except json.JSONDecodeError:
            continue
        if ld.get("@type") == "Product":
            split_social([u for u in ld.get("sameAs") or [] if "novostroiki-yerevan" not in u], rec)
            if ld.get("image") and not rec["images"]:
                rec["images"] = [ld["image"]]
            geo = ld.get("geo") or {}
            if rec["lat"] is None and geo:
                rec["lat"], rec["lng"] = clean_coord(geo.get("latitude"), geo.get("longitude"))
    area = md_field(md, "Area")
    rating = md_field(md, "Rating")
    rec["description"] = short(f"{md_field(md, 'Type')}; {md_field(md, 'Status')}; area {area}; price {md_field(md, 'Price')}; "
                               f"livability rating {rating}".replace("(How the rating is calculated)", ""))
    return rec


def scrape_novostroiki() -> list[dict]:
    """All project pages listed in novostroiki-yerevan.com sitemap (English)."""
    sm = fetch(f"{NOVO}/sitemap-0.xml")
    urls = sorted(set(re.findall(rf"<loc>({re.escape(NOVO)}/en/p/[^<]+/)</loc>", sm)))
    out = []
    for u in urls:
        rec = novo_record(u)
        if rec:
            out.append(rec)
    return out


# ----------------------------------------------------------------------------- ar-go.am
ARGO = "https://ar-go.am"
ARGO_STATUS = {"կառուցման փուլում": "under construction", "շինարարության փուլում": "under construction",
               "ավարտված": "completed", "շահագործման հանձնված": "completed", "պատրաստ": "completed",
               "նախագծային": "planned", "մեկնարկ": "planned", "վաճառված": "sold"}


def argo_overview(page: str) -> dict:
    """Map of <h6>label</h6><p>value</p> overview elements on an ARGO project page."""
    return {strip_tags(k): strip_tags(v) for k, v in re.findall(
        r'<h6 class="mb-0">(.*?)</h6>\s*<p class="text mb-0 fz15">(.*?)</p>', page, re.S)}


def argo_units(page: str) -> list[tuple]:
    """Apartment rows from the first page of the ARGO units table."""
    units = []
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S):
        cells = [strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)]
        kind = next((c for c in cells if "սենյակ" in c), "")
        if len(cells) >= 4 and kind:
            rooms = re.sub(r"\D", "", kind) + ("+" if "+" in kind else "")
            units.append((rooms, to_num(cells[-3]), to_num(cells[-1]), "AMD"))
    return units


def argo_record(url: str) -> dict | None:
    """Build a record from a server-rendered ar-go.am project page (Armenian)."""
    page = fetch(url)
    m = re.search(r'<h2 class="sp-lg-title">(.*?)</h2>', page, re.S)
    if not m:
        return None
    rec = blank("ar-go.am", url)
    rec["title"] = strip_tags(m.group(1))
    if a := re.search(r'<p class="text fz15 mb-0 pr10 bdrrn-sm">(.*?)</p>', page, re.S):
        rec["address"] = strip_tags(a.group(1))
    rec["city"], rec["district"] = guess_city_district(rec["address"])
    labels = [strip_tags(x).lower() for x in re.findall(r'<i class="fas fa-circle fz10 pe-2"></i>(.*?)</a>', page, re.S)]
    rec["status"] = next((v for lab in labels for k, v in ARGO_STATUS.items() if k in lab), None)
    if rec["status"] is None and labels:
        print(f"  ? ar-go unknown status {labels} {url}", file=sys.stderr)
    ov = argo_overview(page)
    art = re.search(r'<div class="text mb10 paragraph overflow-hidden article">(.*?)</div>\s*</div>', page, re.S)
    body = strip_tags(art.group(1)) if art else ""
    rec["developer"] = ov.get("Կառուցապատող", "")
    if not rec["developer"] and (dm := re.search(r"Կառուցապատող(?: ընկերություն)?\s*[՝:`]\s*([^\n]+)", body)):
        rec["developer"] = dm.group(1).strip()
    rec["completion"] = norm_completion(ov.get("Աշխատանքների ավարտ"))
    if rec["status"] == "sold":
        rec["status"] = "under construction" if rec["completion"] and not completion_is_past(rec["completion"]) else "completed"
    if rec["status"] is None and completion_is_past(rec["completion"]):
        rec["status"] = "completed"
    if pr := re.search(r'<h3 class="price mb-0">(.*?)</h3>\s*<p class="text space fz15">(.*?)</p>', page, re.S):
        raw = strip_tags(pr.group(1)) + " " + strip_tags(pr.group(2))
        rec["price_currency_raw"] = raw
        if "ք/մ" in raw and "դրամ" in raw:
            rec["price_min_amd_m2"] = to_num(raw)
        elif "ք/մ" in raw and ("$" in raw or "usd" in raw.lower()):
            rec["price_min_usd_m2"] = to_num(raw)
        rec["price_min_amd_m2"], rec["price_min_usd_m2"] = sane_price(rec["price_min_amd_m2"], rec["price_min_usd_m2"])
    if poi := re.search(r"poi%5Bpoint%5D=([\d.]+)%2C([\d.]+)", page):
        rec["lat"], rec["lng"] = clean_coord(poi.group(2), poi.group(1))
    elif ll := re.search(r"map-widget/v1/\?ll=([\d.]+)%2C([\d.]+)", page):
        rec["lat"], rec["lng"] = clean_coord(ll.group(2), ll.group(1))
    fill_city(rec)
    if fl := re.search(r"Հարկերի քանակ\s*[՝:`]?\s*([^\n]+)", body):
        rec["floors"] = fl.group(1).strip()
    rec["phones"] = ["+374 55 200707"]
    rec["website"] = url
    rec["images"] = list(dict.fromkeys(re.findall(r'class="popup-img[^"]*" href="(https?://[^"]+)"', page)))[:MAX_IMAGES]
    rec["apartments"] = apartments_summary(argo_units(page))
    stats = "; ".join(f"{k}: {v}" for k, v in ov.items() if k != "Կառուցապատող")
    rec["description"] = short(f"{stats}. {body}")
    rec["type"] = "residential"
    return rec


def scrape_argo() -> list[dict]:
    """All projects linked from ar-go.am/projects."""
    listing = fetch(f"{ARGO}/projects")
    urls = sorted(set(re.findall(r"https://ar-go\.am/project/[a-z0-9\-]+", listing)))
    return [r for r in (argo_record(u) for u in urls) if r]


# ----------------------------------------------------------------------------- acba.am
ACBA_PAGE = "https://www.acba.am/hy/individuals/loans/mortgage/constructors"


def acba_fields(content_html: str) -> dict:
    """Pair consecutive <p><strong>Label</strong></p><p>value</p> blocks from ACBA item HTML."""
    paras = [strip_tags(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", content_html, re.S)]
    paras = [p for p in paras if p]
    fields, i = {}, 0
    while i < len(paras) - 1:
        label = paras[i].rstrip(" *:").strip()
        if len(label) < 60 and not re.search(r"\d{3}", label):
            fields[label] = paras[i + 1]
            i += 2
        else:
            i += 1
    return fields


def acba_record(item: dict) -> dict:
    """Convert an ACBA ng-state 'product_developer' item into a schema record."""
    rec = blank("acba.am", f"{ACBA_PAGE}#{item.get('id')}")
    f = acba_fields(item.get("content") or "")
    get = lambda *keys: next((v for k, v in f.items() for key in keys if key in k), "")
    rec["title"] = (item.get("title") or "").strip()
    rec["developer"] = re.sub(r"^.*?Կառուցապատող\S*\s*", "", strip_tags(item.get("description") or "")).strip(" -–")
    rec["address"] = get("Հասցե")
    rec["city"], rec["district"] = guess_city_district(rec["address"])
    status = get("Կարգավիճակ").lower()
    rec["status"] = ("completed" if re.search(r"ավարտ|շահագործ", status) else
                     "under construction" if re.search(r"կառուց|շինարար", status) else None)
    rec["floors"] = short(re.sub(r"^-$", "", get("Հարկերի քանակ")), 60)
    rec["completion"] = norm_completion(get("Շահագործման ամսաթիվ", "ավարտ"))
    price = get("1 ք.մ")
    rec["price_currency_raw"] = price
    num = price_per_m2(price)
    if num and re.search(r"\$|usd|դոլար", price, re.I):
        rec["price_min_usd_m2"] = num
    elif num:
        rec["price_min_amd_m2"] = num
    rec["price_min_amd_m2"], rec["price_min_usd_m2"] = sane_price(rec["price_min_amd_m2"], rec["price_min_usd_m2"])
    rec["phones"] = phones_from(get("Հեռախոս"))
    if m := re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", get("Էլ")):
        rec["email"] = m.group(0)
    web = get("Կայք")
    if web:
        split_social(re.findall(r"https?://\S+|www\.\S+", web), rec)
    if item.get("image"):
        rec["images"] = [item["image"]]
    rec["type"] = "residential"
    rec["description"] = short("; ".join(f"{k}: {v}" for k, v in f.items() if "Կոնտակտ" not in k and "Բանկից" not in k))
    return rec


def scrape_acba() -> list[dict]:
    """Projects from ACBA bank's 'apartments from developers' page (Angular transfer state)."""
    page = fetch(ACBA_PAGE)
    m = re.search(r'<script id="ng-state" type="application/json">(.*?)</script>', page, re.S)
    if not m:
        print("  ! acba ng-state not found", file=sys.stderr)
        return []
    try:
        state = json.loads(m.group(1))
    except json.JSONDecodeError:
        return []
    items = []
    for v in state.values():
        b = v.get("b") if isinstance(v, dict) else None
        if isinstance(b, dict) and b.get("tmp_type") == "product_developers":
            items = [x for x in b.get("items") or [] if x.get("tmp_type") == "product_developer"]
            break
    return [acba_record(x) for x in items]


# ----------------------------------------------------------------------------- evoca.am
EVOCA_PAGE = "https://www.evoca.am/en/construction-companies"


def evoca_record(idx: int, title: str, body: str) -> dict:
    """Convert the ``idx``-th Evocabank accordion entry into a schema record."""
    rec = blank("evoca.am", f"{EVOCA_PAGE}#{idx}-{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}")
    text = strip_tags(re.sub(r"<table.*?</table>", " ", body, flags=re.S))
    text = re.sub(r"\s*\n\s*", " ", text)
    labels = r"(Project|Developer|Builder|Constructor|Phone|Tel\.?|Address(?:es)?|Adress|Аdress|Building adress|Office Adress|Sales Manager|Website|The loan is provided)\s*[:։]"

    def field(*names: str) -> str:
        parts = re.split(labels, text)
        for i in range(1, len(parts) - 1, 2):
            if parts[i].lower().rstrip(".") in [n.lower() for n in names]:
                return parts[i + 1].strip(" \"'")
        return ""

    project = field("Project")
    rec["developer"] = re.sub(r'["«»“”]', "", field("Developer", "Builder", "Constructor")).strip() or title
    rec["title"] = project or title
    rec["address"] = field("Building adress", "Address", "Addresses", "Adress", "Аdress") or field("Office Adress")
    rec["city"], rec["district"] = guess_city_district(rec["address"])
    rec["phones"] = phones_from(field("Phone", "Tel", "Tel."))
    web = field("Website")
    if web:
        rec["website"] = web if web.startswith("http") else f"https://{web}"
    rec["images"] = [f"https://www.evoca.am{src}" if src.startswith("/") else src
                     for src in re.findall(r'<img[^>]+src="([^"]+)"', body)][:MAX_IMAGES]
    rec["type"] = "residential"
    rec["description"] = short(text)
    return rec


def scrape_evoca() -> list[dict]:
    """Partner construction companies/projects listed by Evocabank."""
    page = fetch(EVOCA_PAGE)
    blocks = re.findall(r'<span class="accordion__title-text[^"]*">(.*?)</span>\s*</div>\s*'
                        r'<div class="accordion__content[^"]*">(.*?)</div>\s*</div>', page, re.S)
    return [evoca_record(i, strip_tags(t), b) for i, (t, b) in enumerate(blocks, 1)]


# ----------------------------------------------------------------------------- byblosbankarmenia.am
BYBLOS_PAGE = "https://www.byblosbankarmenia.am/en/developers"


def scrape_byblos() -> list[dict]:
    """Partner developer cards on Byblos Bank Armenia's developers page."""
    page = fetch(BYBLOS_PAGE)
    out = []
    for title, img, body in re.findall(r'<div class="hidden_title">(.*?)</div>\s*<div class="hidden_image">(.*?)</div>\s*'
                                       r'<div class="hidden_text">(.*?)</div>\s*<div class="hidden_address">', page, re.S):
        title = strip_tags(title)
        rec = blank("byblosbankarmenia.am", f"{BYBLOS_PAGE}#{re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')}")
        text = strip_tags(body)
        rec["title"] = title
        if m := re.search(r"Address:\s*([^\n]+)", text):
            rec["address"] = m.group(1).strip()
        elif m := re.search(r"\bat ([\d/]+ [A-Z][\w. ]+?)\.", text):
            rec["address"] = m.group(1)
        elif m := re.search(r"on ([A-Z]\. [A-Z]\w+ Street)", text):
            rec["address"] = m.group(1)
        rec["city"], rec["district"] = guess_city_district(rec["address"])
        rec["city"] = rec["city"] or "Yerevan"
        if m := re.search(r"\b([\w ]+ LLC)\b", title):
            rec["developer"] = m.group(1)
        rec["phones"] = phones_from(text)
        links = re.findall(r'href="(https?://[^"]+)"', body)
        rec["website"] = links[0] if links else ""
        if img.strip():
            rec["images"] = [f"https://www.byblosbankarmenia.am/{img.strip().lstrip('/')}"]
        rec["type"] = "residential"
        rec["status"] = "under construction" if "being constructed" in text else None
        rec["description"] = short(text)
        out.append(rec)
    return out


# ----------------------------------------------------------------------------- main
SOURCES = [("myhome.am", scrape_myhome), ("redgroup.am", scrape_redgroup),
           ("novostroiki-yerevan.com", scrape_novostroiki), ("ar-go.am", scrape_argo),
           ("acba.am", scrape_acba), ("evoca.am", scrape_evoca), ("byblosbankarmenia.am", scrape_byblos)]


def dedupe(records: list[dict]) -> list[dict]:
    """Drop duplicate records sharing source + source_url (first wins)."""
    seen, out = set(), []
    for r in records:
        key = (r["source"], r["source_url"])
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def write(records: list[dict]) -> None:
    """Atomically write the output JSON."""
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(OUT)


def report(records: list[dict]) -> None:
    """Print per-source coverage stats."""
    by = defaultdict(list)
    for r in records:
        by[r["source"]].append(r)
    for src, rs in by.items():
        coords = sum(r["lat"] is not None for r in rs)
        addr_only = sum(r["lat"] is None and bool(r["address"]) for r in rs)
        price = sum(bool(r["price_min_usd_m2"] or r["price_min_amd_m2"]) for r in rs)
        imgs = sum(bool(r["images"]) for r in rs)
        devs = len({r["developer"] for r in rs if r["developer"]})
        print(f"{src}: {len(rs)} projects, {devs} developers, coords {coords}, address-only {addr_only}, price {price}, images {imgs}")


def main(selected: list[str]) -> None:
    """Run the selected (default: all) catalog scrapers, rewriting the output after each."""
    existing = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() and selected else []
    records = [r for r in existing if r["source"] not in selected]
    for name, fn in SOURCES:
        if selected and name not in selected:
            continue
        print(f"== {name}", file=sys.stderr)
        try:
            got = fn()
        except Exception as e:  # keep other sources running
            print(f"  ! {name} failed: {e!r}", file=sys.stderr)
            continue
        print(f"   {len(got)} records", file=sys.stderr)
        records = dedupe(records + got)
        write(records)
    report(records)


if __name__ == "__main__":
    main(sys.argv[1:])
