import hashlib, itertools, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; FL = aoi._S["fl"]; F0 = aoi._S["flipped"][0]
n = len(P)
QUADS = [4, 92, 167]
def txt(idxs):
    s = set(idxs)
    return "\r\n\r\n".join((F0[i] if i in s else P[i]).replace(chr(0), "\r\n") for i in range(n))
hits = []
def run(name, idxs):
    s = set(idxs)
    t = txt(s)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None:
        hits.append((name, idx, h))
        print("*** HIT ***", name, "idx", idx, h)
    return h
print("exhaustive over the 12 quad paragraphs")
Q = [q + k for q in QUADS for k in range(4)]
print("quad paragraphs:", Q)
cnt = 0
for r in range(1, len(Q) + 1):
    for c in itertools.combinations(Q, r):
        run("", c)
        cnt += 1
print("subsets tested:", cnt, "hits:", hits)
print()
print("--- also: per-quad whole / halves / singles / cross-quad patterns ---")
for k, q in enumerate(QUADS):
    run(f"quad{k} whole", [q, q+1, q+2, q+3])
    run(f"quad{k} FF", [q, q+1])
    run(f"quad{k} WW", [q+2, q+3])
    run(f"quad{k} first2", [q, q+1])
    run(f"quad{k} last2", [q+2, q+3])
for k in range(3):
    run(f"quads 0..{k} whole", [x for q in QUADS[:k+1] for x in (q, q+1, q+2, q+3)])
    run(f"quads 0..{k} FF", [x for q in QUADS[:k+1] for x in (q, q+1)])
    run(f"quads 0..{k} WW", [x for q in QUADS[:k+1] for x in (q+2, q+3)])
    run(f"quads 0..{k} first-of-pair", [q for q in QUADS[:k+1] for x in (q,)])
    run(f"quads 0..{k} second-of-pair", [x for q in QUADS[:k+1] for x in (q+1,)])
run("all 3 quads whole", [x for q in QUADS for x in (q, q+1, q+2, q+3)])
run("all 3 quads FF+WW interleaved", [x for q in QUADS for x in (q, q+2)])
