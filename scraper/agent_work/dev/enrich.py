"""Crawl each developer homepage: verify it is alive, find the projects listing URL, socials, emails, phones."""
import json, re, html
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse, unquote
from fetch import fetch

FREEMAIL = {"gmail.com", "mail.ru", "yandex.ru", "yandex.com", "yahoo.com", "bk.ru", "list.ru", "icloud.com",
            "hotmail.com", "rambler.ru", "inbox.ru", "outlook.com"}
AGENT = {"ar-go.am", "redgroup.am", "construction.am", "karucapatoxic.am", "hsbc.am", "dignisi.am"}
HREF_PAT = re.compile(r"(?i)(/projects?/?(\?.*)?$|/proekty/?$|/our-projects|/portfolio/?$|/objects/?$|/complexes/?$|"
                      r"/buildings/?$|/properties/?$|/nakhagtser|/%D5%B6%D5%A1%D5%AD%D5%A1%D5%A3%D5%AE%D5%A5%D6%80|"
                      r"page=project_list|/works/?$|/residential-complexes|/novostroyki/?$|/projects/all)")
TEXT_PAT = re.compile(r"(?i)^\s*(our\s+)?(projects?|նախագծեր|նախագծերը|проекты|наши проекты|объекты|portfolio|"
                      r"residential complexes|complexes|buildings|properties|works|մեր նախագծերը|բնակելի համալիրներ|"
                      r"жилые комплексы|ongoing projects|current projects|all projects)\s*$")
PROJ_ITEM = re.compile(r"(?i)/(project|projects|proekt|property|properties|building|buildings|complex)/[^/?#]+")


def anchors(t):
    for m in re.finditer(r"(?is)<a\b[^>]*href=[\"']([^\"'#]+)[\"'][^>]*>(.*?)</a>", t):
        yield m.group(1).strip(), re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))).strip()


def same_site(u, host):
    h = urlparse(u).netloc.lower().replace("www.", "")
    return h == host or h.endswith("." + host) or host.endswith("." + h)


def analyze(site):
    st, fu, t = fetch(site)
    if not st.startswith("2") and site.startswith("https://"):
        st2, fu2, t2 = fetch("http://" + site[8:])
        if st2.startswith("2"):
            st, fu, t = st2, fu2, t2
    res = dict(status=st, final_url=fu, projects_url=None, facebook=None, instagram=None, emails=[], phones=[],
               item_links=0, n_links=0, title=None)
    if not st.startswith("2") or len(t) < 200:
        return res
    tm = re.search(r"(?is)<title[^>]*>(.*?)</title>", t)
    res["title"] = html.unescape(re.sub(r"\s+", " ", tm.group(1))).strip()[:120] if tm else None
    host = urlparse(fu).netloc.lower().replace("www.", "")
    cands, items = [], set()
    for href, txt in anchors(t):
        u = urljoin(fu, href)
        if not u.startswith("http"):
            continue
        res["n_links"] += 1
        if "facebook.com" in u and not res["facebook"] and "sharer" not in u:
            res["facebook"] = u
        if "instagram.com" in u and not res["instagram"]:
            res["instagram"] = u
        if not same_site(u, host):
            continue
        path = unquote(urlparse(u).path)
        score = 0
        if HREF_PAT.search(u) or HREF_PAT.search(path):
            score += 2
        if TEXT_PAT.match(txt or ""):
            score += 3
        if score:
            cands.append((score, -len(u), u))
        if PROJ_ITEM.search(path):
            items.add(u)
    res["item_links"] = len(items)
    if cands:
        cands.sort(reverse=True)
        res["projects_url"] = cands[0][2]
    elif len(items) >= 2:
        res["projects_url"] = fu
        res["projects_note"] = "no listing page; project pages linked from homepage"
    res["emails"] = sorted({e.lower() for e in re.findall(r"[\w.+-]+@[\w-]+\.[a-z]{2,6}", t)
                            if not re.search(r"(?i)\.(png|jpg|webp|svg|gif)$|sentry|example|wixpress|domain\.com", e)})[:5]
    res["phones"] = sorted({re.sub(r"[^\d+]", "", p) for p in re.findall(r"tel:([+\d\s()-]{6,})", t)})[:5]
    return res


def main():
    data = json.load(open("merged.json"))
    sites = {}
    for o in data:
        cand = []
        if o["website"]:
            cand.append(o["website"])
        if o.get("email") and "@" in o["email"]:
            d = o["email"].split("@")[-1].lower()
            if d not in FREEMAIL and d not in AGENT:
                cand.append("https://" + d)
        o["_cands"] = cand
        for c in cand:
            u = c if "//" in c else "https://" + c
            base = f"{urlparse(u).scheme}://{urlparse(u).netloc}/"
            sites[c] = u if o["website"] == c else base
    with ThreadPoolExecutor(12) as ex:
        results = dict(zip(sites, ex.map(lambda c: analyze(sites[c]), sites)))
    json.dump(results, open("enrich_results.json", "w"), ensure_ascii=False, indent=1)
    json.dump(data, open("merged.json", "w"), ensure_ascii=False, indent=1)
    for c, r in results.items():
        print(r["status"], c[:45], "->", (r["projects_url"] or "-")[:70], r["item_links"], r["n_links"])


if __name__ == "__main__":
    main()
