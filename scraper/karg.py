"""Company registry lookup on karg.am — the public mirror of e-register.moj.am (state register)
and of its beneficial-owner register (BOR).

What it gives per company: status (active/inactive), legal form, registration date, legal address,
NACE activity, director, founders with their shares, and the pages of those founders, which list
every other company the same person holds. Those shared people are what the connections graph is
built from.

Usage:
    from karg import search, company, founder
    hits = search("Կապիտալ Բիլդ")            # [{"tax_id","name","status","address","nace","url"}, …]
    c = company("00144692")                   # card: director, founders, address, status, …
    p = founder(c["founders"][0]["key"])      # that person's other companies

CLI:
    python3 karg.py search "Կապիտալ Բիլդ"
    python3 karg.py company 00144692
    python3 karg.py founder c8960556deb4
"""
from __future__ import annotations

import html as htmllib
import json
import re
import sys
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://karg.am"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
CACHE_DIR = Path(__file__).resolve().parent / ".cache_karg"
MIN_INTERVAL = 0.4  # polite delay between requests, shared by all threads
SOURCE_NOTE = "karg.am (mirror of e-register.moj.am / BOR)"
ROLES = {"Հիմնադիր": "founder", "Ղեկավար": "director", "Տնօրեն": "director", "Գլխավոր տնօրեն": "director"}
_lock = threading.Lock()
_last_call = 0.0


# ---------------------------------------------------------------- fetching
def company_url(tax_id: str) -> str:
    return f"{BASE}/company/{tax_id}?lang=hy"


def founder_url(key: str) -> str:
    return f"{BASE}/founder/{key}?lang=hy"


def search_url(query: str) -> str:
    return f"{BASE}/search?q={urllib.parse.quote(query)}"


def _fetch(url: str, retries: int = 3) -> str:
    """GET ``url`` as text, with an on-disk cache and a polite shared delay. "" when every try fails."""
    global _last_call
    CACHE_DIR.mkdir(exist_ok=True)
    cf = CACHE_DIR / (re.sub(r"[^\w.-]+", "_", url.split("://", 1)[-1])[:150] + ".html")
    if cf.exists():
        return cf.read_text(encoding="utf-8")
    for attempt in range(retries):
        with _lock:
            wait = MIN_INTERVAL - (time.monotonic() - _last_call)
            if wait > 0:
                time.sleep(wait)
            _last_call = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "hy,en;q=0.8"})
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8", "replace")
            cf.write_text(body, encoding="utf-8")
            return body
        except Exception as e:  # noqa: BLE001 — network errors are expected, keep going
            if attempt == retries - 1:
                print(f"karg: {url}: {e}", file=sys.stderr)
                return ""
            time.sleep(2 * (attempt + 1))
    return ""


# ---------------------------------------------------------------- parsing
def _txt(s: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def _h1(page: str) -> str | None:
    """Page heading without the trailing country/status badge."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    return _txt(re.sub(r"<span.*?</span>", " ", m.group(1), flags=re.S)) if m else None


def _facts(page: str) -> dict:
    """The <dl class="k-facts"> table as {label: value text}."""
    m = re.search(r'<dl class="k-facts">(.*?)</dl>', page, re.S)
    if not m:
        return {}
    pairs = re.findall(r"<dt>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", m.group(1), re.S)
    return {_txt(k): _txt(v) for k, v in pairs}


def _status(value: str) -> str | None:
    """Registry status normalised to "active" / "inactive" (Գործող / Չգործող)."""
    if not value:
        return None
    if "Չգործող" in value or "Ոչ գործող" in value:
        return "inactive"
    return "active" if "Գործող" in value else None


def _date(value: str) -> str | None:
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", value or "")
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else None


def search(query: str, limit: int = 10) -> list[dict]:
    """Company search by name. Returns [{"tax_id","name","status","address","nace","url"}, …]."""
    page = _fetch(search_url(query))
    out = []
    for block in re.findall(r'<a class="k-row" href="/company/(\d+)[^"]*">(.*?)</a>', page, re.S):
        tax_id, body = block
        name = _txt(re.search(r"<strong>(.*?)</strong>", body, re.S).group(1)) if "<strong>" in body else ""
        small = _txt(re.search(r"<small>(.*?)</small>", body, re.S).group(1)) if "<small>" in body else ""
        parts = [p.strip() for p in small.split("·")]
        out.append({
            "tax_id": tax_id, "name": name, "status": _status(small),
            "address": parts[2] if len(parts) > 2 else None, "nace": parts[3] if len(parts) > 3 else None,
            "url": company_url(tax_id),
        })
        if len(out) >= limit:
            break
    return out


def company(tax_id: str) -> dict | None:
    """One company card: registry facts, director and founders (with shares and founder page keys)."""
    page = _fetch(company_url(tax_id))
    if not page or "k-facts" not in page:
        return None
    f = _facts(page)
    name = _h1(page)
    founders = []
    fsec = re.search(r"<!-- Founders -->(.*?)</section>", page, re.S)
    if fsec:
        for card in re.findall(r'<div class="k-founder-card">(.*?)</div>\s*</div>', fsec.group(1), re.S):
            link = re.search(r'href="/founder/([0-9a-f]+)[^"]*"[^>]*>(.*?)</a>', card, re.S)
            share = re.search(r'k-fn-val">([\d.]+)', card)
            if link:
                founders.append({"key": link.group(1), "name": _txt(link.group(2)),
                                 "share": round(float(share.group(1)), 2) if share else None,
                                 "url": founder_url(link.group(1))})
    director = f.get("Տնօրեն") or f.get("Ղեկավար")
    links = re.search(r"<h2>Կապված Ընկերություններ</h2>(.*?)</section>", page, re.S)
    hints = {}
    if links:
        for label, key in (("Ընդհանուր հիմնադիր", "shared_founder"), ("Ընդհանուր հասցե", "shared_address"),
                           ("Ընդհանուր կայք", "shared_website"), ("Ընդհանուր ղեկավար", "shared_director")):
            m = re.search(rf"{label}: (\d+)", links.group(1))
            if m:
                hints[key] = int(m.group(1))
    cases = re.search(r"Դատական գործեր</div>\s*<div class=\"k-court-value\">(\d+)", page)
    return {
        "tax_id": tax_id, "name": name, "status": _status(f.get("Կարգավիճակ", "")),
        "status_text": f.get("Կարգավիճակ"), "form": f.get("Կազմակերպաիրավական ձև"),
        "registered": _date(f.get("Գրանցման ամսաթիվ", "")), "address": f.get("Իրավաբանական հասցե"),
        "nace": f.get("NACE ծածկագիր"), "director": director, "founders": founders,
        "taxes_amd": int(re.sub(r"\D", "", f.get("Վճարված հարկեր", "")) or 0) or None,
        "court_cases": int(cases.group(1)) if cases else None,
        "link_hints": hints, "url": company_url(tax_id), "source": SOURCE_NOTE,
    }


def founder(key: str) -> dict | None:
    """One person's page: every company they founded or run, plus the people they share companies with."""
    page = _fetch(founder_url(key))
    if not page or "/company/" not in page:
        return None
    name = _h1(page)
    companies = []
    for tax_id, body in re.findall(r'href="/company/(\d+)[^"]*"[^>]*>(.*?)</a>', page, re.S):
        smalls = re.findall(r"<small[^>]*>(.*?)</small>", body, re.S)
        cname = _txt(re.search(r"<strong>(.*?)</strong>", body, re.S).group(1)) if "<strong>" in body else _txt(body)
        role = re.search(r"(Հիմնադիր|Ղեկավար|Տնօրեն)(?:\s*\(([\d.]+)%\))?", _txt(body))
        address = _txt(smalls[1]).split("·")[0].strip() if len(smalls) > 1 else None
        if not cname:
            continue
        companies.append({
            "tax_id": tax_id, "name": cname, "status": _status(_txt(smalls[0]) if smalls else ""),
            "role": ROLES.get(role.group(1)) if role else None,
            "share": round(float(role.group(2)), 2) if role and role.group(2) else None,
            "address": address or None, "registered": _date(_txt(smalls[1])) if len(smalls) > 1 else None,
            "url": company_url(tax_id),
        })
    people = []
    rel = re.search(r"Կապակցված անձինք(.*?)(?:</section>|<footer)", page, re.S)
    if rel:
        for pkey, body in re.findall(r'href="/founder/([0-9a-f]+)[^"]*"[^>]*>(.*?)</a>', rel.group(1), re.S):
            pname = re.search(r"<strong>(.*?)</strong>", body, re.S)
            role = _txt(re.search(r"<small>(.*?)</small>", body, re.S).group(1)) if "<small>" in body else None
            people.append({"key": pkey, "name": _txt(pname.group(1)) if pname else _txt(body),
                           "role": ROLES.get(role), "url": founder_url(pkey)})
    return {"key": key, "name": name, "companies": companies, "related_people": people,
            "url": founder_url(key), "source": SOURCE_NOTE}


if __name__ == "__main__":
    cmd, *rest = sys.argv[1:] or ["--help"]
    if cmd == "search" and rest:
        print(json.dumps(search(" ".join(rest)), ensure_ascii=False, indent=1))
    elif cmd == "company" and rest:
        print(json.dumps(company(rest[0]), ensure_ascii=False, indent=1))
    elif cmd == "founder" and rest:
        print(json.dumps(founder(rest[0]), ensure_ascii=False, indent=1))
    else:
        print(__doc__)
        sys.exit(1)
