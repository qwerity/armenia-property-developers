import rec
from rec import imgs
D = rec.Dev("26_mountainvillage", "Mountain Village Dilijan", "https://mountainvillage.am/en", [], "sales@mountainvillage.am")
u = "https://mountainvillage.am/en"
im = [x.replace("http://", "https://") for x in imgs(u, "images/", r"mobile|heading_bg|master_plan|dilijan\.png", 20)]
D.add("https://mountainvillage.am/en/terraces", "Mountain Village - Terraces (Phase 1)", auto=False, city="Dilijan", district="Tavush", address="Dilijan", status="under construction", type="residential",
      images=im[:12], videos=["https://vimeo.com/1172248485"],
      description="Mountain Village Terraces: phase 1 of an exclusive clubhouse residential complex in Dilijan. Cascading premium building by Proforma inspired by cliffs and caves, 22 spacious apartments each with its own green terrace, 39 parking lots, individual lockers, co-working areas, playground and living room; delivered in white box with optional Scandinavian Chic / Basic+ interior packages. Green-building standards, professional property management, nearby tennis, pool, gym, basketball, football. Later phases: townhouses, apart-hotel, club house (phase 2) and premium cottages (phase 3).")
D.add(u, "Mountain Village - Townhouses, Apart Hotel & Club House (Phase 2)", auto=False, city="Dilijan", district="Tavush", address="Dilijan", status="planned", type="mixed",
      images=im[:4], description="Phase 2 of Mountain Village Dilijan master plan: townhouses, apart-hotel and club house next to the Terraces premium apartment building; shared sports facilities and property management.")
D.add(u, "Mountain Village - Cottages (Phase 3)", auto=False, city="Dilijan", district="Tavush", address="Dilijan", status="planned", type="residential",
      images=im[:4], description="Phase 3 of Mountain Village Dilijan master plan: premium-class cottages within the clubhouse residential community.")
D.save()
