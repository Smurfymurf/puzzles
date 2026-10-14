import hashlib
TARGET = "8b71bade9685d3388452bc4755b06a0d"
base = '"What?"'
def md5(s): return hashlib.md5(s.encode("utf-8")).hexdigest()
print("sanity md5:", md5(base)[:8], "(expect 184826be)")
c = {}
def add(s, tag):
    if s not in c: c[s] = tag
for a in "Ww":
    for b in "tT":
        add(base[:1] + a + base[2:4] + b + base[5:], "case")
add('"WHAT?"', "upper"); add('"what?"', "lower")
for lq in ['"', '\u201c', '\u2018', "'", '']:
    for rq in ['"', '\u201d', '\u2019', "'", '']:
        add(lq + "What?" + rq, "quotes"); add(lq + "whaT?" + rq, "quotes")
ws = ['', ' ', '  ', '\t', '\r', '\n', '\r\n', '\xa0', '\u200b', '\u2009', '\u202f', ' \r\n', '\r\n ']
for w in ws:
    for t in [base, '"whaT?"', '"what?"']:
        add(w + t, "lead"); add(t + w, "trail"); add(w + t + w, "both")
for t in [base, '"whaT?"']:
    add(t.replace('"', '&quot;'), "entity"); add(t.replace('"', '\\"'), "escaped")
    for p, s in [("<p>", "</p>"), ("<p>", ""), ("", "</p>")]:
        add(p + t + s, "tags")
print("candidates:", len(c))
hit = [(repr(s), tag) for s, tag in c.items() if md5(s) == TARGET]
print("HITS:", hit if hit else "none")
