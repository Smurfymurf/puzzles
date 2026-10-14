import hashlib, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
L = aoi._S["letters"]
print("aoi loads:", aoi.PARAS)
print("paras:", len(aoi._S["paras"]), "letters:", len(L), repr(L))
KNOWN = "47ff387425c1a283c22eac15f0268867"
TARGETS = {"14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "ESCROW", "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN": "STAGE1"}
def mask_for(excl):
    m = 0
    for i, c in enumerate(L):
        if c not in excl: m |= 1 << i
    return m
S = set(L)
VAR = {"certified": mask_for(set("aismt")), "complement": mask_for(S - set("aismt")),
       "none": mask_for(S), "all": mask_for(set())}
for k, v in VAR.items(): print("mask", k, v)
hits = []
for combo in aoi.COMBOS:
    for name, mask in VAR.items():
        txt = aoi._text(mask, combo)
        h = hashlib.md5(txt.encode("utf-8")).hexdigest()
        idx = aoi.check(txt)
        mark = " <== KNOWN BASE" if h == KNOWN else ""
        if idx is not None:
            hits.append((name, combo, h, idx)); mark += "  *** HIT ***"
        print(f"{name:11s} {str(combo):42s} len={len(txt):6d} {h}{mark}")
print("---")
print("hits:", hits if hits else "none")
