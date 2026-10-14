import hashlib, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; n = len(P)
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
QUOTES = "\"'\u201c\u201d\u2018\u2019"
def strict_first(p):
    for c in p:
        if c.isalpha(): return c.lower()
        if c not in QUOTES: return ""
    return ""
def skip_first(p):
    for c in p:
        if c.isalpha(): return c.lower()
    return ""
SQ = [i for i in range(n) if strict_first(P[i]) == ""]
print("paragraphs with a non-letter first char (quote etc):", len(SQ))
def build(groups, mode):
    F = aoi._S["flipped"][MODES.index(mode)]
    return "\r\n\r\n".join((F[i] if groups[i] else P[i]).replace(chr(0), "\r\n") for i in range(n))
def report(tag, groups, mode):
    t = build(groups, mode)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None: print("*** HIT ***", tag, mode, h, flush=True)
    return h
print("--- strict first-char semantics, quoted paragraphs in the '' group ---")
for mode in MODES:
    for excl in (set("aismt"), set("aismt") | {""}):
        g = [strict_first(P[i]) not in excl for i in range(n)]
        report("strict excl=" + ("".join(sorted(excl)) or "-"), g, mode)
        print("   strict excl=" + ("".join(sorted(excl)) or "-"), mode, "flip count", sum(g))
print("--- quoted vs non-quoted, alone ---")
for mode in MODES:
    print("   quoted-only", mode, report("q", [i in SQ for i in range(n)], mode))
    print("   non-quoted", mode, report("nq", [i not in SQ for i in range(n)], mode))
print("--- index-based rules (lowerFirst) ---")
for N in range(2, 25):
    for r in range(N):
        g = [(i % N) == r for i in range(n)]
        if 0 < sum(g) < n:
            h = report(f"i%{N}=={r}", g, "lowerFirst")
for k in (7, 13, 21, 77):
    for tag, g in ((f"first{k}", [i < k for i in range(n)]), (f"last{k}", [i >= n - k for i in range(n)])):
        report(tag, g, "lowerFirst")
print("done")
