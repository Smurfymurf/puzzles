import hashlib, os, re, sys
from collections import defaultdict
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; n = len(P)
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
def build(groups, mode):
    F = aoi._S["flipped"][MODES.index(mode)]
    return "\r\n\r\n".join((F[i] if groups[i] else P[i]).replace(chr(0), "\r\n") for i in range(n))
def report(tag, groups, mode):
    t = build(groups, mode)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None: print("*** HIT ***", tag, mode, h, flush=True)
    else: print(f"  {tag:30s} {mode:11s} flips={sum(groups):3d} {h}")
print("--- CORRECTED: first CHARACTER not a letter ---")
def sf(p):
    c = p[0] if p else ""
    return c.lower() if c.isalpha() else ""
Q = [i for i in range(n) if sf(P[i]) == ""]
qmarks = [i for i in range(n) if P[i][:1] in "\"'\u201c\u201d\u2018\u2019"]
print("first char not a letter:", len(Q), "| starts with a quote:", len(qmarks))
for mode in MODES:
    for excl in (set("aismt"), set("aismt") | {""}, set()):
        report("strict excl=" + ("".join(sorted(excl)) or "-"), [sf(P[i]) not in excl for i in range(n)], mode)
print("--- DUPLICATES as signs ---")
norm = [re.sub(r"\s+", " ", p.replace(chr(0), " ")).strip().lower() for p in P]
ex = defaultdict(list)
for i, x in enumerate(norm): ex[x].append(i)
dups = sorted(i for v in ex.values() if len(v) > 1 for i in v)
print("exact duplicate paragraphs:", dups)
pr = defaultdict(list)
for i, x in enumerate(norm): pr[x[:25]].append(i)
pdups = sorted(i for v in pr.values() if len(v) > 1 for i in v)
print("shared 25-char prefix:", pdups)
for v in pr.values():
    if len(v) > 1: print("   group", v, "->", repr(norm[v[0]][:60]))
for mode in MODES:
    report("exact duplicates", [i in set(dups) for i in range(n)], mode)
    report("shared 25-char prefix", [i in set(pdups) for i in range(n)], mode)
