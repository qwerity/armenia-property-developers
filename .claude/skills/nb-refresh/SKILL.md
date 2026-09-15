---
name: nb-refresh
description: Full periodic refresh of the Armenia new-builds map — status check, recrawl all sources, discover new sources, re-verify flagged prices/locations/stages, update developer reputation, rebuild, and report. Use for "full refresh", "update everything", or a scheduled run.
argument-hint: "[--quick]  (quick = cached recrawl + verify only, no discovery/reputation)"
---

# nb-refresh

Orchestrates the other skills in order. Work from the `armenia-new-builds` folder.

1. `/nb-status` — note stale sources and pending queues.
2. `/nb-recrawl all --fresh` (or without `--fresh` for `--quick`).
3. Unless `--quick`: `/nb-discover-sources` (time-box to the highest-yield leads in its LEARNINGS).
4. `/nb-verify all` — only the queues produced after the recrawl.
5. Unless `--quick`: `/nb-reputation all-unresearched`, plus developers whose grade is D/E.
6. Final `python3 scraper/pipeline.py build`, open the app, confirm no console errors, and compare `status` before/after.
7. Report: totals before → after, biggest changes (from diff reports), what each skill learned, and decisions needed.

Self-improvement: each sub-skill runs its own loop; here, record orchestration issues (ordering, timing, agent limits, costs) in `LEARNINGS.md` and adjust this sequence when a step proves unnecessary or missing. Commit `nb-refresh: …`.
