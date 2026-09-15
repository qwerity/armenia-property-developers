---
name: nb-reputation
description: Research developer/constructor reputation for the Armenia new-builds map — legal entities and tax IDs, datalex.am court cases (buyer lawsuits, bankruptcy, criminal), registry status and news — and rebuild the A–E developer ratings with source links. Use for "check developer reputation", "legal issues", "update ratings", or a specific developer name.
argument-hint: "[all-unresearched | <developer name> ...] [--batches N]"
---

# nb-reputation

Work from the `armenia-new-builds` folder. Read `LEARNINGS.md` first (namesakes, project LLCs, search-quota fallbacks).

## 1. Queue
- Named developers: build the input file yourself from `web/data/projects.json` (same fields as the audit queue).
- Otherwise: `python3 scraper/pipeline.py audit reputation --batches 3` (developers with no or low-confidence research).
- Re-check high-risk developers periodically even if researched (grade D/E or bankruptcy flags) — datalex gains cases monthly.

## 2. Research (background agents, one per batch, single message)
Prompt = `agent_prompt.md` with `INPUT_FILE` → queue file, `OUTPUT_FILE` → `scraper/developer_reputation_<YYYYMMDD>_<i>.json`, `SCRATCH` → fresh scratchpad folder. Court lookups only through `scraper/datalex.py` with `datalex.MIN_INTERVAL = 4` and a single queue runner. Coordinators must compile their own output file before finishing.

## 3. Rebuild and review
`python3 scraper/pipeline.py build`. In the diff report check grade changes; open 2–3 changed developers in the app and confirm the court links (datalex `case_id` links), registry links and news links work.
Scoring lives in `scraper/reputation.py`; change weights only when the user decides (open questions: age-weighting of old cases, bankruptcy grade cap).

## 4. Self-improve and commit
Follow `../SELF_IMPROVEMENT.md`. Record namesake false positives, new project-LLC mappings, and search fallbacks that worked.
