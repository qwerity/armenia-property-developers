import rec
from rec import imgs
D = rec.Dev("19_haus", "Haus AM", "https://haus.am/", ["+37444084411"], "info@haus.am",
            {"facebook": "https://www.facebook.com/hausamllc", "instagram": "https://www.instagram.com/haus__am"})
TAX = " Sold directly by developer; mortgage (0% down payment offer, from 12.5%) and income-tax refund up to 500,000 AMD/month."
H = [("a1", "House A1", 155, 400, 3, 2, "M. Mkrtchyan district", "completed", None, None, "finished with pool, pergolas, landscaped yard, 2-car parking"),
     ("a2", "House A2", 155, 400, 3, 2, "M. Mkrtchyan district", "completed", None, None, "finished with pool, pergolas, landscaped yard, 2-car parking"),
     ("a3", "House A3", 155, 375, 3, 2, "M. Mkrtchyan district", "completed", None, None, "white-frame delivery (frame, walls, metal roof, fence, doors/windows, facade, gas/water/power connections)"),
     ("a4", "House A4", 155, 375, 3, 2, "M. Mkrtchyan district", "completed", None, None, "white-frame delivery (frame, walls, metal roof, fence, doors/windows, facade, gas/water/power connections)"),
     ("a5", "House A5", 131, 375, 3, 2, "M. Mkrtchyan district", "under construction", "2026", 79000000, "white-frame delivery (frame, walls, metal roof, fence, doors/windows, facade, utility connections)"),
     ("b1", "House B1", 175, 400, 4, 2, "M. Mkrtchyan district", "completed", None, None, "finished with pool, pergolas, landscaped yard, 2-car parking"),
     ("t12", "Townhouse T12", 177, 225, 3, 2, "P. Sevak district", "completed", None, None, "monolithic RC house, living-kitchen, 3 bathrooms, balcony, summer kitchen/terrace"),
     ("v1", "House V1", 174, 400, 4, 3, "B district", "under construction", "2025", 80000000, "white-frame delivery (frame, walls, metal roof, fence, doors/windows, facade, utility connections)")]
for slug, title, area, land, bed, fl, dist, st, comp, price, extra in H:
    u = f"https://haus.am/list/{slug}"
    kw = {}
    if price:
        kw = dict(price_currency_raw=f"special price {price:,} AMD (house + {land} sq m land)", apartments=[{"rooms": f"{bed} bedrooms", "area_min": area, "area_max": area, "price_from": price, "currency": "AMD"}])
    else:
        kw = dict(price_currency_raw="sold", apartments=[{"rooms": f"{bed} bedrooms", "area_min": area, "area_max": area}])
    D.add(u, f"Haus AM {title} (Arinj)", auto=False, city="Arinj", district="Kotayk", address=f"Arinj, {dist}", status=st, completion=comp, floors=str(fl),
          images=imgs(u, "haus.am/(list/)?img/"), videos=[v.split("?")[0].replace("/embed/", "/watch?v=") for v in rec.vids(u)][:1],
          description=f"{title}: {fl}-storey private house of {area} sq m on a fenced {land} sq m plot in Arinj ({dist}), {bed} bedrooms, ~1.4 km from Babajanyan St (Avan); {extra}." + (" Status: sold." if st == "completed" else "") + TAX, **kw)
D.save("individual houses in Arinj; land-plot listings (L1/L2) skipped")
