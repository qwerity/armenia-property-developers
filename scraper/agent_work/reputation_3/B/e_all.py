import json
def L(hy,en,tax=None,form="ՍՊԸ",yr=None,src="",role=None):
    d={"name_hy":hy,"name_en":en,"tax_id":tax,"form":form,"registered_year":yr,"source_url":src}
    if role: d["role"]=role
    return d
def E(dev,role,les,founded,dl,news,pos,conf,notes):
    return {"developer":dev,"role":role,"legal_entities":les,"founded_year":founded,"datalex_names":dl,
            "tax_ids":[l["tax_id"] for l in les if l["tax_id"]],"news_issues":news,"positives":pos,"entity_confidence":conf,"notes":notes}
ACBA="https://www.acba.am/hy/individuals/loans/mortgage/constructors"
EVO="https://www.evoca.am/en/construction-companies"
rg_notes="ACBA Bank developer list names «ՌԻՉ-ԳԱՌԴԵՆ» ՍՊԸ as developer of Rich Garden 2 (Zovuni 36th st, 2nd lane 26), same phones/email as Rich Garden. construction.am lists Rich Garden since 2021, office Davtashen 4th district 35/2; no TIN shown. Registry spelling may be ՌԻՉ-ԳԱՌԴԵՆ or ՌԻՉ ԳԱՐԴԵՆ."
out=[
E("Rich Garden","developer",[L("«Ռիչ-Գառդեն» ՍՊԸ","Rich Garden LLC",None,"ՍՊԸ",2021,ACBA)],2021,["Ռիչ-Գառդեն","Ռիչ Գարդեն","Ռիչ Գառդեն"],[],
  [{"title":"ACBA Bank mortgage partner developer","url":ACBA,"summary":"Rich Garden 2 is on ACBA's list of partner developers for mortgage purchases."},
   {"title":"Completed Rich Garden townhouse complex (18 connected houses, Zovuni)","url":"https://www.construction.am/arm/apartments-in-new-developments/rich-garden/","summary":"construction.am lists the first Rich Garden complex as completed in 2022."}],"medium",rg_notes),
E("Rich-garden","developer",[L("«Ռիչ-Գառդեն» ՍՊԸ","Rich Garden LLC",None,"ՍՊԸ",2021,ACBA)],2021,["Ռիչ-Գառդեն","Ռիչ Գարդեն","Ռիչ Գառդեն"],[],
  [{"title":"ACBA Bank mortgage partner developer","url":ACBA,"summary":"Rich Garden 2 (Zovuni, 10 units, completion 2027) listed on ACBA's partner developer page."}],"high",rg_notes+" Same company as 'Rich Garden'."),
E("Prime Developers","developer",[
   L("«Նորդեռն Գեյթս» ԲԲԸ","Northern Gates OJSC",None,"ԲԲԸ",None,EVO,"project company for Northern Gates (Z. Sarkavagi 128), phone matches Prime Developers"),
   L("«ՄԼԼ Ինդաստրիզ» ՍՊԸ","MLL Industries LLC",None,"ՍՊԸ",2001,"https://primedevelopers.am/en/about","parent/founder, general contractor (MLL Group)")],None,["Նորդեռն Գեյթս","ՄԼԼ Ինդաստրիզ","Փրայմ Դեվելոպերս"],[],
  [{"title":"Part of MLL Group / MLL Industries (est. 2001)","url":"https://primedevelopers.am/en/about","summary":"Prime Developers says it belongs to MLL Group whose contractor MLL Industries worked on the US Embassy, Zvartnots airport terminals and UWC Dilijan."},
   {"title":"Evocabank partner developer (Northern Gates OJSC)","url":EVO,"summary":"Northern Gates OJSC appears on Evocabank's list of partner construction companies."}],"medium",
  "Prime Developers is a brand; Evocabank lists the Northern Gates project under \"Northern Gates\" OJSC with Prime Developers' phone +374 98 844 771. Discovery Plaza (Aharonyan 2) legal entity not identified. Armenian spelling of Northern Gates/MLL Industries not verified (could be ՄԼԼ Ինդասթրիզ). Prime Developers says projects from 2001 via MLL Industries."),
E("Brawerk  (formerly Metsn Erik )","developer",[
   L("«Բրավերկ» ՍՊԸ (նախկինում «Մեծն Էրիկ» ՍՊԸ)","Braverk LLC (Brawerk), formerly Metsn Erik LLC",None,"ՍՊԸ",1995,"https://brawerk.am/hy/terms-and-conditions")],1995,["Բրավերկ","Մեծն Էրիկ","Շիրակ-95"],[],
  [{"title":"30+ year contractor: 60+ projects incl. 52 residential buildings","url":"https://brawerk.am/hy/braverki-masin","summary":"Company says it was founded in Gyumri in 1995 as Shirak-95, later Metsn Erik, and built 52 apartment buildings, schools, clinics, and restored Kumayri heritage buildings and the Gyumri TUMO building."},
   {"title":"Rebranding from Metsn Erik to Brawerk (May 2026)","url":"https://brawerk.am/hy/norutyunner/rebrending-Metsn-Erik-y-veranvanvel-e-Braverk","summary":"Company announced renaming after 31 years of activity."}],"high",
  "Terms page: site operated by «Braverk» ՍՊԸ, trading as BRAWERK, formerly «Metsn Erik» ՍՊԸ; address Arshakunyats 67/15, Yerevan. History: Shirak-95 (Gyumri, 1995) -> Metsn Erik -> Brawerk; led by Levon Shahumyan (history page). Check datalex under both old and new names. Registry name may still be ՄԵԾՆ ԷՐԻԿ."),
E("МЕЦН ЭРИК","developer",[
   L("«Մեծն Էրիկ» ՍՊԸ (այժմ «Բրավերկ» ՍՊԸ)","Metsn Erik LLC (now Braverk LLC / Brawerk)",None,"ՍՊԸ",1995,"https://brawerk.am/hy/terms-and-conditions")],1995,["Մեծն Էրիկ","Բրավերկ","Շիրակ-95"],[],
  [{"title":"30+ year contractor: 60+ projects incl. 52 residential buildings","url":"https://brawerk.am/hy/braverki-masin","summary":"Same company as Brawerk; founded 1995 in Gyumri, broad public/residential/heritage portfolio."}],"high",
  "Same company as 'Brawerk  (formerly Metsn Erik )' - identical phones (+37455707082, +37491659002). Retro Realty (Avan, Tumanyan 46/2) is one of its finished projects per karucapatoxic."),
E("Mountain Plaza","developer",[L("«Մաունթին Պլազա» ՍՊԸ","Mountain Plaza LLC",None,"ՍՊԸ",None,"https://mountainplaza.am/")],None,["Մաունթին Պլազա","Մաունթեն Պլազա","Մոունթին Պլազա"],[],[],"low",
  "Website Telegram handle 'MountainPlazaLLC' suggests the brand is itself an LLC; not confirmed in any registry-type source. Contractors listed on site: Master Invest LLC (earthworks), Malkhasyan Shin LLC (construction), Dragsman LLC (concrete), North Invest LLC; completion certificate expected spring 2027. Project G. Hovsepyan 48/3, Nork-Marash."),
E("Khakhamyan Heritage","developer",[],None,["Խախամյան Հերիթեյջ","Խախամյան"],[],[],"low",
  "Only source is ac-box.com listing projects 'Sar in' and 'IVY' (AMANOO projects) on G. Hovsepyan 40/16 and 38/10. No legal entity found; searching by founder surname Khakhamyan may help. Web search budget was exhausted before deeper lookup."),
E("Elit Project Group","developer",[L("«Էլիտ Պրոջեկտ Գրուպ» ՍՊԸ","Elit Project Group LLC",None,"ՍՊԸ",None,"https://elitprojectgroup.am/")],None,["Էլիտ Պրոջեկտ Գրուպ","Էլիթ Պրոեկտ Գրուպ","Էլիտ Պրոեկտ Գրուպ"],[],[],"low",
  "Website (JS app) describes Elit Project Group as a developer (Abovyan Park apartment building, townhouses in Abovyan). Legal form/spelling not confirmed; name assumed to match brand."),
E("Project EVN (construction management)","contractor",[L(None,"Project EVN",None,None,None,"https://www.projectevn.com/about-us/")],None,["Փրոջեկտ Իվիէն","Պրոեկտ ԵՎՆ"],[],[],"low",
  "Construction/project management consultancy (8 Vardanants blind alley, Yerevan; team Artur Ter-Simonyan, Haykaz Danielyan), not a developer; its site shows managed projects (Areni Guest House, Lavan Sevan). No legal entity name disclosed; datalex matches unlikely."),
E("HAY DEVELOP","developer",[L("«Հայ Դեվելոփ» ՍՊԸ","Hay Develop LLC",None,"ՍՊԸ",None,"https://myhome.am/hy/building/245")],None,["Հայ Դեվելոփ","Հայ Դևելոփ"],[],
  [{"title":"Listed as Ameriabank (myhome.am) partner developer","url":"https://myhome.am/hy/partners/developers/88","summary":"HAY DEVELOP has a developer profile on Ameriabank's myhome.am platform for its 17-storey Arabkir project (H. Emin 1st lane)."}],"low",
  "Only brand name on myhome.am (developer id 88); contact email idjevanatun@mail.ru hints at a link to an 'Ijevanatun' entity but unverified. Facebook page created 2024."),
E("Mitstart","developer",[L("«Միթսթարթ» ՍՊԸ","Mitstart LLC",None,"ՍՊԸ",None,"https://ar-go.am/project/zovbuilding")],None,["Միթսթարթ","Միտստարտ"],[],
  [{"title":"Evocabank partner developer","url":EVO,"summary":"Evocabank lists Mitstart LLC as builder of the Zovuni 1st street project."}],"high",
  "ar-go.am Zov Bilding page: developer «ՄԻԹՍԹԱՐԹ» ՍՊԸ, builder «ԴԻ.ՍԻ. ՔՈՄՓԱՆԻ» ՍՊԸ, bank Evocabank. Same phone (055-200-707 / 041-200-700) is also used by 'Man Invest Group' (Kanakeravan) on the Evocabank list - possibly related companies."),
E("Midis Construction","developer",[L("«Միդիս Քոնսթրաքշն» ՍՊԸ","Midis Construction LLC",None,"ՍՊԸ",None,EVO)],None,["Միդիս Քոնսթրաքշն","Միդիս Կոնստրուկցիա","Միդիս Կոնստրաքշն"],[],
  [{"title":"Evocabank partner developer","url":EVO,"summary":"Evocabank lists \"Midis Construction\" LLC as developer of Midis Park (Dzoraghbyur), sales via Silver Real Estate."}],"high",
  "Evocabank: developer \"Midis Construction\" LLC, sales manager Silver Real Estate (sreal.am, phones +37455386500 shared with AAA SHIN). myhome.am shows Armenian name ՄԻԴԻՍ ՔՈՆՍԹՐԱՔՇՆ."),
E("MIDIS CONSTRUCTION","developer",[L("«Միդիս Քոնսթրաքշն» ՍՊԸ","Midis Construction LLC",None,"ՍՊԸ",None,"https://myhome.am/en/project/1")],None,["Միդիս Քոնսթրաքշն","Միդիս Կոնստրուկցիա","Միդիս Կոնստրաքշն"],[],
  [{"title":"Evocabank partner developer","url":EVO,"summary":"Midis Park listed with Evocabank; also on Ameriabank's myhome.am."}],"high","Same as 'Midis Construction'. myhome.am developer name ՄԻԴԻՍ ՔՈՆՍԹՐԱՔՇՆ, email midisconstruction@mail.ru."),
E("AAA SHIN","developer",[L("«ԱԱԱ Շին» ՍՊԸ","AAA Shin LLC",None,"ՍՊԸ",None,"https://myhome.am/")],None,["ԱԱԱ Շին","Էյ Էյ Էյ Շին","ԵՌԱԿԻ Ա ՇԻՆ"],[],[],"low",
  "Vista Residence (Dro 13/1) listed on myhome.am/karucapatoxic under 'AAA SHIN'; contact phones/email belong to Silver Real Estate agency (sreal.am) which also sells Midis Park. Legal form and Armenian spelling not verified."),
E("Lusabac (Sunrise Residential Complex)","developer",[L("«Ատարադ» ՍՊԸ","Atarad LLC",None,"ՍՊԸ",None,"https://lusabac.am/am/privacy")],None,["Ատարադ","Լուսաբաց"],[],[],"medium",
  "lusabac.am privacy policy and consent pages are issued by «Ատարադ» ՍՊԸ, which operates the Lusabac/Rassvet (Sunrise) complex site at G. Hovsepyan 26/15, Nork-Marash. Likely the developer/project company; role not stated explicitly."),
E("Zoar","developer",[L("«Ռութ Քոնստրակտ» ՍՊԸ","Root Construct LLC",None,"ՍՊԸ",None,ACBA)],None,["Ռութ Քոնստրակտ","Ռութ Կոնստրակտ","Զոար"],[],
  [{"title":"ACBA Bank partner developer; project completed","url":ACBA,"summary":"ACBA lists ՌՈՒԹ ՔՈՆՍՏՐԱԿՏ LLC as developer of a completed 14-storey, 106-unit building in Arinj, P. Sevak block 4th st 2/1."}],"high",
  "ZOAR Residence (P. Sevak block 4th street 2, Arinj) contact email root.construct.armenia@gmail.com and phone 041 221 205 match ACBA's entry for «ՌՈՒԹ ՔՈՆՍՏՐԱԿՏ» ՍՊԸ."),
E("Royal Rezidens","developer",[L("«Ռոյալ Ռեզիդենս» ՍՊԸ","Royal Residence LLC",None,"ՍՊԸ",None,ACBA)],None,["Ռոյալ Ռեզիդենս"],[],
  [{"title":"ACBA Bank partner developer; completed 16-storey building","url":ACBA,"summary":"ACBA lists «ՌՈՅԱԼ ՌԵԶԻԴԵՆՍ» ՍՊԸ as developer of the finished 132-unit building at Halabyan 20/16, Ajapnyak."}],"high","ACBA developer page: «ՌՈՅԱԼ ՌԵԶԻԴԵՆՍ» ՍՊԸ, Halabyan 20/16, home@royalresidence.am, site royalresidence.me."),
E("Rem Group","developer",[L("«Ռեմ Գրուպ» ՍՊԸ","Rem Group LLC","02209604","ՍՊԸ",1996,"https://www.construction.am/companies/rem-group/"),
   L("«Էլեն Ռիելթի» ՍՊԸ","Elen Realty LLC",None,"ՍՊԸ",None,"https://www.construction.am/companies/rem-group/","sales agent (email elenrealtyllc@mail.ru)")],1996,["Ռեմ Գրուպ","Էլեն Ռիելթի"],[],
  [{"title":"Licensed general contractor since 1996","url":"https://www.construction.am/companies/rem-group/","summary":"construction.am shows Rem Group LLC (TIN 02209604, head Armen Rshtuni) with category-1 construction licences across building and utility works."}],"high",
  "construction.am company card: \"Rem Group\" LLC, TIN 02209604, Armen Rshtuni, 8/9 Frunze St. Project Rem Tower at Frunze 8/9. Contact email refers to Elen Realty LLC (likely sales agent), unverified."),
E("Bedeck","developer",[L("«Բեդեք» ՍՊԸ","Bedeck LLC","00450801","ՍՊԸ",2009,"https://www.construction.am/companies/bedeck/")],2009,["Բեդեք","Բեդեկ"],[],
  [{"title":"Licensed general contractor since 2009","url":"https://www.construction.am/companies/bedeck/","summary":"construction.am shows Bedeck LLC (TIN 00450801, head Garnik Avetisyan) with category-1 licences incl. residential, power, HVAC, hydraulic and transport structures."}],"high",
  "construction.am company card: \"Bedeck\" LLC, TIN 00450801, Garnik Avetisyan, 87 Sasuntsi David St. Project: Bedeck Davtashen Complex (Pirumyanner 13). Armenian spelling assumed."),
E("Green Property Development","developer",[L("«Գրին Փրոփերթի Դեվելոփմենթ» ՍՊԸ","Green Property Development LLC",None,"ՍՊԸ",2019,"https://azatutyuncomplex.am/about"),
   L("«Մետրոշին» ՍՊԸ","Metroshin",None,None,None,"https://azatutyuncomplex.am/about","general contractor")],2019,["Գրին Փրոփերթի Դեվելոփմենթ","Գրին Պրոպերտի Դեվելոպմենթ"],[],[],"medium",
  "azatutyuncomplex.am 'About': developer of Azatutyun complex (Azatutyan 26/1) is «Գրին Փրոփերթի Դեվելոփմենթ», founded 2019, first project; construction company Metroshin, works with VG... for construction management. Legal form not stated (assumed ՍՊԸ).")
]
json.dump(out,open('e_all.json','w'),ensure_ascii=False)
