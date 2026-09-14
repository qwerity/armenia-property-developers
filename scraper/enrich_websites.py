"""Enrich projects from their official websites (meta description, images, videos, contacts).

Reads web/data/karucapatoxic.json and scraper/extra_sources.json, visits each distinct
project/developer website once, and writes scraper/website_enrichment.json keyed by URL.
"""
import html as htmllib
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent
SOURCES = [ROOT.parent / "web" / "data" / "karucapatoxic.json", ROOT / "extra_sources.json", *sorted(ROOT.glob("developer_projects*.json"))]
OUT = ROOT / "website_enrichment.json"
CACHE = ROOT / ".cache_web"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/128 Safari/537.36"
SKIP_HOSTS = ("facebook.com", "instagram.com", "t.me", "google.com", "list.am", "dignisi.am", "hsbc.am", "karucapatoxic.am")
MAX_BYTES = 3_000_000


def fetch(url: str) -> tuple[str, str] | None:
    """Return (final_url, html) or None; cached on disk, never raises."""
    CACHE.mkdir(exist_ok=True)
    cf = CACHE / (re.sub(r"[^a-zA-Z0-9]+", "_", url)[:180] + ".json")
    if cf.exists():
        d = json.loads(cf.read_text(encoding="utf-8"))
        return (d["url"], d["html"]) if d.get("html") else None
    result = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8", "Accept-Language": "en,hy;q=0.8,ru;q=0.6"})
        with urllib.request.urlopen(req, timeout=20) as r:
            if "html" in (r.headers.get("Content-Type") or "html"):
                raw = r.read(MAX_BYTES)
                charset = r.headers.get_content_charset() or "utf-8"
                result = (r.geturl(), raw.decode(charset, errors="replace"))
    except Exception as e:
        print(f"  ! {url}: {e}", file=sys.stderr)
        return None
    cf.write_text(json.dumps({"url": result[0] if result else url, "html": result[1] if result else ""}), encoding="utf-8")
    return result


def meta(doc: str, *names: str) -> str | None:
    for n in names:
        for pat in (
            rf'<meta[^>]+(?:property|name)=["\']{re.escape(n)}["\'][^>]*content=["\']([^"\']+)',
            rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']{re.escape(n)}["\']',
        ):
            m = re.search(pat, doc, re.I)
            if m and m.group(1).strip():
                return htmllib.unescape(m.group(1).strip())
    return None


def visible_paragraphs(doc: str, limit: int = 700) -> str | None:
    body = re.sub(r"(?is)<(script|style|noscript|svg|nav|header|footer)[^>]*>.*?</\1>", " ", doc)
    paras = []
    for m in re.finditer(r"(?is)<p[^>]*>(.*?)</p>", body):
        t = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip()
        if len(t) >= 80 and not re.search(r"cookie|copyright|©|all rights reserved", t, re.I):
            paras.append(t)
        if sum(map(len, paras)) >= limit:
            break
    text = " ".join(paras)
    return (text[:limit].rsplit(" ", 1)[0] + "…") if len(text) > limit else (text or None)


def extract(url: str) -> dict | None:
    got = fetch(url)
    root = "{0.scheme}://{0.netloc}/".format(urlparse(url))
    if not got and url.rstrip("/") != root.rstrip("/"):
        got = fetch(root)
    if not got:
        return None
    final, doc = got
    links = set(htmllib.unescape(h) for h in re.findall(r'(?:href|src)=["\']([^"\']+)', doc, re.I))
    videos = set()
    for h in links | set(re.findall(r"https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)[\w-]{11}", doc)):
        m = re.search(r"(?:youtube(?:-nocookie)?\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([\w-]{11})", h)
        if m:
            videos.add(f"https://www.youtube.com/watch?v={m.group(1)}")
        elif re.search(r"vimeo\.com/(?:video/)?\d+", h):
            videos.add(h if h.startswith("http") else "https:" + h)
    social = {}
    for h in links:
        for key, pat in (("facebook", r"facebook\.com/(?!sharer|share|dialog|tr\b|plugins)[\w.\-/?=]+"),
                         ("instagram", r"instagram\.com/[\w.\-]+"), ("telegram", r"t\.me/[\w\-]+"),
                         ("youtube", r"youtube\.com/(?:@|channel/|c/|user/)[\w\-]+"), ("tiktok", r"tiktok\.com/@[\w.\-]+"),
                         ("linkedin", r"linkedin\.com/company/[\w\-]+")):
            if key not in social and re.search(pat, h, re.I) and h.startswith("http"):
                social[key] = h
    phones = sorted({re.sub(r"[^\d+]", "", h[4:]) for h in links if h.lower().startswith("tel:") and len(re.sub(r"\D", "", h)) >= 8})
    emails = sorted({h[7:].split("?")[0].strip().lower() for h in links if h.lower().startswith("mailto:") and "@" in h})
    og_img = meta(doc, "og:image", "twitter:image")
    title = meta(doc, "og:title") or (re.search(r"(?is)<title[^>]*>(.*?)</title>", doc) or [None, None])[1]
    return {
        "final_url": final,
        "title": htmllib.unescape(re.sub(r"\s+", " ", title)).strip() if title else None,
        "description": meta(doc, "og:description", "description", "twitter:description"),
        "text": visible_paragraphs(doc),
        "image": urljoin(final, og_img) if og_img else None,
        "videos": sorted(videos)[:6],
        "social": social,
        "phones": phones[:5],
        "emails": [e for e in emails if not e.endswith((".png", ".jpg"))][:3],
    }


def candidate_urls() -> list[str]:
    urls = set()
    for src in SOURCES:
        if not src.exists():
            continue
        for p in json.loads(src.read_text(encoding="utf-8")):
            for u in (p.get("website"), p.get("developer_website"), p.get("developer_url")):
                if isinstance(u, str) and u.startswith("http"):
                    host = urlparse(u).netloc.lower()
                    if host and not any(host.endswith(s) for s in SKIP_HOSTS):
                        urls.add(u.split("#")[0])
    return sorted(urls)


def main() -> int:
    urls = candidate_urls()
    print(f"{len(urls)} websites to enrich", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = dict(zip(urls, ex.map(extract, urls)))
    ok = {u: r for u, r in results.items() if r}
    OUT.write_text(json.dumps(ok, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"enriched {len(ok)}/{len(urls)} -> {OUT}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
