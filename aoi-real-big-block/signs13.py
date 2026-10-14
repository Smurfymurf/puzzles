import hashlib, os, re, sys
from collections import defaultdict
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
aoi._init()
P = aoi._S["paras"]; n = len(P)
MODES = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")
def flip_para(p, mode):
    idx = [i for i, ch in enumerate(p) if ch.isalpha()]
    if not idx: return p
    L = list(p)
    if mode == "lowerFirst": L[idx[0]] = L[idx[0]].lower(); L[idx[-1]] = L[idx[-1]].upper()
    elif mode == "upperFirst": L[idx[0]] = L[idx[0]].upper(); L[idx[-1]] = L[idx[-1]].lower()
    elif mode == "firstOnly": L[idx[0]] = L[idx[0]].lower()
    else: L[idx[-1]] = L[idx[-1]].upper()
    return "".join(L)
def build(g, mode):
    return "\r\n\r\n".join(flip_para(p.replace(chr(0), "\r\n"), mode) if g[i] else p.replace(chr(0), "\r\n") for i, p in enumerate(P))
HITS = []
def test(tag, g, mode):
    t = build(g, mode)
    h = hashlib.md5(t.encode("utf-8")).hexdigest()
    idx = aoi.check(t)
    if idx is not None:
        print("*** HIT ***", tag, mode, "idx", idx, h, flush=True); HITS.append((tag, mode))
norm = [re.sub(r"\s+", " ", p.replace(chr(0), " ")).strip().lower() for p in P]
cnt = defaultdict(int)
for x in norm: cnt[x] += 1
dup = [cnt[x] > 1 for x in norm]
NORM = [re.sub(r"\s+", " ", p.replace(chr(0), " ")).strip() for p in P]
pre = defaultdict(list)
for i, x in enumerate(NORM): pre[x[:25]].append(i)
pdup = [len(pre[x[:25]]) > 1 for x in NORM]
preds = {}
def add(nm, fn): preds[nm] = [bool(fn(P[i], i)) for i in range(n)]
add("starts lowercase", lambda p, i: p[:1].islower())
add("ends with uppercase letter", lambda p, i: next((c for c in reversed(p) if c.isalpha()), "").isupper())
add("contains a quote", lambda p, i: '"' in p or "'" in p)
add("contains digit", lambda p, i: any(c.isdigit() for c in p))
add("contains colon", lambda p, i: ":" in p)
add("contains paren", lambda p, i: "(" in p or ")" in p)
add("contains internal br", lambda p, i: chr(0) in p)
add("len>100", lambda p, i: len(p) > 100)
add("len>200", lambda p, i: len(p) > 200)
add("len>350", lambda p, i: len(p) > 350)
add("words>20", lambda p, i: len(re.findall(r"[A-Za-z'-]+", p)) > 20)
add("sentences>1", lambda p, i: len(re.split(r"(?<=[.!?])\s+", p)) > 1)
add("sentences>2", lambda p, i: len(re.split(r"(?<=[.!?])\s+", p)) > 2)
add("contains Satoshi", lambda p, i: "Satoshi" in p)
add("contains Thomas", lambda p, i: "Thomas" in p)
add("contains Bitcoin", lambda p, i: "Bitcoin" in p)
add("contains Grycoin", lambda p, i: "Grycoin" in p)
add("contains Aoi", lambda p, i: "Aoi" in p)
add("contains Hal", lambda p, i: "Hal" in p)
add("contains IBM", lambda p, i: "IBM" in p)
add("contains nonce", lambda p, i: "nonce" in p.lower())
add("contains anagram", lambda p, i: "anagram" in p.lower())
add("contains Satoshi|Thomas|Hal|IBM|nonce|anagram", lambda p, i: any(w in p for w in ("Satoshi", "Thomas", "Hal", "IBM", "nonce", "anagram")))
add("first word For/First/When/While/Face/Fairly", lambda p, i: re.match(r"(?i)(for|first|when|while|face|fairly)\b", p.strip()) is not None)
add("is exact duplicate", lambda p, i: dup[i])
add("shares 25-char prefix", lambda p, i: pdup[i])
add("index < 20", lambda p, i: i < 20)
add("index > n-20", lambda p, i: i > n - 20)
add("index %% 7 == 0", lambda p, i: i % 7 == 0)
names = list(preds)
print("predicates:", len(names))
for nm in names:
    for sign, g in (("", preds[nm]), ("NOT ", [not x for x in preds[nm]])):
        for mode in MODES:
            test(sign + nm, g, mode)
    print("  tested", nm, "flips", sum(preds[nm]), flush=True)
print("--- pairs (lowerFirst) ---")
for a in range(len(names)):
    for b in range(a + 1, len(names)):
        A, B = preds[names[a]], preds[names[b]]
        for op, g in (("AND", [A[i] and B[i] for i in range(n)]), ("OR", [A[i] or B[i] for i in range(n)]),
                      ("AND-NOT", [A[i] and not B[i] for i in range(n)]), ("XOR", [A[i] != B[i] for i in range(n)])):
            if 0 < sum(g) < n:
                test(f"{names[a]} {op} {names[b]}", g, "lowerFirst")
print("HITS:", HITS if HITS else "none")
