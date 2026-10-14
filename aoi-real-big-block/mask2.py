import hashlib, hmac, os, sys, time
import multiprocessing as mp
try: mp.set_start_method("fork")
except RuntimeError: pass
from multiprocessing import Pool
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi
from mnemonic import Mnemonic

TARGET = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
STAGE1 = "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
COMBOS = [("\r\n\r\n", "", "lowerFirst", True), ("\n\n", "", "lowerFirst", True),
          ("\r\n\r\n", "\r\n", "lowerFirst", True), ("\n\n", "\n", "lowerFirst", True),
          ("\r\n", "", "lowerFirst", True), ("\n", "", "lowerFirst", True)]

aoi._init()
L = aoi._S["letters"]; P = aoi._S["paras"]; FL = aoi._S["fl"]; li = aoi._S["li"]
A0 = [p.replace(chr(0), "\r\n") for p in P]
B0 = [f.replace(chr(0), "\r\n") for f in aoi._S["flipped"][0]]
BIT = [1 << li[i][FL[i]] for i in range(len(P))]
N = 1 << len(L)
print("paras", len(P), "letters", len(L), "space", N)

W = Mnemonic("english").wordlist
PP = 2**256 - 2**32 - 977
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
NB = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
def _dbl(t):
    x,y,z=t
    if z==0 or y==0: return (0,1,0)
    yy=y*y%PP; S=4*x*yy%PP; M=3*x*x%PP; X=(M*M-2*S)%PP
    return (X, (M*(S-X)-8*yy*yy)%PP, 2*y*z%PP)
def _addj(t,u):
    if t[2]==0: return u
    if u[2]==0: return t
    x1,y1,z1=t; x2,y2,z2=u
    z1z1=z1*z1%PP; z2z2=z2*z2%PP
    u1=x1*z2z2%PP; u2=x2*z1z1%PP
    s1=y1*z2*z2z2%PP; s2=y2*z1*z1z1%PP
    if u1==u2:
        return _dbl(t) if s1==s2 else (0,1,0)
    h=(u2-u1)%PP; r=(s2-s1)%PP; hh=h*h%PP; hhh=h*hh%PP; u1hh=u1*hh%PP
    X=(r*r-hhh-2*u1hh)%PP
    return (X, (r*(u1hh-X)-s1*hhh)%PP, h*z1*z2%PP)
def _mul(k):
    r=(0,1,0); base=(Gx,Gy,1)
    for bit in bin(k)[2:]:
        r=_dbl(r)
        if bit=="1": r=_addj(r,base)
    return r
def pub(k):
    x,y,z=_mul(k)
    zi=pow(z,PP-2,PP); zi2=zi*zi%PP
    X=x*zi2%PP; Y=y*zi2*zi%PP
    return bytes([2+(Y&1)])+X.to_bytes(32,"big")
B58="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58(b):
    n=int.from_bytes(b,"big"); s=""
    while n: n,r=divmod(n,58); s=B58[r]+s
    for c in b:
        if c==0: s="1"+s
        else: break
    return s
def ripemd160(msg):
    r1=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8,3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12,1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2,4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13]
    r2=[5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12,6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2,15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13,8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14,12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11]
    s1=[11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8,7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12,11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5,11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12,9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6]
    s2=[8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6,9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11,9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5,15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8,8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11]
    K1=[0,0x5A827999,0x6ED9EBA1,0x8F1BBCDC,0xA953FD4E]; K2=[0x50A28BE6,0x5C4DD124,0x6D703EF3,0x7A6D76E9,0]
    def rol(x,n): return ((x<<n)|(x>>(32-n)))&0xffffffff
    def f(j,x,y,z):
        if j<16: return x^y^z
        if j<32: return (x&y)|(~x&z)
        if j<48: return (x|~y)^z
        if j<64: return (x&z)|(y&~z)
        return x^(y|~z)
    ml=len(msg)*8; msg=msg+b"\x80"
    while len(msg)%64!=56: msg+=b"\x00"
    msg+=ml.to_bytes(8,"little")
    h=[0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0]
    for off in range(0,len(msg),64):
        X=[int.from_bytes(msg[off+4*i:off+4*i+4],"little") for i in range(16)]
        a,b,c,d,e=h; aa,bb,cc,dd,ee=h
        for j in range(80):
            t=(a+f(j,b,c,d)+X[r1[j]]+K1[j//16])&0xffffffff; t=(rol(t,s1[j])+e)&0xffffffff
            a,e,d,c,b=e,d,rol(c,10),b,t
            t=(aa+f(79-j,bb,cc,dd)+X[r2[j]]+K2[j//16])&0xffffffff; t=(rol(t,s2[j])+ee)&0xffffffff
            aa,ee,dd,cc,bb=ee,dd,rol(cc,10),bb,t
        t=(h[1]+c+dd)&0xffffffff; h[1]=(h[2]+d+ee)&0xffffffff; h[2]=(h[3]+e+aa)&0xffffffff
        h[3]=(h[4]+a+bb)&0xffffffff; h[4]=(h[0]+b+cc)&0xffffffff; h[0]=t
    return b"".join(x.to_bytes(4,"little") for x in h)
def addr(k):
    h=ripemd160(hashlib.sha256(pub(k)).digest())
    return b58(b"\x00"+h+hashlib.sha256(hashlib.sha256(b"\x00"+h).digest()).digest()[:4])
def seed_of(h):
    e=bytes.fromhex(h)
    bits=(int.from_bytes(e,"big")<<4)|(hashlib.sha256(e).digest()[0]>>4)
    m=" ".join(W[(bits>>(11*(11-i)))&2047] for i in range(12))
    return hashlib.pbkdf2_hmac("sha512", m.encode(), b"mnemonic", 2048)
def master(seed):
    I=hmac.new(b"Bitcoin seed",seed,hashlib.sha512).digest()
    return int.from_bytes(I[:32],"big"), I[32:]
def ckd(k,c,i):
    data=(b"\x00"+k.to_bytes(32,"big")+i.to_bytes(4,"big")) if i>=2**31 else (pub(k)+i.to_bytes(4,"big"))
    I=hmac.new(c,data,hashlib.sha512).digest()
    return (int.from_bytes(I[:32],"big")+k)%NB, I[32:]
def chk(h):
    k,c=master(seed_of(h))
    for j in (44+2**31,2**31,2**31,0): k,c=ckd(k,c,j)
    for idx in range(6):
        a=addr(ckd(k,c,idx)[0])
        if a==TARGET: return idx,"ESCROW"
        if a==STAGE1: return idx,"STAGE1"
    return None,None

assert ripemd160(b"").hex()=="9c1185a5c5e9fc54612808977ee8f548b2258d31"
assert addr(1)=="1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"

CERT = ("\r\n\r\n","","lowerFirst",True)
h0=hashlib.md5(aoi._text(3796477,CERT).encode()).hexdigest()
print("base md5", h0, "expect 47ff387425c1a283c22eac15f0268867")
print("our addr0", addr(master(seed_of(h0))[0]))
import aoi as _a
print("aoi addr0", _a.bip44_address(seed_of(h0), 0))

def work(rng):
    lo,hi=rng; out=[]
    for mask in range(lo,hi):
        txt="\r\n\r\n".join([B0[i] if (mask&BIT[i]) else A0[i] for i in range(len(P))])
        h=hashlib.md5(txt.encode("utf-8")).hexdigest()
        idx,who=chk(h)
        if idx is not None: out.append((mask,idx,who,h))
    return out

if __name__=="__main__":
    CH=65536
    rs=[(i,min(i+CH,N)) for i in range(0,N,CH)]
    t0=time.time(); done=0; hits=[]
    with Pool() as pool:
        for res in pool.imap_unordered(work,rs):
            done+=CH
            if res:
                hits.extend(res)
                for m,i,w,h in res:
                    print("HIT",m,i,w,h,flush=True)
                    open(os.path.join(D,"mask2_HIT.txt"),"a").write(f"{m} {i} {w} {h}\n")
            el=time.time()-t0
            if el>0:
                r=done/el
                print(f"  {min(done,N)}/{N} {r:.0f}/s ETA {(N-done)/r/60:.1f} min",flush=True)
    print("DONE hits", hits if hits else "none", f"{time.time()-t0:.0f}s")
