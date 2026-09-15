import rec
from rec import imgs
D = rec.Dev("21_felicity", "Lav-Sar (FeliCity)", "https://felicity.am/", ["+37494002209", "+37498371377", "+37410371371", "+37410371373"], "lavsar2019@gmail.com",
            {"facebook": "https://www.facebook.com/felicity.bnakelihamalir/", "instagram": "https://www.instagram.com/felicity_residentialcomplex/"})
u = "https://felicity.am/shenqer/felicity-nor-norq/"
D.add(u, "FeliCity Nor Nork", auto=False, lat=40.1827, lng=44.5633, district="Nor Nork", address="Davit Bek St 5/5", status="under construction", type="mixed",
      images=imgs(u, r"felicity-nor-nork-image"), apartments=[{"rooms": "various", "area_min": 53, "area_max": 124}],
      description="FeliCity Nor Nork: premium multifunctional residential complex on Davit Bek St 5/5 plot next to Surb Sargis church of Nor Nork and a newly landscaped city park, with Ararat views. 11-point seismic resistance, playground, commercial spaces on the ground floor; apartments 53-124 sq m. For sale.")
u = "https://felicity.am/shenqer/felicity-davitashen/"
D.add(u, "FeliCity Davtashen", auto=False, district="Davtashen", address="Anastas Mikoyan St 27", status="under construction",
      images=["https://felicity.am/wp-content/uploads/2025/01/davtashen.jpg"], apartments=[{"rooms": "2-4", "area_min": 65, "area_max": 163}],
      description="FeliCity Davtashen: premium multi-apartment complex 200 m from Davtashen bridge near the Yerevan-Yeghvard highway and Hrazdan gorge, with views of Masis, Aragats and Ara mountains. Multiple sections on gently sloping terrain (~4 m level difference); 2-4 room apartments of 65-163 sq m with large kitchens, hallways, utility rooms and loggias; free-planning option. For sale.")
D.save()
