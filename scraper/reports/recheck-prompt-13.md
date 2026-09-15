Task: FULL re-check of new-building projects in Armenia — every number and the location of each project in the input — against live sources.

Input: /Users/ksh/agents/news-agent/armenia-new-builds/scraper/reports/recheck-all-13.json — each item: id, title, developer, address, district/region, lat/lng (current map pin), geo_precision, current prices (usd_m2_min/amd_m2_min/usd_m2_max, usd_from/amd_from, min_area_m2), floors, completion, stage, sold_out, price_observations (raw figure per source), previous_price_check / previous_location_check (verdicts from an earlier manual check, if any), source_urls, website.

Read first (pitfalls learned so far): /Users/ksh/agents/news-agent/armenia-new-builds/.claude/skills/nb-verify/LEARNINGS.md

For EACH project, open its sources LIVE (developer site first, then myhome.am / redgroup.am unit listings, karucapatoxic.am, ar-go.am, others). Curl with full browser headers (UA "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", Accept text/html, Accept-Language en). Browser pane tools (mcp__Claude_Browser__*) ONLY in your own new tab (tabs_create) for client-rendered pages; close it after; never navigate or reload other tabs.

A. PRICES — current minimum price per m² of AVAILABLE apartments (exclude sold/reserved units), max per m² if shown, cheapest available apartment total + area. Mind AMD vs USD, per m² vs total, thousands. If there's no public price now: say why (sold out / on request / not published).
B. OTHER NUMBERS — floors (as published, e.g. "16" or "9,15"), completion / handover date (YYYY-MM or YYYY), sold out yes/no.
C. LOCATION — the true site: coordinates from a map on a source page (Google embed: use the `!2z` base64 DMS marker or `!3d<lat>!4d<lng>`/`@lat,lng`, NOT the `!2d/!3d` viewport centre; Yandex `pt=`/`ll=` = lng,lat; JSON-LD geo; Leaflet data), and the exact site address (not the sales office). If no map exists, confirm the address via OpenStreetMap Nominatim (https://nominatim.openstreetmap.org/search?format=jsonv2&countrycodes=am&q=...; User-Agent "armenia-new-builds-map/1.0"; STRICT limit: at most 1 request every 25 seconds — many agents share it; use it only when no source map exists). Compare with the current pin: "correct" if within ~150 m.
D. IDENTITY — check that all source_urls describe the same building/phase; list the ones that don't.

Previously checked items still need the live check, but you can be quick if sources are unchanged.

Write /Users/ksh/agents/news-agent/armenia-new-builds/scraper/recheck_20260915_13.json as a JSON array, one object per input id (rewrite the file after every 3–5 projects so progress survives):
{"id": "", "title": "",
 "price": {"verdict": "confirmed|corrected|unverifiable", "usd_m2": number|null, "amd_m2": number|null, "usd_m2_max": number|null, "currency_shown": "AMD|USD", "apartment_from_total": number|null, "apartment_from_area_m2": number|null, "evidence_url": "", "evidence_text": "<exact price text, <=120 chars>", "sold_out": true|false|null, "wrong_merge_urls": [], "notes": ""},
 "numbers": {"floors": "string|null", "completion": "YYYY-MM|YYYY|null", "evidence_url": "", "notes": ""},
 "location": {"verdict": "correct|moved|unlocatable", "lat": number|null, "lng": number|null, "precision": "exact|address|street|district|null", "address": "<site address, Latin preferred>", "evidence_url": "", "evidence": "<short>", "notes": ""}}
Verdict "confirmed" = current usd_m2_min within ±10 %; "corrected" = give the right values. For location "moved" give lat/lng; "correct" may repeat current lat/lng.

Rules: <=2 req/s per host; no logins, captchas or forms. Scratchpad: /private/tmp/claude-501/-Users-ksh-agents-news-agent/f5b9a1b5-d32a-41e5-8985-b59a55e0d0ba/scratchpad/recheck_13/
Report at the end (short): counts per verdict for price and location, the 5 biggest price corrections and 5 largest moves, and any NEW recurring pitfall.
