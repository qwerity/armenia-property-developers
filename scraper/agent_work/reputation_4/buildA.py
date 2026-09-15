import json
names=[x['developer'] for x in json.load(open('group_A.json'))]
K='https://karg.am/company/{}?lang=hy'
RG='https://redgroup.am/projects/'
EV='https://www.evoca.am/hy/construction-companies'
def E(hy,en,tin,form,yr,src): return {"name_hy":hy,"name_en":en,"tax_id":tin,"form":form,"registered_year":yr,"source_url":src}
R={}
R['1SQ']=dict(role="developer",legal_entities=[E("«1ԷՍՔՅՈՒ-ԱՐԳՈ» ՍՊԸ","1SQ-Argo LLC","05018645","ՍՊԸ",2012,K.format("05018645")),
  E("«ՄԱՆ ԻՆՎԵՍՏ ԳՐՈՒՊ» ՍՊԸ","Man Invest Group LLC","03570825","ՍՊԸ",2023,EV),
  E("«ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ» ՍՊԸ","Dalan Technologies LLC","02832033","ՍՊԸ",2020,"https://cubeinvest.am/bond-issuance-conditions/dalan-technopark")],
  founded_year=2018,datalex_names=["1ԷՍՔՅՈՒ-ԱՐԳՈ","1ԷՍՔՅՈՒ ԱՐԳՈ","1SQ ARGO"],
  news_issues=[],
  positives=[{"title":"Construction/project manager of Dalan Technopark (154,000 m2, LEED/BOMA), financed by Ardshinbank","url":"https://hy.wikipedia.org/wiki/Դալան_տեխնոպարկ","summary":"Wikipedia and redgroup.am name 1SQ as the managing developer; builder D&S Construction; partner bank Ardshinbank."},
   {"title":"Evoca Bank partner developer (1ԷՍՔՅՈՒ-ԱՐԳՈ, Ashtarak Yerevanyan 2/10)","url":EV,"summary":"Evocabank lists «1ԷՍՔՅՈՒ-ԱՐԳՈ» ՍՊԸ as developer, sales via Argo Realty, phone +374 55 200 707."},
   {"title":"Portfolio of ~11 completed projects managed","url":"https://1-sq.am/","summary":"Site lists completed projects (Level 16, Isakov 12/11, Mikoyan 2/3, Tigran Mets 47/1, Halabyan 75/1, Silikyan Town House, Kechi etc.); in business since 2018."}],
  confidence="medium",
  notes="1SQ presents itself as project manager ('1SQ Estate Development'); each project uses its own permit-holder LLC which mostly could not be identified. «1ԷՍՔՅՈՒ-ԱՐԳՈ» ՍՊԸ (Ashtarak) is the confirmed developer for Ashtarak Yerevanyan 2/10 (Evoca list; registry reg. date 23.04.2012 per karg.am, possibly re-registration). 1SQ's phone +374 55 200 707 is the same number Evoca lists for «ՄԱՆ ԻՆՎԵՍՏ ԳՐՈՒՊ» ՍՊԸ (Kanakeravan, Nor Hachn) – strong link to the Man Invest Group brand (queued in main queue). Dalan Technopark owner/bond issuer is «ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ» ՍՊԸ (queued under '1SQ Estate Development'). Contractor on other projects per hints: «ԲԱՂՐԱՄՅԱՆՇԻՆ». Related «1ԷՍՔՅՈՒ ԿԱՀՈՒՅՔ ԵՎ ԴԻԶԱՅՆ» (01251674) and «1ԷՍՔՅՈՒ ԱԳՐՈ» (04439626) exist in registry. News search was not possible (WebSearch quota exhausted early in this run); no issues found in pages read.")
R['1SQ Estate Development (sales: RED Invest Group)']=dict(role="developer",legal_entities=[
  E("«ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ» ՍՊԸ","Dalan Technologies LLC","02832033","ՍՊԸ",2020,"https://cubeinvest.am/bond-issuance-conditions/dalan-technopark"),
  E("«1ԷՍՔՅՈՒ-ԱՐԳՈ» ՍՊԸ","1SQ-Argo LLC","05018645","ՍՊԸ",2012,K.format("05018645"))],
  founded_year=2018,datalex_names=["ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ","ԴԱԼԱՆ ՏԵԽՆՈԼՈԳԻԱՆԵՐ"],news_issues=[],
  positives=[{"title":"Dalan Technopark bonds registered by Central Bank of Armenia (AMD 2.5bn + USD 10m)","url":"https://cubeinvest.am/bond-issuance-conditions/dalan-technopark","summary":"Issuer «ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ» ՍՊԸ; prospectus registered by CBA 08.10.2025; placement by Cube Invest."},
   {"title":"Dalan Technopark financed by Ardshinbank; construction managed by 1SQ","url":RG+"bnakarankarucapatoxic-dalantechnologypark","summary":"redgroup.am: construction management by 1SQ Estate Development, designer Qproject, builder D&S construction, 2023-01 to 2026-08, partner bank Ardshininvestbank."}],
  confidence="high",
  notes="Same company group as '1SQ' (researched once). Dalan Technopark and Dalan Technopark Apartments (Tsitsernakaberd hwy 9/1). Issuer/owner entity «ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ» ՍՊԸ, ՀՎՀՀ 02832033, registered 23.09.2020, legal address V. Sargsyan 10 (Piazza Grande building) – the same building as «ԹԱՐԳԵԹ ԳՐՈՒՊ» ՓԲԸ (Target Development), suggesting a possible ownership link to Target Development (unverified). RED Invest Group is sales agent only.")
R['Posterum  (sales: RED Invest Group)']=dict(role="developer",legal_entities=[E("«ՊՈՍՏԵՌՈՒՄ» ՍՊԸ","Posterum LLC","02671144","ՍՊԸ",2017,K.format("02671144"))],
  founded_year=2017,datalex_names=["ՊՈՍՏԵՌՈՒՄ","ՊՈՍՏԵՐՈՒՄ"],news_issues=[],
  positives=[{"title":"Davinchi Club House project page","url":RG+"bnakarankarucapatoxic-davinci-club-house","summary":"Developer «Պոստեռում» ՍՊԸ, designer «Ռեֆորմ» ՍՊԸ, builder «Պրոֆ Մոնոլիտ» ՍՊԸ (08248357); project just started, completion 2029-12."}],
  confidence="high",
  notes="Armenian redgroup.am page gives «Պոստեռում» ՍՊԸ; registry (karg.am/e-register) ՊՈՍՏԵՌՈՒՄ 02671144, reg. 18.12.2017, legal address Hndkastani 2 = project site; activity property rental; 4 founders with 25% each. No completed residential track record found; no news found (news search limited).")
R['BULDOZER GROUP  (sales: RED Invest Group)']=dict(role="developer",legal_entities=[E("«ԲՈՒԼԴՈԶԵՐ ԳՐՈՒՊ» ՍՊԸ","Buldozer Group LLC","06950197","ՍՊԸ",2015,K.format("06950197")),
  E("«ՇԻՆՎԵԿՏՈՐ» ՍՊԸ (contractor)","Shinvector LLC","00178968","ՍՊԸ",2018,RG+"bnakarankarucapatoxic-heaven-heights")],
  founded_year=2015,datalex_names=["ԲՈՒԼԴՈԶԵՐ ԳՐՈՒՊ","ՇԻՆՎԵԿՏՈՐ"],news_issues=[],
  positives=[{"title":"Evoca Bank partner developer (High Park, G. Hovsepyan 58/15)","url":EV,"summary":"Evocabank list: developer «ԲՈՒԼԴՈԶԵՐ ԳՐՈՒՊ» ՍՊԸ, project High Park at Hovsepyan 58/15 (same site as Heaven Heights)."}],
  confidence="high",
  notes="redgroup.am Heaven Heights page: developer «ԲՈՒԼԴՈԶԵՐ ԳՐՈՒՊ» ՍՊԸ, designer «Արբակ և Որդիներ», builder «ՇԻՆՎԵԿՏՈՐ» ՍՊԸ, partner bank Evocabank, construction 2025-06 to end 2028. Registry: 06950197, reg. 20.04.2015, legal address Tashir (Lori), founders Alexander Kharin 50%, Armine Ghulyan 25%, Vahe Karapetyan 25%. Only one registry match. Evoca calls the project 'High Park' – project apparently renamed. No news found (news search limited).")
R['Advanced Development (sales: RED Invest Group)']=dict(role="developer",legal_entities=[E("«ԸԴՎԱՆՍԴ ԴԻՎԵԼԸՓՄԵՆԹ» ՍՊԸ","Advanced Development LLC","01545212","ՍՊԸ",2003,K.format("01545212"))],
  founded_year=2003,datalex_names=["ԸԴՎԱՆՍԴ ԴԻՎԵԼԸՓՄԵՆԹ","ԷԴՎԱՆՍԴ ԴԵՎԵԼՈՓՄԵՆԹ","ԱԴՎԱՆՍԴ ԴԵՎԵԼՈՓՄԵՆԹ"],news_issues=[],
  positives=[{"title":"Garunavan I-IV housing series with Tuscan architects","url":"https://www.garunavan.am/en/about-us","summary":"Villa and low-rise districts in Nor Nork/Bagrevand; Garunavan 2 and 3 completed; director Armen Khodabakhshyan."},
   {"title":"IDBank mortgage-partner developer (Garunavan 4)","url":"https://idbank.am/documents/IDBank%20constructors%20pptt.pdf","summary":"Listed by IDBank (found in earlier research run)."}],
  confidence="high",
  notes="redgroup.am Garunavan 4 page: developer «Ըդվանսդ Դիվելըփմենթ» ՍՊԸ, designer «Թոսքան» ՍՊԸ. Registry 01545212 (reg. 14.02.2003, Hanrapetutyan 22, construction of buildings). Datalex worker already returned 4 cases for this name set (check namesakes). No negative news found (limited search).")
R['Azurit (sales: RED Invest Group)']=dict(role="contractor",legal_entities=[E("«ԱԶՈՒՐԻՏ» ՍՊԸ","Azurit LLC","02621811","ՍՊԸ",2013,K.format("02621811")),
  E("«ՀԼ ՔՈՆՍՏՐԱՔՇՆ» ՍՊԸ (developer of Lumina)","HL Construction LLC","00515687","ՍՊԸ",2023,RG+"bnakaran-karucapatoxic-lumina")],
  founded_year=2013,datalex_names=["ԱԶՈՒՐԻՏ","ՀԼ ՔՈՆՍՏՐԱՔՇՆ","ՀԼ ԿՈՆՍՏՐՈՒԿՑԻԱ"],news_issues=[],
  positives=[{"title":"Builder of Amikson Sapfir project (Juventus-branded Sapfir)","url":RG+"bnakarankarucapatoxic-sapfir","summary":"redgroup.am: developer «Ամիկսոն Սապֆիր» ՍՊԸ, builder «Ազուրիտ» ՍՊԸ."},
   {"title":"Lumina Residence partner bank Ameriabank","url":RG+"bnakaran-karucapatoxic-lumina","summary":"Lumina (Hovsepyan 58/9): developer «ՀԼ ՔՈՆՍՏՐԱՔՇՆ» ՍՊԸ, partner bank Ameriabank."}],
  confidence="medium",
  notes="redinvest.am English text says 'Developer: Azurit' for Lumina Residence, but the Armenian redgroup.am page names «ՀԼ ՔՈՆՍՏՐԱՔՇՆ» ՍՊԸ as developer; Azurit appears elsewhere as builder (Շինարար) – so Azurit is most likely the construction contractor and HL Construction the permit holder. Registry: AZURIT LLC 02621811 (Baghramyan 2, specialized construction, reg. 2013); ՀԼ ՔՈՆՍՏՐԱՔՇՆ 00515687 (Suvorov 69, reg. date 17.02.2023 per karg.am). Datalex worker returned 7 cases for ԱԶՈՒՐԻՏ – check for inactive namesake «ԱԶՈՒՐԻՏ-Մ» (04216477).")
R['Avan Residence (sales: RED Invest Group)']=dict(role="developer",legal_entities=[E("«ԱՎԱՆ ՌԵԶԻԴԵՆՍ» ՍՊԸ","Avan Residence LLC","01334037","ՍՊԸ",2023,K.format("01334037")),
  E("«ՄԱԼԽԱՍՅԱՆՇԻՆ» ՍՊԸ (contractor)","Malkhasyanshin LLC","01263123","ՍՊԸ",2014,RG+"bnakaran-karucapatoxic-avanresidence")],
  founded_year=2023,datalex_names=["ԱՎԱՆ ՌԵԶԻԴԵՆՍ","ՄԱԼԽԱՍՅԱՆՇԻՆ","ՄԱԼԽԱՍՅԱՆ ՇԻՆ"],news_issues=[],positives=[],
  confidence="high",
  notes="redgroup.am: developer «Ավան Ռեզիդենս» ՍՊԸ, builder «Մալխասյան Շին» ՍՊԸ (Mher Mkrtchyan 17). Registry: ԱՎԱՆ ՌԵԶԻԴԵՆՍ 01334037, sole founder Tigran Malkhasyan, legal address Silikyan 5th st. 52/4 – same address as «ՄԱԼԽԱՍՅԱՆ ՀՈԼԴԻՆԳ» (01341239); contractor MALKHASYANSHIN 01263123 at Silikyan 5th st. 52 (founder Marina Vardanyan) – i.e. a Malkhasyan family group. No news found (limited search).")
R['Tida 23 (sales: RED Invest Group)']=dict(role="developer",legal_entities=[E("«ՏԻԴԱ 2023» ՍՊԸ","Tida 2023 LLC","01058751","ՍՊԸ",2023,K.format("01058751"))],
  founded_year=2023,datalex_names=["ՏԻԴԱ 2023","ՏԻԴԱ-2023"],news_issues=[],
  positives=[{"title":"The Hill Residence partner bank Ameriabank","url":RG+"bnakaran-karucapatoxic-thehill","summary":"Developer «Տիդա 2023» ՍՊԸ, construction start Jan 2024; partner bank Ameriabank."}],
  confidence="high",
  notes="Display name 'Tida 23' is a truncation of «Տիդա 2023» ՍՊԸ (redgroup.am). Registry 01058751, reg. 22.08.2023, Nor Nork. Single-project SPV, no track record found; inactive older «ՏԻԴԱ» (00250845) is a different company.")
R['New Home  (sales: RED Invest Group)']=dict(role="developer",legal_entities=[E("«ՆՅՈՒ ՀՈՄ» ՍՊԸ","New Home LLC","00210956","ՍՊԸ",2019,K.format("00210956"))],
  founded_year=2019,datalex_names=["ՆՅՈՒ ՀՈՄ"],
  news_issues=[{"date":"2026","title":"2 enforcement proceedings listed (CESA) for ՆՅՈՒ ՀՈՄ","url":K.format("00210956"),"summary":"karg.am company card shows 2 compulsory-enforcement (ԴԱՀԿ) proceedings for tax ID 00210956; nature/amount unknown – verify on cesa.am/datalex."}],
  positives=[{"title":"Completed Davtashen 2nd district 22/2 building (07/2020-12/2021)","url":RG+"bnakarankarucapatoxic-davitashenum","summary":"redgroup.am: developer «Նյու Հոմ» ՍՊԸ, completed project marketed with RED Invest Group."}],
  confidence="high",
  notes="Name already queued in queue_main.jsonl (not re-queued). Registry 00210956, legal address Davtashen 2nd district 22/2 (= the project), sole founder Bagrat Khachatryan. Same company as 'New Home' in other groups.")
R['Lorida Group']=dict(role="developer",legal_entities=[E("«ԼՈՐԻԴԱ ԳՐՈՒՊ» ՍՊԸ","Lorida Group LLC","02833894","ՍՊԸ",2020,K.format("02833894"))],
  founded_year=2020,datalex_names=["ԼՈՐԻԴԱ ԳՐՈՒՊ"],news_issues=[],
  positives=[{"title":"Shushi Palace complex (8 buildings), Ajapnyak Nazarbekyan 44/13, completed 2023","url":"https://www.construction.am/arm/apartments-in-new-developments/ajapnyak-nazarbekyan-44-13/","summary":"construction.am lists developer Lorida Group, status completed 2023."}],
  confidence="high",
  notes="Only registry match: ԼՈՐԻԴԱ ԳՐՈՒՊ 02833894 (Nork-Marash, Verin Antarayin 17), founders Hrag Samuel Salibyan 60%, Khanik Petrosyan 40%. karg.am reg. date 24.11.2020 (may be re-registration since Shushi Palace predates). Map item's phone/email are RED Invest's (sales agent). No news found (limited search).")
R['L Zara']=dict(role="developer",legal_entities=[E("«Լ ԶԱՌԱ» ՍՊԸ","L Zara LLC","02691408","ՍՊԸ",2019,K.format("02691408")),
  E("«ՄՈՍՍ ԳՐՈՒՊ» ՍՊԸ (designer/construction company)","Moss Group LLC","00466044","ՍՊԸ",2015,RG+"bnakarankarucapatoxic-hanrapetutyan")],
  founded_year=2019,datalex_names=["Լ ԶԱՌԱ","ԷԼ ԶԱՌԱ","Լ-ԶԱՌԱ","ՄՈՍՍ ԳՐՈՒՊ"],
  news_issues=[{"date":"2026","title":"Developer company inactive; 1 enforcement proceeding listed","url":K.format("02691408"),"summary":"Registry shows «Լ ԶԱՌԱ» (02691408) status 'Չգործող' (inactive/liquidated) with 1 CESA enforcement proceeding. Project Hanrapetutyan 61 was reported completed 04/2022, so dissolution after completion is plausible (SPV)."}],
  positives=[{"title":"Hanrapetutyan 61 building completed (06/2021-04/2022)","url":RG+"bnakarankarucapatoxic-hanrapetutyan","summary":"36 apartments; developer «Լ Զառա» ՍՊԸ, construction company «ՄՈՍՍ Գրուպ» ՍՊԸ."}],
  confidence="high",
  notes="Registry founders Harutyun Badajyan 50%, John Farkhoyan 50%; legal address Demirchyan 36. Moss Group 00466044 (Erebuni, founder Tereza Melkonyan). Buyer-warranty claims against a dissolved SPV may be hard to pursue.")
R['Art Company']=dict(role="developer",legal_entities=[E("«ԱՐՏՔՈՄՓԱՆԻ» ՍՊԸ","ArtCompany LLC","00117212","ՍՊԸ",2012,K.format("00117212")),
  E("«ԱԿՆ ՔՈՆՍԹՐԱՔՇՆ» ՍՊԸ","AKN Construction LLC","02637648","ՍՊԸ",2015,K.format("02637648"))],
  founded_year=2012,datalex_names=["ԱԿՆ ՔՈՆՍԹՐԱՔՇՆ"],
  news_issues=[{"date":"2025-07-11","title":"Company 'official clarification' responding to negative user reviews","url":"https://artco.am/","summary":"artco.am news item 'Պաշտոնական պարզաբանում' says critical opinions about the company have appeared on public platforms; full text loads via AJAX and could not be read – the underlying complaints are unverified."}],
  positives=[{"title":"Large/medium taxpayer publishing audited financial statements (2021-2024)","url":"https://artco.am/","summary":"Audited statements posted on site; «ԱՐՏՔՈՄՓԱՆԻ» 00117212 in MinFin large/medium organisations list."},
   {"title":"Multiple completed complexes (Forest, Leningradyan, Crane, Ani)","url":"https://karucapatoxic.am/en/88","summary":"8 projects in our data, 3 completed; ongoing Gyurjyan Cascade, Firdus Prime, Ani Premium."}],
  confidence="high",
  notes="«ԱՐՏՔՈՄՓԱՆԻ» already queued in queue_main.jsonl; only «ԱԿՆ ՔՈՆՍԹՐԱՔՇՆ» (acceptance act on artco.am, same legal address Tsitsernakaberd hwy 8/3) queued here. Registry founders Hirant Kurtyan 60%, Vahe Petrosyan 40% (matches site). Contractor per hints: «ՄԼԼ ԻՆԴԱՍԹՐԻԱԼ». See also 'Levon Amirkhanyan' record: its construction.am listing carries Art Company's phone (+374 15 333000) and artcompany.marketing email, suggesting Art Company took over / markets the stalled Khanjyan 29 site (unverified).")
R['Levon Amirkhanyan']=dict(role="developer",legal_entities=[E("«ԼԵՎՈՆ ԱՄԻՐԽԱՆՅԱՆ» ՍՊԸ","Levon Amirkhanyan LLC","00837356","ՍՊԸ",1998,K.format("00837356")),
  E("«ՎԵՆԵՑԻԱ ՊԼԱԶԱ» ՍՊԸ (related)","Venetsia Plaza LLC",None,"ՍՊԸ",None,"https://hetq.am/hy/article/58622")],
  founded_year=1998,datalex_names=["ԼԵՎՈՆ ԱՄԻՐԽԱՆՅԱՆ","ՎԵՆԵՑԻԱ ՊԼԱԶԱ","ԲՐԵԴՎԵԼ ԻՆՎԵՍՏՄԵՆՏՍ"],
  news_issues=[{"date":"2015-02-19","title":"Մահացած գործարարը գրավադրել էր բնակիչների բնակարանները (Deceased businessman had mortgaged residents' apartments)","url":"https://hetq.am/hy/article/58622","summary":"After director Abram (Hamlet) Amirkhanyan's death (16.02.2015), buyers at Sayat-Nova 40, Khanjyan 29, Charents 70/8, Vardanants 69 alleged their pre-paid apartments had been pledged to banks (incl. Ardshinbank) without their knowledge; alleged fraud/money laundering; linked companies «ՎԵՆԵՑԻԱ ՊԼԱԶԱ», «ՈՒՐՄ», «Ագրոպետրոլ սերվիս», Bredwell Investments Corp."},
   {"date":"2017-2024","title":"Khanjyan 29 construction halted; company activity terminated","url":"https://www.construction.am/arm/apartments-in-new-developments/khanjyan-st-29/","summary":"construction.am: Khanjyan 29 status 'Դադարեցված' (suspended), note 'Կազմակերպության գործունեությունը դադարեցված է'; registry shows «ԼԵՎՈՆ ԱՄԻՐԽԱՆՅԱՆ» 00837356 inactive."},
   {"date":"","title":"Khanjyan 29/1 building reported as a hazard (drug users, garbage)","url":"https://news.am/arm/news/855924.html","summary":"news.am article (title via search; page blocked 403, date unknown) on the abandoned Khanjyan 29/1 building."}],
  positives=[{"title":"Charents 70/8, Lvovyan 14/1, Vardanants 69 listed as completed (2017-2018)","url":"https://www.construction.am/arm/apartments-in-new-developments/charents-street-70-8/","summary":"construction.am shows the other three buildings completed."}],
  confidence="high",
  notes="SERIOUS: legacy developer, company inactive, stalled Khanjyan 29 and mortgage/fraud allegations (2015). Registry: ԼԵՎՈՆ ԱՄԻՐԽԱՆՅԱՆ 00837356, reg. 1998, inactive. Our map shows Khanjyan 29 with 132 apts, exploitation 12/2027 and Art Company contact data – the site appears to have been revived, probably by Art Company (not verified); beware that the 'developer' label on our map is stale.")
milon=dict(role="developer",legal_entities=[E("«ՄԻԼՈՆ ՄԱՅՆԻՆԳ» ՍՊԸ","Milon Mining LLC","01540483","ՍՊԸ",2001,K.format("01540483"))],
  founded_year=None,datalex_names=[],news_issues=[],
  positives=[{"title":"Three large projects in Abovyan/Arinj (Milon Tower 400 apts, Milon Hills, Milon Plaza 168 apts)","url":"https://myhome.am/en/building/239","summary":"myhome.am and milonmining.am list projects; Milon Plaza started 2021-22."}],
  confidence="medium",
  notes="«ՄԻԼՈՆ ՄԱՅՆԻՆԳ» already queued in queue_main.jsonl – not re-queued. Registry single match 01540483, legal address Arinj B district 1st st. 1/1 (next to Milon Hills), karg.am reg. date 05.09.2001 (may be re-registration). 'Milon Mining' and 'MILON MINING' are the same company – researched once. milonmining.am is a JS app; no owner/about text retrievable. News search not possible (WebSearch quota exhausted); none found.")
R['Milon Mining']=milon
R['MILON MINING']=dict(milon)
R['ML MINING']=dict(role="developer",legal_entities=[E("«ՄԼ ՄԱՅՆԻՆԳ» ՍՊԸ","ML Mining LLC","02569362","ՍՊԸ",2003,K.format("02569362")),
  E("«ՄԼ ՄԱՅՆԻՆԳ ՔՈՆՍԹՐԱՔՇՆ» ՍՊԸ","ML Mining Construction LLC","00229929","ՍՊԸ",2020,K.format("00229929"))],
  founded_year=2008,datalex_names=[],
  news_issues=[{"date":"2023-06-16","title":"ML Mining denies reports of bankruptcy proceedings","url":"https://www.araratnews.am/show/85128","summary":"oragir.news reported ML Mining and its owner in bankruptcy; company denied (owner David Sukiasyan), no evidence bankruptcy proceeded."},
   {"date":"2026","title":"2 enforcement proceedings listed (CESA)","url":K.format("02569362"),"summary":"karg.am shows 2 ԴԱՀԿ enforcement proceedings for 02569362; details unknown."}],
  positives=[{"title":"Large taxpayer (TOP-1000) and state urban-development partner","url":"https://tech.news.am/rus/news/3958/ml-mining-realizuet-sovmestno-s-gosudarstvom-tri-krupniykh-gradostroitelniykh-proekta.html","summary":"Three big projects with the state; Ardshinbank partner; public-servant housing at Adonts 19/8."}],
  confidence="high",
  notes="Names already queued in queue_main.jsonl (ՄԼ ՄԱՅՆԻՆԳ) – not re-queued. Findings reused from earlier research run (reputation_1) and karg.am. Armavir H. Baghramyan 39 project; also contractor for «ԱԲՈՎՅԱՆ ՍԻԹԻ ՀԱՈՒՍ». Not related to Milon Mining (different registry entities).")
R['Kamertoon']=dict(role="developer",legal_entities=[E("«ԿԱՄԵՐՏՈՒՆ» ՍՊԸ","Kamertoon LLC","00484465","ՍՊԸ",2019,K.format("00484465")),
  E("«ԿԱՄԵՐՏՈՒՆ ԴԵՎԵԼՈՓՄԵՆԹ» ՍՊԸ","Kamertoon Development LLC","02951315","ՍՊԸ",2026,K.format("02951315"))],
  founded_year=2019,datalex_names=["ԿԱՄԵՐՏՈՒՆ","ԿԱՄԵՐՏՈՒՆ ԴԵՎԵԼՈՓՄԵՆԹ"],news_issues=[],
  positives=[{"title":"BREEAM-certified premium multifunctional complex next to Parajanov Museum","url":"https://kamertoon.am/about-us/","summary":"Architects Proforma Studio; co-founders Suren Pahlevanyan (CEO) and David Tavadian."}],
  confidence="high",
  notes="Registry: ԿԱՄԵՐՏՈՒՆ 00484465, legal address Parajanov 8 land plot, founders Suren Pahlevanyan 50%, Hasmik Pahlevanyan 50% (matches site's CEO). A new «ԿԱՄԵՐՏՈՒՆ ԴԵՎԵԼՈՓՄԵՆԹ» (02951315) registered 03.07.2026 at the same address. Unrelated inactive «ԿԱՄԵՐՏՈՆ» companies exist – spelling ՈՒՆ vs ՈՆ matters. No news found (limited search).")
R['Target Development']=dict(role="developer",legal_entities=[E("«ԹԱՐԳԵԹ ԳՐՈՒՊ» ՓԲԸ","Target Group CJSC","02710123","ՓԲԸ",2010,K.format("02710123")),
  E("«ԹԱՐԳԵԹ ԴԻՎԵԼՈՓՄԵՆՏ» (brand as on Spyur)","Target Development",None,"unknown",2010,"https://www.spyur.am/en/companies/target-development/7271/")],
  founded_year=2010,datalex_names=["ԹԱՐԳԵԹ ԳՐՈՒՊ","ԹԱՐԳԵԹ ԴԻՎԵԼՈՓՄԵՆՏ","ԹԱՐԳԵԹ ԴԵՎԵԼՈՓՄԵՆԹ"],news_issues=[],
  positives=[{"title":"Developer/manager of Piazza Grande premium mixed-use complex near Republic Square","url":"https://www.spyur.am/en/companies/target-development/7271/","summary":"Spyur: founded 2010, manages premium office/residential/retail property in Yerevan; office at Piazza Grande (V. Sargsyan 10)."}],
  confidence="medium",
  notes="Spyur lists «ԹԱՐԳԵԹ ԴԻՎԵԼՈՓՄԵՆՏ» but no registry company of that name exists; the registry entity at the same address (V. Sargsyan 10, offices 6-7) is «ԹԱՐԳԵԹ ԳՐՈՒՊ» ՓԲԸ 02710123 (reg. 23.11.2010, property rental/management) – matched by address and year; also «ԹԱՐԳԵԹ ԶԱՐԳԱՑՄԱՆ ՀԻՄՆԱԴՐԱՄ» (Target Development Foundation, 02848256) at the same address. «ԴԱԼԱՆ ԹԵՔՆՈԼՈՋԻՍ» and «ՍԱԼՍԱ ԴԻՎԵԼՈՓՄԵՆԹ» are also registered in the Piazza Grande building – possible group link. td.am blocked (mod_security) to direct fetch.")
R['Club House Yerevan']=dict(role="unknown",legal_entities=[],founded_year=None,datalex_names=["ՔԼԱԲ ՀԱՈՒՍ ԵՐԵՎԱՆ","ՔԼԱԲ ՀԱՈՒՍ"],news_issues=[],positives=[],
  confidence="low",
  notes="Project name used as developer name (Tigran Mets 33/2, 30 apartments). Contact +374 91 002144, Safaryandevid@gmail.com (suggests a person named Devid/David Safaryan). No registry company named ՔԼԱԲ ՀԱՈՒՍ found on karg.am; dignisi/novostroiki pages do not name the legal entity. Queued project name as a fallback only.")
R['Hay Develop']=dict(role="unknown",legal_entities=[],founded_year=None,datalex_names=["ՀԱՅ ԴԵՎԵԼՈՓ","ՀԱՅ ԴԻՎԵԼՈՓ"],news_issues=[],positives=[],
  confidence="low",
  notes="HAY VIEW project (H. Emin 1st alley, plot 23, Arabkir; completion 2028-04). No registry company matching ՀԱՅ ԴԵՎԵԼՈՓ / ՀԱՅ ԴԻՎԵԼՈՓ / ՀԱՅ ԴԻՎԵԼԸՓ on karg.am; the brand may be a trade name of an unidentified LLC. Queued plausible spellings with low confidence.")
R['GM Development']=dict(role="developer",legal_entities=[E("«ՋԻ ԷՄ ԴԻՎԵԼԸՓՄԵՆԹ» ՍՊԸ","GM Development LLC","02885352","ՍՊԸ",2023,K.format("02885352"))],
  founded_year=2023,datalex_names=["ՋԻ ԷՄ ԴԻՎԵԼԸՓՄԵՆԹ","ՋԻ ԷՄ ԴԵՎԵԼՈՓՄԵՆԹ"],news_issues=[],
  positives=[{"title":"Evoca Bank partner developer (PARK VIEW, Ghapantsyan 4/9)","url":EV,"summary":"Evocabank lists PARK VIEW, developer «ՋԻ ԷՄ ԴԻՎԵԼԸՓՄԵՆԹ» ՍՊԸ, tel +374 55 094949."}],
  confidence="high",
  notes="Registry 02885352, reg. 24.02.2023, Sayat-Nova 19, founders Ruben Alaverdyan 50%, Vyacheslav Drugov 50%. Not to be confused with «ՋԻ ԷՄ ԻՆՎԵՍՏ» (00222163). Young single-project company; no news found (limited search).")
out=[]
for n in names:
    r=R[n]; d={"developer":n}; d.update(r); out.append(d)
json.dump(out,open('research_A.json','w'),ensure_ascii=False,indent=1)
print(len(out),'written; missing:',[n for n in names if n not in R])
