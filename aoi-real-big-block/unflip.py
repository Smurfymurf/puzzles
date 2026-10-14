#!/usr/bin/env python3
# unflip.py - switch K paragraphs to the OTHER side of the case rule (mask differs by K).
# usage: unflip.py [K]   (default 3)
import os, sys, hashlib, time, itertools
import aoi, toggle2 as t
aoi._init()
S=aoi._S
mask=0
for i,c in enumerate(S["letters"]):
    if c not in set("itasm"): mask|=1<<i
JOIN="\r\n\r\n"
T0b=aoi._text(mask,(JOIN,"","lowerFirst",True)).encode('utf-8')
J=JOIN.encode()
off=0; FL=[]
for p in T0b.split(J):
    idx=[i for i,c in enumerate(p) if 65<=c<=90 or 97<=c<=122]
    FL.append((off+idx[0], off+idx[-1]) if idx else None)
    off += len(p)+len(J)
cand=[i for i,f in enumerate(FL) if f]
def main():
    K=int(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1].isdigit() else 3
    from math import comb
    tot=sum(comb(len(cand),k) for k in range(1,K+1))
    print('base md5',hashlib.md5(T0b).hexdigest(),'paras',len(cand),'K',K,'TOTAL',tot,flush=True)
    t0=time.time(); n=0; last=t0; hits=0
    for k in range(1,K+1):
        for combo in itertools.combinations(cand,k):
            b=bytearray(T0b)
            for i in combo:
                a,z=FL[i]; b[a]^=0x20; b[z]^=0x20
            h=t._hit(b); n+=1
            if h:
                hits+=1
                print('*** HIT k=%d combo=%s addr=%s'%(k,combo,h[1]),flush=True)
                open(os.path.expanduser('~/unflip_HIT.txt'),'a').write(repr((k,combo,h))+'\n')
            now=time.time()
            if now-last>=10:
                last=now; r=n/max(now-t0,1e-9)
                print('  %d/%d %.0f/s ETA %.1f min'%(n,tot,r,(tot-n)/r/60),flush=True)
    print('DONE %d hits=%d %.1fs'%(n,hits,time.time()-t0))
if __name__=='__main__': main()
