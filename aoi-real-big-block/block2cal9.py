#!/usr/bin/env python3
import hashlib, itertools, sys
sys.path.insert(0, ".")
import aoi
ADDR = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
H160 = "09d565074752019721ce68c58548ebc13750d5cc"
PUB  = "039ad91b631e5e2f0915b682c6ab8a29d81bb464a2ffc8ebf9702aad7b238192dc"
exec(open("block2cal.py").read().split("seps =")[0])

print("address consistency:", aoi.b58check(b"\x00" + bytes.fromhex(H160)), "==", ADDR)
print("pubkey->hash160 ok:", aoi.hash160(bytes.fromhex(PUB)).hex() == H160)

raw = "\n\n".join(P)
i = raw.index("I expected otherwise"); j = raw.index("himself") + 6
base = raw[:i] + "i" + raw[i+1:]
base = base[:j] + base[j].swapcase() + base[j+1:]
off, bounds = 0, []
for p in P:
    idxs = [k for k, c in enumerate(p) if c.isalpha()]
    bounds.append((off + idxs[0], off + idxs[-1])); off += len(p) + 2

def P_addr(b32):
    k = int.from_bytes(b32, "big") % (2**256)
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
    txt = bytes(b); h = hashlib.md5(txt).digest()
    if not h.hex().startswith("3c6"): continue
    tests = {
        "sha256(text)":      hashlib.sha256(txt).digest(),
        "sha256(md5)":       hashlib.sha256(h).digest(),
        "sha256(md5hex)":    hashlib.sha256(h.hex().encode()).digest(),
        "md5":               h,
        "md5*2":             h + h,
    }
    for name, k in tests.items():
        if P_addr(k) == ADDR: found.append((name, combo, h.hex()))
    sd = seed(h)
    for k in range(0, 60):
        if aoi.bip44_address(sd, k) == ADDR: found.append(("bip44", combo, k, h.hex()))
print("FOUND:", len(found))
for x in found[:10]: print(" ", x)
