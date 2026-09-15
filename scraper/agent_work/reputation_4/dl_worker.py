import hashlib, json, sys, time
from pathlib import Path
sys.path.insert(0, "/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
import datalex
datalex.MIN_INTERVAL = 4
D = Path(__file__).resolve().parent
Q = D / "datalex_queue.jsonl"
R = D / "datalex_results"
R.mkdir(exist_ok=True)


def key(item):
    return hashlib.md5(json.dumps([sorted(item["names"]), item.get("tax_id")], ensure_ascii=False).encode()).hexdigest()


while True:
    items = []
    for qf in sorted(D.glob("queue_*.jsonl")):
        for l in qf.read_text(encoding="utf-8").splitlines():
            try:
                items.append(json.loads(l))
            except ValueError:
                pass
    todo = [i for i in items if not (R / f"{key(i)}.json").exists()]
    if not todo:
        if (D / "DONE").exists():
            break
        time.sleep(10)
        continue
    it = todo[0]
    t = time.time()
    try:
        cases = datalex.find_cases(it["names"], tax_id=it.get("tax_id"))
    except Exception as e:
        cases = [{"error": str(e)}]
    (R / f"{key(it)}.json").write_text(json.dumps({"item": it, "cases": cases}, ensure_ascii=False), encoding="utf-8")
    print(f"{it['dev']} {it['names']} -> {len(cases)} ({time.time()-t:.0f}s)", flush=True)
