#!/usr/bin/env python3
"""Same 257 candidates, but try alternative derivations + wider index."""
import hashlib, itertools, sys
sys.path.insert(0, ".")
import aoi
ADDR = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
exec(open("block2cal.py").read().split("seps =")[0])

raw = "\n\n".join(P)
i = raw.index("I expected otherwise"); j = raw.index("himself") + 6
base = raw[:i] + "i" + raw[i+1:]
base = base[:j] + base[j].swapcase() + base[j+1:]
off, bounds = 0, []
for p in P:
    idxs = [k for k, c in enumerate(p) if c.isalpha()]
    bounds.append((off + idxs[0], off + idxs[-1])); off += len(p) + 2

def addr_priv(b32):
    k = int.from_bytes(b32, "big")
    return aoi.b58check(b"\x00" + aoi.hash160(aoi._pub(k.to_bytes(32, "big"), True)))

def seed(e):
    mn = aoi.entropy_to_mnemonic(e)
    if isinstance(mn, bytes): mn = mn.decode()
    return hashlib.pbkdf2_hmac("sha512", mn.encode(), b"mnemonic", 2048, 64)

found = []
for combo in itertools.product(range(4), repeat=len(P)):
    b = bytearray(base.encode())
    for p, m in enumerate(combo):
        if m & 1: b[bounds[p][0]] = chr(b[bounds[p][0]]).swapcase().encode()[0]
        if m & 2: b[bounds[p][1]] = chr(b[bounds[p][1]]).swapcase().encode()[0]
    h = hashlib.md5(bytes(b)).digest()
    if not h.hex().startswith("3c6"): continue
    if addr_priv(h) == ADDR: found.append(("rawpriv", combo, h.hex()))
    if addr_priv(hashlib.sha256(h).digest()) == ADDR: found.append(("sha256", combo, h.hex()))
    sd = seed(h)
    for k in range(0, 200):
        if aoi.bip44_address(sd, k) == ADDR: found.append(("bip44", combo, k, h.hex()))
print("FOUND:", len(found))
for x in found[:10]: print(" ", x)
