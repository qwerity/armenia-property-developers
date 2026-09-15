import rec, re, f
D = rec.Dev("05_arcada", "Arcada Construction", "https://arcada.am/", ["+37433310410", "+37441310410", "+37441210210"], "info@arcada.am",
            {"facebook": "https://www.facebook.com/kapavor"})
def info(u):
    h = f.get(u)
    ids = []
    for i in re.findall(r'"file_uniq_id":"(\w+)","file_name":"[^"]*","file_uniq_name":"\w+\.(?:jpe?g|png|webp)"', h, re.I):
        if i not in ids: ids.append(i)
    im = [f"https://arcada.am/file.php?class_name=default_model_item_file&file_uniq_id={i}&size_mode=2" for i in ids[:12]]
    m = re.search(r'"latitude":"([\d.]+)","longitude":"([\d.]+)"', h)
    lat, lng = (float(m.group(1)), float(m.group(2))) if m and float(m.group(1)) > 0 else (None, None)
    return dict(images=im, lat=lat, lng=lng, videos=rec.vids(u), auto=False)
P = "https://arcada.am/?app=AppProject&page="
u = P+"district&project_id=1"
D.add(u, "Greenville residential district", district="Davtashen", address="Tigran Petrosyan St 83", status="completed", completion="2022-08", floors="5",
      price_min_amd_m2=400000, price_currency_raw="from 400000 AMD (list page)", **info(u),
      description="Greenville residential district: 9 five-storey buildings, landscaped recreation zone, playground, sports ground, 24/7 security, 12,965 sq m total area, open parking; apartments from 62.5 sq m delivered with exterior door and windows, partitioned rooms, plastered walls, levelled floors; facade clad, quality lifts. Built 10/2019-08/2022, completion act 2022-08-02.")
u = P+"district&project_id=2"
D.add(u, "Griboyedov Park", district="", address="Griboyedov St 17", status="under construction", floors="14,15,16",
      price_min_amd_m2=390000, price_currency_raw="from 390000 AMD (subject to availability)", **info(u),
      description="Griboyedov Park: multi-apartment complex of 6 buildings with 14, 15 and 16 floors and two levels of underground parking; apartments from 50.8 sq m. Construction progress photos for sections 1-3 and 4-6 through 2026.")
u = P+"district&project_id=3"
D.add(u, "Arthouse", district="Davtashen", address="Zovuni, 30th St, 2nd lane 25 (next to Greenville, T. Petrosyan)", status="completed", completion="2022-09", floors="9",
      price_min_amd_m2=400000, price_currency_raw="from 400000 AMD (list page)", **info(u),
      description="Arthouse: complex of 2 nine-storey buildings with one underground parking level; apartments from 36.7 sq m, delivered with quality exterior door and windows, partitioned, plastered, levelled floors; clad facade and quality lifts. Completed 09/2022 (occupancy permit 2023-03-01).")
u = P+"district&project_id=4"
D.add(u, "Ember residential complex", district="Malatia-Sebastia", address="Monte Melkonyan St 24", status="under construction", floors="8,13",
      price_min_amd_m2=380000, price_currency_raw="from 380000 AMD (subject to availability)", **info(u),
      description="Ember: 2 buildings of 8 and 13 floors with three underground parking levels next to Yerevan Park (200 m); apartments from 37 sq m. Landscaped yard (2,590 sq m green area), playground and sports ground, gazebos, 9+ seismic resistance, 24/7 security, sound/thermal insulation, central heating/cooling with individual control. TUMO, Dalma Garden Mall, Sports-concert complex within 2-3 km. Construction permit 2024-12-09; progress photos to 08.2026.")
u = P+"district&project_id=5"
D.add(u, "Urmia residential complex", district="Davtashen", address="Tigran Petrosyan St 81/2", status="under construction", floors="17",
      price_min_amd_m2=400000, price_currency_raw="from 400000 AMD (subject to availability)", **info(u),
      description="Urmia: 2 buildings of 17 floors each (16 residential + 1 commercial) with two-level underground parking, next to Arcada's Greenville and Arthouse; apartments from 49 sq m, almost all with balconies. Landscaped yard, gazebos, 9+ seismic resistance, 24/7 security, insulation, gas supply. Delivered with door/windows, partitions, plaster, levelled floors. Construction permit 2025-12-26.")
u = P+"building&project_id=6"
D.add(u, "Ember Business Center", district="Malatia-Sebastia", address="Monte Melkonyan St 24/1", status="under construction", floors="4", type="commercial", **info(u),
      description="Ember Business Center next to Ember residential complex: reinforced-concrete frame on 1685 sq m plot, 3 underground floors (parking for 61-64 cars) and 4 above-ground floors; supermarket and food outlet on ground floor, offices above; 32 units, 1 passenger + 1 freight lift. Progress photos to 09.2026.")
D.save()
