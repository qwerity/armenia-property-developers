import sys; sys.path.insert(0,'.')
from mk import *
U="http://www.moskovyan-passage.am/"
P=[rec(source_url=U,title="Moskovyan Passage",developer="Moskovyan Passage (AIG / Lasker Limited / Ak And Ak Building Technologies)",developer_url=U,city="Yerevan",district="Kentron",address="35 Moskovyan St (corner of Spendiaryan St), Yerevan",
 completion="2012",status="completed",floors="14",type="mixed",phones=["+37412221125"],email="info@moskovyan-passage.am",
 social={"facebook":"https://www.facebook.com/102777401745283","instagram":"https://www.instagram.com/moskovyan35passage/"},
 images=[U+"carusel1.jpg",U+"carusel2.jpg",U+"carusel3.jpg",U+"Eexterior_1.jpg",U+"Eexterior_2.jpg",U+"Eexterior_3.jpg",U+"Eexterior_4.jpg",U+"Eexterior_5.jpg",U+"Interior_1.jpg",U+"home_inter.jpg",U+"winery_1.jpg",U+"restaurant_1.jpg"],
 description="Elite multifunctional residential complex combining Tamanyan-style ornament with modern architecture; apartments for sale and rent plus commercial spaces for lease. Residential floors 4-13 with 52 apartments of 113-500 m2 in 4 entrances (Moskovyan and Spendiaryan streets); floors 1-3 VTB Bank Armenia head office; 8th-floor 300-seat restaurant; residents-only winery (-2) and planned 14th-floor gym/spa; 3 underground levels (parking, commercial). 9-point seismic resistance, thick insulated walls, water reservoirs, central heating, 24/7 security. Built 2006-2012, in use.",
 apartments=[{"rooms":"","area_min":113,"area_max":500,"price_from":None,"currency":None}])]
save("25_moskovyan",P)
