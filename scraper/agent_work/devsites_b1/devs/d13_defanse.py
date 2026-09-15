import rec, re, f
D = rec.Dev("13_defanse", "Defanse Housing Invest", "https://defansehousing.com/", ["+37495020020", "+37495040040", "+37495060060", "+37411700007"], "info@defansehousing.com",
            {"facebook": "https://www.facebook.com/defansehousing/", "instagram": "https://www.instagram.com/defanse_housing/"})
B = "https://defansehousing.com/en/district/"
def im(slug):
    out = []
    for x in re.findall(r'https://defansehousing\.com/storage/images/(?:complexes|complex_blocks|gallery_images|levels)/[^"\'\s)]+\.(?:jpe?g|png|webp)', f.get(B+slug)):
        if x not in out: out.append(x)
    return out[:12]
COMMON = "Part of the 140 ha Defanse Housing district at Tichina 320 near the North-South highway (first district: 66 premium buildings on 43 ha, 40 ha central forest park). 10-point seismic resistance on basalt, fiber-cement ventilated cladding, granite lobbies, 2-5 room apartments of 50.77-192 sq m, panoramic aluminium windows, 15-16 floor buildings with 2 underground parking levels and central heating, 23-floor buildings with 3 parking levels and central heating/cooling, EV charging, parks, fountains, controlled access."
for letter, rng in [("a", "320/2-320/11"), ("b", "320/12-320/21"), ("g", "320/23-320/32"), ("d", "320/33-320/42"), ("e", "320/44-320/53"), ("z", "320/54-320/63")]:
    s = f"apartment-complex-{letter}"
    D.add(B+s, f'Defanse Housing - Residential complex "{letter.upper()}"', auto=False, district="Defanse Housing district", address=f"Tichina St {rng}", status="under construction", floors="15,16",
          images=im(s), description=f'Residential complex "{letter.upper()}" of the first residential district: 10 apartment buildings ({rng}). ' + COMMON)
for n in ["1", "22", "43"]:
    s = f"complex-of-apartment-buildings/building-320-{n}"
    D.add(B+s, f"Defanse Housing - Apartment building 320/{n}", auto=False, district="Defanse Housing district", address=f"Tichina St 320/{n}", status="under construction", floors="23",
          images=im(s), description=f"Standalone high-rise apartment building 320/{n} in the first residential district (23-floor tower type with 3 underground parking levels, central heating and cooling). " + COMMON)
D.add(B+"complex-of-apartment-buildings-2nd-phase", "Defanse Housing - Second residential district", auto=False, district="Defanse Housing district", address="Tichina St 320", status="planned",
      images=im("complex-of-apartment-buildings-2nd-phase"), description="Second phase of Defanse Housing district: second residential district of 42 residential buildings on 35 ha with a school and at least 2 kindergartens. District infrastructure: gas, Aparan water, separate sewage, 250 MW substation.")
D.add(B+"business-center", "Defanse Housing - Business center", auto=False, district="Defanse Housing district", address="Tichina St 320", status="planned", type="commercial",
      images=im("business-center"), description="Third phase of Defanse Housing district: business center of more than 500,000 sq m modelled on Paris La Defense, plus sport complex, trade center and multi-functional diagnostic and oncology centers.")
D.save("per-complex records; site has no coordinates or public prices")
