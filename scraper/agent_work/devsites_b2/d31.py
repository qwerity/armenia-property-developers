import sys; sys.path.insert(0,'.')
from mk import *
dev="Prime Developers (MLL Group)"; du="https://primedevelopers.am/"; ph=["+37498844771","+37477890047"]; em="info@primedevelopers.am"
so={"facebook":"https://www.facebook.com/profile.php?id=100095614057576","instagram":"https://www.instagram.com/primedevelopers__"}
P=[rec(source_url="https://primedevelopers.am/en/project/NORTHERN-GATES",title="Northern Gates",developer=dev,developer_url=du,city="Yerevan",district="Avan",address="128 Zoravar Sarkavagi St (Z. Sarkavagi 128), Yerevan",
 price_currency_raw="Apartments from 21,000,000 AMD; installments from 140,000 AMD/month",status="under construction",floors="18",type="residential",phones=ph,email=em,social=so,
 images=["https://primedevelopers.am/storage/Home/81.jpg","https://primedevelopers.am/storage/News/IMG_2781.PNG"],
 description="Eco-class multi-residential complex in the developing part of Avan, 8 km from Republic Square: 3 buildings (sections AB and C, up to 18 floors) with separate entrances, public spaces on lower floors, above-ground and 2-level underground parking, natural stone facades, individual heating/cooling, energy-saving materials, large green area with playground, garden, gazebo, football/volleyball/basketball courts and bonfire area. Apartments 40-118 m2 from 21,000,000 AMD; sales started Q3 2025 (105 available).",
 apartments=[{"rooms":"","area_min":40,"area_max":118,"price_from":21000000,"currency":"AMD"}]),
 rec(source_url="https://primedevelopers.am/en/project/discovery-plaza",title="Discovery Plaza",developer=dev,developer_url=du,city="Yerevan",district="Ajapnyak",address="2 Aharonyan St, Yerevan",
 price_currency_raw="Apartments from 31,663,200 AMD",status="under construction",type="residential",phones=ph,email=em,social=so,
 images=["https://primedevelopers.am/build/assets/discovery-e8e96697.jpg","https://primedevelopers.am/storage/About/91.jpg","https://primedevelopers.am/storage/News/IMG_1659.PNG"],
 description="Residential project 300 m from Yeraz Park and 10 minutes' drive from Republic Square, named after a preserved Soviet mosaic of human evolution found on site and integrated into the building. Four buildings with own entrances, public spaces and 2-level underground parking, natural stone facades, individual heating; rooftop BBQ, co-working, bicycle parking, gym, pool, billiards, playground, optional valet. Apartments 50-142 m2 from 31,663,200 AMD; sales since Q3 2023, only a few left; corridor finishing underway (2026).",
 apartments=[{"rooms":"","area_min":50,"area_max":142,"price_from":31663200,"currency":"AMD"}])]
save("31_prime",P,{"note":"Dilijan Eye (known) not listed on site"})
