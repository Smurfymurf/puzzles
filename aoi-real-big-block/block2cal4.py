#!/usr/bin/env python3
"""Correct pipeline. Sanity = Stage One first; then discriminate the 257 vs Block 2 addr."""
import hashlib, itertools, sys
sys.path.insert(0, ".")
import aoi
ADDR = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
exec(open("block2cal.py").read().split("seps =")[0])

def seed(e):
    mn = aoi.entropy_to_mnemonic(e)
    if isinstance(mn, bytes): mn = mn.decode()
    return hashlib.pbkdf2_hmac("sha512", mn.encode(), b"mnemonic", 2048, 64)

print("SANITY stage1 idx0:", aoi.bip44_address(seed(bytes.fromhex(aoi.STAGE1_MD5)), 0))
print("         expected  : 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN")

def v(p, m):
    if m == 0: return p
    a = list(p); idx = [i for i, c in enumerate(a) if c.isalpha()]
    if m & 1: a[idx[0]] = a[idx[0]].swapcase()
    if m & 2: a[idx[-1]] = a[idx[-1]].swapcase()
    return "".join(a)

cand = []
for combo in itertools.product(range(4), repeat=len(P)):
    h = hashlib.md5("\n\n".join(v(P[i], combo[i]) for i in range(len(P))).encode()).digest()
    if h.hex().startswith("3c6"): cand.append((combo, h))
print("prefix-3c6 candidates:", len(cand))

hits = []
for combo, h in cand:
    s = seed(h)
    for i in range(0, 30):
        if aoi.bip44_address(s, i) == ADDR:
            hits.append((combo, i, h.hex()))
print("ADDRESS HITS:", len(hits))
for x in hits[:10]: print(" ", x)
