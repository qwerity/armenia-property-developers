import sys; sys.path.insert(0,'.')
from mk import *
D="https://www.datocms-assets.com/62348/"
dev="Renshin Urban Investments"; du="https://renshin.am/"; ph=["+37411900100"]; em="info@renshin.am"
so={"facebook":"https://www.facebook.com/renshin.llc","instagram":"https://www.instagram.com/renshin_investment/","youtube":"https://www.youtube.com/@renshinurbaninvestments"}
B="https://renshin.am/en/projects/"
def R(**k): 
    k.setdefault("social",so); return rec(developer=dev,developer_url=du,phones=ph,email=em,**k)
P=[R(source_url=B+"Skyline/",title="Skyline",city="Yerevan",district="Arabkir",address="Baghramyan Ave - Orbeli St crossroad, Yerevan",lat=40.193334,lng=44.495882,
  price_min_amd_m2=1400000,price_currency_raw="Studio 26 m2 from 36,400,000 AMD (mortgage 359,832 AMD/month) - en.skyline-evn.am",status="under construction",type="mixed",website="https://en.skyline-evn.am/",email_="",
  social={"facebook":"https://www.facebook.com/skylineevn","instagram":"https://www.instagram.com/skyline.evn/","telegram":"https://t.me/SkylineEvn_bot"},
  images=[D+x for x in ["1751355506-3.jpg","1751355506-4.jpg","1751359168-13.png","1751359589-crop.png","1751367423-1-comp.png","1751367423-12-comp.png","1751367423-13-comp.png","1647515944-1-min.jpg"]],
  description="'City-in-a-city' high-rise district at the Baghramyan-Orbeli crossroads near Barekamutyun and Baghramyan metro: architecture by Laguarda.Low (New York), engineering by Arup, 20,000 m2 green area. Apartments (from 26 m2 studios) delivered with high-quality finishing, built-in kitchens and furnishing. On-site offices and coworking, conference halls, cafes and restaurants, sports club, medical and education centres, electric shuttle buses to the centre and electric carsharing. Concrete works ongoing (2026).") ,
 R(source_url=B+"Tumanyan%208/",title="Tumanyan 8",city="Yerevan",district="Kentron",address="8 Tumanyan St, Yerevan",status="under construction",type="mixed",
  images=[D+x for x in ["1783519662-make_night_version_202604201705.jpg","1779433306-make_night_version_202604201705.jpeg","1779434259-let_mentioned_part_202604171051.jpeg","1786711876-image-4.png"]],
  description="New premium multifunctional complex in Yerevan's Small Centre at Tumanyan 8 combining residential, commercial and aparthotel functions, with a limited number of apartments for living or investment."),
 R(source_url=B+"Buzand_91/",title="Buzand 91",city="Yerevan",district="Kentron",address="89/91 Buzand St, Yerevan",completion="2013",status="completed",floors="16",type="residential",
  images=[D+x for x in ["1647520742-img_buzand_1920.jpg","1647521323-rectangle-56-min.jpg","1647521326-rectangle-56-1-min.jpg"]],
  description="Premium residential complex in classical Tamanyan style with natural tuff cladding next to Diana Abgar park, 5 minutes' walk from Republic Square and the Opera: 16 upper + 3 ground floors, 2-4 room apartments of 63-230 m2 (64, 87, 123, 131, 147, 230 m2), 3 m ceilings, insulated windows, terraces. Completed and launched in 2013.",
  apartments=[{"rooms":"2","area_min":64,"area_max":64,"price_from":None,"currency":None},{"rooms":"3","area_min":87,"area_max":131,"price_from":None,"currency":None},{"rooms":"4","area_min":147,"area_max":230,"price_from":None,"currency":None}]),
 R(source_url=B+"Sasna_Tsrer_1/",title="Sasna Tsrer I",city="Yerevan",district="Davtashen",address="Sasna Tsrer St, near Davtashen bridge, Yerevan",status="completed",floors="14,16,20",type="mixed",
  images=[D+x for x in ["1647516970-img_sasna-tsrer-1_1920.jpg","1647517353-2-min.jpg","1647517360-7-min.jpg","1647517364-dji_0037-min.jpg","1647517368-dsc_0262-min.jpg"]],
  description="Multifunctional residential complex by the Hrazdan gorge next to Davtashen bridge: three sections of 14, 16 and 20 upper floors plus 2 base floors, 1-4 room apartments of 40-141 m2 with panoramic views of the gorge, Ararat, Ara and Aragats; reinforced concrete with tuff cladding; near Komitas Ave and Barekamutyun metro.",
  apartments=[{"rooms":"1-4","area_min":40,"area_max":141,"price_from":None,"currency":None}]),
 R(source_url=B+"Sasna_Tsrer_2/",title="Sasna Tsrer II",city="Yerevan",district="Davtashen",address="3 Sasna Tsrer St, Yerevan",status="completed",floors="16,20",type="residential",
  images=[D+x for x in ["1646663788-img_1-d76e80e03461be2462ba576b03bec8fa.jpg","1646663790-img_2-461ccc7dcdd0c5e439e6914b0f1bc35f.jpg","1646663875-feature-794025a51a3526231bd840a8e4ef4e48.jpeg","1647515010-1-min.jpg","1647515013-2-min.jpg","1647515016-3-min.jpg"]],
  description="Business-class complex at Sasna Tsrer 3 on the right side of Davtashen bridge, opposite Sasna Tsrer I: three buildings (two 16-storey, one 20-storey), stepped floors with tuff cladding, floor-to-ceiling windows with gorge and Ararat views, 3 m ceilings; top two floors are duplexes of 153-312 m2 with large balconies.")]
for r in P: r.pop("email_",None)
save("34_renshin",P,{"note":"Artlife Kempinski recorded under Artlife entry; Cascade complex = GTB Cascade (recorded under GTB)"})
