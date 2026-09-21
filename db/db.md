# armenia-new-builds.sqlite

One SQLite file with every project, developer and source behind the map and the analytics page.
Nothing else is needed to query it: `sqlite3 db/armenia-new-builds.sqlite`, or open it in DB Browser
for SQLite, DBeaver, TablePlus, DuckDB, pandas, etc.

The file is generated from `web/data/projects.json` (the dataset the web app loads) plus
`scraper/sources.json` (the source registry). Rebuild it after any dataset change:

```bash
python3 scraper/export_db.py
```

<!-- counts -->
_Data generated 2026-09-21._

| Table | Rows |
| --- | ---: |
| `connection_edges` | 1,318 |
| `connection_nodes` | 1,287 |
| `developer_cases` | 495 |
| `developer_entities` | 440 |
| `developer_flags` | 182 |
| `developer_links` | 2,179 |
| `developers` | 366 |
| `meta` | 13 |
| `project_contacts` | 2,663 |
| `project_geo_obs` | 998 |
| `project_media` | 6,869 |
| `project_notes` | 1,598 |
| `project_price_obs` | 1,323 |
| `project_prices_by_floor` | 19 |
| `project_prices_by_rooms` | 515 |
| `project_sources` | 1,319 |
| `project_working_hours` | 177 |
| `projects` | 735 |
| `sources` | 140 |
<!-- /counts -->

## Conventions

- **Money.** `usd_*` columns are US dollars, `amd_*` are Armenian drams, converted with the rate in
  `meta.amd_per_usd` on the build date. `*_m2_min` / `*_m2_max` are per square metre; `usd_from` /
  `amd_from` is the cheapest listed unit (whole apartment).
- **Booleans** are `1` / `0`, and `NULL` when the source never said.
- **Prices are asking prices** published by developers and aggregators, not registered sale prices.
- **`last_known_*`** holds the last price seen before the project stopped publishing one. Those
  projects have `price_confidence = 'none'` and `usd_m2_min IS NULL`, so they never distort averages.
- **Geography** is normalized: `region` / `district` come from a point-in-polygon test against
  official boundaries, while `source_region` / `source_district` keep what the source claimed.
- **Coordinates** are WGS84. `geo_precision` says how exact the pin is: `exact` (a marker from the
  source), `address`, `street`, `district`.
- **Text** is English where available; `title_am` / `title_ru` / `address_am` keep the originals.

## Tables

### `meta`
Key/value build info: `generated` (dataset date), `amd_per_usd`, `count`, crawl statistics and the
list of source domains. All values are strings; lists are JSON.

### `projects`
One row per project, 735 of them. Beyond the obvious name/place/price columns:

| Column | Meaning |
| --- | --- |
| `kind` | `Apartments`, `Houses / townhouses`, `Mixed use`, `Commercial` |
| `status` | `completed`, `under construction`, `planned`, `unknown` |
| `stage` | `finished`, `in progress`, `just started`, `not started`, `stalled`, `unknown` |
| `stage_estimated` | 1 when the stage was inferred (from completion date or imagery), not stated |
| `sold_out` | 1 when the source says no units are left |
| `price_confidence` | `verified` (re-checked on the source), `high`, `medium`, `low`, `none` |
| `price_verdict` | result of the manual re-check: `confirmed`, `corrected`, `unverifiable` |
| `price_evidence_url`, `price_evidence_text`, `price_notes` | what that verdict was based on |
| `location_verdict` | `correct`, `moved` (pin was corrected), `unlocatable` |
| `bench_usd_m2`, `bench_scope`, `bench_n` | median $/m² of *other* apartment projects in the same district (or region) |
| `discount_pct` | how far below that benchmark this project is: **positive = cheaper**, negative = pricier |
| `info_score` | 0–100 completeness of the record (price, contacts, images, dates…) |
| `developer` vs `developer_group` | name as published vs normalized name used for grouping |
| `developer_inferred` | 1 when the developer was guessed from the project site, not stated |
| `developer_grade`, `developer_score` | copied from `developers` for easy filtering |
| `elevation_m` | ground elevation, used by the 3D map camera |
| `source`, `source_url` | where the record was first built from; all sources are in `project_sources` |

### Project child tables
All keyed by `project_id`.

- **`project_sources`** — every site this project was found on (`name`, `url`). Projects are merged
  across sources, so one project often has several. `dead` and `checked` record a link that no longer
  answered when `scraper/check_urls.py` last ran (`missing` = 404, `unreachable` = DNS/TLS/timeout,
  `blocked` = the host refuses scripts); such links are kept as provenance, not deleted.
- **`project_price_obs`** — every price seen, per source: `kind` (`m2` or `unit`), `usd`, `amd`,
  `usd_m2`, the raw string, `used` (1 = it fed the reconciled price), and `flags` (JSON) for
  parsing or disagreement warnings. This is the audit trail behind `projects.usd_m2_min`.
- **`project_geo_obs`** — every coordinate seen, per source. The final pin is a reconciliation of these.
- **`project_prices_by_rooms`** — price/area ranges per room count. `current = 1` for live prices,
  `0` for `last_known` ones.
- **`project_prices_by_floor`** — per-floor $/m² where the source publishes it, same `current` flag.
- **`project_media`** — `kind` is `image` or `video`, in source order (`seq`).
- **`project_contacts`** — `kind` is `phone` or a social network (`facebook`, `instagram`,
  `telegram`, `linkedin`, `youtube`, `whatsapp`, `tiktok`).
- **`project_working_hours`** — sales office hours; `days` is a JSON array like `["Mo","Tu"]`.
- **`project_notes`** — small lists kept out of the main table: `price_flag` (a source disagreeing
  with the consensus), `info_missing` (fields the record lacks), `geo_support` / `geo_outlier`
  (sources that agreed or disagreed on the location), `merged_id` (ids of duplicates folded in).

### `developers`
One row per normalized developer (`developer_group` in `projects`), with the A–E reputation rating.

- `score` 0–100 and `grade` A (best) to E, from `track_record` (max 30), `delivery` (20),
  `legal` (30), `validation` (10), `transparency` (10).
- `data` is `full` or `limited` — how much research backs the grade. `NULL` grade means the
  developer was never researched (mostly one-project developers).
- `court_*` are case counts from datalex.am: `court_by_individuals` is the one to watch, since those
  are usually buyers suing the developer; `court_bankruptcy` counts cases where it is the debtor.
- Entries with no company found keep `NULL` counts — absence of cases is not the same as "clean".

Child tables, which together are the evidence behind every grade:

- **`developer_flags`** — the short warnings shown in the UI (182 rows).
- **`developer_entities`** — legal entities with tax id, `source_url` and `registry_url`
  (440 rows, 206 with a registry link), so a company can be looked up at e-register.am / karg.am.
- **`developer_cases`** — 495 notable court cases, each with `case_number`, `tab`
  (`civil`, `bankruptcy`, `criminal`, `administrative`, `payment_order`), `filed`, `why` it matters
  and a datalex.am deep link (`https://datalex.am/?app=AppCaseSearch&case_id=…`) that opens the case.
- **`developer_links`** — `verify` (1,017 rows; 339 are the datalex.am searches used, the rest are
  registry, tax and company pages), `news` (104 negative items with date and summary),
  `positive` (279 awards and completed projects), `searched_name` (779 name variants searched,
  which is what the case counts in `developers.court_*` were collected under).

### `connection_nodes` / `connection_edges`
The ownership graph behind the connections card on the analytics page, built by
`scraper/connections.py` from the state register of legal entities and its beneficial-owner data
(e-register.moj.am, read through karg.am) plus bankruptcy cases from datalex.am.

- **`connection_nodes`** — one row per developer (`dev:<slug>`), registered company (`co:<tax id>`)
  and owner/director (`pe:<owner key>`). Companies carry the register's `status`
  (`active` / `inactive`), `form`, `registered` date, legal `address`, `nace` activity and
  `director`; `url` is the registry card and `sources` the full link list (registry, e-register
  search, azdarar.am bulletin search).
- `bankruptcy` is `declared` (a bankruptcy case against the company **and** the register no longer
  shows it as active), `self_declared` (the company is the claimant against itself — it filed for its
  own bankruptcy) or `case` (a case is pending); `bankruptcy_cases` holds the datalex deep links.
  Corrections with a source live in `scraper/connections_manual.json`.
- `component` groups nodes into a connected cluster and `component_developers` counts the developers
  in it — `component_developers > 1` means those developers are linked to each other.
- **`connection_edges`** — `entity` (developer → its registered company, `evidence` links the source
  that ties them), `founder` / `director` (person → company, `label` carries the share),
  `address` (two companies registered at the same legal address), and the family layer:
  `family` (a documented tie from `scraper/family_ties.json`, `evidence` links the document),
  `family_lead` (two owners in one cluster sharing a surname) and `same_person` (one name appearing
  twice in the owner register). The last two are **leads to check, not facts** — no Armenian public
  register records kinship — and the site hides them unless the reader asks for them.
- **`v_bankruptcies`** — one row per flagged company with its developers and case links.

### `sources`
Every site the data came from: the 23 crawlers described in `scraper/sources.json`
(`in_registry = 1`, with `kind`, `crawler`/`script`, `method` = how the data is extracted, `status`
of `ok`/`degraded`/`blocked`/`dead`/`candidate`, and `last_crawled`) plus the 117 developer
websites that projects cite but that have no registry entry (`in_registry = 0`). `projects` counts
how many projects each one contributed. Per-project links are in `project_sources`, and the exact
figures each source published are in `project_price_obs` / `project_geo_obs`.

### Views and search
- **`v_projects`** — the columns most queries need.
- **`v_priced_apartments`** — apartment projects with a current price; use this for any price average.
- **`v_district_prices`** — count and min/avg/max $/m² per district.
- **`v_developer_stats`** — per developer: projects, building vs finished, average $/m², court counts.
- **`v_sources`** — per source: projects contributed, price and coordinate observations, status.
- **`project_search`** — FTS5 index over title, developer, address and description.

## Example queries

Cheapest districts by average asking price:

```sql
SELECT region, district, projects, avg_usd_m2 FROM v_district_prices WHERE projects >= 5 ORDER BY avg_usd_m2;
```

Apartments under construction, priced below their district, by a developer graded A or B:

```sql
SELECT title, district, usd_m2_min, discount_pct, developer_group, developer_grade
FROM v_priced_apartments
WHERE stage IN ('in progress', 'just started') AND discount_pct > 10
  AND developer_grade IN ('A', 'B') AND sold_out IS NOT 1
ORDER BY discount_pct DESC;
```

Where a project's price came from:

```sql
SELECT source, raw, usd_m2, used FROM project_price_obs WHERE project_id = '4acapitalam-408';
```

Which sources the data came from, and how much each contributed:

```sql
SELECT name, kind, projects, price_observations, status FROM v_sources WHERE projects > 0;
```

Every source that published a price for one project, with the raw figures:

```sql
SELECT ps.name, ps.url, o.raw, o.usd_m2, o.used
FROM project_sources ps LEFT JOIN project_price_obs o ON o.project_id = ps.project_id AND o.source = ps.name
WHERE ps.project_id = '4acapitalam-408';
```

Court cases behind a developer's rating, with datalex.am links to open each one:

```sql
SELECT case_number, tab, filed, why, url FROM developer_cases WHERE developer = 'ML Mining' ORDER BY filed DESC;
```

Developers sued most often by individuals:

```sql
SELECT name, projects, grade, court_by_individuals, court_bankruptcy
FROM developers WHERE court_by_individuals > 0 ORDER BY court_by_individuals DESC LIMIT 20;
```

Full-text search:

```sql
SELECT p.title, p.district, p.usd_m2_min FROM project_search s
JOIN projects p ON p.id = s.id WHERE project_search MATCH 'residence AND arabkir';
```

## Caveats

- A snapshot, not a feed: everything is as of `meta.generated`. Re-run the crawl (`/nb-recrawl`) and
  this exporter to refresh.
- Prices are per-project starting prices, not per-unit listings, and exclude parking and finishing.
- 353 projects have no current public price, usually because they are finished or sold out.
- Court data covers published datalex.am records; a case can name a company whose link to the brand
  is indirect, so read `developer_cases.why` before drawing conclusions.
- The ownership graph is only as complete as the register: the beneficial-owner section is missing for
  part of the companies, and a developer whose legal entity could not be matched has no company node at
  all. Shared legal addresses are a hint, not proof of a common owner — business centres host many
  unrelated firms (addresses shared by more than eight companies are dropped as noise).
- `connection_nodes.bankruptcy_confirmed` holds the azdarar.am notice (or other document) when the
  status was confirmed rather than inferred; `bankruptcy_basis` always says in words which it is.
- `connection_nodes.bankruptcy = 'declared'` is inferred from a court case plus the register's status,
  not from a verdict document; datalex.am publishes no verdict in its case list. The official notice is
  published on azdarar.am, which is linked from every flagged company, and confirmations are recorded by
  hand in `scraper/connections_manual.json`.
