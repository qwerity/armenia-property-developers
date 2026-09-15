import sys, re, time
from f import fetch, text

KW = r"(20(1[5-9]|2[0-9]))|շահագործ|հանձն|сдач|ввод|complet|commission|handover|under construction|ready|sold|кварт|квартал|Q[1-4]|ավարտ|կառուց|строител|construction"
url = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
raw = fetch(url)
t = text(raw)
print("LEN", len(raw), len(t))
print(t[:600])
seen = 0
for m in re.finditer(KW, t, re.I):
    if seen >= n:
        break
    print("...", t[max(0, m.start() - 120):m.end() + 120])
    seen += 1
