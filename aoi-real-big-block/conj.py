import hashlib, os, sys, time
import multiprocessing as mp
try: mp.set_start_method("fork")
except RuntimeError: pass
from multiprocessing import Pool
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; F0 = aoi._S["flipped"][0]; n = len(P)
def fst(p): return next((c.lower() for c in p if c.isalpha()), "")
def lst(p): return next((c.lower() for c in reversed(p) if c.isalpha()), "")
FIRST = [fst(p) for p in P]; LAST = [lst(p) for p in P]
A = [p.replace(chr(0), "\r\n") for p in P]
B = [f.replace(chr(0), "\r\n") for f in F0]
LL = sorted(set(LAST) - {""})
print("distinct last letters:", len(LL), LL)
S1 = {"f", "w", "e"}
def build(S2):
    return "\r\n\r\n".join((B[i] if (FIRST[i] in S1 and LAST[i] in S2) else A[i]) for i in range(n))
def work(rng):
    lo, hi = rng; out = []
    for m in range(lo, hi):
        S2 = {LL[j] for j in range(len(LL)) if (m >> j) & 1}
        t = build(S2)
        h = hashlib.md5(t.encode("utf-8")).hexdigest()
        idx = aoi.check(t)
        if idx is not None: out.append((m, "".join(sorted(S2)), idx, h))
    return out
if __name__ == "__main__":
    print("--- title / edge tests ---")
    for nm, idxs in (("all paragraphs", list(range(n))), ("title excluded", list(range(1, n)))):
        for mode, Fx in (("lowerFirst", F0), ("none", P)):
            t = "\r\n\r\n".join((Fx[i] if mode != "none" else P[i]).replace(chr(0), "\r\n") for i in idxs)
            h = hashlib.md5(t.encode("utf-8")).hexdigest()
            print(f"  {nm:16s} {mode:11s} len={len(t):6d} {h}" + ("  *** HIT ***" if aoi.check(t) is not None else ""))
    print("--- conjunction sweep: first in {f,w,e} AND last in S2 ---")
    N = 1 << len(LL); CH = 8192
    rs = [(i, min(i + CH, N)) for i in range(0, N, CH)]
    t0 = time.time(); done = 0; hits = []
    with Pool() as pool:
        for res in pool.imap_unordered(work, rs):
            done += CH
            if res:
                for m, s2, idx, h in res:
                    hits.append(res); print("*** HIT ***", m, s2, "idx", idx, h, flush=True)
            if done % (CH * 8) == 0 or done >= N:
                el = time.time() - t0; r = done / el
                print(f"  {min(done,N)}/{N} {r:.0f}/s ETA {(N-done)/r/60:.1f} min", flush=True)
    print("DONE hits", hits if hits else "none", round(time.time() - t0), "s")
