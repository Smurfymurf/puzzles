#!/usr/bin/env python3
"""Recover the exact flip set of Grycoin Block 2 by brute force (target prefix 3c6).
Per paragraph: 0=untouched, 1=toggle first alpha, 2=toggle last alpha, 3=both."""
import hashlib, itertools
exec(open("block2cal.py").read().split("seps =")[0])   # reuse P

def v(p, m):
    if m == 0: return p
    a = list(p); idx = [i for i, c in enumerate(a) if c.isalpha()]
    if m & 1: a[idx[0]] = a[idx[0]].swapcase()
    if m & 2: a[idx[-1]] = a[idx[-1]].swapcase()
    return "".join(a)

hits = []
for combo in itertools.product(range(4), repeat=len(P)):
    s = "\n\n".join(v(P[i], combo[i]) for i in range(len(P)))
    h = hashlib.md5(s.encode()).hexdigest()
    if h.startswith("3c6"): hits.append((h, combo))
print("hits:", len(hits))
for h, c in hits[:20]: print(h, c)
