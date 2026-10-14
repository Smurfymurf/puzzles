#!/usr/bin/env python3
import hashlib, itertools, os, time, multiprocessing as mp, threading
PID = "8b71bade9685d3388452bc4755b06a0d"
DONE  = os.path.expanduser("~/x_what2_done.log")
FOUND = os.path.expanduser("~/x_what2_FOUND.txt")
CTR = None

def _init(c):
    global CTR; CTR = c

def case_variants(w):
    return {''.join(cs) for cs in itertools.product(
        *[(c.lower(),c.upper()) if c.isalpha() else (c,) for c in w])}
def flip(t):
    idx=[i for i,ch in enumerate(t) if ch.isalpha()]
    if len(idx)<2: return t
    L=list(t); L[idx[0]]=L[idx[0]].lower(); L[idx[-1]]=L[idx[-1]].upper(); return ''.join(L)

bases=["what","what?","what!","what.","what..","what...","what?!","what!?","what??",
 "what now","what now?","what is it","what is it?","what is this","what is this?",
 "what is going on","what is going on?","what happened","what happened?",
 "what do you mean","what do you mean?","what did you say","what did you say?",
 "what are you doing","what are you doing?","what the","what the?","what the...",
 "what's going on","what's going on?","what's this","what's this?",
 "huh","huh?","so what","so what?","what for","what for?"]
words=set()
for b in bases: words |= case_variants(b)
words=sorted(words)

pre =["", '"', "'", "\u201c", "\u2018", "(", " "]
post=["", '"', "'", "\u201d", "\u2019", ")", " ", "\n"]
S=['?','!','.','"',"'",' ',"\u00a0",'-','_','*','~','(',')',':',';',',']
suf2=sorted({a+b for a in ['']+S for b in ['']+S})

NW=max(1,(os.cpu_count() or 2)-1)
TOTAL=len(words)*len(pre)*len(post)*len(suf2)

def work(w):
    ident=mp.current_process()._identity
    slot=((ident[0]-1)%NW) if ident else 0
    n=0
    if hashlib.md5(w.encode()).hexdigest()==PID: return (w,w)
    for p in pre:
        for q in post:
            for s in suf2:
                c=p+w+q+s
                if hashlib.md5(c.encode()).hexdigest()==PID: return (w,c)
                f=flip(c)
                if f!=c and hashlib.md5(f.encode()).hexdigest()==PID: return (w,f)
                n+=1
                if n>=20000: CTR[slot]+=n; n=0
    CTR[slot]+=n
    return (w,None)

def prog(t0):
    while True:
        time.sleep(10)
        d=sum(CTR); el=time.time()-t0; r=d/el if el else 0
        print("done %d/%d %.2f%% %.2e/s eta %.1f min"%(d,TOTAL,100*d/TOTAL,r,(TOTAL-d)/r/60 if r else 0),flush=True)

def main():
    global CTR
    CTR=mp.Array('q',NW)
    seen=set(x for x in open(DONE).read().splitlines() if x) if os.path.exists(DONE) else set()
    todo=[w for w in words if w not in seen]
    print("words %d todo %d TOTAL %d workers %d"%(len(words),len(todo),TOTAL,NW),flush=True)
    if not todo: print("nothing to do"); return
    t0=time.time(); threading.Thread(target=prog,args=(t0,),daemon=True).start()
    with mp.Pool(NW, initializer=_init, initargs=(CTR,)) as pool:
        for w,r in pool.imap_unordered(work,todo,chunksize=64):
            with open(DONE,"a") as fh: fh.write(w+"\n")
            if r:
                print("FOUND",repr(r),flush=True)
                with open(FOUND,"a") as fh: fh.write(repr(r)+"\n")
    print("done",flush=True)

if __name__=="__main__": main()
