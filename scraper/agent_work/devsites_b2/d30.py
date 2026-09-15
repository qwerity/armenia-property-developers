import sys; sys.path.insert(0,'.')
from mk import *
U="https://parajanov.am/wp-content/uploads/"
P=[rec(source_url="https://parajanov.am/property/",title="Parajanov Club House",developer="Rutsog Invest (RID LLC)",developer_url="https://parajanov.am/",city="Yerevan",district="Kentron",address="15/5 Paronyan St, Yerevan",
 price_currency_raw="price from 5000 m2 (as shown on site; currency unspecified)",completion="2026",status="under construction",floors="27",type="residential",phones=["+37493995588","+79165679134"],email="sales@parajanov.am",
 social={"facebook":"https://www.facebook.com/parajanovclubhouse","instagram":"https://www.instagram.com/parajanov_club_house/"},
 images=[U+"2023/03/CloseUp_Cam1_Post_a-copy_p-scaled.jpg",U+"2023/03/Paronian0002_Post_LightMix-Interactive-copy-1-scaled-e1679336848346.jpg",U+"2023/04/Paronian0004_Post_LightMix-Interactive-copy-3-2.jpg",U+"2023/04/rsz_1_cshading_lightmix_copy_f-2.jpg",U+"2026/02/ЖК-PARAJANOV_Двухкомнатная-кв_Гостиная-02-small.jpg",U+"2023/03/razdan_2.jpeg",U+"2023/01/parajanov-NEW-center-map-e1675431553892.jpg"],
 description="'First club house in Armenia' overlooking the Hrazdan Canyon with Ararat views, at Paronyan 15/5: 16,960 m2, 27 floors, 125 one- to three-bedroom luxury apartments (customizable plans, very large windows). Lower part terraces down the canyon slope with Armenian arched architecture; tower in bionic style (architect Zaza Verulashvili). Olympic-size pool, rooftop pool, spa club, fitness garden, private valley access, playground, 24/7 concierge, 5-level underground parking. Completion 2026.",
 apartments=[{"rooms":"1-3 bedroom","area_min":None,"area_max":None,"price_from":None,"currency":None}])]
save("30_parajanov",P)
