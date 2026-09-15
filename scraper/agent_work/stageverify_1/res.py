import json, sys, os

OUT = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/stage_verified_1.json"
SRC = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.stage_verify_1.json"


def add(rec):
    data = json.load(open(OUT)) if os.path.exists(OUT) else []
    titles = {x["id"]: x["title"] for x in json.load(open(SRC))}
    rec.setdefault("title", titles.get(rec["id"], ""))
    order = ["id", "title", "stage", "start", "completion", "confidence", "evidence_url", "evidence", "imagery", "notes"]
    rec = {k: rec.get(k) for k in order}
    data = [x for x in data if x["id"] != rec["id"]] + [rec]
    idx = {k: i for i, k in enumerate(titles)}
    data.sort(key=lambda x: idx.get(x["id"], 999))
    json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(len(data), "records")


if __name__ == "__main__":
    for r in json.loads(sys.stdin.read()):
        add(r)
