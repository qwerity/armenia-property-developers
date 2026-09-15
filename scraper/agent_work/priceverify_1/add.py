"""Upsert verification entries (JSON list on stdin) into price_verified_1.json, keeping input order."""
import json, sys, os

OUT = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/price_verified_1.json"
INP = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.price_verify_1.json"
RATE = 363.5
KEYS = ["id", "title", "verdict", "usd_m2", "amd_m2", "currency_shown", "apartment_from_total", "apartment_from_area_m2",
        "evidence_url", "evidence_text", "sold_out", "wrong_merge_urls", "notes"]

order = {x["id"]: (i, x["title"]) for i, x in enumerate(json.load(open(INP)))}
cur = {e["id"]: e for e in json.load(open(OUT))} if os.path.exists(OUT) else {}
for e in json.load(sys.stdin):
    assert e["id"] in order, e["id"]
    e.setdefault("title", order[e["id"]][1])
    if e.get("amd_m2") and not e.get("usd_m2"):
        e["usd_m2"] = round(e["amd_m2"] / RATE)
    if e.get("usd_m2") and not e.get("amd_m2"):
        e["amd_m2"] = round(e["usd_m2"] * RATE)
    for k in KEYS:
        e.setdefault(k, [] if k == "wrong_merge_urls" else None)
    assert e["verdict"] in ("confirmed", "corrected", "unverifiable")
    assert len(e["evidence_text"] or "") <= 120, e["id"]
    cur[e["id"]] = {k: e[k] for k in KEYS}
res = sorted(cur.values(), key=lambda e: order[e["id"]][0])
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
print(len(res), "entries;", {v: sum(e["verdict"] == v for e in res) for v in ("confirmed", "corrected", "unverifiable")})
