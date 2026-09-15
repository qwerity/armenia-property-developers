"""Merge entity/news research with datalex court results into developer_reputation_2.json."""
import hashlib, json, re, sys
from collections import Counter
from pathlib import Path
D = Path(__file__).parent
OUT = Path("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developer_reputation_2.json")
DEVS = json.load(open("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.rep_devs_2.json"))
OVR = json.loads((D / "overrides.json").read_text()) if (D / "overrides.json").exists() else {}
ORG = re.compile(r"ՍՊԸ|ՓԲԸ|ԲԲԸ|ԲԸ\b|\bԱՁ\b|<<|«|\"|ՀՀ|համայնք|ՀԱՄԱՅՆՔ|բանկ|ԲԱՆԿ|ծառայ|ԾԱՌԱՅ|կոմիտե|ԿՈՄԻՏԵ|նախարար|ՆԱԽԱՐԱՐ|տեսչ|ՏԵՍՉ|քաղաքապետ|ՔԱՂԱՔԱՊԵՏ|դատախազ|ԴԱՏԱԽԱԶ|ՊՈԱԿ|հիմնադրամ|ՀԻՄՆԱԴՐԱՄ|ԿԵՆՏՐՈՆ|կենտրոն|ՀԿ|ՕՕՕ|ООО|ЗАО|LLC|CJSC|ԳՐԱՍԵՆՅԱԿ|գրասենյակ|ԱՇԽԱՏԱԿԱԶՄ|ապահովագր|ԱՊԱՀՈՎԱԳՐ|ՍՆԱՆԿՈՒԹՅԱՆ|կառավարիչ|ԿԱՌԱՎԱՐԻՉ|ՎԱՐՉԱԿԱԶՄ|վարչակազմ|ՄԱՐԶՊԵՏ|մարզպետ|ԷԼԵԿՏՐԱԿԱՆ|ԿՈՄՈՒՆԱԼ|ՋՐԱՅԻՆ|ԳԱԶՊՐՈՄ|ՎԵՈԼԻԱ|ՅՈՒՔՈՄ|ԲԻԼԱՅՆ|ՎԻՎԱ|ԹԻՄ|ԸՆԿԵՐՈՒԹՅՈՒՆ|ընկերություն|ԿԱՌՈՒՑԱՊԱՏՈՂ")

def key(dev): return hashlib.md5(dev.encode()).hexdigest()[:10]

SURNAME = re.compile(r"(յան|յանց|եան|ով|ովա|ենկո|ունց|ինա|ևա|եվա|ուկ|ենց)$", re.I)

def _person(seg):
    if ORG.search(seg): return False
    w = seg.split()
    if not 2 <= len(w) <= 4: return False
    if any(SURNAME.search(x) for x in w[1:3]): return True
    return len(w) == 3 and not seg.isupper() and w[2].endswith(("ի", "ու", "ա"))

def is_individual(party):
    return any(_person(p.strip()) for p in party.split(","))

def claim_kind(c):
    c = c.lower(); k = []
    if re.search(r"բռնագանձ|վերադարձ", c): k.append("money recovery")
    if re.search(r"լուծ", c) and "պայմանագ" in c: k.append("contract termination")
    if re.search(r"բնակարան|սեփականության իրավունք|հանձն|փոխանց", c): k.append("apartment/ownership")
    if "վնաս" in c: k.append("damages")
    if "պարտավոր" in c: k.append("obligation performance")
    if "սնանկ" in c: k.append("bankruptcy")
    return k

def summarize(cases):
    cs = [c for c in cases if "error" not in c]
    errs = [c for c in cases if "error" in c]
    tabs = Counter(c["tab"] for c in cs)
    resp = [c for c in cs if c["role"] == "respondent"]
    ind = [c for c in resp if c["tab"] in ("civil", "payment_order") and is_individual(c["claimant"])]
    bkr = [c for c in resp if c["tab"] == "bankruptcy"]
    s = {"total": len(cs), "respondent": len(resp), "claimant": len(cs) - len(resp),
         "respondent_by_individuals": len(ind), "bankruptcy_as_debtor": len(bkr),
         "criminal": tabs.get("criminal", 0), "administrative": tabs.get("administrative", 0),
         "payment_order": tabs.get("payment_order", 0), "since_2021": sum(1 for c in cs if c["filed"] >= "2021"),
         "civil": tabs.get("civil", 0), "bankruptcy_total": tabs.get("bankruptcy", 0),
         "individual_claim_types": dict(Counter(k for c in ind for k in claim_kind(c["claim"])))}
    notable = []
    def add(c, why):
        if len(notable) < 5 and all(n["case_number"] != c["case_number"] for n in notable):
            notable.append({"case_number": c["case_number"], "tab": c["tab"], "filed": c["filed"], "why": why})
    for c in sorted(bkr, key=lambda c: c["filed"], reverse=True): add(c, f"bankruptcy petition against company by {c['claimant'][:60]}: {c['claim'][:120]}")
    for c in sorted([c for c in cs if c["tab"] == "criminal"], key=lambda c: c["filed"], reverse=True): add(c, f"criminal case ({c['role']}): {c['claim'][:140]}")
    for c in sorted(ind, key=lambda c: c["filed"], reverse=True): add(c, f"individual {c['claimant'][:50]} v company: {c['claim'][:140]}")
    for c in sorted([c for c in resp if c not in ind and c not in bkr and c["tab"] != "criminal"], key=lambda c: c["filed"], reverse=True): add(c, f"{c['claimant'][:60]} v company ({c['tab']}): {c['claim'][:120]}")
    return s, notable, errs

ents = {}
for f in sorted(D.glob("entities_*.json")):
    try:
        for it in json.loads(f.read_text()): ents[it["developer"]] = it
    except Exception as e: print("bad", f, e, file=sys.stderr)
res = []
for dv in DEVS:
    name = dv["developer"]; it = ents.get(name)
    if not it: continue
    raw = D / "court_raw" / f"{key(name)}.json"
    rec = {"developer": name, "role": it.get("role", "unknown"), "legal_entities": it.get("legal_entities", []),
           "founded_year": it.get("founded_year"), "searched_names": it.get("datalex_names", []),
           "court": None, "news_issues": it.get("news_issues", []), "positives": it.get("positives", []),
           "confidence": it.get("confidence", "low"), "notes": it.get("notes", "")}
    if raw.exists():
        r = json.loads(raw.read_text())
        o0 = OVR.get(name) or {}
        cases = r["cases"]
        if o0.get("drop_all"): cases = []
        if o0.get("keep_party_regex"):
            cases = [c for c in cases if "error" in c or re.search(o0["keep_party_regex"], c["respondent"] if c["role"] == "respondent" else c["claimant"])]
        if o0.get("drop_party_regex"):
            cases = [c for c in cases if "error" in c or not re.search(o0["drop_party_regex"], c["respondent"] if c["role"] == "respondent" else c["claimant"])]
        s, notable, errs = summarize(cases)
        rec["searched_names"] = r["names"]
        rec["court"] = {k: s[k] for k in ("total", "respondent", "claimant", "respondent_by_individuals", "bankruptcy_as_debtor", "criminal", "administrative", "payment_order", "since_2021")}
        rec["court"]["civil"] = s["civil"]; rec["court"]["individual_claim_types"] = s["individual_claim_types"]
        rec["court"]["notable"] = notable
        if errs: rec["court"]["errors"] = [e["error"] for e in errs][:5]
    o = OVR.get(name) or {}
    for k, v in o.items():
        if k in ("drop_all", "keep_party_regex", "drop_party_regex"): continue
        if k == "court" and rec["court"]: rec["court"].update(v)
        elif k == "notes_append": rec["notes"] = (rec["notes"] + " " + v).strip()
        else: rec[k] = v
    res.append(rec)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
print(len(res), "written;", sum(1 for r in res if r["court"]), "with court")
