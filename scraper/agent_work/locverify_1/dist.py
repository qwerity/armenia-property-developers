import sys,math
a=list(map(float,sys.argv[1:5]))
R=6371000;p1,p2=math.radians(a[0]),math.radians(a[2]);dp=p2-p1;dl=math.radians(a[3]-a[1])
h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
print(round(2*R*math.asin(math.sqrt(h))))
