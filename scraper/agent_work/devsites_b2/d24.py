import sys,json; sys.path.insert(0,'.')
from mk import *
b={x['id']:x for x in json.load(open('milon_b.json'))['data']}
dev="Milon Mining"; du="https://www.milonmining.am/"; ph=["+37444940909","+37460770909","+37433940909"]; em="info@milonmining.am"
so={"facebook":"https://www.facebook.com/MilonMining.am","instagram":"https://www.instagram.com/milon.mining"}
P=[rec(source_url="https://www.milonmining.am/apartments?building=3",title="Milon Tower",developer=dev,developer_url=du,city="Abovyan",district="Kotayk",address="5/1 Friendship (Barekamutyun) Square, Abovyan",lat=40.271465,lng=44.618668,
 price_min_amd_m2=460000,price_currency_raw="460,000-533,000 AMD/m2 (available units via api.milonmining.am); from 17,000,018 AMD (35.1 m2)",completion="2027-10",status="under construction",floors="18",type="mixed",phones=ph,email=em,social=so,website=du,
 images=[b[3]['main_image']]+b[3]['images'][:11],
 description="Business-class multifunctional complex in the greenest part of Abovyan at Friendship Square 5/1 with shopping, entertainment and development centres; almost fully glazed facades for maximum daylight. 18 floors, ~456-461 apartments of 35.1-240 m2, parking; started Nov 2024, completion Oct 2027. Income tax refund applies; parking with 20% discount offer.",
 apartments=[{"rooms":"1","area_min":35.1,"area_max":35.1,"price_from":17000018,"currency":"AMD"},{"rooms":"2","area_min":40.2,"area_max":87.6,"price_from":20502000,"currency":"AMD"},{"rooms":"3","area_min":69,"area_max":96.1,"price_from":36570000,"currency":"AMD"},{"rooms":"4","area_min":89.1,"area_max":121.3,"price_from":46332000,"currency":"AMD"},{"rooms":"5","area_min":170.6,"area_max":174,"price_from":88740000,"currency":"AMD"}]),
 rec(source_url="https://www.milonmining.am/apartments?building=1",title="Milon Hills District",developer=dev,developer_url=du,city="Arinj",district="Kotayk",address="Arinj B district, 1st St 7, Abovyan community",lat=40.281379,lng=44.62814,
 price_min_amd_m2=550000,price_currency_raw="550,000-600,000 AMD/m2 (remaining units); 2-room 63.5 m2 from 34,925,000 AMD",completion="2026-09",status="under construction",floors="14",type="mixed",phones=ph,email=em,social=so,website=du,
 images=[b[1]['main_image']]+b[1]['images'][:11],
 description="Milon Hills district in Arinj B (Abovyan community): multifunctional residential complex with leisure venues, large park and separate townhouses. 14-floor building with 210 apartments of 47-165 m2 (6 still available), parking; started Sept 2023, completion Sept 2026.",
 apartments=[{"rooms":"2","area_min":63.5,"area_max":64,"price_from":34925000,"currency":"AMD"},{"rooms":"4","area_min":119,"area_max":119,"price_from":71400000,"currency":"AMD"}]),
 rec(source_url="https://www.milonmining.am/about",title="Milon Plaza",developer=dev,developer_url=du,city="Abovyan",district="Kotayk",address="5 August 23 St, Abovyan",completion="2025-12",status="completed",type="residential",phones=ph,email=em,social=so,website=du,
 description="Multi-apartment complex started 2021-2022 at 23 Augusti St 5 in Abovyan, distinctive architecture; 168 apartments of 50.5-324 m2 and 52 parking spaces; planned completion Dec 2025 (building permit extended). Sold out / not in current listings.")]
save("24_milon",P)
