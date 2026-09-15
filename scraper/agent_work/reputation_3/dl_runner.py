import glob, json, re, sys, time, hashlib
from pathlib import Path
sys.path.insert(0, "/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
import datalex
datalex.MIN_INTERVAL = 4
R = Path(__file__).resolve().parent
OUT = R / "datalex"
OUT.mkdir(exist_ok=True)


def wanted():
    w = {}
    seeds = R / "seeds.json"
    if seeds.exists():
        for dev, v in json.loads(seeds.read_text()).items():
            if dev.startswith("_"):
                continue
            w.setdefault(dev, {"names": [], "tax": []})
            w[dev]["names"] += v.get("names", [])
            w[dev]["tax"] += v.get("tax", [])
    for f in sorted(glob.glob(str(R / "web_*.json"))):
        try:
            arr = json.loads(Path(f).read_text())
        except Exception:
            continue
        for x in arr:
            d = w.setdefault(x["developer"], {"names": [], "tax": []})
            d["names"] += [n for n in x.get("datalex_names") or [] if n]
            d["tax"] += [t for t in (x.get("tax_ids") or []) if t]
            for e in x.get("legal_entities") or []:
                if e.get("tax_id"):
                    d["tax"].append(str(e["tax_id"]))
    excl = set()
    if seeds.exists():
        excl = {datalex.normalize_org(n) for n in json.loads(seeds.read_text()).get("_exclude", [])}
    for d in w.values():
        seen, names = set(excl), []
        for n in d["names"]:
            k = datalex.normalize_org(n)
            if k and k not in seen:
                seen.add(k)
                names.append(n)
        d["names"] = names[:4]
        d["tax"] = list(dict.fromkeys(d["tax"]))
    return w


def slug(dev):
    return hashlib.md5(dev.encode()).hexdigest()[:10]


while True:
    did = False
    for dev, v in wanted().items():
        if not v["names"]:
            continue
        f = OUT / f"{slug(dev)}.json"
        sig = {"names": v["names"], "tax": v["tax"]}
        if f.exists() and json.loads(f.read_text()).get("sig") == sig:
            continue
        cases = []
        taxes = v["tax"] or [None]
        for t in taxes:
            for c in datalex.find_cases(v["names"], tax_id=t):
                if c not in cases:
                    cases.append(c)
        f.write_text(json.dumps({"developer": dev, "sig": sig, "cases": cases}, ensure_ascii=False))
        print(time.strftime("%H:%M:%S"), dev, v["names"], len(cases), flush=True)
        did = True
    if (R / "STOP").exists() and not did:
        break
    if not did:
        time.sleep(60)
