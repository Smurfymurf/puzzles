import hashlib, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; F0 = aoi._S["flipped"][0]; n = len(P)
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
def fL(p): return next((c.lower() for c in p if c.isalpha()), "")
FIRST = [fL(p) for p in P]
MARK = set()
for q in (4, 92, 167): MARK |= {q, q + 1, q + 2, q + 3}
CERT = {i for i in range(n) if FIRST[i] not in set("aismt")}
print("marker paragraphs:", sorted(MARK))
print("certified flips:", len(CERT))
def test(tag, S, mode):
    t = "\r\n\r\n".join((F0[i] if i in S else P[i]).replace(chr(0), "\r\n") for i in range(n))
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    print(f"  {tag:26s} {mode:11s} n={len(S):3d} {h}" + ("  *** HIT idx=%d ***" % idx if idx is not None else ""))
sets = {
    "markers only": MARK,
    "certified only": CERT,
    "certified | markers": CERT | MARK,
    "certified & markers": CERT & MARK,
    "certified - markers": CERT - MARK,
    "certified ^ markers": CERT ^ MARK,
    "all - markers": set(range(n)) - MARK,
}
for nm, S in sets.items():
    for mode in MODES:
        test(nm, S, mode)
