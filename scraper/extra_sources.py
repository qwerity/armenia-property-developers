"""Scrape Armenian new-building projects from sources other than karucapatoxic.am.

Sources: geoln.com, construction.am, yerevan.etagi.com, dignisi.am, ac-box.com, newcity.am.
Output: ./extra_sources.json — list of normalized project dicts (see ``blank()``).
Only items with coordinates or a street address are kept.
"""
import html as htmllib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"
HERE = Path(__file__).resolve().parent
OUT = HERE / "extra_sources.json"
CACHE = HERE / ".cache_extra"
DELAY = 0.6
_DEC = json.JSONDecoder()
ARMENIA_BBOX = (38.8, 41.35, 43.4, 46.7)  # lat_min, lat_max, lng_min, lng_max


def fetch(url: str, retries: int = 3) -> str:
    """Fetch ``url`` as text with on-disk cache, polite delay and retry/backoff.

    Returns "" when every attempt fails (the failure is logged to stderr).
    """
    CACHE.mkdir(exist_ok=True)
    cf = CACHE / (re.sub(r"[^a-zA-Z0-9]+", "_", url).strip("_")[:180] + ".html")
    if cf.exists() and cf.stat().st_size > 500:
        return cf.read_text(encoding="utf-8")
    for attempt in range(retries):
        try:
            time.sleep(DELAY)
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en,ru;q=0.8"})
            with urllib.request.urlopen(req, timeout=40) as r:
                text = r.read().decode("utf-8", errors="replace")
            cf.write_text(text, encoding="utf-8")
            return text
        except Exception as e:  # network errors, 4xx/5xx
            if attempt == retries - 1:
                print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
                return ""
            time.sleep(2 ** attempt)
    return ""


def blank(source: str, url: str) -> dict:
    """Return an empty record in the output schema."""
    return {
        "source": source, "source_url": url, "title": "", "developer": "", "developer_url": "",
        "city": "", "district": "", "address": "", "lat": None, "lng": None,
        "price_min_usd_m2": None, "price_min_amd_m2": None, "price_currency_raw": "",
        "completion": None, "status": None, "floors": "", "type": None, "phones": [],
        "email": "", "website": "", "social": {}, "images": [], "videos": [], "description": "",
    }


def strip_tags(s: str) -> str:
    """HTML fragment -> collapsed plain text."""
    s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s or "", flags=re.S)
    s = re.sub(r"<br\s*/?>|</(p|li|div|h\d)>", "\n", s)
    s = htmllib.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"[ \t\r\f\v]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()


def short(text: str, n: int = 600) -> str:
    """Single-line text truncated at a word boundary to at most ``n`` chars."""
    t = re.sub(r"\s+", " ", text or "").strip()
    if len(t) <= n:
        return t
    return t[: n - 1].rsplit(" ", 1)[0] + "…"


def to_num(s) -> float | None:
    """Parse '1 185', '400,000', '1500.5' to a number; None if not parseable."""
    if s is None:
        return None
    digits = re.sub(r"[^\d.]", "", str(s).replace(",", ""))
    try:
        return float(digits) if digits else None
    except ValueError:
        return None


def valid_coords(lat, lng) -> bool:
    """True when lat/lng fall inside Armenia's bounding box."""
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return False
    return ARMENIA_BBOX[0] <= lat <= ARMENIA_BBOX[1] and ARMENIA_BBOX[2] <= lng <= ARMENIA_BBOX[3]


def set_coords(rec: dict, lat, lng) -> None:
    """Store coordinates on ``rec`` only if they are inside Armenia."""
    if valid_coords(lat, lng):
        rec["lat"], rec["lng"] = round(float(lat), 7), round(float(lng), 7)


def set_price(rec: dict, value, currency: str, raw: str) -> None:
    """Store a per-m² price under the USD or AMD field based on ``currency``."""
    v = to_num(value)
    if not v:
        return
    rec["price_currency_raw"] = raw.strip()
    if currency.upper() in ("USD", "$"):
        rec["price_min_usd_m2"] = v
    elif currency.upper() in ("AMD", "֏", "DRAM"):
        rec["price_min_amd_m2"] = v


def ld_json_blocks(page: str) -> list:
    """All parseable JSON-LD objects in a page (flattening @graph)."""
    out = []
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        items = d if isinstance(d, list) else d.get("@graph", [d])
        out.extend(x for x in items if isinstance(x, dict))
    return out


# ---------------------------------------------------------------- geoln.com
GEOLN = "https://geoln.com"


def geoln_project_urls() -> list[str]:
    """Collect Armenian project URLs from geoln country/city listing pages."""
    seeds = ["/ru/armenia", "/ru/armenia?page=2", "/ru/armenia/yerevan", "/ru/armenia/yerevan-new-buildings-on-map"]
    urls, cities = set(), set()
    for s in seeds:
        page = fetch(GEOLN + s)
        urls.update(re.findall(r'href="(/ru/armenia/[a-z0-9-]+/[a-z0-9-]+)"', page))
        cities.update(re.findall(r'href="(/ru/armenia/[a-z0-9-]+)"', page))
    for c in sorted(cities - {"/ru/armenia/cheap-construction-homes", "/ru/armenia/yerevan-new-buildings-on-map"}):
        urls.update(re.findall(r'href="(/ru/armenia/[a-z0-9-]+/[a-z0-9-]+)"', fetch(GEOLN + c)))
    return sorted(GEOLN + u for u in urls)


def geoln_text_field(text: str, label: str) -> str:
    """Value on the line(s) following ``label`` in geoln page text."""
    m = re.search(re.escape(label) + r"\s*\n\s*([^\n]+)(?:\n\s*(\d{4}))?", text)
    if not m:
        return ""
    return " ".join(x.strip() for x in m.groups() if x)


def geoln_project(url: str) -> dict | None:
    """Parse one geoln project page (JSON-LD Event/FAQ + visible text)."""
    page = fetch(url)
    if not page:
        return None
    rec = blank("geoln", url)
    rec["type"] = "residential"
    for b in ld_json_blocks(page):
        if b.get("@type") == "Event" and b.get("location"):
            loc = b["location"]
            rec["title"] = rec["title"] or loc.get("name", "")
            rec["address"] = rec["address"] or (loc.get("address") or {}).get("streetAddress", "")
            geo = loc.get("geo") or {}
            if rec["lat"] is None:
                set_coords(rec, geo.get("latitude"), geo.get("longitude"))
            rec["developer"] = rec["developer"] or b.get("performer", "")
            if b.get("image"):
                rec["images"].append(urllib.parse.urljoin(GEOLN, b["image"].replace(".medium.", ".large.")))
        if b.get("@type") == "FAQPage":
            for q in b.get("mainEntity", []):
                ans = (q.get("acceptedAnswer") or {}).get("text", "")
                if "квадратн" in q.get("name", "") + ans:
                    m = re.search(r"([\d\s]+)\$", ans)
                    if m:
                        set_price(rec, m.group(1), "USD", ans)
                if "этаж" in q.get("name", ""):
                    m = re.search(r"(\d+)\s+этаж", ans)
                    rec["floors"] = m.group(1) if m else rec["floors"]
    rec["city"] = _geoln_city_from_url(url)
    text = strip_tags(page[page.find("<body"):])
    done = geoln_text_field(text, "Окончание постройки")
    rec["completion"] = done or None
    if done and (m := re.search(r"(\d{4})", done)):
        rec["status"] = "under construction" if int(m.group(1)) >= time.localtime().tm_year else None
    rec["floors"] = rec["floors"] or geoln_text_field(text, "Этажей")
    m = re.search(r"Описание новостройки(.*?)(Окончание постройки|$)", text, re.S)
    desc_block = re.search(r'<div[^>]*class="[^"]*(description|about)[^"]*"[^>]*>(.*?)</div>', page, re.S)
    rec["description"] = short(strip_tags(desc_block.group(2))) if desc_block else ""
    gallery = page[page.find("Рендеры"): page.find("Рендеры") + 8000] if "Рендеры" in page else ""
    for img in re.findall(r"/uploads/building_photos/[0-9a-f]+\.(?:large|medium)\.jpg", gallery):
        full = GEOLN + img.replace(".medium.", ".large.")
        if full not in rec["images"]:
            rec["images"].append(full)
    rec["images"] = list(dict.fromkeys(rec["images"]))[:10]
    return rec


def _geoln_city_from_url(url: str) -> str:
    """City slug from a geoln project URL, title-cased."""
    parts = urllib.parse.urlparse(url).path.split("/")
    return parts[3].replace("-", " ").title() if len(parts) > 3 else ""


def scrape_geoln() -> list[dict]:
    """All geoln Armenian projects."""
    return [r for u in geoln_project_urls() if (r := geoln_project(u))]


# ------------------------------------------------------------ construction.am
CAM = "https://www.construction.am"
YEREVAN_DISTRICTS = {
    "Kentron", "Center", "Arabkir", "Ajapnyak", "Avan", "Davtashen", "Nor Nork", "Kanaker-Zeytun",
    "Nork-Marash", "Shengavit", "Malatia-Sebastia", "Erebuni", "Nubarashen",
}


def cam_table(page: str) -> dict:
    """Label -> value from the construction.am project details table."""
    rows = {}
    for tr in re.findall(r"<tr>(.*?)</tr>", page, re.S):
        tds = [strip_tags(t) for t in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        if len(tds) >= 3 and tds[1]:
            rows[tds[1]] = re.sub(r"\s+", " ", tds[2]).strip()
    return rows


def cam_project(url: str) -> dict | None:
    """Parse one construction.am new-development page."""
    page = fetch(url)
    if not page:
        return None
    rec = blank("construction.am", url)
    m = re.search(r'<li class="active"><h3[^>]*>(.*?)</h3>', page, re.S)
    full_title = strip_tags(m.group(1)) if m else ""
    parts = [p.strip() for p in full_title.split(",")]
    rec["district"] = parts[0] if parts else ""
    rec["title"] = parts[-1] if parts else full_title
    rec["address"] = ", ".join(parts[1:]) if len(parts) > 1 else ""
    rec["city"] = "Yerevan" if rec["district"] in YEREVAN_DISTRICTS else rec["district"]
    if (m := re.search(r"maps/embed/v1/place\?[^\"']*q=(-?[\d.]+),(-?[\d.]+)", page)):
        set_coords(rec, m.group(1), m.group(2))
    rows = cam_table(page)
    dev = re.search(r'Developer</td>\s*<td[^>]*>\s*<a href="([^"]+)"[^>]*>(.*?)</a>', page, re.S)
    rec["developer"] = strip_tags(dev.group(2)) if dev else rows.get("Developer", "")
    rec["developer_url"] = dev.group(1) if dev else ""
    comp = rows.get("Completion", "")
    rec["completion"] = re.sub(r"\s*/\s*(Completed)", "", comp) or None
    rec["status"] = "completed" if "Completed" in comp else ("under construction" if comp else None)
    rec["floors"] = rows.get("Floors Above Ground", "")
    purpose = rows.get("Functional Purpose", "").lower()
    rec["type"] = ("mixed" if "commercial" in purpose and "resid" in purpose
                   else "commercial" if re.search(r"commercial|office|business", purpose)
                   else "residential" if purpose else None)
    pm = re.search(r"Price:\s*([^<]*)", page)
    raw_price = strip_tags(pm.group(1)) if pm else ""
    if raw_price and "No information" not in raw_price:
        cur = "USD" if re.search(r"\$|USD", raw_price) else "AMD" if re.search(r"AMD|֏|dram", raw_price, re.I) else ""
        nums = re.findall(r"\d[\d,\s.]*", raw_price)
        if nums and cur:
            set_price(rec, nums[0], cur, raw_price)
        else:
            rec["price_currency_raw"] = raw_price
    body = re.search(r'<div class="panel-body fontsize-16[^"]*"[^>]*>(.*?)</div>', page, re.S)
    rec["description"] = short(strip_tags(body.group(1))) if body else ""
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    imgs = re.findall(r'(https://www\.construction\.am/images/apartmentimages/new/%s/[^"?]+\.(?:jpe?g|png|webp))' % re.escape(slug), page)
    rec["images"] = [i for i in dict.fromkeys(imgs) if "_525x350" not in i][:10]
    rec["videos"] = list(dict.fromkeys(re.findall(r'(https?://(?:www\.)?(?:youtube\.com/(?:embed/|watch\?v=)|youtu\.be/)[\w-]+)', page)))
    return rec


def scrape_construction_am() -> list[dict]:
    """All projects linked from construction.am/apartments.php."""
    listing = fetch(CAM + "/apartments.php")
    urls = sorted(set(re.findall(r'href="(https://www\.construction\.am/apartments-in-new-developments/[^"]+/)"', listing)))
    return [r for u in urls if (r := cam_project(u))]


# --------------------------------------------------------- yerevan.etagi.com
ETAGI = "https://yerevan.etagi.com"


def json_objects_after(page: str, marker: str) -> list:
    """raw_decode the JSON value opened by the last '{' or '[' inside each ``marker`` occurrence."""
    out, pos = [], 0
    opener = max(marker.rfind("{"), marker.rfind("["))
    while (i := page.find(marker, pos)) != -1:
        start = i + opener
        try:
            obj, end = _DEC.raw_decode(page, start)
            out.append(obj)
            pos = end
        except json.JSONDecodeError:
            pos = i + len(marker)
    return out


def etagi_deadline(code) -> str | None:
    """Etagi deadline code (year*4 + quarter) -> 'YYYY-Qn'."""
    try:
        c = int(code)
    except (TypeError, ValueError):
        return None
    return f"{(c - 1) // 4}-Q{(c - 1) % 4 + 1}" if c > 4000 else None


def etagi_project(item: dict) -> dict | None:
    """Enrich one etagi listing complex with its detail page (coords, description, photos)."""
    cid, slug = item.get("newcomplex_id"), item.get("nntr") or "jk"
    url = f"{ETAGI}/en-us/zastr/jk/{slug}-{cid}/"
    page = fetch(url)
    rec = blank("etagi", url)
    meta = item.get("meta") or {}
    rec["title"] = item.get("newcomplex_name") or meta.get("newcomplex", "")
    rec["developer"] = (item.get("builder") or "").strip()
    city = meta.get("city") or ""
    rec["city"] = "Yerevan" if re.search(r"Ереван|Երևան|վարչական շրջան", city) else city
    rec["district"] = meta.get("district") or ""
    rec["address"] = meta.get("street") or ""
    rec["completion"] = etagi_deadline(item.get("min_deadline") or item.get("max_deadline"))
    rec["status"] = "under construction"
    rec["type"] = "residential"
    set_price(rec, item.get("price_m2"), "USD", f"from ${item.get('price_m2')}/m² (etagi min price per m²)")
    if item.get("main_photo"):
        rec["images"].append(item["main_photo"])
    gps = next(iter(json_objects_after(page, '"newHouseGps":[')), []) if page else []
    for g in gps:
        set_coords(rec, g.get("la"), g.get("lo"))
        for p in g.get("params") or []:
            rec["floors"] = rec["floors"] or str(p.get("floors") or "")
        if rec["lat"] is not None:
            break
    house = next(iter(json_objects_after(page, '"newHouse":{')), {}) if page else {}
    if isinstance(house, dict):
        rec["description"] = short(house.get("description", ""))
        if (ph := house.get("phone")) and re.search(r"\d{5}", str(ph)):
            rec["phones"] = [ph]
    for photos in json_objects_after(page, '"groupedNewcomplexMedia":{'):
        for p in (photos.get("photos") or []):
            if p.get("fname") and p["fname"] not in rec["images"]:
                rec["images"].append(p["fname"])
        break
    rec["images"] = rec["images"][:10]
    return rec


def scrape_etagi() -> list[dict]:
    """All complexes listed on yerevan.etagi.com/zastr (single SSR page)."""
    listing = fetch(ETAGI + "/en-us/zastr/")
    items = {}
    for obj in json_objects_after(listing, '{"newcomplex_id":'):
        if isinstance(obj, dict) and obj.get("class") == "newHouses":
            items[obj["newcomplex_id"]] = obj
    return [r for it in items.values() if (r := etagi_project(it))]


# ------------------------------------------------------------------ dignisi.am
DIGNISI = "https://dignisi.am"


def dignisi_project(url: str) -> dict | None:
    """Parse a dignisi.am English project page (JSON-LD + header/stat list)."""
    page = fetch(url)
    if not page:
        return None
    rec = blank("dignisi", url)
    rec["type"] = "residential"
    for b in ld_json_blocks(page):
        if b.get("@type") == "ApartmentComplex":
            rec["title"] = b.get("name", "")
            geo, addr = b.get("geo") or {}, b.get("address") or {}
            set_coords(rec, geo.get("latitude"), geo.get("longitude"))
            rec["city"] = addr.get("addressLocality", "")
            rec["description"] = short(b.get("description", ""))
    if rec["lat"] is None and "Dubai" in page[:200000] and "/new-buildings/yerevan" not in page:
        return None
    if (m := re.search(r"<h1[^>]*>.*?</h1>\s*<p[^>]*>(.*?)</p>", page, re.S)):
        loc = [x.strip() for x in strip_tags(m.group(1)).split("·")]
        rec["address"] = loc[0] if loc else ""
        rec["district"] = loc[1] if len(loc) > 1 else ""
    crumbs = re.findall(r'href="/en/new-buildings/([a-z0-9-]+)(?:/([a-z0-9-]+))?"[^>]*>([^<]+)</a><span aria-hidden', page)
    if crumbs:
        city_slug, sub, name = crumbs[-1]
        rec["city"] = city_slug.replace("-", " ").title()
        rec["district"] = name if sub else rec["district"]
    header = page[page.find("<h1"): page.find("<h1") + 6000]
    status = re.search(r"</svg>(Under construction|Completed|Planned|Ready|Handed over)</span>", header)
    if status:
        rec["status"] = "completed" if status.group(1) in ("Completed", "Ready", "Handed over") else status.group(1).lower()
    if (pm := re.search(r">from(?:<!-- -->|\s)*([\d,]+)(?:<!-- -->|\s)*([֏$€])", header)):
        set_price(rec, pm.group(1), "AMD" if pm.group(2) == "֏" else "USD" if pm.group(2) == "$" else "", f"from {pm.group(1)} {pm.group(2)}/m²")
    stats = dict((strip_tags(k), strip_tags(v)) for k, v in re.findall(r"<dt[^>]*>(.*?)</dt><dd[^>]*>(.*?)</dd>", page, re.S))
    rec["completion"] = stats.get("Handover") or None
    rec["floors"] = stats.get("Floors", "")
    imgs = [src for src, alt in re.findall(r'<img[^>]*?src="(https://nkar\.dignisi\.am/[^"]+)"[^>]*?alt="([^"]*)"', page)
            if htmllib.unescape(alt).strip() == rec["title"]]
    rec["images"] = list(dict.fromkeys(imgs))[:10]
    return rec


def scrape_dignisi() -> list[dict]:
    """All dignisi.am projects from its sitemap, dropping ones outside Armenia."""
    sm = fetch(DIGNISI + "/sitemap.xml")
    urls = sorted(set(re.findall(r"<loc>(https://dignisi\.am/en/projects/[^<]+)</loc>", sm)))
    out = []
    for u in urls:
        r = dignisi_project(u)
        if r and r["lat"] is not None:  # catalogue also lists Dubai/Cyprus/Batumi; only Armenian coords pass
            out.append(r)
    return out


# ------------------------------------------------------------------ ac-box.com
ACBOX = "https://ac-box.com"
ACBOX_CITIES = {"Ереван": "Yerevan", "Цахкадзор": "Tsaghkadzor", "Прошян": "Proshyan", "Зовуни": "Zovuni"}


def acbox_json_parse_args(page: str) -> list[tuple[str, object]]:
    """Decode every ``name: JSON.parse('...')`` Alpine.js payload on the page."""
    out = []
    for m in re.finditer(r"(\w+): JSON\.parse\('((?:[^'\\]|\\.)*)'\)", page):
        try:
            js_str = json.loads('"' + m.group(2).replace('"', '\\"') + '"')
            out.append((m.group(1), json.loads(js_str)))
        except json.JSONDecodeError:
            continue
    return out


def acbox_record(b: dict) -> dict:
    """Normalize one ac-box building payload."""
    rec = blank("ac-box", b.get("url", ""))
    rec["title"] = b.get("title", "")
    rec["developer"] = b.get("developer") or ""
    rec["website"] = rec["developer_url"] = b.get("developer_website") or ""
    city = b.get("city") or ""
    rec["city"] = ACBOX_CITIES.get(city, city)
    rec["district"], rec["address"] = b.get("district") or "", b.get("address") or ""
    rec["completion"] = b.get("completion") or None
    rec["type"] = "residential"
    emb = b.get("map_embed_url") or ""
    if (m := re.search(r"pt=(-?[\d.]+)%2C(-?[\d.]+)", emb)) or (m := re.search(r"ll=(-?[\d.]+)%2C(-?[\d.]+)", emb)):
        set_coords(rec, m.group(2), m.group(1))
    raw = b.get("price") or ""
    if (pm := re.search(r"([$֏€])\s*([\d\s ]+)", raw)):
        set_price(rec, pm.group(2), "USD" if pm.group(1) == "$" else "AMD" if pm.group(1) == "֏" else "", raw)
    wa = b.get("developer_whatsapp_url") or ""
    if (pm := re.search(r"wa\.me/(\d+)", wa)):
        rec["phones"] = ["+" + pm.group(1)]
        rec["social"]["whatsapp"] = "https://wa.me/" + pm.group(1)
    if b.get("developer_telegram_url"):
        rec["social"]["telegram"] = b["developer_telegram_url"]
    rec["images"] = [urllib.parse.urljoin(ACBOX, g) for g in (b.get("gallery") or [])][:10]
    rec["videos"] = [v["url"].split("?")[0] for v in (b.get("videos") or []) if v.get("url")]
    rec["description"] = short(b.get("description_text") or strip_tags(b.get("description_html") or ""))
    return rec


def scrape_acbox() -> list[dict]:
    """All ac-box catalogue buildings (every project page embeds the full catalogue)."""
    listing = fetch(ACBOX + "/novostroyki")
    urls = sorted(set(re.findall(r'href="(https://ac-box\.com/novostroyki/(?!gorod/)[a-z0-9-]+)"', listing)))
    buildings: dict[str, dict] = {}
    for u in urls:
        for name, obj in acbox_json_parse_args(fetch(u)):
            if isinstance(obj, dict) and obj.get("slug"):
                prev = buildings.get(obj["slug"], {})
                if name == "initialBuilding" or not prev:
                    buildings[obj["slug"]] = {**prev, **obj}
    return [acbox_record(b) for b in buildings.values()]


# ------------------------------------------------------------------ newcity.am
NEWCITY = "https://newcity.am"


def scrape_newcity() -> list[dict]:
    """New City developer projects; address/completion parsed from meta description."""
    listing = fetch(NEWCITY + "/en/projects")
    out = []
    for u in sorted(set(re.findall(r'href="(https://newcity\.am/en/projects/[a-z0-9-]+)"', listing))):
        page = fetch(u)
        desc = re.search(r'<meta name="description" content="([^"]*)"', page)
        d = htmllib.unescape(desc.group(1)) if desc else ""
        addr = re.search(r"\(([^)]*\d[^)]*)\)", d)
        if not addr:
            continue
        rec = blank("newcity.am", u)
        name = re.search(r"-\s*([^()\-]+?)\s*\(", d)
        rec["title"] = name.group(1).strip() if name else u.rsplit("/", 1)[-1].replace("-", " ").title()
        rec["developer"], rec["developer_url"], rec["website"] = "New City", NEWCITY, NEWCITY
        rec["city"], rec["address"], rec["type"] = "Yerevan", addr.group(1), "residential"
        if (c := re.search(r"Completion:\s*([A-Za-z]+\s+\d{4}|\d{4})", d)):
            rec["completion"] = c.group(1)
            rec["status"] = "under construction"
        rec["description"] = short(d)
        og = re.findall(r'<meta property="og:image" content="([^"]+)"', page)
        rec["images"] = og[:10]
        out.append(rec)
    return out


# ---------------------------------------------------------------------- main
SCRAPERS = {
    "geoln": scrape_geoln,
    "construction.am": scrape_construction_am,
    "etagi": scrape_etagi,
    "dignisi": scrape_dignisi,
    "ac-box": scrape_acbox,
    "newcity.am": scrape_newcity,
}


TITLE_NOISE = re.compile(
    r"residential|residence|residance|complex|district|building|house|plaza|club|new|"
    r"жк|жилой|комплекс|բնակելի|համալիր|թաղամաս|ռեզիդենս", re.I)


def norm_title(title: str) -> str:
    """Lower-cased title with generic words and punctuation removed (for fuzzy matching)."""
    return re.sub(r"[\W_]+", "", TITLE_NOISE.sub("", title.lower()))


def distance_m(a: dict, b: dict) -> float:
    """Approximate metres between two records with coordinates (equirectangular)."""
    from math import cos, radians, hypot
    dy = (a["lat"] - b["lat"]) * 111_320
    dx = (a["lng"] - b["lng"]) * 111_320 * cos(radians((a["lat"] + b["lat"]) / 2))
    return hypot(dx, dy)


def richness(r: dict) -> int:
    """Number of populated fields; used to pick the survivor among duplicates."""
    return sum(1 for k, v in r.items() if v not in (None, "", [], {}))


def same_project(a: dict, b: dict) -> bool:
    """Cross-source duplicate test: matching normalized title and within 300 m."""
    if a["lat"] is None or b["lat"] is None or distance_m(a, b) > 300:
        return False
    ta, tb = norm_title(a["title"]), norm_title(b["title"])
    if len(ta) < 4 or len(tb) < 4:
        return False
    return ta == tb or ta in tb or tb in ta


def dedupe(records: list[dict]) -> list[dict]:
    """Keep locatable items, drop repeated URLs, and merge cross-source duplicates.

    The richest record of a duplicate group survives; the others' URLs are kept in
    ``alt_source_urls`` so no provenance is lost.
    """
    seen, uniq = set(), []
    for r in records:
        key = r["source_url"].rstrip("/").lower()
        if key in seen or not (r["lat"] is not None or r["address"]):
            continue
        seen.add(key)
        uniq.append(r)
    uniq.sort(key=richness, reverse=True)
    out: list[dict] = []
    for r in uniq:
        match = next((o for o in out if o["source"] != r["source"] and same_project(o, r)), None)
        if match is None:
            r.setdefault("alt_source_urls", [])
            out.append(r)
        else:
            match["alt_source_urls"].append(r["source_url"])
            for f in ("price_min_usd_m2", "price_min_amd_m2", "developer", "completion", "floors", "description"):
                if not match[f] and r[f]:
                    match[f] = r[f]
            if not match["images"]:
                match["images"] = r["images"]
    return out


def main(selected: list[str]) -> None:
    """Run the selected scrapers (all by default) and write OUT."""
    results = []
    for name, fn in SCRAPERS.items():
        if selected and name not in selected:
            continue
        print(f"[{name}] scraping…", file=sys.stderr)
        try:
            recs = fn()
        except Exception as e:  # keep other sources running
            print(f"[{name}] FAILED: {e!r}", file=sys.stderr)
            continue
        print(f"[{name}] {len(recs)} records", file=sys.stderr)
        results.extend(recs)
    results = dedupe(results)
    OUT.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {len(results)} records -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
