#!/usr/bin/env python3
"""Model-free: toggle any 1 or 2 alpha positions in the span; keep md5 prefix 3c6;
check survivors against Block 2's prize address."""
import hashlib, sys
sys.path.insert(0, ".")
import aoi
ADDR = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
exec(open("block2cal.py").read().split("seps =")[0])

raw = "\n\n".join(P)
pos = [i for i, c in enumerate(raw) if c.isalpha()]
print("alpha positions:", len(pos), " pairs:", len(pos)*(len(pos)-1)//2)

def seed(e):
    mn = aoi.entropy_to_mnemonic(e)
    if isinstance(mn, bytes): mn = mn.decode()
    return hashlib.pbkdf2_hmac("sha512", mn.encode(), b"mnemonic", 2048, 64)

hits = []
def test(s, tag):
    h = hashlib.md5(s.encode()).digest()
    if h.hex().startswith("3c6"):
        sd = seed(h)
        for i in range(30):
            if aoi.bip44_address(sd, i) == ADDR: hits.append((tag, i, h.hex()))

for i in pos:
    test(raw[:i] + raw[i].swapcase() + raw[i+1:], ("1", i))
print("after singles:", len(hits))

for a in range(len(pos)):
    ia = pos[a]; ra = raw[:ia] + raw[ia].swapcase() + raw[ia+1:]
    for b in range(a+1, len(pos)):
        ib = pos[b]
        test(ra[:ib] + ra[ib].swapcase() + ra[ib+1:], ("2", ia, ib))
print("TOTAL HITS:", len(hits))
for x in hits[:20]: print(" ", x)
