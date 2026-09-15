import rec, json, re, html
D = rec.Dev("42_sundaytowers", "Up Development (Sunday Towers)", "https://www.sundayeveryday.am/", ["+37444100300"], "info@upd.am",
            {"facebook": "https://www.facebook.com/sundayeveryday.upd", "instagram": "https://www.instagram.com/sundayeveryday.upd"})
BASE = rec.BASE + "/cache/"
lst = {x["slug"]: x for x in json.load(open(BASE + "sunday_list.json"))["data"]} if False else None
L = {"b": (12, 1000000, 58554000, 63.75), "g": (6, 1400000, 79650000, 53.1), "d": (6, 1150000, 86254000, 61.61), "e": (6, 1150000, 72852500, 58.45), "z": (10, 1200000, 39994200, 39.01)}
GEN = ("Part of Sunday Towers (Up Development) at Gevorg Vardanyan 1/3, Arabkir: 6 architecturally distinct buildings, car-free courtyard with playground, pond and paths, 500+ parking spaces, kids club, gym, supermarket, bakery, coffee spot, outdoor pool and spa. Cascade and Victory Park 1.5 km. Income tax refund offer.")
gal_all = ["https://api.sundaytowers.am/storage/webp/" + x for x in ["8-min-671a1ebf89f61.webp", "6-min-673c692d50913.webp", "3g-min-671a1ec4d6276.webp", "20-min-671a1ebf75aa8.webp", "Sunday_Towers_Facilities_03-6716aa3a463d7.webp", "2-min-671a1ec50bd85.webp", "4-min-671a1ebfc3e8d.webp", "7-min-671a1ebf7326f.webp"]]
for b in "bgdez":
    d = json.load(open(BASE + f"sunday_{b}.json"))["data"]
    gal = [g["url"] for g in (d.get("gallery") or []) if g.get("type") == "image"]
    desc = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(d.get("blockDescription") or ""))).strip()
    desc = re.split(r" As part of| As a part of the larger| Residents will", desc)[0]
    fl, ppm, pmin, amin = L[b]
    D.add(f"https://sundaytowers.am/en/buildings/{b}/", f"Sunday Towers - Building {b.upper()}", auto=False, lat=40.19721, lng=44.50349, district="Arabkir", address="Gevorg Vardanyan St 1/3",
          status="under construction", completion=d.get("year"), floors=str(fl), price_min_amd_m2=ppm, price_currency_raw=f"from {ppm:,} AMD/sq m; apartments from {pmin:,} AMD",
          images=gal + gal_all, apartments=[{"rooms": "various", "area_min": amin, "price_from": pmin, "currency": "AMD"}],
          description=(desc + " " if len(desc) > 30 else f"Sunday Towers building {b.upper()}, {fl} floors, completion {d.get('year')}. ") + GEN)
D.add("https://sundaytowers.am/en/", "Sunday Towers - Building A", auto=False, lat=40.19721, lng=44.50349, district="Arabkir", address="Gevorg Vardanyan St 1/3", status="planned",
      images=["https://api.sundaytowers.am/storage/webp/8-min-671a1ebf89f61.webp"], description="Building A of Sunday Towers, marked 'Coming Soon' on the site. " + GEN)
D.save("data from api.sundaytowers.am/api/buildings; coords from site map widget")
