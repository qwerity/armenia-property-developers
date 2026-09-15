---
name: nb-verify
description: Re-check extracted numbers of the Armenia new-builds map against live sources — prices (per m², cheapest unit), locations (pins vs addresses), and construction stages (incl. satellite imagery) — using parallel agents on audit queues, then apply the verified results. Use for "recheck prices", "check locations", "verify stages", or after a recrawl.
argument-hint: "[prices | locations | stages | all] [--batches N]"
---

# nb-verify

Work from the `armenia-new-builds` folder. Read `LEARNINGS.md` first — it lists the recurring pitfalls (sold units, currency slips, placeholder pins, embed centres).

## 1. Build the queues
```
python3 scraper/pipeline.py audit <kind> --batches 3
```
Queues land in `scraper/reports/queue-<kind>-<i>.json`. Report the counts. If a queue is empty, say so and skip that kind. If a queue is huge (> 150), confirm with the user or verify the highest-impact items first (largest discount, most-viewed, flagged developers).

For a FULL recheck of every project (user asks to "recheck all"): build one queue per ~42 projects from `web/data/projects.json`, use `templates/full.md` (price + numbers + stage + location in one pass), output `scraper/recheck_<YYYYMMDD>_<i>.json`, then `python3 scraper/apply_recheck.py <YYYYMMDD>` before building. Keep ≤ 18 agents (20-agent concurrency limit).

## 2. Launch agents (background, one per batch, in a single message)
- Prompt = the matching template in `templates/` (`prices.md`, `locations.md`, `stages.md`) with placeholders replaced:
  - `INPUT_FILE` → the queue file,
  - `OUTPUT_FILE` → `scraper/<price|geo|stage>_verified_<YYYYMMDD>_<i>.json` (new files; older results stay),
  - `SCRATCH` → a fresh folder under the session scratchpad.
- Remind agents: own browser tab only, Nominatim ≤ 1 req/4 s shared, no logins/captchas.

## 3. Apply
When all agents report: `python3 scraper/pipeline.py build`. The build applies `price_verified_*`, `geo_verified_*`, `stage_verified_*` (latest file wins per project; corrected > confirmed). Check the diff report and spot-check 2–3 corrections in the app (preview server `armenia-new-builds`).
- Duplicates the agents report → `scraper/merge_overrides.json`.
- Wrong merges → they are dropped automatically via `wrong_merge_urls`.

## 4. Self-improve and commit
Follow `../SELF_IMPROVEMENT.md`. Typical promotions: a new audit rule in `scraper/pipeline.py` (`audit_prices`, `audit_locations`, `audit_stages`), a price-parsing fix in `scraper/price_audit.py`, a template tweak for a pitfall agents hit repeatedly.
