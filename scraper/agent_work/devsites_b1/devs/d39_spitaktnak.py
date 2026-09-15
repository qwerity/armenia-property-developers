import rec
from rec import imgs
D = rec.Dev("39_spitaktnak", "Spitak Tnak", "https://spitaktnak.am/", ["+37493712007", "+37410239181"], "salesgroup.spitaktnak@gmail.com", {"facebook": "https://www.facebook.com/spitaktnak/"})
u = "https://spitaktnak.am/en/current/nairi"
D.add(u, 'NAIRI residential public complex', auto=False, district="Arabkir", address="Paruyr Sevak St 51/2", status="under construction", floors="12,14,16", type="mixed",
      images=imgs(u, "storage/media/(current|complex|gallery)"),
      apartments=[{"rooms": "2-4", "area_min": 51, "area_max": None}],
      description="Nairi residential-public complex by Spitak Tnak on Paruyr Sevak St: 5 buildings (A and B 12 floors, C and D 14 floors, E 16 floors), 422 apartments of 2-4 rooms from 51 sq m, three-level underground parking for 330 cars, public service areas, separate green courtyard. Sales: +374 93 71 20 07.")
W = "https://spitaktnak.am/en/works/"
for slug, title, dist, addr, year, fl, n, amin, amax, extra in [
    ("multi-apartment-62-komitas-ave", "Multi-apartment complex 62 Komitas Ave", "Arabkir", "Komitas Ave 62", "2009", "14", 96, 56, 132, "two-level underground parking for 46 cars, individual heating, security systems"),
    ("residential-building-51-mamikonyants-str-51", "Residential building 51 Mamikonyants St", "Arabkir", "Mamikonyants St 51", "2006", "9", 42, 60, 120, "individual heating, yard"),
    ("residential-complex-12-charents-str", "Residential complex 12 Charents St", "Kentron", "Charents St 12", "2009", "12", 41, 62, 90, "one-level underground parking for 20 cars, central heating and air conditioning"),
    ("residential-complex-14-gulakyan-str", "Residential complex 14 Gulakyan St", "Arabkir", "Gulakyan St 14", "2009", "14", 52, 75, 100, "individual heating, security systems"),
    ("residential-complex-141-hrachya-nersisyan-str", "Residential complex 14/1 Hrachya Nersisyan St", "Arabkir", "Hrachya Nersisyan St 14/1", "2007", "7", 88, 75, 120, "one-level underground parking for 40 cars, individual heating, yard"),
    ("residential-complex-241-yer-kochar-str", "Residential complex 24/1 Yervand Kochar St", "Kentron", "Yervand Kochar St 24/1", "2009", "5", 20, 65, 95, "individual heating, security systems"),
    ("residential-complex-27-arabkir-str-16", "Residential complex 27th Arabkir St 1/6", "Arabkir", "Arabkir 27th St 1/6", "2013", "14", 46, 93, 146, "two-level underground parking for 36 cars, individual heating, yard"),
]:
    u = W + slug
    D.add(u, title, auto=False, district=dist, address=addr, status="completed", completion=year, floors=fl, images=imgs(u, "storage/media/work"),
          apartments=[{"rooms": "various", "area_min": amin, "area_max": amax}],
          description=f"{title}, Yerevan: multi-apartment building by Spitak Tnak put into operation in {year}; {fl} floors, {n} apartments of {amin}-{amax} sq m; {extra}; seismic resistant.")
D.save("Paruyr Sevak apartment complex works entry has no details (assumed = Nairi)")
