import rec
from rec import imgs
D = rec.Dev("02_amgroup", "AM Group", "http://www.amgroup.am/en", ["+37410588424", "+37493588424"], "")
B = "https://www.amgroup.am/en/works/"
N = " AM Group (doors/windows, glass facades, Alucobond) lists this building among its selected works as facade/window contractor; it is a reference work, not a project marketed for sale by AM Group."
for slug, title, addr, dist in [
    ("residential_yerevan_paronyan", "Residential building, Paronyan str.", "Paronyan St", "Kentron"),
    ("residential_yerevan_verin-antara", "Residential complex, Verin Antarayin str.", "Verin Antarayin St", "Kentron"),
    ("residential_yerevan_dzorap", "Residential complex, Dzorap", "Dzorapi St", "Kentron"),
    ("yeraz_residential_yerevan", "Yeraz residential complex", "", ""),
    ("residential_yerevan_lusavorich", "Residential building, Grigor Lusavorich str.", "Grigor Lusavorich St", "Kentron"),
    ("residential_yerevan_yerznkyan", "Residential building, Yerznkyan str.", "Yerznkyan St", "Kentron"),
    ("residential_yerevan_komitas", "Residential building, Komitas ave.", "Komitas Ave", "Arabkir"),
    ("residential_yerevan_griboedov", "Residential building, Griboyedov str.", "Griboyedov St", "Kentron"),
    ("residential_nor-hachn_tumanyan", "Residential complex, Nor Hachn, Tumanyan str.", "Tumanyan St, Nor Hachn", "Kotayk"),
]:
    u = B + slug
    kw = dict(city="Nor Hachn") if "hachn" in slug else {}
    D.add(u, title, address=addr, district=dist, status="completed", images=imgs(u, r"amgroup\.am/upload/", r"\.am//"),
          description=title + "." + N, **kw)
D.save("windows/facade contractor; residential reference works only")
