# Self-improvement protocol (shared by all nb-* skills)

Every nb-* run ends with this loop. It is how the skills get better over time.

1. **Record** — append a dated entry to the skill's `LEARNINGS.md`: what worked, what broke (site changed, blocked, new format, false positives), numbers (items processed, corrections, failures). Facts only, no filler.
2. **Promote** — if a learning is durable and changes how the job should be done, edit the skill itself:
   - `SKILL.md` steps, thresholds or ordering,
   - agent prompt templates (`templates/*.md`, `agent_prompt.md`, `project_schema.md`),
   - `scraper/sources.json` (status ok/degraded/blocked/dead, method notes, last_crawled),
   - code in `scraper/` (a scraper fix, a new audit rule in `pipeline.py`, a dedupe rule) — keep changes minimal and match surrounding style.
   Remove or rewrite advice that proved wrong; do not let LEARNINGS.md contradict SKILL.md.
3. **Curate data corrections as data** — confirmed duplicates → `scraper/merge_overrides.json`; confirmed coordinates → `scraper/geo_overrides.json` or `geo_verified_*.json`; manual checks → `price_verified_*`, `stage_verified_*`, `developer_reputation_*`. Never hard-code one-off fixes in Python.
4. **Verify** — rebuild (`python3 scraper/pipeline.py build`) and confirm the app still loads (preview server `armenia-new-builds`, no console errors) when code changed.
5. **Commit** — one commit per run: data + learnings + skill edits, message `nb-<skill>: <summary>`, ending with the attribution line required by the session. Never push unless the user asks.
6. **Report** to the user: what changed (diff report path), what the skill learned, and anything that needs their decision.

Guardrails: polite crawling (<=2 req/s per host; Nominatim <=1 req/4 s across agents; datalex via `scraper/datalex.py` only), no logins/captchas/paywalls, respect robots disallow for APIs, never delete caches (pipeline renames them), keep `.env` and `web/config.js` out of git.
