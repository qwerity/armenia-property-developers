import sys; sys.path.insert(0,'.')
from mk import *
U="https://step-construction.am/wp-content/uploads/2023/04/"
dev="Step Construction"; du="https://step-construction.am/"; ph=["+37444096666"]; em="info@step-construction.am"
so={"facebook":"https://www.facebook.com/Stepdevelopmentconstructioncompany","instagram":"https://www.instagram.com/step_development/"}
B="https://step-construction.am/project/"
def R(**k): return rec(developer=dev,developer_url=du,phones=ph,email=em,social=so,type="residential",**k)
P=[R(source_url=B+"bagrevand-4-townhouses/",title="4 Townhouses in Bagrevand",city="Yerevan",district="Nor Nork",address="Bagrevand, Yerevan",images=[U+"Avan-title_merged-1.jpg"],
   description="Group of 4 townhouses in Bagrevand delivered by Step Construction from architectural design through construction."),
 R(source_url=B+"byurakan-villas/",title="Byurakan Villas Complex",city="Byurakan",district="Aragatsotn",address="Byurakan, Aragatsotn",images=[U+"1-1.jpg",U+"9-1024x1024.jpg"],
   description="Complex of 4 villas in Byurakan designed and built by Step Construction (design to construction)."),
 R(source_url=B+"5-townhouses-duryan/",title="5 Townhouses in Duryan district",city="Yerevan",district="Avan",address="Duryan district, Avan-Arinj",images=[U+x for x in ["PHOTO-2022-12-16-11-38-29.jpg","PHOTO-2022-12-16-11-38-29-1.jpg","PHOTO-2022-12-16-11-38-29-2.jpg","PHOTO-2022-12-16-11-38-30.jpg","PHOTO-2022-12-16-11-38-30-1.jpg","PHOTO-2022-12-16-11-38-31.jpg"]],status="completed",
   description="Group of 5 townhouses in the Duryan district designed and built by Step Construction (photos of built houses, Dec 2022).")]
save("39_step",P,{"note":"single private houses and cinema studio skipped; Shushi Palace (collaboration) recorded under RED Invest/Lorida Group"})
