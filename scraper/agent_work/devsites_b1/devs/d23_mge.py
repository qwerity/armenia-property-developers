import rec
from rec import imgs
D = rec.Dev("23_mge", "MGE Construction", "https://mge.am/", ["+37444600809", "+37494140441", "+37411600088", "+37441600809"], "info@mge.am",
            {"facebook": "https://www.facebook.com/MiaTown2022", "instagram": "https://www.instagram.com/mia_town_mge_construction/"})
P = "https://mge.am/projects.php?id=%d&lang=en"
VIEWS = "Views: Aragats (north), Ararat (south), Zvartnots airport (west), Yerevan Lake and city panorama (east)."
u = P % 1
D.add(u, "Mia Town", auto=False, address="near North-South highway", status="under construction", images=imgs(u, "uploads/projects"),
      price_min_amd_m2=550000, price_currency_raw="550,000 AMD per sq m (apartments); commercial 800,000 AMD/sq m",
      apartments=[{"rooms": "2 bedrooms", "area_min": 57.01, "area_max": 60.57, "price_from": 31355500, "currency": "AMD"}, {"rooms": "3 bedrooms", "area_min": 83.08, "area_max": 83.08, "price_from": 45694000, "currency": "AMD"}, {"rooms": "4 bedrooms", "area_min": 134.78, "area_max": 153.36, "price_from": 74129000, "currency": "AMD"}],
      description="Mia Town: multi-apartment complex of three buildings near the North-South highway with 195 apartments plus commercial areas; 152-space parking on floors -1/-2; kindergarten, clinic, playground, 1,640 sq m green recreation area, 24/7 security, stained-glass windows. " + VIEWS)
u = P % 2
D.add(u, "Mia Residence", auto=False, address="near North-South highway, next to Mia Town", status="planned", floors="15", type="mixed", images=imgs(u, "uploads/projects"),
      description="Mia Residence: 15-storey complex of two buildings next to Mia Town with 210 apartments; parking on floors -1 to -3; floors 1-5 function as a shopping mall; playground, 1,640 sq m green area, 24/7 security, stained-glass windows. " + VIEWS)
u = P % 3
D.add(u, "NaMi Park", auto=False, address="", status="planned", images=imgs(u, "uploads/projects"),
      description="NaMi Park: new residential building with 65 apartments, contemporary architecture, children's playground and commercial spaces; school, kindergarten and park directly across the street. Location not specified on site.")
u = P % 4
D.add(u, "MGE Town Houses (Sayat-Nova village)", auto=False, city="Sayat-Nova", district="Ararat", address="Sayat-Nova village, Masis community", status="under construction", floors="2", images=imgs(u, "uploads/projects"),
      apartments=[{"rooms": "3 bedrooms", "area_min": 120, "area_max": 120}],
      description="Town Houses in Sayat-Nova village (Masis community), next to Masis city, 12.6 km from Yerevan: two-storey houses (60 sq m ground floor with living room, kitchen, bathroom; 60 sq m upper floor with 3 bedrooms), stained-glass windows, private 150 sq m yard with small swimming pool and recreation corner.")
D.save()
