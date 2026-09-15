import rec, json, urllib.parse
D = rec.Dev("46_retroshin", "Retro Shin", "https://www.retroshin.am/", ["+37499998833"], "info@retroshin.am",
            {"facebook": "https://m.facebook.com/RetroShinAM", "instagram": "https://www.instagram.com/retroshinam/"})
p = json.load(open(rec.BASE + "/cache/retro_projects.json"))[0]
ar = json.load(open(rec.BASE + "/cache/retro_areas_offset_0_limit_100_sort_price_types_APARTMENT.json"))["areas"]
ppm = min(round(a["price"] / a["area"]) for a in ar)
F = "https://api.retroshin.am/admin/files"
D.add("https://www.retroshin.am/hy/buildings", "Atlantic Plaza", auto=False, lat=p["latitude"], lng=p["longitude"], district="Ajapnyak", address="Samvel Gevorgyan St 4", status="completed", completion="2023", floors="16", type="mixed",
      price_min_amd_m2=ppm, price_currency_raw=f"available apartments ~93 sq m from {min(a['price'] for a in ar):,} AMD (~{ppm:,} AMD/sq m)",
      images=[F + p["mediaMain"]["path"], F + "/D-3.jpeg", F + "/f--8--1.jpeg"],
      apartments=[{"rooms": "3", "area_min": 93.1, "area_max": 93.3, "price_from": min(a["price"] for a in ar), "currency": "AMD"}],
      description="Atlantic Plaza by Retro Shin at Samvel Gevorgyan 4, Yerevan: residential building (building A1) with 16 above-ground floors plus 2 underground parking levels, 218 units in total (28 available incl. parking), commercial real estate on the first floors, ~120 sq m office space, 140 sq m green area, 30+ parking spaces. Apartments marked completed/2023; remaining 3-room ~93 sq m units ~80.4-80.9M AMD. Mortgage available.")
D.save("from api.retroshin.am (single project)")
