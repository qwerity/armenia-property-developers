"""Poll names.json and run datalex.find_cases for each (developer, names, tax_id) entry not yet done."""
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
import datalex  # noqa: E402

datalex.MIN_INTERVAL = 4
S = Path(__file__).resolve().parent
OUT = S / "court"
OUT.mkdir(exist_ok=True)


def key(dev, names, tax):
    return hashlib.md5(json.dumps([dev, sorted(names), tax], ensure_ascii=False).encode()).hexdigest()[:12]


while True:
    try:
        todo = json.loads((S / "names.json").read_text(encoding="utf-8"))
    except Exception:
        todo = {}
    pending = sorted([(d, v) for d, v in todo.items() if not (OUT / f"{key(d, v['names'], v.get('tax_id'))}.json").exists()], key=lambda x: not x[0].startswith("__probe"))
    if not pending:
        if (S / "DONE").exists():
            break
        time.sleep(20)
        continue
    dev, v = pending[0]
    k = key(dev, v["names"], v.get("tax_id"))
    t = time.time()
    cases = datalex.find_cases(v["names"], tax_id=v.get("tax_id"), tabs=v.get("tabs"), max_pages=v.get("max_pages", 5))
    (OUT / f"{k}.json").write_text(json.dumps({"developer": dev, "names": v["names"], "tax_id": v.get("tax_id"), "cases": cases},
                                              ensure_ascii=False), encoding="utf-8")
    print(f"{dev}: {len(cases)} cases ({time.time() - t:.0f}s)", flush=True)
