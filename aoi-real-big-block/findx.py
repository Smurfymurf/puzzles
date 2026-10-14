import hashlib, glob, json, os, re
TARGET = "8b71bade9685d3388452bc4755b06a0d"
ROOTS = [os.path.expanduser("~"), os.path.expanduser("~/puzzles"), os.path.expanduser("~/puzzles/aoi-real-big-block")]
files = set()
for r in ROOTS:
    for pat in ("*.json", "*/*.json", "*/*/*.json"):
        files |= set(glob.glob(os.path.join(r, pat)))
print("json files found:", len(files))
def md5(s): return hashlib.md5(s.encode("utf-8")).hexdigest()
def walk(o, out):
    if isinstance(o, str): out.append(o)
    elif isinstance(o, list):
        for x in o: walk(x, out)
    elif isinstance(o, dict):
        for v in o.values(): walk(v, out)
hits = []; seen = 0
for f in sorted(files):
    try: o = json.load(open(f, encoding="utf-8"))
    except Exception: continue
    out = []; walk(o, out)
    for s in out:
        if not s or len(s) > 3000: continue
        seen += 1
        if md5(s) == TARGET: hits.append((f, "WHOLE", s[:140]))
        for piece in re.split(r"(?<=[.!?])\s+|\n", s):
            p = piece.strip()
            if p and md5(p) == TARGET: hits.append((f, "PIECE", p[:140]))
print("strings scanned:", seen)
print("HITS:", hits if hits else "none")
