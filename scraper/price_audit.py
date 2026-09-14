"""Cross-check price-per-m² observations from every source and pick a consensus value.

Each project accumulates `price_obs` entries (one per source figure):
    {"source", "kind": "m2"|"implied", "usd": float|None, "amd": float|None, "raw": str|None}
`reconcile()` converts, validates, clusters them and writes:
    usd_m2_min / amd_m2_min (consensus), price_confidence, price_flags, price_obs (annotated)
"""
import re
import statistics

MIN_USD_M2, MAX_USD_M2 = 350, 9000          # plausible new-build range in Armenia (2026)
RATE_TOLERANCE = 0.25                         # AMD/USD pair must be within ±25 % of the reference rate
AGREE = 0.20                                  # observations within ±20 % of each other agree
# Reliability/freshness weights: live unit-level catalogs and developer sites > maintained aggregators > stale directories.
SOURCE_WEIGHT = {
    "myhome.am": 3, "redgroup.am": 3, "redinvest.am": 3, "karucapatoxic.am": 2, "citynest.am": 2,
    "novostroiki-yerevan.com": 1.5, "ar-go.am": 1.5, "acba.am": 1.5, "dignisi.am": 1, "yerevan.etagi.com": 1,
    "ac-box.com": 1, "geoln.com": 0.5, "construction.am": 0.5,
}
DEVELOPER_SITE_WEIGHT = 2.5
SOURCE_FAMILY = {"redinvest.am": "redgroup.am"}


def weight(source: str) -> float:
    return SOURCE_WEIGHT.get(source, DEVELOPER_SITE_WEIGHT)


def family(source: str) -> str:
    return SOURCE_FAMILY.get(source, source)


def _score(group: list[tuple[float, dict]]) -> float:
    best: dict[str, float] = {}
    for _, o in group:
        fam = family(o["source"])
        best[fam] = max(best.get(fam, 0), weight(o["source"]))
    return sum(best.values())


def _weighted_median(group: list[tuple[float, dict]]) -> float:
    rows = sorted((v, weight(o["source"])) for v, o in group)
    half, acc = sum(w for _, w in rows) / 2, 0.0
    for v, w in rows:
        acc += w
        if acc >= half:
            return v
    return rows[-1][0]


def _num(v) -> float | None:
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v) if v > 0 else None
    m = re.search(r"\d[\d\s,]*\.?\d*", str(v))
    try:
        f = float(m.group(0).replace(" ", "").replace(",", "")) if m else None
    except ValueError:
        return None
    return f if f and f > 0 else None


def observation(source: str, usd=None, amd=None, raw=None, kind="m2") -> dict | None:
    usd, amd = _num(usd), _num(amd)
    if usd is None and amd is None:
        return None
    return {"source": source, "kind": kind, "usd": usd, "amd": amd, "raw": raw}


def implied_observation(source: str, total, area, currency: str | None, raw=None) -> dict | None:
    """Per-m² price implied by an apartment's total price and its area."""
    total, area = _num(total), _num(area)
    if not total or not area or area < 15 or area > 1000:
        return None
    per_m2 = total / area
    cur = (currency or "").upper()
    if cur == "USD" or (not cur and per_m2 < 20000):
        return observation(source, usd=per_m2, raw=raw, kind="implied")
    return observation(source, amd=per_m2, raw=raw, kind="implied")


def _to_usd(o: dict, rate: float) -> tuple[float | list[float] | None, list[str]]:
    """Resolve one observation to USD/m² (or a list of candidates when ambiguous), noting inconsistencies."""
    flags = []
    usd, amd = o.get("usd"), o.get("amd")
    if amd is not None and amd < 20000:          # USD value stored in the AMD field
        usd, amd = usd or amd, None
        flags.append("amd field held a USD value")
    if usd is not None and usd > 20000:          # AMD value stored in the USD field
        usd, amd = None, amd or usd
        flags.append("usd field held an AMD value")
    from_amd = amd / rate if amd else None
    if usd and from_amd:
        ratio = amd / usd
        if abs(ratio / rate - 1) > RATE_TOLERANCE:
            flags.append(f"USD {usd:.0f} and AMD {amd:.0f} disagree (implied rate {ratio:.0f})")
            plausible = [v for v in (usd, from_amd) if MIN_USD_M2 <= v <= MAX_USD_M2]
            if len(plausible) == 1:
                return plausible[0], flags
            return (plausible or None), flags
        return usd, flags
    value = usd or from_amd
    if value is not None and not (MIN_USD_M2 <= value <= MAX_USD_M2):
        # common unit slips: thousands of AMD ("489" meaning 489,000 ֏) or per-apartment totals
        if amd is None and usd is not None and MIN_USD_M2 <= usd * 1000 / rate <= MAX_USD_M2 and usd < MIN_USD_M2:
            flags.append(f"{usd:.0f} looks like thousands of AMD")
            return usd * 1000 / rate, flags
        flags.append(f"{value:.0f} $/m² outside plausible range")
        return None, flags
    return value, flags


def _cluster(values: list[tuple[float, dict]]) -> list[tuple[float, dict]]:
    """Group of observations agreeing within AGREE that carries the most source weight."""
    best: list = []
    for v, _ in values:
        group = [(x, o) for x, o in values if abs(x / v - 1) <= AGREE]
        if _score(group) > _score(best):
            best = group
    return best


def reconcile(p: dict, rate: float, is_house: bool = False) -> None:
    obs = [o for o in p.get("price_obs") or [] if o]
    resolved, ambiguous = [], []
    for o in obs:
        usd, flags = _to_usd(o, rate)
        o["flags"] = flags
        if isinstance(usd, list):
            ambiguous.append((usd, o))
            continue
        o["usd_m2"] = round(usd) if usd else None
        if usd:
            resolved.append((usd, o))
    for candidates, o in ambiguous:
        # a self-contradictory USD/AMD pair: keep whichever figure the other sources support, else the AMD one
        anchor = statistics.median(v for v, _ in resolved) if resolved else None
        pick = min(candidates, key=lambda c: abs(c / anchor - 1)) if anchor else o["amd"] / rate
        if anchor and abs(pick / anchor - 1) > 0.35:
            o["usd_m2"] = None
            o["flags"].append("neither figure matches other sources — ignored")
            continue
        o["usd_m2"] = round(pick)
        o["flags"].append(f"resolved to ${pick:.0f}/m²" + (" (matches other sources)" if anchor else " (AMD figure)"))
        resolved.append((pick, o))
    p["price_obs"] = obs
    if not resolved:
        p["usd_m2_min"] = p["amd_m2_min"] = None
        p["usd_m2_max"] = p["amd_m2_max"] = None
        p["price_confidence"] = "none" if not obs else "rejected"
        p["price_flags"] = sorted({f for o in obs for f in o["flags"]})
        return
    stated = [(v, o) for v, o in resolved if o["kind"] == "m2"]
    cluster = _cluster(stated) if stated else _cluster(resolved)
    base = statistics.median(v for v, _ in cluster)
    # apartment-derived figures confirm the cluster when roughly in line (the cheapest unit is rarely on the cheapest floor)
    cluster += [(v, o) for v, o in resolved if o["kind"] == "implied" and 0.8 <= v / base <= 1.6]
    distinct_sources = {family(o["source"]) for _, o in cluster}
    stated_in_cluster = [(v, o) for v, o in cluster if o["kind"] == "m2"]
    consensus = _weighted_median(stated_in_cluster or cluster)
    outliers = [o for v, o in resolved if not any(o is c for _, c in cluster)]
    flags = sorted({f for o in obs for f in o["flags"]})
    for o in outliers:
        flags.append(f"{o['source']}: ${o['usd_m2']}/m² disagrees with consensus ${consensus:.0f}")
    support = _score(cluster)
    conflict = _score([(v, o) for v, o in resolved if any(o is x for x in outliers) and o["kind"] == "m2"])
    if len(distinct_sources) >= 2 and support >= 2 * conflict:
        confidence = "high"
    elif support > conflict:
        confidence = "medium"
    else:
        confidence = "low"
    old_min = p.get("usd_m2_min")
    for o in obs:
        o["used"] = any(o is c for _, c in cluster)
    p["usd_m2_min"] = round(consensus)
    source_amd = next((o["amd"] for v, o in cluster if round(v) == round(consensus) and o.get("amd") and o["amd"] >= 20000), None)
    p["amd_m2_min"] = round(source_amd) if source_amd else round(consensus * rate / 1000) * 1000
    if not p.get("usd_m2_max") or p["usd_m2_max"] < p["usd_m2_min"] or (old_min and abs(old_min / consensus - 1) > AGREE):
        p["usd_m2_max"], p["amd_m2_max"] = p["usd_m2_min"], p["amd_m2_min"]
    p["price_confidence"] = confidence
    p["price_flags"] = flags
