import rec
D = rec.Dev("45_haekshin", "HAEKSHIN Construction (ANPP Construction)", "https://haekshin.am/", ["+37410423272", "+37410428272"], "info@haekshin.am",
            {"facebook": "https://www.facebook.com/HAEKSHINConstructionCompany", "instagram": "https://www.instagram.com/bridgeview_yerevan/"})
S = "https://system.haekshin.am/storage/projects/"
P = "https://haekshin.am/hy/projects/"
D.add(P+"as", "Bridgeview residential complex", auto=False, district="Davtashen", address="Davtashen 10th St, plot 15/5", status="completed", floors="22",
      images=[S+"9Toyu00Jud9R7SVQ7tUKOkNkkYZMxYTEmiMeAUps.jpeg"],
      description="Bridgeview: multi-apartment residential complex built by HAEKSHIN (client ANPP Construction CJSC) with 22 floors above ground and a 4-level underground parking; 158 apartments; views of Davtashen bridge and Ararat on one side and Aragats on the other; developer offers interior finishing services. Started 2021; construction completed.")
D.add(P+"baghramyan", "Baghramyan Residence", auto=False, district="Kentron", address="Marshal Baghramyan Ave 37", status="under construction", completion="2029", floors="18", type="mixed",
      images=[S+"cTumxdYNsJfzC6a0FMp3Wss3DwjJWFjeuyLTqGjG.jpeg"],
      description="Baghramyan Residence: multifunctional residential complex at Baghramyan 37 built by HAEKSHIN (2025-2029): 18 above-ground floors (16 full residential, 17-18 set back), 4-level underground parking with 184 spaces, commercial floors 1-2 and part of 3, typical residential floors 4-16; lightweight stone-texture ventilated facade, fire-rated self-closing stair doors. Surrounded by 2-5 storey buildings.")
D.add(P+"sevak", "NOVA residential complex", auto=False, district="Kanaker-Zeytun", address="Paruyr Sevak St 5/1", status="under construction", completion="2029", floors="17", type="mixed",
      images=[S+"5kOfU91ud99PwH9zMKwC3kavH4GaqlwAFwzFQWrX.jpeg"], apartments=[{"rooms": "various", "area_min": 34.7, "area_max": 105}],
      description="NOVA: new 17-storey residential building by HAEKSHIN in Kanaker-Zeytun (Paruyr Sevak 5/1) with sections A, B, C, 3 entrances and 10 lifts; 492 apartments of 34.7-105 sq m on floors 4-17; 4 underground parking levels with 364 spaces; 3 floors of commercial/business space; ~40% of site landscaped; gas supply, apartments delivered with gas boiler and air conditioners. Construction 2026-2029.")
D.add(P+"hk", "Firdus Prime Residence (LOT 10-11 building)", auto=False, district="Kentron", address="Tigran Mets Ave, near Republic Square", status="under construction", completion="2027", floors="12",
      images=[S+"I1X3DDYeFxJVlCefmRTnPovJZVDF5hLaH3pFV6UZ.jpeg"],
      description="Firdus Prime Residence in central Yerevan on Tigran Mets Ave next to Republic Square: HAEKSHIN builds the LOT 10-11 building - 12 floors, apartments from 45.3 sq m. Works 2025-2027 (HAEKSHIN as contractor).")
D.add(P+"gareginnjhdeh", "Garegin Nzhdeh 15/1 residential building", auto=False, district="Shengavit", address="Garegin Nzhdeh St 15/1", status="under construction", floors="9",
      images=[S+"ASXn8umPO6r86jhwXWwkchFzLk9KEnfW6KCoWPGg.jpeg"],
      description="High-rise multi-apartment residential building at G. Nzhdeh 15/1 built by HAEKSHIN for client Vishka LLC: 2-level underground parking and 9 above-ground floors; works ongoing since 2023 (contractor project).")
D.save("from system.haekshin.am/api/projects; Defanse district (contractor role) omitted as covered by Defanse Housing Invest")
