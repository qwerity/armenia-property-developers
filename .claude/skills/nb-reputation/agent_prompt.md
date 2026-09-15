Task: research the reputation and legal record of Armenian real-estate developers / construction companies.

Input: INPUT_FILE — each item: developer (display name), name_variants, projects (count on our map), stages (finished/in progress/...), website, sample_projects, phones, emails, sources.

For EACH developer:
1. Identify the legal entity/entities (a brand often uses a project-specific LLC): Armenian legal name (e.g. «Կապիտալ Բիլդ» ՍՊԸ), Latin name, legal form, tax ID (ՀՎՀՀ) and registration year if findable. Look at: the developer website footer/contacts/"about", sales contracts or privacy pages, myhome.am builder pages, construction.am company pages, bank partner lists, news (WebSearch in Armenian/Russian/English), state registry e-register.am if reachable. Mark role: "developer" | "sales agent" | "contractor" | "unknown".
2. Court records on datalex.am — use the ready helper (do NOT re-implement):
      cd /Users/ksh/agents/news-agent/armenia-new-builds/scraper && python3 -c "import datalex, json; datalex.MIN_INTERVAL=4; print(json.dumps(datalex.find_cases(['<Armenian legal name without quotes/ՍՊԸ>', '<alt Armenian spelling>'], tax_id='<ՀՎՀՀ or None>'), ensure_ascii=False))"
   Names must be in ARMENIAN script as registered (datalex stores Armenian names, usually upper-case; the helper normalises case/quotes/legal form). Try the likely spellings (e.g. transliterations of English brand names: Capital Build → Կապիտալ Բիլդ). The helper filters fuzzy matches to exact party names; still sanity-check that hits are the same company (tax id in claim text, context).
   Summarise: counts by tab (civil / bankruptcy / administrative / criminal / payment_order) and role (respondent vs claimant); how many as respondent were filed by INDIVIDUALS (likely buyers: person names, not ՍՊԸ/ՓԲԸ) and what they claim (money recovery, contract termination, apartment handover, damages); bankruptcy cases where the company is the debtor; criminal cases; cases in the last 5 years (filed >= 2021). Pick up to 5 notable cases with case_number + one-line reason.
3. News / public issues via WebSearch: unfinished or frozen buildings, buyer protests, fraud, bankruptcy, permit violations, collapses/safety incidents, sanctions — and positives (awards, large completed portfolio, major bank partnerships). Only include items you actually found with a URL.

Output OUTPUT_FILE — JSON array, rewrite after every few developers:
{"developer": "", "role": "developer|sales agent|contractor|unknown",
 "legal_entities": [{"name_hy": "", "name_en": "", "tax_id": null, "form": "ՍՊԸ|ՓԲԸ|...", "registered_year": null, "source_url": ""}],
 "founded_year": null, "searched_names": ["exact strings passed to datalex"],
 "court": {"total": 0, "respondent": 0, "claimant": 0, "respondent_by_individuals": 0, "bankruptcy_as_debtor": 0, "criminal": 0, "administrative": 0, "payment_order": 0, "since_2021": 0,
           "notable": [{"case_number": "", "tab": "", "filed": "", "why": ""}]},
 "news_issues": [{"date": "", "title": "", "url": "", "summary": ""}],
 "positives": [{"title": "", "url": "", "summary": ""}],
 "confidence": "high|medium|low", "notes": ""}
If the legal entity cannot be identified, still search datalex with the most plausible Armenian spelling, set confidence "low" and explain.
Rules: no logins/captchas/forms beyond the datalex helper; be polite (<=2 req/s per host; datalex via the helper only). Scratchpad: SCRATCH
Report at the end: developers with serious issues (bankruptcy, criminal, many buyer lawsuits, frozen projects) and any entity-identification problems.
