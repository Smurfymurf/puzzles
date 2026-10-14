import hashlib, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
def report(tag, t):
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    print(f"{tag:40s} len={len(t):6d} {h}" + ("  *** HIT idx=%d ***" % idx if idx is not None else ""))
print("=== STRUCT = p ===")
aoi.STRUCT[0] = "p"; aoi._init()
P = aoi._S["paras"]
br = [i for i, p in enumerate(P) if chr(0) in p]
nb = [i for i, p in enumerate(P) if "\u00a0" in p]
print("paras", len(P), "| br paragraphs", br, "| NBSP paragraphs", nb)
for i in br + nb:
    print(f"  [{i}] {P[i][:96]!r}")
def build_p(idxs, mode):
    F = aoi._S["flipped"][MODES.index(mode)]
    return "\r\n\r\n".join((F[i] if i in idxs else p).replace(chr(0), "\r\n") for i, p in enumerate(P))
for mode in MODES:
    for nm, ss in (("br paragraphs", br), ("NBSP paragraphs", nb), ("br+NBSP", sorted(set(br) | set(nb)))):
        report(f"p / {nm} / {mode}", build_p(set(ss), mode))
print("=== STRUCT = br (split on internal br) ===")
aoi.STRUCT[0] = "br"; aoi._init()
L = aoi._S["letters"]
print("paras", len(aoi._S["paras"]), "letters", len(L), L)
for excl in (set("aismt"), set()):
    m = 0
    for i, c in enumerate(L):
        if c not in excl: m |= 1 << i
    for mode in MODES:
        report(f"br / excl={''.join(sorted(excl)) or '-'} / {mode}", aoi._text(m, ("\r\n\r\n", "", mode, True)))
