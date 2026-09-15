import sys; sys.path.insert(0,'.')
from mk import *
I="https://layeghvard.am/news_images/"
P=[rec(source_url="https://layeghvard.am/",title="Los Angeles Yeghvard Townhouses",developer="House Construction LLC (LA Yeghvard)",developer_url="https://layeghvard.am/",city="Yeghvard",district="Kotayk",address="Azatamartikneri district, 11th St 47-51, Yeghvard",
 completion="IV 2026",status="under construction",floors="2",type="residential",phones=["+37433831631","+37491811113"],email="layeghvard@gmail.com",
 social={"facebook":"https://www.facebook.com/layeghvard","instagram":"https://www.instagram.com/layeghvard/"},videos=["https://www.youtube.com/watch?v=ARgSDpRY2sI"],
 images=[I+"1_13_big.jpg",I+"1_14_big.jpg",I+"1_15_big.jpg",I+"1_16_big.jpg",I+"1_5_big.jpg",I+"1_8_big.jpg",I+"1_9_big.jpg",I+"1_10_big.jpg","https://layeghvard.am/images/index-9-1047x531.png"],
 description="'Los Angeles' district of 23 modern townhouses in green, quiet Yeghvard, 10 minutes from Yerevan, with views of Ararat, Aragats and Ara and near St. Sargis church. Each 160 m2: 40 m2 yard, 44.2 m2 ground floor, 53 m2 upper floor, 40.9 m2 flat usable roof, 13.7 m2 closed kitchen. Modern stone, metal structures and large glazing; energy-efficient. Delivered plastered with water, electricity and gas. Sold by the developer with income-tax refund and flexible payment; completion end of 2026.",
 apartments=[{"rooms":"townhouse","area_min":160,"area_max":160,"price_from":None,"currency":None}])]
save("22_layeghvard",P)
