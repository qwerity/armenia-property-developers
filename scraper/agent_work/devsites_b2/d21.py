import sys; sys.path.insert(0,'.')
from mk import *
U="https://leningradyan.am/wp-content/uploads/2024/04/"
dev="Total Shin LLC (Leningradyan Residence)"; du="https://leningradyan.am/"; ph=["+37455391919"]; em="info@leningradyan.am"
so={"facebook":"https://www.facebook.com/Leningradyan.Residence","instagram":"https://www.instagram.com/leningradyan_residence/","telegram":"https://t.me/+37455391919"}
P=[rec(source_url="https://leningradyan.am/en/",title="Leningradyan Residence",developer=dev,developer_url=du,city="Yerevan",district="Ajapnyak",address="19/12 Leningradyan St, Yerevan",
 price_min_amd_m2=500000,price_currency_raw="500,000-650,000 AMD per 1 sq.m.",completion="II half 2027",status="under construction",floors="16",type="residential",phones=ph,email=em,social=so,videos=["https://www.youtube.com/watch?v=L3vJn2GLOu8"],
 images=[U+"Գլխավոր-նկար_1-1024x576.jpg",U+"Հարմարավետ-պատշգամբներ_9-scaled.jpg",U+"Հարմարավետ-պատշգամբներ_4-scaled.jpg",U+"Կանաչ-զոնա-խաղահրաօարակ_3-scaled.jpg",U+"4-4-scaled.jpg",U+"Ստորգետնյա-ավտոկայանատեղիներ_1-scaled.jpg","https://leningradyan.am/wp-content/uploads/2025/11/332211.2.png"],
 description="Premium-class residence by Total Shin LLC (founded 2023) at Leningradyan 19/12 near the Karen Demirchyan sports-concert complex and Yerevan Park (Noy district): 3 blocks (A 86, B 75, G 86 apartments = 247), 16 storeys, apartments from 47.4 m2, penthouses with terraces, 173 underground parking lots, 1,236 m2 green zone, playground, fountain, public spaces on the 1st floor, individual gas. Delivered plastered with partitions, doors and windows. Cash, installments or mortgage (Fast Bank; young families programme). Completion H2 2027.",
 apartments=[{"rooms":"","area_min":47.4,"area_max":None,"price_from":None,"currency":"AMD"}])]
N="https://leningradyan.am/en/#projects"
for a,s,d,img in [("14","completed","Premium-class building with modern earthquake-resistant construction, underground parking and green yard.",U+"Մանուկ-Աբեղյան-14_2.jpg"),
                  ("17","completed","Monolithic premium-class building with parking and separate cooling system; delivered with iron door and aluminium triple-glazed windows.",U+"Մանուկ-Աբեղյան-17_3-scaled.jpg"),
                  ("19/1","under construction","Six-storey premium multi-apartment building in central Yerevan behind the Radio House near Yerevan State University, with a small green park; school, kindergarten, park and shops nearby.",U+"357x285-px.jpg")]:
    P.append(rec(source_url=N+"-abeghyan-"+a.replace("/","-"),title="Manuk Abeghyan "+a,developer="Nash Group LLC",developer_url=du,city="Yerevan",district="Kentron",address=a+" Manuk Abeghyan St, Yerevan",status=s,floors="6" if a=="19/1" else None,type="residential",phones=ph,email=em,social=so,images=[img],description=d+" Marketed by the Leningradyan Residence team (Nash Group LLC)."))
save("21_leningradyan",P)
