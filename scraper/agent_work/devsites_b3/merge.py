import json, glob, os, re

D = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developer_projects_b3.json"
KEYS = ["source", "source_url", "title", "developer", "developer_url", "city", "district", "address", "lat", "lng",
        "price_min_usd_m2", "price_min_amd_m2", "price_currency_raw", "completion", "status", "floors", "type", "phones",
        "email", "website", "social", "images", "videos", "description", "apartments"]


def norm(r, dev):
    o = {}
    for k in KEYS:
        v = r.get(k, dev.get(k))
        if v is None:
            v = {"phones": [], "images": [], "videos": [], "social": {}, "apartments": None}.get(k, None if k in ("lat", "lng", "price_min_usd_m2", "price_min_amd_m2", "completion", "status", "type") else "")
        o[k] = v
    s = {"facebook": "", "instagram": "", "youtube": "", "telegram": ""}
    s.update(o["social"] or {})
    o["social"] = s
    o["images"] = list(dict.fromkeys(u.replace(" ", "%20") for u in o["images"]))[:12]
    o["videos"] = list(dict.fromkeys(o["videos"]))
    o["description"] = (o["description"] or "")[:700]
    if o["apartments"] is None:
        del o["apartments"]
    return o


out, seen = [], set()
for f in sorted(glob.glob(os.path.join(D, "recs", "*.json"))):
    j = json.load(open(f))
    dev = j["dev"]
    for r in j["projects"]:
        o = norm(r, dev)
        key = (o["source_url"], o["title"].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(o)
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(out), "records")
