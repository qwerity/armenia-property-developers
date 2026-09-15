import sys; sys.path.insert(0,'.')
from mk import *
M="https://siluet.am/upload/medialibrary/"
P=[rec(source_url="https://siluet.am/",title="Siluet Residence",developer="Siluet Invest",developer_url="https://siluet.am/",city="Yerevan",district="Kanaker-Zeytun",address="Near D. Anhaght St - K. Ulnetsi St intersection, Victory Park slope, Yerevan",lat=40.201698,lng=44.530921,
 status="under construction",floors="14",type="residential",phones=["+37455111040","+37455111050"],email="info@siluet.am",
 social={"facebook":"https://www.facebook.com/p/Siluet-Residence-61561954467773/","instagram":"https://www.instagram.com/siluet_residence"},
 images=[M+x for x in ["ecf/eq14f9yffs6zfrzpd22bq7d3mpbgzddw.jpg","4ce/43u89mmtdrhhwy7aa155j15rrx18ayjy.jpg","0c6/79ulrl8drz056x704tvjeyfdedaeq5os.jpg","e09/jys9i83nngg81x37i47unujapbwt5k31.jpg","610/447uzy2g5vboncowktm0hy554j2vod3o.jpg"]],
 description="Premium-class gated complex of two distinctive 14-storey buildings (ground floor public, setback top floor) designed by Graphit Architectural Studio, on the high slope of Victory Park near the Anhaght/Ulnetsi intersection, visible from Mashtots Ave. ~4,000 m2 site with only 1,600 m2 built; 2,400 m2 car-free restricted-access landscaped courtyard; underground parking entered from the street; parametric facades with perimeter balconies; energy-efficient boiler house with central heating and hot water; 4 European lifts per building; managed by Siluet Invest after completion.")]
save("35_siluet",P)
