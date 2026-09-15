import json
exec(open("part1.py").read().split("out=[")[0])
out=json.load(open("part1.json"))
MH="https://myhome.am/hy/building/"
NS=" News search not performed for this developer: the session's WebSearch quota was exhausted, so news_issues/positives are empty by lack of coverage, not confirmed clean."
out+=[
rec("EREBUNI-ARMANI","developer",
 [ent("Էրեբունի-Արմանի","Erebuni-Armani","ՍՊԸ",MH+"110")],
 ["Էրեբունի-Արմանի","Էրեբունի Արմանի","Արմանի-Էրեբունի"],[],[],
 "high","myhome.am (Ameriabank platform) building 110 lists Կառուցապատող ԷՐԵԲՈՒՆԻ-ԱՐՄԱՆԻ ՍՊԸ, address Yerevan, Erebuni, Erebunu 5; phones +374 77 311000, +374 55 510055. Project Erebuni 2/2 bldg A (161 flats, completion 09/2026, income-tax refund eligible). Likely the same developer as 'Armani - Erebuni' multifunctional complex at Erebuni 2/1 (karucapatoxic.am/en/110) in the local dataset. Tax ID not found."+NS),
rec("HATIS PARK REZIDENCE","developer",
 [ent("Հատիս Պարկ Ռեզիդենս","Hatis Park Residence","unknown",MH+"352")],
 ["Հատիս Պարկ Ռեզիդենս","Հատ Շին","Հատիս Շին"],[],[],
 "low","myhome.am building 352 lists Կառուցապատող ՀԱՏԻՍ ՊԱՐԿ ՌԵԶԻԴԵՆՍ without legal form (address Kotayk, Akunk / Nor Gyugh 1st st 7; phone +374 97 350005). This is probably a project brand; contact email hatshin2023@mail.ru hints at an LLC named like «Հատ Շին»/«Հատիս Շին» registered ~2023 - unverified guess for datalex. Project: 120 panel-built flats, completion 06/2028, no income-tax refund. Tax ID not found."+NS),
rec("Los Angeles Yeghvard","developer",
 [ent("Հաուս Քոնսթրաքշն","House Construction","ՍՊԸ","https://redgroup.am/projects/bnakarankarucapatoxic-north-yard")],
 ["Հաուս Քոնսթրաքշն","Հաուս Կոնստրուկցիա","Հաուզ Քոնսթրաքշն"],[],
 [{"title":"Ameriabank partner bank for the Yeghvard townhouse project","url":"https://redgroup.am/projects/bnakarankarucapatoxic-north-yard","summary":"23-townhouse Yeghvard project lists Ameriabank as partner bank, designer TF + Architects and builder Arm Construct."}],
 "high","layeghvard.am footer reads '© House Construction LLC'; local dataset also has 'House Construction (LA Yeghvard)'. redgroup.am 'North Yard' page (23 two-storey townhouses in Yeghvard, same count as LA Yeghvard) states Կառուցապատող՝ «Հաուս Քոնսթրաքշն» ՍՊԸ, designer «Թի Էֆ + Արքիթեքթս» ՍՊԸ, builder «Arm Construct» ՍՊԸ, construction start 2025. 'House Construction' is a generic name - same-name companies likely exist in registry. Tax ID not found."+NS),
rec("STRONG BUILDINGS","developer",
 [ent("Սթրոնգ Բիլդինգս","Strong Buildings","ՍՊԸ",MH+"312",None,None)],
 ["Սթրոնգ Բիլդինգս","Ստրոնգ Բիլդինգս"],[],[],
 "high","myhome.am building 312 lists Կառուցապատող ՍԹՐՈՆԳ ԲԻԼԴԻՆԳՍ ՍՊԸ, registered address Yerevan, Artsakhi st 18 bldg, apt 75; email strong.buildings2022@gmail.com suggests incorporation around 2022 (not confirmed). Project Abovyan, Sevan st 4/10 A & B (204 flats, completion 11/2028). Tax ID not found."+NS),
rec("CAVEMAN RESIDENCE","developer",
 [ent("Քեյվմեն Ռեզիդենս","Caveman Residence","unknown",MH+"269")],
 ["Քեյվմեն Ռեզիդենս","Դիլիջան Ինն","Մովսեսյան և Գործընկերներ"],[],[],
 "low","myhome.am building 269 lists Կառուցապատող ՔԵՅՎՄԵՆ ՌԵԶԻԴԵՆՍ without legal form (Dilijan, Orjonikidze 81/3; phone +374 95 717611). Description calls it the second project of 'DilijanINN' (hotel dilijaninn.am at Orjonikidze 104/1); contact email movsesyanandpartners@gmail.com suggests a 'Movsesyan and Partners' entity. The registered developer LLC is therefore unconfirmed - datalex names 2-3 are speculative. Tax ID not found."+NS),
rec("GTG ANHAGHT","developer",
 [ent("Ջի Թի Բի Անհաղթ","GTB Anhaght","ՍՊԸ","https://gtbholdings.com/about/?lang=hy"),
  ent("Ջի Թի Բի Հոլդինգս","GTB Holdings","ՍՊԸ","https://gtbholdings.com/about/",None,2022)],
 ["Ջի Թի Բի Անհաղթ","ԳԹԲ Անհաղթ","Ջի Թի Բի Հոլդինգս"],[],
 [{"title":"Part of GTB Holdings group (steel plant, Cascade Cultural Hub)","url":"https://gtbholdings.com/about/","summary":"Parent GTB Holdings (founded 2022, CEO Tiran Hakobyan) groups GTB Steel, GTB Tower, GTB Development (Cascade Cultural Hub with Jean-Michel Wilmotte) and contractor GTBuild."}],
 "high","'GTG' is a myhome.am typo for GTB: myhome.am building 233 shows «ԳՏԳ Անհաղթ ՍՊԸ» with address Proshyan 12 and email armen@gtbholding.com / site anhaght.gtbholdings.com, which are GTB Holdings' HQ and domain. GTB Holdings' Armenian About page names subsidiary «Ջի Թի Բի Անհաղթ» ՍՊԸ; parent footer «ՋԻ ԹԻ ԲԻ ՀՈԼԴԻՆԳՍ» ՍՊԸ. Project Davit Anhaght 25 (43 flats, 8 floors). Construction by «Ջի Թի Բիլդ» ՍՊԸ (GTBuild). Tax IDs not found."+NS),
]
assert len(out)==15
json.dump(out,open("../web_D.json","w"),ensure_ascii=False,indent=1)
print([o["developer"] for o in out])
