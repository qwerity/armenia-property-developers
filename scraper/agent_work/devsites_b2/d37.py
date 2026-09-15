import sys; sys.path.insert(0,'.')
from mk import *
U="https://shinstroyhouse.am/wp-content/uploads/2024/09/"
dev="Shin-Stroy House"; du="https://shinstroyhouse.am/"; ph=["+37439500066","+37493343651"]; em="shinstroyhouse@mail.ru"
so={"facebook":"https://www.facebook.com/profile.php?id=61571822864897","instagram":"https://www.instagram.com/shin_stroy_company"}
imgs=[U+"459275020_122152701638261648_7923325830563946537_n.jpg",U+"photo_5424772848989365334_x.jpg",U+"photo_5424772848989365333_x.jpg",U+"photo_5424772848989365332_x.jpg"]
P=[rec(source_url=du+"#duryan-5th-street",title="Shin-Stroy House residential complex, Duryan 5th St 56-58",developer=dev,developer_url=du,city="Arinj",district="Kotayk",address="Duryan district, 5th St 56-58, Arinj (Avan), Abovyan community",
 price_min_amd_m2=440000,price_currency_raw="1 m2 from 440,000 AMD; income tax refund; affordable housing for servicemen programme",completion="IV 2025",status="completed",type="residential",phones=ph,email=em,social=so,images=imgs,
 description="Residential buildings in the Duryan district of Arinj next to Avan: apartments of 37-87 m2 sold directly by the developer with mortgage or installments, from 440,000 AMD/m2; income-tax refund and the affordable-housing-for-servicemen programme apply. Commissioning scheduled for Q4 2025.",
 apartments=[{"rooms":"","area_min":37,"area_max":87,"price_from":None,"currency":"AMD"}]),
 rec(source_url=du+"#duryan-2nd-street",title="Shin-Stroy House residential complex, Duryan 2nd St 66/11",developer=dev,developer_url=du,city="Arinj",district="Kotayk",address="Duryan district, 2nd St 66/11, Arinj, Abovyan community",
 status="completed",completion="2024",type="residential",phones=ph,email=em,social=so,images=imgs[:1],
 description="Residential complex in the Duryan district of Arinj (Kotayk), commissioned in 2024; apartments available with mortgage or installment payment.")]
save("37_shinstroy",P,{"note":"site names projects only as template labels; known names Duryan 2 / Wellstone not shown"})
