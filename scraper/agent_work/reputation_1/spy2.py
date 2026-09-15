import sys,re
from spy import page
for p in sys.argv[1:]:
    t=page(p)
    i=t.find('Սփյուռ» :')
    j=t.find('Ֆոտոշարք') if 'Ֆոտոշարք' in t else i+1500
    print('##',p); print(t[i+9:i+900])
    k=t.find('Գործունեություն ',i)
    print('  ACT:',t[k:k+500])
    for m in re.finditer(r'(ՀՎՀՀ|Հիմնադր|գրանցման|Tax|\b\d{8}\b)',t): print('  HIT:',t[max(0,m.start()-60):m.start()+60])
    print()
