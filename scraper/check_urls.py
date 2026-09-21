"""Check that every URL in the dataset still resolves to a real page.

Covers the source URLs a project was built from (`source_url` and `sources[].url`) and, with
--websites, the project and developer sites. Results are cached in scraper/url_check.json so a
re-run only re-tests what changed or what failed.

Usage:
    python3 scraper/check_urls.py [--websites] [--only HOST] [--recheck] [--workers N]

A host that answers 403/429 to a script is reported as "blocked", not dead: those need a browser.
"""
from __future__ import annotations

import argparse
import json
import random
import ssl
import threading
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "web" / "data" / "projects.json"
OUT = ROOT / "scraper" / "url_check.json"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/128.0.0.0 Safari/537.36")
HOST_DELAY = 1.0
TIMEOUT = 25

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


def check(url: str, ctx: ssl.SSLContext) -> dict:
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
            body = r.read(4096)
            return {"status": r.status, "final_url": r.url, "bytes": len(body),
                    "verdict": classify(r.status, None), "ms": round((time.monotonic() - started) * 1000),
                    "checked": time.strftime("%Y-%m-%d")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final_url": url, "verdict": classify(e.code, None), "error": e.reason and str(e.reason),
                "ms": round((time.monotonic() - started) * 1000), "checked": time.strftime("%Y-%m-%d")}
    except Exception as e:  # noqa: BLE001 — DNS, TLS, timeouts and resets all mean "cannot reach"
        return {"status": None, "final_url": url, "verdict": "unreachable", "error": f"{type(e).__name__}: {e}",
                "ms": round((time.monotonic() - started) * 1000), "checked": time.strftime("%Y-%m-%d")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--websites", action="store_true", help="also check project and developer websites")
    ap.add_argument("--only", help="limit to URLs on this host")
    ap.add_argument("--recheck", action="store_true", help="ignore the cache and test everything again")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    data = json.loads(PROJECTS.read_text())
    cited = urls_from(data, args.websites)
    cache = json.loads(OUT.read_text()) if OUT.exists() and not args.recheck else {}
    todo = [u for u in cited if (not args.only or args.only in urlsplit(u).netloc)
            and (u not in cache or cache[u].get("verdict") != "ok")]
    print(f"{len(cited)} URLs cited, {len(todo)} to check ({len(cited) - len(todo)} already verified)", flush=True)

    ctx = ssl.create_default_context()
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for url, res in zip(todo, pool.map(lambda u: check(u, ctx), todo)):
            cache[url] = {**res, "projects": len(cited[url])}
            done += 1
            if done % 25 == 0:
                print(f"  {done}/{len(todo)}", flush=True)
    OUT.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")

    tested = {u: cache[u] for u in cited if u in cache}
    counts = Counter(r["verdict"] for r in tested.values())
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
