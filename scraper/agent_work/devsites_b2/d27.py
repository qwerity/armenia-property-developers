import sys; sys.path.insert(0,'.')
from mk import *
dev="National Group"; du="https://nationalgroup.am/"; ph=["+37491843333","+37495843333","+37496559981"]; em="info@nationalgroup.am"
so={"facebook":"https://www.facebook.com/National-Group-104392118019168/","instagram":"https://www.instagram.com/nationalgroup.am/"}
U="https://nationalgroup.am/wp-content/uploads/"; B="https://nationalgroup.am/index.php/"
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,social=so,**k)
P=[R(source_url=B+"nor-avan-hamalir/",title="Nor Avan Residential Complex",city="Yerevan",district="Avan",address="37/1 Hrachya Acharyan St, Yerevan",price_min_amd_m2=420000,price_currency_raw="420,000-550,000 AMD per m2",completion="2025-12",status="under construction",floors="16,18",type="residential",
  images=[U+"2024/10/nor-avan-5-webp-834x1024.webp",U+"2024/10/nor-avan-2-webp-1024x768.webp",U+"2024/10/nor-avan1-webp-1024x779.webp",U+"2024/10/nor-avan-4-webp-1024x768.webp",U+"2024/10/nor-avan-6-webp-834x1024.webp",U+"2024/10/nor-avan-8-webp-878x1024.webp",U+"2024/10/nor-avan-7-webp-834x1024.webp"],
  description="Multi-apartment complex in Avan at Acharyan 37/1: six buildings of 16 and 18 floors with 444 apartments; 2,700 m2 green zone, residents' swimming pool, playground, gym, supermarket, kids development centre, open and closed cafes. Construction started Sept 2023, more than half sold; planned completion Dec 2025. 420,000-550,000 AMD/m2."),
 R(source_url=B+"garegin-nzhdeh-23-3/",title="Garegin Nzhdeh 23/3",city="Yerevan",district="Shengavit",address="23/3 Garegin Nzhdeh St, Yerevan",price_min_amd_m2=530000,price_currency_raw="530,000 AMD per m2",completion="2024-11",status="completed",floors="14",type="residential",
  images=[U+"2024/10/23-3-webp-718x1024.webp",U+"2024/09/2M1A7737-webp-scaled-e1726744452172.webp",U+"2024/09/1400be86-a2b7-4439-b5b0-5c255ccfd80d-webp.webp",U+"2024/09/2M1A7777-webp-scaled.webp",U+"2024/09/2M1A7722-webp-1-scaled.webp"],
  description="14-storey residential building with 96 bright apartments with open loggias and views, underground parking and two modern lifts. Construction Feb 2021 - Nov 2024. 530,000 AMD/m2."),
 R(source_url=B+"garefin-nzhdeh-23-6/",title="Garegin Nzhdeh 23/6",city="Yerevan",district="Shengavit",address="23/6 Garegin Nzhdeh St, Yerevan",price_min_amd_m2=530000,price_currency_raw="530,000 AMD per m2",completion="2021-04",status="completed",type="residential",
  images=[U+"2024/10/236-1024x678.jpeg"],description="Modern residential building with 42 apartments in a busy, convenient part of Yerevan; built March 2018 - April 2021, fully occupied and commissioned.")]
save("27_national",P)
