# nb-reputation learnings

## 2026-09-15 (initial build)
- datalex search is word-fuzzy: always filter to exact party names (datalex.py does) and sanity-check namesakes (Mets Syunik wine co., Vardanyanshin old Kotayk company, ՇԱՄԱԽՅԱՆ surname/street).
- Brands often sign contracts through project LLCs (Shinas for Tigran Mets, Magnolia Comfort for Zover, Arcada Construction for Ember, Gasparyan & Sons for Capital Build) — search those too.
- Tax IDs: karg.am/company/<id> and construction.am company pages are the quickest sources.
- WebSearch quota (200/session) runs out quickly with parallel agents; use news-site search pages (azatutyun, hetq, factor, aravot, armlur, 168.am) and Bing/Google News RSS as fallback, and mark coverage as partial in notes.
- "respondent_by_individuals" is a name-pattern heuristic; employee wage claims and shareholder disputes (Lorida Group) inflate it — note these.
- Zero datalex hits for companies with known tax IDs (Bedeck, TOP BUILDINGS, SIL Capital) usually means a spelling variant — try more variants.
- Coordinator agents that spawn helpers must run the final compile themselves; one run left a worker idling for 16 h waiting for a DONE file.
