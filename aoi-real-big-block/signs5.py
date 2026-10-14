import hashlib, os, re, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; FL = aoi._S["fl"]; F0 = aoi._S["flipped"][0]; L = aoi._S["letters"]
n = len(P)
SPLIT = re.compile(r"((?<=[.!?\u201d\u2019])[ ]+)")
def fu(s, mode):
    idx = [i for i, c in enumerate(s) if c.isalpha()]
    if not idx: return s
    a = list(s)
    if mode == "lowerFirst": a[idx[0]] = a[idx[0]].lower(); a[idx[-1]] = a[idx[-1]].upper()
    elif mode == "upperFirst": a[idx[0]] = a[idx[0]].upper(); a[idx[-1]] = a[idx[-1]].lower()
    elif mode == "firstOnly": a[idx[0]] = a[idx[0]].lower()
    elif mode == "lastOnly": a[idx[-1]] = a[idx[-1]].upper()
    return "".join(a)
def build(idxs, mode, level):
    out = []
    for i, p in enumerate(P):
        if i not in idxs:
            out.append(p.replace(chr(0), "\r\n")); continue
        if level == "para":
            out.append(fu(p, mode).replace(chr(0), "\r\n"))
        else:
            parts = SPLIT.split(p)
            for k in range(0, len(parts), 2):
                parts[k] = fu(parts[k], mode)
            out.append("".join(parts).replace(chr(0), "\r\n"))
    return "\r\n\r\n".join(out)
def mask_set(m):
    return {i for i in range(n) if (m >> aoi._S["li"][i][FL[i]]) & 1}
def run(name, idxs, mode, level):
    t = build(set(idxs), mode, level)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    mark = "  *** HIT idx=" + str(idx) + " ***" if idx is not None else ""
    print(f"{name:30s} {mode:10s} {level:5s} n={len(set(idxs)):3d} {h}{mark}")
QUADS = [4, 92, 167]
sets = {
    "quads whole": [x for q in QUADS for x in (q, q+1, q+2, q+3)],
    "quads FF only": [x for q in QUADS for x in (q, q+1)],
    "quads WW only": [x for q in QUADS for x in (q+2, q+3)],
    "quad0 only": [4, 5, 6, 7],
    "all f/w": [i for i in range(n) if FL[i] in "fw"],
    "all paragraphs": list(range(n)),
    "certified mask": list(mask_set(3796477)),
    "mask complement": list(mask_set(397826)),
}
for nm, ss in sets.items():
    for mode in ("lowerFirst", "upperFirst", "firstOnly", "lastOnly"):
        for level in ("para", "sent"):
            run(nm, ss, mode, level)
