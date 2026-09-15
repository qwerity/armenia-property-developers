import json

OUT = '/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.work/reputation_3/web_C.json'


def K(tid):
    return f'https://karg.am/company/{tid}?lang=hy'


def ent(hy, en, tid, form, yr, src):
    return {"name_hy": hy, "name_en": en, "tax_id": tid, "form": form, "registered_year": yr, "source_url": src}


def rec(dev, role, ents, founded, dl, issues, pos, conf, notes):
    return {"developer": dev, "role": role, "legal_entities": ents, "founded_year": founded,
            "datalex_names": dl, "tax_ids": [e["tax_id"] for e in ents if e["tax_id"]],
            "news_issues": issues, "positives": pos, "entity_confidence": conf, "notes": notes}


METTA_ENT = ent("«Մետտա Գրուպ» ՍՊԸ", "METTA GROUP LLC", "00092629", "ՍՊԸ", 2007, K("00092629"))
METTA_NOTES = ("newkomitas.am names «Մետտա Գրուպ» ՍՊԸ as builder; evoca.am lists \"METTA GROUP\" LLC at H. Arghutyan 15/8, 15/10. "
               "karg.am (e-register data): ՄԵՏՏԱ ԳՐՈՒՊ ՀՎՀՀ 00092629, active, legal address Arghutyan St 10 Arabkir, registration date shown 01.04.2007, "
               "founders incl. Vladimir Gasparyan (37%) and Georgi Gasparyan (25%). Spyur (spyur.am/metta) lists the same LLC, foreign-owned, est. 2005, "
               "classified as building-materials/mining manufacturer. A YouTube clip links the name to the former Vanadzor 'Prometey Khimprom' plant (unverified). "
               "Do not confuse with ՄԵՏԱ ԳՐՈՒՊ (single Տ, 02301503). Site claims 100,000+ m2 built in Sochi (not independently verified). "
               "Developer-wide news search was curtailed: session WebSearch budget exhausted.")
METTA_POS = [{"title": "New Komitas: ~3,200-apartment district on Arghutyan St, Arabkir", "url": "https://newkomitas.am/",
              "summary": "Company's own site presents a 20-building, 18-storey district with school/kindergarten and underground parking, completion 2027."},
             {"title": "Listed as developer partner on Evoca Bank construction-company list", "url": "https://www.evoca.am/en/construction-companies#22-metta-group-llc",
              "summary": "Evoca Bank lists METTA GROUP LLC among construction companies for its mortgage programme."}]

R = [
    rec("Alliance 64", "developer",
        [ent("«Ալիանս 64» ՍՊԸ", "ALLIANCE 64 LLC", "00203152", "ՍՊԸ", 2019, K("00203152"))],
        None, ["Ալիանս 64", "Ալյանս 64", "Ալիանս Ինվեստմենթ"], [],
        [{"title": "Alliance Plaza (Fuchik 1/1, 291 apartments) and Alliance Park (Sarmen 88)", "url": "https://allianceinvestment.am/",
          "summary": "Brand 'Alliance Investment' (same phone/email alliance64@icloud.com) presents two completed Yerevan residential projects."}],
        "medium",
        "Brand name matches registry entry ԱԼԻԱՆՍ 64 (ՀՎՀՀ 00203152, active, Arabkir, S. Abgar Tagavori St 73; NACE L68.20 renting own property) on karg.am; registration date shown 20.05.2019 may be a re-registration since Alliance Plaza is older. "
        "Consumer brand on website is 'Alliance Investment' - no LLC by that name tied to projects (ԱԼՅԱՆՍ ԻՆՎԵՍՏ 02270942 is an inactive food wholesaler, unrelated). No news search possible (WebSearch budget exhausted)."),
    rec("Metta Group", "developer", [METTA_ENT], 2005, ["Մետտա Գրուպ"], [], METTA_POS, "high", METTA_NOTES),
    rec("TOP BUILDINGS", "developer",
        [ent("«Թոփ Բիլդինգս» ՍՊԸ", "TOP BUILDINGS LLC", "01055684", "ՍՊԸ", 2023, K("01055684"))],
        2023, ["Թոփ Բիլդինգս", "Թոփ Բիլդինգ"], [], [],
        "high",
        "Website topbuildings.am uses Armenian name «Թոփ Բիլդինգս» and address Ashkhabad St 9/2, Avan; karg.am registry card ԹՈՓ ԲԻԼԴԻՆԳՍ ՀՎՀՀ 01055684 has the same legal address (Nor Nork district, Ashkhabadi 9/2), registered 02.06.2023, sole founder Artur Hayrapetyan. Young company with a single 16-storey project in progress. No news search possible (WebSearch budget exhausted)."),
    rec("Green Hills", "developer",
        [ent("«Գրին Հիլզ» ՍՊԸ", "GREEN HILLS LLC", "00485201", "ՍՊԸ", 2019, K("00485201"))],
        2019, ["Գրին Հիլզ"], [], [],
        "high",
        "greenhills.am footer: 'Գրին Հիլզ ՍՊԸ', office Antarayin 170, site David Bek 103/5. karg.am: ԳՐԻՆ ՀԻԼԶ ՀՎՀՀ 00485201, active, reg. 12.06.2019, legal address Nork 2nd St 42 (Nork-Marash), sole founder Ara Hayrapetyan. Only one registry entity of that name found. No news search possible (WebSearch budget exhausted)."),
    rec("ARMAT Realty", "sales agent",
        [ent("«Սագա Շին» ՍՊԸ", "SAGA SHIN LLC", "01300595", "ՍՊԸ", 2020, K("01300595")),
         ent("«Արմաթ» ՍՊԸ (broker, unconfirmed)", "ARMAT LLC", None, "ՍՊԸ", None, "https://www.americanaarmenia.com/")],
        None, ["Սագա Շին", "Արմաթ", "Արմատ Ռիելթի"], [],
        [{"title": "Americana Armenia gated community near Vahakni", "url": "https://www.americanaarmenia.com/",
          "summary": "Townhouse/apartment community marketed by ARMAT; site lists all properties as sold."}],
        "medium",
        "ARMAT is a real-estate agency/broker (agent Galust Avagyan); construction.am text says Armat Real Estate Agency acts jointly with Saga-Shin LLC. Builder SaGa-Shin: karg.am ՍԱԳԱ ՇԻՆ ՀՎՀՀ 01300595, active, reg. 27.02.2020, founders Khachatur Galstyan 50% (named as director on americanaarmenia.com) and Tigran Sahakyan 50% (named as NY developer) - strong match. "
        "ARMAT LLC itself not identified in registry: ԱՐՄԱԹ 02512833 (1995) is inactive; several ԱՐՄԱՏ* companies are unrelated. The 'Amelia Residence' (Davtyan 51) attribution from geoln.com is unverified."),
    rec("Cascade Hills", "developer",
        [ent("«Ալ Համռա Ռիել Իսթեյթ» ՍՊԸ", "AL HAMRA REAL ESTATE ARMENIA LLC", "01560249", "ՍՊԸ", 2007, K("01560249"))],
        2007, ["Ալ Համռա Ռիել Իսթեյթ", "Ալ Համրա Ռիել Էսթեյթ Արմենիա", "Կասկադ Հիլզ"], [],
        [{"title": "Cascade Hills gated complex, 10 buildings, Antarayin 160/5", "url": "https://www.construction.am/companies/cascade-hills/",
          "summary": "Project of UAE-based Al Hamra Real Estate (Ras Al Khaimah); first stone laid in August 2008, completed turnkey complex."}],
        "medium",
        "construction.am company page says Al Hamra Real Estate Developers set up Al Hamra Real Estate Armenia LLC (GM Haig Puzantian) to build Cascade Hills. karg.am: ԱԼ ՀԱՄՌԱ ՌԻԵԼ ԻՍԹԵՅԹ ՀՎՀՀ 01560249, reg. 31.05.2007, legal address Antarayin 160/5 (same as project), now INACTIVE (Չգործող). "
        "ԿԱՍԿԱԴ ՀԻԼԶ (02642389) is the residents' condominium (համատիրություն) at Antarayin 160/7, not the developer. Contact email royal.building.22@mail.ru suggests a current sales/management party - possibly ՌՈՅԱԼ ԲԻԼԴԻՆԳ ՍՊԸ (02853247, reg. 2022, founder Vahe Manukyan) - unconfirmed. A related non-resident entry ԱԼ ՀԱՄՌԱ ՌԻԵԼԹ ԻՍԹԵՅԹ ԴԻՎԵԼՈՓՄԵՆԹ ՍՊԸ (02889723) also exists."),
    rec("Eliteshin Group", "developer",
        [ent("«Էլիտշին Գրուպ» ՍՊԸ", "ELITESHIN GROUP LLC", "00488732", "ՍՊԸ", 2019, K("00488732"))],
        2019, ["Էլիտշին Գրուպ"], [], [],
        "medium",
        "karg.am: ԷԼԻՏՇԻՆ ԳՐՈՒՊ ՀՎՀՀ 00488732, active, reg. 19.12.2019, legal address Nubarashen A-1 district 19, sole founder Tigran Nersisyan - consistent with contact email gevorgyan.nersisyan@mail.ru. Project: Lvovyan Tower, Lvovyan 19/7 (Nor Nork). Similar-named but distinct: ԷԼԻՏՇԻՆ (02518289), ԷԼԻՏՇԻՆ-1 (01308005), ԷԼԻՏՇԻՆ 77 (02859802)."),
    rec("Kanach Tagh", "developer",
        [ent("«Կանաչ Թաղ» ՍՊԸ", "KANACH TAGH LLC", "02283032", "ՍՊԸ", 2019, K("02283032"))],
        None, ["Կանաչ Թաղ", "Ավետիսյան Էսթեյթ"], [], [],
        "low",
        "Brand = 'Kanach Tagh' townhouse district at Acharyan 37/27, Avan (4 three-storey buildings, finished). karg.am ԿԱՆԱՉ ԹԱՂ ՀՎՀՀ 02283032 (reg. 18.11.2019, Shengavit, Shiraki 74/2) is INACTIVE; founders Alina Vardanyan 67% / Manush Avetisyan 33% - surname Avetisyan matches contact email info@avetisyanestate.com, but link is not proven. "
        "ԿԱՆԱՉ ԹԱՂԱՄԱՍ (01078757, reg. 2025) at exactly Acharyan 37/27 building 4 is the residents' condominium, not the developer. Real developer may be an 'Avetisyan Estate' entity - not found."),
    rec("Lav-Sar", "developer",
        [ent("«Լավ-Սար» ՍՊԸ", "LAV-SAR LLC", "02588839", "ՍՊԸ", 2008, K("02588839"))],
        2008, ["Լավ-Սար", "Լավ Սար", "Ֆելիսիթի"], [],
        [{"title": "FeliCity Davtashen residential district (3rd block)", "url": "https://felicity.am/shenqer/felicity-davitashen/",
          "summary": "Multi-block FeliCity complex in Davtashen; construction.am lists the company as developer since 2008."}],
        "high",
        "construction.am Lav-Sar LTD: since 2008, Davtashen 3rd district 31/1. karg.am: ԼԱՎ-ՍԱՐ ՀՎՀՀ 02588839, active, reg. 01.04.2008, legal address Davtashen 3rd district 31/1 (exact match), NACE F41.20 building construction, sole founder Emin Yeghiazaryan. Note SIL Capital (02281157) founder is Vahagn Yeghiazaryan - possible family link, unverified."),
    rec("SIL Capital Construction", "developer",
        [ent("«Սիլ Կապիտալ» ՍՊԸ", "SIL CAPITAL LLC", "02281157", "ՍՊԸ", 2019, K("02281157"))],
        None, ["Սիլ Կապիտալ", "Սիլ Կապիտալ Կոնստրուկցիա"], [], [],
        "medium",
        "construction.am address 11/1 Smbat Zoravar St matches karg.am ՍԻԼ ԿԱՊԻՏԱԼ ՀՎՀՀ 02281157 (active, legal address Smbat Zoravar 11/1, Shengavit; reg. date shown 30.07.2019; NACE M70.22 management consulting; sole founder Vahagn Yeghiazaryan). No separate 'SIL Capital Construction' entity found in registry autocomplete. Project Davtyan 1/4 (finished)."),
    rec("Coordinate (Koordinat )", "developer",
        [ent("«Կոորդինատ» ՍՊԸ", "KOORDINAT LLC", "03554812", "ՍՊԸ", 2020, K("03554812"))],
        2020, ["Կոորդինատ"], [], [],
        "high",
        "coordinat.am: 'Կառուցապատող «Կոորդինատ» ՍՊԸ' for Black & White Residence, Tartu 1/1 Abovyan. karg.am ԿՈՈՐԴԻՆԱՏ ՀՎՀՀ 03554812 (03 prefix = Kotayk), active, reg. 05.08.2020, legal address Abovyan 4th microdistrict 53, sole founder Samvel Vardanyan. Different: ԿՈՈՐԴԻՆԱՏՈՐ (00466843, Erebuni), ԿՈՈՐԴԻՆԱՏ-Ա (inactive, Goris)."),
    rec("Metta Group (New Komitas)", "developer", [METTA_ENT], 2005, ["Մետտա Գրուպ"], [], METTA_POS, "high", METTA_NOTES),
    rec("Retro Shin", "developer",
        [ent("«Ռետրո-Շին» ՍՊԸ", "RETRO-SHIN LLC", "02698612", "ՍՊԸ", 2019, K("02698612"))],
        None, ["Ռետրո-Շին", "Ռետրոշին"], [],
        [{"title": "Atlantic Plaza, Samvel Gevorgyan 4, Davtashen (218 units, completed 2023)", "url": "https://www.retroshin.am/hy/buildings",
          "summary": "Completed 16-storey residential building with commercial ground floors; earlier project at 3 Ghapantsyan."}],
        "medium",
        "Website: 'Retroshin LLC'. karg.am: ՌԵՏՐՈ-ՇԻՆ ՀՎՀՀ 02698612, active, NACE F41.20 construction, legal address Hyusisayin Ave 1, Kentron; reg. date shown 05.06.2019; sole founder Alfred Manukov. Only active construction entity with that name; no address cross-check available (retroshin.am returned empty to curl)."),
    rec("Moskovyan Passage (AIG / Lasker Limited / Ak And Ak Building Technologies)", "developer",
        [ent("«Լասկեր Լիմիթեդ» (ոչ ռեզիդենտ, մշտական հաստատություն)", "LASKER LIMITED (Armenian permanent establishment)", "02660879", "ոչ ռեզիդենտ", 2017, K("02660879")),
         ent("«Լասկեր» ՍՊԸ", "LASKER LLC", "02571182", "ՍՊԸ", 2004, K("02571182"))],
        None, ["Լասկեր Լիմիթեդ", "Լասկեր", "Էյ Այ Ջի"], [],
        [{"title": "Moskovyan Passage, Moskovyan 35 - VTB Bank Armenia head office tenant", "url": "http://www.moskovyan-passage.am/",
          "summary": "Elite mixed-use building built 2006-2012 in central Yerevan hosting VTB Bank Armenia HQ on floors 1-3."}],
        "medium",
        "karg.am: ԼԱՍԿԵՐ ԼԻՄԻԹԵԴ ՀՎՀՀ 02660879 is a non-resident operating via permanent establishment, address Moskovyan 35 (exact building address) - likely the foreign owner/lessor. ԼԱՍԿԵՐ ՍՊԸ 02571182 (reg. 2004, Nalbandyan 5, NACE L68.20 renting property, founder Arin Richard Muradi Sipan) is a probable related local entity - link inferred from name only. "
        "'AIG' and 'Ak And Ak Building Technologies' not found in karg.am autocomplete (tried Armenian transliterations); roles unknown (possibly contractor)."),
    rec("Baghramyanshin & Valex (Abovyan Hills partners)", "developer",
        [ent("«Վարդանյանշին» ՍՊԸ", "VARDANYANSHIN LLC", "02857626", "ՍՊԸ", 2022, K("02857626")),
         ent("«Վալեքս» ՍՊԸ", "VALEX LLC", "04432033", "ՍՊԸ", 2019, K("04432033")),
         ent("«Բաղրամյանշին» ԲԲԸ", "BAGHRAMYANSHIN OJSC", "04600132", "ԲԲԸ", 2002, K("04600132"))],
        None, ["Բաղրամյանշին", "Վալեքս", "Վարդանյանշին"], [],
        [{"title": "Avan Hills completed; Abovyan Hills second joint project", "url": "https://abovyanhills.am/about",
          "summary": "Partners completed the Avan Hills multifunctional complex and formed a project company for Abovyan Hills (230+ units)."}],
        "medium",
        "abovyanhills.am/about: Avan Hills built jointly by Բաղրամյանշին ԲԲ and Վալեքս ՍՊ; Abovyan Hills developer is Վարդանյանշին ՍՊԸ founded by them. karg.am: ՎԱՐԴԱՆՅԱՆՇԻՆ 02857626 (reg. 2022, Vardanants 7, construction, founder Vardan Vardanyan 100%); ՎԱԼԵՔՍ 04432033 (reg. 2019, Kanaker-Zeytun, founders Vardan Vardanyan 45%, Aleksan Byuzandyan 45%, Levon Grigoryan 10%) - shared founder supports the link. "
        "ԲԱՂՐԱՄՅԱՆՇԻՆ ԲԲԸ 04600132 (reg. 2002, construction) has a registry address in Lernagog, Armavir (Baghramyan region) - name/form match but not confirmed as the same partner. Also exists ՎԱՐԴԱՆՅԱՆՇԻՆ ԿՈՆՑԵՌՆ (08257202, same founder). ՎԱԼԵՔՍ ՇԻՆ (00226654) is a different company."),
    rec("Luyser", "developer",
        [ent("«Լույսեր» ՓԲԸ", "LUYSER CJSC", "01291675", "ՓԲԸ", 2019, K("01291675"))],
        None, ["Լույսեր"], [],
        [{"title": "Luyser residential complex (4 buildings, Kirk Kerkorian 23/7) and Luyser Center", "url": "https://luyser.am/hy",
          "summary": "Completed four-building complex in Malatia-Sebastia plus a 14,300 m2 multifunctional centre under way nearby."}],
        "high",
        "karucapatoxic.am listing shows developer 'Luyser Pby' (= ՓԲԸ). karg.am: ԼՈՒՅՍԵՐ ՓԲԸ ՀՎՀՀ 01291675, active, NACE F41.10 development, legal address Leningradyan St 31 (Ajapnyak), next to Luyser Center at Leningradyan 29/12; registration date shown 29.04.2019. Unrelated: ԷԴԵՍՍԱՅԻ ԼՈՒՅՍԵՐ, ԼՈՒՅՍԵՐ ԳՐԱԽԱՆՈՒԹ."),
    rec("ST Service  / Mikshin", "developer",
        [ent("«Միկշին» ՍՊԸ", "MIKSHIN LLC", "01561878", "ՍՊԸ", 2007, K("01561878")),
         ent("«Էս Թի Սերվիս» ՍՊԸ", "ST SERVICE LLC", "01566381", "ՍՊԸ", 2009, K("01566381"))],
        2007, ["Միկշին", "Էս Թի Սերվիս"],
        [{"date": "2016-04-08", "title": "The General: An Armenian Master of Offshores (Panama Papers)", "url": "https://www.occrp.org/en/project/the-panama-papers/the-general-an-armenian-master-of-offshores",
          "summary": "OCCRP investigation into offshore holdings of the family of ex-defence minister Mikael Harutyunyan notes his son Tigran is sole owner of Mikshin, which won an 800m AMD government apartment contract."},
         {"date": "2015-05-17", "title": "Yeraz district populated at state-budget expense: apartments bought by government for 755m AMD", "url": "https://iravaban.net/en/87164.html",
          "summary": "Iravaban.net reports that 16 of 28 flats bought by state bodies (NSS, Prosecutor's Office, Finance Ministry etc.) for employees came from Mikshin and Mikmetal in the Yeraz district at Adonts St 8 and 8/2."}],
        [{"title": "Yeraz residential district, Arabkir", "url": "https://stservice.am/about",
          "summary": "Large district developed by Mikshin and built in-house by sister contractor ST Service (about 300 staff)."},
         {"title": "Mikshin 15th anniversary interview: ~1,700 apartments built in Yeraz, 1,700 more planned", "url": "https://banks.am/en/news/interviews/22981",
          "summary": "Founder Tigran Harutyunyan describes the group's portfolio including development, IT, a foundation and the MyLer ski resort project (2022)."},
         {"title": "Myler Mountain Resort covered by Los Angeles Times as Armenia's largest investment project", "url": "https://armenpress.am/en/article/1243661",
          "summary": "Armenpress (March 2026) credits Mikshin founder Tigran Harutyunyan with conceiving the $1.3bn Myler resort project."}],
        "high",
        "Mikshin = developer, ST Service = contractor (sister). karg.am: ՄԻԿՇԻՆ 01561878 (reg. 22.11.2007, Byron St 4, Nork-Marash, founder Tigran Harutyunyan 100%) and ԷՍ ԹԻ ՍԵՐՎԻՍ 01566381 (reg. 27.03.2009, same Byron St 4, construction, director Stepan Khachatryan) - shared address confirms the pair. ՄԻՔՇԻՆ-Մ (01349257) is unrelated. Owner Tigran Harutyunyan is the son of former Defence Minister Mikael Harutyunyan (per OCCRP) - politically exposed family; related company Mikmetal also sold Yeraz flats."),
    rec("ASR", "developer",
        [ent("«ԱՍՌ» ՍՊԸ", "ASR LLC", "09422707", "ՍՊԸ", 2011, K("09422707"))],
        None, ["ԱՍՌ", "Էյ Էս Ար"], [], [],
        "low",
        "myhome.am/building/272: developer 'ԱՍՌ ՍՊԸ', office Artsakh Ave 4th lane 5/5 Shengavit, email asr.llc@mail.ru, project Acharyan 43/20 Avan (6 floors, 50 apts, cinder block). karg.am has one active ԱՍՌ LLC: ՀՎՀՀ 09422707, reg. 13.09.2011, legal address Arami 64 Kentron, founder Sasun Aghajanyan - name matches but address differs; tax ID not confirmed as the developer."),
    rec("METTA GROUP", "developer", [METTA_ENT], 2005, ["Մետտա Գրուպ"], [], METTA_POS, "high", METTA_NOTES),
]

for r in R:
    for e in r["legal_entities"]:
        pass
for r in R:
    if 'budget exhausted' not in r['notes']:
        r['notes'] += ' News coverage check limited (session WebSearch budget exhausted; only Google News RSS used) - absence of issues is not evidence of a clean record.'
json.dump(R, open(OUT, 'w'), ensure_ascii=False, indent=1)
print(len(R))
