"""Ownership connections between developers and constructors.

Crawls the public registry mirror (karg.am → e-register.moj.am and its beneficial-owner register)
for every developer in the dataset, follows each founder to the other companies that person holds,
and looks up bankruptcy cases on datalex.am. The result is a graph — developers, their legal
entities and the people behind them — written to ``web/data/connections.json`` for the analytics
page. Every node and edge carries the links it was built from.

Usage:
    python3 connections.py crawl [--limit N] [--workers 4] [--skip-datalex]
    python3 connections.py build
    python3 connections.py status

Files:
    scraper/connections_raw.json      crawl output (registry cards, people, court cases)
    scraper/connections_manual.json   hand-checked corrections: confirmed bankruptcies, bad matches
    web/data/connections.json         the graph the site loads
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import karg
from datalex import case_url, find_cases, normalize_org

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROJECTS = ROOT / "web" / "data" / "projects.json"
RAW = HERE / "connections_raw.json"
MANUAL = HERE / "connections_manual.json"
OUT = ROOT / "web" / "data" / "connections.json"

BUILD_NACE = re.compile(r"F4[123]|շինարար|Շինարար|ՇԻՆԱՐԱՐ|անշարժ գույք|ԱՆՇԱՐԺ ԳՈՒՅՔ|նախագծ", re.I)
NOISE_ADDRESS = re.compile(r"^\s*(ԵՐԵՎԱՆ|YEREVAN)?\s*$")


# ---------------------------------------------------------------- names
def norm(name: str | None) -> str:
    """Company-name key: no quotes, legal form, punctuation or case (Armenian, Latin, Cyrillic)."""
    return normalize_org(re.sub(r"\([^)]*\)", " ", name or ""))


ADDR_NOISE = re.compile(r"\b(ԹԱՂԱՄԱՍ|ՓՈՂՈՑ|ՊՈՂՈՏԱ|ՓՈՂ|ՊՈՂ|ՓՈՂՈՑԻ|ՇԵՆՔ|ՏԱՐԱԾՔ|ԳՐԱՍԵՆՅԱԿ|ԲՆԱԿԱՐԱՆ|ԲՆ|Փ|Պ|ՓՄ|ՆՐԲ|ՆՐԲԱՆՑՔ|ԽՃ|ՇԱՐՔ)\b\.?")
ADDR_ABBR = {"Վ": "ՎԵՐԻՆ", "Ն": "ՆԵՐՔԻՆ", "Գ": "ԳԼԽԱՎՈՐ"}


def norm_address(a: str | None) -> str:
    """Legal-address key: upper case, abbreviations expanded, street-type words and flat numbers dropped."""
    a = re.sub(r"[^\w\s./-]+", " ", (a or "").upper())
    a = re.sub(r"\b([ՎՆԳ])\s*\.\s*(?=[Ա-Ֆ])", lambda m: ADDR_ABBR[m.group(1)] + " ", a)
    a = ADDR_NOISE.sub(" ", a)
    a = re.sub(r"\s+", " ", a).strip()
    return a


def display_name(name: str | None) -> str:
    """People come from the register in mixed case — show ԳՐԻԳՈՐ ՏԻԳՐԱՆՅԱՆ as Գրիգոր Տիգրանյան."""
    n = (name or "").strip()
    return " ".join(w.capitalize() if w.isupper() else w for w in n.split()) if n.isupper() else n


def is_person(name: str | None) -> bool:
    """A founder row is a person when it is not an obvious company name."""
    n = (name or "").strip()
    return bool(n) and not re.search(r"ՍՊԸ|ՓԲԸ|ԲԲԸ|LLC|CJSC|OJSC|ООО|ЗАО", n, re.I)


def azdarar_url(name: str) -> str:
    """Official bulletin search (azdarar.am publishes bankruptcy and liquidation notices)."""
    return f"https://www.azdarar.am/announcments/search?keyword={urllib.parse.quote(name)}"


def datalex_search_url() -> str:
    return "https://datalex.am/?app=AppCaseSearch"


def eregister_url(tax_id: str) -> str:
    return f"https://e-register.moj.am/hy/search/companies?q={urllib.parse.quote(tax_id)}"


# ---------------------------------------------------------------- dataset side
def developers() -> list[dict]:
    """Developer groups from the built dataset, with their researched legal entities."""
    projects = json.loads(PROJECTS.read_text(encoding="utf-8"))["projects"]
    groups: dict[str, dict] = {}
    for p in projects:
        g = p.get("developer_group") or p.get("developer")
        if not g or g.strip().lower() in {"unknown developer", "unknown"}:
            continue
        d = groups.setdefault(g, {"group": g, "slug": p.get("developer_slug"), "projects": 0, "names": set(),
                                  "entities": [], "grade": None, "score": None, "role": None, "project_ids": []})
        d["projects"] += 1
        d["project_ids"].append(p["id"])
        for key in ("developer", "developer_am"):
            if p.get(key):
                d["names"].add(p[key])
        rep = p.get("developer_rep") or {}
        if rep.get("grade") and not d["grade"]:
            d["grade"], d["score"] = rep["grade"], rep.get("score")
        r = rep.get("research") or {}
        if r and not d["entities"]:
            d["role"] = r.get("role")
            d["names"].update(n for n in r.get("searched_names") or [] if n)
            d["entities"] = [e for e in r.get("legal_entities") or [] if e.get("name_hy") or e.get("name_en")]
            d["court"] = r.get("court") or {}
    for d in groups.values():
        d["names"] = sorted(d["names"])
        d["project_ids"] = d["project_ids"][:50]
    return sorted(groups.values(), key=lambda d: -d["projects"])


# ---------------------------------------------------------------- resolving
def pick(hits: list[dict], want: str) -> dict | None:
    """Best registry hit for a name: exact name match, construction activity and active status first."""
    exact = [h for h in hits if norm(h["name"]) == want]
    if not exact:
        return None
    exact.sort(key=lambda h: (BUILD_NACE.search(h.get("nace") or "") is None, h.get("status") != "active"))
    best = dict(exact[0])
    best["ambiguous"] = [h["tax_id"] for h in exact[1:]]
    return best


def resolve_entity(entity: dict) -> dict:
    """Registry company for one researched legal entity: by tax id when known, else by exact name."""
    out = {"name_hy": entity.get("name_hy"), "name_en": entity.get("name_en"), "tax_id": entity.get("tax_id"),
           "evidence_url": entity.get("source_url"), "match": None}
    if entity.get("tax_id"):
        out["match"] = "tax_id"
        return out
    for name in (entity.get("name_hy"), entity.get("name_en")):
        want = norm(name)
        if len(want) < 4:
            continue
        query = re.sub(r"[«»\"]", " ", re.sub(r"\([^)]*\)", " ", name)).strip()
        hit = pick(karg.search(query), want)
        if hit:
            out.update({"tax_id": hit["tax_id"], "match": "name", "matched_name": hit["name"],
                        "query": query, "ambiguous": hit.get("ambiguous") or []})
            return out
        out["query"] = query
    out["search_url"] = karg.search_url(out.get("query") or (entity.get("name_hy") or ""))
    return out


# ---------------------------------------------------------------- crawl
def crawl(limit: int | None, workers: int, skip_datalex: bool, deep: bool = False) -> dict:
    devs = developers()
    if limit:
        devs = devs[:limit]
    print(f"resolving legal entities of {len(devs)} developers…", file=sys.stderr)
    with ThreadPoolExecutor(workers) as ex:
        for d in devs:
            d["resolved"] = list(ex.map(resolve_entity, d["entities"]))

    tax_ids = sorted({r["tax_id"] for d in devs for r in d["resolved"] if r.get("tax_id")})
    print(f"fetching {len(tax_ids)} company cards…", file=sys.stderr)
    with ThreadPoolExecutor(workers) as ex:
        cards = list(ex.map(karg.company, tax_ids))
    companies = {c["tax_id"]: c for c in cards if c}

    keys = sorted({f["key"] for c in companies.values() for f in c["founders"]})
    print(f"fetching {len(keys)} founder pages…", file=sys.stderr)
    with ThreadPoolExecutor(workers) as ex:
        pages = list(ex.map(karg.founder, keys))
    people = {p["key"]: p for p in pages if p}

    # Second hop: the other companies those people hold. Their registry row on the owner page already
    # carries name, status, address and registration date, so a full card is only fetched with --deep.
    more = sorted({c["tax_id"] for p in people.values() for c in p["companies"]} - set(companies))
    if deep:
        print(f"fetching {len(more)} companies of the same owners…", file=sys.stderr)
        with ThreadPoolExecutor(workers) as ex:
            for c in ex.map(karg.company, more):
                if c:
                    companies[c["tax_id"]] = c
    else:
        print(f"{len(more)} companies of the same owners taken from the owner pages", file=sys.stderr)
        for p in people.values():
            for c in p["companies"]:
                if c["tax_id"] not in companies:
                    companies[c["tax_id"]] = {
                        "tax_id": c["tax_id"], "name": c["name"], "status": c.get("status"),
                        "address": c.get("address"), "registered": c.get("registered"),
                        "founders": [], "url": c["url"], "partial": True, "source": karg.SOURCE_NOTE,
                    }

    bankruptcy = {}
    if not skip_datalex:
        targets = {}
        for d in devs:
            for r in d["resolved"]:
                c = companies.get(r.get("tax_id") or "")
                names = {n for n in (r.get("name_hy"), r.get("matched_name"), c and c.get("name")) if n}
                if names:
                    targets[r.get("tax_id") or norm(r.get("name_hy"))] = sorted(names)
        print(f"datalex bankruptcy search for {len(targets)} companies…", file=sys.stderr)

        def cases(item):
            key, names = item
            try:
                return key, [c for c in find_cases(names, tabs=["bankruptcy"], max_pages=2) if "error" not in c]
            except Exception as e:  # noqa: BLE001
                print(f"datalex {key}: {e}", file=sys.stderr)
                return key, []

        with ThreadPoolExecutor(min(workers, 3)) as ex:
            for key, rows in ex.map(cases, targets.items()):
                bankruptcy[key] = rows

    raw = {"generated": date.today().isoformat(), "developers": devs, "companies": companies,
           "people": people, "bankruptcy": bankruptcy}
    RAW.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    print(f"{RAW.name}: {len(devs)} developers, {len(companies)} companies, {len(people)} people, "
          f"{sum(len(v) for v in bankruptcy.values())} bankruptcy cases", file=sys.stderr)
    return raw


def bankruptcy_pass(workers: int, limit: int | None = None) -> None:
    """Search datalex for bankruptcy cases of every company in the crawl that has not been searched yet.

    The crawl itself only searches the developers' own entities; this extends the same search to the other
    companies their owners hold, so a bankrupt sister company is flagged too.
    """
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    known = raw.setdefault("bankruptcy", {})
    todo = [(tax, [c["name"]]) for tax, c in raw["companies"].items() if tax not in known and c.get("name")]
    todo = todo[:limit] if limit else todo
    print(f"datalex bankruptcy search for {len(todo)} more companies…", file=sys.stderr)

    def search(item):
        key, names = item
        try:
            return key, [c for c in find_cases(names, tabs=["bankruptcy"], max_pages=2) if "error" not in c]
        except Exception as e:  # noqa: BLE001
            print(f"datalex {key}: {e}", file=sys.stderr)
            return key, None

    done = 0
    with ThreadPoolExecutor(min(workers, 3)) as ex:
        for key, rows in ex.map(search, todo):
            if rows is not None:
                known[key] = rows
                done += 1
    RAW.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    print(f"{done} companies searched, {sum(1 for v in known.values() if v)} with bankruptcy cases", file=sys.stderr)


# ---------------------------------------------------------------- bankruptcy
def bankruptcy_status(company: dict, cases: list[dict], manual: dict) -> dict | None:
    """
    Classify a company's bankruptcy exposure from its datalex cases and registry status.

    self_declared  the company itself filed for bankruptcy (it is the claimant against itself)
    declared       a bankruptcy case against it and the company is no longer active in the register,
                   or a hand-checked confirmation in connections_manual.json
    case           a bankruptcy case is pending against it
    creditor cases (the company suing someone else's estate) are kept but never flagged.
    """
    me = {norm(company.get("name")), *(norm(n) for n in company.get("aliases") or [])} - {""}
    own, against, creditor = [], [], []
    for c in cases:
        clm, res = norm(c.get("claimant")), norm(c.get("respondent"))
        row = {"case_number": c.get("case_number"), "claimant": c.get("claimant"), "respondent": c.get("respondent"),
               "filed": c.get("filed") or None, "url": case_url(c.get("case_id"))}
        if res in me and clm in me:
            own.append(row)
        elif res in me:
            against.append(row)
        elif clm in me:
            creditor.append(row)
    fix = manual.get(company.get("tax_id") or "") or {}
    status = None
    if own:
        status = "self_declared"
    elif against:
        status = "declared" if company.get("status") == "inactive" else "case"
    if fix.get("status"):
        status = fix["status"]
    if not status:
        return None
    basis = {
        "self_declared": "the company is the claimant in a bankruptcy case against itself",
        "declared": "a bankruptcy case against the company, and the register no longer shows it as active",
        "case": "a bankruptcy case against the company is pending; the register still shows it as active",
    }[status]
    if fix.get("source_url"):
        basis = fix.get("note") or "confirmed by hand against the source linked below"
    return {
        "status": status,
        "basis": basis,
        "cases": (own + against)[:8],
        "creditor_cases": creditor[:5],
        "confirmed_by": fix.get("source_url"),
        "note": fix.get("note"),
        "sources": [
            {"title": "datalex.am — bankruptcy cases", "url": datalex_search_url()},
            {"title": "azdarar.am — official bulletin", "url": azdarar_url(company.get("name") or "")},
        ],
    }


# ---------------------------------------------------------------- graph
def build() -> dict:
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    manual = json.loads(MANUAL.read_text(encoding="utf-8")) if MANUAL.exists() else {}
    companies, people = raw["companies"], raw["people"]
    fixes = manual.get("companies") or {}
    dropped = set(manual.get("drop_companies") or [])

    # every name a company was searched under, so a court record filed under the brand name still matches
    aliases: dict[str, set[str]] = defaultdict(set)
    for d in raw["developers"]:
        for r in d["resolved"]:
            if r.get("tax_id"):
                aliases[r["tax_id"]].update(n for n in (r.get("name_hy"), r.get("matched_name")) if n)

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    seen_edges = set()

    def edge(src: str, dst: str, kind: str, **rest) -> None:
        key = (src, dst, kind, rest.get("label"))
        if src == dst or key in seen_edges or src not in nodes or dst not in nodes:
            return
        seen_edges.add(key)
        edges.append({"source": src, "target": dst, "kind": kind, **rest})

    # developers -------------------------------------------------------
    dev_of_company: dict[str, set[str]] = defaultdict(set)
    for d in raw["developers"]:
        did = f"dev:{d['slug'] or norm(d['group'])}"
        nodes[did] = {"id": did, "type": "developer", "label": d["group"], "projects": d["projects"],
                      "grade": d.get("grade"), "score": d.get("score"), "role": d.get("role"),
                      "slug": d.get("slug"), "project_ids": d.get("project_ids") or [],
                      "lawsuits": (d.get("court") or {}).get("respondent_by_individuals"),
                      "sources": [{"title": "Projects on the map", "url": f"index.html#dev={urllib.parse.quote(d['group'])}"}]}
        for r in d["resolved"]:
            tax = r.get("tax_id")
            if not tax or tax in dropped or tax not in companies:
                continue
            dev_of_company[tax].add(did)

    # companies --------------------------------------------------------
    for tax, c in companies.items():
        if tax in dropped:
            continue
        # only registry fields may be overridden by hand; "status" in a fix means the bankruptcy status,
        # not the register's, and must not overwrite it
        fix = {k: v for k, v in (fixes.get(tax) or {}).items() if k in {"name", "address", "director", "nace", "form"}}
        c = {**c, **fix, "aliases": sorted(aliases.get(tax, ()))}
        cid = f"co:{tax}"
        cases = raw["bankruptcy"].get(tax) or []
        bank = bankruptcy_status(c, cases, fixes)
        nodes[cid] = {
            "id": cid, "type": "company", "label": c.get("name") or tax, "tax_id": tax,
            "status": c.get("status"), "form": c.get("form"), "registered": c.get("registered"),
            "address": c.get("address"), "nace": c.get("nace"), "director": c.get("director"),
            "court_cases": c.get("court_cases"), "bankruptcy": bank, "partial": bool(c.get("partial")) or None,
            "developers": sorted(dev_of_company.get(tax, ())),
            "sources": [
                {"title": "Registry card (karg.am / e-register)", "url": c.get("url")},
                {"title": "e-register.moj.am company search", "url": eregister_url(tax)},
                {"title": "azdarar.am bulletin search", "url": azdarar_url(c.get("name") or tax)},
            ],
        }

    for tax, devs in dev_of_company.items():
        for did in devs:
            e = next((r for d in raw["developers"] for r in d["resolved"]
                      if r.get("tax_id") == tax and f"dev:{d['slug'] or norm(d['group'])}" == did), {})
            edge(did, f"co:{tax}", "entity", label="legal entity",
                 evidence=e.get("evidence_url"), match=e.get("match"))

    # people -----------------------------------------------------------
    for key, p in people.items():
        if not is_person(p.get("name")):
            continue
        mine = [c for c in p["companies"] if f"co:{c['tax_id']}" in nodes]
        pid = f"pe:{key}"
        nodes[pid] = {"id": pid, "type": "person", "label": display_name(p["name"]), "companies": len(p["companies"]),
                      "sources": [{"title": "Owner card (karg.am / BOR)", "url": p["url"]}]}
        for c in p["companies"]:
            if f"co:{c['tax_id']}" in nodes:
                edge(pid, f"co:{c['tax_id']}", c.get("role") or "founder",
                     label=f"{c.get('share')}%" if c.get("share") else (c.get("role") or "founder"))
        if not mine:
            nodes.pop(pid)

    # directors named on a card but not in the owner register ------------
    by_person_name = {norm(n["label"]): n["id"] for n in nodes.values() if n["type"] == "person"}
    for cid, n in list(nodes.items()):
        if n["type"] != "company" or not n.get("director"):
            continue
        name = re.split(r",", n["director"])[0].strip()
        pid = by_person_name.get(norm(name))
        if pid:
            edge(pid, cid, "director", label="director")

    # shared legal address ------------------------------------------------
    by_address: dict[str, list[str]] = defaultdict(list)
    for n in nodes.values():
        if n["type"] == "company" and n.get("address") and not NOISE_ADDRESS.match(n["address"]):
            by_address[norm_address(n["address"])].append(n["id"])
    for addr, ids in by_address.items():
        if 1 < len(ids) <= 8:  # a shared office block is a hint; a mass-registration address is noise
            for i, a in enumerate(ids):
                for b in ids[i + 1:]:
                    edge(a, b, "address", label="same legal address", detail=addr)

    # keep only what connects something ----------------------------------
    degree = Counter()
    for e in edges:
        degree[e["source"]] += 1
        degree[e["target"]] += 1
    for nid, n in list(nodes.items()):
        if n["type"] != "developer" and not degree[nid]:
            nodes.pop(nid)
    edges = [e for e in edges if e["source"] in nodes and e["target"] in nodes]

    # components, so the page can show only clusters that link two developers
    parent = {nid: nid for nid in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        a, b = find(e["source"]), find(e["target"])
        if a != b:
            parent[a] = b
    comp_of = {nid: find(nid) for nid in nodes}
    comp_devs = Counter(comp_of[nid] for nid, n in nodes.items() if n["type"] == "developer")
    comp_id = {c: i for i, c in enumerate(sorted({comp_of[n] for n in nodes}))}
    for nid, n in nodes.items():
        n["component"] = comp_id[comp_of[nid]]
        n["component_developers"] = comp_devs[comp_of[nid]]

    flagged = [n for n in nodes.values() if n["type"] == "company" and n.get("bankruptcy")]
    meta = {
        "generated": date.today().isoformat(),
        "crawled": raw.get("generated"),
        "developers": sum(n["type"] == "developer" for n in nodes.values()),
        "companies": sum(n["type"] == "company" for n in nodes.values()),
        "people": sum(n["type"] == "person" for n in nodes.values()),
        "edges": len(edges),
        "linked_clusters": sum(1 for c, n in comp_devs.items() if n > 1),
        "bankruptcies": Counter(n["bankruptcy"]["status"] for n in flagged),
        "sources": [
            {"title": "e-register.moj.am — state register of legal entities", "url": "https://e-register.moj.am/hy/search/companies"},
            {"title": "karg.am — registry and beneficial-owner mirror", "url": "https://karg.am/"},
            {"title": "datalex.am — judicial information system", "url": datalex_search_url()},
            {"title": "azdarar.am — official bulletin (bankruptcy notices)", "url": "https://www.azdarar.am/"},
        ],
    }
    OUT.write_text(json.dumps({"meta": meta, "nodes": list(nodes.values()), "edges": edges}, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=1), file=sys.stderr)
    return meta


def status() -> None:
    if not RAW.exists():
        print("no crawl yet — run: python3 connections.py crawl", file=sys.stderr)
        return
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    resolved = [r for d in raw["developers"] for r in d["resolved"]]
    print(json.dumps({
        "crawled": raw["generated"],
        "developers": len(raw["developers"]),
        "entities": len(resolved),
        "resolved": Counter(r.get("match") or "unresolved" for r in resolved),
        "companies": len(raw["companies"]),
        "people": len(raw["people"]),
        "companies_with_bankruptcy_cases": len(raw["bankruptcy"]),
    }, ensure_ascii=False, indent=1))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("crawl")
    c.add_argument("--limit", type=int)
    c.add_argument("--workers", type=int, default=4)
    c.add_argument("--skip-datalex", action="store_true")
    c.add_argument("--deep", action="store_true", help="also fetch full cards for the owners' other companies")
    b = sub.add_parser("bankruptcy", help="datalex bankruptcy search for companies the crawl did not cover")
    b.add_argument("--workers", type=int, default=3)
    b.add_argument("--limit", type=int)
    sub.add_parser("build")
    sub.add_parser("status")
    a = ap.parse_args()
    if a.cmd == "crawl":
        crawl(a.limit, a.workers, a.skip_datalex, a.deep)
        build()
    elif a.cmd == "bankruptcy":
        bankruptcy_pass(a.workers, a.limit)
        build()
    elif a.cmd == "build":
        build()
    else:
        status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
