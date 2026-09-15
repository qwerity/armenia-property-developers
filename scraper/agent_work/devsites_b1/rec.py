"""Record builder: import rec; D=rec.Dev(slug, developer, developer_url, phones, email, social); D.add(...); D.save()"""
import json, os, re, glob
from urllib.parse import urlparse
import f as F
BASE = os.path.dirname(os.path.abspath(__file__))
FINAL = "/Users/ksh/agents/news-agent/armenia-new-builds/scraper/developer_projects_b1.json"
KEYS = ["source","source_url","title","developer","developer_url","city","district","address","lat","lng","price_min_usd_m2","price_min_amd_m2","price_currency_raw","completion","status","floors","type","phones","email","website","social","images","videos","description","apartments"]

def coords(url, i=0):
    c = F.meta(url, F.get(url))["coords"]
    return (float(c[i][0]), float(c[i][1])) if c else (None, None)

def imgs(url, pat="", excl=None, n=12):
    out = [u for u in F.meta(url, F.get(url))["images"] if (not pat or re.search(pat, u)) and not (excl and re.search(excl, u))]
    return out[:n]

def vids(url):
    v = []
    for x in F.meta(url, F.get(url))["videos"]:
        x = ("https:" + x) if x.startswith("//") else x
        if x not in v: v.append(x)
    return v

class Dev:
    def __init__(self, slug, developer, developer_url, phones=(), email="", social=None):
        self.slug, self.recs = slug, []
        self.d = dict(developer=developer, developer_url=developer_url, phones=list(phones), email=email,
                      social={"facebook": "", "instagram": "", "youtube": "", "telegram": "", **(social or {})})
    def add(self, source_url, title, **kw):
        r = {k: None for k in KEYS}
        r.update(source=urlparse(source_url).netloc.replace("www.", ""), source_url=source_url, title=title,
                 phones=list(self.d["phones"]), email=self.d["email"], social=dict(self.d["social"]),
                 developer=self.d["developer"], developer_url=self.d["developer_url"], website=source_url,
                 images=[], videos=[], city="Yerevan", type="residential", price_currency_raw="", description="", address="", district="")
        if kw.get("auto", True):
            lat, lng = coords(source_url)
            r["lat"], r["lng"] = lat, lng
        kw.pop("auto", None)
        for k, v in kw.items():
            if k == "social": r["social"].update(v)
            else: r[k] = v
        if r["apartments"] is None: del r["apartments"]
        if r["description"] and len(r["description"]) > 700: r["description"] = r["description"][:697] + "..."
        r["images"] = r["images"][:12]
        self.recs.append(r); return r
    def save(self, note=""):
        json.dump({"developer": self.d["developer"], "note": note, "projects": self.recs}, open(f"{BASE}/out/{self.slug}.json", "w"), ensure_ascii=False, indent=1)
        merge(); print(self.slug, len(self.recs), "saved")

def merge():
    allr, seen = [], set()
    for p in sorted(glob.glob(f"{BASE}/out/*.json")):
        for r in json.load(open(p))["projects"]:
            k = (r["source_url"], r["title"])
            if k in seen: continue
            seen.add(k); allr.append(r)
    json.dump(allr, open(FINAL, "w"), ensure_ascii=False, indent=1)
