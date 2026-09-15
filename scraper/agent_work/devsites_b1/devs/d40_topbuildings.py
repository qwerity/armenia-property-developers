import rec, re, f
D = rec.Dev("40_topbuildings", "TOP BUILDINGS", "https://topbuildings.am/", ["+37433583333", "+37411253333"], "info@topbuildings.am",
            {"facebook": "https://www.facebook.com/profile.php?id=61555972335140", "instagram": "https://www.instagram.com/top_buildings_armenia/"})
u = "https://topbuildings.am/"
im = []
for x in re.findall(r'https://topbuildings\.am/image/cache/catalog/img/[^"\s]+?-980x1280[wh]\.JPG\.webp|https://topbuildings\.am/image/cache/catalog/img/image_hero[^"\s]+', f.get(u)):
    if x not in im: im.append(x)
D.add(u, "TOP BUILDINGS (Ashkhabad 9/2)", district="Avan", address="Ashkhabad St 9/2, Avan", status="under construction", completion="2026-09", floors="16",
      price_min_amd_m2=410000, price_currency_raw="410,000-475,000 AMD per sq m (apartment list)", images=im,
      apartments=[{"rooms": "1", "area_min": 43.7, "area_max": 44.0, "price_from": 30590000, "currency": "AMD"}, {"rooms": "2", "area_min": 58.5, "area_max": 74.6, "price_from": 27495000, "currency": "AMD"},
                  {"rooms": "3", "area_min": 65.8, "area_max": 102.7, "price_from": 30926000, "currency": "AMD"}, {"rooms": "4", "area_min": 127.8, "area_max": 127.8, "price_from": 95850000, "currency": "AMD"},
                  {"rooms": "5", "area_min": 126.8, "area_max": 160.3, "price_from": 59596000, "currency": "AMD"}],
      description="TOP BUILDINGS: 16-storey residential complex in Avan (Ashkhabad St 9/2) with stylish architecture, bright spacious apartments with stained-glass windows and penthouses on top floors. 118 apartments (1-5 rooms, 43.7-160.3 sq m, 3 m ceilings), 76 parking spaces on 2 underground levels, 2 lifts, 1,980 sq m site with landscaped garden and playground, security post, gas, commercial spaces; school, supermarket, kindergarten nearby. Construction completion September 2026. Prices ~410-475k AMD/sq m.")
D.save()
