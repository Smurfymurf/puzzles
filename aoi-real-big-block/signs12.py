import hashlib, os, sys
from collections import Counter
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; n = len(P)
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
print("--- non-ASCII census ---")
c = Counter(); where = {}
for i, p in enumerate(P):
    for ch in p:
        if ord(ch) > 126:
            c[ch] += 1; where.setdefault(ch, []).append(i)
for ch, k in sorted(c.items()):
    print(f"  U+{ord(ch):04X} {ch!r} x{k} paras={sorted(set(where[ch]))[:12]}")
print("  total non-ASCII:", sum(c.values()))
def flip_para(p, mode):
    idx = [i for i, ch in enumerate(p) if ch.isalpha()]
    if not idx: return p
    L = list(p)
    if mode == "lowerFirst": L[idx[0]] = L[idx[0]].lower(); L[idx[-1]] = L[idx[-1]].upper()
    elif mode == "upperFirst": L[idx[0]] = L[idx[0]].upper(); L[idx[-1]] = L[idx[-1]].lower()
    elif mode == "firstOnly": L[idx[0]] = L[idx[0]].lower()
    else: L[idx[-1]] = L[idx[-1]].upper()
    return "".join(L)
def firstletter(p):
    for ch in p:
        if ch.isalpha(): return ch.lower()
    return ""
TR = {
    "keep": lambda s: s,
    "nbsp->space": lambda s: s.replace("\u00a0", " "),
    "nbsppair->2space": lambda s: s.replace("\u00a0 ", "  "),
    "nbsppair->1space": lambda s: s.replace("\u00a0 ", " "),
    "nbsp->delete": lambda s: s.replace("\u00a0", ""),
}
def report(tag, tr, groups, mode):
    parts = []
    for i, p in enumerate(P):
        q = tr(p).replace(chr(0), "\r\n")
        parts.append(flip_para(q, mode) if groups[i] else q)
    t = "\r\n\r\n".join(parts)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None: print("*** HIT ***", tag, mode, h, flush=True)
    else: print(f"  {tag:18s} {mode:11s} flips={sum(groups):3d} {h}")
for name, tr in TR.items():
    for gname, groups in (
        ("none", [False] * n),
        ("certified", [firstletter(tr(P[i])) not in set("aismt") for i in range(n)]),
        ("all", [True] * n),
    ):
        for mode in MODES:
            report(f"{name}/{gname}", tr, groups, mode)
