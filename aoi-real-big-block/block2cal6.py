#!/usr/bin/env python3
"""Test the author's OWN stated Block 2 solution: 'I'->'i' and 'himself'->'himselF'."""
import hashlib, sys
sys.path.insert(0, ".")
import aoi
exec(open("block2cal.py").read().split("seps =")[0])

raw = "\n\n".join(P)
i = raw.index("I expected otherwise")
j = raw.index("himself") + 6            # the 'f' of himself
s = raw[:i] + "i" + raw[i+1:]
s = s[:j] + s[j].swapcase() + s[j+1:]
print("changed snippet:", repr(s[i:i+8]), "...", repr(s[j-8:j+2]))
h = hashlib.md5(s.encode()).hexdigest()
print("md5:", h, "  prefix3:", h[:3], " (author says 3c6)")

def seed(e):
    mn = aoi.entropy_to_mnemonic(e)
    if isinstance(mn, bytes): mn = mn.decode()
    return hashlib.pbkdf2_hmac("sha512", mn.encode(), b"mnemonic", 2048, 64)
sd = seed(bytes.fromhex(h))
print("addr idx0..5:", [aoi.bip44_address(sd, k) for k in range(6)])
print("block2 prize :", "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi")
