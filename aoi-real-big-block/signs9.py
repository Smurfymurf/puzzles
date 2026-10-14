import os, re, sys
from collections import Counter
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]
def anchors(p):
    w = re.findall(r"[A-Za-z][A-Za-z'-]*", p)
    s = re.findall(r"[A-Za-z][A-Za-z'-]*", re.split(r"(?<=[.!?])\s+", p)[0]) if p else []
    return {
        "para_first": next((c.lower() for c in p if c.isalpha()), ""),
        "para_last": next((c.lower() for c in reversed(p) if c.isalpha()), ""),
        "firstword_first": w[0][0].lower() if w else "",
        "firstword_last": w[0][-1].lower() if w else "",
        "lastword_first": w[-1][0].lower() if w else "",
        "lastword_last": w[-1][-1].lower() if w else "",
        "firstsent_first": s[0][0].lower() if s else "",
    }
F = os.path.expanduser("~/finney.txt")
fps = [p for p in open(F, encoding="utf-8").read().replace("\r\n", "\n").split("\n") if p.strip()]
flip = [p for p in fps if p[next(i for i, c in enumerate(p) if c.isalpha())].upper() not in "ITSAM"]
noflip = [p for p in fps if p not in flip]
print("=== STAGE ONE separability by anchor ===")
for k in anchors("x"):
    A = {anchors(p)[k] for p in flip}
    B = {anchors(p)[k] for p in noflip}
    ok = not (A & B)
    print(f"{k:18s} flipped={sorted(A)}  unflipped={sorted(B)}  SEPARABLE={ok}")
    if ok: print(f"    -> implied exclude set: {''.join(sorted(B))}")
print()
print("=== chapter anchor histograms ===")
for k in anchors("x"):
    print(" ", k, sorted(Counter(anchors(p)[k] for p in P).items()))
