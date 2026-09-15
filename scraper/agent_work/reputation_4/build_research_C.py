import json, os

D = os.path.dirname(os.path.abspath(__file__))
NOTE_SEARCH = " WebSearch budget for the session was exhausted early in this group, so news coverage beyond the cited items was not searched; absence of issues is NOT evidence of a clean record."


def le(name_hy, name_en, form, url, year=None, tax=None):
    return {"name_hy": name_hy, "name_en": name_en, "tax_id": tax, "form": form, "registered_year": year, "source_url": url}


amanoo_entities = [le("«Խախամյան Հերիթիջ» ՍՊԸ", "Khakhamyan Heritage LLC", "ՍՊԸ", "http://env.am/announcement/public-reviews/Khakhamyan-heritage-07-08-2023")]
amanoo_pos = [
    {"title": "500 million drams to clean Yerevan's air: Khakhamyan Heritage restores the Nork forests", "url": "https://armenpress.am/en/article/1257824", "summary": "AMD 500m programme with Yerevan Municipality to restore 4 ha of Nork forest; phase 1 greened 2 ha, 1,100 trees/shrubs."},
    {"title": "IVY at AMANOO completed and inhabited", "url": "https://www.amanoo.am/en/", "summary": "First phase (Ivy, 4 buildings, 50 residences) completed; Sarin under construction to 2028; whole 11 ha district planned to 2036."},
]
amanoo_news = [
    {"date": "2023-08-07", "title": "EIA application by «Խախամյան Հերիթիջ» ՍՊԸ for multi-apartment building at G. Hovsepyan 46/10", "url": "http://env.am/announcement/public-reviews/Khakhamyan-heritage-07-08-2023", "summary": "Routine environmental impact pre-assessment public hearing (16 Aug 2023) - regulatory record, not an adverse finding."},
]
amanoo_notes = "Brand AMANOO by Khakhamyan Heritage (founder Avetis Khakhamyan). Registered spelling «Խախամյան Հերիթիջ» ՍՊԸ confirmed via env.am and jobs.am employer page; tax ID not found. No negative news found in searches for Amanoo/Khakhamyan (permit/forest controversy query returned only positive coverage). Same company as display names 'Khakhamyan Heritage (AMANOO)' and 'Amanoo'."

rows = [
    {"developer": "Khakhamyan Heritage (AMANOO)", "role": "developer", "legal_entities": amanoo_entities, "founded_year": None,
     "datalex_names": ["ԽԱԽԱՄՅԱՆ ՀԵՐԻԹԻՋ", "ԽԱԽԱՄՅԱՆ ՀԵՐԻԹԵՅՋ", "ԱՄԱՆՈՒ"], "news_issues": amanoo_news, "positives": amanoo_pos,
     "confidence": "high", "notes": amanoo_notes},
    {"developer": "Amanoo", "role": "developer", "legal_entities": amanoo_entities, "founded_year": None,
     "datalex_names": ["ԽԱԽԱՄՅԱՆ ՀԵՐԻԹԻՋ", "ԽԱԽԱՄՅԱՆ ՀԵՐԻԹԵՅՋ", "ԱՄԱՆՈՒ"], "news_issues": amanoo_news, "positives": amanoo_pos,
     "confidence": "high", "notes": amanoo_notes},
    {"developer": "AR-SHIN CONSTRUCT", "role": "developer",
     "legal_entities": [le("«ԱՐ-ՇԻՆ ՔՈՆՍԹՐԱՔԹ» ՍՊԸ", "AR-SHIN CONSTRUCT LLC", "ՍՊԸ", "https://myhome.am/en/building/211")],
     "founded_year": None, "datalex_names": ["ԱՐ-ՇԻՆ ՔՈՆՍԹՐԱՔԹ", "ԱՐ ՇԻՆ ՔՈՆՍԹՐԱՔԹ", "ԱՐ-ՇԻՆ ԿՈՆՍՏՐՈՒԿՏ"],
     "news_issues": [], "positives": [],
     "confidence": "high", "notes": "Legal name shown on myhome.am builder card (Armenian ԱՐ-ՇԻՆ ՔՈՆՍԹՐԱՔԹ ՍՊԸ; English typo 'AR-SHI CONSTRUCT LLC'); office Norashen 47/5, Ajapnyak; projects Nor Aresh 42nd St 30/2 and NEW POINT TOWNHOUSE (sold out). Small builder, no press coverage found." + NOTE_SEARCH},
    {"developer": "Kam Developments", "role": "developer",
     "legal_entities": [le("«Կամ Դեվելոփմենթս» ՍՊԸ", "Kam Developments LLC", "ՍՊԸ", "https://www.evoca.am/hy/construction-companies")],
     "founded_year": None, "datalex_names": ["ԿԱՄ ԴԵՎԵԼՈՓՄԵՆԹՍ", "ՔԱՄ ԴԵՎԵԼՈՓՄԵՆԹՍ", "ԿԱՄ ԴԻՎԵԼՈՓՄԵՆԹՍ"],
     "news_issues": [],
     "positives": [{"title": "Listed as Evoca Bank and Byblos Bank Armenia mortgage partner", "url": "https://www.evoca.am/en/construction-companies#21-kam-developments-llc", "summary": "Bank-financed mortgages (own resources) for Davitashen Village townhouses (G. Aghababyan 7/7-7/18) and Ajapnyak G-1 district plots."}],
     "confidence": "medium", "notes": "Evoca's Armenian list spells «Կամ Դեվելոփմենթս» ՍՊԸ. Website field points to Sold Realty Facebook page - Sold Realty appears to be exclusive sales agent. Armenian search for the name returned nothing relevant." + NOTE_SEARCH},
    {"developer": "NovaVan Residence (New Home  / Lore Construction)", "role": "developer",
     "legal_entities": [le("«Լոռե Քոնսթրաքշն» ՍՊԸ", "Lore Construction LLC", "ՍՊԸ", "https://factor.am/906356.html", 2025)],
     "founded_year": 2025, "datalex_names": ["ԼՈՌԵ ՔՈՆՍԹՐԱՔՇՆ", "ԼՈՌԵ ԿՈՆՍՏՐՈՒԿՑԻԱ", "ՆՈՎԱՎԱՆ"],
     "news_issues": [{"date": "2025-06-26", "title": "Բանտապետը սեփականաշնորհել է բանտի շենքը, ԱԱԾ վարչության պետ որդին՝ վաճառել (Factor.TV)", "url": "https://factor.am/906356.html",
                      "summary": "The 3,749 m² plot at 14 Tumanyan St, Vanadzor was a former prison building privatised in 2006-07 by the then prison director Shaverdi Alchanguyan; his son Karen Alchanguyan (ex-head of NSS Lori department) sold it on 30 Apr 2025 to «Լոռե Քոնսթրաքշն» ՍՊԸ, founded 13 days earlier (17 Apr 2025) by director Bagrat Khachatryan. 13-storey project got preliminary approval after 20 May 2025 hearing; municipal officials raised seismic (usual 4-5 storey limit) and groundwater concerns."}],
     "positives": [],
     "confidence": "high", "notes": "Developer entity for NovaVan (14 Tumanyan St, Vanadzor; construction 2026-Nov 2028, 161 apartments) is Lore Construction LLC (email loreconstructionllc@gmail.com). Website claims '30,000+ satisfied customers, 700 apartments' - likely borrowed from the New Home brand (Yerevan sales office Davtashen 2nd district 22/2); 'New Home' (ՆՅՈՒ ՀՈՄ) already queued in queue_main. Very young SPV (2025) with a controversial land provenance; no track record under its own name." + NOTE_SEARCH},
    {"developer": "Lav-Sar (FeliCity)", "role": "developer",
     "legal_entities": [le("«Լավ-Սար» ՍՊԸ", "Lav-Sar LLC", "ՍՊԸ", "https://www.estate.am/felicity-%D5%A2%D5%B6%D5%A1%D5%AF%D5%A5%D5%AC%D5%AB-%D5%B0%D5%A1%D5%B4%D5%A1%D5%AC%D5%AB%D6%80-p34")],
     "founded_year": 2019, "datalex_names": ["ԼԱՎ-ՍԱՐ", "ԼԱՎ ՍԱՐ"],
     "news_issues": [],
     "positives": [{"title": "FeliCity Davitashen completed; second FeliCity project in Nor Nork", "url": "https://felicity.am/", "summary": "FeliCity Davitashen (Mikoyan 25/27, 4 residential 16-storey buildings + public building) completed 2025; FeliCity Nor Nork (David Bek lane 5/5) on sale."}],
     "confidence": "medium", "notes": "estate.am and 2GIS list 'Լավ-Սար' as the FeliCity developer (office A. Mikoyan 127). founded_year 2019 inferred only from email lavsar2019@gmail.com. Names already queued in queue_main (not repeated). No issue found in a targeted Armenian search." + NOTE_SEARCH},
    {"developer": "Fast Pro", "role": "developer",
     "legal_entities": [le("«Ֆասթ Պրո» ՍՊԸ", "Fast Pro LLC", "ՍՊԸ", "https://fastpro.am/", 2023),
                        le("Վի Էմ Բիլդինգ", "VM Building", "unknown", "https://www.evoca.am/hy/construction-companies")],
     "founded_year": 2023, "datalex_names": ["ՖԱՍԹ ՊՐՈ", "ՖԱՍՏ ՊՐՈ", "ՎԻ ԷՄ ԲԻԼԴԻՆԳ", "ՎԻ-ԷՄ ԲԻԼԴԻՆԳ"],
     "news_issues": [],
     "positives": [{"title": "Evoca Bank mortgage partner for VM Building (Malkhasyants 9/4)", "url": "https://www.evoca.am/hy/construction-companies", "summary": "Evoca lists 'Վի Էմ Բիլդինգ', Arabkir, Malkhasyants 9/4, phone +374 41 10 14 15 (same as Fast Pro)."}],
     "confidence": "medium", "notes": "Fast Pro LLC (founded 2023 per caller hint) markets VM Building; Evoca lists the project under 'Վի Էմ Բիլդինգ' (legal form not shown - may be the brand, not a registered entity). ՖԱՍԹ ՊՐՈ/ՖԱՍՏ ՊՐՈ already queued in queue_main; only VM Building names queued here. fastpro.am renders client-side, no legal info extractable." + NOTE_SEARCH},
    {"developer": "Zeytoun Build", "role": "developer",
     "legal_entities": [le("«Զեյթուն Բիլդ» ՍՊԸ (spelling unconfirmed)", "Zeytun Build LLC", "ՍՊԸ", "http://zeytunbuild.am/")],
     "founded_year": None, "datalex_names": ["ԶԵՅԹՈՒՆ ԲԻԼԴ", "ԶԵՅԹՈՒՆ ԲԻԼԹ", "ԶԵՅԹՈՒՆԲԻԼԴ"],
     "news_issues": [],
     "positives": [{"title": "Zeytun Build complex commissioned 12.2024", "url": "https://karucapatoxic.am/en/62", "summary": "Three-section 16/18-storey monolithic complex at Paruyr Sevak 51/11 with kindergarten and 3-level underground parking; commissioning 12.2024."}],
     "confidence": "low", "notes": "Only the brand 'Զեյթուն Բիլդ' (karucapatoxic title_am) is confirmed; website has no legal info. Email hbgroup352@gmail.com hints at a related 'HB Group' (not queued - too uncertain/generic)." + NOTE_SEARCH},
    {"developer": "Jet Set Construct", "role": "developer",
     "legal_entities": [le("«Ջեթ Սեթ Քոնսթրաքթ» ՍՊԸ (form assumed)", "Jet Set Construct", "ՍՊԸ", "https://www.construction.am/arm/companies/jet-set-construct/", 2007)],
     "founded_year": 2007, "datalex_names": ["ՋԵԹ ՍԵԹ ՔՈՆՍԹՐԱՔԹ", "ՋԵԹ ՍԵԹ ԿՈՆՍՏՐՈՒԿՏ"],
     "news_issues": [], "positives": [{"title": "Abelyan 2/1 (Ajapnyak) commissioned 03.2023", "url": "https://karucapatoxic.am/en/128", "summary": "10-16 storey residential building completed."}],
     "confidence": "medium", "notes": "construction.am (Armenian page) spells 'Ջեթ Սեթ Քոնսթրաքթ', founded 2007, Dzorapi 70/3; builds high-rise residential/commercial. Legal form not shown." + NOTE_SEARCH},
    {"developer": "Armat Realty", "role": "sales agent",
     "legal_entities": [le("«Արմատ Ռիելթի» (form unknown)", "Armat Realty", "unknown", "https://www.construction.am/arm/companies/armat-realty/", 2021),
                        le("«ԱՄԵՐԻԿԱՆԱ «ՍԱԳԱ ՇԻՆ»» ՍՊԸ", "Americana Saga Shin LLC", "ՍՊԸ", "https://www.construction.am/arm/apartments-in-new-developments/americana-armenia/")],
     "founded_year": 2021, "datalex_names": ["ԱՐՄԱՏ ՌԻԵԼԹԻ", "ԱՐՄԱՏ ՌԵԱԼԹԻ"],
     "news_issues": [], "positives": [],
     "confidence": "medium", "notes": "Armat Realty is a real-estate agency (founded 2021, Shinararneri 28/2) that markets Americana jointly with Saga-Shin LLC (the actual developer); construction.am also lists it for Amelia Residence (Arabkir 29). Shares phone +374 93 913191 with Amerikana. Saga Shin names already queued in queue_main." + NOTE_SEARCH},
    {"developer": "Amerikana Saga Shin", "role": "developer",
     "legal_entities": [le("«ԱՄԵՐԻԿԱՆԱ «ՍԱԳԱ ՇԻՆ»» ՍՊԸ", "Americana Saga Shin LLC", "ՍՊԸ", "https://www.acba.am/hy/individuals/loans/mortgage/constructors#10195")],
     "founded_year": None, "datalex_names": ["ՍԱԳԱ ՇԻՆ", "ՍԱԳԱ-ՇԻՆ"],
     "news_issues": [],
     "positives": [{"title": "ACBA Bank mortgage partner - Americana (G. Chaush 140-142)", "url": "https://www.acba.am/hy/individuals/loans/mortgage/constructors#10195", "summary": "Completed 4-storey buildings, 184 apartments; listed among ACBA constructor partners."}],
     "confidence": "high", "notes": "Legal name per caller hint/ACBA; Armat Realty is sales agent. Names queued in queue_main, not repeated. Planned 16 houses + 6 apartment buildings next to Vahakni (Proshyan/Chaush 140)." + NOTE_SEARCH},
    {"developer": "Royal Classic House", "role": "developer",
     "legal_entities": [le("«Ռոյալ Կլասիկ Հաուզ» (form unknown)", "Royal Classic House", "unknown", "https://www.construction.am/arm/companies/royal-classic-house/", 2013)],
     "founded_year": 2013, "datalex_names": ["ՌՈՅԱԼ ԿԼԱՍԻԿ ՀԱՈՒԶ", "ՌՈՅԱԼ ԿԼԱՍԻԿ ՀԱՈՒՍ"],
     "news_issues": [],
     "positives": [{"title": "Royal Classic House, Buzand 3 - completed 2013", "url": "https://www.construction.am/arm/apartments-in-new-developments/royal-classic-house/", "summary": "9,000 m² residential/business complex 70 m from Republic Square, architect Narek Sargsyan (then Chief Architect of Armenia); built by GLG Company."}],
     "confidence": "low", "notes": "construction.am profile is a business-centre/property-management entity at Buzand 3 (founded 2013); project text says it was built by 'GLG Company' - GLG's registered name not found (Armenian spelling unknown, not queued)." + NOTE_SEARCH},
    {"developer": "Vardanyanshin  (Abovyan Hills)", "role": "developer",
     "legal_entities": [le("«Վարդանյանշին» ՍՊԸ", "Vardanyanshin LLC", "ՍՊԸ", "https://abovyanhills.am/"),
                        le("«Բաղրամյանշին» (founder; site says ԲԲ)", "Baghramyanshin", "unknown", "https://abovyanhills.am/"),
                        le("«Վալեքս» (founder; site says ՍՊ)", "Valex", "unknown", "https://abovyanhills.am/")],
     "founded_year": None, "datalex_names": ["ՎԱՐԴԱՆՅԱՆՇԻՆ", "ՎԱՐԴԱՆՅԱՆ ՇԻՆ", "ԲԱՂՐԱՄՅԱՆՇԻՆ", "ԲԱՂՐԱՄՅԱՆ ՇԻՆ", "ՎԱԼԵՔՍ", "ՎԱԼԵՔՍ ՍՊ"],
     "news_issues": [],
     "positives": [{"title": "Founders previously delivered Avan Hills multifunctional complex", "url": "https://abovyanhills.am/", "summary": "Abovyan Hills site: Baghramyanshin and Valex jointly built Avan Hills; Vardanyanshin LLC created by them for Abovyan Hills (154 flats, 4,597 m² plot, construction progressing - 1st residential floor Mar 2026)."}],
     "confidence": "high", "notes": "Vardanyanshin names already in queue_main; queued founders Baghramyanshin and Valex here. 'ՎԱԼԵՔՍ' is short and could match namesakes - verify case parties. Office Tsarav Aghbyur 61/4." + NOTE_SEARCH},
    {"developer": "Solar City / Solar Siti", "role": "developer",
     "legal_entities": [le("«Սոլար Սիթի» (form unknown)", "Solar City", "unknown", "https://www.construction.am/arm/companies/solar-city/", 2017)],
     "founded_year": 2017, "datalex_names": ["ՍՈԼԱՐ ՍԻԹԻ", "ՍՈԼԱՐ-ՍԻԹԻ"],
     "news_issues": [],
     "positives": [{"title": "Nansen residential complex (Nansen 26/1, Nor Nork) - completion Q4 2021", "url": "https://geoln.com/ru/armenia/yerevan/nansen", "summary": "14-storey monolithic building, 91 flats, energy class A+, 58 underground parking spaces."}],
     "confidence": "medium", "notes": "construction.am profile 'Սոլար Սիթի', founded 2017, Tsitsernakaberd hwy 1/2, builds high-rise residential. Legal form not shown." + NOTE_SEARCH},
]

asba_entities = [le("«Ազգային սոցիալական բնակարանային ասոցիացիա» հիմնադրամ", "National Social Housing Association (ASBA) Foundation", "հիմնադրամ", "https://www.construction.am/arm/companies/national-social-housing-association-foundation-asba/", 2010)]
asba_pos = [{"title": "First social affordable rental housing project in Armenia - Dilijan", "url": "https://www.asba.am/en/Dilijan/", "summary": "Non-profit Dutch-Armenian foundation; phase I 16 energy-efficient terraced apartments completed Dec 2014 (Dutch International Guarantees for Housing, guaranteed by Groen West)."}]
asba_notes = "Non-profit foundation (not an LLC) founded 2010, Baghramyan Ave 18 apt 2. Same organisation under both ASBA display names. 'ԱՍԲԱ' is a short acronym - datalex hits must be checked for namesakes." + NOTE_SEARCH
for dn in ["National Social Housing Association (ASBA)", "National Social Housing Association (ASBA Foundation)"]:
    rows.append({"developer": dn, "role": "developer", "legal_entities": asba_entities, "founded_year": 2010,
                 "datalex_names": ["ԱԶԳԱՅԻՆ ՍՈՑԻԱԼԱԿԱՆ ԲՆԱԿԱՐԱՆԱՅԻՆ ԱՍՈՑԻԱՑԻԱ", "ԱՍԲԱ"], "news_issues": [], "positives": asba_pos,
                 "confidence": "high", "notes": asba_notes})

rows += [
    {"developer": "Hovnanian International  (Vahakni Residential Community)", "role": "developer",
     "legal_entities": [le("«Հովնանյան Ինթերնեյշնլ» ՍՊԸ (spelling/form unconfirmed)", "Hovnanian International L.T.D.", "ՍՊԸ", "https://www.vahakni.com/en/about")],
     "founded_year": None, "datalex_names": ["ՀՈՎՆԱՆՅԱՆ ԻՆԹԵՐՆԵՅՇՆԼ", "ՀՈՎՆԱՆՅԱՆ ԻՆՏԵՐՆԵՅՇՆԼ", "ՀՈՎՆԱՆՅԱՆ ԻՆՏԵՐՆԱՑԻՈՆԱԼ"],
     "news_issues": [],
     "positives": [{"title": "Vahakni gated community, Ajapnyak (since 2000s)", "url": "https://www.vahakni.com/en", "summary": "Large completed American-style community with Ararat Valley Country Club, golf course, QSI school; site copyright 2004-2026."}],
     "confidence": "low", "notes": "Website states community is 'constructed and built by Hovnanian International L.T.D.' (Vahak Hovnanian, US builder). Armenian registered spelling not found; three plausible transliterations queued." + NOTE_SEARCH},
    {"developer": "Melkonyan Realty", "role": "sales agent",
     "legal_entities": [le("«Մելքոնյան Ռիելթի» (form unknown)", "Melkonyan Realty", "unknown", "https://www.construction.am/arm/companies/melkonyan-realty/", 2018),
                        le("«Պալլադիո-Շին» (contractor/builder; form unknown)", "Palladio-Shin", "unknown", "https://www.construction.am/arm/apartments-in-new-developments/palladio-shin/")],
     "founded_year": 2018, "datalex_names": ["ՄԵԼՔՈՆՅԱՆ ՌԻԵԼԹԻ", "ՊԱԼԼԱԴԻՈ ՇԻՆ", "ՊԱԼԱԴԻՈ ՇԻՆ"],
     "news_issues": [],
     "positives": [{"title": "High Park residential community (Avan) - completed 2017", "url": "https://www.construction.am/arm/apartments-in-new-developments/palladio-shin/", "summary": "27 loft-style detached houses planned (8 built at listing time), designs by Cherkezyan architectural studio."}],
     "confidence": "medium", "notes": "construction.am classifies Melkonyan Realty (founded 2018, Kievyan 5) as a realtor/valuation agency; houses were 'built by Palladio-Shin construction organisation' (listing slug palladio-shin). US phone +1 559 suggests diaspora owner. Role could be developer-marketer." + NOTE_SEARCH},
    {"developer": "Alma-ata Rezidens", "role": "developer",
     "legal_entities": [le("«Ալմա-Աթա Ռեզիդենս» (form unknown)", "Alma-Ata Residence", "unknown", "https://yerevan.etagi.com/en-us/zastr/jk/jk-54415/")],
     "founded_year": None, "datalex_names": ["ԱԼՄԱ-ԱԹԱ ՌԵԶԻԴԵՆՍ", "ԱԼՄԱ ԱԹԱ ՌԵԶԻԴԵՆՍ", "ԱԼՄԱԱԹԱ ՌԵԶԻԴԵՆՍ"],
     "news_issues": [], "positives": [],
     "confidence": "low", "notes": "Etagi lists developer as 'ԱԼՄԱ-ԱԹԱ ՌԵԶԻԴԵՆՍ' for complex at Alma-Ata St 1/4 (Avan), delivery 'Finished', 41 offers from AMD 511k/m². Likely project-named SPV; no other source." + NOTE_SEARCH},
    {"developer": "Snart Construction Company", "role": "developer",
     "legal_entities": [le("«Սնառտ» (form unknown)", "Snart Construction Company", "unknown", "https://www.construction.am/arm/companies/snart-construction-company/", 2003)],
     "founded_year": 2003, "datalex_names": ["ՍՆԱՌՏ", "ՍՆԱՌՏ ՇԻՆԱՐԱՐԱԿԱՆ ԸՆԿԵՐՈՒԹՅՈՒՆ"],
     "news_issues": [],
     "positives": [{"title": "Riviera, A. Mikoyan 2/2 (Davtashen) - completed 2013", "url": "https://www.construction.am/arm/apartments-in-new-developments/rivera-mikoyan-st-2-2-davtashen/", "summary": "Commissioned residential building with 9,000 m² landscaped area; company describes itself as one of Armenia's largest multi-profile builders (residential, industrial, hydro, gas/water pipelines)."}],
     "confidence": "medium", "notes": "construction.am: 'Սնառտ Շինարարական Ընկերություն', founded 2003, Manandyan 33. Registered form not shown (ՍՊԸ or ՓԲԸ). Also general contractor - datalex hits may involve public-works contracts." + NOTE_SEARCH},
    {"developer": "Dream House", "role": "developer",
     "legal_entities": [le("«Դրիմ Հաուս» (form unknown)", "Dream House", "unknown", "https://www.construction.am/arm/companies/dream-house/", 2017)],
     "founded_year": 2017, "datalex_names": ["ԴՐԻՄ ՀԱՈՒՍ", "ԴՐԻՄ ՀԱՈՒԶ"],
     "news_issues": [],
     "positives": [{"title": "Dream House, David Bek St (Erebuni) - completed 2020", "url": "https://www.construction.am/arm/apartments-in-new-developments/dream-house-david-bek/", "summary": "Completed residential building."}],
     "confidence": "low", "notes": "construction.am: 'Դրիմ Հաուս', founded 2017, contact Arsen Nagdalyan (email anagdalyan@), Nork-Marash. Name is generic - multiple unrelated 'Dream House' entities likely; verify datalex hits." + NOTE_SEARCH},
    {"developer": "Goght Urban Valley", "role": "developer",
     "legal_entities": [le("unknown (brand Goght Urban Valley)", "Goght Urban Valley", "unknown", "https://goghtvalley.com/en")],
     "founded_year": None, "datalex_names": ["ԳՈՂՏ ՈՒՐԲԱՆ ՎԵԼԻ", "ԳՈՂԹ ՈՒՐԲԱՆ ՎԵԼԻ", "ԳՈՂՏ ՎԵԼԻ"],
     "news_issues": [],
     "positives": [
         {"title": "Winner, 'Best Special Project' - Novosti-Armenia 20th anniversary (Dec 2023)", "url": "https://goghtvalley.com/en/news/31/goght-urban-valley-winner-in-the-best-special-project-category", "summary": "Award for special project 'Armenian Architectural Symphony'."},
         {"title": "MoU with Le Rond Group and Accor for Swissôtel Park Village & Wellness Resort", "url": "https://goghtvalley.com/en/news/37/a-five-star-swissotel-resort-featuring-a-wellness-center-and-a-nature-park-will-open-in-armenias-goght-urban-valley", "summary": "Five-star Swissôtel resort planned inside the 70 ha project (Kotayk); founder/investor Hrayr Melkonyan, spokesman Movses Dzavaryan."}],
     "confidence": "low", "notes": "Website shows no legal entity; founder/investor Hrayr Melkonyan (possible link to Melkonyan Realty unverified). Queued brand transliterations only - datalex may return nothing if the SPV has another name." + NOTE_SEARCH},
]

json.dump(rows, open(os.path.join(D, "research_C.json"), "w"), ensure_ascii=False, indent=1)
print(len(rows))
