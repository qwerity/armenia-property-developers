import rec
from rec import imgs
D = rec.Dev("37_seray", "Seray Homes (Seray Developments)", "https://seraydevelopments.com/", ["+9613251800"], "",
            {"facebook": "https://www.facebook.com/seraydevelopments/", "instagram": "https://www.instagram.com/seraydevelopments/"})
P = "https://seraydevelopments.com/portfolio/"
X = r"_c\.jpg"
LOC = "on the Verin Antarayin residential hill just above the Cascade, central Yerevan, with south views to the city and Ararat and north views over Saralanji highway"
SPEC = " Monolithic RC structure, travertine/basalt cladding, European tiles and parquet, PVC double-glazed windows, BAXI boiler heating, split A/C, Grohe sanitary ware, marble lobby, CCTV, videophone, lift."
u = P + "otevan-residence-apartments-for-sale-in-yerevan-armenia/"
D.add(u, "Otevan Residence (Otevan 1)", auto=False, district="Kentron", address="Verin Antarayin, above Cascade", status="completed", floors="4",
      images=imgs(u, "uploads/", X), videos=["https://www.youtube.com/watch?v=" + v.split("embed/")[1].split("?")[0] for v in rec.vids(u)][:6],
      apartments=[{"rooms": "various", "area_min": 50, "area_max": 170}],
      description=f"Otevan Residence (Otevan 1) by Lebanese developer Seray Developments, {LOC}. Turn-key building of 20 apartments over four floors (50-170 sq m) plus a 20 sq m office, flexible layouts; fully finished." + SPEC)
u = P + "otevan-residence-2/"
D.add(u, "Otevan 2", auto=False, district="Kentron", address="Verin Antarayin, above Cascade", status="under construction", images=imgs(u, "uploads/", X + r"|80x80"),
      description=f"Otevan 2: current Seray Developments turn-key residential building in the Otevan series, {LOC}; typical floor plans downloadable." + SPEC)
u = P + "otevan-3/"
D.add(u, "Otevan 3", auto=False, district="Kentron", address="Verin Antarayin, above Cascade", status="completed", floors="4", images=imgs(u, "uploads/", X),
      apartments=[{"rooms": "various", "area_min": 50, "area_max": 170}],
      description=f"Otevan 3 (past project), blocks A and B, {LOC}; apartments 50-170 sq m. Monolithic RC per European code, 30 cm thermo-insulated clay-brick walls, fair-faced concrete and glass balustrades, aluminium double-glazed windows, granite lobby, glass curtain wall on staircase.")
u = P + "otevan-4/"
D.add(u, "Otevan 4", auto=False, district="Kentron", address="Verin Antarayin, above Cascade (Otevan series)", status="planned", images=[],
      description="Otevan 4: future Seray Developments project in the Otevan series in Yerevan; project info not yet published (specs: monolithic RC, thermo-insulated clay brick, aluminium double glazing).")
D.save()
