import rec
from rec import imgs
D = rec.Dev("25_monumenthills", "Monument Hills", "https://monumenthills.am/", ["+37455054055"], "",
            {"facebook": "https://www.facebook.com/profile.php?id=100093405620312"})
g = imgs("https://monumenthills.am/gallery", "Images/", r"map|agi|Kids|stolica|75504765")
h = imgs("https://monumenthills.am/", "Images/", r"map|agi|Kids|stolica|75504765")
D.add("https://monumenthills.am/", "Monument Hills", auto=False, lat=40.201990787869654, lng=44.53072717179904, district="Kanaker-Zeytun", address="Davit Anhaght St 6", status="under construction", floors="15",
      images=(g + [x for x in h if x not in g])[:12], apartments=[{"rooms": "various", "area_min": 62, "area_max": 149}],
      description="Monument Hills: multi-apartment residential district of 3 buildings (A, B, C), 15 floors each, at Davit Anhaght 6 with views of Victory Park, Ararat and central Yerevan (Victory Park 1.3 km, Cascade 2.2 km). Apartments 62-149 sq m (combinable), 3 m ceilings; RC frame with 9-point seismic resistance, soundproof windows, lifts A-4/B-2/C-4, fire alarm and suppression, CCTV, intercom. 4,000 sq m green zone, 2-level parking with 260 spaces, EV charging, playground, gazebo, bike parking. Partner bank Inecobank.")
D.save()
