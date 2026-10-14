#!/usr/bin/env python3
"""Fix the author's 2 stated changes, then search paragraph first/last flips around them."""
import hashlib, itertools, sys
sys.path.insert(0, ".")
import aoi
ADDR = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
exec(open("block2cal.py").read().split("seps =")[0])

raw = "\n\n".join(P)
i = raw.index("I expected otherwise"); j = raw.index("himself") + 6
base = raw[:i] + "i" + raw[i+1:]
base = base[:j] + base[j].swapcase() + base[j+1:]

# per-paragraph first/last alpha positions in base (same length as raw)
off, bounds = 0, []
for p in P:
    idxs = [k for k, c in enumerate(p) if c.isalpha()]
    bounds.append((off + idxs[0], off + idxs[-1])); off += len(p) + 2

def seed(e):
    mn = aoi.entropy_to_mnemonic(e)
    if isinstance(mn, bytes): mn = mn.decode()
    return hashlib.pbkdf2_hmac("sha512", mn.encode(), b"mnemonic", 2048, 64)

hits, ncand = [], 0
for combo in itertools.product(range(4), repeat=len(P)):
    b = bytearray(base.encode())
    for p, m in enumerate(combo):
        if m & 1: b[bounds[p][0]] = chr(b[bounds[p][0]]).swapcase().encode()[0]
        if m & 2: b[bounds[p][1]] = chr(b[bounds[p][1]]).swapcase().encode()[0]
    h = hashlib.md5(bytes(b)).digest()
    if h.hex().startswith("3c6"):
        ncand += 1; sd = seed(h)
        for k in range(30):
            if aoi.bip44_address(sd, k) == ADDR: hits.append((combo, k, h.hex()))
print("prefix-3c6:", ncand, " ADDRESS HITS:", len(hits))
for x in hits[:10]: print(" ", x)
