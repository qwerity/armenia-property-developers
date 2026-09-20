"""Export the built dataset into one portable SQLite database.

The web app reads web/data/projects.json; this script flattens the same data (plus the source
registry) into relational tables so it can be queried with SQL, and regenerates db/db.md's
row-count table.

Usage: python3 scraper/export_db.py [--out db/armenia-new-builds.sqlite]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
PROJECTS_JSON = ROOT / "web" / "data" / "projects.json"
SOURCES_JSON = ROOT / "scraper" / "sources.json"
DEFAULT_OUT = ROOT / "db" / "armenia-new-builds.sqlite"

SCHEMA = """
PRAGMA journal_mode = DELETE;

CREATE TABLE meta (
  key   TEXT PRIMARY KEY,
  value TEXT
);

CREATE TABLE projects (
  id                  TEXT PRIMARY KEY,
  title               TEXT NOT NULL,
  title_full          TEXT,
  title_am            TEXT,
  title_ru            TEXT,
  kind                TEXT,            -- Apartments | Houses / townhouses | Mixed use | Commercial
  status              TEXT,            -- completed | under construction | planned | unknown
  stage               TEXT,            -- finished | in progress | just started | not started | stalled | unknown
  stage_estimated     INTEGER,         -- 1 = inferred, not stated by the source
  progress_pct        INTEGER,
  sold_out            INTEGER,
  region              TEXT,
  district            TEXT,
  address             TEXT,
  address_am          TEXT,
  sales_address       TEXT,
  source_region       TEXT,            -- region as written by the source, before normalization
  source_district     TEXT,
  lat                 REAL,
  lng                 REAL,
  elevation_m         INTEGER,
  geo_precision       TEXT,            -- exact | address | street | district
  geo_spread_m        INTEGER,         -- distance spread between source coordinates
  location_note       TEXT,
  location_verdict    TEXT,            -- correct | moved | unlocatable (manual re-check)
  location_evidence   TEXT,
  location_evidence_url TEXT,
  location_notes      TEXT,
  developer           TEXT,            -- name as written by the source
  developer_group     TEXT,            -- normalized developer, used for grouping and colors
  developer_inferred  INTEGER,         -- 1 = guessed from the project name/site, not stated
  developer_grade     TEXT,            -- A..E, copy of developers.grade
  developer_score     INTEGER,
  developer_website   TEXT,
  developer_about     TEXT,
  completion          TEXT,            -- normalized completion date/quarter as published
  completion_text     TEXT,            -- raw text from the source
  completion_year     INTEGER,
  start               TEXT,
  floors              TEXT,
  min_area_m2         REAL,
  usd_m2_min          INTEGER,         -- current asking price per m², USD
  usd_m2_max          INTEGER,
  amd_m2_min          INTEGER,
  amd_m2_max          INTEGER,
  usd_from            INTEGER,         -- cheapest listed unit, USD
  amd_from            INTEGER,
  last_known_usd_m2   INTEGER,         -- last price seen before it disappeared from the source
  last_known_amd_m2   INTEGER,
  currency_raw        TEXT,
  price_updated       TEXT,
  income_tax_refund   INTEGER,
  price_confidence    TEXT,            -- verified | high | medium | low | none
  price_verdict       TEXT,            -- confirmed | corrected | unverifiable (manual re-check)
  price_evidence_url  TEXT,
  price_evidence_text TEXT,
  price_notes         TEXT,
  bench_usd_m2        INTEGER,         -- median price of comparable projects
  bench_scope         TEXT,            -- district | region
  bench_n             INTEGER,
  discount_pct        REAL,            -- positive = cheaper than the benchmark, negative = pricier
  stage_confidence    TEXT,
  stage_evidence      TEXT,
  stage_evidence_url  TEXT,
  stage_imagery       TEXT,
  stage_notes         TEXT,
  info_score          INTEGER,         -- 0-100 completeness of the record
  description         TEXT,
  description_site    TEXT,
  email               TEXT,
  website             TEXT,
  contacts_via_developer INTEGER,
  popularity          INTEGER,
  source              TEXT,            -- source the record was first built from
  source_url          TEXT
);
CREATE INDEX ix_projects_region ON projects(region, district);
CREATE INDEX ix_projects_dev ON projects(developer_group);
CREATE INDEX ix_projects_stage ON projects(stage);
CREATE INDEX ix_projects_price ON projects(usd_m2_min);

CREATE TABLE project_sources (
  project_id TEXT NOT NULL REFERENCES projects(id),
  name       TEXT NOT NULL,
  url        TEXT
);
CREATE INDEX ix_project_sources ON project_sources(project_id);

CREATE TABLE project_price_obs (
  project_id TEXT NOT NULL REFERENCES projects(id),
  source     TEXT,
  kind       TEXT,      -- m2 | unit
  usd        REAL,
  amd        REAL,
  usd_m2     INTEGER,
  raw        TEXT,      -- price string as published
  used       INTEGER,   -- 1 = fed the reconciled price on projects
  flags      TEXT       -- JSON array of parsing/consensus warnings
);
CREATE INDEX ix_price_obs ON project_price_obs(project_id);

CREATE TABLE project_geo_obs (
  project_id TEXT NOT NULL REFERENCES projects(id),
  source     TEXT,
  lat        REAL,
  lng        REAL,
  address    TEXT
);
CREATE INDEX ix_geo_obs ON project_geo_obs(project_id);

CREATE TABLE project_prices_by_rooms (
  project_id TEXT NOT NULL REFERENCES projects(id),
  current    INTEGER,   -- 1 = on sale now, 0 = last known before it went off-market
  rooms      TEXT,
  area_min   REAL,
  area_max   REAL,
  usd_from   INTEGER,
  amd_from   INTEGER,
  usd_to     INTEGER,
  amd_to     INTEGER
);
CREATE INDEX ix_by_rooms ON project_prices_by_rooms(project_id);

CREATE TABLE project_prices_by_floor (
  project_id TEXT NOT NULL REFERENCES projects(id),
  current    INTEGER,
  floors     TEXT,
  rooms      TEXT,
  usd_m2     INTEGER,
  amd_m2     INTEGER
);
CREATE INDEX ix_by_floor ON project_prices_by_floor(project_id);

CREATE TABLE project_media (
  project_id TEXT NOT NULL REFERENCES projects(id),
  kind       TEXT NOT NULL,  -- image | video
  seq        INTEGER,
  url        TEXT
);
CREATE INDEX ix_media ON project_media(project_id, kind);

CREATE TABLE project_contacts (
  project_id TEXT NOT NULL REFERENCES projects(id),
  kind       TEXT NOT NULL,  -- phone | facebook | instagram | telegram | linkedin | youtube | whatsapp | tiktok
  value      TEXT
);
CREATE INDEX ix_contacts ON project_contacts(project_id);

CREATE TABLE project_working_hours (
  project_id TEXT NOT NULL REFERENCES projects(id),
  days       TEXT,   -- JSON array, e.g. ["Mo","Tu"]
  start_time TEXT,
  end_time   TEXT
);

CREATE TABLE project_notes (
  project_id TEXT NOT NULL REFERENCES projects(id),
  kind       TEXT NOT NULL,  -- price_flag | info_missing | geo_support | geo_outlier | merged_id
  value      TEXT
);
CREATE INDEX ix_notes ON project_notes(project_id, kind);

CREATE TABLE developers (
  name                     TEXT PRIMARY KEY,
  projects                 INTEGER,
  score                    INTEGER,   -- 0-100
  grade                    TEXT,      -- A (best) .. E
  data                     TEXT,      -- full | limited: how much research backs the grade
  track_record             REAL,      -- score components, max 30/20/30/10/10
  delivery                 REAL,
  legal                    REAL,
  validation               REAL,
  transparency             REAL,
  role                     TEXT,      -- developer | contractor | agency ...
  confidence               TEXT,
  founded_year             INTEGER,
  court_total              INTEGER,   -- datalex.am case counts
  court_respondent         INTEGER,
  court_claimant           INTEGER,
  court_by_individuals     INTEGER,   -- respondent in cases filed by individuals (buyer disputes)
  court_bankruptcy         INTEGER,
  court_criminal           INTEGER,
  court_administrative     INTEGER,
  court_payment_order      INTEGER,
  court_since_2021         INTEGER,
  notes                    TEXT
);

CREATE TABLE developer_flags (
  developer TEXT NOT NULL REFERENCES developers(name),
  flag      TEXT
);
CREATE INDEX ix_dev_flags ON developer_flags(developer);

CREATE TABLE developer_entities (
  developer       TEXT NOT NULL REFERENCES developers(name),
  name_hy         TEXT,
  name_en         TEXT,
  tax_id          TEXT,
  form            TEXT,   -- LLC / CJSC / sole proprietor ...
  registered_year INTEGER,
  source_url      TEXT,
  registry_url    TEXT
);
CREATE INDEX ix_dev_entities ON developer_entities(developer);

CREATE TABLE developer_cases (
  developer   TEXT NOT NULL REFERENCES developers(name),
  case_number TEXT,
  tab         TEXT,   -- civil | bankruptcy | criminal | administrative | payment_order
  filed       TEXT,
  why         TEXT,
  url         TEXT    -- datalex.am deep link
);
CREATE INDEX ix_dev_cases ON developer_cases(developer);

CREATE TABLE developer_links (
  developer TEXT NOT NULL REFERENCES developers(name),
  kind      TEXT,   -- verify | news | positive | searched_name
  title     TEXT,
  url       TEXT,
  date      TEXT,
  summary   TEXT
);
CREATE INDEX ix_dev_links ON developer_links(developer, kind);

CREATE TABLE sources (
  name         TEXT PRIMARY KEY,
  kind         TEXT,   -- aggregator | developer | bank | agency ...
  crawler      TEXT,
  script       TEXT,
  method       TEXT,
  status       TEXT,   -- ok | degraded | blocked | dead | candidate
  last_crawled TEXT,
  notes        TEXT
);

CREATE VIEW v_projects AS
SELECT p.id, p.title, p.kind, p.stage, p.region, p.district, p.address, p.lat, p.lng,
       p.developer_group, p.developer_grade, p.completion_year,
       p.usd_m2_min, p.usd_from, p.price_confidence, p.discount_pct, p.sold_out, p.source_url
FROM projects p;

CREATE VIEW v_priced_apartments AS
SELECT * FROM projects
WHERE kind = 'Apartments' AND usd_m2_min IS NOT NULL;

CREATE VIEW v_district_prices AS
SELECT region, district,
       COUNT(*)            AS projects,
       MIN(usd_m2_min)     AS min_usd_m2,
       ROUND(AVG(usd_m2_min)) AS avg_usd_m2,
       MAX(usd_m2_min)     AS max_usd_m2
FROM v_priced_apartments
GROUP BY region, district
ORDER BY avg_usd_m2 DESC;

CREATE VIEW v_developer_stats AS
SELECT d.name, d.grade, d.score, d.projects,
       SUM(CASE WHEN p.stage IN ('in progress', 'just started') THEN 1 ELSE 0 END) AS building,
       SUM(CASE WHEN p.stage = 'finished' THEN 1 ELSE 0 END) AS finished,
       ROUND(AVG(p.usd_m2_min)) AS avg_usd_m2,
       d.court_by_individuals, d.court_bankruptcy
FROM developers d LEFT JOIN projects p ON p.developer_group = d.name
GROUP BY d.name
ORDER BY d.projects DESC;

CREATE VIRTUAL TABLE project_search USING fts5(
  id UNINDEXED, title, title_am, title_ru, developer, address, district, region, description
);
"""


# ---------------------------------------------------------------- helpers
def b(value: Any) -> int | None:
    """SQLite has no boolean type: store 1/0 and keep NULL when the field is absent."""
    return None if value is None else int(bool(value))


def js(value: Any) -> str | None:
    return None if value in (None, [], {}) else json.dumps(value, ensure_ascii=False)


def sub(record: dict, field: str, key: str) -> Any:
    return (record.get(field) or {}).get(key)


def insert(cur: sqlite3.Cursor, table: str, rows: list[dict]) -> None:
    if not rows:
        return
    cols = list(rows[0].keys())
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})"
    cur.executemany(sql, [tuple(r[c] for c in cols) for r in rows])


# ---------------------------------------------------------------- rows
def project_row(p: dict, rep: dict | None) -> dict:
    return {
        "id": p["id"], "title": p["title"], "title_full": p.get("title_full"), "title_am": p.get("title_am"),
        "title_ru": p.get("title_ru"), "kind": p.get("kind"), "status": p.get("status"), "stage": p.get("stage"),
        "stage_estimated": b(p.get("stage_estimated")), "progress_pct": p.get("progress_pct"),
        "sold_out": b(p.get("sold_out")), "region": p.get("region"), "district": p.get("district"),
        "address": p.get("address"), "address_am": p.get("address_am"), "sales_address": p.get("sales_address"),
        "source_region": p.get("source_region"), "source_district": p.get("source_district"),
        "lat": p.get("lat"), "lng": p.get("lng"), "elevation_m": p.get("elevation_m"),
        "geo_precision": p.get("geo_precision"), "geo_spread_m": p.get("geo_spread_m"),
        "location_note": p.get("location_note"),
        "location_verdict": sub(p, "location_check", "verdict"),
        "location_evidence": sub(p, "location_check", "evidence"),
        "location_evidence_url": sub(p, "location_check", "evidence_url"),
        "location_notes": sub(p, "location_check", "notes"),
        "developer": p.get("developer"), "developer_group": p.get("developer_group"),
        "developer_inferred": b(p.get("developer_inferred")),
        "developer_grade": (rep or {}).get("grade"), "developer_score": (rep or {}).get("score"),
        "developer_website": p.get("developer_website"), "developer_about": p.get("developer_about"),
        "completion": p.get("completion"), "completion_text": p.get("completion_text"),
        "completion_year": p.get("completion_year"), "start": p.get("start"), "floors": p.get("floors"),
        "min_area_m2": p.get("min_area_m2"),
        "usd_m2_min": p.get("usd_m2_min"), "usd_m2_max": p.get("usd_m2_max"),
        "amd_m2_min": p.get("amd_m2_min"), "amd_m2_max": p.get("amd_m2_max"),
        "usd_from": p.get("usd_from"), "amd_from": p.get("amd_from"),
        "last_known_usd_m2": p.get("last_known_usd_m2"), "last_known_amd_m2": p.get("last_known_amd_m2"),
        "currency_raw": p.get("currency_raw"), "price_updated": p.get("price_updated"),
        "income_tax_refund": b(p.get("income_tax_refund")), "price_confidence": p.get("price_confidence"),
        "price_verdict": sub(p, "price_verification", "verdict"),
        "price_evidence_url": sub(p, "price_verification", "evidence_url"),
        "price_evidence_text": sub(p, "price_verification", "evidence_text"),
        "price_notes": sub(p, "price_verification", "notes"),
        "bench_usd_m2": p.get("bench_usd_m2"), "bench_scope": p.get("bench_scope"), "bench_n": p.get("bench_n"),
        "discount_pct": p.get("discount_pct"),
        "stage_confidence": sub(p, "stage_check", "confidence"),
        "stage_evidence": sub(p, "stage_check", "evidence"),
        "stage_evidence_url": sub(p, "stage_check", "evidence_url"),
        "stage_imagery": sub(p, "stage_check", "imagery"), "stage_notes": sub(p, "stage_check", "notes"),
        "info_score": p.get("info_score"), "description": p.get("description"),
        "description_site": p.get("description_site"), "email": p.get("email"), "website": p.get("website"),
        "contacts_via_developer": b(p.get("contacts_via_developer")), "popularity": p.get("popularity"),
        "source": p.get("source"), "source_url": p.get("source_url"),
    }


def child_rows(p: dict) -> dict[str, list[dict]]:
    """Every one-to-many part of a project record, keyed by table name."""
    pid = p["id"]
    rooms = [{"project_id": pid, "current": current, "rooms": r.get("rooms"), "area_min": r.get("area_min"),
              "area_max": r.get("area_max"), "usd_from": r.get("usd_from"), "amd_from": r.get("amd_from"),
              "usd_to": r.get("usd_to"), "amd_to": r.get("amd_to")}
             for current, field in ((1, "prices_by_rooms"), (0, "last_known_prices_by_rooms"))
             for r in p.get(field) or []]
    floors = [{"project_id": pid, "current": current, "floors": r.get("floors"), "rooms": r.get("rooms"),
               "usd_m2": r.get("usd_m2"), "amd_m2": r.get("amd_m2")}
              for current, field in ((1, "prices_by_floor"), (0, "last_known_prices_by_floor"))
              for r in p.get(field) or []]
    media = ([{"project_id": pid, "kind": "image", "seq": i, "url": u} for i, u in enumerate(p.get("images") or [])]
             + [{"project_id": pid, "kind": "video", "seq": i, "url": u} for i, u in enumerate(p.get("videos") or [])])
    contacts = ([{"project_id": pid, "kind": "phone", "value": v} for v in p.get("phones") or []]
                + [{"project_id": pid, "kind": k, "value": v} for k, v in (p.get("social") or {}).items() if v])
    notes = [{"project_id": pid, "kind": kind, "value": v}
             for kind, field in (("price_flag", "price_flags"), ("info_missing", "info_missing"),
                                 ("geo_support", "geo_support"), ("geo_outlier", "geo_outliers"),
                                 ("merged_id", "merged_ids"))
             for v in p.get(field) or []]
    return {
        "project_sources": [{"project_id": pid, "name": s.get("name"), "url": s.get("url")} for s in p.get("sources") or []],
        "project_price_obs": [{"project_id": pid, "source": o.get("source"), "kind": o.get("kind"), "usd": o.get("usd"),
                               "amd": o.get("amd"), "usd_m2": o.get("usd_m2"), "raw": o.get("raw"),
                               "used": b(o.get("used")), "flags": js(o.get("flags"))} for o in p.get("price_obs") or []],
        "project_geo_obs": [{"project_id": pid, "source": o.get("source"), "lat": o.get("lat"), "lng": o.get("lng"),
                             "address": o.get("address")} for o in p.get("geo_obs") or []],
        "project_prices_by_rooms": rooms,
        "project_prices_by_floor": floors,
        "project_media": media,
        "project_contacts": contacts,
        "project_working_hours": [{"project_id": pid, "days": js(w.get("days")), "start_time": w.get("startTime"),
                                   "end_time": w.get("endTime")} for w in p.get("working_hours") or []],
        "project_notes": notes,
    }


def developer_rows(projects: list[dict]) -> tuple[list[dict], dict[str, list[dict]]]:
    """One row per normalized developer, with its reputation research spread over child tables."""
    reps: dict[str, dict] = {}
    counts: dict[str, int] = {}
    for p in projects:
        name = p.get("developer_group") or "Unknown developer"
        counts[name] = counts.get(name, 0) + 1
        if p.get("developer_rep") and name not in reps:
            reps[name] = p["developer_rep"]
    rows, flags, entities, cases, links = [], [], [], [], []
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        rep = reps.get(name) or {}
        comp = rep.get("components") or {}
        res = rep.get("research") or {}
        court = res.get("court") or {}
        rows.append({
            "name": name, "projects": n, "score": rep.get("score"), "grade": rep.get("grade"),
            "data": rep.get("data"), "track_record": comp.get("track_record"), "delivery": comp.get("delivery"),
            "legal": comp.get("legal"), "validation": comp.get("validation"), "transparency": comp.get("transparency"),
            "role": res.get("role"), "confidence": res.get("confidence"), "founded_year": res.get("founded_year"),
            "court_total": court.get("total"), "court_respondent": court.get("respondent"),
            "court_claimant": court.get("claimant"), "court_by_individuals": court.get("respondent_by_individuals"),
            "court_bankruptcy": court.get("bankruptcy_as_debtor"), "court_criminal": court.get("criminal"),
            "court_administrative": court.get("administrative"), "court_payment_order": court.get("payment_order"),
            "court_since_2021": court.get("since_2021"), "notes": res.get("notes"),
        })
        flags += [{"developer": name, "flag": f} for f in rep.get("flags") or []]
        entities += [{"developer": name, "name_hy": e.get("name_hy"), "name_en": e.get("name_en"),
                      "tax_id": e.get("tax_id"), "form": e.get("form"), "registered_year": e.get("registered_year"),
                      "source_url": e.get("source_url"), "registry_url": e.get("registry_url")}
                     for e in res.get("legal_entities") or []]
        cases += [{"developer": name, "case_number": c.get("case_number"), "tab": c.get("tab"),
                   "filed": c.get("filed"), "why": c.get("why"), "url": c.get("url")}
                  for c in res.get("notable_cases") or []]
        links += [{"developer": name, "kind": "verify", "title": l.get("title"), "url": l.get("url"),
                   "date": None, "summary": l.get("note")} for l in res.get("verify_links") or []]
        links += [{"developer": name, "kind": "news", "title": l.get("title"), "url": l.get("url"),
                   "date": l.get("date"), "summary": l.get("summary")} for l in res.get("news_issues") or []]
        links += [{"developer": name, "kind": "positive", "title": l.get("title"), "url": l.get("url"),
                   "date": None, "summary": l.get("summary")} for l in res.get("positives") or []]
        links += [{"developer": name, "kind": "searched_name", "title": s, "url": None, "date": None, "summary": None}
                  for s in res.get("searched_names") or []]
    return rows, {"developer_flags": flags, "developer_entities": entities,
                  "developer_cases": cases, "developer_links": links}


def source_rows() -> list[dict]:
    if not SOURCES_JSON.exists():
        return []
    data = json.loads(SOURCES_JSON.read_text())
    return [{"name": s.get("name"), "kind": s.get("kind"), "crawler": s.get("crawler"), "script": s.get("script"),
             "method": s.get("method"), "status": s.get("status"), "last_crawled": s.get("last_crawled"),
             "notes": s.get("notes")} for s in data.get("sources") or []]


def meta_rows(meta: dict, projects: list[dict]) -> list[dict]:
    rows = [{"key": k, "value": js(v) if isinstance(v, (list, dict)) else str(v)} for k, v in meta.items()]
    rows.append({"key": "project_count", "value": str(len(projects))})
    return rows


# ---------------------------------------------------------------- build
def build(out: Path) -> sqlite3.Connection:
    data = json.loads(PROJECTS_JSON.read_text())
    projects: list[dict] = data["projects"]
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()
    con = sqlite3.connect(out)
    cur = con.cursor()
    cur.executescript(SCHEMA)

    reps = {p["developer_group"]: p["developer_rep"] for p in projects if p.get("developer_rep")}
    insert(cur, "meta", meta_rows(data["meta"], projects))
    insert(cur, "projects", [project_row(p, reps.get(p.get("developer_group"))) for p in projects])
    children: dict[str, list[dict]] = {}
    for p in projects:
        for table, rows in child_rows(p).items():
            children.setdefault(table, []).extend(rows)
    for table, rows in children.items():
        insert(cur, table, rows)

    dev_rows, dev_children = developer_rows(projects)
    insert(cur, "developers", dev_rows)
    for table, rows in dev_children.items():
        insert(cur, table, rows)
    insert(cur, "sources", source_rows())

    cur.executemany(
        "INSERT INTO project_search (id, title, title_am, title_ru, developer, address, district, region, description)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [(p["id"], p.get("title"), p.get("title_am"), p.get("title_ru"), p.get("developer_group"),
          p.get("address"), p.get("district"), p.get("region"), p.get("description")) for p in projects],
    )
    con.commit()
    cur.execute("VACUUM")
    return con


def counts(con: sqlite3.Connection) -> list[tuple[str, int]]:
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        " AND name NOT LIKE 'project_search%' ORDER BY name")]
    return [(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]) for t in tables]


def update_docs(doc: Path, rows: Iterable[tuple[str, int]], generated: str) -> None:
    """Refresh the row-count block in db.md between the <!-- counts --> markers."""
    if not doc.exists():
        return
    table = ["| Table | Rows |", "| --- | ---: |"] + [f"| `{t}` | {n:,} |" for t, n in rows]
    body = f"<!-- counts -->\n_Data generated {generated}._\n\n" + "\n".join(table) + "\n<!-- /counts -->"
    text = doc.read_text()
    start, end = text.find("<!-- counts -->"), text.find("<!-- /counts -->")
    if start == -1 or end == -1:
        return
    doc.write_text(text[:start] + body + text[end + len("<!-- /counts -->"):])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    con = build(args.out)
    rows = counts(con)
    generated = con.execute("SELECT value FROM meta WHERE key = 'generated'").fetchone()[0]
    con.close()
    update_docs(args.out.parent / "db.md", rows, generated)
    print(f"{args.out} ({args.out.stat().st_size / 1e6:.1f} MB)")
    for table, n in rows:
        print(f"  {table:26} {n:>7,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
