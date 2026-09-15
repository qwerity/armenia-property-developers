import sys, re, json, f, concurrent.futures as cf
args=[a for a in sys.argv[1:] if not a.startswith('--')]
opts=dict(a[2:].split('=',1) for a in sys.argv[1:] if a.startswith('--'))
n=int(opts.get('n',2500)); skip=opts.get('skip',''); imgpat=opts.get('img','')
with cf.ThreadPoolExecutor(3) as ex: list(ex.map(f.get,args))
for u in args:
    h=f.get(u); m=f.meta(u,h); t=f.text(h)
    if skip:
        i=t.find(skip); t=t[i:] if i>=0 else t
    imgs=[i for i in m['images'] if (not imgpat or re.search(imgpat,i))]
    print('=====',u, '|', m['title']); print('COORDS',m['coords'],'VID',m['videos'],'IFR',[x for x in m['iframes'] if 'map' in x][:2])
    print('IMGS',len(imgs),imgs[:14]); print(t[:n]); print()
