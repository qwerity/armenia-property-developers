import sys,math
a=list(map(float,sys.argv[1:]))
def h(la1,lo1,la2,lo2):
    R=6371000;p=math.radians
    return 2*R*math.asin(math.sqrt(math.sin(p(la2-la1)/2)**2+math.cos(p(la1))*math.cos(p(la2))*math.sin(p(lo2-lo1)/2)**2))
for i in range(4,len(a)+1,2): print(round(h(a[0],a[1],a[i-2],a[i-1])))
