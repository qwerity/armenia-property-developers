import sys; sys.path.insert(0,'.')
from mk import *
I="https://dgaconstruction.am/image/cache/catalog/BUILDINGS/"
P=[rec(source_url="https://dgaconstruction.am/",title="DGA Construction residential building (Hatis St, Abovyan)",developer="DGA Construction",developer_url="https://dgaconstruction.am/",city="Abovyan",district="Kotayk",address="1/85 Hatis St, Abovyan",lat=40.276018,lng=44.639694,
 price_min_amd_m2=500000,price_currency_raw="500,000 AMD/m2 (most units); up to 600,000 AMD/m2",status="under construction",floors="16",type="residential",phones=["+37433015509"],email="info@dgaconstruction.am",
 images=[I+"WhatsAppImage2024-09-27at10.54.48(1)-1441x732w.jpeg.webp",I+"WhatsAppImage2024-09-27at10.54.47(1)-1441x732w.jpeg.webp",I+"WhatsAppImage2024-09-27at10.54.47(2)-1441x732w.jpeg.webp",I+"WhatsAppImage2024-09-27at10.54.48-1441x732w.jpeg.webp"],
 description="Residential building in Abovyan by DGA Construction (which also runs concrete production and machinery). Interactive apartment selector lists ~97 apartments on floors 2-16 with 2 underground parking levels; 2- and 4-room layouts of 53-112 m2 (53-58, 63.5, 73-75, 87-88, 95-98, 111-112 m2). Price 500,000 AMD/m2 (select units 600,000).",
 apartments=[{"rooms":"2","area_min":53.8,"area_max":97.3,"price_from":None,"currency":"AMD"},{"rooms":"4","area_min":99.8,"area_max":111.3,"price_from":None,"currency":"AMD"}])]
save("12_dga",P)
