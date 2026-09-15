import rec, re, f
D = rec.Dev("08_monterosso", "Azbuka Development RA (Monterosso)", "https://monterosso.am/en", ["+37493388055", "+37493137115", "+37443710242"], "official-am@azbuka.am",
            {"facebook": "https://www.facebook.com/share/193pkubMhe/", "instagram": "https://www.instagram.com/monterosso_yerevan"})
u = "https://monterosso.am/en"; h = f.get(u); im = []
for x in re.findall(r'https://static\.tildacdn\.net/tild[\w-]+/[\w.-]+\.(?:jpe?g|webp)', h):
    if x not in im: im.append(x)
D.add(u, "Monterosso", district="Nork-Marash", address="Garegin Hovsepyan St 52/5", status="under construction", floors="5", images=im[:12],
      videos=[], description="Monterosso by Azbuka Development: business-class residential complex in Nork-Marash with Italian-inspired architecture, 10,000 sq m complex area at 1,164 m altitude, 5-floor buildings with 4-6 apartments per floor. Ergonomic 1-3 bedroom layouts, terraces, master bedrooms, walk-in closets, laundry rooms, panoramic views of Yerevan and Ararat. Landscaped courtyard, rooftop lounge, lobby, underground parking and storage cellars. 3 min walk to new park, 7 min to city centre. Sales open (parking as gift promo); sales office Verin Antarayin 138/2. 3D tours available.")
D.save()
