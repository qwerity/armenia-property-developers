"""Developer reputation score (0–100, grade A–E) from track record, delivery, court records, validation and transparency.

Inputs: projects of one developer group (from build_dataset) + optional research record
(scraper/developer_reputation_*.json: legal entities, datalex court summary, news issues, positives).
"""
import json
import math
from urllib.parse import quote_plus

from karg import public_url

from datalex import case_index, case_url
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VALIDATING_SOURCES = {"myhome.am", "acba.am", "evoca.am", "redgroup.am", "redinvest.am", "byblosbankarmenia.am"}
GRADES = [(80, "A"), (65, "B"), (50, "C"), (35, "D"), (0, "E")]


CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1}


def research_key(name: str | None) -> str:
    """Loose key for matching developer names across batches (case, punctuation, legal forms, '(…)' notes)."""
    import re
    n = re.sub(r"\([^)]*\)", " ", (name or "").lower())
    n = re.sub(r"\b(llc|cjsc|ojsc|ltd|group|grup|construction|development|developer|company|residence|residential complex|ооо|ооо)\b", " ", n)
    return re.sub(r"[^a-z0-9ա-ֆа-я]+", "", n)


def load_research() -> dict:
    """Research records keyed by developer display name and by loose name key (best confidence wins)."""
    out = {}
    for f in sorted(ROOT.glob("developer_reputation_*.json")):
        try:
            rows = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            continue
        for r in rows if isinstance(rows, list) else []:
            if not (isinstance(r, dict) and r.get("developer")):
                continue
            for key in {r["developer"], research_key(r["developer"])}:
                if key and CONFIDENCE_RANK.get(r.get("confidence"), 0) >= CONFIDENCE_RANK.get((out.get(key) or {}).get("confidence"), -1):
                    out[key] = r
    return out


def find_research(research: dict, group: str, projects: list[dict]) -> dict | None:
    """Research for a developer group: exact name, then loose match on the group or any developer name variant."""
    if group in research:
        return research[group]
    names = [group, *{p.get("developer") for p in projects if p.get("developer")}, *{p.get("developer_am") for p in projects if p.get("developer_am")}]
    for n in names:
        k = research_key(n)
        if len(k) >= 4 and k in research:
            return research[k]
    return None


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


_CASES: dict | None = None


def _case_link(case_number: str | None, found_url: str | None = None) -> str | None:
    global _CASES
    if found_url:
        return found_url
    if _CASES is None:
        _CASES = case_index()
    hit = _CASES.get(case_number or "")
    return case_url(hit["case_id"]) if hit else None


_LINK_CHECKS: dict | None = None


def link_dead(url: str | None) -> str | None:
    """The verdict scraper/check_urls.py recorded for a link, when it is not "ok"."""
    global _LINK_CHECKS
    if _LINK_CHECKS is None:
        path = Path(__file__).resolve().parent / "url_check.json"
        _LINK_CHECKS = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    verdict = (_LINK_CHECKS.get(url or "") or {}).get("verdict")
    return verdict if verdict and verdict != "ok" else None


def register_url(query: str | None) -> str | None:
    """Official state register, which opens a company from a tax id in the URL.

    karg.am (the mirror the crawl read) now answers 403 to everyone, so it is no longer linked.
    """
    return f"https://e-register.moj.am/hy/search/companies?query={quote_plus(query)}" if query else None


def _verify_links(developer: str, entities: list[dict]) -> list[dict]:
    """Links a user can open to check the record themselves."""
    names = [e.get("name_hy") for e in entities if e.get("name_hy")] or [developer]
    plain = names[0].replace("«", "").replace("»", "")
    return [
        {"title": "Datalex court case search", "url": "https://datalex.am/?app=AppCaseSearch",
         "note": f"datalex has no URL for a party search: type «{plain}» into the claimant or respondent field. "
                 "The case links above open a case directly (the site asks for a captcha first)."},
        {"title": "News search (Google)", "url": f"https://www.google.com/search?q={quote_plus(f'\"{developer}\" կառուցապատող OR застройщик OR developer')}&tbm=nws"},
        {"title": "Buyer complaints search (Google)", "url": f"https://www.google.com/search?q={quote_plus(f'\"{plain}\" դատարան OR բողոք OR жалоба OR суд')}"},
    ]


def public_research(r: dict | None) -> dict | None:
    """Subset of a research record shown in the UI, with source links for every claim."""
    if not r:
        return None
    court = r.get("court") or {}
    entities = r.get("legal_entities") or []
    return {
        "role": r.get("role"), "confidence": r.get("confidence"), "founded_year": r.get("founded_year"),
        "legal_entities": [
            {**{k: e.get(k) for k in ("name_hy", "name_en", "tax_id", "form", "registered_year")},
             # where the record was read, unless that was karg.am, which now refuses every request
             "source_url": None if "karg.am" in (e.get("source_url") or "") else e.get("source_url"),
             "registry_url": register_url(e.get("tax_id"))}
            for e in entities
        ][:4],
        "searched_names": (r.get("searched_names") or [])[:6],
        "court": {k: court.get(k) for k in ("total", "respondent", "claimant", "respondent_by_individuals", "bankruptcy_as_debtor",
                                            "criminal", "administrative", "payment_order", "since_2021")},
        "notable_cases": [{**c, "url": _case_link(c.get("case_number"), c.get("url"))} for c in (court.get("notable") or [])[:5]],
        "verify_links": _verify_links(r.get("developer") or "", entities),
        "news_issues": [{**n, "url": public_url(n.get("url")), "dead": link_dead(public_url(n.get("url")))}
                        for n in (r.get("news_issues") or [])[:5] if public_url(n.get("url"))],
        "positives": [{**n, "url": public_url(n.get("url")), "dead": link_dead(public_url(n.get("url")))}
                      for n in (r.get("positives") or [])[:3] if public_url(n.get("url"))],
        "notes": r.get("notes"),
    }
