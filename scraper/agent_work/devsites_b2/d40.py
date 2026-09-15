import sys; sys.path.insert(0,'.')
from mk import *
dev="Target Development"; du="https://td.am/"; ph=["+37410501501"]; em="info@targetdevelopment.am"
G="https://td.am/gallery/"
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,city="Yerevan",**k)
P=[R(source_url="https://td.am/portfolio.html#piazza-grande",title="Piazza Grande Business Center",district="Kentron",address="Near Central Bank / Yerevan City Hall, Kentron, Yerevan",status="completed",type="commercial",images=[G+"piazza_grande/2_small.jpg"],
   description="Premium mixed-use business centre in the heart of Yerevan next to the Central Bank, UN building, HSBC, Yerevan City Hall, ministries and the Marriott; turnkey offices of 100-2,000 m2 for lease, near the subway."),
 R(source_url="https://td.am/portfolio.html#paronyan-offices",title="Paronyan Street Offices",district="Kentron",address="Paronyan St, Yerevan",status="completed",type="commercial",images=[G+"paronyan_comm/1_small.jpg"],
   description="Renovated office premises of 75-320 m2 for lease with kitchenettes, reception, modern HVAC, 24-hour security and CCTV."),
 R(source_url="https://td.am/portfolio.html#northern-avenue",title="Northern Avenue Retail",district="Kentron",address="Northern Avenue, Yerevan",status="completed",type="commercial",images=[G+"north/1_small.jpg"],
   description="Retail spaces for lease on Northern Avenue, the pedestrian boulevard in central Yerevan, suitable for boutiques, cafes and branch offices."),
 R(source_url="https://td.am/portfolio_res.html",title="Paronyan Street Apartments",district="Kentron",address="Paronyan St, Yerevan",status="completed",type="residential",
   description="Building in downtown Yerevan with furnished apartments for lease with views of Mount Ararat, modern kitchens and bathrooms, walking distance to restaurants, shops, schools and theatres."),
 R(source_url="https://td.am/portfolio_invest.html",title="Kanaker-Zeytun Multifunctional Complex (investment project)",district="Kanaker-Zeytun",address="Davit Anhaght St, Kanaker-Zeytun, Yerevan",status="planned",type="mixed",
   description="Investment project for a multifunctional complex in the centre of Kanaker-Zeytun district directly on Davit Anhaght St, next to the French and European universities and the district administration.")]
save("40_target",P,{"note":"site dated 2011; lease-oriented commercial portfolio"})
