"""Developer reputation score (0–100, grade A–E) from track record, delivery, court records, validation and transparency.

Inputs: projects of one developer group (from build_dataset) + optional research record
(scraper/developer_reputation_*.json: legal entities, datalex court summary, news issues, positives).
"""
import json
import math
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VALIDATING_SOURCES = {"myhome.am", "acba.am", "evoca.am", "redgroup.am", "redinvest.am", "byblosbankarmenia.am"}
GRADES = [(80, "A"), (65, "B"), (50, "C"), (35, "D"), (0, "E")]


def load_research() -> dict:
    """Research records keyed by developer display name."""
    out = {}
    for f in sorted(ROOT.glob("developer_reputation_*.json")):
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for r in rows if isinstance(rows, list) else []:
            if isinstance(r, dict) and r.get("developer"):
                out[r["developer"]] = r
    return out


def _overdue(p: dict, today: date) -> bool:
    try:
        return bool(p.get("completion")) and date.fromisoformat(p["completion"][:10]) < today and p.get("stage") in ("in progress", "just started")
    except ValueError:
        return False


def score_developer(projects: list[dict], research: dict | None, today: date | None = None) -> dict:
    """
    Compute a transparent reputation score.

    Components (max points): track record 30, delivery 20, legal 30, validation 10, transparency 10.
    Legal penalties are scaled by portfolio size (large developers naturally attract more suits).
    Returns {"score","grade","components":{...},"flags":[...],"data":"full|limited"}.
    """
    today = today or date.today()
    r = research or {}
    court = r.get("court") or {}
    flags = []
    n = len(projects)
    finished = sum(p.get("stage") == "finished" for p in projects)
    founded = r.get("founded_year") or min(
        (e.get("registered_year") for e in r.get("legal_entities") or [] if isinstance(e.get("registered_year"), int)), default=None)

    years = max(0, today.year - founded) if isinstance(founded, int) and 1990 <= founded <= today.year else None
    track = min(finished, 10) * 2 + (min(years, 20) / 2 if years is not None else min(n, 5))
    stalled = sum(p.get("stage") == "stalled" for p in projects)
    overdue = sum(_overdue(p, today) for p in projects)
    delivery = max(0.0, 20 - 10 * stalled - 4 * overdue)
    if stalled:
        flags.append(f"{stalled} stalled project(s)")
    if overdue:
        flags.append(f"{overdue} project(s) past completion date")

    size = math.sqrt(max(n, 1))
    legal = 30.0 if research else 15.0  # unknown legal record is neutral, not clean
    bankrupt = int(court.get("bankruptcy_as_debtor") or 0)
    criminal = int(court.get("criminal") or 0)
    buyer_suits = int(court.get("respondent_by_individuals") or 0)
    other_resp = max(0, int(court.get("respondent") or 0) - buyer_suits)
    issues = len(r.get("news_issues") or [])
    if bankrupt:
        legal -= 30
        flags.append(f"bankruptcy case(s) as debtor: {bankrupt}")
    if criminal:
        legal -= min(15, 7 * criminal)
        flags.append(f"criminal case(s): {criminal}")
    if buyer_suits:
        legal -= min(15, 3 * buyer_suits / size)
        flags.append(f"{buyer_suits} lawsuit(s) by individuals")
    legal -= min(8, 0.5 * other_resp / size)
    if issues:
        legal -= min(15, 5 * issues)
        flags.append(f"{issues} negative news item(s)")
    legal = max(0.0, legal)
    if not research:
        flags.append("court records not checked yet")

    validated = any(s.get("name") in VALIDATING_SOURCES for p in projects for s in p.get("sources") or [])
    verified_price = any(p.get("price_confidence") in ("verified", "high") for p in projects)
    validation = (6 if validated else 0) + (4 if verified_price else 0)
    transparency = sum(p.get("info_score") or 0 for p in projects) / max(n, 1) / 10

    total = round(track + delivery + legal + validation + transparency)
    has_research = bool(research) and research.get("confidence") in ("high", "medium")
    grade = next(g for threshold, g in GRADES if total >= threshold)
    return {
        "score": total, "grade": grade, "data": "full" if has_research else "limited",
        "components": {"track_record": round(track, 1), "delivery": round(delivery, 1), "legal": round(legal, 1),
                       "validation": validation, "transparency": round(transparency, 1)},
        "flags": flags,
    }


def public_research(r: dict | None) -> dict | None:
    """Subset of a research record shown in the UI."""
    if not r:
        return None
    court = r.get("court") or {}
    return {
        "role": r.get("role"), "confidence": r.get("confidence"), "founded_year": r.get("founded_year"),
        "legal_entities": [{k: e.get(k) for k in ("name_hy", "name_en", "tax_id", "form", "registered_year")} for e in r.get("legal_entities") or []][:4],
        "court": {k: court.get(k) for k in ("total", "respondent", "claimant", "respondent_by_individuals", "bankruptcy_as_debtor",
                                            "criminal", "administrative", "payment_order", "since_2021")},
        "notable_cases": (court.get("notable") or [])[:5],
        "news_issues": (r.get("news_issues") or [])[:5],
        "positives": (r.get("positives") or [])[:3],
        "notes": r.get("notes"),
    }
