import hashlib, os, re, sys
from collections import Counter
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; FL = aoi._S["fl"]; L = aoi._S["letters"]
def fw(p):
    m = re.search(r"[A-Za-z][A-Za-z'-]*", p); return m.group(0) if m else ""
def lw(p):
    w = re.findall(r"[A-Za-z][A-Za-z'-]*", p); return w[-1] if w else ""
F = os.path.expanduser("~/finney.txt")
fps = [p for p in open(F, encoding="utf-8").read().replace("\r\n", "\n").split("\n") if p.strip()]
print("=== STAGE ONE, 5 flipped paragraphs, what the rule actually does ===")
for i, p in enumerate(fps):
    a = next((j for j, c in enumerate(p) if c.isalpha()), -1)
    if a < 0: continue
    if p[a].upper() in "ITSAM": continue
    b = max(j for j, c in enumerate(p) if c.isalpha())
    q = p[:a] + p[a].lower() + p[a+1:b] + p[b].upper() + p[b+1:]
    print(f"[{i}] {fw(p)} ... {lw(p)}")
    print(f"    {p[:56]}")
    print(f"    {q[:56]}")
print("first letters of flipped:", "".join(fw(p)[0] for i, p in enumerate(fps) if (lambda s: s and s[next(j for j,c in enumerate(s) if c.isalpha())].upper() not in "ITSAM")(p)))
print("last letters of flipped :", "".join(lw(p)[-1] for i, p in enumerate(fps) if (lambda s: s and s[next(j for j,c in enumerate(s) if c.isalpha())].upper() not in "ITSAM")(p)))
print()
print("=== CHAPTER: first-letter histogram ===")
print(sorted(Counter(FL).items()))
for t in ("f", "w"):
    idx = [i for i, x in enumerate(FL) if x == t]
    print(f"{t}: {len(idx)} paragraphs -> {idx[:60]}")
    print(f"   last letters: {''.join((lw(P[i])[-1] if lw(P[i]) else '?') for i in idx)}")
print()
def mask_for(s):
    m = 0
    for i, c in enumerate(L):
        if c in s: m |= 1 << i
    return m
print("=== direct escrow tests (CRLFCRLF, lowerFirst) ===")
for s in [set("fw"), set("f"), set("w"), set("fw")|set("b"), set("fwk"), set("fwb"), set("fwv"), set("fwh")]:
    txt = aoi._text(mask_for(s), ("\r\n\r\n", "", "lowerFirst", True))
    h = hashlib.md5(txt.encode("utf-8")).hexdigest()
    idx = aoi.check(txt)
    print(f"{sorted(s)!s:22s} len={len(txt)} {h} {'*** HIT idx=' + str(idx) + ' ***' if idx is not None else ''}")
