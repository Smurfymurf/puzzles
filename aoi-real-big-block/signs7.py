import hashlib, itertools, os, sys, time
from collections import Counter
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; F0 = aoi._S["flipped"][0]; n = len(P)
def la(s):
    for i in range(len(s) - 1, -1, -1):
        if s[i].isalpha(): return s[i].lower()
    return ""
LAST = [la(p) for p in P]
print("distinct last letters:", sorted(Counter(LAST).items()))
F = os.path.expanduser("~/finney.txt")
fps = [p for p in open(F, encoding="utf-8").read().replace("\r\n", "\n").split("\n") if p.strip()]
fl, nf = [], []
for p in fps:
    a = next(i for i, c in enumerate(p) if c.isalpha())
    (nf if p[a].upper() in "ITSAM" else fl).append(p)
FL_ = "".join(la(p) for p in fl); NF_ = "".join(la(p) for p in nf)
print("STAGE ONE flipped   last letters:", FL_)
print("STAGE ONE unflipped last letters:", NF_)
print("DISJOINT:", not (set(FL_) & set(NF_)))
def txt(idxs):
    return "\r\n\r\n".join((F0[i] if i in idxs else P[i]).replace(chr(0), "\r\n") for i in range(n))
def run(label, idxs):
    t = txt(set(idxs))
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None:
        print("*** HIT ***", label, "idx", idx, h, flush=True)
    return idx
S = "stnmy"
print("--- last letter IN subset ---")
for r in range(1, 6):
    for c in itertools.combinations(S, r):
        run("last in " + "".join(c), [i for i in range(n) if LAST[i] in c])
print("--- last letter NOT in subset ---")
for r in range(1, 6):
    for c in itertools.combinations(S, r):
        run("last NOT in " + "".join(c), [i for i in range(n) if LAST[i] not in c])
letters = sorted(set(LAST) - {""})
k = len(letters)
print("--- full sweep over", k, "distinct last letters, space", 2 ** k, "---")
t0 = time.time(); done = 0
for m in range(1, 2 ** k):
    Sx = {letters[j] for j in range(k) if (m >> j) & 1}
    run("set=" + "".join(sorted(Sx)), [i for i in range(n) if LAST[i] in Sx])
    done += 1
    if done % 4096 == 0:
        el = time.time() - t0
        print(f"  {done}/{2**k-1} {done/el:.0f}/s ETA {(2**k-1-done)/(done/el)/60:.1f} min", flush=True)
print("sweep done", round(time.time() - t0), "s")
