import rec
from rec import imgs
D = rec.Dev("44_zeytunbuild", "Zeytoun Build (HB Group)", "http://zeytunbuild.am/", ["+37455352352", "+37411352352"], "hbgroup352@gmail.com",
            {"facebook": "https://www.facebook.com/zeytunbuild", "instagram": "https://www.instagram.com/zeytun_build_/"})
u = "http://zeytunbuild.am/"
D.add("http://zeytunbuild.am/hy", "Zeytun Build residential complex", auto=False, lat=40.20286, lng=44.5451, district="Kanaker-Zeytun", address="Paruyr Sevak St 51/11", status="under construction", floors="16,18", type="mixed",
      images=[x for x in imgs(u, "uploads/", r"hark|genplan", 20)][:12],
      description="Zeytun Build: multifunctional residential complex in Kanaker-Zeytun on one of Yerevan's elevated sunny areas (Paruyr Sevak 51/11). Monolithic seismic-resistant structure of 3 sections (two 18-floor, middle 16-floor); kindergarten and pre-school on the ground floor; 3-level underground parking, landscaped yard, 24/7 security, night lighting, new-generation lifts; ceilings 3 m, apartments e.g. 4-room 116.68 sq m. Most listed apartments on floors 10+ shown as sold; mortgage available.")
D.save()
