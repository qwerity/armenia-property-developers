import rec
from rec import imgs
D = rec.Dev("01_1sq", "1SQ", "https://1-sq.am/", ["+37455603613"], "info@1-sq.am",
            {"facebook": "https://www.facebook.com/share/1Ci85UbLYS/", "instagram": "https://www.instagram.com/1sq_estate_development"})
B = "https://1-sq.am/services/"
I = lambda u: imgs(u, "uploads", r"avtokayanateghi")
MG = "1SQ acts as development/project manager."
u = B+"davtashen-3th-district-105-106-areas/"
D.add(u, "Davtashen 3rd district, plots 105-106", district="Davtashen", address="Davtashen 3rd district, plots 105-106", status="under construction", floors="5",
      phones=["+37455603613", "+37455200707"], images=I(u),
      description="Planned multi-apartment building on plots 105-106 of Davtashen 3rd district: 5 residential floors (top floor mansard) plus basement; 32 apartments (mostly 2-room, some 1- and 3-room); 8 underground parking spaces; landscaped yard. Sales via ARGO Realty (+374 55 200 707).")
u = B+"karapet-ulnetsi-58-20/"
D.add(u, "Karapet Ulnetsi 58/20", district="Arabkir", address="Karapet Ulnetsi St 58/20", status="completed", images=I(u),
      description="Multi-apartment complex of three residential buildings in one of the greenest, ecologically cleanest parts of Yerevan with panoramic city views. Listed under 1SQ finished projects. "+MG)
u = B+"28-5-sahmanadrutyan-square-hrazdan-city/"
D.add(u, "Hrazdan, Sahmanadrutyan Square 28/5", city="Hrazdan", district="Kotayk", address="Sahmanadrutyan Square 28/5, Hrazdan", status="under construction", floors="15", images=I(u),
      description="15-storey residential building in Hrazdan combining classical and modern style, high seismic resistance; ground floor commercial/public spaces; 16 underground parking spaces; passenger (8) and freight (12) lifts; CCTV, fire alarm, security, backup power and water. Apartments delivered in white frame (partitions, plastered floors, gypsum walls, entrance door and windows, no interior finishing). Landscaped yard.")
u = B+"dalan-technologies/"
D.add(u, "Dalan Technopark", district="Kanaker-Zeytun", address="Tsitsernakaberdi highway 9/1", status="under construction", floors="22", type="commercial",
      images=imgs(u, "uploads/2025|uploads/2024/11") + ["https://1-sq.am/wp-content/uploads/2024/10/dalan.jpg"],
      description="Dalan Technopark - the largest project managed by 1SQ: a technology and business center 10 minutes from central Yerevan built to LEED and BOMA standards. 154,000 sq m total, 22 floors, ~3000 office workplaces: 34,300 sq m class-A offices, 5,500 sq m exhibition hall, 1,600 sq m conference hall, 500 sq m event hall, 1000+ parking spaces, 4,300 sq m sports center with pool, 9,000 sq m hotel, 6,000 sq m restaurants/food court.")
u = B+"isakov-12-11/"
D.add(u, "Tsovakal Isakov 12/11", district="Erebuni", address="Tsovakal Isakov Ave 12/11", status="under construction", images=I(u),
      description="Residential complex on Admiral Isakov Avenue: 239 apartments, 150 underground parking spaces; high seismic standards, quality facade, CCTV, fire alarm, 24/7 security, 2 lifts (8 and 12 persons) per building, designer finished lobbies, landscaped territory.")
u = B+"level-16/"
D.add(u, "LEVEL 16 (Leningradyan 29/17)", district="Ajapnyak", address="Leningradyan St 29/17, Noy district", status="under construction", floors="14,16", images=I(u),
      description="LEVEL 16: residential complex in Noy district of two sections with 14 and 16 floors above ground and 3 underground levels. 196 apartments, 144 underground parking spaces, 667 sq m of commercial space on the ground floors; CCTV, fire systems, 24/7 security, 2 lifts per building (8 and 12 persons), finished lobbies, landscaped territory. Online construction camera available.")
u = B+"%d5%a1%d5%b6%d5%a1%d5%bd%d5%bf%d5%a1%d5%bd-%d5%b4%d5%ab%d5%af%d5%b8%d5%b5%d5%a1%d5%b6-2-3/"
D.add(u, "Anastas Mikoyan 2/3", district="Ajapnyak", address="Anastas Mikoyan St 2/3", status="completed", floors="16", images=I(u),
      apartments=[{"rooms": "various", "area_min": 47, "area_max": 147}, {"rooms": "penthouse", "area_min": 200, "area_max": 200}],
      description="16-storey residential building: ground floor commercial spaces of 38.3-189.8 sq m with large shop windows and ~4 m ceilings; floors II-XV apartments of 47-147 sq m, most with separate kitchens; floor XVI has two premium penthouses of 200 sq m. ~40 cm insulated pumice-block exterior walls with ventilated energy-saving facade. Finished project.")
u = B+"%d5%bf%d5%ab%d5%a3%d6%80%d5%a1%d5%b6-%d5%b4%d5%a5%d5%ae-47-1/"
D.add(u, "Tigran Mets 47/1", district="Kentron", address="Tigran Mets Ave 47/1", status="completed", images=I(u),
      apartments=[{"rooms": "1-4", "area_min": 52, "area_max": 128}],
      description="Residential buildings on Tigran Mets Avenue with designer layouts; every apartment has a balcony; 1- to 4-room apartments from 52 to 128 sq m; larger units have two bathrooms. Finished project.")
u = B+"town-house/"
D.add(u, "Town House (Silikyan)", district="Shengavit", address="Silikyan district", status="completed", images=I(u),
      description="Town House residential complex in Silikyan district, commissioned: 26 detached houses, each with its own garage. 1SQ manages the neighbourhood.")
u = B+"kechi/"
D.add(u, "Kechi hotel-residential complex", city="Tsaghkadzor", district="Kotayk", address="Kechi Residence, Tsaghkadzor", status="completed", type="resort", images=I(u),
      description="'Kechi' hotel and residential complex (Kechi Residence) in Tsaghkadzor resort town. "+MG)
u = B+"arghishti-48-8/"
D.add(u, "Argishti 48/8", district="Kentron", address="Argishti St 48/8", status="completed", floors="4", images=I(u),
      description="Residential building at Argishti 48/8 with 4 floors above ground and 1 underground, distinctive exterior style, seismic standards, high-quality facade, CCTV, fire alarm, 24/7 security. "+MG)
u = B+"zeytun/"
D.add(u, "Zeytun, 10th street 15", district="Kanaker-Zeytun", address="10th St 15, Zeytun", status="completed", floors="4", images=I(u),
      description="4-storey residential building in Kanaker-Zeytun with 12 apartments and 8-car underground parking; commissioned with fully landscaped green yard (construction completed). "+MG)
u = B+"kievyan/"
D.add(u, "Kievyan Residence", district="Arabkir", address="Barbyusi St 66", status="completed", floors="7", images=I(u),
      description="Kievyan Residence: modern premium complex with 7 floors above ground and 3 underground, 40 apartments with panoramic views of Kievyan bridge, Hrazdan gorge and Mount Ararat. On the slope of Hrazdan gorge next to Kievyan bridge and SAS supermarket at Barbyusi 66; mostly glass facade; 2 underground parking levels, 2 commercial floors and 6 residential floors; reception, lounge, 24/7 concierge.")
u = B+"verin-antarayin/"
D.add(u, "Verin Antarayin 136/11", district="Kentron", address="Verin Antarayin St 136/11", status="completed", images=I(u),
      description="Residential building at Verin Antarayin 136/11. "+MG)
u = B+"arev/"
D.add(u, "Arev premium residential complex", district="Kentron", address="Khanjyan St 9/3", status="completed", images=I(u),
      description="'Arev' premium-class residential complex on Khanjyan street, central Yerevan. "+MG)
u = B+"ulneci-32-10/"
D.add(u, "Karapet Ulnetsi 32/10", district="Arabkir", address="Karapet Ulnetsi St 32/10", status="completed", images=I(u),
      description="Residential building at Karapet Ulnetsi 32/10. "+MG)
u = B+"sevak-5/"
D.add(u, "Paruyr Sevak 5", district="Arabkir", address="Paruyr Sevak St 5", status="completed", images=I(u),
      description="Residential building at Paruyr Sevak 5; apartment handover started (per 1SQ news). "+MG)
u = B+"halabyan-75-1/"
D.add(u, "Halabyan Residence (Halabyan 75/1)", district="Ajapnyak", address="Halabyan St 75/1", status="completed", images=I(u),
      description="Halabyan Residence at Halabyan 75/1; completion act received (per 1SQ news). "+MG)
u = B+"sevqareci/"
D.add(u, "Sevkaretsi Sako 77", district="Erebuni", address="Sevkaretsi Sako St 77", status="under construction", floors="6", phones=["+37455603613", "+37455200707"], images=I(u),
      description="Building with 1 underground and 6 above-ground floors (top floor set back): 15 apartments (3 per typical floor, 2 on top), 1 apartment and a 79.1 sq m commercial space on the ground floor, 12-car underground parking also designed as shelter; flat roof, fire-rated stair doors. Sales via ArGo Realty +374 55 200707.")
u = B+"ashtarak_yerevanyan_2/"
D.add(u, "Ashtarak, Yerevanyan street 2/10", city="Ashtarak", district="Aragatsotn", address="Yerevanyan St 2/10, Ashtarak", status="under construction", floors="14,15", phones=["+37455603613", "+37455200707"], images=I(u),
      description="Planned multi-apartment complex in Ashtarak (Aragatsotn): buildings A (14 residential floors) and B (15 residential floors) with accessible roof terraces, commercial spaces on semi-basement and ground floors, separate semi-underground public building. 253 apartments, 97 underground parking spaces, 1993.61 sq m public space. Sales via ARGO Realty +374 55 200 707.")
D.save()
