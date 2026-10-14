import hashlib, os, json, itertools, sys
from multiprocessing import Pool
import aoi, toggle2 as t
J=sys.argv[1] if len(sys.argv)>1 else "\r\n\r\n"
GROUPS=[(4,7),(92,95),(167,170),(229,233)]
aoi._init(); S=aoi._S; m=0
for i,c in enumerate(S["letters"]):
    if c not in set("itasm"): m|=1<<i
base=aoi._text(m,(J,"","lowerFirst",True)).encode()
sepb=J.encode(); paras=base.split(sepb)
pos=[]; off=0
for i,p in enumerate(paras):
    al=[j for j,ch in enumerate(p) if 65<=ch<=90 or 97<=ch<=122]
    if al and any(a<=i<=b for a,b in GROUPS):
        pos.append(off+al[0]); pos.append(off+al[-1])
        pos.extend(off+x for x in al[1:-1])
    off+=len(p)+len(sepb)
pos=sorted(set(pos))
def work(cmb):
    b=bytearray(base)
    for p in cmb: b[p]^=0x20
    for ki,h in t.derive(hashlib.md5(b).digest()):
        if h in (t.TH,t.SH): return (bytes(b), t.b58check(b"\x00"+h))
    return None
if __name__=="__main__":
    n=len(pos)
    tot=n+n*(n-1)//2+n*(n-1)*(n-2)//6
    print("ffww positions",n,"total",tot,flush=True)
    with Pool(os.cpu_count()-1) as pool:
        for k in (1,2,3):
            for r in pool.imap_unordered(work, itertools.combinations(pos,k), chunksize=2000):
                if r: print("FOUND", r, flush=True)
    print("done")
