import rec, re, f
D = rec.Dev("20_ivygarden", "IVY Garden LLC (PJKT Development)", "https://www.ivygarden.am/", ["+37493041002"], "info@ivygarden.am",
            {"instagram": "https://instagram.com/ivygarden.am/"})
u = "https://www.ivygarden.am/"
im = []
for x in f.meta(u, f.get(u))["images"]:
    m = re.search(r"media/(cf0b6c_[0-9a-f]+~mv2\.(?:jpe?g|png))", x)
    if m and "w_1440" in x or (m and "blur" in x):
        full = "https://static.wixstatic.com/media/" + m.group(1)
        if full not in im: im.append(full)
D.add(u, "IVY Garden", district="Nork-Marash", address="Armenakyan St 108/7", status="under construction", images=im,
      apartments=[{"rooms": "1 bedroom", "area_min": 65, "area_max": 65}, {"rooms": "2 bedrooms", "area_min": 101, "area_max": 116}, {"rooms": "3 bedrooms", "area_min": 181, "area_max": 181}],
      description="IVY Garden: premium residential complex at Armenakyan 108/7 in Nork-Marash, elevated ecologically clean area 2.5 km from the city centre with views of the city and Mount Ararat. Land 1,662.99 sq m including 913.23 sq m green space with park and playgrounds. Apartments: 1-bedroom 65 sq m, 2-bedroom 101-116 sq m, 3-bedroom 181 sq m with 3 bathrooms and 2 balconies. Construction process page and public contract published. Developer PJKT Development.")
D.save()
