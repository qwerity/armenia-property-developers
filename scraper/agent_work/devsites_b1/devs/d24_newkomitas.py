import rec
D = rec.Dev("24_newkomitas", "Metta Group (New Komitas)", "https://newkomitas.am/", ["+37444471010", "+37455785505"], "komitascity1983@gmail.com",
            {"facebook": "https://www.facebook.com/New.Komitas", "instagram": "https://www.instagram.com/new_komitas", "youtube": "https://www.youtube.com/@NewKomitasResidentalComplex"})
M = "https://newkomitas.am/api/media/file/sites/site-komitas/originals/"
D.add("https://newkomitas.am/", "New Komitas", auto=False, lat=40.21397, lng=44.510243, district="Arabkir", address="Komitas Ave / Arghutyan St 15/7", status="under construction", completion="2027", floors="18", type="mixed",
      price_currency_raw="starting price 28M AMD (apartment)", images=[M + x + ".webp" for x in ["mcw54nv7xqm4ajtqb3181pkq", "yuq5lkq1ty9v4uiar2t0qzz8", "em7y9loovs3t2rsfpx3zulpg", "mtri5jos3vklu4z8tq4wk3ge", "c3ipz8phtoiu3rrxdb8k72pn", "t7iko0wvqxyzmw1sb83d0lfw", "z6dpx991l3rc1cbehhvn8tgx"]],
      videos=["https://www.youtube.com/watch?v=YfdILm-BV_M"],
      description="New Komitas: large residential district on Komitas Avenue in Arabkir by Metta Group (100,000+ sq m built in Sochi). 1,620 apartments, 18 floors, completion 2027, prices from 28M AMD. Seismic-resistant construction, energy-saving smart building systems, central heating/cooling (no gas), 3,123 underground parking spaces plus free surface parking, 24/7 security, 4 ha retail/leisure zone, 4-storey education complex with school and kindergarten, playgrounds, football/volleyball/tennis courts. Near Komitas park (0.3 km), school 55, Yeritasardakan metro 1.2 km. Cash, installment or mortgage.")
D.save()
