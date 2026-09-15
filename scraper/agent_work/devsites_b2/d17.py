import sys,re; sys.path.insert(0,'.')
from mk import *
from f import get
h=get('https://www.greenprojectarm.com/')
ids=[]
for m in re.findall(r'static\.wixstatic\.com/media/(bf6fcc_\w+~mv2\.\w+)',h):
    if m not in ids: ids.append(m)
W=lambda i:"https://static.wixstatic.com/media/"+i
byp=lambda p:[W(i) for i in ids if i.startswith("bf6fcc_"+p)]
gal=[W(i) for i in ids if i[7:15] not in ("70211aeb","ba142847","4866c9d2")]
dev="Green Project (Green Avan)"; du="https://www.greenprojectarm.com/"; ph=["+37494664522"]; em="sales@greenprojectarm.com"
so={"facebook":"https://www.facebook.com/greenprojectyerevan","instagram":"https://www.instagram.com/__green_project__","telegram":"http://t.me/greenprojectarm"}
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,social=so,website=du,**k)
P=[R(source_url=du+"#green-avan",title="Green Avan Residential Complex",city="Yerevan",district="Avan",address="Avan, Yerevan (40°13'27\"N 44°35'16\"E)",lat=40.224167,lng=44.587778,
  price_min_amd_m2=370000,price_currency_raw="from 370,000 AMD (per m2, early construction stage); mortgage from 10% down; income tax refund",status="under construction",type="residential",images=gal[:12],
  description="Residential complex in Avan with underground parking, 2 modern lifts, landscaped green area, outdoor recreation zone and children's playground. Apartments from 370,000 AMD/m2 at the initial construction stage; cash purchase on special terms or mortgage from 10% down payment; income tax refund law applies."),
 R(source_url=du+"#green-nork",title="Green Nork (Kanach Nork) residential buildings",city="Yerevan",district="Nor Nork",address="38/11 H. Gyurjyan St, Nor Nork, Yerevan",lat=40.18594,lng=44.551374,
  price_min_usd_m2=1200,price_currency_raw="from $1200 (per m2, initial stage)",floors="4",type="residential",images=byp("ba142847"),
  description="Four new 4-storey residential buildings at H. Gyurjyan St 38/11 in Nor Nork: underground parking (1 space per unit), 2 lifts, outdoor rest area, landscaped greenery, playground. From $1,200/m2 at the initial stage; cash or mortgage from 10% down."),
 R(source_url=du+"#green-townhouse",title="Green Townhouse Kasakh",city="Kasakh",district="Kotayk",address="Hovhannes Tumanyan St, Kasakh village, Nairi community, Kotayk",
  price_min_amd_m2=370000,price_currency_raw="1 m2 from 370,000 AMD; mortgage from 10% down; income tax refund",floors="2",type="residential",images=byp("4866c9d2"),
  description="Four modern two-storey townhouses in Kasakh village (Nairi community), 11 km from Republic Square: 98, 120, 124 and 141 m2, terrace, outdoor parking, landscaped grounds and playground. From 370,000 AMD/m2; cash or mortgage from 10% down; income tax refund.",
  apartments=[{"rooms":"townhouse","area_min":98,"area_max":141,"price_from":None,"currency":"AMD"}])]
save("17_greenavan",P)
