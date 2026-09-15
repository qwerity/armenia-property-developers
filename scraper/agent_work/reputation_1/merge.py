"""Merge research_*.json (entities/news) with court/*.json (datalex) into developer_reputation_1.json.

Also syncs names.json from research datalex_names so the court runner picks them up.
Usage: python3 merge.py [--sync-only]
"""
import glob
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/Users/ksh/agents/news-agent/armenia-new-builds/scraper")
import datalex  # noqa: E402

S = Path(__file__).resolve().parent
OUT = Path("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developer_reputation_1.json")
DEVS = json.loads(Path("/Users/ksh/agents/news-agent/armenia-new-builds/scraper/.rep_devs_1.json").read_text(encoding="utf-8"))
ORG_RE = re.compile(r"ՍՊԸ|ՓԲԸ|ԲԲԸ|ԱՁ|ՀԿ|ՊՈԱԿ|ՀՈԱԿ|[«»\"<>“”]|&lt;|ԲԱՆԿ|ՀՀ |ՀԱՆՐԱՊԵՏՈՒԹՅՈՒՆ|ՀԱՄԱՅՆՔ|ՔԱՂԱՔԱՊԵՏԱՐԱՆ|ԿՈՄԻՏԵ|"
                    r"ԾԱՌԱՅՈՒԹՅՈՒՆ|ՆԱԽԱՐԱՐՈՒԹՅՈՒՆ|ԴԱՏԱԽԱԶ|ՄԻՈՒԹՅՈՒՆ|ԸՆԿԵՐՈՒԹՅՈՒՆ|ՏԵՍՉԱԿԱՆ|ԿԱՌԱՎԱՐԻՉ|ՀԻՄՆԱԴՐԱՄ|ԿՈՈՊԵՐԱՏԻՎ|ԳՐԱՍԵՆՅԱԿ|"
                    r"ՎԱՐՉԱԿԱՆ|ՇՐՋԱՆ|ՏԵԼԵԿՈՄ|ԱՐՄԵՆԻԱ|ԱՌՈՂՋԱՐԱՆ|ՋՈՒՐ|ՀԱՄԱՏԻՐՈՒԹՅՈՒՆ|ԳԱԶ|ԷԼԵԿՏՐԱԿԱՆ|ՑԱՆՑ|ՀԱՅԱՍՏԱՆ|ՀԻՄՆԱՐԿ|ՄԱՐԶ|ՎԱՐՉԱՊԵՏ|"
                    r"LLC|CJSC|ООО|ЗАО|[A-Z]{3,}", re.I)


SUP = json.loads((S / "supplement.json").read_text(encoding="utf-8")) if (S / "supplement.json").exists() else {}


def key(dev, names, tax):
    return hashlib.md5(json.dumps([dev, sorted(names), tax], ensure_ascii=False).encode()).hexdigest()[:12]


def load_research() -> dict:
    res = {}
    for f in sorted(glob.glob(str(S / "research_*.json"))):
        try:
            for r in json.loads(Path(f).read_text(encoding="utf-8")):
                res[r["developer"]] = r
        except Exception as e:
            print(f"skip {f}: {e}", file=sys.stderr)
    return res


def sync_names(research: dict) -> dict:
    p = S / "names.json"
    names = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    for dev, r in research.items():
        dn = [n.strip() for n in r.get("datalex_names") or [] if n and n.strip()]
        if not dn:
            continue
        cur = names.get(dev, {})
        if cur.get("locked"):
            continue
        tax = r.get("datalex_tax_id") or cur.get("tax_id")
        merged, normed = [], set()
        for nm in dn + cur.get("names", []):
            if datalex.normalize_org(nm) not in normed:
                normed.add(datalex.normalize_org(nm))
                merged.append(nm)
        merged = merged[:3]
        names[dev] = {"names": merged, "tax_id": tax}
    p.write_text(json.dumps(names, ensure_ascii=False, indent=1), encoding="utf-8")
    return names


def is_individual(party: str) -> bool:
    parts = [x.strip() for x in re.split(r"[,;]", party or "") if x.strip()]
    if not parts:
        return False
    return all(not ORG_RE.search(p.upper()) and not re.search(r"\d", p) and 2 <= len(p.split()) <= 4 for p in parts)


def filed_year(c: dict) -> str:
    if c.get("filed"):
        return c["filed"]
    m = re.search(r"/(\d{2})$", c.get("case_number") or "")
    if not m:
        return ""
    c["filed"] = f"20{m.group(1)}" if int(m.group(1)) <= 30 else f"19{m.group(1)}"
    return c["filed"]


def claim_kind(claim: str) -> str:
    c = (claim or "").lower()
    kinds = []
    if re.search(r"սնանկ", c):
        kinds.append("bankruptcy")
    if re.search(r"լուծ|դադարեց", c):
        kinds.append("contract termination")
    if re.search(r"բնակարան|սեփականության իրավունք|հանձն|տիրապետում", c):
        kinds.append("apartment/ownership")
    if re.search(r"վնաս", c):
        kinds.append("damages")
    if re.search(r"անվավեր", c):
        kinds.append("invalidation")
    if re.search(r"բռնագանձ|գումար|պարտք|վճար", c):
        kinds.append("money recovery")
    return ", ".join(kinds) or "other"


DESCRIPTORS = {"ՍՊ", "ՍԿ", "ՓԲ", "ԲԲ", "ԸՆԿԵՐՈՒԹՅՈՒՆ", "ԸՆԿ", "ՍՊԱՌՈՂԱԿԱՆ", "ԿՈՈՊԵՐԱՏԻՎ", "ՍԱՀՄԱՆԱՓԱԿ", "ՊԱՏԱՍԽԱՆԱՏՎՈՒԹՅԱՄԲ",
               "ՓԱԿ", "ԲԱԺՆԵՏԻՐԱԿԱՆ", "ՏՆՕՐԵՆ", "ՇԻՆԱՐԱՐԱԿԱՆ", "ՍՊԸ"}


def strict_match(c: dict, targets: set, tax: str | None) -> bool:
    if tax and tax in (c.get("claim") or ""):
        return True
    side = c["respondent"] if c["role"] == "respondent" else c["claimant"]
    for part in re.split(r"[,;]", side):
        words = datalex.normalize_org(part).split()
        for t in targets:
            tw = t.split()
            if words[:len(tw)] == tw and all(w in DESCRIPTORS for w in words[len(tw):]):
                return True
    return False


def summarize(cases: list, names: list | None = None, tax: str | None = None) -> dict:
    cs = [c for c in cases if "error" not in c]
    targets = {datalex.normalize_org(n) for n in names or []}
    dropped = [c for c in cs if targets and not strict_match(c, targets, tax)]
    cs = [c for c in cs if c not in dropped]
    for c in cs:
        filed_year(c)
    resp = [c for c in cs if c["role"] == "respondent"]
    indiv = [c for c in resp if c["tab"] in ("civil", "payment_order") and is_individual(c["claimant"])]
    bankr = [c for c in resp if c["tab"] == "bankruptcy"]
    crim = [c for c in cs if c["tab"] == "criminal"]
    court = {"total": len(cs), "respondent": len(resp), "claimant": len(cs) - len(resp), "respondent_by_individuals": len(indiv),
             "bankruptcy_as_debtor": len(bankr), "criminal": len(crim),
             "administrative": sum(c["tab"] == "administrative" for c in cs), "payment_order": sum(c["tab"] == "payment_order" for c in cs),
             "since_2021": sum((c.get("filed") or "") >= "2021" for c in cs), "notable": []}
    picked = []
    for c in sorted(bankr, key=lambda x: x.get("filed") or "", reverse=True):
        picked.append((c, f"bankruptcy case against the company (claimant: {c['claimant']})"))
    for c in crim:
        picked.append((c, f"criminal case ({c['role']}); {c['claim'][:120]}"))
    for c in sorted(indiv, key=lambda x: x.get("filed") or "", reverse=True):
        picked.append((c, f"individual {c['claimant']} v. company: {claim_kind(c['claim'])} — {c['claim'][:100]}"))
    for c in sorted([c for c in resp if c not in indiv and c not in bankr and c not in crim], key=lambda x: x.get("filed") or "", reverse=True):
        picked.append((c, f"{c['claimant']} v. company ({c['tab']}): {claim_kind(c['claim'])} — {c['claim'][:100]}"))
    for c in sorted([c for c in cs if c["role"] == "claimant"], key=lambda x: x.get("filed") or "", reverse=True):
        if re.search(r"զրպարտ|վիրավորանք", c["claim"]):
            picked.append((c, f"company sued {c['respondent']} for defamation — {c['claim'][:90]}"))
    for c in sorted([c for c in cs if c["role"] == "claimant"], key=lambda x: x.get("filed") or "", reverse=True):
        picked.append((c, f"company v. {c['respondent']} ({c['tab']}): {claim_kind(c['claim'])} — {c['claim'][:90]}"))
    seen = set()
    for c, why in picked:
        if c["case_number"] in seen:
            continue
        seen.add(c["case_number"])
        court["notable"].append({"case_number": c["case_number"], "tab": c["tab"], "filed": c.get("filed"), "why": why})
        if len(court["notable"]) >= 5:
            break
    kinds = {}
    for c in indiv:
        for k in claim_kind(c["claim"]).split(", "):
            kinds[k] = kinds.get(k, 0) + 1
    other_tax = sorted({t for c in cs for t in re.findall(r"ՀՎՀՀ[^\d]{0,6}(\d{8})", c.get("claim") or "")})
    parties = {}
    for c in cs:
        nm = datalex.normalize_org(c["respondent"] if c["role"] == "respondent" else c["claimant"])
        parties[nm] = parties.get(nm, 0) + 1
    parties["__dropped__"] = sorted({datalex.normalize_org(c["respondent"] if c["role"] == "respondent" else c["claimant"])[:40] for c in dropped})
    parties["__dropped_n__"] = len(dropped)
    return court, kinds, other_tax, sum(1 for c in cases if "error" in c), parties


def main():
    research = load_research()
    names = sync_names(research)
    if "--sync-only" in sys.argv:
        return
    out = []
    for d in DEVS:
        dev = d["developer"]
        r = research.get(dev, {})
        n = names.get(dev)
        rec = {"developer": dev, "role": r.get("role", "unknown"), "legal_entities": r.get("legal_entities", []),
               "founded_year": r.get("founded_year"), "searched_names": n["names"] if n else [],
               "court": None, "news_issues": r.get("news_issues", []), "positives": r.get("positives", []),
               "confidence": r.get("confidence", "low"), "notes": r.get("notes", "")}
        sup = SUP.get(dev, {})
        for fld in ("news_issues", "positives"):
            urls = {x.get("url") for x in rec[fld]}
            rec[fld] += [x for x in sup.get(fld, []) if x.get("url") not in urls]
        if sup.get("notes"):
            rec["notes"] = (rec["notes"] + " " + sup["notes"]).strip()
        for fld in ("role", "confidence", "legal_entities", "founded_year"):
            if fld in sup:
                rec[fld] = sup[fld]
        cf = S / "court" / f"{key(dev, n['names'], n.get('tax_id'))}.json" if n else None
        extra = []
        if cf and cf.exists():
            data = json.loads(cf.read_text(encoding="utf-8"))
            court, kinds, taxes, errs, parties = summarize(data["cases"], data["names"], data.get("tax_id"))
            dropped, ndropped = parties.pop("__dropped__"), parties.pop("__dropped_n__")
            if ndropped:
                extra.append(f"Excluded {ndropped} fuzzy-matched cases of differently named parties (" + "; ".join(dropped[:4]) + ").")
            if len(parties) > 1:
                extra.append("Matched party names: " + "; ".join(f"{k[:60]} ({v})" for k, v in sorted(parties.items(), key=lambda x: -x[1])[:6]) + ".")
            rec["court"] = court
            if kinds:
                extra.append("Individual-claimant respondent case types: " + ", ".join(f"{k} {v}" for k, v in sorted(kinds.items(), key=lambda x: -x[1])) + ".")
            if taxes:
                extra.append("Tax IDs seen in claim texts: " + ", ".join(taxes) + ".")
            if errs:
                extra.append(f"{errs} datalex query errors.")
        else:
            extra.append("Court search pending/not run.")
        extra += [x for x in (S / "court_notes.json").exists() and [json.loads((S / "court_notes.json").read_text(encoding="utf-8")).get(dev)] or [] if x]
        if extra:
            rec["notes"] = (rec["notes"] + " | Court: " + " ".join(extra)).strip(" |")
        out.append(rec)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    done = sum(1 for x in out if x["court"] is not None)
    print(f"wrote {len(out)} records; research {len(research)}; court done {done}")


if __name__ == "__main__":
    main()
