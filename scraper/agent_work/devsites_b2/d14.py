import sys; sys.path.insert(0,'.')
from mk import *
from urllib.parse import quote
I="https://elitprojectgroup.am/adm/images/"
q=lambda n: I+quote(n)
dev="Elit Project Group"; du="https://elitprojectgroup.am/"; ph=["+37493363882","+37441248818","+37491773369"]; em="info.elit@mail.ru"
so={"facebook":"https://www.facebook.com/abovyanpark","instagram":"https://www.instagram.com/abovyanpark/"}
P=[rec(source_url="https://elitprojectgroup.am/apartaments",title="Abovyan Park apartment building (Elit Project Group)",developer=dev,developer_url=du,city="Abovyan",district="Kotayk",address="23 Augusti St, 1st lane 4/7, Abovyan",lat=40.271366,lng=44.628076,
 price_min_amd_m2=510000,price_currency_raw="AMD 510 000 per m2; income tax refund applies",status="under construction",type="residential",phones=ph,email=em,social=so,website="https://estate.ameriabank.am/building/124",
 images=[q("_25_54_1502_building1.jpg"),q("_20_94_1547_Render_4.png"),q("_28_77_1034_new_project2.jpeg"),q("_48_71_1079_new_project3.png"),q("_31_64_1047_new_project4.jpeg"),q("_49_65_1047_WhatsApp Image 2025-02-18 at 12.43.42.jpeg")],
 description="Apartment building under construction in Abovyan by Elit Project Group (20 years in construction). Apartments of 33, 39.5, 50 and 55.5 m2 at 510,000 AMD/m2; income-tax mortgage refund; Ameriabank partner building.",
 apartments=[{"rooms":"1-2","area_min":33,"area_max":55.5,"price_from":16830000,"currency":"AMD"}]),
 rec(source_url="https://elitprojectgroup.am/townhouses",title="Elit Project Group Townhouses Abovyan",developer=dev,developer_url=du,city="Abovyan",district="Kotayk",address="Abovyan",price_currency_raw="52 million AMD (140 m2 townhouse + 130 m2 land)",status="completed",floors="2",type="residential",phones=ph,email=em,social=so,
 images=[q("_29_75_1074_townhouse1.jpeg"),q("_46_81_1065_townhouse2.jpeg"),q("_21_51_1080_townhouse3.jpeg"),q("_18_97_1026_townhouse4.jpeg"),q("_43_55_1514_450716038_122111721314371617_2372927945435853513_n.jpg"),q("_14_56_1025_WhatsApp Image 2025-02-18 at 12.50.26 (1).jpeg")],
 description="Ready-built two-storey townhouses in Abovyan: 140 m2 house plus 130 m2 of private land for 52 million AMD; income-tax refund applies.",
 apartments=[{"rooms":"townhouse","area_min":140,"area_max":140,"price_from":52000000,"currency":"AMD"}])]
save("14_elit",P)
