import hashlib, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; FL = aoi._S["fl"]; F0 = aoi._S["flipped"][0]
n = len(P)
def lastalpha(p):
    for i in range(len(p)-1,-1,-1):
        if p[i].isalpha(): return p[i].lower()
    return ""
LAST = [lastalpha(p) for p in P]
def txt(idxs):
    return "\r\n\r\n".join((F0[i] if i in idxs else P[i]).replace(chr(0), "\r\n") for i in range(n))
def run(name, idxs):
    s = set(idxs)
    t = txt(s)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    ll = "".join(LAST[i] for i in sorted(s)).upper()
    mark = "  *** HIT idx=" + str(idx) + " ***" if idx is not None else ""
    print(f"{name:32s} n={len(s):3d} md5={h} last={ll[:44]}{mark}")
print("chapter paragraphs:", n)
pairs = [i for i in range(n-1) if FL[i] in "fw" and FL[i+1] == FL[i]]
quads = [i for i in range(n-3) if [FL[i], FL[i+1], FL[i+2], FL[i+3]] == ["f", "f", "w", "w"]]
print("adjacent f/w pairs at:", pairs)
print("FFWW quads at:", quads)
pset = set()
for i in pairs: pset |= {i, i+1}
qset = set()
for i in quads: qset |= {i, i+1, i+2, i+3}
ff = set(); ww = set()
for i in range(n-1):
    if FL[i] == "f" and FL[i+1] == "f": ff |= {i, i+1}
    if FL[i] == "w" and FL[i+1] == "w": ww |= {i, i+1}
print("---")
run("ALL f/w paragraphs", [i for i in range(n) if FL[i] in "fw"])
run("all f/w adjacent pairs", pset)
run("FFWW quads", qset)
run("FF pairs only", ff)
run("WW pairs only", ww)
run("f/w, last in stnm", [i for i in range(n) if FL[i] in "fw" and LAST[i] in "stnm"])
run("f/w, last NOT in stnm", [i for i in range(n) if FL[i] in "fw" and LAST[i] not in "stnm"])
run("pairs with last in stnm", [i for i in pset if LAST[i] in "stnm"])
for k, i in enumerate(quads):
    run(f"quad {k} alone (starts para {i})", [i, i+1, i+2, i+3])
