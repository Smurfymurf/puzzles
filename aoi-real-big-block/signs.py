import os, re
F = os.path.expanduser("~/finney.txt")
raw = open(F, encoding="utf-8").read().replace("\r\n", "\n")
paras = [p for p in raw.split("\n") if p.strip()]
print("finney paras:", len(paras))
def fa(p):
    for i, c in enumerate(p):
        if c.isalpha(): return i
    return -1
def fw(p):
    m = re.search(r"[A-Za-z][A-Za-z'-]*", p)
    return m.group(0) if m else ""
def lw(p):
    w = re.findall(r"[A-Za-z][A-Za-z'-]*", p)
    return w[-1] if w else ""
base = [fa(p) >= 0 and p[fa(p)].upper() not in "ITSAM" for p in paras]
base0 = [not p or p[0] not in set("ITASM") for p in paras]
print("flip count first-alpha-rule:", sum(base), "| literal p[0] rule:", sum(base0), "| identical:", base == base0)
for i, p in enumerate(paras):
    print(f"{i:3d} {'FLIP' if base[i] else '----'} | {p[:74]}")
MSG = "Today I come out If you want to know Satoshi's true identity recognize the signs".split()
CONTENT = ["Today", "come", "out", "know", "true", "identity", "recognize", "signs", "Satoshi"]
print("FLIP first-words:", sorted({fw(p) for i, p in enumerate(paras) if base[i]}))
print("NONE first-words:", sorted({fw(p) for i, p in enumerate(paras) if not base[i]}))
def test(name, pred):
    got = [pred(p) for p in paras]
    print(f"{name:32s} count={sum(got):3d} exact_match={got == base}")
test("first word in MSG", lambda p: fw(p) in MSG)
test("contains any MSG word", lambda p: any(w in p for w in MSG))
test("contains any CONTENT word", lambda p: any(w in p for w in CONTENT))
test("first word in CONTENT", lambda p: fw(p) in CONTENT)
test("last word in MSG", lambda p: lw(p) in MSG)
test("first letter is lowercase", lambda p: fa(p) >= 0 and p[fa(p)].islower())
test("first word is all-lowercase", lambda p: fw(p).islower() and fw(p) != "")
