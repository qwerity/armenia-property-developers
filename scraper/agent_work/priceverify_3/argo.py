import re,sys,hashlib
u=sys.argv[1]
t=open('pages/'+hashlib.md5(u.encode()).hexdigest()[:10]+'.txt').read()
rows=[(float(m.group(5).replace(',','')),int(m.group(6).replace(',','')),int(m.group(7).replace(',','')),m.group(4),m.group(2),m.group(3)) for m in re.finditer(r'Apartment (\S+) Building (\S+) (-?\d+) (\S+ սենյակ) ([\d.,]+) ([\d,]+) ([\d,]+)',t)]
print('units',len(rows))
for r in sorted(rows,key=lambda r:r[1])[:6]: print('  m2price',r[1],'total',r[2],'area',r[0],r[3],'bldg',r[4],'fl',r[5], 'check',round(r[2]/r[0]))
print('cheapest total',min(rows,key=lambda r:r[2]) if rows else None)
