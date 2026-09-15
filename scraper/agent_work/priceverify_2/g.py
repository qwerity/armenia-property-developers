import sys,re
sys.path.insert(0,__import__('os').path.dirname(__file__))
from fetch import fname
pat=sys.argv[1]; n=int(sys.argv[2])
for u in sys.argv[3:]:
    t=open(fname(u)+'.txt',errors='ignore').read()
    print('=====',u,len(t))
    seen=0
    for m in re.finditer(pat,t,re.I):
        s=max(0,m.start()-n); print('  ..',t[s:m.end()+n].replace('\n',' | ')); seen+=1
        if seen>25: break
