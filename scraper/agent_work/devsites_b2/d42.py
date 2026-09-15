import sys; sys.path.insert(0,'.')
from mk import *
U="https://urban-unit.com/wp-content/uploads/2017/07/"
P=[rec(source_url="https://urban-unit.com/project/urban-house/",title="Urban House",developer="Urban Unit",developer_url="https://urban-unit.com/",city="Yerevan",district="Kentron",address="Plot N7620, left side of Cascade residential complex, Yerevan",
 completion="2017",status="completed",floors="4",type="residential",phones=["+37477548081","+37493333222"],email="info@urban-unit.com",social={"facebook":"https://www.facebook.com/Urban-Unit-204615879563488/"},
 images=[U+"Urban_House_00.jpg",U+"Urban_House_01.jpg",U+"Urban_House_03.jpg",U+"Urban_House_04.jpg",U+"Urban_House_05.jpg"],
 description="Four-storey multi-apartment building (1,340 m2) built 2016-2017 on a 495 m2 triangular plot beside the Cascade, facing south-east to Mount Ararat and panoramic Yerevan views; volume of two semi-cylinders, basement parking, open-air colonnade entrance, travertine facade, attic apartment with large open balcony, green surroundings.")]
save("42_urbanunit",P,{"note":"rest of portfolio is architecture/interior design services (skipped)"})
