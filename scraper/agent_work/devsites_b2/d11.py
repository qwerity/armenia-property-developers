import sys; sys.path.insert(0,'.')
from mk import *
dev="Care Building Services (CBS)"; du="https://cbs-construction.am/"; ph=["+37444033888","+37455618618","+37460618618"]; em="cbs@cbs-construction.am"
so={"facebook":"https://www.facebook.com/CareBuildingServices/","instagram":"https://www.instagram.com/cbs_construction.am/"}
B="https://cbs-construction.am/%D5%B6%D5%A1%D5%AD%D5%A1%D5%A3%D5%AE%D5%A5%D6%80/"; U="https://cbs-construction.am/wp-content/uploads/"
amen="Malkhasyants complex services: 24/7 security and maintenance, CCTV, sports clubs, playground, car wash, uninterrupted power supply, 4,000 m2 closed courtyard."
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,social=so,**k)
P=[R(source_url=B+"%d5%b4%d5%a1%d5%ac%d5%ad%d5%a1%d5%bd%d5%b5%d5%a1%d5%b6%d6%81-8/",title="Malkhasyants 8",city="Yerevan",district="Arabkir",address="8 Malkhasyants St, Yerevan",lat=40.210696,lng=44.507781,completion="2028",status="under construction",floors="14",type="residential",
  images=[U+"2026/04/Մալխասյանց-8.jpg",U+"2026/04/Մալխասյանց-8-2.jpg",U+"2026/04/Մալխասյանց-8-3.jpg",U+"2026/04/Մալխասյանց-8-5.jpg",U+"2026/04/Մալխասյանց-8-6.jpg",U+"2026/06/Մալխասյանց-8-scaled.jpg"],
  description="Continuation of the established Malkhasyants residential complex in Arabkir: 14-storey building, 3,392 m2 development area, apartments of 67-107 m2 (combinable up to 200.8 m2), 180 parking spaces. Construction started April 2026, completion 2028. "+amen,
  apartments=[{"rooms":"","area_min":67,"area_max":200.8,"price_from":None,"currency":None}]),
 R(source_url=B+"%d5%b4%d5%a1%d5%ac%d5%ad%d5%a1%d5%bd%d5%b5%d5%a1%d5%b6%d6%81-6-1/",title="Malkhasyants 6/1",city="Yerevan",district="Arabkir",address="6/1 Malkhasyants St, Yerevan",lat=40.210696,lng=44.507781,completion="2025",status="completed",floors="14",type="residential",
  images=[U+"2026/01/111-2-1024x600.png",U+"2026/01/6_1_1-e1768815175162.png",U+"2026/01/6_1_2.png",U+"2026/01/6_1_3.png"],
  description="Part of the Malkhasyants complex: 14-storey building (13 residential floors + 1 public), 28,000 m2, apartments 57-122 m2, 146 parking spaces in separate 1 underground + 5 above-ground level garage. A+ energy certificate, 9+ seismic resistance, substation with two independent feeds, car-free green courtyard with playground. Built 2021-2025; last 3 apartments (97-109 m2) for sale. "+amen),
 R(source_url=B+"%d5%b4%d5%a1%d5%ac%d5%ad%d5%a1%d5%bd%d5%b5%d5%a1%d5%b6%d6%81-4/",title="Malkhasyants 4",city="Yerevan",district="Arabkir",address="4 Malkhasyants St, Yerevan",lat=40.210696,lng=44.507781,completion="2023",status="completed",floors="14",type="residential",
  images=[U+"2026/04/77-Մալխասյանց4-768x1024.jpg",U+"2026/04/77-Մալխասյանց4-2-768x1024.jpg",U+"2026/01/4_1.png",U+"2026/01/4_2.png"],
  description="Part of the Malkhasyants complex: 14-storey building (13 residential + 1 public floor), 22,000 m2, apartments 57.7-122 m2, 146 parking spaces (1 underground + 5 above-ground levels). A+ energy class, 9+ seismic resistance, dual-feed substation, closed green car-free courtyard. Built 2020-2023; last 77 m2 2-room apartment available. "+amen),
 R(source_url=B+"%d5%b7%d5%ab%d6%80%d5%a1%d5%a6-43/",title="Shiraz 43 multifunctional complex",city="Yerevan",district="Ajapnyak",address="43 Shiraz St, Ajapnyak, Yerevan",completion="2027",status="under construction",floors="3",type="commercial",images=[U+"2026/01/3-19-1290x600.jpg"],
  description="Modern 3-storey multifunctional building of 12,000 m2 with fully glazed facade, designed and built by CBS; open flexible floor plates for offices, retail, medical centre, education, co-working, restaurant or car showroom. Started 2024, completion 2027."),
 R(source_url=B+"%d5%a1%d5%b5%d5%a3%d5%a5%d5%b1%d5%b8%d6%80-38/",title="Aygedzor 42 mansion",city="Yerevan",district="Arabkir",address="42 Aygedzor St, Yerevan",price_currency_raw="1,200,000 USD (whole house)",status="under construction",type="residential",images=[U+"2026/04/Այգեձոր-42.jpg"],
  description="Exclusive newly built modern private house for sale in the prestigious Aygedzor neighbourhood: 500 m2 living area on a 350 m2 plot with private courtyard, high-end architecture near the city centre. Price USD 1,200,000.")]
save("11_cbs",P)
