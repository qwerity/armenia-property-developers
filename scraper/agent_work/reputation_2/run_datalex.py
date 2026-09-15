"""Poll entities_*.json and run datalex.find_cases for each developer whose names are known."""
import hashlib, json, sys, time
from pathlib import Path
sys.path.insert(0, "/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
import datalex
datalex.MIN_INTERVAL = 4
D = Path(__file__).parent
RAW = D / "court_raw"; RAW.mkdir(exist_ok=True)
TOTAL = len(json.load(open("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.rep_devs_2.json")))

def key(dev): return hashlib.md5(dev.encode()).hexdigest()[:10]

while True:
    done = 0
    for f in sorted(D.glob("entities_*.json")):
        try: items = json.loads(f.read_text())
        except Exception: continue
        for it in items:
            names = [n.strip() for n in it.get("datalex_names") or [] if n and n.strip()]
            out = RAW / f"{key(it['developer'])}.json"
            if out.exists():
                prev = json.loads(out.read_text())
                if prev["names"] == names and prev.get("tax_id") == it.get("tax_id_for_search"):
                    done += 1; continue
            if not names: continue
            t = it.get("tax_id_for_search")
            print(time.strftime("%H:%M:%S"), it["developer"], names, t, flush=True)
            cases = datalex.find_cases(names, tax_id=t)
            out.write_text(json.dumps({"developer": it["developer"], "names": names, "tax_id": t, "cases": cases}, ensure_ascii=False))
            print("  ->", len(cases), flush=True)
            done += 1
    if done >= TOTAL: print("ALL DONE"); break
    time.sleep(60)
