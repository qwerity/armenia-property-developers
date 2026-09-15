"""Combine merged developer groups with crawl results into developers_master.json."""
import json, re
from urllib.parse import urlparse, urlunparse

OUT = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developers_master.json"
data = json.load(open("merged.json"))
crawl = json.load(open("enrich_results.json"))
from enrich import analyze, FREEMAIL, AGENT
for o in data:
    cand = ([o["website"]] if o["website"] else [])
    if o.get("email") and "@" in o["email"]:
        dm = o["email"].split("@")[-1].lower().strip()
        if dm not in FREEMAIL and dm not in AGENT:
            cand.append("https://" + dm)
    cand += [s for s in o.get("_other_sites", []) if s not in cand]
    o["_cands"] = cand
    for c in cand:
        if c not in crawl:
            crawl[c] = analyze(c if "//" in c else "https://" + c)
            print("crawled new", c, crawl[c]["status"])
json.dump(crawl, open("enrich_results.json", "w"), ensure_ascii=False, indent=1)

PROJECTS_OVERRIDE = {
    "mlmining.am": ("https://mlmining.am/construction", "JS-light page listing construction projects"),
    "metruminvest.am": ("https://metruminvest.am/en/projects", "JS-rendered (needs headless browser)"),
    "haekshin.am": ("https://haekshin.am/hy/projects", "JS-rendered (needs headless browser)"),
    "retroshin.am": ("https://www.retroshin.am/hy/buildings", "JS-rendered (needs headless browser)"),
    "mikshin.am": ("https://www.mikshin.am/projects", "JS-rendered (needs headless browser)"),
    "muargroup.am": ("https://muargroup.am/", "JS-rendered; project pages /projects/<id> linked from homepage"),
    "elitprojectgroup.am": ("https://elitprojectgroup.am/apartaments", "JS-rendered; also /townhouses and /finished-works"),
    "milonmining.am": ("https://www.milonmining.am/apartments", "JS-rendered; also /townhouses"),
    "smart-city.am": ("https://smart-city.am/CommunitySelection", "JS-rendered; communities at /Community?communityId=N"),
    "rgconstruction.am": ("https://rgconstruction.am/hy/works/all", "JS-rendered (needs headless browser)"),
    "redinvest.am": ("https://www.redinvest.am/en/developers", "sales agent catalog of developer projects; JSON API https://redgroup.am/api/projects?page=N"),
    "sagashin.am": ("https://www.sagashin.am/#projects", "JS-rendered single page; projects section"),
    "fastpro.am": ("https://fastpro.am/", "JS-rendered single page; projects section"),
    "citynest.am": ("https://citynest.am/en", "sales/management company; project subpages e.g. /cityview/am, /nest/am, /allur/am, /milanofirenze/am, /tmtower/am"),
    "gtbholdings.com": ("https://gtbholdings.com/companies/", "group companies = projects (GTB Cascade, Anhaght, Proshyan, Tower)"),
    "vahakni.com": ("https://www.vahakni.com/en", "houses/townhouses/apartments linked from homepage"),
    "defansehousing.com": ("https://defansehousing.com/en", "district blocks at /en/district/<block>"),
    "1-sq.am": ("https://1-sq.am/current-projects/", "also /finished-projects/"),
    "mge.am": ("https://mge.am/projects.php?lang=hy", ""),
    "newkomitas.am": ("https://newkomitas.am/", "project pages /projects/<uuid> linked from homepage"),
    "townhouse.am": ("https://townhouse.am/townhouses.html", "also /houses.html"),
    "spitaktnak.am": ("https://spitaktnak.am/works", "contractor portfolio"),
    "amanoo.am": ("https://www.amanoo.am/", "sub-projects /ivy/ and /sarin/ linked from homepage"),
    "zover.am": ("https://www.zover.am/#projects", "single-page site"),
    "seraydevelopments.com": ("https://seraydevelopments.com/construction-projects-in-yerevan-armenia/", "multi-country developer; Armenia page"),
    "artresidence.am": ("https://artresidence.am/hy", "Next.js site; buildings at /hy/buildings/<name>, /hy/projects/Tsaghkadzor"),
    "primedevelopers.am": ("https://primedevelopers.am/en", "project pages /en/project/<NAME>"),
    "elitegroup.am": ("http://elitegroup.am/en/menu/1/", "project pages /en/projects/<id> linked from menu pages"),
    "novavan.am": ("https://novavan.am/", "single-project site"),
    "clubhouseyerevan.am": ("https://www.clubhouseyerevan.am/", "single-project site (also shown on artresidence.am/hy/buildings/club-house)"),
    "sahakyanshin.com": ("https://www.sahakyanshin.com/", "project pages linked from homepage"),
    "pullmanyerevan.com": ("https://www.pullmanyerevan.com/residences", "single-project site"),
    "kamertoon.am": ("https://kamertoon.am/premises/type/apartments/", "single-project site"),
    "renco.it": ("https://www.renco.it/projects", "global portfolio; Armenian projects: Piazza Grande, Milano & Firenze Towers"),
    "shushi-palace.am": ("https://www.shushi-palace.am/apartments", "single-project site (JS)"),
    "promgroup.am": ("https://promgroup.am/en/projects/", "contractor portfolio of residential complexes"),
    "tesaranresidence.am": ("https://tesaranresidence.am/en#projects", "single-page site"),
    "sundayeveryday.am": ("https://sundaytowers.am/", "Sunday Towers project site (also sundayeveryday.am/projects/)"),
    "tigranmetsresidence.am": ("https://tigranmetsresidence.am/", "single-project site; TM Tower sold via citynest.am/tmtower/am"),
    "adatech.am": (None, None),
}
NAME_OVERRIDE = {"smart-city.am": "Smart City Developer (Global Real Estate)", "tigranmetsresidence.am": "Tigran Mets Group (TMR / Shinas)", "parajanov.am": "Parajanov Club House (RID LLC / Rutsog Invest)", "allur.am": "Allur Dilijan (Shamakhyan LLC)", "felicity.am": "Lav-Sar (FeliCity)", "sophene.am": "Jacobs Shen (Sophene)", "luyser.am": "Luyser", "brawerk.am": "Brawerk", "monterosso.am": "Azbuka Development RA (Monterosso)", "komitaspark.am": "Ord Development (Komitas Park)", "shushi-palace.am": "Lorida Group (Shushi Palace)", "pullmanyerevan.com": "TechnoTun (Pullman Residences)", "abovyanhills.am": "Vardanyanshin (Abovyan Hills)", "libertyone.am": "Capital Plus (Liberty One)", "azatutyuncomplex.am": "Green Property Development (Azatutyan Complex)", "newkomitas.am": "Metta Group (New Komitas)"}
SITE_OVERRIDE = {"smart-city.am": "https://smart-city.am/", "elitegroup.am": "http://elitegroup.am/", "parajanov.am": "https://parajanov.am/", "defansehousing.com": "https://defansehousing.com/", "metruminvest.am": "https://metruminvest.am/", "tigranmetsresidence.am": "https://tigranmetsresidence.am/", "4acapital.am": "https://4acapital.am/"}
EXTRA_NOTES = {
    "4acapital.am": "Projects also marketed via City Nest (citynest.am): City View, Nest Residence, Movenpick, Aivazovsky.",
    "citynest.am": "Sales/property-management company marketing projects of 4A Capital, Renco (Milano & Firenze), Tigran Mets Group (TM Tower), Mountain Village, Allur Dilijan and others.",
    "redinvest.am": "RED Invest Group: exclusive sales agent (not builder) for ~47 projects of many developers.",
    "clubhouseyerevan.am": "Clubhouse at G. Hovsepyan 22/11; etagi attributes it to Faith Built, karucapatoxic email is faithbuilt.am.",
}


REDIRECT_OK = {"hbgroup.am", "zeytunbuild.am", "tmr.am", "tigranmetsresidence.am", "dalantechnopark.com", "dalantechnologies.com", "dalantechnologies.am", "liashin.am", "liashin.com", "novel.am", "norq.am", "smart-city.am", "hovint.am", "vahakni.com", "upd.am", "sundayeveryday.am"}


def host(u):
    return re.sub(r"^www\.", "", urlparse(u).netloc.lower()) if u else None


def clean_social(u):
    if not u:
        return None
    u = u.replace("http://https://", "https://").strip()
    p = urlparse(u)
    if not p.netloc:
        return None
    path = p.path.rstrip("#")
    q = p.query if "profile.php" in path else ""
    q = "&".join(x for x in q.split("&") if x.startswith("id="))
    return urlunparse((p.scheme or "https", p.netloc, path, "", q, ""))


def clean_site(u):
    p = urlparse(u)
    return urlunparse((p.scheme, p.netloc, p.path, "", "", ""))


def norm_phone(p):
    d = re.sub(r"\D", "", p)
    if d.startswith("00"):
        d = d[2:]
    if len(d) == 8:
        d = "374" + d
    if len(d) == 9 and d.startswith("0"):
        d = "374" + d[1:]
    return "+" + d if len(d) >= 11 else None


out = []
for o in data:
    notes = list(o["_notes"])
    website, pu, pnote = None, None, None
    live = None
    dead = []
    for c in o.get("_cands", []):
        r = crawl.get(c)
        if r and r["status"].startswith("2") and (r.get("n_links", 0) > 0 or r.get("title")):
            ch, fh = host(c if "//" in c else "https://" + c), host(r["final_url"])
            if fh and ch and fh != ch and fh not in REDIRECT_OK and ch not in REDIRECT_OK:
                notes.append(f"{c} redirects to {r['final_url']} (other company site; not used)")
                continue
            live = (c, r)
            break
        dead.append(c)
    if live:
        c, r = live
        website = clean_site(r["final_url"]) if host(r["final_url"]) == host(c if "//" in c else "https://" + c) else clean_site(c if "//" in c else "https://" + c)
        h = host(r["final_url"]) or host(c)
        website = SITE_OVERRIDE.get(h, website)
        if h in PROJECTS_OVERRIDE:
            pu, pnote = PROJECTS_OVERRIDE[h]
        if not pu:
            pu = r.get("projects_url")
            pnote = r.get("projects_note")
        if not pu and h != "adatech.am":
            pu = website
            pnote = "no dedicated projects page found; scrape homepage (single-project/landing or JS-rendered site)"
        if c != o["website"] and o["website"]:
            notes.append(f"listed website {o['website']} is offline; using {website} (from email domain)")
        elif c != o["website"]:
            notes.append("website taken from contact email domain / alternate listed site")
        o["facebook"] = o["facebook"] or r.get("facebook")
        o["instagram"] = o["instagram"] or r.get("instagram")
        if not o["email"] and r.get("emails"):
            o["email"] = r["emails"][0]
        o["phones"] = o["phones"] + r.get("phones", [])
        if h in EXTRA_NOTES:
            notes.append(EXTRA_NOTES[h])
    if dead and not live:
        notes.append("listed website offline/unreachable: " + ", ".join(sorted(set(dead))))
    elif dead and live and o["website"] in dead and not any("offline" in n for n in notes):
        notes.append("listed website offline: " + o["website"])
    if pnote:
        notes.append("projects_url: " + pnote)
    if o["_aliases"]:
        notes.append("also listed as: " + "; ".join(o["_aliases"][:12]))
    if o["_other_sites"]:
        notes.append("other sites: " + ", ".join(o["_other_sites"][:6]))
    if o["_project_sites"]:
        notes.append("project sites: " + ", ".join(clean_site(s) for s in o["_project_sites"][:8]))
    phones, seen = [], set()
    for p in o["phones"]:
        n = norm_phone(p)
        if n and n not in seen:
            seen.add(n); phones.append(n)
    email = (o["email"] or "").strip().lower()
    if "company-name" in email:
        email = ""
    out.append({
        "name": NAME_OVERRIDE.get(host(website), o["name"]).replace("&amp;", "&").strip(),
        "website": website,
        "projects_url": pu,
        "facebook": clean_social(o["facebook"]),
        "instagram": clean_social(o["instagram"]),
        "phones": phones[:6],
        "email": email,
        "found_via": o["found_via"],
        "known_projects": o["known_projects"][:40],
        "notes": " | ".join(dict.fromkeys(n for n in notes if n)),
    })

# final dedupe by website host (groups may converge after redirects)
by_host, final = {}, []
for d in sorted(out, key=lambda d: (-len(d["found_via"]), d["name"].lower())):
    h = host(d["website"])
    if h and h in by_host:
        k = by_host[h]
        k["found_via"] = sorted(set(k["found_via"]) | set(d["found_via"]))
        k["known_projects"] += [p for p in d["known_projects"] if p.lower() not in {x.lower() for x in k["known_projects"]}]
        k["phones"] += [p for p in d["phones"] if p not in k["phones"]]
        k["phones"] = k["phones"][:6]
        k["notes"] = " | ".join(x for x in [k["notes"], "merged with: " + d["name"]] if x)
        continue
    if h:
        by_host[h] = d
    final.append(d)
final.sort(key=lambda d: d["name"].lower())
json.dump(final, open(OUT, "w"), ensure_ascii=False, indent=2)
print("total", len(final), "website", sum(1 for d in final if d["website"]),
      "projects_url", sum(1 for d in final if d["projects_url"]),
      "projects_url!=website", sum(1 for d in final if d["projects_url"] and d["projects_url"] != d["website"]))
