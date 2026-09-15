# nb-recrawl learnings

## 2026-09-14/15 (initial build)
- Many developer sites return 406 without full browser Accept/Accept-Language headers (e.g. 4acapital.am).
- Map referrer: images from ar-go.am and similar block hotlinking with a Referer — the web app sends no-referrer.
- Dedupe pitfalls: same building across sources with Armenian vs Latin titles; different buildings with shared street name. Curated merges live in scraper/merge_overrides.json (by source URL) — add new confirmed groups there instead of loosening thresholds.
- Titles in ALL-CAPS Armenian are transliterated at build time (build_dataset.latinize_names).
- Open-Meteo elevation rate-limits (429): elevation.py backs off; re-run build to fill gaps.
