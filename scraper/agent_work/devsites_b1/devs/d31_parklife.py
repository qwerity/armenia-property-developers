import rec
from rec import imgs
D = rec.Dev("31_parklife", "Parklife Eco Residency", "https://parklife.am/", ["+37433925555"], "info@parklife.am",
            {"facebook": "https://www.facebook.com/profile.php?id=61563063566025", "instagram": "https://www.instagram.com/parklife_ecoresidency/"})
u = "https://parklife.am/en"
D.add(u, "Parklife Eco Residency", auto=False, district="Nor Nork", address="Bagrevand St 84, Nor Nork 2nd block", status="under construction", floors="2-3",
      images=imgs("https://parklife.am/", "storage/") + ["https://parklife.am/storage/%D5%B0%D5%A1%D5%BF%D5%A1%D5%AF%D5%A1%D5%A3%D5%AB%D5%AE/Trilogy_page-0001.jpg"],
      apartments=[{"rooms": "TRILOGY house (-1,1,2 floors + roof), plot 552.8 sq m", "area_min": 414.83, "area_max": 414.83}],
      description="Parklife Eco Residency: 20 ha eco residential district in the highest part of Yerevan (Nor Nork 2nd block) with views of Ararat, Aragats, Hatis, Ara and the whole city. 107 private houses of 6 types (Trilogy, Lunar, Hills, Quadro House, Inline) plus apartment buildings. E.g. Trilogy: 552.8 sq m plot, 414.83 sq m house over 3 levels with garage, roof 152 sq m, terraces. Planned kindergarten, medical center, church, business center, sports club with indoor/outdoor pools, shopping, EV charging, tennis and football fields, park with fountains, bike paths. Sales office Komitas 56.")
D.save()
