import rec
from rec import imgs
D = rec.Dev("04_amanoo", "Khakhamyan Heritage (AMANOO)", "https://www.amanoo.am/", ["+37433031100", "+37491000107"], "info@amanoo.am",
            {"facebook": "https://www.facebook.com/amanooyerevan", "instagram": "https://www.instagram.com/amanoo_yerevan/", "youtube": "https://www.youtube.com/@khakhamyanheritage4732"})
A = "G. Hovsepyan St 38/11, Nork"
u = "https://www.amanoo.am/en/ivy/"
D.add(u, "IVY at AMANOO", district="Nork-Marash", address=A, status="completed", floors="4-6",
      images=imgs(u, "uploads/20", r"amanoodark|thumbs"),
      apartments=[{"rooms": "1-4 bedroom, duplex, penthouse", "area_min": 60, "area_max": 430}],
      description="IVY - first completed project of the gated AMANOO green district on the Nork slope, 2.5 km from Yerevan centre. 1 ha plot with only 50 residences in four buildings (Ivy 1-4) of 4-6 floors, inspired by ivy leaves; 1-4 bedroom flats, duplexes and penthouses; 3.4 m clear ceilings (4.2 m in top-floor units), floor-to-ceiling windows, private landscaped terraces, rooftop gardens with private pools. Landscape with lake, river, waterfall, alleys, underground parking. Ready for occupancy.")
u = "https://www.amanoo.am/en/sarin/"
D.add(u, "Sarin at AMANOO", district="Nork-Marash", address=A, status="under construction", completion="2028", floors="4-7",
      images=imgs(u, "uploads/20", r"amanoodark|thumbs|hark"),
      apartments=[{"rooms": "various", "area_min": 51, "area_max": 550}],
      description="Sarin - AMANOO district project on 1.5 ha inspired by the Armenian Highlands; construction 2024-2028. Apartments 51-550 sq m in a 4-7 floor building using biomimicry/biophilic design, 75% green area, lake and waterfall facade views, rooftop greenery and pools. Amenities: 100 sq m gym, indoor pool with 7 m ceiling, 9 open-air pools, 125 resident + 22 guest parking spaces, 4 elevators, 7 entrances, playground, childcare centre, 300 sq m reception lounge, 11 waterfalls, helipad. 3D tour available.")
D.save()
