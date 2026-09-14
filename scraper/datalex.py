"""Court-case lookup on datalex.am (Armenian Judicial Information System) by organisation name.

Usage:
    from datalex import find_cases
    cases = find_cases(["Կապիտալ Բիլդ", "Capital Build"], tax_id="00144692")

CLI:
    python3 datalex.py "Կապիտալ Բիլդ" ["alt name" ...] [--tax 00144692]
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://datalex.am/json.php"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CACHE_DIR = Path(__file__).resolve().parent / ".cache_datalex"
MIN_INTERVAL = 1.5
CASE_TYPES = {  # tab -> (grid, caseTypeID)
    "civil": ("datalex_civ_case_info", 2),
    "bankruptcy": ("datalex_bankr_case_info", 3),
    "administrative": ("datalex_adm_case_info", 5),
    "criminal": ("datalex_crim_case_info", 1),
    "payment_order": ("datalex_paym_case_info", 6),
}
_last_call = 0.0
LEGAL_FORMS = r"ՍՊԸ|ՓԲԸ|ԲԲԸ|ԱՁ|ՀԿ|LLC|CJSC|OJSC|ООО|ЗАО|ОАО"


def _post(org: str, role: str, tab: str, page: int, rows: int = 100) -> dict:
    global _last_call
    grid, type_id = CASE_TYPES[tab]
    crit = {k: "" for k in ("claimant_first_name", "claimant_last_name", "claimant_organization_name", "respondant_first_name",
                             "respondant_last_name", "respondant_organization_name", "claim", "court", "datavor_id", "case_number")}
    crit[f"{role}_organization_name"] = org
    crit.update({"verdict": {"value": ["", ""], "type": ["2", "2"]}, "start_date": {"start": "", "end": ""},
                 "hearing_date": {"start": "", "end": ""}, "verdict_date": {"start": "", "end": ""}})
    arg = [crit, {"_search": False, "nd": int(time.time() * 1000), "rows": rows, "page": str(page), "sidx": "", "sord": "asc"}, grid, False]
    params = {"gridSearchDescription": grid, "filterParams": [], "caseType": tab, "caseTypeID": type_id, "sortByPrecedent": False,
              "showViewCaseIcon": True, "showCaseIcons": True, "parentModuleID": "Common/ModCaseGrid", "moduleID": "Common/ModGrid",
              "viewID": "common-mod-grid", "currIndex": 0, "identName": None, "hasError": False, "useScrollToErrorField": True}
    body = urllib.parse.urlencode({
        "appName": "AppCaseSearch", "appPage": "default", "moduleID": "Common/ModGrid", "class": "", "function": "getGridDataList",
        "name": "Common/ModGrid", "type": "modules", "dataType": "json", "arg": json.dumps(arg, ensure_ascii=False), "module_params": json.dumps(params),
    }).encode()
    key = re.sub(r"[^\w]+", "_", f"{tab}_{role}_{org}_{page}")[:150]
    CACHE_DIR.mkdir(exist_ok=True)
    cf = CACHE_DIR / f"{key}.json"
    if cf.exists():
        return json.loads(cf.read_text(encoding="utf-8"))
    wait = MIN_INTERVAL - (time.monotonic() - _last_call)
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest", "Referer": "https://datalex.am/?app=AppCaseSearch"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.load(r)
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))
    _last_call = time.monotonic()
    cf.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def case_url(case_id: str | int | None) -> str | None:
    """Direct link that opens a case's details dialog on datalex.am."""
    return f"https://datalex.am/?app=AppCaseSearch&case_id={case_id}" if case_id else None


def case_index() -> dict:
    """case_number -> {"case_id","tab"} from every cached datalex search response (no network)."""
    index = {}
    for f in CACHE_DIR.glob("*.json"):
        tab = f.name.split("_", 1)[0]
        tab = "payment_order" if tab == "payment" else tab
        try:
            rows = (json.loads(f.read_text(encoding="utf-8")).get("result") or {}).get("data") or []
        except ValueError:
            continue
        for row in rows:
            if row.get("case_number") and row.get("case_id"):
                index.setdefault(row["case_number"], {"case_id": row["case_id"], "tab": tab})
    return index


def normalize_org(name: str) -> str:
    """Upper-case organisation name without quotes, legal-form suffixes or punctuation (Armenian/Latin/Cyrillic)."""
    n = (name or "").replace("&lt;", "<").replace("&gt;", ">")
    n = re.sub(r"[«»\"“”„'<>()]", " ", n)
    n = re.sub(rf"\b({LEGAL_FORMS})\b|ՍՊԸ|ՓԲԸ|ԲԲԸ", " ", n, flags=re.I)
    n = re.sub(r"[^\w\s-]", " ", n)
    return re.sub(r"[\s-]+", " ", n).strip().upper()


def _party_matches(party: str, targets: set[str]) -> bool:
    p = normalize_org(party)
    return bool(p) and any(p == t or (len(t) >= 6 and re.search(rf"(^| ){re.escape(t)}( |$)", p)) for t in targets)


def find_cases(names: list[str], tax_id: str | None = None, tabs: list[str] | None = None, max_pages: int = 5) -> list[dict]:
    """
    All datalex cases where the organisation is a respondent or claimant.

    Datalex search is fuzzy (word match), so results are filtered to parties whose normalised name equals
    one of `names` — or whose claim text mentions `tax_id` (ՀՎՀՀ) when given.

    Returns list of {"case_number","tab","role","claimant","respondent","claim","judge","filed","case_id"}.
    """
    targets = {normalize_org(n) for n in names if normalize_org(n)}
    out, seen = [], set()
    for tab in tabs or list(CASE_TYPES):
        for name in names:
            for role in ("respondant", "claimant"):
                page, pages = 1, 1
                while page <= min(pages, max_pages):
                    try:
                        res = (_post(name, role, tab, page).get("result") or {})
                    except Exception as e:  # network / server error: record and continue
                        out.append({"error": f"{tab}/{role}/{name}: {e}"})
                        break
                    pages = int(res.get("totalPages") or 1)
                    for row in res.get("data") or []:
                        party = row.get(f"{role}_full_name") or row.get(f"{role}_name") or ""
                        claim = row.get("claim") or ""
                        if not (_party_matches(party, targets) or (tax_id and tax_id in claim)):
                            continue
                        key = (row.get("case_number"), tab)
                        if key in seen:
                            continue
                        seen.add(key)
                        out.append({
                            "case_number": row.get("case_number"), "tab": tab, "role": "respondent" if role == "respondant" else "claimant",
                            "claimant": (row.get("claimant_full_name") or row.get("claimant_name") or "").replace("&lt;", "<").replace("&gt;", ">"),
                            "respondent": (row.get("respondant_full_name") or row.get("respondant_name") or "").replace("&lt;", "<").replace("&gt;", ">"),
                            "claim": re.sub(r"\s+", " ", claim.replace("&lt;", "<").replace("&gt;", ">"))[:400],
                            "judge": row.get("judge_name"), "filed": (row.get("creation_datetime") or "")[:10], "case_id": row.get("case_id"),
                        })
                    page += 1
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    tax = None
    if "--tax" in args:
        i = args.index("--tax")
        tax = args[i + 1]
        args = args[:i] + args[i + 2:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cases = find_cases(args, tax_id=tax)
    print(json.dumps(cases, ensure_ascii=False, indent=1))
    print(f"{len([c for c in cases if 'error' not in c])} cases", file=sys.stderr)
