#!/usr/bin/env python3
# pidphrase.py - preimage search md5(S)=pid over multi-word quoted phrases.
# usage: pidphrase.py [maxwords]   (default 4)
import re, sys, os, html, hashlib, time, collections, itertools
from multiprocessing import Pool, cpu_count
HOME=os.path.expanduser('~')
PID='8b71bade9685d3388452bc4755b06a0d'; PIDB=bytes.fromhex(PID)
EXTRA="what wait huh hey why who how reverse Turing test turing humanity human humans artificial intelligence \
machine mean means meant think thought know knew say said ask asked tell told want need will would can could \
problem solution question answer thing things way ways time times again still just only even also too very \
really quite much many more most less least sure certain maybe perhaps course right wrong first second last \
next other another same different one two three".split()
raw=open(os.path.join(HOME,'wp_raw.html'),encoding='utf-8').read()
txt=html.unescape(re.sub(r'<[^>]+>','',raw))
vocab=[w for w,_ in collections.Counter(re.findall(r"[A-Za-z']+",txt.lower())).most_common(70)]
for w in EXTRA:
    if w.lower() not in vocab: vocab.append(w.lower())
VOCAB=sorted(set(vocab))
FIRST=['What','what','Wait','wait','Huh','huh','Hey','hey','Why','why','Who','who','How','how',
       'Wha','A','The','Is','Do','You','Are','So','Oh','Ah','No','Yes','Really','And','But','That','This']
OPEN=['"','\u201c',"'",'']
CLOSE=['?','?"','?\u201d','?!','!?','?!"','...','.','!','!"']
def gen(N):
    for n in range(1,N+1):
        for ws in itertools.product(VOCAB, repeat=n-1):
            tail=' '.join(ws)
            for f in FIRST:
                ph = f if not tail else f+' '+tail
                for o in OPEN:
                    for c in CLOSE: yield o+ph+c
def _chk(chunk):
    out=[]
    for s in chunk:
        if hashlib.md5(s.encode()).digest()==PIDB: out.append(s)
    return out
def chunks(it,size=200000):
    buf=[]
    for x in it:
        buf.append(x)
        if len(buf)>=size: yield buf; buf=[]
    if buf: yield buf
def main():
    N=int(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1].isdigit() else 4
    V=len(VOCAB)
    tot=sum(len(FIRST)*(V**(n-1))*len(OPEN)*len(CLOSE) for n in range(1,N+1))
    print('vocab',V,'maxwords',N,'TOTAL',tot,flush=True)
    t0=time.time(); n=0; last=t0
    with Pool(cpu_count()-1) as p:
        for r in p.imap_unordered(_chk, chunks(gen(N))):
            n+=200000
            for s in r: print('*** PID HIT',repr(s),flush=True)
            now=time.time()
            if now-last>=10:
                last=now; rate=n/max(now-t0,1e-9)
                print('  %d/%d %.0f/s ETA %.1f min'%(n,tot,rate,(tot-n)/rate/60),flush=True)
    print('DONE %d %.1fs'%(n,time.time()-t0))
if __name__=='__main__': main()
