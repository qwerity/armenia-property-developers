import json, glob, sys, re
sys.path.insert(0, '.')
from merge import court_summary, is_individual, cats
only = sys.argv[1:]
for f in glob.glob('datalex/*.json'):
    j = json.load(open(f))
    if only and j['developer'] not in only: continue
    cs = [c for c in j['cases'] if 'error' not in c]
    s, ind = court_summary(j['cases'])
    s.pop('notable')
    print('\n=====', j['developer'], j['sig']['names'], j['sig']['tax'], s)
    for c in sorted(cs, key=lambda c: c['filed'], reverse=True):
        tag = 'IND' if c in ind else ''
        cl = re.sub(r'^.*?(ԽՆԴՐՈՒՄ ԵՄ|ԽՆԴՐՈՒՄ ԵՆՔ|խնդրում եմ|խնդրում ենք|Խնդրում եմ|Խնդրում ենք)', '', c['claim'])[:170]
        print(f" {c['filed']} {c['tab'][:4]} {c['role'][:4]} {tag:3} {c['case_number']} | {c['claimant'][:35]} v {c['respondent'][:30]} | {cl}")
