import sys; sys.path.insert(0,'.')
from mk import *
U="https://sophene.am/wp-content/uploads/"
P=[rec(source_url="https://sophene.am/",title="Sophene Club House",developer="Jacobs Shen LLC (Sophene)",developer_url="https://sophene.am/",city="Yerevan",district="Nork-Marash",address="26 Aghbyur Serob St, Yerevan",
 status="under construction",type="residential",phones=["+37499533332"],email="sales@sophene.am",
 social={"facebook":"https://www.facebook.com/SopheneClubHouse","instagram":"https://www.instagram.com/sophene.am"},
 images=[U+"2024/12/1-2-1-scaled.jpg",U+"2024/12/05-1-1-scaled.jpg",U+"2024/12/02-2-1-1-scaled.jpg",U+"2024/12/photo_2024-10-08_16-49-37.jpg",U+"2024/12/photo_2024-10-08_16-49-27.jpg",U+"2024/12/photo_2024-10-08_16-50-06.jpg",U+"2025/01/01-3.jpg",U+"2025/01/02-5.jpg",U+"2025/01/03-6.jpg"],
 description="Boutique luxury club house on an elevated site at Aghbyur Serob 26 with views of Ararat and the city skyline: 20 apartments of 73-136 m2, each with terraces and balconies in every bedroom; no commercial areas. Underground parking with car lift, 9.5-magnitude seismic design, Schuco triple-glazed windows, Mitsubishi Electric City Multi R2 VRF, Ostendorf soundproofed pipes, VIMAR systems, Thyssen lifts. Delivered with levelled walls/floors and insulation. Developer Jacobs Shen LLC; contractor Spitak Tnak; design Q Project / ARMAT.",
 apartments=[{"rooms":"","area_min":73,"area_max":136,"price_from":None,"currency":None}])]
save("20_sophene",P)
