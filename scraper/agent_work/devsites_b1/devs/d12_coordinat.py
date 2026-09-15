import rec
D = rec.Dev("12_coordinat", "Coordinate (Koordinat LLC)", "https://coordinat.am/", ["+37433607040"], "info@coordinat.am")
u = "https://coordinat.am/"
D.add(u, "Black & White Residence", auto=False, lat=40.270139, lng=44.628833, city="Abovyan", district="Kotayk", address="Tartu St 1/1, Abovyan", status="under construction",
      images=["https://coordinat.am/img/revolution-slider/main-slider/4.jpg", "https://coordinat.am/img/revolution-slider/main-slider/1.jpg", "https://coordinat.am/img/revolution-slider/main-slider/2.jpg", "https://coordinat.am/img/1.jpg", "https://coordinat.am/img/2.jpg", "https://coordinat.am/img/3.jpg", "https://coordinat.am/img/5.jpg", "https://coordinat.am/img/6.jpg"],
      description="Black & White Residence: business-class residential building with closed courtyard by developer Koordinat LLC. 24/7 water supply and backup power, lift service, garbage collection from apartment, smart security, gardener; rubber-surfaced playground, modern gazebo, fire-pit zone, mature 5 m trees. Views to sunset, Ararat, Ara, Aragats and Hatis (Jesus statue). Full sound insulation, 3 m flat ceilings, energy-saving glazing. House rules prohibit facade changes.")
D.save()
