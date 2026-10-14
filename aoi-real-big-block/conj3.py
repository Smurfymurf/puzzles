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
S1 = None; OP = None
def work(rng):
    lo, hi = rng; out = []
    for m in range(lo, hi):
        S2 = {LL[j] for j in range(len(LL)) if (m >> j) & 1}
        parts = []
        for i in range(n):
            c1 = FIRST[i] in S1
            c2 = LAST[i] in S2
            f = (c1 or c2) if OP == "OR" else (c1 != c2)
            parts.append(B[i] if f else A[i])
        t = "\r\n\r\n".join(parts)
        h = hashlib.md5(t.encode("utf-8")).hexdigest()
        idx = aoi.check(t)
        if idx is not None: out.append((m, "".join(sorted(S2)), idx, h))
    return out
if __name__ == "__main__":
    N = 1 << len(LL); CH = 8192
    rs = [(i, min(i + CH, N)) for i in range(0, N, CH)]
    for op in ("OR", "XOR"):
        for nm, S1v in (("fwe", set("fwe")), ("fw", set("fw")), ("aismt", set("aismt"))):
            S1 = S1v; OP = op
            print("===", op, nm, "===", flush=True)
            t0 = time.time(); done = 0
            with Pool() as pool:
                for res in pool.imap_unordered(work, rs):
                    done += CH
                    if res:
                        for m, s2, idx, h in res:
                            print("*** HIT ***", op, nm, s2, "idx", idx, h, flush=True)
                    if done % (CH * 8) == 0 or done >= N:
                        el = time.time() - t0; r = done / el
                        print(f"  {min(done,N)}/{N} {r:.0f}/s ETA {(N-done)/r/60:.1f} min", flush=True)
            print("  done", op, nm, round(time.time() - t0), "s", flush=True)
