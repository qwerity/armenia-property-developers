import rec
from rec import imgs
D = rec.Dev("17_goght", "Goght Urban Valley", "https://goghtvalley.com/en", ["+37433753377"], "info@goghtvalley.com",
            {"facebook": "https://www.facebook.com/people/Goght-Urban-Valley/100090218746804/", "instagram": "https://www.instagram.com/goght.valley/"})
u = "https://goghtvalley.com/en"
D.add(u, "Goght Urban Valley", city="Goght", district="Kotayk", address="Goght village, Garni community, Kotayk", status="under construction", floors="1-2", type="mixed",
      images=imgs(u, "storage/"), videos=["https://www.youtube.com/watch?v=eWF79iNxlMA"],
      apartments=[{"rooms": "villa 1-2 storey (A/B/D/N types)", "area_min": 118, "area_max": 229}, {"rooms": "duplex / small villa (E types), 2 bedrooms", "area_min": 73.5, "area_max": 86.15}],
      description="Goght Urban Valley: 'city within a city' in Goght village (Garni community, Kotayk) at the foot of Khosrov Forest Reserve with Ararat views. 70 ha total with 55 ha green zone, ~140 villas and 20 apartments; 1-2 storey villas by Black Architects, ARCH Coop, Kljyan Archi Bureau, UrUrban (houses 73.5-229 sq m on 350-1080 sq m plots). Planned park, amphitheatre, hotel (Swissotel resort announced), restaurants, coworking, sports and medical centres, spa, school, kindergarten, art studios; project management office and personalized design.")
D.save()
