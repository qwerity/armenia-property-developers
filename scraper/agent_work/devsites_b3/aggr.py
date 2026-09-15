import re,sys
from collections import defaultdict
def aggr(items, cur):
    """items: list of (rooms, area, price)"""
    d=defaultdict(list)
    for r,a,p in items: d[r].append((a,p))
    out=[]
    for r in sorted(d):
        v=d[r]; out.append({"rooms":r,"area_min":min(a for a,_ in v),"area_max":max(a for a,_ in v),"price_from":min(p for _,p in v if p) if any(p for _,p in v) else None,"currency":cur})
    ppm=min(p/a for _,a,p in items if p and a)
    return out, round(ppm)
