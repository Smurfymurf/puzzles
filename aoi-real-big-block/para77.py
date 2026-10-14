#!/usr/bin/env python3
# para77.py - splice candidate para-77 texts and check the ESCROWS (not the pid).
import os, sys, hashlib, time, itertools
import aoi, toggle2 as t
aoi._init()
P=aoi._S["paras"]; IDX=77
assert P[IDX]=='"What?"', P[IDX]
JOIN="\r\n\r\n"
ALPHA="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ?!.,;:'\"()-&/"
def build(X):
    le='\r\n'
    out=[]
    for i,p in enumerate(P):
        q = X if i==IDX else p
        fl=aoi._first_letter(q,True)
        if fl and fl not in 'itasm': q=aoi._flip(q,'lowerFirst')
        out.append(q.replace('\x00',le))
    return JOIN.join(out)
def gen():
    base='"What?"'
    C=set([base])
    # case variants + quote/punct/ws decorations
    for m in range(1<<4):
        w=''.join(ch.upper() if (m>>i)&1 else ch.lower() for i,ch in enumerate('What'))
        for o in ('"','\u201c',"'",''):
            for c in ('?','?"','?\u201d','?!','!?','.','!','...'):
                for pre in ('',' ','\n','\t'):
                    for post in ('',' ','\n','\t'):
                        C.add(pre+o+w+c+post)
    # edit distance <=2 over ALPHA
    cur=set([base])
    allc=set([base])
    for _ in range(2):
        nxt=set()
        for s in cur:
            for i in range(len(s)):
                for ch in ALPHA:
                    if ch!=s[i]: nxt.add(s[:i]+ch+s[i+1:])
            for i in range(len(s)+1):
                for ch in ALPHA: nxt.add(s[:i]+ch+s[i:])
            for i in range(len(s)): nxt.add(s[:i]+s[i+1:])
        nxt-=allc; allc|=nxt; cur=nxt
    C|=allc
    return C
def main():
    C=gen()
    print('candidates',len(C),flush=True)
    t0=time.time(); n=0; last=t0; hits=0
    for X in C:
        T=build(X).encode('utf-8')
        h=t._hit(T); n+=1
        if h:
            hits+=1
            print('*** HIT', repr(X), h[1], flush=True)
            open(os.path.expanduser('~/para77_HIT.txt'),'a').write(repr((X,h))+'\n')
        now=time.time()
        if now-last>=10:
            last=now; r=n/max(now-t0,1e-9)
            print('  %d/%d %.0f/s ETA %.1f min'%(n,len(C),r,(len(C)-n)/r/60),flush=True)
    print('DONE %d hits=%d %.1fs'%(n,hits,time.time()-t0))
if __name__=='__main__': main()
