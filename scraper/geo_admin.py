"""Assign canonical province (marz), Yerevan district / town names to coordinates using OSM boundaries.

Boundary sources (downloaded once via Overpass into scraper/geo/):
  admin_raw.json   — Armenia relations admin_level 4 (provinces), 6/8 (towns / communities)
  yerevan_raw.json — relations inside Yerevan, admin_level 5 (12 districts)
"""
import json
import re
from functools import lru_cache
from pathlib import Path

from shapely.geometry import LineString, Point
from shapely.ops import linemerge, polygonize, unary_union
from shapely.prepared import prep

GEO = Path(__file__).resolve().parent / "geo"
CANONICAL = {
    "Norq Marash": "Nork-Marash", "Nor Norq": "Nor Nork", "Qanaqer-Zeytun": "Kanaker-Zeytun",
    "Tsakhkadzor": "Tsaghkadzor", "Vagharshapat": "Vagharshapat (Etchmiadzin)",
}
TOWN_ALIASES = {
    "tsakhkadzor": "Tsaghkadzor", "etchmiadzin": "Vagharshapat (Etchmiadzin)", "echmiadzin": "Vagharshapat (Etchmiadzin)",
    "vagharshapat": "Vagharshapat (Etchmiadzin)", "էջմիածին": "Vagharshapat (Etchmiadzin)", "dzorakhbyur": "Dzoraghbyur",
    "կոտայք": None, "kotayk": None, "yerevan": None, "armenia": None,
}


def _relation_polygon(el: dict):
    outers, inners = [], []
    for m in el.get("members", []):
        if m.get("type") != "way" or len(m.get("geometry") or []) < 2:
            continue
        line = LineString([(p["lon"], p["lat"]) for p in m["geometry"]])
        (inners if m.get("role") == "inner" else outers).append(line)
    outer = unary_union(list(polygonize(linemerge(outers)))) if outers else None
    if outer is None or outer.is_empty:
        return None
    if inners:
        holes = unary_union(list(polygonize(linemerge(inners))))
        if not holes.is_empty:
            outer = outer.difference(holes)
    return outer.buffer(0)


def _name(tags: dict) -> str:
    n = tags.get("name:en") or tags.get("name") or ""
    n = re.sub(r"\s+Province$", "", n)
    return CANONICAL.get(n, n)


@lru_cache(maxsize=1)
def _layers():
    layers = {"province": [], "district": [], "town": []}
    for fname, levels in (("admin_raw.json", {"4": "province", "6": "town", "8": "town"}), ("yerevan_raw.json", {"5": "district"})):
        f = GEO / fname
        if not f.exists():
            continue
        for el in json.loads(f.read_text(encoding="utf-8")).get("elements", []):
            layer = levels.get(el.get("tags", {}).get("admin_level"))
            if not layer:
                continue
            poly = _relation_polygon(el)
            if poly is not None:
                layers[layer].append((_name(el["tags"]), prep(poly)))
    return layers


def _lookup(layer: str, lng: float, lat: float) -> str | None:
    pt = Point(lng, lat)
    return next((name for name, poly in _layers()[layer] if poly.contains(pt)), None)


PROVINCES = {"yerevan", "kotayk", "ararat", "armavir", "aragatsotn", "tavush", "lori", "shirak", "syunik", "vayots dzor", "gegharkunik"}
YEREVAN_DISTRICT_WORDS = re.compile(r"avan|davtashen|arabkir|kentron|ajapnyak|nork|zeytun|zeytoun|malat|shengavit|erebuni|nubarashen|"
                                    r"արաբկիր|ավան|կենտրոն|դավթաշեն|աջափնյակ|նորք|զեյթուն|մալաթիա|центр|арабкир|норк|зейтун", re.I)


PROVINCE_NAMES = {
    "Yerevan": r"yerevan|երևան|ереван", "Kotayk": r"kotayk|կոտայք|котайк", "Ararat": r"ararat province|ararat region|արարատի մարզ|араратск",
    "Armavir": r"armavir|արմավիր|армавир", "Aragatsotn": r"aragatsotn|արագածոտն|арагацотн", "Tavush": r"tavush|տավուշ|тавуш",
    "Lori": r"\blori\b|լոռի|лори", "Shirak": r"shirak|շիրակ|ширак", "Syunik": r"syunik|սյունիք|сюник",
    "Vayots Dzor": r"vayots|վայոց|вайоц", "Gegharkunik": r"gegharkunik|գեղարքունիք|гегаркуник",
}


def province_hint(text: str) -> str | None:
    """Province explicitly named in free text (excluding Yerevan, which appears in many suburban addresses)."""
    found = [name for name, pat in PROVINCE_NAMES.items() if name != "Yerevan" and re.search(pat, text or "", re.I)]
    return found[0] if len(found) == 1 else None


DISTRICT_PATTERNS = {
    "Arabkir": r"arabkir|արաբկիր|арабкир", "Kentron": r"kentron|կենտրոն|кентрон", "Ajapnyak": r"ajapnyak|աջափնյակ|аджапняк",
    "Avan": r"\bavan\b|ավան|аван", "Davtashen": r"davtashen|դավթաշեն|давташен", "Erebuni": r"erebuni|էրեբունի|эребуни",
    "Kanaker-Zeytun": r"kanaker|zeytun|zeytoun|qanaqer|քանաքեռ|զեյթուն|канакер|зейтун", "Malatia-Sebastia": r"malat|մալաթիա|малатия",
    "Nor Nork": r"nor[\s-]?nor[kq]|նոր նորք|нор[\s-]норк", "Nork-Marash": r"nor[kq][\s-]marash|նորք[\s-]մարաշ|норк[\s-]мараш",
    "Nubarashen": r"nubarashen|նուբարաշեն|нубарашен", "Shengavit": r"shengavit|շենգավիթ|шенгавит",
}
TOWN_PATTERNS = {
    "Arinj": r"arinj|առինջ|аринж", "Abovyan": r"\babovyan\b(?!\s+(st|street|district|փ))|աբովյան քաղաք", "Tsaghkadzor": r"tsa[gk]h?kadzor|ծաղկաձոր|цахкадзор",
    "Dilijan": r"dilijan|դիլիջան|дилижан", "Jrvezh": r"jrvezh|djrvezh|ջրվեժ|джрвеж", "Zovuni": r"zovuni|զովունի|зовуни",
    "Masis": r"\bmasis\b|մասիս|масис", "Vagharshapat": r"echmiadzin|etchmiadzin|vagharshapat|էջմիածին|вагаршапат",
}


def mentioned_place(text: str) -> tuple[str | None, str | None]:
    """(province, district/town) explicitly named in an address string, when unambiguous."""
    t = text or ""
    towns = [n for n, pat in TOWN_PATTERNS.items() if re.search(pat, t, re.I)]
    if len(towns) == 1:
        return None, towns[0]
    districts = [n for n, pat in DISTRICT_PATTERNS.items() if re.search(pat, t, re.I)]
    if len(districts) == 1 and not towns:
        return "Yerevan", districts[0]
    return None, None


def normalize_town(name: str | None) -> str | None:
    """Canonical town name from free-text source values; None for province names or Yerevan districts."""
    if not name:
        return None
    n = re.sub(r"\([^)]*\)", "", name).strip()
    parts = [x.strip() for x in n.split(",") if x.strip()]
    parts = [re.sub(r"\b(province|region|marz|community|city|town|village)\b|քաղաք|համայնք|մարզ|село|город", "", x, flags=re.I).strip() for x in parts]
    parts = [x for x in parts if x and x.lower() not in PROVINCES]
    if not parts:
        return None
    key = parts[-1].lower()
    if key in TOWN_ALIASES:
        return TOWN_ALIASES[key]
    if YEREVAN_DISTRICT_WORDS.search(key) and "arinj" not in key and "առինջ" not in key:
        return None
    return parts[-1][:1].upper() + parts[-1][1:]


def locate(lat: float, lng: float, fallback_town: str | None = None) -> tuple[str | None, str | None]:
    """
    Return (province, district_or_town) for a coordinate.

    In Yerevan the second value is one of the 12 administrative districts; elsewhere it is the
    OSM town polygon if the point falls in one, otherwise the normalized source town name.
    """
    province = _lookup("province", lng, lat)
    if province == "Yerevan":
        return province, _lookup("district", lng, lat) or "Yerevan"
    return province, _lookup("town", lng, lat) or normalize_town(fallback_town) or f"{province} (other)"
