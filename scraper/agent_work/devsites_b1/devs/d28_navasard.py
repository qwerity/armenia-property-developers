import rec
from rec import imgs
D = rec.Dev("28_navasard", "Navasard Shinarar", "https://navasardshinarar.am/en", ["+37494884088"], "navasardshinararllc@gmail.com",
            {"facebook": "https://www.facebook.com/people/Navasard/61553810724403/", "instagram": "https://www.instagram.com/navasard_construction_company/"})
B = "https://navasardshinarar.am/en/"
I = lambda s: imgs(B + s, "files/portfolio-images/", "styles/")
N = " Navasard Shinarar is the construction contractor (portfolio entry, not a sales listing)."
D.add(B+"acharyan-residential-complex", "Acharyan Residential Complex", auto=False, district="Avan", address="Acharyan St, Avan", status="under construction", images=I("acharyan-residential-complex"),
      description="Acharyan Residential Complex: multi-apartment residential building on Acharyan St in Avan, Yerevan; framework construction works ongoing for client Avan Project LLC." + N)
D.add(B+"ashtarak-residential-complex", "Ashtarak residential complex (Ashtaraketsu 31)", auto=False, city="Ashtarak", district="Aragatsotn", address="Ashtaraketsu St 31, Ashtarak", status="under construction", images=I("ashtarak-residential-complex"),
      description="Multi-apartment residential building at Ashtaraketsu 31 in Ashtarak; construction ongoing for client Global Media Lab LLC." + N)
D.add(B+"monte-residential-complex", "MONTE residential complex", auto=False, district="Ajapnyak", address="Leningradyan St 23/18", status="under construction", images=I("monte-residential-complex"),
      description="MONTE residential complex: multi-apartment residential building at Leningradyan 23/18, Yerevan; framework construction ongoing for client Elite Residence." + N)
D.add(B+"genesis-twin-residential-building-ejmiatsin", "Genesis Twin Residential Building", auto=False, city="Vagharshapat", district="Armavir", address="Alaverdyan St 6, Vagharshapat (Etchmiadzin)", status="under construction", images=I("genesis-twin-residential-building-ejmiatsin"),
      description="Genesis Twin: multi-apartment residential building at Alaverdyan St 6, Vagharshapat (Etchmiadzin); construction and interior finishing works ongoing for client Residential complex Artimed LLC." + N)
D.save("contractor portfolio; residential entries only")
