"""Merge research_*.json (entities/news) with datalex_results/* into developer_reputation_4.json."""
import json, re, glob, sys
sys.path.insert(0, "/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
from datalex import normalize_org
from pathlib import Path

D = Path(__file__).resolve().parent
OUT = Path("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developer_reputation_4.json")
DEVS = json.load(open("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.rep_devs_4.json"))
ORG = re.compile(r"ՍՊԸ|ՓԲԸ|ԲԲԸ|ՀԿ|ՊՈԱԿ|ՊՈԱԿ|«|»|\"|ԲԱՆԿ|բանկ|Բանկ|համայնք|Համայնք|ՀԱՄԱՅՆՔ|ծառայություն|Ծառայություն|ԾԱՌԱՅՈՒԹՅՈՒՆ|կոմիտե|Կոմիտե|ԿՈՄԻՏԵ|նախարարություն|ՆԱԽԱՐԱՐՈՒԹՅՈՒՆ|Նախարարություն|ՀԱՆՐԱՊԵՏՈՒԹՅՈՒՆ|Հանրապետություն|հիմնադրամ|ՀԻՄՆԱԴՐԱՄ|Հիմնադրամ|ԿԵՆՏՐՈՆ|կենտրոն|քաղաքապետարան|ՔԱՂԱՔԱՊԵՏԱՐԱՆ|Քաղաքապետարան|դատախազ|ԴԱՏԱԽԱԶ|Դատախազ|տեսչական|ՏԵՍՉԱԿԱՆ|Տեսչական|մարմին|ՄԱՐՄԻՆ|ԳՐԱՍԵՆՅԱԿ|գրասենյակ|ընկերություն|ԸՆԿԵՐՈՒԹՅՈՒՆ|ԱՁ|LLC|CJSC|ООО|ЗАО|ОАО|ԿՈՈՊԵՐԱՏԻՎ|ԳՈՐԾԱԿԱԼՈՒԹՅՈՒՆ|ՎԱՐՉՈՒԹՅՈՒՆ|վարչություն|Վարչություն|ԿԱԶՄԱԿԵՐՊՈՒԹՅՈՒՆ|կազմակերպություն|Կազմակերպություն|ՄԻՈՒԹՅՈՒՆ|միություն|ԿՈՄՊԱՆԻԱ|Ռոստելեկոմ|Ա\.Ձ")


ORG2 = re.compile(r"ԳՐՈՒՊ|գրուպ|Գրուպ|ԻՆՇՈՒՐԱՆՍ|ինշուրանս|Ինշուրանս|ՋՈՒՐ|Ջուր|ԱՐՄԵՆԻԱ|Արմենիա|ՔՆՍԹՐԱՔՇՆ|ՔՈՆՍԹՐԱՔՇՆ|ԴԵՎԵԼՈՓՄԵՆԹ|համատիրություն|ՀԱՄԱՏԻՐՈՒԹՅՈՒՆ|Բիլդինգ|ԲԻԼԴԻՆԳ|(^| )ՇԻՆ( |$)|(^| )Շին( |$)|ՏԵԼԵԿՈՄ|ՓԱՅՈՆԻԵՐԶ|ԷՖԵՍ|Այլոֆթ|սնանկության|կառավարիչ|\d")


def is_individual(name: str) -> bool:
    """True when a datalex party string looks like one or more natural persons (buyers), not an organisation."""
    n = (name or "").strip()
    if not n or ORG.search(n) or ORG2.search(n):
        return False
    first = n.split(",")[0].split()
    if len(first) == 2 and first[0].isupper() and first[1].isupper():
        return False
    return 2 <= len(first) <= 4


def load_research():
    res = {}
    for f in sorted(D.glob("research_*.json")):
        try:
            for r in json.load(open(f, encoding="utf-8")):
                res[r["developer"]] = r
        except (ValueError, KeyError):
            print("bad", f)
    return res


def load_cases():
    by_dev = {}
    for f in D.glob("datalex_results/*.json"):
        d = json.load(open(f, encoding="utf-8"))
        by_dev.setdefault(d["item"]["dev"].strip(), []).append(d)
    return by_dev


def year_of(c):
    if c.get("filed"):
        return c["filed"][:4]
    m = re.search(r"/(\d\d)$", c.get("case_number") or "")
    return ("20" + m.group(1)) if m else ""


def own_party(c):
    return normalize_org(c["respondent"] if c["role"] == "respondent" else c["claimant"])


def summarize(cases, overrides):
    inc = [re.compile(x) for x in overrides.get("party_include", [])]
    exc = [re.compile(x) for x in overrides.get("party_exclude", [])]
    cs = [c for c in cases if "error" not in c and (c["case_number"], c["tab"]) not in overrides.get("exclude", set())
          and (not inc or any(r.search(own_party(c).upper()) for r in inc))
          and not any(r.search(own_party(c).upper()) for r in exc)]
    errs = [c["error"] for c in cases if "error" in c]
    uniq = {}
    for c in cs:
        uniq.setdefault((c["case_number"], c["tab"], c["role"]), c)
    cs = list(uniq.values())
    ct = lambda f: sum(1 for c in cs if f(c))
    court = {
        "total": len({(c["case_number"], c["tab"]) for c in cs}),
        "respondent": ct(lambda c: c["role"] == "respondent"),
        "claimant": ct(lambda c: c["role"] == "claimant"),
        "respondent_by_individuals": ct(lambda c: c["role"] == "respondent" and is_individual(c["claimant"])),
        "bankruptcy_as_debtor": ct(lambda c: c["tab"] == "bankruptcy" and c["role"] == "respondent"),
        "criminal": ct(lambda c: c["tab"] == "criminal"),
        "administrative": ct(lambda c: c["tab"] == "administrative"),
        "payment_order": ct(lambda c: c["tab"] == "payment_order"),
        "since_2021": len({(c["case_number"], c["tab"]) for c in cs if year_of(c) >= "2021"}),
        "notable": overrides.get("notable", []),
    }
    return court, cs, errs


if __name__ == "__main__":
    research = load_research()
    cases = load_cases()
    ov = json.load(open(D / "overrides.json", encoding="utf-8")) if (D / "overrides.json").exists() else {}
    out, detail = [], {}
    for dv in DEVS:
        name = dv["developer"]
        r = research.get(name, {})
        o = dict(ov.get(name, {}))
        if "same_as" in o:
            o = {**ov[o["same_as"]], **{k: v for k, v in o.items() if k != "same_as"}}
        o["exclude"] = {tuple(x) for x in o.get("exclude", [])}
        wanted = {x.strip().upper() for x in r.get("datalex_names", []) + o.get("names", [])}
        items = [it for v in cases.values() for it in v
                 if it["item"]["dev"].strip() == name.strip() or wanted & {x.strip().upper() for x in it["item"]["names"]}]
        if "names" in o:
            only = {x.strip().upper() for x in o["names"]}
            items = [it for it in items if only & {x.strip().upper() for x in it["item"]["names"]}]
        allc, searched = [], []
        for it in items:
            searched += it["item"]["names"]
            allc += it["cases"]
        court, cs, errs = summarize(allc, o)
        detail[name] = cs
        rec = {
            "developer": name, "role": o.get("role") or r.get("role", "unknown"),
            "legal_entities": r.get("legal_entities", []) + o.get("entities_add", []), "founded_year": r.get("founded_year"),
            "searched_names": list(dict.fromkeys(searched)), "court": court,
            "news_issues": r.get("news_issues", []) + o.get("news_add", []), "positives": r.get("positives", []) + o.get("positives_add", []),
            "confidence": o.get("confidence") or r.get("confidence", "low"),
            "notes": " ".join(x for x in [r.get("notes", ""), o.get("notes", ""), ("datalex errors: " + "; ".join(errs)) if errs else ""] if x).strip(),
        }
        out.append(rec)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (D / "court_detail.json").write_text(json.dumps(detail, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(out), "written;", sum(1 for x in out if x["searched_names"]), "with datalex;", sum(1 for x in out if x["legal_entities"]), "with entities")
