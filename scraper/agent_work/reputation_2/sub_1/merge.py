import json, glob, os

D = os.path.dirname(os.path.abspath(__file__))
order = [x["developer"] for x in json.load(open(os.path.join(D, "..", "chunk_1.json")))]
recs = {}
for f in glob.glob(os.path.join(D, "e_*.json")):
    for r in json.load(open(f)):
        assert r["developer"] in order, r["developer"]
        recs[r["developer"]] = r
out = [recs[n] for n in order if n in recs]
json.dump(out, open(os.path.join(D, "..", "entities_1.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "of", len(order), "missing:", [n for n in order if n not in recs])
