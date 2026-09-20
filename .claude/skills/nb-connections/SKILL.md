---
name: nb-connections
description: Rebuild the developer/constructor connections graph of the Armenia new-builds map — registry companies, their owners and directors (e-register.moj.am via karg.am), shared addresses, and bankruptcy status from datalex.am — and refresh the analytics graph with source links. Use for "who owns this developer", "connections between developers", "which developers are bankrupt", or after new developers are added.
argument-hint: "[crawl | build | <developer name>] [--deep]"
---

# nb-connections

Work from the `armenia-new-builds` folder. Read `LEARNINGS.md` first (name-matching traps, namesakes, mass-registration addresses).

## 1. Crawl
`python3 scraper/connections.py crawl --workers 4` resolves every developer's legal entities to registry
companies (tax id when the research has one, otherwise an exact-name search on karg.am), fetches the company
cards, follows every founder to their other companies, and searches datalex.am for bankruptcy cases.
Add `--deep` to fetch full cards for the owners' other companies too (slower, adds directors and activity).
Caches: `scraper/.cache_karg/`, `scraper/.cache_datalex/` — delete a file to refetch that page.

`python3 scraper/connections.py status` prints how many entities resolved by tax id, by name, or not at all.
Unresolved entities carry a `search_url`; resolving a few by hand into `scraper/connections_manual.json`
(`companies: {"<tax id>": {...}}`) is usually worth more than loosening the matcher.

## 2. Check before publishing
- Open the analytics page, pick 2–3 clusters, and follow the karg.am / e-register / datalex links on the nodes.
- A wrong company on a developer is worse than a missing one: drop it via `drop_companies` in
  `scraper/connections_manual.json` and note why.
- Shared-address edges between more than 8 companies are dropped as mass-registration noise; if a real
  office block still produces a hairball, raise the threshold in `connections.py` rather than hiding nodes.

## 3. Bankruptcy marks
Status is derived: `self_declared` (the company filed against itself), `declared` (a case against it and the
company is no longer active in the register), `case` (a case is pending). Upgrade or correct a status only
with a source — `{"<tax id>": {"status": "declared", "source_url": "…", "note": "…"}}` in
`scraper/connections_manual.json`. azdarar.am (the official bulletin) is the authority for
"սնանկ է ճանաչվել"; it blocks non-Armenian IPs, so it is linked for the reader, not crawled.

## 4. Rebuild and commit
`python3 scraper/connections.py build` writes `web/data/connections.json`; `python3 scraper/export_db.py`
refreshes the `connection_nodes` / `connection_edges` tables. Commit the raw crawl, the graph and the db.

## 5. Self-improve
Follow `../SELF_IMPROVEMENT.md`. Record namesake matches that fooled the resolver, registry quirks, and any
new field karg.am starts exposing.
