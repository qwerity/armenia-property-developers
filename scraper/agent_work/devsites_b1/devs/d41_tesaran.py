import rec
from rec import imgs
D = rec.Dev("41_tesaran", "Tesaranshin (Tesaran Residence)", "https://tesaranresidence.am/en", ["+37493449744"], "info@tesaranresidence.am",
            {"facebook": "https://www.facebook.com/tesaran.residental", "instagram": "https://instagram.com/tesaran.residence"})
u = "https://tesaranresidence.am/en"
D.add(u, "Tesaran Residential Complex (private houses & townhouses)", auto=False, lat=40.262233, lng=44.533819, city="Kanakeravan", district="Kotayk", address="Kanakeravan village 2, Nor Hachn community, Kotayk", status="under construction", floors="2",
      images=imgs(u, "storage/|new_gen_plan"),
      apartments=[{"rooms": "4 (private house)", "area_min": 123, "area_max": 195.85}, {"rooms": "5 (townhouse)", "area_min": 173, "area_max": 178.9}, {"rooms": "villa", "area_min": 453, "area_max": 453}],
      description="Tesaran Residential Complex in Kanakeravan (Nor Hachn community, Kotayk) on an elevated site with views of Ararat, Aragats and Ara: 112 private houses and townhouses (houses 123-195.85 sq m, townhouses 173-178.9 sq m, villas 453 sq m; most early units sold out). Planned wellness and leisure park, tennis and basketball courts, swimming pools, restaurant (450 sq m), pump track, spa, gym, playgrounds, 24/7 security. Payment: houses 40% / townhouses 30% down, 50% over 14 months, 10% on handover; mortgage ~13.2%, income tax refund. Office Arami St 64 (Boulevard Plaza).")
D.save()
