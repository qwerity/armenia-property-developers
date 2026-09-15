import sys,re,hashlib,os
SP=os.path.dirname(os.path.abspath(__file__))
u=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else r'(֏|AMD|դրամ|USD|\$|м²|m²|մ²|m2|sq)'
w=int(sys.argv[3]) if len(sys.argv)>3 else 80
t=open(os.path.join(SP,'pages',hashlib.md5(u.encode()).hexdigest()[:10])+'.txt').read()
seen=set();n=0
for m in re.finditer(pat,t,re.I):
    s=t[max(0,m.start()-w):m.end()+w]
    k=s[w//2:w+w//2]
    if k in seen: continue
    seen.add(k);print('...',s);n+=1
    if n>60: break
