import sys; sys.path.insert(0,'.')
from mk import *
P=[rec(source_url="https://deka.am/resort/",title="Byurakan Resort",developer="Deka (Deka 10 LLC)",developer_url="https://deka.am/",city="Byurakan",district="Aragatsotn",address="Byurakan, Aragatsotn",status="planned",type="resort",phones=["+37411590101","+37444590101"],email="info@deka.am",
 social={"facebook":"https://www.facebook.com/www.deka.am","instagram":"https://instagram.com/deka.am","youtube":"https://www.youtube.com/channel/UCZGIrHna_-SRTv7W1GaqXsg"},
 description="Resort project in Byurakan announced as 'coming soon' on the Deka site; no further details published. Deka otherwise markets turnkey private-house construction (2-storey houses of 102-148 m2 from 23.5-31.5 million AMD) and house design catalogue.")]
save("13_deka",P,{"note":"Deka sells house designs/turnkey private house construction; only branded project is Byurakan Resort (coming soon)"})
