import sys; sys.path.insert(0,'.')
from mk import *
dev="Movsesyan & Partners"; du="https://movsesyanandpartners.am/"; ph=["+37455224746","+37495717611"]; em="movsesyanandpartners@gmail.com"
so={"facebook":"https://www.facebook.com/movsesyanpartners.am","instagram":"https://www.instagram.com/movsesyan_partners"}
I="https://movsesyanandpartners.am/img/"
rows=[("Dilijan Inn Apartment Complex","Dilijan","Tavush","104/1 Orjonikidze St, Dilijan","portfolio-1.jpg","resort"),
("Kasakhum","Kasakh","Kotayk","Vahan Teryan 3rd St, plot 32, Kasakh","portfolio-2.jpg","residential"),
("Garni project","Garni","Kotayk","Garni, Kotayk","portfolio-3..jpeg","residential"),
("Avan project","Yerevan","Avan","Avan, Yerevan","portfolio-4.jpeg","residential"),
("Davtashen project","Yerevan","Davtashen","Davtashen, Yerevan","portfolio-5.jpeg","residential"),
("Byurakan project","Byurakan","Aragatsotn","Byurakan, Aragatsotn","portfolio-6.jpeg","residential")]
P=[rec(source_url=du+"project.html#"+re.sub(r'\W+','-',t.lower()),title=t,developer=dev,developer_url=du,city=c,district=d,address=a,type=ty,phones=ph,email=em,social=so,website=du+"project.html",images=[I+img],
  description=f"Project listed in the Movsesyan & Partners Construction portfolio ({a}); the site gives only name, location and a render/photo. The company provides construction, renovation, architecture and interior design.") for t,c,d,a,img,ty in rows]
save("26_movsesyan",P,{"note":"Caveman Residence (known) not on site; project pages have no details"})
