"""Check that every URL in the dataset still resolves to a real page — and shows the right project.

Covers the source URLs a project was built from (`source_url` and `sources[].url`) and, with
--websites, the project and developer sites. Results are cached in scraper/url_check.json so a
re-run only re-tests what changed or what failed.

With --content the page body is also searched for evidence of the project it is cited for (title in
any of its three languages, street and house number, developer name). A page that answers 200 but
never mentions the project is the failure mode a status check cannot see: a site that renames its
slugs and serves its home page instead of a 404.

Usage:
    python3 scraper/check_urls.py [--content] [--websites] [--only HOST] [--recheck] [--workers N]

A host that answers 403/429 to a script is reported as "blocked", not dead: those need a browser.
"""
from __future__ import annotations

import argparse
import json
import random
import ssl
import threading
import time
import re
import urllib.error
import urllib.request
from html import unescape
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "web" / "data" / "projects.json"
CONNECTIONS = ROOT / "web" / "data" / "connections.json"
OUT = ROOT / "scraper" / "url_check.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")
HOST_DELAY = 1.0
TIMEOUT = 25
MAX_BODY = 1_500_000

_host_lock = defaultdict(threading.Lock)
_host_last: dict[str, float] = {}


def urls_from(data: dict, websites: bool) -> dict[str, list[str]]:
    """Every URL to test, mapped to the projects that cite it."""
    cited: dict[str, list[str]] = defaultdict(list)
    for p in data["projects"]:
        for url in [p.get("source_url"), *[s.get("url") for s in p.get("sources") or []]]:
            if url:
                cited[url].append(p["id"])
        if websites:
            for url in (p.get("website"), p.get("developer_website")):
                if url:
                    cited[url].append(p["id"])
    return cited


def evidence_urls() -> dict[str, list[str]]:
    """Every other link the pages show: reputation evidence, court cases, registry cards, notices.

    Search helpers (a Google query we build for the reader) are left out — there is nothing to
    verify in them, and Google answers a script with a challenge anyway.
    """
    cited: dict[str, list[str]] = defaultdict(list)
    def add(url, who):
        if isinstance(url, str) and url.startswith("http") and "google.com/search" not in url:
            cited[url].append(who)

    for p in json.loads(PROJECTS.read_text())["projects"]:
        for field in ("price_verification", "location_check", "stage_check"):
            add((p.get(field) or {}).get("evidence_url"), p["id"])
        r = (p.get("developer_rep") or {}).get("research") or {}
        for e in r.get("legal_entities") or []:
            add(e.get("source_url"), p["developer_group"])
            add(e.get("registry_url"), p["developer_group"])
        for group in ("notable_cases", "news_issues", "positives", "verify_links"):
            for item in r.get(group) or []:
                add(item.get("url"), p["developer_group"])

    if CONNECTIONS.exists():
        graph = json.loads(CONNECTIONS.read_text())
        for n in graph["nodes"]:
            for src in n.get("sources") or []:
                add(src.get("url"), n["label"])
            for c in n.get("cases") or []:
                add(c.get("url"), n["label"])
            bank = n.get("bankruptcy") or {}
            for src in bank.get("sources") or []:
                add(src.get("url"), n["label"])
            add((bank.get("notice") or {}).get("url"), n["label"])
            add(bank.get("confirmed_by"), n["label"])
            for c in bank.get("cases") or []:
                add(c.get("url"), n["label"])
        for e in graph["edges"]:
            add(e.get("evidence"), e.get("kind"))
        for src in (graph.get("meta") or {}).get("sources") or []:
            add(src.get("url"), "meta")
    return cited


def squash(text: str) -> str:
    """Lowercase and drop everything but letters and digits, so punctuation and spacing cannot differ."""
    return re.sub(r"[^0-9a-z\u0530-\u058f\u0400-\u04ff]+", "", (text or "").lower())


STOP = {"residential", "complex", "house", "housing", "building", "buildings", "project", "street",
        "district", "yerevan", "armenia", "quarter", "new", "the", "and", "llc", "ltd", "residence",
        "բնակելի", "համալիր", "շենք", "փողոց", "երևան", "жилой", "комплекс", "дом", "улица", "ереван"}


def tokens(text: str) -> list[str]:
    """Distinctive words of a name: the generic half of "X Residential Complex" says nothing."""
    words = re.findall(r"[0-9a-z\u0530-\u058f\u0400-\u04ff]+", (text or "").lower())
    return [w for w in words if len(w) >= 3 and w not in STOP]


def signals(p: dict) -> list[tuple[str, list[str]]]:
    """Groups of words, any of which the right page should carry, strongest first."""
    out = []
    for field in ("title", "title_full", "title_am", "title_ru"):
        t = tokens(p.get(field) or "")
        if t:
            out.append((field, t))
    address = p.get("address") or ""
    street = tokens(re.sub(r"\d+[/\-\d]*", " ", address.split(",")[0]))
    house = re.findall(r"\b(\d{1,3})(?:[/\-]\d+)?\b", address.split(",")[0])
    if street:
        out.append(("address", street + house[:1]))
    dev = tokens(p.get("developer") or "")
    if dev and p.get("developer") != "Unknown developer":
        out.append(("developer", dev))
    return out


def body_text(html: str) -> str:
    """Visible text plus embedded JSON — these sites ship their content in Next.js payloads."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    payload = " ".join(re.findall(r"<script[^>]*>(.*?)</script>", html, re.S | re.I))
    return unescape(text + " " + payload)


def content_verdict(html: str, projects: list[dict], url: str = "") -> dict:
    """How well the page matches the project(s) it is cited for.

    Sites rename a project between catalogues ("Nor Avan Complex" vs "Nor Avan Residential Complex"),
    so words are compared rather than whole strings: most of a name's distinctive words, or the street
    plus house number, is a match; a few words is weak; nothing at all is a mismatch.
    """
    text = body_text(html).lower() + " " + url.lower()
    if len(text) < 200:
        return {"content": "empty"}
    words = set(re.findall(r"[0-9a-z\u0530-\u058f\u0400-\u04ff]+", text))
    best = {"content": "mismatch", "checked_projects": [p["id"] for p in projects[:3]]}
    for p in projects:
        for field, group in signals(p):
            hits = sum(1 for w in group if w in words)
            if not hits:
                continue
            ratio = hits / len(group)
            if ratio >= 0.6 or (field == "address" and hits >= 2):
                return {"content": "match", "matched": p["id"], "matched_on": field,
                        "evidence": f"{hits}/{len(group)} words of {field}"}
            best = {"content": "weak", "matched": p["id"], "matched_on": field,
                    "evidence": f"{hits}/{len(group)} words of {field}"}
    return best


def polite(host: str) -> None:
    """One request per host per second, so a slow site is never hit in parallel."""
    with _host_lock[host]:
        wait = HOST_DELAY - (time.monotonic() - _host_last.get(host, 0))
        if wait > 0:
            time.sleep(wait + random.uniform(0, 0.2))
        _host_last[host] = time.monotonic()


def classify(status: int | None, error: str | None) -> str:
    if status is None:
        return "unreachable"
    if status in (403, 429):
        return "blocked"
    if status == 404 or status == 410:
        return "missing"
    if 200 <= status < 400:
        return "ok"
    return "error"


def encoded(url: str) -> str:
    """Percent-encode an IRI: Armenian paths are common here and urllib only speaks ASCII."""
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc.encode("idna").decode("ascii") if not parts.netloc.isascii() else parts.netloc,
                       quote(parts.path, safe="/%:@!$&'()*+,;=~"), quote(parts.query, safe="=&%:/?+,;@"), ""))


def check(url: str, ctx: ssl.SSLContext, projects: list[dict] | None = None) -> dict:
    """GET the page (HEAD is rejected or faked by too many of these sites) and read a little of it."""
    host = urlsplit(url).netloc
    polite(host)
    req = urllib.request.Request(encoded(url), headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en,hy;q=0.8,ru;q=0.6",
    })
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
            body = r.read(MAX_BODY if projects else 4096)
            res = {"status": r.status, "final_url": r.url, "bytes": len(body),
                   "verdict": classify(r.status, None), "ms": round((time.monotonic() - started) * 1000),
                   "checked": time.strftime("%Y-%m-%d")}
            if projects:
                res.update(content_verdict(body.decode("utf-8", "replace"), projects, url))
            return res
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final_url": url, "verdict": classify(e.code, None), "error": e.reason and str(e.reason),
                "ms": round((time.monotonic() - started) * 1000), "checked": time.strftime("%Y-%m-%d")}
    except Exception as e:  # noqa: BLE001 — DNS, TLS, timeouts and resets all mean "cannot reach"
        return {"status": None, "final_url": url, "verdict": "unreachable", "error": f"{type(e).__name__}: {e}",
                "ms": round((time.monotonic() - started) * 1000), "checked": time.strftime("%Y-%m-%d")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--content", action="store_true", help="also verify the page names the project it is cited for")
    ap.add_argument("--links", action="store_true", help="check the evidence links instead: court cases, registry cards, notices")
    ap.add_argument("--websites", action="store_true", help="also check project and developer websites")
    ap.add_argument("--only", help="limit to URLs on this host")
    ap.add_argument("--recheck", action="store_true", help="ignore the cache and test everything again")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    data = json.loads(PROJECTS.read_text())
    cited = evidence_urls() if args.links else urls_from(data, args.websites)
    cache = json.loads(OUT.read_text()) if OUT.exists() and not args.recheck else {}
    by_id = {p["id"]: p for p in data["projects"]}
    done_key = "content" if args.content else "verdict"
    todo = [u for u in cited if (not args.only or args.only in urlsplit(u).netloc)
            and (u not in cache or cache[u].get("verdict") != "ok" or (args.content and not cache[u].get("content")))]
    print(f"{len(cited)} URLs cited, {len(todo)} to check ({len(cited) - len(todo)} already verified)", flush=True)

    ctx = ssl.create_default_context()
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        run = lambda u: check(u, ctx, [by_id[i] for i in cited[u] if i in by_id] if args.content else None)  # noqa: E731
        for url, res in zip(todo, pool.map(run, todo)):
            cache[url] = {**res, "projects": len(cited[url])}
            done += 1
            if done % 25 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
    OUT.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")

    tested = {u: cache[u] for u in cited if u in cache}
    counts = Counter(r["verdict"] for r in tested.values())
    if args.content:
        print(f"content: {json.dumps(Counter(r.get('content', 'not checked') for r in tested.values()))}")
    print(f"\n{OUT.name}: {json.dumps(counts)}")
    by_host: dict[str, Counter] = defaultdict(Counter)
    for url, r in tested.items():
        by_host[urlsplit(url).netloc][r["verdict"]] += 1
    bad = {h: c for h, c in by_host.items() if c["ok"] == 0}
    for host, c in sorted(bad.items(), key=lambda kv: -sum(kv[1].values())):
        print(f"  {host:34} {dict(c)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
