import sys, re
from f import fetch, text

PATS = [r"^(.*?) \(ՀՎՀՀ", r"Կարգավիճակ (\S+)", r"Գրանցման ամսաթիվ (\d\d\.\d\d\.\d{4})",
        r"Կազմակերպաիրավական ձև (.*?\))", r"Իրավաբանական հասցե (.*?) Հարկման",
        r"Դատական գործեր (\d+)", r"Կատարողական վարույթներ (\d+)", r"AI նկարագրություն (.*?)Աղբյուր"]

for tin in sys.argv[1:]:
    t = text(fetch(f"https://karg.am/company/{tin}"))
    vals = []
    for p in PATS:
        m = re.search(p, t)
        vals.append(m.group(1).strip()[:300] if m else "-")
    fm = re.search(r"Հիմնադիր(?:ներ)?\s*[:(].{0,300}", t[t.find("Ֆինանսներ"):] if "Ֆինանսներ" in t else t)
    print(tin, " | ".join(vals), "| F:", fm.group(0)[:300] if fm else "-")
