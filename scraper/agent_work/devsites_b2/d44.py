import sys; sys.path.insert(0,'.')
from mk import *
I="https://zoar.am/images/"
P=[rec(source_url="https://zoar.am/",title="ZOAR Residence",developer="Root Construct (Zoar)",developer_url="https://zoar.am/",city="Yerevan",district="Avan",address="Avan, Yerevan (40°13'29.1\"N 44°34'31.7\"E)",lat=40.22475,lng=44.575472,
 status="under construction",floors="16",type="residential",phones=["+37441221205"],email="root.construct.armenia@gmail.com",
 social={"facebook":"https://www.facebook.com/profile.php?id=100088731249504","instagram":"https://www.instagram.com/zoar_residence/"},
 images=[I+"structure-carousel/entrance_1.png",I+"structure-carousel/entrance_2.png",I+"structure-carousel/corridor_1.png",I+"structure-carousel/park_1.png",I+"structure-carousel/park_2.png",I+"structure-carousel/parking_1.png",I+"apartaments/apartament_1.png",I+"apartaments/apartament_2.png"],
 description="Residential building in an established neighbourhood with supermarket, shops and fast food on the ground floors, schools and transport nearby: 2 underground parking levels, 1 public floor and 15 residential floors with 106 apartments (48.6-151.8 m2), two premium lifts, security; only 27% site coverage leaving a large courtyard with park and playground; 4.5 m high lobby, 2.9 m wide corridors; individual gas heating, insulated aluminium windows, 9-point seismic resistance, A energy class, drainage system. Finishing packages: Standard, Comfort, Premium (interior design).",
 apartments=[{"rooms":"","area_min":48.6,"area_max":151.8,"price_from":None,"currency":None}])]
save("44_zoar",P)
