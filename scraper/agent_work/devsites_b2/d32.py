import sys,re; sys.path.insert(0,'.')
from mk import *
from f import get
B="https://promgroup.am/en/project/"
def imgs(s):
    h=get(B+s+"/")
    out=[]
    for m in re.findall(r'uploads/20[0-9/]+[^"\' )]+\.(?:jpe?g|png|webp)',h):
        if re.search(r'-\d+x\d+\.|About-us|header-banner|yerevan-slider|yerevanaaa|Rectangle|logo|парник',m): continue
        u="https://promgroup.am/wp-content/"+m
        if u not in out: out.append(u)
    return out[:12]
dev="Prom Group"; du="https://promgroup.am/en/"; ph=["+37493991155","+37493991154"]; em="info@promgroup.am"
so={"facebook":"https://www.facebook.com/Promgroup15","instagram":"https://www.instagram.com/_prom_group_/"}
yt=lambda i:["https://www.youtube.com/watch?v="+i]
def R(s,**k): return rec(source_url=B+s+"/",developer=dev,developer_url=du,phones=ph,email=em,social=so,images=imgs(s),**k)
note=" Listed in the portfolio of Prom Group (general contractor/developer)."
P=[R("hb-construction",title="Prime Residence (Nork-Marash)",city="Yerevan",district="Nork-Marash",address="Nork-Marash, Yerevan",status="under construction",type="residential",
   description="Multi-apartment residential complex under construction in Nork-Marash administrative district by WB Construction Development Company."+note),
 R("double-towers",title="Double Towers",city="Yerevan",address="Yerevan",status="under construction",type="mixed",
   description="Earthquake-resistant residential complex with original architecture: total 33,217 m2 construction (23,747 m2 residential, 1,926 m2 commercial, 7,544 m2 parking) plus 2,084 m2 of additional green areas."+note),
 R("capital-park",title="Capital Park",city="Yerevan",address="2 H. Shiraz St, Yerevan",completion="2026",status="under construction",floors="16",type="residential",videos=yt("t8Oj5DnVRQY"),
   description="Residential complex at H. Shiraz 2: 5 buildings of 16 above-ground floors, 3 underground parking levels (300+ spaces), 524 apartments; completion 2026."+note),
 R("park-avenue",title="Park Avenue",city="Yerevan",district="Arabkir",address="48/6 Griboyedov St, Yerevan",status="completed",floors="12,14,16",type="mixed",videos=yt("agKofRsbCjM"),
   description="Multifunctional residential complex at Griboyedov 48/6, Arabkir: 4 buildings of 12, 14 and 16 floors, 254 underground parking spaces, 2,900 m2 garden with playgrounds and gazebos. Delivered with doors, windows, partitions, plaster and screed; cash or mortgage, income tax refund."+note),
 R("park-gyumri",title="Park Gyumri",city="Gyumri",district="Shirak",address="Gyumri",completion="IV 2024",floors="6",type="residential",videos=yt("DUbV9K6vJus"),
   description="Residential complex in Gyumri: 42,000 m2 construction area, 8 buildings of 6 floors, 1 underground parking level (151 spaces), 342 apartments; planned completion Q4 2024."+note),
 R("basis",title="Basis Residential Complex",city="Yerevan",address="Yerevan",completion="II 2025",type="residential",videos=yt("Es8mIbVxyco"),
   description="Residential complex with 81,000 m2 construction area: 5 buildings, 3 underground parking levels (382 spaces), 443 apartments; planned completion Q2 2025."+note)]
save("32_promgroup",P,{"note":"Armenia Garden and Eden Park also in Prom portfolio - recorded under their developers (Double V, Metrum)"})
