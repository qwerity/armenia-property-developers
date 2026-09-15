# Data commands

Project skills live in `.claude/skills/` (use them as slash commands when Claude Code runs in this folder, or in the parent folder where they show up scoped as `armenia-new-builds:nb-…`).

| Command | What it does |
|---|---|
| `/nb-status` | Dataset health: counts, stages, price confidence, grades, stale sources, pending queues, last diff |
| `/nb-recrawl [all\|karucapatoxic\|extra\|catalogs\|devsites\|enrich] [--fresh]` | Re-crawl existing sources, rebuild, write a change report |
| `/nb-discover-sources [region\|type\|missed URL]` | Find and evaluate new sources/developers, add scrapers and registry entries |
| `/nb-verify [prices\|locations\|stages\|all]` | Re-check flagged numbers on live sources with parallel agents and apply results |
| `/nb-reputation [all-unresearched\|developer…]` | Legal entities, datalex court cases, registry and news → developer A–E ratings |
| `/nb-refresh [--quick]` | Runs the above in order and reports before/after |

Self-improvement: every skill appends to its `LEARNINGS.md` and updates its own `SKILL.md`, prompt templates, `scraper/sources.json` or scraper code when a lesson is durable (see `.claude/skills/SELF_IMPROVEMENT.md`), then commits.

Underlying CLI (usable without Claude):
```
python3 scraper/pipeline.py status
python3 scraper/pipeline.py crawl --only karucapatoxic,extra,catalogs,enrich [--fresh]
python3 scraper/pipeline.py build          # rebuild + scraper/reports/diff-*.md
python3 scraper/pipeline.py audit all      # verification queues in scraper/reports/
```
Key data files: `scraper/sources.json` (source registry), `scraper/developers_master.json`, `scraper/*_verified_*.json` (manual checks), `scraper/developer_reputation_*.json`, `scraper/merge_overrides.json`, `scraper/geo_overrides.json`. Agent helper scripts from the initial research are kept in `scraper/agent_work/` for reference.
