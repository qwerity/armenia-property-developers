Task: identify the legal entities behind Armenian real-estate developers and collect public news (issues + positives). Court records are handled separately by the coordinator - do NOT call datalex.am.

Input records: /Users/ksh/agents/news-agent/armenia-new-builds/scraper/.rep_devs_3.json (array; fields developer, name_variants, projects, stages, website, sample_projects, phones, emails, sources). Process ONLY the developers listed in your assignment (match on the "developer" field exactly).
Extra local context (read-only): /Users/ksh/agents/news-agent/armenia-new-builds/web/data/projects.json -> {"projects":[...]} with fields developer, title, title_am, source_url, description, developer_about, website, address. Descriptions of ar-go.am / myhome.am records sometimes contain the Armenian developer name.

For EACH developer:
1. Legal entity/entities (brands often use project-specific LLCs): Armenian registered name (e.g. «Կապիտալ Բիլդ» ՍՊԸ), Latin name, legal form (ՍՊԸ/ՓԲԸ/ԲԲԸ/ԱՁ...), tax ID (ՀՎՀՀ, 8 digits) and registration year if findable. Sources: developer website footer/contacts/about/privacy/sales-contract pages, myhome.am builder pages, construction.am company pages, ar-go.am project pages, bank partner lists (Ameriabank/Ardshinbank/ACBA/Inecobank mortgage partner lists), news, e-register.am / spyur.am / hetq / azatutyun / civilnet, etc. Use WebSearch (Armenian / Russian / English queries) and WebFetch or curl (UA "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"). Role: "developer" | "sales agent" | "contractor" | "unknown".
2. News / public issues via WebSearch: unfinished or frozen buildings, buyer protests, fraud, bankruptcy, permit violations, collapses/safety incidents, sanctions, criminal cases involving owners. Also positives: awards, large completed portfolio, bank partnerships, notable projects. Only include items you actually found, with URL.
3. datalex_names: the Armenian-script spellings as they are most likely REGISTERED (no quotes, no ՍՊԸ), most likely first, max 3. Transliterate English brand names phonetically in Armenian registry style (e.g. Capital Build -> Կապիտալ Բիլդ, Group -> Գրուպ, Development -> Դեվելոփմենթ, Construction -> Կոնստրուկցիա or Քոնսթրաքշն). If you found a project-specific LLC, include it.

Output: write a JSON array to /Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_3/web_D.json, REWRITE it after each developer (so partial results survive), one object per developer:
{"developer": "<exact developer field>", "role": "...",
 "legal_entities": [{"name_hy": "", "name_en": "", "tax_id": null, "form": "ՍՊԸ", "registered_year": null, "source_url": ""}],
 "founded_year": null, "datalex_names": ["..."], "tax_ids": ["..."],
 "news_issues": [{"date": "YYYY-MM-DD or YYYY", "title": "", "url": "", "summary": ""}],
 "positives": [{"title": "", "url": "", "summary": ""}],
 "entity_confidence": "high|medium|low", "notes": "how the entity was identified, ambiguities, same-name companies"}
Rules: no logins, captchas or form submissions; polite (<=2 req/s per host); scratch files under /Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_3/. Do not reproduce long copyrighted text - summaries in your own words, one sentence. Budget ~6-10 searches per developer; small unknown ones can be quicker. Don't invent tax IDs - null if not found.
Final message: short list of developers with entity found (name + tax id) / not found, and any serious issues seen.

ASSIGNMENT:
["Advanced development (sales: RED Invest Group)", "Royal Hills (sales: RED Invest Group)", "Argavand Towers  (sales: RED Invest Group)", "Omega Plus (sales: RED Invest Group)", "Gevorg Darbinyan (sales: RED Invest Group)", "Villa Town House  (sales: RED Invest Group)", "Villa Town House", "S. S. Brothers  (sales: RED Invest Group)", "Ecology Construction  (sales: RED Invest Group)", "EREBUNI-ARMANI", "HATIS PARK REZIDENCE", "Los Angeles Yeghvard", "STRONG BUILDINGS", "CAVEMAN RESIDENCE", "GTG ANHAGHT"]
