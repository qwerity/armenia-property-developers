"""Official bulletin lookup on azdarar.am — the notices that make a bankruptcy official.

azdarar.am serves the Republic of Armenia's public notices, including "«X» ՍՊԸ-ն սնանկ ճանաչելու և
սնանկության գործով կառավարիչ նշանակելու մասին". It refuses connections from outside Armenia, so this
module is meant to be run **from an Armenian network** (or any host that can reach the site); the rest
of the pipeline treats its output as an optional, hand-collected evidence file.

Usage (on a machine that can reach azdarar.am):
    python3 scraper/azdarar.py check                     # can this host reach the site at all?
    python3 scraper/azdarar.py search "Կվադրա Քոնսթրաքշն"
    python3 scraper/azdarar.py verify                    # every flagged company in the graph
    python3 scraper/azdarar.py parse saved-page.html     # parse a page you saved by hand

`verify` writes scraper/azdarar_notices.json, which connections.py reads when building the graph:
a bankruptcy notice there confirms the company's status and is linked from its node.

Endpoints (the site runs two generations side by side):
    new      https://azdarar.am/hy/public-announcement/search-result/?query=…   (notices since 2025-03-01)
    archive  https://www.azdarar.am/search                                      (older notices)
             detail pages: /announcments/cat/<category>/<id>/ and /announcments/org/<org>/<id>/
"""
from __future__ import annotations

import html as htmllib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GRAPH = ROOT / "web" / "data" / "connections.json"
OUT = HERE / "azdarar_notices.json"
CACHE = HERE / ".cache_azdarar"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DELAY = 1.0
NEW_SEARCH = "https://azdarar.am/hy/public-announcement/search-result/?query="
OLD_SEARCH = "https://www.azdarar.am/search?searchtext="
DETAIL = re.compile(r"/announcments/(?:cat|org)/\d+/\d+/?")
# what the notice says happened
DECLARED = re.compile(r"սնանկ\s+ճանաչ", re.I)
BANKRUPTCY = re.compile(r"սնանկ|պարտապան", re.I)
SELF_FILED = re.compile(r"ինքնակամ|սեփական\s+դիմում", re.I)
_last = 0.0


def google_site_search(name: str) -> str:
    """Fallback link that works from anywhere: the same notices as indexed by Google."""
    query = 'site:azdarar.am "%s"' % name
    return "https://www.google.com/search?q=" + urllib.parse.quote(query)


def search_url(name: str, archive: bool = False) -> str:
    return (OLD_SEARCH if archive else NEW_SEARCH) + urllib.parse.quote(name)


def fetch(url: str, retries: int = 2) -> str:
    """GET with an on-disk cache. Returns "" when the host cannot be reached (that is the usual case
    outside Armenia, and callers are expected to report it rather than fail)."""
    global _last
    CACHE.mkdir(exist_ok=True)
    cf = CACHE / (re.sub(r"[^\w.-]+", "_", url.split("://", 1)[-1])[:150] + ".html")
    if cf.exists():
        return cf.read_text(encoding="utf-8")
    for attempt in range(retries):
        wait = DELAY - (time.monotonic() - _last)
        if wait > 0:
            time.sleep(wait)
        _last = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "hy,en;q=0.8"})
            with urllib.request.urlopen(req, timeout=45) as r:
                body = r.read().decode("utf-8", "replace")
            cf.write_text(body, encoding="utf-8")
            return body
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                print(f"azdarar: {url}: {e}", file=sys.stderr)
                return ""
            time.sleep(2)
    return ""


def _txt(s: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def parse(page: str, base: str = "https://www.azdarar.am") -> list[dict]:
    """Notices on a search-result page: every link to an announcement, with its title.

    Deliberately markup-agnostic — both generations of the site render results as links to
    /announcments/… or /hy/public-announcement/…, and only the wrapper markup differs.
    """
    out, seen = [], set()
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page, re.S):
        href, body = m.group(1), _txt(m.group(2))
        if not (DETAIL.search(href) or "/public-announcement/" in href and re.search(r"/\d+/?$", href)):
            continue
        url = urllib.parse.urljoin(base, href)
        if url in seen or len(body) < 12:
            continue
        seen.add(url)
        out.append({"title": body, "url": url})
    return out


def search(name: str) -> list[dict]:
    """Notices mentioning `name`, from the current platform and the archive."""
    found = []
    for archive in (False, True):
        url = search_url(name, archive)
        page = fetch(url)
        if not page:
            continue
        for n in parse(page, "https://www.azdarar.am" if archive else "https://azdarar.am"):
            n["found_via"] = url
            found.append(n)
    return found


def classify(notices: list[dict]) -> dict | None:
    """The strongest statement the notices make about a bankruptcy."""
    declared = [n for n in notices if DECLARED.search(n["title"])]
    related = [n for n in notices if BANKRUPTCY.search(n["title"])]
    if declared:
        return {"status": "declared", "notice": declared[0], "count": len(declared)}
    if related:
        status = "self_declared" if any(SELF_FILED.search(n["title"]) for n in related) else "case"
        return {"status": status, "notice": related[0], "count": len(related)}
    return None


def reachable() -> bool:
    return bool(fetch("https://azdarar.am/hy/"))


def verify() -> int:
    """Look up every company the graph flags, and store what the bulletin says."""
    if not GRAPH.exists():
        print("build the graph first: python3 scraper/connections.py build", file=sys.stderr)
        return 1
    if not reachable():
        print("azdarar.am is not reachable from this host — run this on a machine in Armenia "
              "(the rest of the pipeline works without it; the site is linked, not required).", file=sys.stderr)
        return 2
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    flagged = [n for n in graph["nodes"] if n.get("bankruptcy")]
    print(f"checking {len(flagged)} flagged companies on azdarar.am…", file=sys.stderr)
    out = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for n in flagged:
        notices = search(n["label"])
        verdict = classify(notices)
        out[n["tax_id"]] = {
            "name": n["label"], "checked": time.strftime("%Y-%m-%d"),
            "notices": notices[:10], "verdict": verdict,
        }
        print(f"  {n['label']}: {len(notices)} notice(s)"
              f"{' → ' + verdict['status'] if verdict else ''}", file=sys.stderr)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{OUT.name}: {len(out)} companies, "
          f"{sum(1 for v in out.values() if v.get('verdict'))} with a bankruptcy notice", file=sys.stderr)
    return 0


def main() -> int:
    cmd, *rest = sys.argv[1:] or ["--help"]
    if cmd == "check":
        ok = reachable()
        print("azdarar.am is reachable" if ok else "azdarar.am is NOT reachable from this host")
        return 0 if ok else 2
    if cmd == "search" and rest:
        print(json.dumps(search(" ".join(rest)), ensure_ascii=False, indent=1))
        return 0
    if cmd == "parse" and rest:
        print(json.dumps(parse(Path(rest[0]).read_text(encoding="utf-8")), ensure_ascii=False, indent=1))
        return 0
    if cmd == "verify":
        return verify()
    print(__doc__)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
