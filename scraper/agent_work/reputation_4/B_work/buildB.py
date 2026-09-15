import json
D='/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_4/'
NS=" News search was cut short: the session-wide WebSearch budget ran out during this group, so only direct fetches of company/directory pages were possible. No negative news verified; absence of issues is NOT evidence of a clean record."
CA='https://www.construction.am/companies/'
def E(hy,en,tax,form,yr,url): return {"name_hy":hy,"name_en":en,"tax_id":tax,"form":form,"registered_year":yr,"source_url":url}
R=[]
def add(dev,role,ents,fy,dl,pos,conf,notes,issues=None):
    R.append({"developer":dev,"role":role,"legal_entities":ents,"founded_year":fy,"datalex_names":dl,"news_issues":issues or [],"positives":pos,"confidence":conf,"notes":notes+NS})
add("New City Projects","developer",[E("ՆՅՈՒ ՍԻԹԻ ՊՐՈՋԵԿՏՍ","New City Projects",None,"ՍՊԸ",2019,"https://www.spyur.am/en/companies/new-city-projects-real-estate-development-company/51373/")],2019,
 ["ՆՅՈՒ ՍԻԹԻ ՊՐՈՋԵԿՏՍ","ՆՅՈՒ ՍԻԹԻ ՊՐՈՋԵՔԹՍ","ՆՅՈՒ ՍԻԹԻ ՓՐՈՋԵՔԹՍ"],
 [{"title":"Presented Armenian projects at International Property Show 2026, Dubai","url":"https://news.am/en/news/1060216","summary":"Director Vahe Davtyan presented residential projects/investment opportunities (per search snippet)."},
  {"title":"Member of the Association of Armenian Developers","url":"https://www.developers.am/hy-AM/members/?strapiId=42","summary":"Listed as association member."}],
 "medium","Yell.am lists «ՆՅՈՒ ՍԻԹԻ ՊՐՈՋԵԿՏՍ» ՍՊԸ; Spyur: est. 2019, director Vahe Davtyan, Tamrazyan 1/2 Yerevan; 16-50 employees; projects Novem, Pallada (Tsaghkadzor), Acharyan, Aria, Shinararner, Lotus Living. Tax ID not found. Individual projects (e.g. Pallada) may be held by separate SPV LLCs — not identified. Datalex worker already returned 0 cases for these spellings.")
add("Art-Residence","developer",[E("ԱՐԹ ՌԵԶԻԴԵՆՍ","Art-Residence","08281495","ՍՊԸ",2020,CA+"art-residence-developer-company/")],2020,
 ["ԱՐԹ ՌԵԶԻԴԵՆՍ","ԱՐԹ-ՌԵԶԻԴԵՆՍ","ԱՐՏ-ՌԵԶԻԴԵՆՍ"],
 [{"title":"Claims 150,000+ sqm completed","url":"https://artresidence.am/en/about","summary":"Company self-description; established 2020 under the name 'Art Group'."}],
 "high","Website footer: '© 2020-2026 ԱՐԹ ՌԵԶԻԴԵՆՍ ՍՊԸ'. construction.am: TIN 08281495, since 2020. Founder/board chairman Davit Abovyan; co-founder/CEO Nver Safaryan. Formerly named 'Art Group' (site also has an 'Արթ-Գրուպ ՍՊԸ' page) — old court cases could be under ԱՐԹ ԳՐՈՒՊ (too generic to queue). Note: construction.am's 'Feyt Bilt' entry links to the Art-Residence company page — likely a portal data error, but could indicate a relationship.")
fb_ent=[E("ՖԵՅԹ ԲԻԼԹ ՔՈՆՍԹՐԱՔՇՆ","Faith Built Construction",None,"ՍՊԸ",2018,"https://www.construction.am/arm/companies/faith-built-construction/")]
for dev in ["Feyt Bilt","Faith Built"]:
    add(dev,"developer",fb_ent,2018,["ՖԵՅԹ ԲԻԼԹ ՔՈՆՍԹՐԱՔՇՆ","ՖԵՅԹ ԲԻԼԴ ՔՈՆՍԹՐԱՔՇՆ","ՖԵՅԹ ԲԻԼԹ ՔՆՍԹՐԱՔՇՆ"],
     [{"title":"M.L. House premium complex, Monte Melkonyan 10","url":"https://tunmun.am/en/new/2536/","summary":"18-floor complex listed as Faith Built project."}],
     "medium","'Feyt Bilt' and 'Faith Built' are the same company (ՖԵՅԹ ԲԻԼԹ = transliteration; same info@faithbuilt.am). Registered name per construction.am/YouTube/bizratings: «ՖԵՅԹ ԲԻԼԹ ՔՈՆՍԹՐԱՔՇՆ» (kaռուցապատող ընկերություն), since 2018 (one directory says 2016). Tax ID not found. Short names ՖԵՅԹ ԲԻԼԹ/ԲԻԼԴ were already queued in main; here the full name was queued. faithbuilt.am did not resolve (DNS) on 2026-09-14. construction.am 'Feyt Bilt' entry points at the Art-Residence page (likely error).")
sh_ent=[E("ՇԱՄԱԽՅԱՆ","Shamakhyan",None,"ՍՊԸ",None,"https://myhome.am/en/building/140")]
for dev in ["Allur Dilijan (Shamakhyan )","SHAMAKHYAN"]:
    add(dev,"developer",sh_ent,None,["ՇԱՄԱԽՅԱՆ"],
     [{"title":"Abandoned Dilijan bakery to be reconstructed into ALLUR residential complex","url":"https://www.construction.am/news/802-allur-residential-complex-dilijan-armenia-storaket-studio/","summary":"Adaptive reuse of the former Tavush bread factory (13,000 m2) designed by Storaket studio."}],
     "medium","Same project/company: myhome.am building 140 names developer «ՇԱՄԱԽՅԱՆ» ՍՊԸ, Dilijan, Shamakhyan 1/2 (brand ALLUR, allur.am); sales outsourced to City Nest (sales@citynest.am). ՇԱՄԱԽՅԱՆ already queued in main (not repeated). Name equals the street name, so datalex hits must be checked for namesakes. Tax ID and owners not found. Planned completion June 2025 slipped to 09/2026 for block 2 (myhome.am) — schedule slip only, no dispute found.")
add("City Nest Property Management (sales agent)","sales agent",[E("ՍԻԹԻ ՆԵՍԹ","City Nest",None,"unknown",None,"https://citynest.am/en")],None,["ՍԻԹԻ ՆԵՍԹ","ՍԻԹԻ ՆԵՍՏ"],
 [{"title":"Sales/advisory for Movenpick Resort Tsaghkadzor, Milano Firenze Towers, Only One, Allur","url":"https://citynest.am/en","summary":"Outsourced sales, advisory and property management firm."}],
 "low","City Nest is a sales/advisory outsourcer, not the developer. Legal form/tax ID not found (site footer only '© 2023 City Nest'). Underlying developers: Milano Firenze Towers — Renco (Italian Renco group; Armenian entity not identified), Allur — «ՇԱՄԱԽՅԱՆ» ՍՊԸ; Only One, Mountain Village Dilijan, TM Tower, Nor Etch developers not identified. Queued names are a guess and may be too generic.")
add("APEX GM Developer","developer",[E("ՋԻ ԷՄ ԴԵՎԵԼՈՓԵՐ","GM Developer",None,"ՍՊԸ",2016,"https://apex-gm.am/%d5%b4%d5%a5%d6%80-%d5%b4%d5%a1%d5%bd%d5%ab%d5%b6/"),E("ՏՐԱՊԻԶՈՆ ՔՈՆՍԹՐԱՔՇՆ","Trapizon Construction",None,"ՍՊԸ",None,"https://firdus.am/")],2016,
 ["ՋԻ ԷՄ ԴԵՎԵԼՈՓԵՐ","ՋԻ ԷՄ ԴԻՎԵԼՈՓԵՐ","ՋԻ-ԷՄ ԴԵՎԵԼՈՓԵՐ","ՏՐԱՊԻԶՈՆ ՔՈՆՍԹՐԱՔՇՆ","ՏՐԱՊԻԶՈՆ ԿՈՆՍՏՐՈՒԿՑԻԱ"],
 [{"title":"Built Sos Sargsyan National Theatre (Gov. decision 2017 N1148-A)","url":"https://apex-gm.am/%d5%b4%d5%a5%d6%80-%d5%b4%d5%a1%d5%bd%d5%ab%d5%b6/","summary":"Company claims construction of the theatre and Amiryan 26/4 residential building."}],
 "high","apex-gm.am: «Ջի Էմ Դեվելոփեր» (APEX brand) founded 2016. firdus.am: construction permit for 33rd (Firdus) district issued to «ՏՐԱՊԻԶՈՆ ՔՈՆՍԹՐԱՔՇՆ» and «ՋԻ ԷՄ ԴԵՎԵԼՈՓԵՐ» ՍՊ ընկերություններ. construction.am lists main contractor for Firdus as ML Mining (queued in another group). The Firdus/33rd district redevelopment of historic old-Yerevan housing next to Republic Square has been publicly contested by heritage activists and residents in past years — NOT verified with a URL in this session; recommend manual check (news for 'Ֆիրդուս թաղամաս'). Tax IDs not found.")
add("New Arinj Residence","developer",[E("ՆՅՈՒ ԱՌԻՆՋ ՌԵԶԻԴԵՆՍ","New Arinj Residence",None,"unknown",None,"https://myhome.am/en/building/350")],None,
 ["ՆՅՈՒ ԱՌԻՆՋ ՌԵԶԻԴԵՆՍ","Ն.Ա. ՔՈՆՍԹՐԱՔՇՆ","ՆԱ ՔՈՆՍԹՐԱՔՇՆ"],[],"low",
 "myhome.am shows developer as 'Նյու Առինջ Ռեզիդենս' (brand-like, no legal form) for Arinj and also for Aldina Residence, Gulakyan 85 Arabkir. Contact email na.constructionllc2024@gmail.com suggests an 'N.A. Construction' LLC registered ~2024 — spelling guessed. No tax ID/website.")
ar_ent=[E("ԱՐԿԱԴԱ ՔՈՆՍԹՐԱՔՇՆ","Arcada Construction",None,"ՍՊԸ",1997,"https://arcada.am/?app=AppPage&page=about")]
for dev in ["Arcada","Arcada Construction"]:
    add(dev,"developer",ar_ent,1997,["ԱՐԿԱԴԱ ՔՈՆՍԹՐԱՔՇՆ","ԱՐԿԱԴԱ ԿՈՆՍՏՐՈՒԿՑԻԱ"],
     [{"title":"Long track record; publishes audited financial statements","url":"https://arcada.am/?app=AppPage&page=about","summary":"Founded 1997; site lists financial statements with independent audit opinion (2023) and bank partners (Ameriabank, IDBank, AEB, HSBC...)."}],
     "high","'Arcada' and 'Arcada Construction' are the same company: arcada.am — «Արկադա Քոնսթրաքշն» ՍՊԸ, founded 1997, exec. director Tigran Bayburtyan, office Davtashen 2nd bl. 17/14. Short ԱՐԿԱԴԱ already queued in main. Project emails asiamegastroy.am@mail.ru and info@sahakyanshin.com indicate partner/SPV companies (Asia Mega Stroy, Sahakyan Shin) for some projects (Davtashen 26/13, Panorama Dalma) — not verified. Ord Development lists info@arcada.am too (possible affiliation). Tax ID not found.")
add("Ord Development","developer",[E("ՕՐԴ ԴԵՎԵԼՈՓՄԵՆԹ","Ord Development","00112424","ՍՊԸ",2019,CA+"ord-development/")],2019,
 ["ՕՐԴ ԴԵՎԵԼՈՓՄԵՆԹ","ՕՐԴ ԴԻՎԵԼՈՓՄԵՆԹ","ՕՐԴ-ԴԵՎԵԼՈՓՄԵՆԹ"],
 [{"title":"Komitas Park district: 15 buildings, 1418 apartments, 221,000 m2","url":"https://www.construction.am/apartments-in-new-developments/komitas-park/","summary":"Large Arabkir project (Griboyedov 48), 50% sold per portal; Ord is developer and main contractor."}],
 "medium","construction.am: 'Ord Development' LLC, TIN 00112424, since 2019, head Levon Ordukhanyan, Mamikonyants 38/3. TIN format (leading 00) unusual — verify. Also listed with info@arcada.am, suggesting a link to Arcada Construction.")
add("Filishin","contractor",[E("ՖԻԼԻՇԻՆ","Filishin","07905342","ՍՊԸ",2005,CA+"filishin/")],2005,["ՖԻԼԻՇԻՆ"],
 [{"title":"Major contractor incl. works of national significance","url":"http://filishin.am/about/","summary":"Founded 2005 by Suren Hakobyan; site cites presidential palace and public/institutional works, audit by N-AUDIT LLC."},
  {"title":"Barekamutyun complex (5 buildings, 400 parking) completed 2023","url":"https://www.construction.am/apartments-in-new-developments/arabkir-barekamutyun-complex/","summary":"Listed as developer."}],
 "high","construction.am: 'Filishin' LLC, TIN 07905342, since 2007 (site says founded 2005), head Suren Hakobyan. Acts as developer for own residential projects and as large general contractor; shares phones/email (info@haekshin.am) with «ՀԱԷԿՇԻՆ» — affiliated group. Queued again with tax ID (name already in main).")
add("Nova Building","developer",[E("ՆՈՎԱ ԲԻԼԴԻՆԳ","Nova Building",None,"unknown",None,"https://novabuilding.am/"),E("ՀԱԷԿՇԻՆ","Haekshin",None,"ՓԲԸ",2004,"https://novabuilding.am/")],None,
 ["ՆՈՎԱ ԲԻԼԴԻՆԳ","ՆՈՎԱ ԲԻԼԴԻՆԳՍ","ՀԱԷԿՇԻՆ","ՀԱԵԿՇԻՆ"],
 [{"title":"Backed by Haekshin, ~250 projects since 2004","url":"https://novabuilding.am/","summary":"Nova Building (Paruyr Sevak 5/1, 17 floors, 3 blocks) names «ՀԱԷԿՇԻՆ» as partner; Haekshin claims ~250 projects since 2004."}],
 "low","The actual developer legal entity for Nova Building is not stated on novabuilding.am (site template also shows 'Baghramyan Residence'); only «ՀԱԷԿՇԻՆ» is named as partner (form ՓԲԸ per coordinator hint). Contacts overlap with Filishin (same phones +37410423272/428272). Queued brand name as a guess plus ՀԱԷԿՇԻՆ.")
add("Shin-Stroy House","developer",[E("ՇԻՆ-ՍՏՐՈՅ ՀԱՈՒՍ","Shin-Stroy House",None,"ՍՊԸ",2020,"https://shinstroyhouse.am/")],2020,["ՇԻՆ-ՍՏՐՈՅ ՀԱՈՒՍ","ՇԻՆ ՍՏՐՈՅ ՀԱՈՒՍ"],[],"high",
 "Website: «ՇԻՆ-ՍՏՐՈՅ ՀԱՈՒՍ» ՍՊԸ founded 2020; address Arinj/Duryan district; projects Duryan 2 (Avan, Duryan 5th st 56-58) and Wellstone (Nver Safaryan St 11/11). Tax ID not found. Small, young developer.")
add("Gevmik","developer",[E("ԳԵՎՄԻԿ","Gevmik","01222961","ՍՊԸ",1999,CA+"gevmik-llc/")],1999,["ԳԵՎՄԻԿ"],
 [{"title":"Several completed 14-storey complexes (Sebastia 3/3, Fuchik 1/3, Leningradyan 29/14)","url":"https://www.construction.am/apartments-in-new-developments/3-3-sebastia/","summary":"Long-running Yerevan developer/contractor since 1999."}],
 "high","construction.am: 'Gevmik' LLC, TIN 01222961, since 1999, head Hrayr Atanesyan, Gogol 38. Name already queued in main; re-queued with tax ID.")
add("Itarco Construction","developer",[E("ԻՏԱՐԿՈ ՔՈՆՍԹՐԱՔՇՆ","Itarco Construction",None,"ՓԲԸ",2002,CA+"itarco-construction-cjsc/")],2002,
 ["ԻՏԱՐԿՈ ՔՈՆՍԹՐԱՔՇՆ","ԻՏԱՐԿՈ ԿՈՆՍՏՐՈՒԿՑԻԱ","ԻԹԱՐԿՈ ՔՈՆՍԹՐԱՔՇՆ"],
 [{"title":"Paruyr Sevak 9 mixed-use building completed 2016","url":"https://www.construction.am/apartments-in-new-developments/zeytun-paruyr-sevak-9/","summary":"17-floor building with seismic isolation pads."}],
 "medium","construction.am slug 'itarco-construction-cjsc' => CJSC (ՓԲԸ); since 2002, head Burak Kirkoryan, Agatangeghos 2. Profile last updated 2023; no active projects. Armenian spelling guessed; tax ID not found.")
add("Nork Residential Complex","developer",[E("ՆՈՐՔ ԲՆԱԿԵԼԻ ՀԱՄԱԼԻՐ","Nork Residential Complex",None,"unknown",None,"https://myhome.am/en/building/316")],None,
 ["ՆՈՐՔ ԲՆԱԿԵԼԻ ՀԱՄԱԼԻՐ","ՆՈՐՔ ՌԵԶԻԴԵՆՇԱԼ ՔՈՄՓԼԵՔՍ"],[],"low",
 "myhome.am developer label 'Նորք բնակելի համալիր' (brand, no legal form) for Sero Khanzadyan 5/5, 131/9, 131/10 (completed 2016). Legal entity not identified; queued names are guesses.")
add("Gazavik","developer",[E("ԳԱԶԱՎԻԿ","Gazavik",None,"ՍՊԸ",None,"https://www.acba.am/hy/individuals/loans/mortgage/constructors#8981"),E("ՊՐՈՄ ԳՐՈՒՊ","Prom Group",None,"ՍՊԸ",2015,"https://promgroup.am/en/about-us/")],None,
 ["ՊՐՈՄ ԳՐՈՒՊ","ԿԱՊԻՏԱԼ ՊԱՐԿ"],
 [{"title":"Capital Park: 16 floors, 524 apartments, ACBA mortgage partner","url":"https://www.acba.am/hy/individuals/loans/mortgage/constructors#8981","summary":"Shirazi 2, Ajapnyak; commissioning 29.12.2026."}],
 "medium","Gazavik is the developer of Capital Park (Shirazi 2); ԳԱԶԱՎԻԿ already queued in main. Construction by Prom Group LLC (promgroup.am, founded 2015 by Hayk Hunanyan; 'we are building the complex where you bought an apartment'). Role of Prom Group = contractor/affiliate; queued ՊՐՈՄ ԳՐՈՒՊ and brand ԿԱՊԻՏԱԼ ՊԱՐԿ (latter may be generic). Tax IDs not found.")
add("Shinart Group","developer",[E("ՇԻՆԱՐՏ ԳՐՈՒՊ","Shinart Group","00921868","ՍՊԸ",2019,CA+"shinart-group/"),E("ՔՈՄՖՈՐԹ ԲԻԼԴ","Comfort Build",None,"ՍՊԸ",None,"https://comfortbuild.am/")],2019,
 ["ՇԻՆԱՐՏ ԳՐՈՒՊ","ՇԻՆԱՐՏ-ԳՐՈՒՊ","Ս.Կ. ԳՐՈՒՊ","ՔՈՄՖՈՐԹ ԲԻԼԴ"],
 [{"title":"Nazarbekyan Towers completed 2023 (385 apts); Evocabank partner","url":"https://www.construction.am/apartments-in-new-developments/ajapnyak-nazarbekyan-towers/","summary":"3 buildings, 7-21 floors; sales rep Comfort Build."}],
 "high","construction.am: 'Shinart Group' LLC, TIN 00921868, since 2019. Sales via Comfort Build LLC (info@comfortbuild.am). Evocabank list shows S.K. Group LLC (Leningradyan 27/6) with the same phone +374 33 400410 — likely affiliated; queued too.")
add("Up Development","developer",[E("ԱՓ ԴԵՎԵԼՈՓՄԵՆԹ","Up Development",None,"unknown",None,CA+"up-development/")],None,
 ["ԱՓ ԴԵՎԵԼՈՓՄԵՆԹ","ԱՊ ԴԵՎԵԼՈՓՄԵՆԹ","ԱՓ ԴԻՎԵԼՈՓՄԵՆԹ"],
 [{"title":"Sunday Towers, Arabkir: 6 buildings, 32,620 m2, completion 2027","url":"https://www.construction.am/apartments-in-new-developments/norakaruyc-arabkirum-sunday-towers/","summary":"Main contractor AAB Construction (AAB Project LLC); contact info@upd.am."}],
 "low","construction.am lists 'Up Development' (no legal form/TIN), G. Vardanyan 1a; our record's email info@archicon.am belongs to Archicon LLC (likely designer/marketing). Armenian spelling guessed.")
order=[x['developer'] for x in json.load(open(D+'group_B.json'))]
m={r['developer']:r for r in R}
missing=[o for o in order if o not in m]; extra=[k for k in m if k not in order]
assert not missing and not extra,(missing,extra)
json.dump([m[o] for o in order],open(D+'research_B.json','w'),ensure_ascii=False,indent=1)
print(len(order),'written')
