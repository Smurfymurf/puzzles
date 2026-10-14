import hashlib, urllib.request, gzip, io, tarfile, os
T = "8b71bade9685d3388452bc4755b06a0d"
def h(t): return hashlib.md5(t.encode()).hexdigest()

# try a compact English sentence list first
cands = set()
srcs = [
 "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/fakenews-gambling-porn/hosts",
]
# a few ready sentence lists
for u in ("https://raw.githubusercontent.com/1f604/sarcasm-detection/master/datasets/sarcasm.txt",):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"}), timeout=60)
        d = r.read()
        if r.headers.get("Content-Encoding")=="gzip": d = gzip.decompress(d)
        for line in d.decode("utf-8","replace").splitlines():
            s = line.strip()
            if s: cands.add(s); cands.add('"%s"' % s)
    except Exception as e: print("ERR", u, e)

print("cands", len(cands), "hits", [repr(c) for c in cands if h(c) == T])
