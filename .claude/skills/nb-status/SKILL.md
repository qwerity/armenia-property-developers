---
name: nb-status
description: Show the state of the Armenia new-builds dataset — project/source counts, stages, price confidence, developer grades, pending verification queues, stale sources and the last change report. Use when the user asks "status", "what's the state of the data", or before deciding what to refresh.
---

# nb-status

1. Run `python3 scraper/pipeline.py status` from the `armenia-new-builds` folder.
2. Read `scraper/sources.json`: list sources whose `last_crawled` is older than 30 days or whose status is not `ok`.
3. If `scraper/reports/` has a latest `diff-*.md`, summarise it in 3–5 lines.
4. Check `git status --short` for uncommitted data or skill edits.
5. Reply with a short table and a recommendation of which nb-* skill to run next (e.g. stale sources → `/nb-recrawl`, many low-confidence prices → `/nb-verify prices`, unresearched developers → `/nb-reputation`).

Then follow `../SELF_IMPROVEMENT.md` (usually only step 1 — note anything surprising in `LEARNINGS.md`).
