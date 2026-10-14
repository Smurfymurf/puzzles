import hashlib, hmac, json, os, re

D = os.path.expanduser("~/puzzles/aoi-real-big-block")
SEP = "\r\n\r\n"
TARGETS = {"14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "ESCROW", "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN": "STAGE1"}
KNOWN_BASE = "47ff387425c1a283c22eac15f0268867"

def ripemd160(msg):
    r1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,
          3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,
          4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13]
    r2 = [5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,
          15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,
          12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11]
    s1 = [11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,
          11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,
          9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6]
    s2 = [8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,
          9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,
          8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11]
    K1 = [0x00000000,0x5A827999,0x6ED9EBA1,0x8F1BBCDC,0xA953FD4E]
    K2 = [0x50A28BE6,0x5C4DD124,0x6D703EF3,0x7A6D76E9,0x00000000]
    def rol(x,n): return ((x<<n)|(x>>(32-n)))&0xffffffff
    def f(j,x,y,z):
        if j<16: return x^y^z
        if j<32: return (x&y)|(~x&z)
        if j<48: return (x|~y)^z
        if j<64: return (x&z)|(y&~z)
        return x^(y|~z)
    ml = len(msg)*8
    msg = msg + b"\x80"
    while len(msg)%64 != 56: msg += b"\x00"
    msg += ml.to_bytes(8,"little")
    h = [0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0]
    for off in range(0,len(msg),64):
        X = [int.from_bytes(msg[off+4*i:off+4*i+4],"little") for i in range(16)]
        a,b,c,d,e = h; aa,bb,cc,dd,ee = h
        for j in range(80):
            t = (a + f(j,b,c,d) + X[r1[j]] + K1[j//16]) & 0xffffffff
            t = (rol(t,s1[j]) + e) & 0xffffffff
            a,e,d,c,b = e,d,rol(c,10),b,t
            t = (aa + f(79-j,bb,cc,dd) + X[r2[j]] + K2[j//16]) & 0xffffffff
            t = (rol(t,s2[j]) + ee) & 0xffffffff
            aa,ee,dd,cc,bb = ee,dd,rol(cc,10),bb,t
        t = (h[1]+c+dd)&0xffffffff
        h[1] = (h[2]+d+ee)&0xffffffff
        h[2] = (h[3]+e+aa)&0xffffffff
        h[3] = (h[4]+a+bb)&0xffffffff
        h[4] = (h[0]+b+cc)&0xffffffff
        h[0] = t
    return b"".join(x.to_bytes(4,"little") for x in h)

assert ripemd160(b"").hex() == "9c1185a5c5e9fc54612808977ee8f548b2258d31", "ripemd160 self-test failed"

P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
def _inv(a): return pow(a, P-2, P)
def _add(p,q):
    if p is None: return q
    if q is None: return p
    if p[0]==q[0] and (p[1]+q[1])%P==0: return None
    if p==q: l = (3*p[0]*p[0])*_inv(2*p[1])%P
    else: l = (q[1]-p[1])*_inv(q[0]-p[0])%P
    x = (l*l-p[0]-q[0])%P
    return (x,(l*(p[0]-x)-p[1])%P)
def _mul(k,pt=(Gx,Gy)):
    r=None
    while k:
        if k&1: r=_add(r,pt)
        pt=_add(pt,pt); k>>=1
    return r
def pub(k):
    x,y=_mul(k); return bytes([2+(y&1)])+x.to_bytes(32,"big")
B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58(b):
    n=int.from_bytes(b,"big"); s=""
    while n: n,r=divmod(n,58); s=B58[r]+s
    for c in b:
        if c==0: s="1"+s
        else: break
    return s
def h160(b): return ripemd160(hashlib.sha256(b).digest())
def addr(k):
    h=h160(pub(k)); return b58(b"\x00"+h+hashlib.sha256(hashlib.sha256(b"\x00"+h).digest()).digest()[:4])

assert addr(1)=="1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH", "secp256k1 self-test failed"

import glob
def _pick(names):
    home = os.path.expanduser("~")
    tried = []
    for root in [home, D, os.path.join(home,"puzzles")]:
        for n in names:
            cand = os.path.join(root, n)
            tried.append(cand)
            if os.path.isfile(cand): return cand
    for root in [D, os.path.join(home,"puzzles")]:
        for n in names:
            hits = sorted(glob.glob(os.path.join(root, "**", n), recursive=True))
            if hits: return hits[0]
    raise SystemExit("not found, tried:\n" + "\n".join(tried))
WORDS = open(_pick(["bip39.txt","bip39_english.txt","english.txt"])).read().split()
print("wordlist:", len(WORDS))
assert len(WORDS) == 2048, len(WORDS)
def entropy_to_seed(ent):
    cs = hashlib.sha256(ent).digest()[0] >> 4
    val = (int.from_bytes(ent,"big") << 4) | cs
    m = " ".join(WORDS[(val >> (11*(11-i))) & 2047] for i in range(12))
    return hashlib.pbkdf2_hmac("sha512", m.encode(), b"mnemonic", 2048)
def master(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return int.from_bytes(I[:32],"big"), I[32:]
def ckd(k,c,i):
    data = (b"\x00"+k.to_bytes(32,"big")+i.to_bytes(4,"big")) if i>=2**31 else (pub(k)+i.to_bytes(4,"big"))
    I = hmac.new(c,data,hashlib.sha512).digest()
    return (int.from_bytes(I[:32],"big")+k)%N, I[32:]
def derive(md5hex, idx):
    seed = entropy_to_seed(bytes.fromhex(md5hex))
    k,c = master(seed)
    for j in [44+2**31, 2**31, 2**31, 0, idx]: k,c = ckd(k,c,j)
    return addr(k)

raw = json.load(open(_pick(["aoi_paras.json","second.json","paras.json"])))
if isinstance(raw, dict):
    if all(str(x).isdigit() for x in raw): raw = [raw[x] for x in sorted(raw, key=lambda z:int(z))]
    else:
        for key in ("paras","paragraphs","second","text"):
            if key in raw: raw = raw[key]; break
if isinstance(raw, list) and raw and isinstance(raw[0], dict):
    raw = [d.get("text", d.get("para", d.get("p",""))) for d in raw]
if isinstance(raw, str):
    t = raw.rstrip("\r\n")
    raw = t.split("\r\n\r\n") if "\r\n\r\n" in t else t.split("\n\n")
paras = list(raw)
assert len(paras) > 200, len(paras)
print("paragraphs:", len(paras))
print("first:", repr(paras[0][:50]))
print("last :", repr(paras[-1][-50:]))

SPLIT = re.compile(r"((?<=[.!?\u201d\u2019\"'])\s+)")
def fa(u):
    for i,ch in enumerate(u):
        if ch.isalpha(): return i
    return -1
def flip(u):
    a = fa(u)
    if a < 0: return u
    b = a
    for i in range(len(u)-1, -1, -1):
        if u[i].isalpha(): b = i; break
    L = list(u)
    L[a] = L[a].lower()
    if b != a: L[b] = L[b].upper()
    return "".join(L)
def keep(u, mode):
    a = fa(u)
    if a < 0: return False
    if mode == "all": return True
    if mode == "none": return False
    ins = u[a].upper() in "ITSAM"
    return ins if mode == "ITSAM" else not ins
def build(mode, level):
    out = []
    for p in paras:
        if level == "para":
            out.append(flip(p) if keep(p, mode) else p)
        else:
            parts = SPLIT.split(p)
            for i in range(0, len(parts), 2):
                if keep(parts[i], mode): parts[i] = flip(parts[i])
            out.append("".join(parts))
    return SEP.join(out)

variants = []
for mode in ["none","all","notITSAM","ITSAM"]:
    variants.append(("para_"+mode, build(mode,"para")))
variants.append(("para_firstonly", SEP.join((lambda s: s[:fa(s)]+s[fa(s)].lower()+s[fa(s)+1:] if fa(s)>=0 else s)(p) for p in paras)))
variants.append(("para_lastonly", SEP.join((lambda s: (s[:max([i for i,c in enumerate(s) if c.isalpha()])]+s[max([i for i,c in enumerate(s) if c.isalpha()])].upper()+s[max([i for i,c in enumerate(s) if c.isalpha()])+1:]) if any(c.isalpha() for c in s) else s)(p) for p in paras)))
for mode in ["none","all","notITSAM","ITSAM"]:
    variants.append(("sent_"+mode, build(mode,"sent")))

print("---")
for label, txt in variants:
    h = hashlib.md5(txt.encode("utf-8")).hexdigest()
    tag = " <== KNOWN BASE" if h == KNOWN_BASE else ""
    hits = []
    for idx in range(6):
        a = derive(h, idx)
        if a in TARGETS: hits.append((TARGETS[a], idx))
    print(f"{label:16s} len={len(txt):6d} md5={h}{tag} hits={hits if hits else '-'}")
print("---")
print("targets:", TARGETS)
