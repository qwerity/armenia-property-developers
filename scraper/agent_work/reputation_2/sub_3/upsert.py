#!/usr/bin/env python3
"""usage: upsert.py ENTRY.json -- upsert entry (by developer) into entities_3.json keeping chunk order."""
import json, sys, os

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(B, "entities_3.json")
order = [x["developer"] for x in json.load(open(os.path.join(B, "chunk_3.json")))]
new = json.load(open(sys.argv[1]))
new = new if isinstance(new, list) else [new]
cur = json.load(open(out)) if os.path.exists(out) else []
d = {e["developer"]: e for e in cur}
for e in new:
    assert e["developer"] in order, e["developer"]
    d[e["developer"]] = e
res = [d[n] for n in order if n in d]
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
print("entries:", len(res))
