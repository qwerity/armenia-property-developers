import rec, re, f
D = rec.Dev("43_teryan5", "Teryan 5 LLC", "https://www.teryan5.am/", ["+37411222225"], "info@teryan5.am",
            {"facebook": "https://www.facebook.com/teryan5.am/", "instagram": "https://www.instagram.com/teryan5.am/"})
u = "https://www.teryan5.am/"
im = []
for x in f.meta(u, f.get(u))["images"]:
    m = re.search(r"media/(9c3ead_[0-9a-f]+~mv2\.jpe?g|d8d584_[0-9a-f]+~mv2_d_\d+_\d+_s_2\.jpg)", x)
    if m:
        full = "https://static.wixstatic.com/media/" + m.group(1)
        if full not in im: im.append(full)
D.add(u, "Teryan 5", auto=False, district="Kentron", address="Vahan Teryan St 5", status="completed", type="mixed", images=im,
      description="Teryan 5: premium mixed-use building in downtown Yerevan with 75 exclusive glass-rich residences overlooking the city and Ararat, 113 parking lots, and a 173-room Courtyard by Marriott hotel on the lower floors (hotel operating). Common areas designed by Broadway Malyan (UK); 24/7 concierge, hotel room service, filtered fresh-air ventilation, high-speed lifts, centralized heating/cooling, fitness and spa centers, coffee shop.")
D.save()
