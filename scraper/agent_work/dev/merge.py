"""Merge raw.json records into deduplicated developer groups -> merged.json."""
import json, re
from urllib.parse import urlparse

recs = json.load(open("raw.json"))

AGENT_DOMAINS = {"ar-go.am", "redgroup.am", "sreal.am", "hsbc.am", "dignisi.am", "norakaruyc.info", "facebook.com",
                 "instagram.com", "t.me", "construction.am", "wa.me", "pages.am", "youtube.com", "linkedin.com", "tiktok.com", "karucapatoxic.am", "building.am"}
DOMAIN_EQ = {
    "technotun.com": "pullmanyerevan.com", "technodom.am": "pullmanyerevan.com",
    "vbconstruction.am": "vbc.am", "charagayt.am": "mlmining.am", "ntc.am": "mlmining.am",
    "byuregh.am": "mlmining.am", "skyline-evn.am": "renshin.am", "en.skyline-evn.am": "renshin.am",
    "tsaghkadzorhills.am": "artresidence.am", "firdusresidence.am": "artco.am", "sundayeveryday.am": "upd.am",
    "pallada.am": "newcity.am", "elitarshin.com": "elitarshin.com", "redinvest.am": "redinvest.am",
    "temp.gtbholdings.com": "gtbholdings.com", "anhaght.gtbholdings.com": "gtbholdings.com",
    "cbs-construction.am": "cbs-construction.am", "hye-land.com": "hye-land.com",
    "tmr.am": "tigranmetsresidence.am", "upd.am": "sundayeveryday.am", "hovint.am": "vahakni.com",
    "azbuka.am": "monterosso.am", "libertyone.am": "libertyone.am", "dalantechnologies.am": "dalantechnopark.com",
    "dalantechnologies.com": "dalantechnopark.com", "movenpicktsaghkadzor.am": "4acapital.am",
}
NAME_ALIAS = {
    "artco": "artcompany", "art company": "artcompany", "artcompany": "artcompany", "արտքոմփանի": "artcompany",
    "art residence": "artresidence", "art residence developer company": "artresidence",
    "bedeck construction": "bedeck", "bedeck": "bedeck", "pars": "bedeck", "bedeck masis": "bedeck",
    "new city": "newcity", "new city project": "newcity", "new city projects": "newcity",
    "մետրում ինվեստ": "metrum invest",
    "faith built": "faithbuilt", "faith built construction": "faithbuilt", "ֆեյթ բիլթ": "faithbuilt",
    "элит груп": "elite group", "elit grup": "elite group", "էլիտ գրուպ": "elite group",
    "renshin urban investments": "renshin", "renshin": "renshin", "skyline renshin": "renshin",
    "renshin urban investments": "renshin",
    "arm construct 1": "arm construct", "arm construc t 1": "arm construct",
    "zover estates": "zover", "zover estate": "zover", "magnolia comfort": "zover",
    "zover estates magnolia comfort": "zover",
    "khakhamyan heritage": "amanoo", "amanoo": "amanoo",
    "city nest": "citynest", "city nest property management": "citynest", "onlyone": "citynest",
    "boosab residence": "citynest",
    "arcada construction": "arcada", "ember": "arcada", "urmia": "arcada",
    "метта групп": "metta group", "ооо метта групп": "metta group", "new komitas": "metta group",
    "мецн эрик": "metsn erik", "metsn erik ltd": "metsn erik", "истейт инвестмент энд дивелопмент": "kievian residence", "иджеванатун": "hay develop", "ньюэйдж констракшн": "new age", "нью эйдж констракшн": "new age", "new age": "new age", "novatun": "novatun", "novatun our dream house": "novatun", "ալմա աթա ռեզիդենս": "alma ata residence", "ջավ ա շին": "jav a shin", "zover estates magnolia comfort": "zover", "noy invest group": "noy invest group", "shin stroy house": "shin stroy house", "tigran mets residential complex": "tigran mets group", "armani erebuni": "erebuni armani", "armani erebuni multifunctional complex": "erebuni armani", "retro realty": "metsn erik", "h g m d": "ngmd", "н г м д": "ngmd", "forma": "forma development management", "gyurjyan cascade": "artcompany", "verelq": "verelq 777", "verelk residential district": "verelq 777", "hl construction": "hl construction", "pullman residences yerevan": "technotun", "man group": "man group", "royal building": "royal building", "kasakhum": "movsesyan partners",
    "oriental stones": "orient stone",
    "sunday towers": "up development",
    "prime developments": "prime developers",
    "care building services": "cbs", "care building services cbs": "cbs", "malkհasyants 12": "cbs",
    "մալխասյանց": "cbs",
    "ijevanatun construction company": "hay develop", "hay develop ijevanatun construction company": "hay develop",
    "зао иджеванатун": "hay develop", "ijevanatun construction development": "hay develop",
    "հրաչ և ռուբեն": "national group", "hrach ruben": "national group",
    "ռութ կոնտրակթ": "zoar", "root construct": "zoar", "root contract": "zoar",
    "եռյակ կապիտալ": "yeryak capital",
    "գրանդշին": "grandshin",
    "գազավիկ": "capital park residential complex",
    "felicity նոր նորք": "lav sar", "felicity residential complex": "lav sar", "lav sar": "lav sar",
    "լույսեր": "luyser", "luyser residential complex": "luyser",
    "ռիչ": "rich garden", "rich garden 2": "rich garden",
    "արարէ": "arare",
    "v construction": "v b construction", "piazza grande": "renco", "r g construction": "rg construction", "nor tun": "ml mining", "spitak tnak": "nairi residential public complex", "melkonyan realty": "high park", "brawerk metsn erik construction organization": "brawerk", "brawerk": "brawerk", "noy luxury apartments": "noy luxury apartment",
    "tida 2023": "venni group", "tida 23": "venni group",
    "jacobs shen": "sophene", "sophene club house": "sophene",
    "zeytoun build": "zeytun build", "hb group": "zeytun build", "zeytun build": "zeytun build",
    "horizon invest": "horizon 95", "horizon 95": "horizon 95",
    "midis park": "midis construction",
    "gtg anhaght": "gtb holdings", "gtb development": "gtb holdings",
    "global real estate": "smart city developer", "smart city": "smart city developer",
    "artcompany": "artcompany", "haekshin": "haekshin", "haek construction": "haekshin",
    "haekshin construction anpp construction": "haekshin",
    "monte": "monte", "monte residential complex": "monte",
    "norq": "nork residential complex", "norq residential complex": "nork residential complex",
    "technotun": "technotun", "4a capital": "4a capital",
    "rid": "parajanov", "parajanov club house rid": "parajanov", "parajanov club house": "parajanov",
    "vardanyanshin abovyan hills": "vardanyanshin",
    "riverview dilijan river side": "river side", "riverview dilijan": "river side",
    "movsesyan partners": "movsesyan partners", "kasakhum": "movsesyan partners",
    "caveman residence": "movsesyan partners",
    "tmr tm tower shinas": "tmr", "shinas": "tmr", "tm tower": "tmr",
    "tsaghkadzor park": "metrum invest", "eden park": "metrum invest", "emin 6": "metrum invest",
    "toon 27": "metrum invest", "rubinyants complex": "metrum invest",
    "masis central residential complex": "metrum invest",
    "arshakunyats residence": "capital build", "best land": "capital build",
    "firdus prime residence": "artcompany", "er shin": "artcompany",
    "avan project": "newcity", "gm construction": "newcity", "nobby": "newcity",
    "dakava construction": "ml mining",
    "greenwood residence": "ecoshin group",
    "pallada tsaghkadzor": "newcity",
    "solar city cjsc": "solar city", "solar city սոլար սիթի": "solar city",
    "armat": "armat realty",
    "gm developer": "gm development",
    "1sq argo": "ar go realty", "ar go realty": "ar go realty", "argo realty": "ar go realty",
    "just developer": "just developer",
    "north shine": "north shine",
    "renco armestate": "renco", "renco": "renco",
    "d g a realty": "dga realty",
    "high park yerevan palladio shin": "high park",
    "seray homes seray developments": "seray",
    "green rock management group": "green rock", "green rock": "green rock",
    "shushi palace": "lorida group",
    "orient stone": "orient stone",
    "hyeland construction": "hayland", "hayland": "hayland",
    "comfort build": "shinart group",
    "sil capital construction": "sil capital construction",
    "mövenpick resort tsaghkadzor": "4a capital", "movenpick resort tsaghkadzor": "4a capital",
    "lorida group": "lorida group",
    "estate investment and development": "kievian residence", "kievian residence": "kievian residence",
    "ararat park residential complex": "yeryak capital",
    "rutsog invest": "parajanov", "tmr": "tigran mets group", "shinas": "tigran mets group",
    "tm tower": "tigran mets group", "tmr tm tower shinas": "tigran mets group",
    "ap development": "up development", "hyeland": "hayland", "art group": "sv ga art group",
    "luyser cjsc": "luyser", "elite group cjsc": "elite group", "haekshin cjsc": "haekshin",
    "iv capital": "eve capital", "ratko partner group": "ratco partner group", "shant bnakeli": "shant residential",
    "green property development": "azatutyun multi functional complex", "capital plus": "capital plus",
    "monument hills": "monument hills", "azbuka development ra": "azbuka development ra",
    "target development": "target development",
}
AGENT_EMAILS = {"silver.rea.estate@gmail.com", "info@ar-go.am", "sales@citynest.am", "info@citynest.am", "relocator.armenia@gmail.com", "realtyretro@gmail.com", "dga.realtor@gmail.com", "dga-realty@yandex.ru", "sales.mlmining@gmail.com", "info@mlmining.am", "sales@newcity.am", "info@newcity.am"}
DROP_NAMES = {"a p realty", "yerkir real estate agency", "sold realty", "ava granite", "team systems electrical engineering and low current systems",
              "esco concern", "volta"}


def norm_name(n):
    n = n.lower().replace("&amp;", "&")
    n = re.sub(r'["«»“”\'`()\.,:;]', " ", n)
    n = re.sub(r"\b(llc|cjsc|ojsc|ltd|ooo|ооо|зао|сп)\b|սպը|փբը|ծաղկաձոր ltd", " ", n)
    n = n.replace("&", " ").replace("-", " ").replace("/", " ")
    n = re.sub(r"\s+", " ", n).strip()
    return NAME_ALIAS.get(n, n)


def dom(u):
    if not u:
        return None
    if "//" not in u:
        u = "https://" + u
    d = urlparse(u).netloc.lower().split(":")[0]
    d = re.sub(r"^www\.", "", d)
    d = DOMAIN_EQ.get(d, d)
    if not d or "." not in d or any(d == a or d.endswith("." + a) for a in AGENT_DOMAINS):
        return None
    return d


parent = list(range(len(recs)))


def find(i):
    while parent[i] != i:
        parent[i] = parent[parent[i]]
        i = parent[i]
    return i


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra


keys = {}
for i, r in enumerate(recs):
    r["_n"] = norm_name(r["name"])
    r["_d"] = dom(r["website"])
    if r["name"] == "Elitar Shin" and r["_d"] == "dga-realty.am":
        r["_d"] = None
        r["notes"] = (r["notes"] + "; sales via D.G.A. Realty (dga-realty.am)").strip("; ")
    em = (r.get("email") or "").strip().lower()
    if em in AGENT_EMAILS or "company-name" in em:
        em = ""
    for k in (("n", r["_n"]), ("d", r["_d"]), ("e", em)):
        if k[1]:
            if k in keys:
                union(keys[k], i)
            else:
                keys[k] = i

groups = {}
for i, r in enumerate(recs):
    if r["_n"] in DROP_NAMES:
        continue
    groups.setdefault(find(i), []).append(r)

out = []
for g in groups.values():
    names = [r["name"] for r in g]
    # prefer a Latin brand name from curated sources
    def score(r):
        s = 0
        if re.search(r"[A-Za-z]", r["name"]): s += 10
        if r["source"] in ("construction.am/developers", "pages.am/real-estate-developers", "websearch", "karucapatoxic.am"): s += 5
        if re.search(r"\b(LLC|CJSC|LTD|ООО)\b", r["name"]): s -= 3
        if "developer name not given" in (r["notes"] or ""): s -= 8
        return s
    best = max(g, key=score)
    doms = [r["_d"] for r in g if r["_d"]]
    webs = {}
    for r in g:
        if r["_d"]:
            webs.setdefault(r["_d"], r["website"])
    dom_pick = max(set(doms), key=doms.count) if doms else None
    projects, seen = [], set()
    for r in g:
        for p in r["projects"]:
            k = p.lower().strip()
            if k not in seen:
                seen.add(k); projects.append(p.strip())
    emails = [r["email"] for r in g if r.get("email") and "company-name" not in r["email"]]
    phones = []
    for r in g:
        for p in r["phones"]:
            d = re.sub(r"\D", "", p)
            if d and d not in [re.sub(r"\D", "", x) for x in phones]:
                phones.append(p)
    notes = sorted({r["notes"] for r in g if r["notes"]})
    aliases = sorted({n for n in names if n != best["name"]})
    other_sites = sorted({w for d, w in webs.items() if d != dom_pick})
    proj_sites = sorted({s for r in g for s in r.get("project_sites", [])})
    out.append(dict(
        name=best["name"], website=webs.get(dom_pick), projects_url=None,
        facebook=next((r["facebook"] for r in g if r.get("facebook")), None),
        instagram=next((r["instagram"] for r in g if r.get("instagram")), None),
        phones=phones[:6], email=emails[0] if emails else "",
        found_via=sorted({r["source"] for r in g}), known_projects=projects,
        _aliases=aliases, _other_sites=other_sites, _project_sites=proj_sites, _notes=notes))
json.dump(out, open("merged.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "with website:", sum(1 for o in out if o["website"]))
for o in sorted(out, key=lambda o: o["name"].lower()):
    print(f'{o["name"][:40]:40} {str(o["website"])[:45]:45} {len(o["found_via"])} {o["_aliases"][:4]} {o["_other_sites"][:3]}')
