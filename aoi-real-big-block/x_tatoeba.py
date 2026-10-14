import hashlib, bz2, urllib.request, os
T = "8b71bade9685d3388452bc4755b06a0d"
def h(t): return hashlib.md5(t.encode()).hexdigest()
path = "/tmp/eng_sentences.tsv.bz2"
if not os.path.exists(path):
    print("downloading...")
    urllib.request.urlretrieve("https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2", path)
n = 0; hits = []
with bz2.open(path, "rt", encoding="utf-8", errors="replace") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3: continue
        s = parts[2]
        n += 1
        if h(s) == T or h('"%s"' % s) == T:
            hits.append(s)
print("sentences", n, "hits", hits)
