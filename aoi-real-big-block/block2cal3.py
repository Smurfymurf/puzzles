#!/usr/bin/env python3
"""Discriminate the 257 prefix-3c6 Block-2 flip sets against the Block-2 prize address."""
import hashlib, itertools, sys
sys.path.insert(0, ".")
import aoi
ADDR = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
exec(open("block2cal.py").read().split("seps =")[0])

def v(p, m):
    if m == 0: return p
    a = list(p); idx = [i for i, c in enumerate(a) if c.isalpha()]
    if m & 1: a[idx[0]] = a[idx[0]].swapcase()
    if m & 2: a[idx[-1]] = a[idx[-1]].swapcase()
    return "".join(a)

print("aoi api:", [n for n in dir(aoi) if not n.startswith("__")])
cand = []
for combo in itertools.product(range(4), repeat=len(P)):
    h = hashlib.md5("\n\n".join(v(P[i], combo[i]) for i in range(len(P))).encode()).digest()
    if h.hex().startswith("3c6"): cand.append((combo, h))
print("prefix-3c6 candidates:", len(cand))

def try_addr(entropy, i):
    for call in (lambda: aoi.bip44_address(entropy, i),
                 lambda: aoi.bip44_address(entropy)[i]):
        try: return call()
        except Exception: pass
    return None

hits = []
for combo, h in cand:
    for i in range(0, 30):
        a = try_addr(h, i)
        if a is None: break
        if a == ADDR: hits.append((combo, i, h.hex()))
print("ADDRESS HITS:", len(hits))
for x in hits[:10]: print(" ", x)
