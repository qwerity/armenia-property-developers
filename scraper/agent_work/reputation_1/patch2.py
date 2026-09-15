import json
R=json.load(open('research_2.json'))
D=lambda n: next(r for r in R if r["developer"]==n)
K=lambda t: f"https://karg.am/company/{t}?lang=hy"
def setent(name,i,**kw): D(name)["legal_entities"][i].update(kw)

r=D("AM Group"); setent("AM Group",0,tax_id="00122941",registered_year=2013,source_url=K("00122941"))
r["datalex_tax_id"]="00122941"; r["founded_year"]=2013; r["confidence"]="medium"
r["notes"]=r["notes"].replace("Name 'AM Group' is generic (many unrelated AM Group entities exist); tax ID not found.","karg.am (e-register data) has a single «ԷՅ ԷՄ ԳՐՈՒՊ» ՍՊԸ, TIN 00122941, registered 09.04.2013, legal address V. Vagharshyan 24 (spyur operating address Yervand Kochar 8/2) - probable match, but role as developer is doubtful.")

r=D("Best Land"); setent("Best Land",0,tax_id="00181343",source_url=K("00181343")); setent("Best Land",1,tax_id="00000592",source_url=K("00000592"))
r["datalex_tax_id"]="00181343"
r["legal_entities"]+=[{"name_hy":"«Կապիտալ Բիլդ Պլյուս» ՍՊԸ","name_en":"Capital Build Plus LLC","tax_id":"03024803","form":"ՍՊԸ","registered_year":2020,"source_url":K("03024803")},
                      {"name_hy":"«Կապիտալ Բիլդ Մեկ» ՍՊԸ","name_en":"Capital Build One LLC","tax_id":"03024958","form":"ՍՊԸ","registered_year":2020,"source_url":K("03024958")}]
r["datalex_names"]=["ԿԱՊԻՏԱԼ ԲԻԼԴ","ԿԱՊԻՏԱԼ ԲԻԼԴ ՊԼՅՈՒՍ","ԿԱՊԻՏԱԼ ԲԻԼԴ ՄԵԿ"]
r["news_issues"].insert(3,{"date":"2024-06-26","title":"«Կապիտալ բիլդը» թերություններով է կառուցել շենքը, բնակիչները ամռան շոգին մնացել են առանց ջրի","url":"https://168.am/2024/06/27/2065851.html","summary":"Mediahub/168.am: residents say Capital Build delivered a building with construction defects, leaving them without water in summer heat."})
r["notes"]=r["notes"].replace("Tax ID not found in public sources checked (minfin lists, construction.am, spyur).","TIN 00181343 per karg.am (e-register data; legal address Komitas 19/1, reg. 21.05.2018 - matches e-register BO declaration). Subsidiary «ԵՐԵՎԱՆԻ ԼՈՒՍԱՏԵԽՆԻԿ» ԲԲԸ TIN 00000592 (Komitas 59). Tsaghkadzor SPVs «ԿԱՊԻՏԱԼ ԲԻԼԴ ՊԼՅՈՒՍ» (03024803) and «ԿԱՊԻՏԱԼ ԲԻԼԴ ՄԵԿ» (03024958), both Charents St. 36, Tsaghkadzor - likely group entities (name-based inference). Do not confuse with «ԿԱՊԻՏԱԼ ԲԻԼԴԻՆԳ» (08276205) or «ԲԻԼԴԻՆԳ ԿԱՊԻՏԱԼ» (00144692).")

r=D("4A Capital"); setent("4A Capital",0,source_url=K("00239045")); r["notes"]+=" karg.am confirms registered name «4Ա ԿԱՊԻՏԱԼ» ՍՊԸ, TIN 00239045, reg. 30.06.2021, Azatutyan Ave 12/2."

r=D("Renshin Urban Investments"); r["positives"].append({"title":"«Ռենշին» ընկերության պարտատոմսերը ցուցակվել են Հայաստանի ֆոնդային բորսայում","url":"https://tert.am/am/news/2026/07/14/renshin/4277308","summary":"July 2026: Renshin bonds listed on the Armenia Securities Exchange (AMX)."})

r=D("Seray Homes (Seray Developments)"); setent("Seray Homes (Seray Developments)",0,tax_id="02699477",registered_year=2019,source_url=K("02699477"))
r["datalex_tax_id"]="02699477"; r["founded_year"]=2019; r["confidence"]="high"
r["notes"]=r["notes"].replace("Spyur lists","karg.am (e-register data): «ՍԷՐԱՅ ՀՈՄԶ» ՍՊԸ, TIN 02699477, reg. 14.06.2019, active, legal address Paronyan 15/1. Spyur lists")

r=D("Defanse Housing Invest"); setent("Defanse Housing Invest",0,registered_year=2008,source_url=K("00449838"))
r["founded_year"]=2008
r["legal_entities"].append({"name_hy":"«Դեֆանս Հաուզինգ» (non-commercial/association-type entity)","name_en":"Defanse Housing","tax_id":"00515756","form":"other","registered_year":2023,"source_url":K("00515756")})
r["news_issues"]=[
 {"date":"2023-12-09","title":"«Ժողովուրդ». «Դեֆանս Հաուզինգ Ինվեստ» ՓԲԸ-ն ֆինանսական խնդիրներ ունի","url":"https://www.panorama.am/am/news/2023/12/09/Դեֆանս-Հաուզինգ-Ինվեստ/2937533","summary":"Zhoghovurd daily: citizens alerted that Defanse Housing Invest CJSC had accumulated large debts and has financial problems (also reported by lurer.com, yerkir.am)."},
 {"date":"2024-07-17","title":"Հրդեհ է բռնկվել «Դեֆանս Հաուզինգ»-ի նոր կառուցվող թաղամասում","url":"https://auroranews.am/news/2024-07-17-hrdeh-e-brnkvel-defans-hauzing-i-nor-karutsvogh-taghamasum","summary":"Fire broke out in the Defanse Housing district under construction."},
 {"date":"2026-09-11","title":"Շինհրապարակներում պատահարների թիվը աճում է․ վերջին 3,5 տարում 80 մարդ է մահացել","url":"https://hetq.am/hy/article/183861","summary":"Hetq: a worker fell to his death at the Defanse Housing site on 20 July 2026, and another serious fall occurred there the previous September; criminal proceedings opened on both; the Health and Labour Inspectorate had recorded violations at Defanse Housing Invest CJSC in May 2026."}]
r["positives"].append({"title":"Երևանում նոր թաղամաս է կառուցվում՝ «Դեֆանս Հաուզինգ»","url":"https://www.panorama.am/am/news/2022/10/17/Երևան-նոր-թաղամաս/2743739","summary":"Oct 2022 coverage of the launch of the Defanse Housing district."})
r["notes"]="karg.am (e-register data): «ԴԵՖԱՆՍ ՀԱՈՒԶԻՆԳ ԻՆՎԵՍՏ» ՓԲԸ, TIN 00449838, reg. 07.01.2008, legal address Erebuni (Arin Berd); same TIN in Ministry of Finance 2023 large/medium entity list. A second entity «ԴԵՖԱՆՍ ՀԱՈՒԶԻՆԳ» (TIN 00515756, reg. 21.02.2023, non-company legal form - likely residents' association/fund for the district) also exists. construction.am: CJSC building 140-ha district at Tichina 320. Serious issues: reported debts (2023) and fatal worksite accidents with criminal proceedings (2025-2026)."

r=D("ADA Tech"); r["legal_entities"][0]["source_url"]=K("00870486"); r["news_issues"].append({"date":"2014-02-07","title":"Հրդեհ Աճառյան փողոցում. այրվել է «Էյ դի էյ թեք» ընկերության տնակը","url":"https://168.am/2014/02/08/327729.html","summary":"Minor incident: an ADA Tech site cabin burned on Acharyan St."})

r=D("Piazza Grande")
r["legal_entities"]=[{"name_hy":"«Թարգեթ Գրուպ» ՓԲԸ","name_en":"Target Group CJSC (probable legal entity behind 'Target Development')","tax_id":"02710123","form":"ՓԲԸ","registered_year":2010,"source_url":K("02710123")},
 {"name_hy":"«Ռենկո Արմէստեյտ» ՍՊԸ","name_en":"Renco ArmEstate LLC","tax_id":"02560091","form":"ՍՊԸ","registered_year":2001,"source_url":"https://www.spyur.am/am/companies/renco-armestate/2840"},
 {"name_hy":"«Պիացցա Գռանդե» համատիրություն","name_en":"Piazza Grande condominium association","tax_id":"02597125","form":"համատիրություն","registered_year":2011,"source_url":K("02597125")}]
r["datalex_names"]=["ԹԱՐԳԵԹ ԳՐՈՒՊ","ԹԱՐԳԵԹ ԴԻՎԵԼՈՓՄԵՆՏ","ՌԵՆԿՈ ԱՐՄԷՍՏԵՅՏ"]; r["datalex_tax_id"]="02710123"
r["notes"]="Piazza Grande (Vazgen Sargsyan 10) is a completed 2010 Class-A mixed-use building constructed by RENCO (newsarmenia 2010) and managed/marketed by 'Target Development' (td.am; spyur brand «ԹԱՐԳԵԹ ԴԻՎԵԼՈՓՄԵՆՏ», founded 2010, offices in the building). No registered entity named Target Development found on karg.am; «ԹԱՐԳԵԹ ԳՐՈՒՊ» ՓԲԸ (TIN 02710123, reg. 23.11.2010, V. Sargsyan 10, property rental) and «ԹԱՐԳԵԹ ԶԱՐԳԱՑՄԱՆ ՀԻՄՆԱԴՐԱՄ» (02848256, same building) are the likely related entities - inference by address/name. «ՊԻԱՑՑԱ ԳՌԱՆԴԵ» (02597125, 2011) is the building's condominium association. Aug 2026: offices in the business centre were searched/sealed in connection with the Kocharyan criminal case (tenants, not the developer): https://www.pastinfo.am/hy/news/2026/08/25/574585858/1978725"
r["confidence"]="medium"

r=D("Ecoshin Group"); r["legal_entities"][0]["source_url"]=K("01274214")

r=D("IVY Garden  (PJKT Development)"); setent("IVY Garden  (PJKT Development)",0,tax_id="00523564",registered_year=2023)
r["datalex_tax_id"]="00523564"; r["founded_year"]=2023; r["confidence"]="high"
r["notes"]+=" karg.am: «ԱՅՎԻ ԳԱՐԴԵՆ» ՍՊԸ, TIN 00523564, reg. 18.12.2023, legal address Armenakyan 108/7 (matches project address)."

r=D("Deka (Deka 10 )"); setent("Deka (Deka 10 )",0,tax_id="00244843",registered_year=2021,source_url=K("00244843"))
r["legal_entities"].append({"name_hy":"«Դեկա Բիլդ» ՍՊԸ","name_en":"Deka Build LLC","tax_id":"08283061","form":"ՍՊԸ","registered_year":2024,"source_url":K("08283061")})
r["datalex_tax_id"]="00244843"; r["datalex_names"]=["ԴԵԿԱ 10","ԴԵԿԱ ԲԻԼԴ"]; r["confidence"]="high"
r["notes"]+=" karg.am: «ԴԵԿԱ 10» ՍՊԸ TIN 00244843 (reg. 22.10.2021) and «ԴԵԿԱ ԲԻԼԴ» ՍՊԸ TIN 08283061 (reg. 05.08.2024) share legal address Davtashen 1st district 30 - related entity."

r=D("Amikson Sapphire  (sales: RED Invest Group)"); setent("Amikson Sapphire  (sales: RED Invest Group)",0,tax_id="01260357",registered_year=2014)
r["datalex_tax_id"]="01260357"; r["founded_year"]=2014; r["confidence"]="high"; r["datalex_names"]=["ԱՄԻԿՍՈՆ ՍԱՊՖԻՐ","ԱՄԻԿՍՈՆ"]
r["notes"]+=" karg.am: «ԱՄԻԿՍՈՆ ՍԱՊՖԻՐ» ՍՊԸ TIN 01260357, reg. 23.01.2014 (Malatia-Sebastia). RED Invest Group's own entity «ՌԷԴ ԻՆՎԵՍԹ ԳՐՈՒՊ» ՍՊԸ TIN 01274206."

r=D("Modern Construction (sales: RED Invest Group)"); setent("Modern Construction (sales: RED Invest Group)",0,tax_id="00214038",registered_year=2019)
r["datalex_tax_id"]="00214038"; r["founded_year"]=2019; r["datalex_names"]=["ՄՈԴԵՐՆ ՔԸՆՍԹՐԱՔՇՆ","ՄՈԴԵՌՆ ՔԸՆՍԹՐԱՔՇՆ"]
r["notes"]=r["notes"].replace("Generic name - many similarly named entities likely; verify by tax ID.","karg.am: single exact match «ՄՈԴԵՐՆ ՔԸՆՍԹՐԱՔՇՆ» ՍՊԸ, TIN 00214038, reg. 06.12.2019, Mamikonyants St. 42 (Arabkir).")

r=D("House Construction  (sales: RED Invest Group)"); setent("House Construction  (sales: RED Invest Group)",0,tax_id="01332633",registered_year=2023)
r["datalex_tax_id"]="01332633"; r["founded_year"]=2023; r["confidence"]="high"
r["notes"]=r["notes"].replace("Tax ID not found;","karg.am: «ՀԱՈՒՍ ՔՈՆՍԹՐԱՔՇՆ» ՍՊԸ TIN 01332633, reg. 16.01.2023 (Ajapnyak, Vahagni district).")

r=D("Life House  (sales: RED Invest Group)"); setent("Life House  (sales: RED Invest Group)",0,tax_id="01088235",registered_year=2025)
r["datalex_tax_id"]="01088235"; r["founded_year"]=2025
r["notes"]=r["notes"].replace("Generic name; verify by tax ID.","karg.am: single match «ԼԱՅՖ ՀԱՈՒՍ» ՍՊԸ TIN 01088235, reg. 27.10.2025 (Nor Nork, Badal Muradyan 1) - very new company.")

r=D("Slavonic Residence (sales: RED Invest Group)"); setent("Slavonic Residence (sales: RED Invest Group)",0,tax_id="08250022",registered_year=2023)
r["datalex_tax_id"]="08250022"; r["founded_year"]=2023; r["confidence"]="high"
r["notes"]=r["notes"].replace("Tax ID not found;","karg.am: «ՍԼԱՎՈՆԱԿԱՆ ՌԵԶԻԴԵՆՍ» ՍՊԸ TIN 08250022, reg. 10.03.2023, legal address H. Emin 128 (matches project).")

r=D("My Home realty (sales: RED Invest Group)"); setent("My Home realty (sales: RED Invest Group)",0,tax_id="02285089",registered_year=2020)
r["datalex_tax_id"]="02285089"; r["founded_year"]=2020; r["confidence"]="high"
r["notes"]=r["notes"].replace("Tax ID not found;","karg.am: «ՄԱՅ ՀՈՄ ՌԻԵԼԹԻ» ՓԲԸ TIN 02285089, reg. 16.03.2020, status 'Չգործող' (inactive) - project completed 2022, company since inactive.")

r=D("Step Construction"); setent("Step Construction",0,tax_id="01366728",registered_year=2025,source_url=K("01366728"))
r["datalex_tax_id"]="01366728"
r["notes"]=r["notes"].replace("Legal form assumed ՍՊԸ; tax ID not found;","karg.am: «ՍՏԵՓ ՔՈՆՍԹՐԱՔՇՆ» ՍՊԸ TIN 01366728, reg. 25.08.2025 (Leningradyan St., Ajapnyak) - registration date is later than the brand's activity since 2022, so it may be a re-registered/successor entity; an older inactive «ՍՏԵՓ ԲԱՅ ՍՏԵՓ ԿՈՆՍԹՐԱՔՇՆ» (00521345) also exists. Medium match;")

r=D("ARM Construct"); r["legal_entities"][0].update(registered_year=2018,source_url=K("02688892"))
r["legal_entities"].append({"name_hy":"«Արմ Կոնստրակտ» համատիրություն (Komitas 60/3)","name_en":"Arm Construct condominium association","tax_id":"08312863","form":"համատիրություն","registered_year":2025,"source_url":K("08312863")})
r["founded_year"]=2018; r["datalex_names"]=["ԱՐՄ ԿՈՆՍՏՐԱԿՏ","ԱՐՄ ՔՈՆՍԹՐԱՔԹ"]
r["notes"]=r["notes"].replace("registered spelling uncertain, search both.","karg.am confirms registered spelling «ԱՐՄ ԿՈՆՍՏՐԱԿՏ» ՍՊԸ, TIN 02688892, reg. 11.12.2018 (legal address Hyusisayin Ave 5). Unrelated look-alikes: «ԱՐՄ - ԿՈՆՍՏՐԱԿՏ» (00245039), «ԱՐՄ ՔՈՆՍԹՐԱՔԹ» (04466927, Artimet).")
json.dump(R,open('research_2.json','w'),ensure_ascii=False,indent=1)
print('ok',len(R))
