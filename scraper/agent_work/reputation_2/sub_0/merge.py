import json,glob,os,sys
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(D)
order=[x['developer'] for x in json.load(open(R+'/chunk_0.json'))]
es={}
for f in glob.glob(D+'/e_*.json'):
    e=json.load(open(f)); es[e['developer']]=e
bad=[k for k in es if k not in order]
out=[es[k] for k in order if k in es]
json.dump(out,open(R+'/entities_0.json','w'),ensure_ascii=False,indent=1)
print(len(out),'written; unmatched:',bad)
