import rec
D = rec.Dev("34_renco", "Renco ArmEstate (Nuovo Velodromo)", "http://www.renco.it/", ["+37410590799"], "armestate@renco.it", {"facebook": "https://www.facebook.com/rencospa"})
F = "https://www.renco.it/sites/default/files/2024-11/"
D.add("https://www.renco.it/projects/milano-and-firenze-towers", "Milano and Firenze Towers (Nuovo Velodromo)", auto=False, address="former Yerevan velodrome site", status="under construction", completion="2028", floors="24", type="mixed",
      images=[F + x for x in ["Velodrome_Cam_005.jpg", "Velodrome_Cam_001%20-%20Copia.jpg", "Velodrome_Cam_002.jpg", "Velodrome_Cam_007.jpg", "Velodrome_Cam_001.jpg", "Velodrome_Cam_006.jpg"]],
      description="Milano and Firenze Towers: Renco (Italy) residential and commercial development on the site of the former velodrome in Yerevan, designed by Renco's in-house studio with Italian aesthetics. Two 24-floor towers with 151 luxury apartments, 15,000 sq m financial business centre, 2,500 sq m commercial area, outdoor square and redeveloped local park. LEED BD+C Core & Shell, double-insulated walls, ventilated facade, solar-control glazing, autonomous electric heating/cooling per apartment, ground-floor shops and cafes. In progress, delivery end of 2028.")
D.save("renco.it global portfolio lists only Milano & Firenze Towers for Armenia (plus an energy project); Piazza Grande not listed")
