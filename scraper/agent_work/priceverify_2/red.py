import json,subprocess,time,sys
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for pid in sys.argv[1:]:
    r=subprocess.run(['curl','-s','-m','40','-A',UA,'-H','Accept: application/json','-H','Accept-Language: en',f'https://redgroup.am/api/projects/{pid}'],capture_output=True,text=True)
    open(f'red_{pid}.json','w').write(r.stdout)
    d=json.loads(r.stdout); p=d['project']
    print('==',pid,p['slug'],p.get('status'),'all_products_count',d.get('all_products_count'),'min_area',d.get('min_area'),d.get('max_area'))
    print('  keys',[k for k in d])
    pr=d.get('products') or []
    print('  products',len(pr))
    if pr: print('  sample',json.dumps({k:v for k,v in pr[0].items() if not isinstance(v,(list,dict))},ensure_ascii=False)[:600])
    for x in sorted(pr,key=lambda x:(x.get('price') or 0)/(x.get('area') or 1))[:12]:
        print('   ',x.get('property_type_id'),x.get('rooms'),x.get('area'),x.get('price'),'cur',x.get('currency_id'),'status',x.get('status'),'%.0f'%((x.get('price') or 0)/(x.get('area') or 1)))
    time.sleep(1)
