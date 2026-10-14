import os, re, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]
def ai(s):
    return [i for i, c in enumerate(s) if c.isalpha()]
print("=== STAGE ONE: the 5 flipped paragraphs, exact change positions ===")
F = os.path.expanduser("~/finney.txt")
for i, p in enumerate([x for x in open(F, encoding="utf-8").read().replace("\r\n", "\n").split("\n") if x.strip()]):
    a = ai(p)
    if not a or p[a[0]].upper() in "ITSAM": continue
    print(f"[{i}] len={len(p)} first-change {a[0]} {p[a[0]]!r} | last-change {a[-1]} {p[a[-1]]!r}")
    print("    first word:", re.search(r"[A-Za-z'-]+", p).group(0))
    print("    last word :", re.findall(r"[A-Za-z'-]+", p)[-1])
    print("    tail      :", repr(p[-45:]))
print()
print("=== CHAPTER: the 12 quad paragraphs, with every stnm-ending word ===")
for i in [4, 5, 6, 7, 92, 93, 94, 95, 167, 168, 169, 170]:
    p = P[i]
    print(f"--- para {i} (len {len(p)}) ---")
    print(p)
    hits = [(m.start(), m.group(0)) for m in re.finditer(r"[A-Za-z'-]+", p) if m.group(0)[-1].lower() in "stnm"]
    print("    stnm-ending words:", hits)
