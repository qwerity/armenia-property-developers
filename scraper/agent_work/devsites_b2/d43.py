import sys; sys.path.insert(0,'.')
from mk import *
S="https://abovyanhills.am/storage/media/"
dev="Vardanyanshin LLC (Abovyan Hills)"; du="https://abovyanhills.am/"; ph=["+37444400050","+37460500050","+37477561213"]; em="info@abovyanhills.am"
so={"facebook":"https://www.facebook.com/profile.php?id=61575829719682","instagram":"https://www.instagram.com/abovyan_hills/"}
P=[rec(source_url="https://abovyanhills.am/en",title="Abovyan Hills",developer=dev,developer_url=du,city="Abovyan",district="Kotayk",address="Next to Abovyan city stadium, Abovyan",
 price_currency_raw="Bank mortgage or installment payment; service fee ~100 AMD/m2",completion="2028-05",status="under construction",floors="15",type="mixed",phones=ph,email=em,social=so,
 images=["https://abovyanhills.am/img/building.png",S+"sliders/thumbnail/q7xy-.jpg",S+"banner/thumbnail/gfwy-new-baner.jpg",S+"infrastructures/thumbnail/jib0-200.jpg",S+"news/thumbnail/z1ln-2.jpg",S+"news/thumbnail/ri1d-1.jpg",S+"news/thumbnail/qffg-1-10.jpg"],
 description="Multifunctional residential complex next to Abovyan stadium by Vardanyanshin LLC (founded by Baghramyanshin and Valex, builders of Avan Hills): 4,597 m2 site, two buildings of 2 underground + 15 above-ground floors, 154 apartments of 47.9-114.9 m2, 3 m ceilings, 230 underground parking spaces (115 per building), modern gym, condominium management, 24/7 security, EV charging, energy-efficiency certificate. Delivered with doors, windows, plastered partitions, levelled floors. Phase 1 May 2028, phase 2 December 2030; ground-floor works underway (2026).",
 apartments=[{"rooms":"","area_min":47.9,"area_max":114.9,"price_from":None,"currency":None}]),
 rec(source_url="https://abovyanhills.am/about",title="Avan Hills",developer="Baghramyanshin & Valex (Abovyan Hills partners)",developer_url=du,city="Yerevan",district="Avan",address="Avan, Yerevan",status="completed",type="mixed",phones=ph,email=em,social=so,
 description="Multifunctional residential complex previously completed jointly by Baghramyanshin OJSC and Valex LLC, cited on the Abovyan Hills site as their first joint project.")]
save("43_abovyanhills",P)
