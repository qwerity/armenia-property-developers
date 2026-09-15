Task: identify legal entities and find news/public reputation for Armenian real-estate developers.

Input: {DIR}/chunk_{N}.json — each item: developer (display name), name_variants, projects, stages, website, sample_projects, phones, emails, sources.
Extra local context (read-only): /Users/ksh/agents/news-agent/armenia-new-builds/web/data/projects.json ({"projects":[...]}, match on "developer" field; fields developer_about, description, source_url, sources may mention legal names).

For EACH developer:
1. Legal entity/entities (a brand often uses a project-specific LLC): Armenian legal name (e.g. «Կապիտալ Բիլդ» ՍՊԸ), Latin name, legal form (ՍՊԸ/ՓԲԸ/...), tax ID (ՀՎՀՀ, 8 digits) and registration year if findable. Look at: developer website footer/contacts/about/privacy/terms/public offer pages, myhome.am builder pages, construction.am company pages, karucapatoxic.am, ar-go.am project pages, bank partner lists, spyur.am, news (WebSearch in Armenian/Russian/English), e-register.am search results if reachable without login. Mark role: "developer" | "sales agent" | "contractor" | "unknown".
   Also produce "datalex_names": 1-4 Armenian-script spellings of the registered name WITHOUT quotes and WITHOUT legal form (e.g. "Կապիտալ Բիլդ"), most likely first — include project-specific LLCs too. If the Armenian name is not found, give the most plausible transliteration(s) of the brand (Build→Բիլդ, Construction→Կոնստրուկցիա/Քոնսթրաքշն, Group→Գրուպ, Invest→Ինվեստ, Shin→Շին, Development→Դիվելոփմենթ) and say so in notes.
2. News / public issues via WebSearch (Armenian, Russian, English): unfinished or frozen buildings, buyer protests, fraud, bankruptcy, permit violations, collapses/safety incidents, sanctions, criminal cases involving owners — and positives (awards, large completed portfolio, major bank partnerships). Only include items you actually found, with URL. Be careful about same-name confusion (verify it's the same company).

Rules: no logins/captchas/forms; polite fetching (<=2 req/s per host, curl with browser UA). Do NOT query datalex.am (handled separately). Cache pages under {DIR}/sub_{N}/.
Output: {DIR}/entities_{N}.json — JSON array, rewrite after every developer:
{"developer": "<exact display name from input>", "role": "...", "legal_entities": [{"name_hy": "", "name_en": "", "tax_id": null, "form": "", "registered_year": null, "source_url": ""}], "founded_year": null, "datalex_names": [], "tax_id_for_search": null, "news_issues": [{"date": "", "title": "", "url": "", "summary": ""}], "positives": [{"title": "", "url": "", "summary": ""}], "confidence": "high|medium|low", "notes": ""}
Budget: roughly 4-8 web searches/fetches per developer; don't stall on one. Final reply: 2-3 lines only (count done, any serious issues spotted).
