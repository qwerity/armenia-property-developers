---
name: nb-discover-sources
description: Search for NEW sources of Armenian new-building projects — aggregators, bank/agency catalogs, developer websites, regional listings — evaluate them (data access, coverage, coordinates, prices), add the good ones as scrapers and to the registry, and merge their projects. Use for "find new sources", "are we missing projects", or when the user reports a missing project/developer.
argument-hint: "[region | source type | a missed project URL]"
---

# nb-discover-sources

Work from the `armenia-new-builds` folder. Read `LEARNINGS.md` and `scraper/sources.json` (known + dead-end sources) first so you don't re-evaluate them.

## 1. Find candidates
- If the user gave a missed project/developer URL, start there: why was it missed (which source type lacks it)?
- Search (WebSearch; if the quota is exhausted, use news/directory site searches) in English, Russian and Armenian: "новостройки Ереван застройщик", "նորակառույց կառուցապատող", "residential complex <town> Armenia", bank "partner developers" pages, developer associations, construction portals, regions (Gyumri, Vanadzor, Dilijan, Tsaghkadzor, Jermuk, Sevan, Kotayk suburbs).
- Compare every developer found with `scraper/developers_master.json`; new developers with a projects page are candidates too.

## 2. Evaluate each candidate (cheap first)
Check in this order and note it in the registry: public JSON/XHR API (without violating robots disallow), Next/Nuxt payloads, sitemap.xml, JSON-LD, map embeds, plain HTML. Record coverage (projects count, % with coordinates/prices/dates) and freshness. Use full browser headers; the Browser pane only in your own tab.

## 3. Add good sources
- Catalog-like sources: add a function to `scraper/catalog_projects.py` (or a new module following `extra_sources.py` style) that outputs the schema in `../nb-recrawl/project_schema.md`, and register it in `pipeline.py` `CRAWLERS` if it's a new script.
- New developers: append to `scraper/developers_master.json` (same fields) and scrape them into a new `scraper/developer_projects_<name>.json` via agents.
- Add the source to `scraper/sources.json` (`status: ok` or `candidate`, method notes).

## 4. Merge and check
`python3 scraper/pipeline.py build` → read the diff: new projects should be genuinely new; if they duplicate existing pins, add curated groups to `scraper/merge_overrides.json`. Run `python3 scraper/pipeline.py audit all`.

## 5. Self-improve and commit
Follow `../SELF_IMPROVEMENT.md`. Dead ends go into `sources.json` (`blocked`/`dead` with reason) so future runs skip them.
