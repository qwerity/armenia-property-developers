You are researching the reputation / legal identity of Armenian real-estate developers. Work dir (scratchpad): /Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_4/

Input: group_<G>.json in that dir (G given below). Each item: developer (display name — copy it EXACTLY into output), name_variants, projects, stages, website, sample_projects, phones, emails, sources, map_projects (our map entries with source URLs/descriptions).

For EACH developer:
1. Identify the legal entity/entities (brands often use project-specific LLCs): Armenian legal name as registered (e.g. «ԿԱՊԻՏԱԼ ԲԻԼԴ» ՍՊԸ), Latin name, legal form (ՍՊԸ=LLC, ՓԲԸ=CJSC, ԲԲԸ=OJSC, ՀԿ/foundation...), tax ID (ՀՎՀՀ, 8 digits) and registration year if findable. Where to look: developer website footer/contacts/about/privacy/terms/contract pages (WebFetch), myhome.am builder pages, construction.am company pages, ar-go.am project pages ("Կառուցապատող ընկերություն՝ ..."), bank mortgage partner lists (acba.am constructors, evoca, ameriabank, ardshinbank...), karucapatoxic.am, news (WebSearch in Armenian/Russian/English), e-register.am / spyur.am / checkinfo.am / tender (gnumner.am, armeps) pages if reachable without login. Mark role: "developer" | "sales agent" | "contractor" | "unknown".
   Produce the list of Armenian-script name strings most likely registered (upper-case, no quotes, no ՍՊԸ), including plausible alt spellings (e.g. Build → ԲԻԼԴ / ԲԻԼԹ; Group → ԳՐՈՒՊ; Construction → ՔՈՆՍԹՐԱՔՇՆ / ԿՈՆՍՏՐՈՒԿՑԻԱ; Residence → ՌԵԶԻԴԵՆՍ; Development → ԴԵՎԵԼՈՓՄԵՆԹ / ԴԻՎԵԼՈՓՄԵՆԹ). Max 3 strings per entity; avoid very generic single words that would match many unrelated companies.
   AS SOON AS you have the names for a developer, append ONE JSON line to queue_<G>.jsonl in the work dir: {"dev": "<exact developer display name>", "names": ["..."], "tax_id": "<8 digits or null>"} (use python/bash append; one line per entity-name set; you may append additional lines later for other entities of the same developer). A separate worker queries the court database datalex.am with them — do NOT query datalex.am yourself.
2. News / public issues via WebSearch (Armenian, Russian, English; include the brand, legal name, and flagship project names): unfinished or frozen buildings, buyer protests, fraud, bankruptcy, permit violations, demolition orders, collapses/safety incidents, tax evasion, sanctions, criminal cases involving owners — and positives (awards, large completed portfolio, major bank partnerships, well-known completed projects). Only include items you actually found, with URL. Verify the item is about the same company (not a namesake).
Budget: ~4-8 tool calls per small developer, more for large ones (1SQ, Art Company, New City, Arcada, Milon Mining...). Several input items are the same company under different display names (e.g. Milon Mining / MILON MINING, Arcada / Arcada Construction, Amanoo / Khakhamyan Heritage, Faith Built / Feyt Bilt, ASBA x2, Man Invest Grup / MAN INVEST GROUP, Allur Dilijan / SHAMAKHYAN, Bedeck Masis / Pars) — research once, output each display name separately and say so in notes.
Rules: no logins, captchas or form submissions; polite (<=2 req/s per host); no downloads of binaries. Cache anything large under the work dir.

Output: research_<G>.json in the work dir — JSON array, REWRITE after every 2-3 developers so partial results survive:
{"developer": "", "role": "developer|sales agent|contractor|unknown",
 "legal_entities": [{"name_hy": "", "name_en": "", "tax_id": null, "form": "ՍՊԸ|ՓԲԸ|...", "registered_year": null, "source_url": ""}],
 "founded_year": null, "datalex_names": ["exact Armenian strings you queued"],
 "news_issues": [{"date": "", "title": "", "url": "", "summary": ""}],
 "positives": [{"title": "", "url": "", "summary": ""}],
 "confidence": "high|medium|low", "notes": "how the entity was identified, doubts, related brands/owners"}
If the legal entity cannot be identified, still queue the most plausible Armenian spelling, set confidence "low" and explain.
Final message: short list of developers with serious issues found and entity-identification problems.
