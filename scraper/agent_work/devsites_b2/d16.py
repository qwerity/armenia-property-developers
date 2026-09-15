import sys; sys.path.insert(0,'.')
from mk import *
dev="GTB Holdings"; du="https://gtbholdings.com/"; ph=["+37410272227","+37444072227"]; em="info@gtbholdings.com"
so={"facebook":"https://www.facebook.com/gtbholdings","instagram":"https://www.instagram.com/gtbholdings"}
U="https://gtbholdings.com/wp-content/uploads/"; B="https://gtbholdings.com/companies/"
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,social=so,**k)
P=[R(source_url=B+"gtb-tower/",title="GTB Tower",city="Yerevan",district="Arabkir",address="Komitas Market, Komitas Ave, Yerevan",status="under construction",floors="25",type="mixed",
  images=[U+"2025/04/tower-hero.webp",U+"2025/04/tower-1.webp",U+"2025/04/tower-2.webp",U+"2025/04/tower-3.webp",U+"2025/01/tower.jpg",U+"2025/04/tower-video.webp"],videos=["https://youtu.be/Q5SxNUZpsHU"],
  description="25-storey premium mixed-use tower rising above (behind) the iconic Komitas Market, preserving the market's cultural significance. Apartments on floors 7-22, three exclusive penthouses on the 23rd floor and three duplex penthouses on floors 24-25 with city views; lower floors commercial."),
 R(source_url=B+"gtb-anhaght/",title="GTB Anhaght",city="Yerevan",district="Kanaker-Zeytun",address="25 Davit Anhaght St, Yerevan",status="under construction",floors="8",type="mixed",
  images=[U+"2024/01/anhaght-header-1200x570.png",U+"2024/01/anhaght1.jpg",U+"2024/01/anhaght2.jpg",U+"2024/01/anhaght3.jpg",U+"2024/12/anhaght.jpg"],
  description="Contemporary residential complex with smart technology integration at Davit Anhaght 25, Kanaker-Zeytun: 8 floors (2 commercial/facility levels + 6 residential), two-level underground parking for residents and visitors."),
 R(source_url=B+"gtb-proshyan/",title="GTB Proshyan",city="Yerevan",district="Kentron",address="12 Proshyan St, Yerevan",status="planned",type="mixed",images=[U+"2025/04/proshyan-header.webp",U+"2025/01/proshyan.jpg"],
  description="Upcoming modern, practical multifunctional project on Proshyan St (GTB headquarters address); announced as coming soon."),
 R(source_url=B+"gtb-cascade/",title="GTB Cascade (Cascade completion and multifunctional complex)",city="Yerevan",district="Kentron",address="Cascade, Tamanyan St / Mother Armenia side, Yerevan",status="planned",type="mixed",
  images=[U+"2025/04/cascade-hero.webp",U+"2025/04/cascade-big.webp",U+"2025/04/cascade-big-1.webp",U+"2025/04/cascade-big-2.webp",U+"2025/04/cascade-small.webp",U+"2025/04/cascade-small-1.webp"],
  description="GTB Development project by architect Jean-Michel Wilmotte to complete the unfinished upper section of Yerevan's Cascade and connect it to the 'Reborn Armenia' monument, with a Cascade Cultural Hub (1,000-seat concert hall, museum of contemporary art, studios, leisure zones) that becomes public property, plus a new multifunctional complex on the right side of the Cascade.")]
save("16_gtb",P)
