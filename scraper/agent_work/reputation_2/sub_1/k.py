import sys, re, urllib.parse
from f import fetch, text

for q in sys.argv[1:]:
    h = fetch("https://karg.am/search?lang=hy&q=" + urllib.parse.quote(q))
    tins = list(dict.fromkeys(re.findall(r'href="/company/(\d{8})', h)))
    t = text(h)
    i = t.find("Միայն գործող")
    print("###", q, "tins:", tins[:12])
    print(t[i:i + 1500])
