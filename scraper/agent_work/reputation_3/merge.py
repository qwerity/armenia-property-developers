import glob, hashlib, json, re, sys
from pathlib import Path
R = Path(__file__).resolve().parent
SRC = Path("/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
OUT = SRC / "developer_reputation_3.json"

ORG = re.compile(r"ՍՊԸ|ՓԲԸ|ԲԲԸ|ԲԸ\b|ԱՁ|ՀԿ|ՊՈԱԿ|ՀՈԱԿ|«|»|<|>|\"|ԲԱՆԿ|Բանկ|ՀՀ |Հայաստանի|համայնք|ՀԱՄԱՅՆՔ|ԿՈՄԻՏԵ|կոմիտե|ծառայություն|ԾԱՌԱՅՈՒԹՅՈՒՆ|նախարարություն|ՆԱԽԱՐԱՐՈՒԹՅՈՒՆ|ՏԵՍՉԱԿԱՆ|տեսչական|ԴԱՏԱԽԱԶ|դատախազ|ՔԱՂԱՔԱՊԵՏԱՐԱՆ|քաղաքապետարան|ՄԻՈՒԹՅՈՒՆ|ԸՆԿԵՐՈՒԹՅՈՒՆ|ընկերություն|ՖՈՆԴ|հիմնադրամ|ԿԱԶՄԱԿԵՐՊՈՒԹՅՈՒՆ|ԳՐԱՍԵՆՅԱԿ|ՀԱՄԱՏԻՐՈՒԹՅՈՒՆ|համատիրություն|ՍՊԱՌՈՂԱԿԱՆ|LLC|CJSC|ООО|ЗАО|Ltd|LTD", re.I)
KW = [("apartment/ownership", r"բնակարան|սեփականության իրավունք|հանձն|ԲՆԱԿԱՐԱՆ"), ("contract termination/invalidity", r"լուծ|անվավեր|ԼՈՒԾ|ԱՆՎԱՎԵՐ"),
      ("damages", r"վնաս|ՎՆԱՍ"), ("money recovery", r"բռնագանձ|ԲՌՆԱԳԱՆՁ|գումար|տոկոս")]


def slug(dev):
    return hashlib.md5(dev.encode()).hexdigest()[:10]


SURNAME = re.compile(r"(յան|յանց|ունց|ենց|ունի|ցի|ով|ովա|ևա|եվա|ինա|իչ|ուկ|ակ)$", re.I)


def _person(p, cl):
    words = p.split()
    if ORG.search(p) or re.search(r"\d", p) or len(words) not in (2, 3):
        return False
    if f"«{p.upper()}»" in cl or re.search(re.escape(p.upper()) + r"»?\s*(ՍՊԸ|ՓԲԸ|ԲԲԸ|ԱՓԲԸ|ՍՊ ԸՆԿ)", cl):
        return False
    return any(SURNAME.search(w) for w in words) or (len(words) == 3 and words[-1].endswith(("ի", "Ի")))


def is_individual(party, claim=""):
    p = re.sub(r"\s+", " ", (party or "").strip())
    cl = (claim or "").upper()
    return bool(p) and any(_person(x.strip(), cl) for x in p.split(",") if x.strip())


def cats(claim):
    return [k for k, rx in KW if re.search(rx, claim or "")]


def court_summary(cases):
    cs = [c for c in cases if "error" not in c]
    resp = [c for c in cs if c["role"] == "respondent"]
    ind = [c for c in resp if is_individual(c["claimant"], c["claim"]) and c["tab"] in ("civil", "payment_order")]
    s = {"total": len(cs), "respondent": len(resp), "claimant": len(cs) - len(resp), "respondent_by_individuals": len(ind),
         "bankruptcy_as_debtor": sum(c["tab"] == "bankruptcy" and c["role"] == "respondent" for c in cs),
         "criminal": sum(c["tab"] == "criminal" for c in cs), "administrative": sum(c["tab"] == "administrative" for c in cs),
         "payment_order": sum(c["tab"] == "payment_order" for c in cs), "since_2021": sum((c.get("filed") or "") >= "2021" for c in cs), "notable": []}
    return s, ind


def filter_cases(cases, m):
    rx = m.get("exclude_party_regex")
    drop = set(m.get("exclude_cases", []))
    out = []
    for c in cases:
        if "error" not in c:
            party = c["respondent"] if c["role"] == "respondent" else c["claimant"]
            if c["case_number"] in drop or (rx and re.search(rx, party, re.I)):
                continue
        out.append(c)
    return out


def ind_note(ind):
    if not ind:
        return ""
    from collections import Counter
    cnt = Counter(k for c in ind for k in (cats(c["claim"]) or ["unspecified"]))
    return f"Suits by individuals as claimant vs company: {len(ind)} (claim keywords: " + ", ".join(f"{k} {v}" for k, v in cnt.most_common()) + ")."


def main():
    devs = json.loads((SRC / ".rep_devs_3.json").read_text())
    web = {}
    for f in sorted(glob.glob(str(R / "web_*.json"))):
        try:
            for x in json.loads(Path(f).read_text()):
                web[x["developer"]] = x
        except Exception as e:
            print("bad", f, e, file=sys.stderr)
    manual = {}
    for f in sorted(glob.glob(str(R / "manual*.json"))):
        manual.update(json.loads(Path(f).read_text()))
    out = []
    for d in devs:
        name = d["developer"]
        w = web.get(name, {})
        dl = R / "datalex" / f"{slug(name)}.json"
        dlj = json.loads(dl.read_text()) if dl.exists() else {"sig": {"names": []}, "cases": []}
        m = manual.get(name, {})
        cases = filter_cases(dlj["cases"], m)
        court, ind = court_summary(cases)
        auto = ind_note(ind)
        court["notable"] = m.get("notable", [])
        errs = [c["error"] for c in dlj["cases"] if "error" in c]
        notes = " ".join(x for x in [w.get("notes", ""), m.get("court_notes", ""), auto, f"datalex errors: {errs[:3]}" if errs else ""] if x)
        out.append({"developer": name, "role": m.get("role") or w.get("role") or "unknown",
                    "legal_entities": w.get("legal_entities", []), "founded_year": w.get("founded_year"),
                    "searched_names": dlj["sig"]["names"], "court": court,
                    "news_issues": w.get("news_issues", []), "positives": w.get("positives", []),
                    "confidence": m.get("confidence") or w.get("entity_confidence") or "low", "notes": notes.strip()})
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("wrote", len(out), "web", len(web), "datalex", len(glob.glob(str(R / "datalex" / "*.json"))))


if __name__ == "__main__":
    main()
