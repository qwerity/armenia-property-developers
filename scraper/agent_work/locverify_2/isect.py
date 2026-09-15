import sys
from ovp import run
a,b,bb=sys.argv[1],sys.argv[2],sys.argv[3]
q=f'[out:json][timeout:60];way["highway"]["name"~"{a}"]{bb}->.a;way["highway"]["name"~"{b}"]{bb}->.b;node(w.a)->.na;node(w.b)->.nb;node.na.nb;out;'
for e in run(q)["elements"]: print(e["lat"],e["lon"])
