import rec
from rec import imgs
D = rec.Dev("14_ecoshin", "Ecoshin Group", "https://ecoshingroup.am/", ["+37460500590", "+37455160015", "+37491490069", "+37455611100"], "info@ecoshingroup.am",
            {"facebook": "https://www.facebook.com/Ecoshingroup/", "instagram": "https://www.instagram.com/ecoshingroup/"})
u = "https://ecoshingroup.am/"
D.add(u, "Ecoshin - Orbeli residential complex", district="Arabkir", address="Orbeli Brothers St 67/2", status="completed", completion="2019-12", floors="15",
      images=imgs(u, "uploads", r"certificate|parking\.png|elevator|plan|clouds|info_bg|kayq"),
      apartments=[{"rooms": "2-4", "area_min": 55, "area_max": 150}],
      description="Ecoshin-Orbeli residential complex in Arabkir, 5 minutes by car from the centre with access from Kievyan St. Monolithic reinforced-concrete building with travertine and basalt cladding, 15 floors above ground and 3 underground parking levels (142 cars); 3 entrances each with passenger and freight lift; 2-4 room apartments of 55-150 sq m, all with open balconies viewing Hrazdan gorge and Ararat; delivered with levelled floors, plastered walls, door and windows (partitions optional). Landscaped yard with playground. Scheduled commissioning December 2019.")
D.save("single-project site; Kalinin 245/1 not on site")
