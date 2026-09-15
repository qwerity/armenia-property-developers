import json,glob,sys,hashlib,re
n=json.load(open('names.json'))
def key(dev, names, tax): return hashlib.md5(json.dumps([dev, sorted(names), tax], ensure_ascii=False).encode()).hexdigest()[:12]
lim=int(sys.argv[1]); 
for dev in sys.argv[2:]:
    v=n[dev]
    try: d=json.load(open('court/%s.json'%key(dev,v['names'],v.get('tax_id'))))
    except FileNotFoundError: print('== pending',dev); continue
    cs=[c for c in d['cases'] if 'error' not in c]
    print('==',dev,v['names'],v.get('tax_id'),len(cs))
    for c in sorted(cs,key=lambda c:c.get('filed') or c['case_number'][-2:],reverse=True)[:lim]:
        print('  ',c['tab'][:4],c['role'][:4],c['case_number'],(c.get('filed') or '')[:7],'|',c['claimant'][:40],'|',c['respondent'][:40],'|',re.sub(r'\s+',' ',c['claim'])[:130])
