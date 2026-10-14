#!/usr/bin/env python3
import hashlib, itertools, os, time, multiprocessing as mp, threading
T = "8b71bade9685d3388452bc4755b06a0d"
V = ["what","whats","is","are","a","an","the","that","this","it","you","do","does","mean",
     "how","why","so","then","and","of","to","in","for","about","exactly","really","now",
     "turing","test","reverse","artificial","intelligence","human","humanity","singularity",
     "pass","fail","adopt","solution","problem","ways","make","sure","adoption","opportunity",
     "use","will","i","am","no","big","deal","already","familiar","most","one","back","mirror",
     "fun","experiment","know","course","oh","well","ok","okay","huh","say","again","wait"]
V = sorted(set(V))
SEP = [" ", ", "]
WRAP = [('"','?"'), ('"','"'), ('"','!'), ('','?')]
NW = max(1,(os.cpu_count() or 2)-1)
DONE  = os.path.expanduser("~/x12b_done.log")
FOUND = os.path.expanduser("~/x12b_FOUND.txt")
TOTAL = sum((len(V)*len(SEP))**L for L in range(5)) * len(V)
CTR = None

def _init(c):
    global CTR; CTR = c

def _work(first):
    ident = mp.current_process()._identity
    slot = ((ident[0]-1) % NW) if ident else 0
    pend = 0; found = None
    for L in range(1, 6):
        for combo in itertools.product(V, repeat=L-1):
            words = (first,) + combo
            for seps2 in itertools.product(SEP, repeat=L-1):
                inner = words[0] + "".join(s+w for s,w in zip(seps2, words[1:]))
                cap = inner[0].upper() + inner[1:]
                for q1,q2 in WRAP:
                    if hashlib.md5((q1+cap+q2).encode()).hexdigest() == T:
                        found = q1+cap+q2; break
                pend += 1
                if pend >= 100000: CTR[slot] += pend; pend = 0
                if found: break
            if found: break
        if found: break
    CTR[slot] += pend
    return (first, found)

def _progress(t0):
    while True:
        time.sleep(15)
        done = sum(CTR); el = time.time()-t0
        rate = done/el if el else 0
        eta = (TOTAL-done)/rate/60 if rate>0 else 0
        print("done %d/%d  %.3f%%  %.2e it/s  eta %.0f min" % (done, TOTAL, 100.0*done/TOTAL, rate, eta), flush=True)

def main():
    global CTR
    CTR = mp.Array('q', NW)
    seen = set(x for x in open(DONE).read().splitlines() if x) if os.path.exists(DONE) else set()
    todo = [f for f in V if f not in seen]
    print("firsts %d todo %d workers %d TOTAL %d" % (len(V), len(todo), NW, TOTAL), flush=True)
    if not todo: print("nothing to do"); return
    t0 = time.time()
    threading.Thread(target=_progress, args=(t0,), daemon=True).start()
    with mp.Pool(NW, initializer=_init, initargs=(CTR,)) as pool:
        for first, res in pool.imap_unordered(_work, todo, chunksize=1):
            with open(DONE, "a") as fh: fh.write(first+"\n")
            if res:
                print("FOUND", repr(res), flush=True)
                with open(FOUND, "a") as fh: fh.write(repr(res)+"\n")
    print("done", flush=True)

if __name__ == "__main__":
    main()
