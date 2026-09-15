import rec
from rec import imgs
D = rec.Dev("16_forma", "Forma Development Management", "https://forma.am/", ["+37444701111"], "info@forma.am", {"instagram": "https://www.instagram.com/forma.toon"})
X = r"Forma-Construction-Management|/2026/0[12]/|\.webp$|1170x765"
P = "https://forma.am/en/portfolio/"
I = lambda s: imgs("https://forma.am/portfolio/" + s, "uploads", X)
D.add(P+"degor-hotel/", "DEGOR Resort & Spa", auto=False, city="Stepanavan", district="Lori", address="next to Stepanavan Dendropark", status="under construction", type="resort",
      images=I("%d5%a4%d5%a5%d5%a3%d5%b8%d6%80-%d5%b0%d5%b8%d5%a9%d5%a5%d5%ac/"),
      description="DEGOR Resort & Spa in Stepanavan right next to the Dendropark: 7,500 sq m hotel/spa complex designed by Soghomonyan Architects, with indoor and outdoor pools, gym, kids zone, indoor/outdoor restaurants, conference hall and landscaped forest area. Forma provides full development management.")
D.add(P+"dendro-land/", "Dendro Land", auto=False, city="Stepanavan", district="Lori", address="adjacent to Stepanavan Dendropark, Lori", status="under construction", type="resort",
      images=I("%d5%a4%d5%a5%d5%b6%d5%a4%d6%80%d5%b8-%d5%a3%d5%bc%d5%b8%d6%82%d5%ba/"),
      description="Dendro Land: first 'hospitality mall' in Armenia on 37,000 sq m next to the Dendropark in Lori - a park of ~60 prefab mobile houses (AntaRoom zone) with restaurant, food court, game hall, amphitheatre, open-air cinema, active leisure and event zones and a craftsmen town.")
D.add(P+"dili-tropic/", "Dili Tropic", auto=False, city="", district="", address="", status="planned", type="resort",
      images=I("%d5%a4%d5%ab%d5%ac%d5%ab-%d5%bf%d6%80%d5%b8%d5%ba%d5%ab%d5%af/"),
      description="Dili Tropic: 20,000 sq m multifunctional hotel complex under a closed roof creating a single tropical climate space with levels styled as Asia, Africa and Amazonia, tropical pool area usable in winter; individuals can own a summer-home/business unit in the covered 'closed city'. Location not stated on site.")
D.add(P+"g-plaza/", "G Plaza Business Center", auto=False, city="", district="", address="", status="planned", type="commercial",
      images=I("scott-villa-du/"),
      description="G Plaza: A-class business center/business park of 8,500 sq m with innovative, comfortable and secure modern working conditions. Forma development management project; location not stated on site.")
D.save("development-management firm; Forma Toon (house model product without location) skipped")
