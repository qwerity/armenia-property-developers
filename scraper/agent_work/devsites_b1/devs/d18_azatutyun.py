import rec, re, f
from rec import imgs
D = rec.Dev("18_azatutyun", "Green Property Development (Azatutyun Complex)", "https://azatutyuncomplex.am/", ["+37499199000", "+37412599900"], "info@azatutyuncomplex.am",
            {"facebook": "https://www.facebook.com/azatutyuncomplex", "instagram": "https://www.instagram.com/azatutyuncomplex"})
u = "https://azatutyuncomplex.am/en"
h = f.get("https://azatutyuncomplex.am/en/location")
m = re.search(r'(40\.\d+)&quot;,&quot;(44\.531658)', h)
lat, lng = (float(m.group(1)), float(m.group(2))) if m else (None, None)
D.add(u, "Azatutyun Multifunctional Complex", auto=False, lat=lat, lng=lng, district="Kanaker-Zeytun", address="Azatutyan Ave 26/1", status="under construction", floors="18,9", type="mixed",
      images=imgs("https://azatutyuncomplex.am/", "storage/|genplan|hero"),
      apartments=[{"rooms": "various", "area_min": 58.1, "area_max": 94.7}],
      description="Azatutyun multifunctional complex at the northern gateway of Yerevan (Azatutyan Ave 26/1), first project of Green Property Development (founded 2019); builder Metroshin with VGM Projects as construction manager; partners ArtQar Development, First Mortgage Company, Ameriabank, Global Capital Investment Fund. Two buildings: 18-floor residential tower (floors 1-4 commercial, premium apartments ~58-95 sq m above) with tuff arches, and 9-floor office/commercial building. 9+ seismic foundation, BMS smart building system, aluminium windows, non-combustible composite facade, food court, zen gardens, parking. Live construction stream and virtual tour.")
D.save()
