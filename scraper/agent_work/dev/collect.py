"""Collect raw developer records from all discovery sources into raw.json."""
import json, re
from urllib.parse import urlparse

BASE = "/Users/ksh/agents/news-agent/armenia-new-builds"
recs = []
FREEMAIL = {"gmail.com", "mail.ru", "yandex.ru", "yandex.com", "yahoo.com", "bk.ru", "list.ru", "icloud.com",
            "hotmail.com", "rambler.ru", "inbox.ru", "outlook.com"}


def add(name, website=None, source="", projects=(), email=None, phones=(), facebook=None, instagram=None, notes=""):
    recs.append(dict(name=(name or "").strip(), website=(website or "").strip() or None, source=source,
                     projects=[p for p in projects if p], email=email, phones=list(phones), facebook=facebook,
                     instagram=instagram, notes=notes))


# karucapatoxic
for p in json.load(open(f"{BASE}/web/data/karucapatoxic.json")):
    soc = p.get("social") or {}
    web = p.get("developer_website")
    name = p.get("developer")
    proj_site = p.get("website")
    email = p.get("email")
    if not name:
        dom = None
        if proj_site and "hsbc.am" not in proj_site and "dignisi" not in proj_site and "norakaruyc.info" not in proj_site:
            dom = proj_site
        elif email and email.split("@")[-1].lower() not in FREEMAIL and "company-name" not in email:
            dom = "https://" + email.split("@")[-1].lower()
        web = dom
        name = p.get("title")
        note = "developer name not given on karucapatoxic; named after project"
    else:
        note = ""
    add(name, web, "karucapatoxic.am", [p.get("title")], email, p.get("phones") or [], soc.get("facebook"),
        soc.get("instagram"), note)
    if p.get("developer") and proj_site and urlparse(proj_site).netloc and web and \
            urlparse(proj_site).netloc.replace("www.", "") != urlparse(web if "//" in web else "https://" + web).netloc.replace("www.", ""):
        recs[-1]["project_sites"] = [proj_site]

# extra_sources (etagi/ac-box)
for p in json.load(open(f"{BASE}/scraper/extra_sources.json")):
    if p.get("developer"):
        add(p["developer"], p.get("developer_url") or None, p["source"] + " (extra_sources.json)", [p.get("title")])

# construction.am
for c in json.load(open("ca.json")):
    name = re.sub(r"\s*\|.*", "", c["title"]).replace("&amp;", "&").strip()
    web = next((e for e in c["ext"] if not re.search(r"facebook|instagram|youtube|linkedin|t\.me|tiktok", e)), None)
    fb = next((e for e in c["ext"] if "facebook" in e), None)
    ig = next((e for e in c["ext"] if "instagram" in e), None)
    add(name, web, "construction.am/developers", [], (c["emails"] or [None])[0], c["phones"], fb, ig)

# novostroiki-yerevan.com
for s, v in json.load(open("nov.json")).items():
    add(v["h1"].replace("New buildings by ", ""), None, "novostroiki-yerevan.com",
        [x.replace("-", " ").title() for x in v["projects"]])

# geoln
for n in ["Estate Investment and Development", "Arcada", "Lorida Group", "Ord Development", "CBS", "Elite Group",
          "ARMAT Realty", "Modern Town", "Metsn Erik", "Filishin LLC", "Orient Stone", "Capital Build",
          "Solar City", "Faith Built Construction"]:
    add(n, None, "geoln.com", ["Argishti 48/8", "Kievyan Residance"] if n.startswith("Estate") else [])

# myhome.am (Ameriabank)
bld = {}
for b in json.load(open("mh_buildings.json"))["items"]:
    bld.setdefault(b["builder"]["eng"].strip(), set()).add(b["name"]["eng"].strip())
for o in json.load(open("mh_details.json")):
    if not isinstance(o, dict):
        continue
    nm = o["builderBrandName"]["eng"].strip()
    web = o.get("webSite")
    fb = web if web and "facebook" in web else None
    ig = web if web and "instagram" in web else None
    if fb or ig:
        web = None
    if web and not web.startswith("http"):
        web = "https://" + web
    add(nm, web, "myhome.am (Ameriabank partners)", sorted(bld.get(nm, [])), o.get("email"),
        [o["phoneNumber"]] if o.get("phoneNumber") else [], fb, ig)

# unibank partner developers
for n in ["Lorida Group", "Gor-Dav", "Pavilion Group", "Just Developer", "New Era", "S.T.Sh.-Pyramida",
          "Olymp Construction", "Rinvest", "Avan Residence", "Amikson Sapphire", "HTSM", "Park Royal Tsaghkadzor",
          "Smart Construction Group", "Arm-Profit", "Green Development", "Double V Construct", "Elitar Shin",
          "Capital Build", "Yeryak Capital", "MGE Construction", "Eco Standard Shin", "Artimed", "Stroy Trest",
          "Mesropyan Shin"]:
    add(n, "https://www.shushi-palace.am/" if n == "Lorida Group" else None, "unibank.am partner developers")

# evocabank partner developers
evoca = {"ASSTROY": None, "White Island": None, "GM Development": None, "Optima 25": None,
         "Midis Construction": None, "Avenue Group": None, "DGA Construction": None, "Pirumyan Shin": None,
         "In Town": None, "River Side": None, "Man Invest Group": None, "Shinart Group": None, "Amur 21": None,
         "S.K. Group": None, "Top Buildings": "https://topbuildings.am/", "Mitstart": None,
         "Technotun": None, "Buldozer Group": None, "Northern Gates": None, "Konstro": None,
         "Kam Developments": None, "Metta Group": None, "VM Building": None, "SV & GA (Art Group)": "https://art-group.am/hy/home",
         "Vagharsh & Vordiner Concern": None, "SAF Capital": None, "Horizon Invest": None}
for n, w in evoca.items():
    add(n, w, "evoca.am construction-companies")

# ar-go.am project pages
for a in json.load(open("argo.json")):
    if a["developer"]:
        d = re.sub(r"^Company:\s*", "", a["developer"]).split(" Builder:")[0]
        d = re.sub(r'["«»“”]|\b(LLC|CJSC|OJSC|LTD)\b', "", d).strip()
        add(d, None, "ar-go.am projects", [re.sub(r"\s*-\s*ARGO Realty Company", "", a["title"])])

# RED Invest Group project pages
for r in json.load(open("red.json")):
    if r["developer"]:
        d = re.split(r"\s+(Design|Completion|CONSTRUCTION COMPANY)", r["developer"], flags=re.I)[0]
        d = re.sub(r'["«»“”]|\b(LLC|CJSC|OJSC|LTD)\b', "", d).strip()
        if len(d) > 2 and d.lower() != "modern":
            add(d, None, "redinvest.am projects", [r["address"].split(",")[0]])

# Armenian Association of Developers members (developers.am, Armenian names transliterated)
for n in ["Artcompany", "Care Building Services", "1SQ", "Elite Group CJSC", "HAEKSHIN CJSC", "Mikshin", "GM Developer",
          "Renshin", "Solar City CJSC", "Hyeland", "AR-GO Realty", "Arcada Construction", "Arm Construct", "Bedeck",
          "Global Real Estate", "Decora Group", "Advanced Development", "Lerents", "Luyser CJSC", "Khakhamyan Heritage",
          "Capital Build", "Art Group", "Art Residence", "Green Property Development", "Up Development",
          "ANI Premium Development", "Gyurjyan Cascade", "Bagrevand House", "Ratco Partner Group", "Just Developer",
          "Forma", "Renovation Project Management Company", "Azbuka Development RA", "Hrach & Ruben",
          "Shant Residential", "Domum", "Saga Shin", "Aranna Shin", "Eve Capital", "Technotun", "AP Tower",
          "Vardanyanshin", "Green Rock", "DCD", "North Shine", "Midis Construction"]:
    add(n, None, "developers.am (Armenian Association of Developers)")

# pages.am real estate developers
SKIP_PAGES = {"team-systems", "ava-granite", "esco-concern", "volta"}
for c in json.load(open("pages.json")):
    if any(c["slug"].startswith(s) for s in SKIP_PAGES):
        continue
    name = c["title"].replace(" | Electronic Armenia", "").replace("&amp;", "&").strip()
    ext = [e for e in c["ext"] if "construction.am" not in e and "comfy.am" not in e and "wa.me" not in e]
    web = next((e for e in ext if not re.search(r"facebook|instagram|youtube|linkedin|t\.me|tiktok|tripadvisor", e)), None)
    add(name, web, "pages.am/real-estate-developers")

# web search discoveries (verified later by crawl)
manual = [
    ("4A Capital", "https://4acapital.am", ["Movenpick Resort Tsaghkadzor", "Nest Residence", "City View", "Aivazovsky Residential Complex"], "WebSearch + construction.am"),
    ("RED Invest Group", "https://www.redinvest.am/en", [], "exclusive sales agent for many developers; project catalog at /en/developers"),
    ("Renshin Urban Investments", "https://renshin.am/en/", ["Skyline"], "Skyline site: https://en.skyline-evn.am/"),
    ("Seray Homes (Seray Developments)", "https://seraydevelopments.com", ["Otevan 1", "Otevan 3"], "Lebanese developer active in Yerevan"),
    ("Mountain Village Dilijan", "https://mountainvillage.am/en", ["Mountain Village"], ""),
    ("Green Rock Management Group", "https://greenrock.am", ["Multifunctional Complex Dilijan", "Villa 3"], ""),
    ("Riverview Dilijan (River Side LLC)", "https://www.riverviewdilijan.com/en", ["River View Dilijan"], ""),
    ("Movsesyan & Partners", "https://movsesyanandpartners.am", ["Dilijan Inn Apartment Complex", "Kasakhum", "Caveman Residence"], ""),
    ("Vardanyanshin (Abovyan Hills)", "https://abovyanhills.am", ["Abovyan Hills"], ""),
    ("Kamertoon", "https://kamertoon.am", ["Kamertoon"], ""),
    ("Renco ArmEstate", "https://www.renco.it", ["Piazza Grande", "Milano and Firenze Towers (Nuovo Velodromo)"], "Italian Renco + Adamium group; Nuovo Velodromo LLC"),
    ("High Park Yerevan (Palladio Shin)", "https://www.highparkyerevan.com", ["High Park Residential Community"], ""),
    ("Navasard Shinarar", "https://navasardshinarar.am/en", ["Acharyan Residential Complex"], ""),
    ("Prime Developers", "https://primedevelopers.am", ["Northern Gates", "Discovery Plaza", "Dilijan Eye"], ""),
    ("DIT Development / DIT Construction", None, ["Yerevan Downtown (Noragyugh)"], "Government-approved developer of Yerevan Downtown; no website found"),
    ("Arin Berd Eco Village", None, ["Arin Berd residential area"], "Instagram only: https://www.instagram.com/arin_berd_eco_village_yerevan/"),
    ("Haus AM", "https://haus.am", [], "townhouses/houses with income tax refund"),
    ("Project EVN", "https://www.projectevn.com", ["Dilijan Project"], ""),
    ("Parajanov Club House (RID LLC)", "https://parajanov.am", ["Parajanov Club House"], ""),
    ("Skyline (Renshin)", "https://en.skyline-evn.am", ["Skyline"], "project site of Renshin"),
    ("TMR (TM Tower / Shinas)", "https://www.tmr.am", ["TM Tower"], ""),
    ("Smart City Developer", "https://smart-city.am", ["Smart City", "Smart City 2", "Smart City 3"], ""),
    ("Monument Hills", "https://monumenthills.am", ["Monument Hills"], "Davit Anhaght 6, Kanaker-Zeytun"),
    ("Azbuka Development RA", "https://monterosso.am/en", ["Monterosso"], "Russian developer Azbuka Zhilya; azbuka.am domain offline"),
    ("Up Development", "https://sundayeveryday.am", ["Sunday Towers"], "upd.am offline; project site sundayeveryday.am"),
    ("Green Property Development", "https://azatutyuncomplex.am", ["Azatutyan Residential Complex"], ""),
    ("Capital Plus", "https://libertyone.am", ["Liberty One"], ""),
    ("Tesq", None, ["Monolith residential complex (Alikhanyan Brothers St)"], "listed on tunmun.am (site blocked from crawler)"),
    ("Target Development", "https://td.am", [], "real estate investment & development company (office/residential/mixed-use)"),
    ("AM Group", "http://www.amgroup.am/en", ["Residential complex, Verin Antarayin str."], "construction company with residential works"),
    ("Shant Residential", None, ["SHANT Residence"], "Facebook: https://www.facebook.com/shantresidence/"),
    ("Advanced Development", None, ["Garunavan 1", "Garunavan 2", "Garunavan 3", "Garunavan 4"], "project site garunavan.am unreachable; sold via RED Invest Group"),
    ("Elite Group", "http://elitegroup.am", ["Elite Plaza", "Almast Residence"], ""),
]
for n, w, pr, note in manual:
    add(n, w, "websearch", pr, notes=note)

guessed = [("Shin-Stroy House", "https://shinstroyhouse.am", ["Wellstone Residential complex", "Duryan 2 Residential Complex"], ""),
           ("Armat Realty", "https://www.americanaarmenia.com", ["Americana Armenia"], "site is the Americana Armenia project"),
           ("SILUET INVEST", "https://siluet.am", ["Siluet Residence"], ""),
           ("Nova Building", "https://novabuilding.am", ["Nova Building"], ""),
           ("Mountain Plaza", "https://mountainplaza.am", [], "construction/development company"),
           ("Aygedzor Construction Company", "https://aygedzor.am", ["Aygedzor", "Solar Residential Complex"], ""),
           ("Green Hills", "https://greenhills.am", ["Green Hills"], "domain matched by name; verify ownership"),
           ("Park Royal Tsaghkadzor", "https://parkroyal.am", ["Park Royal Tsaghkadzor"], "domain matched by name (JS site); verify"),
           ("Hay Develop", "https://hayview.am", ["Hay View"], "project site Hay View"),
           ("Metsn Erik", "https://www.metsnerik.am", [], ""),
           ("Rem Group", "https://www.remgroup.am", ["Rem Tower"], ""),
           ("Liashin", "https://www.liashin.com", [], "")]
add("Prom Group", "https://promgroup.am/en/", "websearch", ["Double Towers", "Eden Park", "Capital Park", "Armenia Garden", "Basis"], notes="general contractor building many developers' residential complexes")
add("Tesaranshin", "https://tesaranresidence.am/en", "websearch", ["Tesaran townhouses", "Aygedzor 3"])
add("Grandshin", None, "websearch", ["E1 Residence (Acharyan 35/19)"], facebook="https://www.facebook.com/p/E1-Residence-100089550075649/", instagram="https://www.instagram.com/e1_residence/")
add("Yeryak Capital", None, "websearch", ["Ararat Park (Echmiadzin)"], facebook="https://www.facebook.com/araratpark/", instagram="https://www.instagram.com/ararat__park/")
add("Arin Berd Eco Village", None, "websearch", [], instagram="https://www.instagram.com/arin_berd_eco_village_yerevan/")
add("Shant Residential", None, "websearch", [], facebook="https://www.facebook.com/shantresidence/")
for n, w, pr, note in guessed:
    add(n, w, "domain guess (verified by fetch)", pr, notes=note)

json.dump(recs, open("raw.json", "w"), ensure_ascii=False, indent=1)
print(len(recs))
