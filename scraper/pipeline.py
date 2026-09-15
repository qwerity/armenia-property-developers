"""
Armenia new-builds data pipeline CLI (used by the /nb-* project skills).

Usage:
    python3 scraper/pipeline.py status
    python3 scraper/pipeline.py crawl [--fresh] [--only karucapatoxic,extra,catalogs,enrich] [--extra-sources geoln,dignisi]
    python3 scraper/pipeline.py build            # rebuild web/data/projects.json + change report
    python3 scraper/pipeline.py audit [prices|locations|stages|reputation|all] [--batches N]
    python3 scraper/pipeline.py diff             # compare current projects.json with the last snapshot

Outputs:
    scraper/reports/diff-<timestamp>.md|json      what changed since the previous build
    scraper/reports/queue-<kind>-<i>.json          work queues for verification agents
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "web" / "data" / "projects.json"
SNAPSHOT = HERE / "reports" / "projects.prev.json"
REPORTS = HERE / "reports"
SOURCES = HERE / "sources.json"
CRAWLERS = {
    "karucapatoxic": (["karucapatoxic.py"], [".cache"]),
    "extra": (["extra_sources.py"], [".cache_extra"]),
    "catalogs": (["catalog_projects.py"], [".cache_catalogs"]),
    "enrich": (["enrich_websites.py"], [".cache_web"]),
}
PRICE_JUMP = 0.10
MOVE_M = 150


def run(cmd: list[str], env: dict | None = None) -> None:
    print("$", " ".join(cmd), file=sys.stderr, flush=True)
    subprocess.run(cmd, cwd=HERE, check=True, env={**os.environ, **(env or {})})


def load_projects(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["projects"] if path.exists() else []


def haversine_m(a: dict, b: dict) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lng"], b["lat"], b["lng"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742000 * math.asin(math.sqrt(h))


# ---------------------------------------------------------------- crawl
def cmd_crawl(args) -> None:
    """Re-run scrapers. --fresh moves caches aside (renamed, never deleted) so pages are fetched again."""
    only = [s.strip() for s in (args.only or ",".join(CRAWLERS)).split(",") if s.strip()]
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    for name in only:
        if name not in CRAWLERS:
            sys.exit(f"unknown crawler {name!r}; choose from {', '.join(CRAWLERS)}")
        scripts, caches = CRAWLERS[name]
        if args.fresh:
            for c in caches:
                if (HERE / c).exists():
                    (HERE / c).rename(HERE / f"{c}.bak-{stamp}")
        extra = args.extra_sources.split(",") if (name == "extra" and args.extra_sources) else []
        env = {"CATALOG_CACHE": str(HERE / ".cache_catalogs")} if name == "catalogs" else None
        for script in scripts:
            run([sys.executable, script, *extra], env)
    update_source_registry(only)


def update_source_registry(crawled: list[str]) -> None:
    if not SOURCES.exists():
        return
    reg = json.loads(SOURCES.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    for s in reg.get("sources", []):
        if s.get("crawler") in crawled:
            s["last_crawled"] = today
    SOURCES.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------- build + diff
def cmd_build(args) -> None:
    REPORTS.mkdir(exist_ok=True)
    if DATA.exists():
        shutil.copyfile(DATA, SNAPSHOT)
    run([sys.executable, "make_config.py"]) if (ROOT / ".env").exists() else None
    run([sys.executable, "build_dataset.py"])
    cmd_diff(args)


def _index(projects: list[dict]) -> dict:
    """Key projects by every source URL so renamed/merged records still match across builds."""
    idx = {}
    for p in projects:
        for s in p.get("sources") or []:
            if s.get("url"):
                idx.setdefault(s["url"], p)
    return idx


def diff(old: list[dict], new: list[dict]) -> dict:
    """Changes between two builds: added/removed projects, price, stage, location and grade changes."""
    old_idx, new_idx = _index(old), _index(new)
    matched, added, changes = set(), [], {"price": [], "stage": [], "moved": [], "grade": []}
    for p in new:
        prev = next((old_idx[s["url"]] for s in p.get("sources") or [] if s.get("url") in old_idx), None)
        if not prev:
            added.append(p["title"])
            continue
        matched.add(id(prev))
        a, b = prev.get("usd_m2_min"), p.get("usd_m2_min")
        if a and b and abs(b / a - 1) >= PRICE_JUMP:
            changes["price"].append({"title": p["title"], "from": a, "to": b, "pct": round((b / a - 1) * 100, 1)})
        elif bool(a) != bool(b):
            changes["price"].append({"title": p["title"], "from": a, "to": b, "pct": None})
        if prev.get("stage") != p.get("stage"):
            changes["stage"].append({"title": p["title"], "from": prev.get("stage"), "to": p.get("stage")})
        d = haversine_m(prev, p)
        if d >= MOVE_M:
            changes["moved"].append({"title": p["title"], "metres": round(d)})
        ga, gb = (prev.get("developer_rep") or {}).get("grade"), (p.get("developer_rep") or {}).get("grade")
        if ga != gb:
            changes["grade"].append({"developer": p.get("developer_group"), "from": ga, "to": gb})
    removed = [p["title"] for p in old if id(p) not in matched and not any(s.get("url") in new_idx for s in p.get("sources") or [])]
    changes["grade"] = list({(c["developer"], c["from"], c["to"]): c for c in changes["grade"]}.values())
    return {"old_count": len(old), "new_count": len(new), "added": added, "removed": removed, **changes}


def cmd_diff(args) -> None:
    old, new = load_projects(SNAPSHOT), load_projects(DATA)
    if not old:
        print("no previous snapshot; nothing to diff", file=sys.stderr)
        return
    d = diff(old, new)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    REPORTS.mkdir(exist_ok=True)
    (REPORTS / f"diff-{stamp}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    lines = [f"# Build diff {stamp}", "", f"Projects: {d['old_count']} → {d['new_count']}",
             f"Added: {len(d['added'])} · Removed: {len(d['removed'])} · Price changes: {len(d['price'])} · "
             f"Stage changes: {len(d['stage'])} · Moved pins: {len(d['moved'])} · Grade changes: {len(d['grade'])}", ""]
    for key in ("added", "removed"):
        if d[key]:
            lines += [f"## {key.title()}", *[f"- {t}" for t in d[key][:50]], ""]
    for key, fmt in (("price", lambda c: f"- {c['title']}: {c['from']} → {c['to']} ({c['pct']}%)"),
                     ("stage", lambda c: f"- {c['title']}: {c['from']} → {c['to']}"),
                     ("moved", lambda c: f"- {c['title']}: {c['metres']} m"),
                     ("grade", lambda c: f"- {c['developer']}: {c['from']} → {c['to']}")):
        if d[key]:
            lines += [f"## {key.title()}", *[fmt(c) for c in d[key][:80]], ""]
    (REPORTS / f"diff-{stamp}.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:4]))
    print(f"report: scraper/reports/diff-{stamp}.md")


# ---------------------------------------------------------------- audit queues
def _batches(items: list, n: int) -> list[list]:
    return [items[i::n] for i in range(n)] if items else []


def audit_prices(projects: list[dict]) -> list[dict]:
    out = []
    for p in projects:
        reasons = []
        flags = p.get("price_flags") or []
        if any("disagree" in f or "ignored" in f for f in flags):
            reasons.append("source conflict")
        if p.get("price_confidence") in ("low", "rejected"):
            reasons.append("low confidence")
        if p.get("discount_pct") is not None and abs(p["discount_pct"]) >= 35:
            reasons.append(f"{p['discount_pct']}% vs local median")
        if reasons and not p.get("price_verification"):
            out.append({"id": p["id"], "title": p["title"], "developer": p["developer_group"], "district": p.get("district"),
                        "current_usd_m2": p.get("usd_m2_min"), "current_amd_m2": p.get("amd_m2_min"), "usd_from": p.get("usd_from"),
                        "reasons": reasons, "observations": [{k: o.get(k) for k in ("source", "kind", "usd", "amd", "raw", "usd_m2")} for o in p.get("price_obs") or []],
                        "source_urls": [s["url"] for s in p["sources"] if s.get("url")]})
    return out


def audit_locations(projects: list[dict]) -> list[dict]:
    audit = {r["id"]: r for r in json.loads((HERE / "location_audit.json").read_text(encoding="utf-8"))} if (HERE / "location_audit.json").exists() else {}
    out = []
    for p in projects:
        if p.get("location_check"):
            continue  # already verified by hand
        a = audit.get(p["id"], {})
        why = []
        if (a.get("street_dist_m") or 0) >= 400:
            why.append(f"pin {a['street_dist_m']} m from {a.get('street_name')}")
        if p.get("geo_precision") in ("district", "city"):
            why.append(f"approximate ({p['geo_precision']})")
        if (p.get("geo_spread_m") or 0) > 300:
            why.append(f"sources disagree by {p['geo_spread_m']} m")
        if (p.get("location_note") or "").startswith("location uncertain"):
            why.append(p["location_note"])
        if why:
            out.append({"id": p["id"], "title": p["title"], "address": p.get("address"), "lat": p["lat"], "lng": p["lng"],
                        "district": p.get("district"), "region": p.get("region"), "geo_precision": p.get("geo_precision"),
                        "why": why, "sources": [s["url"] for s in p["sources"] if s.get("url")]})
    return out


def audit_stages(projects: list[dict]) -> list[dict]:
    today = date.today().isoformat()
    out = []
    for p in projects:
        overdue = p.get("stage") in ("in progress", "just started") and (p.get("completion") or "9999") < today
        if p.get("stage_check") and not overdue:
            continue
        if p.get("stage") == "unknown" or overdue:
            out.append({"id": p["id"], "title": p["title"], "developer": p["developer_group"], "address": p.get("address"),
                        "district": p.get("district"), "region": p.get("region"), "lat": p["lat"], "lng": p["lng"],
                        "status_raw": p.get("status"), "completion": p.get("completion"), "floors": p.get("floors"),
                        "reason": "past completion date but not finished" if overdue else "unknown stage",
                        "sources": [s["url"] for s in p["sources"] if s.get("url")]})
    return out


def audit_reputation(projects: list[dict]) -> list[dict]:
    groups = {}
    for p in projects:
        g = p.get("developer_group") or ""
        if g == "Unknown developer" or g.endswith("(developer n/a)"):
            continue
        groups.setdefault(g, []).append(p)
    out = []
    for name, members in groups.items():
        rep = members[0].get("developer_rep") or {}
        research = rep.get("research") or {}
        stale = rep.get("data") != "full" or research.get("confidence") == "low"
        if stale:
            out.append({"developer": name, "name_variants": sorted({m.get("developer") for m in members if m.get("developer")}),
                        "projects": len(members), "stages": dict(Counter(m.get("stage") for m in members)),
                        "website": next((m.get("developer_website") or m.get("website") for m in members if m.get("developer_website") or m.get("website")), None),
                        "sample_projects": [m["title"] for m in members][:6], "reason": "no research" if not research else "low-confidence research"})
    return out


AUDITS = {"prices": audit_prices, "locations": audit_locations, "stages": audit_stages, "reputation": audit_reputation}


def cmd_audit(args) -> None:
    projects = load_projects(DATA)
    kinds = list(AUDITS) if args.kind == "all" else [args.kind]
    REPORTS.mkdir(exist_ok=True)
    for kind in kinds:
        for old in REPORTS.glob(f"queue-{kind}-*.json"):
            old.rename(old.with_suffix(".json.done"))
        items = AUDITS[kind](projects)
        for i, batch in enumerate(_batches(items, max(1, min(args.batches, len(items) or 1))), 1):
            (REPORTS / f"queue-{kind}-{i}.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{kind}: {len(items)} items → scraper/reports/queue-{kind}-*.json")


# ---------------------------------------------------------------- status
def cmd_status(args) -> None:
    projects = load_projects(DATA)
    meta = json.loads(DATA.read_text(encoding="utf-8"))["meta"] if DATA.exists() else {}
    reps = {p["developer_group"]: p["developer_rep"] for p in projects if p.get("developer_rep")}
    print(json.dumps({
        "generated": meta.get("generated"), "projects": len(projects), "sources": len(meta.get("sources", [])),
        "stages": Counter(p.get("stage") for p in projects), "price_confidence": Counter(p.get("price_confidence") for p in projects),
        "geo_precision": Counter(p.get("geo_precision") for p in projects),
        "developer_grades": Counter(r["grade"] + ("" if r["data"] == "full" else "?") for r in reps.values()),
        "pending_queues": sorted(q.name for q in REPORTS.glob("queue-*.json")) if REPORTS.exists() else [],
        "last_diff": sorted(p.name for p in REPORTS.glob("diff-*.md"))[-1:] if REPORTS.exists() else [],
        "sources_registry": [{k: s.get(k) for k in ("name", "status", "last_crawled")} for s in json.loads(SOURCES.read_text(encoding="utf-8")).get("sources", [])] if SOURCES.exists() else [],
    }, ensure_ascii=False, indent=1, default=dict))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("crawl")
    c.add_argument("--fresh", action="store_true", help="refetch pages (caches are renamed, not deleted)")
    c.add_argument("--only", help="comma list: " + ",".join(CRAWLERS))
    c.add_argument("--extra-sources", help="limit extra_sources.py to these source keys")
    sub.add_parser("build")
    sub.add_parser("diff")
    a = sub.add_parser("audit")
    a.add_argument("kind", nargs="?", default="all", choices=[*AUDITS, "all"])
    a.add_argument("--batches", type=int, default=3)
    sub.add_parser("status")
    args = ap.parse_args()
    {"crawl": cmd_crawl, "build": cmd_build, "diff": cmd_diff, "audit": cmd_audit, "status": cmd_status}[args.cmd](args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
