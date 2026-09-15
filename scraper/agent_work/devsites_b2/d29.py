import sys; sys.path.insert(0,'.')
from mk import *
dev="Nut Construction"; du="https://townhouse.am/"; ph=["+37455522551","+37455455441","+37455455440"]; em="nutconstruction.sales@gmail.com"
so={"facebook":"https://www.facebook.com/nutconstruction.am","instagram":"https://www.instagram.com/nut.construction/"}
T="https://townhouse.am/img/"
yt=lambda i:"https://www.youtube.com/watch?v="+i
IM=sys.argv[1:] if len(sys.argv)>1 else []
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,social=so,city="Yerevan",district="Avan",type="residential",floors="3",**k)
P=[R(source_url=du+"nut-house.html",title="Nut House Townhouses",address="Avan-Arinj, Khachatur Abovyan district, 7th St, plot 12, Yerevan",status="completed",
  images=[T+f"1/real/nuthouse-{i}.jpg" for i in range(1,6)]+[T+f"1/rend/nuthouse-{i}.jpeg" for i in range(1,5)],videos=[yt("ih5b3ima4r4")],
  description="4 designer three-storey townhouses of ~150 m2 in Avan-Arinj (Khachatur Abovyan district), built with modern construction technology and premium materials; completed and in use.",apartments=[{"rooms":"townhouse","area_min":150,"area_max":150,"price_from":None,"currency":None}]),
 R(source_url=du+"rednut.html",title="Rednut Townhouses",address="Avan-Arinj, Khachatur Abovyan district, 10th St, plot 5, Yerevan",status="under construction",
  images=[u for u in IM if "/2/" in u][:10],videos=[yt("7Oa3nNHEACg")],
  description="4 elegant three-storey townhouses of 213.1 m2 with innovative design, panoramic views and large terraces in Avan-Arinj; ongoing, 360-degree view available.",apartments=[{"rooms":"townhouse","area_min":213.1,"area_max":213.1,"price_from":None,"currency":None}]),
 R(source_url=du+"whitenut.html",title="Whitenut Townhouses",address="Avan-Arinj, Khachatur Abovyan district, 2nd St, plot 29, Yerevan",status="under construction",
  images=[u for u in IM if "/3/" in u][:10],videos=[yt("qU2hZQlK7bk")],
  description="6 three-storey townhouses of 149 m2 in the heart of the Avan-Arinj neighbourhood with advanced engineering systems and smart solutions; ongoing.",apartments=[{"rooms":"townhouse","area_min":149,"area_max":149,"price_from":None,"currency":None}])]
save("29_nut",P,{"note":"custom private houses (Aramus, Arinj) skipped as individual orders"})
