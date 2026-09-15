import rec
from rec import imgs
D = rec.Dev("29_novavan", "NovaVan Residence (New Home LLC / Lore Construction)", "https://novavan.am/", ["+37441442474", "+37444774488"], "loreconstructionllc@gmail.com",
            {"facebook": "https://www.facebook.com/NovaVan.am", "instagram": "https://www.instagram.com/NovaVan.am"})
u = "https://novavan.am/"
D.add(u, "NovaVan Residence", auto=False, city="Vanadzor", district="Lori", address="Tumanyan St 14, Vanadzor", status="under construction", completion="2028-11", floors="12", type="residential",
      price_min_amd_m2=395000, price_currency_raw="from 395,000 AMD/sq m (EN) / 405,000 AMD/sq m (HY); income tax refund",
      images=imgs(u, "uploads/", r"%D5%80%D5%A1%D5%B5|քարտեզ|New-Home|Novavan_simple|novavan\.webp"),
      description="NovaVan Residence in Vanadzor (Lori): construction starts 2026, completion November 2028. 161 apartments (2-5 rooms) in a building with 12 above-ground floors (1 commercial, 11 residential) and 1 underground floor; 1,698 sq m landscaping, playground and recreation zone, CCTV and fire systems, individual heating/cooling, gas/water/power, 9+ seismic resistance, solar energy with power storage, water reservoirs. Prices from 395-405k AMD/sq m, installments, income-tax refund. Developer New Home LLC (founded 2019).")
P = "https://novavan.am/en/the-apartments-have-already-been-put-into-operation/"
for t, city, dist, addr in [
    ("Residential district in Ptghni village", "Ptghni", "Kotayk", "Ptghni village"),
    ("Apartment building G. Hovsepyan 24/4", "Yerevan", "Nork-Marash", "Garegin Hovsepyan St 24/4"),
    ("Reconstruction of apartment building G. Hovsepyan 24/9", "Yerevan", "Nork-Marash", "Garegin Hovsepyan St 24/9"),
    ("Apartment building Davtashen 4th district 2/9", "Yerevan", "Davtashen", "Davtashen 4th district 2/9"),
    ("Apartment building Davtashen 2nd district 22/2, 22/3", "Yerevan", "Davtashen", "Davtashen 2nd district 22/2, 22/3"),
    ("Apartment building Babajanyan 111/1 (B2 29/5)", "Yerevan", "Malatia-Sebastia", "Babajanyan St 111/1 / B2 district 29/5"),
]:
    D.add(P, "New Home LLC - " + t, auto=False, city=city, district=dist, address=addr, status="completed",
          description=t + ": completed project listed in the portfolio of New Home LLC, developer of NovaVan Residence (projects already put into operation).")
D.save()
