import sys,json; sys.path.insert(0,'.')
from mk import *
cards={c['title']:c for c in json.load(open('ml_cards.json'))}
dev="ML Mining"; du="https://mlmining.am/"; ph=["+37410200004","+37455001007","+37499410009","+37495510009"]; em="info@byuregh.am"
so={"facebook":"https://www.facebook.com/mlmining","instagram":"https://www.instagram.com/mlmining"}
dist_map={"Malatia-Sebastia":"Malatia-Sebastia","Avan, Yerevan":"Avan","Kanaker-Zeytun, Yerevan":"Kanaker-Zeytun","Arabkir, Yerevan":"Arabkir","Arabkir":"Arabkir","Center":"Kentron","Nor Nork, Yerevan":"Nor Nork"}
city_map={"Ararat Province, Artashat":("Artashat","Ararat"),"Kotayq, Abovyan":("Abovyan","Kotayk"),"Armavir, Armavir":("Armavir","Armavir"),"Ararat, Ararat":("Ararat","Ararat")}
info={
"Nor Yerevan District":dict(completion="2027-09",status="under construction",floors="9-21",price_min_amd_m2=495000,price_currency_raw="Exclusive price 495,000 AMD/m2 (block 4, noryerevan.com); mortgage 10% down, installments 12-36 months",website="https://noryerevan.com/",
  d="Large district in Malatia-Sebastia: 24 buildings of 9-21 floors, ~3,840 apartments of 35-102 m2, 80,000 m2 site with 40% greenery, 3-level underground parking, 2 lifts per entrance, seismic resistance 9-10, playgrounds and football/volleyball/tennis courts, supermarkets and services. Phased completion: block 1 June 2025, block 2 Dec 2025, block 3 Sept 2027; block 4 in active sales.",vids=["Hwsd9RMjPe8","fntun-0UfVQ"]),
"Avan Towers":dict(completion="2027",status="under construction",floors="14-22",price_min_amd_m2=379000,price_currency_raw="from 379,000 AMD/m2 (avan.am); 2-room 59.5 m2 from 24,335,500 AMD; 3-room 89 m2 from 33,731,000; 4-room 98.8 m2 from 37,445,200; 10% down",website="https://www.avan.am/",
  d="Mega microdistrict in Avan at Acharyan 53: 24 buildings of 14-22 floors, ~5,010 apartments of 35-541 m2, 100,000 m2 total area with 48,000 m2 greenery, glazed facades, 2 premium lifts per entrance, 4-level underground parking, kids and sports courts, supermarkets and beauty salons. Completion planned 2026-2027.",vids=["_v98FT2x0EI"],
  apts=[{"rooms":"2","area_min":59.5,"area_max":None,"price_from":24335500,"currency":"AMD"},{"rooms":"3","area_min":89,"area_max":None,"price_from":33731000,"currency":"AMD"},{"rooms":"4","area_min":98.8,"area_max":None,"price_from":37445200,"currency":"AMD"}]),
"Kanaker Complex":dict(completion="2024",floors="10-16",d="Complex at Melik Melikyan 2/1: 4 buildings of 10-16 floors, 384 apartments of 55.4-93 m2, 9,470 m2 site with 40% greenery, 3-level underground parking, 2 lifts per building; income tax refund. Planned completion 2024.",vids=["Lt_9iPNOw7U","QVCHklZTv2Y"]),
"Kanaker 2 Complex":dict(completion="2025",floors="16-18",d="Complex at Z. Kanakertsi 137/1: 2 buildings of 16-18 floors, 43,412 m2 total floor area, apartments of 54-105 m2, 249 parking spaces on 2 underground levels, 2,870 m2 greenery, playground, public spaces 596-993 m2, seismic resistance 9-10. Planned completion 2025."),
"Adonts Premium Complex":dict(completion="2024",floors="19",d="19-storey premium building at Adonts 19/9: 167 apartments of 55.7-136 m2, 116 parking spaces, 2 lifts, 40% greenery, seismic 9-10; income tax refund. Planned completion 2024.",vids=["XhIsD0AAW1I"]),
"Griboyedov Premium":dict(completion="2025",floors="15-17",d="Premium complex at Adonts 21/2: 2 buildings of 15-17 floors, 178 apartments of 52-112 m2, 5,483 m2 site, 3-level underground parking, 2,364 m2 landscaping, premium lifts. Planned completion 2025."),
"Charagayt Complex":dict(completion="2023-08",floors="14,16,18",website="https://charagayt.am/",d="Charagayt complex at Adonts 19/8: 7 buildings of 14/16/18 floors, 619 apartments of 56-125 m2, 17,000 m2 site, 439 parking spaces, 1,300 m2 greenery, seismic 9-10. Buildings A, B, C and D commissioned; phase 1 April 2023, phase 2 August 2023.",vids=["V6QEtJN5tI8"]),
"Adonts Complex":dict(completion="2024",floors="16",address="Adonts 19/19",d="Complex at Adonts 19/19: 2 buildings of 16 floors, 210 apartments (2-4 rooms, 56-95 m2), 5,632 m2 site with 40.6% greenery, 154-space 2-level underground parking, 2 lifts per building; income tax refund. Completion 2024.",vids=["SlL1o_0mEEQ"]),
"Arabkir 27 Complex":dict(floors="8",address="Arabkir 9th St, 27",d="8-storey building in Arabkir (9th street, 27) with 35 apartments, 4,800 m2 total area, 40% greenery, seismic 9/10, passenger and freight lift.",vids=["gKmdnI8QTAQ"]),
"Mergelyan Residence":dict(d="Residential building at H. Hakobyan 3/20, Arabkir, with 61 apartments, one entrance, passenger and freight lifts."),
"Ayginer Premium":dict(completion="2024",floors="21 + penthouse",d="Premium complex at Arshakunyats 9/2 (Kentron): 3 buildings of 21 floors + penthouses, 738 apartments of 65-139 m2, 13,000 m2 site, 6 premium lifts per building, 525-car 2-level underground parking, 3,650 m2 greenery, playgrounds and mini courts, 9,083 m2 public space on floors 2-3, seismic 9-10; income tax refund.",vids=["kUMp0kuy1Zk"]),
"Dalma Hills":dict(completion="2024",floors="19",d="19-storey building at Monte Melkonyan 16: 176 apartments of 55-139 m2, 2 public floors, parking on 2 underground + 3 above-ground levels, premium lifts.",vids=["P8Q85j-zQxc"]),
"Nor tun complex":dict(d="Nor Tun complex of 6 residential buildings at Mikoyan 9/3, Nor Nork (built with Nor Tun / Dakava Construction)."),
"Artashat Residential Complex":dict(completion="2024",floors="7",address="Shahumyan 23/1",d="3 seven-storey buildings in Artashat at Shahumyan 23/1 with apartments of 60-76.5 m2, 5,200 m2 site, 2,080 m2 greenery, public spaces 2,870 m2, seismic 9-10."),
"Abovyan City House":dict(completion="2024",floors="18",d="Joint project with Abovyan City House: 3 buildings of 18 floors on 23 August St in Abovyan with 500+ apartments; school, music school, kindergarten and college within 25-70 m. Nearly sold out.",vids=["AGZYhvuRUFo"]),
"Artashat Premium":dict(floors="8-9",address="A. Khachatryan 116/1",d="Artashat Premium: 3 residential buildings of 8-9 floors at A. Khachatryan 116/1, Artashat; landscaped, seismic 9-10."),
"Norq Residential Complex":dict(floors="7-16",d="Nork residential complex in Armavir city at Baghramyan 39: 9 buildings of 7-16 floors."),
"Ararat complex":dict(floors="7",d="Nor Ararat complex in Ararat city (Araratyan district 20): 4 seven-storey residential buildings."),
"Nor Dalma Premium Complex":dict(floors="16",d="16-storey premium building at Tsitsernakaberd Highway 3/1 (Malatia-Sebastia) with 271 apartments, passenger and freight lifts."),
}
P=[]
for t,c in cards.items():
    i=info[t]
    city,district=city_map.get(c['region'],("Yerevan",dist_map.get(c['region'],"")))
    addr=(i.get('address') or c['address'])+", "+city
    imgs=[c['img']]
    if t=="Nor tun complex": title="Nor Tun Complex"
    elif t=="Norq Residential Complex": title="Nork Residential Complex (Armavir)"
    elif t=="Ararat complex": title="Nor Ararat Complex"
    else: title=t
    P.append(rec(source_url=c['view'] or "https://mlmining.am/en/construction#"+re.sub(r'\W+','-',t.lower()),title=title,developer=dev,developer_url=du,city=city,district=district,address=addr,lat=c['lat'],lng=c['lng'],
        price_min_amd_m2=i.get('price_min_amd_m2'),price_currency_raw=i.get('price_currency_raw',""),completion=i.get('completion'),status=i.get('status'),floors=i.get('floors'),type="residential",
        phones=ph,email=em,social=so,website=i.get('website') or c['view'] or "https://mlmining.am/en/construction",images=imgs,videos=["https://www.youtube.com/watch?v="+v for v in i.get('vids',[])],
        description=i['d']+" ("+c['details']+")",apartments=i.get('apts')))
save("23_mlmining",P,{"note":"Byuregh district not listed on mlmining.am; byuregh.am returns HTTP 500"})
