Task: re-verify apartment prices for new-building projects in Armenia whose price data is suspicious.
Input: INPUT_FILE (each item: id, title, developer, district, current_usd_m2/current_amd_m2 from the automated reconciler, usd_from, reasons, observations = raw figures per source, source_urls).

For EACH project:
1. Open the most authoritative CURRENT sources (developer's own site first, then myhome.am / redgroup.am unit listings, then karucapatoxic.am, then others). Re-fetch live with full browser headers (UA "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", Accept text/html, Accept-Language en). Browser pane tools (mcp__Claude_Browser__*) only in your OWN new tab if a page is client-rendered; close it afterwards; never navigate other tabs.
2. Determine the current MINIMUM price per m² of AVAILABLE apartments (exclude sold/reserved units — this was the #1 cause of wrong prices), its currency as shown, and the cheapest available apartment total + area. Watch units: AMD vs USD, per m² vs total, thousands ("489" may mean 489,000 ֏).
3. Check that the source URLs describe the SAME building (list different buildings/phases as wrong merges).
4. Verdict: "confirmed" (within ±10%), "corrected" (give right value), "unverifiable" (no public price: sold out / on request — say which).

Write OUTPUT_FILE as a JSON array (rewrite after every few items):
{"id": "", "title": "", "verdict": "confirmed|corrected|unverifiable", "usd_m2": number|null, "amd_m2": number|null, "currency_shown": "AMD|USD", "apartment_from_total": number|null, "apartment_from_area_m2": number|null, "evidence_url": "", "evidence_text": "<exact price text, <=120 chars>", "sold_out": true|false|null, "wrong_merge_urls": [], "notes": ""}
Rules: <=2 req/s per host, no logins/captchas/forms. Scratchpad: SCRATCH
Report: counts per verdict, biggest corrections, and any NEW recurring pitfall (so the skill can learn it).
