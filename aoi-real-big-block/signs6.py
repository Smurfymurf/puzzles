import hashlib, itertools, os, re, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; FL = aoi._S["fl"]
n = len(P)
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
SPLIT = re.compile(r"((?<=[.!?])[ ]+)")
def fu(s, mode):
    idx = [i for i, c in enumerate(s) if c.isalpha()]
    if not idx: return s
    a = list(s)
    if mode == "lowerFirst": a[idx[0]] = a[idx[0]].lower(); a[idx[-1]] = a[idx[-1]].upper()
    elif mode == "upperFirst": a[idx[0]] = a[idx[0]].upper(); a[idx[-1]] = a[idx[-1]].lower()
    elif mode == "firstOnly": a[idx[0]] = a[idx[0]].lower()
    else: a[idx[-1]] = a[idx[-1]].upper()
    return "".join(a)
def build(idxs, mode, level):
    out = []
    for i, p in enumerate(P):
        if i not in idxs:
            out.append(p.replace(chr(0), "\r\n")); continue
        if level == "para":
            out.append(fu(p, mode).replace(chr(0), "\r\n")); continue
        parts = SPLIT.split(p)
        if level == "sent":
            for k in range(0, len(parts), 2): parts[k] = fu(parts[k], mode)
        elif parts and parts[0]:
            parts[0] = fu(parts[0], mode)
        out.append("".join(parts).replace(chr(0), "\r\n"))
    return "\r\n\r\n".join(out)
def test(name, idxs, mode, level, quiet=True):
    t = build(set(idxs), mode, level)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None:
        print("*** HIT ***", name, mode, level, "idx", idx, h, flush=True)
    elif not quiet:
        print(f"  {name} {mode} {level} {h}")
    return idx
QUADS = [4, 92, 167]
Q = [q + k for q in QUADS for k in range(4)]
print("exhaustive over", len(Q), "quad paragraphs x 4 modes x 3 levels")
cnt = 0
for r in range(1, len(Q) + 1):
    for c in itertools.combinations(Q, r):
        for mode in MODES:
            for level in ("para", "sent", "firstsent"):
                test(str(c), c, mode, level)
        cnt += 1
        if cnt % 500 == 0: print("  subsets", cnt, flush=True)
print("subsets done:", cnt)
print("--- content-rule sets ---")
sets = {
    "f/w first letters": [i for i in range(n) if FL[i] in "fw"],
    "first word For/First/Fast/Face/Fairly/When/While": [i for i in range(n) if re.match(r"(?i)(for|first|fast|face|fairly|when|while)\b", P[i].strip())],
    "quads plus 230 block": sorted(set(Q) | {230, 231, 232, 233, 234, 235}),
    "mirror paragraphs 5 and 167": [5, 167],
}
for nm, ss in sets.items():
    print(f"  [{nm}] n={len(ss)}")
    for mode in MODES:
        for level in ("para", "sent"):
            test(nm, ss, mode, level, quiet=False)
