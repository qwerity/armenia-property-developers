"""Second pass: retry dead sites with host variants; find projects URLs via sitemap / common paths."""
import json, re, os, hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from fetch import fetch, D
from enrich import analyze

res = json.load(open("enrich_results.json"))
COMMON = ["/projects", "/en/projects", "/hy/projects", "/am/projects", "/ru/projects", "/project", "/en/project",
          "/projects/", "/portfolio", "/en/portfolio", "/objects", "/buildings", "/hy/buildings"]
LIST_PAT = re.compile(r"(?i)/(en/|hy/|am/|ru/)?(projects?|portfolio|objects|buildings|properties|proekty|nakhagtser|complexes)/?$")


def uncache(u):
    fn = f"{D}/pages/" + hashlib.md5(u.encode()).hexdigest() + ".html"
    for f in (fn, fn + ".meta"):
        if os.path.exists(f):
            os.remove(f)


def retry(site):
    p = urlparse(site if "//" in site else "https://" + site)
    host = p.netloc.replace("www.", "")
    for u in [f"https://www.{host}/", f"http://{host}/", f"http://www.{host}/", f"https://{host}/"]:
        uncache(u)
        r = analyze(u)
        if r["status"].startswith("2"):
            return r
    return None


def sitemap_projects(base):
    urls = []
    for sm in ["sitemap.xml", "sitemap_index.xml", "wp-sitemap.xml"]:
        st, fu, t = fetch(base + sm)
        if st.startswith("2") and "<loc>" in t:
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t)
            for l in locs[:40]:
                if l.endswith(".xml") and re.search(r"(?i)project|portfolio|page|post-type|property|building", l):
                    s2, f2, t2 = fetch(l)
                    locs += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", t2)
            urls = locs
            break
    lists = sorted({u for u in urls if LIST_PAT.search(urlparse(u).path)}, key=len)
    items = [u for u in urls if re.search(r"(?i)/(projects?|portfolio|buildings?|property|properties|complex)/[^/]+/?$", urlparse(u).path)]
    return lists, items


def probe(site, r):
    base = f"{urlparse(r['final_url']).scheme}://{urlparse(r['final_url']).netloc}/"
    lists, items = sitemap_projects(base)
    if lists:
        return lists[0], "found via sitemap.xml"
    if items:
        return None, f"sitemap has {len(items)} project pages e.g. {items[0]}"
    st0, fu0, home = fetch(base)
    for pth in COMMON:
        st, fu, t = fetch(base.rstrip("/") + pth)
        if st.startswith("2") and urlparse(fu).path.rstrip("/") == pth.rstrip("/") and len(t) > 500 \
                and abs(len(t) - len(home)) > 0.05 * max(len(home), 1) and re.search(r"(?i)project|նախագ|проект|portfolio", t):
            return fu, "found by probing common path"
    return None, None


def work(item):
    site, r = item
    if not r["status"].startswith("2"):
        r2 = retry(site)
        if r2:
            r = r2
            r["retry"] = True
    if r["status"].startswith("2") and not r["projects_url"]:
        pu, note = probe(site, r)
        if pu:
            r["projects_url"] = pu
        if note:
            r["projects_note"] = note
    return site, r


with ThreadPoolExecutor(12) as ex:
    out = dict(ex.map(work, res.items()))
json.dump(out, open("enrich_results.json", "w"), ensure_ascii=False, indent=1)
for s, r in sorted(out.items()):
    print(r["status"], s[:40], "->", (r["projects_url"] or "-")[:80], r.get("projects_note", "")[:90])
