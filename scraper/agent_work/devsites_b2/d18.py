import sys; sys.path.insert(0,'.')
from mk import *
dev="Green Rock Management Group"; du="https://greenrock.am/"
so={"facebook":"https://facebook.com/greenrock0/","instagram":"https://www.instagram.com/greenrock_managementgroup"}
U="https://greenrock.am/wp-content/uploads/"; B="https://greenrock.am/project/"
def R(**k): return rec(developer=dev,developer_url=du,social=so,city="Dilijan",district="Tavush",**k)
P=[R(source_url=B+"takhta-residential-complex/",title="Takhta Residential Complex",address="Dilijan, Tavush",status="planned",floors="up to 8",type="mixed",images=[U+"2026/05/Takhta-1.webp",U+"2026/05/Takhta-3.webp"],
  description="New premium residential complex in Dilijan designed by Green Rock with MVRDV, part of the Dilijan ecosystem (hotel, Art Park, Music Hall). Cascading terraces and facade inspired by layered Armenian rock formations; 3 building blocks up to 8 floors combining residential units for permanent living and hotel apartments, with ground-floor restaurants, retail, gym, pool and community space. Under design."),
 R(source_url=B+"multifunctional-complex/",title="Green Rock Multifunctional Complex Dilijan",address="Dilijan, Tavush",status="planned",type="mixed",images=[U+"2025/08/Hotel.webp",U+"2025/08/MusicHall.webp",U+"2025/08/ArtPark.webp",U+"2025/08/Villa3.webp",U+"2025/08/PPLS.webp"],
  description="~60,000 m2 ecosystem in the heart of Dilijan combining a 210-room hotel, 650-seat music hall, co-working, cafe, co-living and a public art park, connected by a covered escalator, hiking trails and bike lanes; 6 main facilities, 800+ new jobs. Under design."),
 R(source_url=B+"hotel/",title="Green Rock Hotel Dilijan",address="Dilijan, Tavush",status="planned",type="resort",images=[U+"2025/08/Hotel.webp"],
  description="Year-round hotel at the foot of the mountain near Dilijan within the Multifunctional Complex: 210 rooms, 3,000 m2 wellness area, 550+ seat conference centre, restaurants, retail, cinema and family spaces; 400+ jobs with training via the hospitality school. Under design."),
 R(source_url=B+"ppls-rooms/",title="PPLS Rooms Co-living",address="Dilijan, Tavush",status="completed",type="residential",images=[U+"2025/08/PPLS_1.jpg",U+"2025/08/PPLS_2.jpg",U+"2025/08/PPLS_4.jpg",U+"2025/08/PPLS_5.jpg",U+"2025/08/PPLS_6.jpg",U+"2025/08/PPLS_7.jpg"],
  description="Co-living housing in Dilijan for up to 200 residents (Green Rock employees, Apicius hospitality school students, ecosystem residents): shared rooms plus larger units on upper floors; adjacent new hospitality school building linked by a shared terrace."),
 R(source_url=B+"villa-3/",title="Villa3 Community Hub",address="Dilijan, Tavush",status="completed",type="commercial",images=[U+"2025/08/Vill3_1-683x1024.jpg",U+"2025/08/Vill3_3.jpg",U+"2025/08/Villa3_4.jpg",U+"2025/08/Villa3_5.jpg",U+"2025/08/Villa3_6.jpg",U+"2025/08/Villa3_7.jpg"],
  description="Coworking hub in a renovated building in Dilijan with workspaces, small lecture hall and rooftop terrace with panoramic views, landscaped surroundings; used for community events and workshops.")]
save("18_greenrock",P,{"skipped":"21 Hollywood (outside Armenia), Music Hall/Art Park/Cabinet cafe (public/F&B), Apicius, Meet Dilijan, Foundation"})
