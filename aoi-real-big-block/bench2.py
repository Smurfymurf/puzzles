import time, os, sys
from multiprocessing import Pool
import toggle2 as t
def work(chunk, B):
    n=0
    for p1,p2 in chunk:
        b=bytearray(B); b[p1]^=0x20; b[p2]^=0x20
        t._hit(b); n+=1
    return n
if __name__=='__main__':
    W=int(sys.argv[1]) if len(sys.argv)>1 else os.cpu_count()-1
    B=t.rule(t.load_canonical()).encode()
    pos=t._alpha(B)[:400]
    pairs=[(pos[i],pos[j]) for i in range(len(pos)) for j in range(i+1,len(pos))]
    CH=1000
    chunks=[pairs[k:k+CH] for k in range(0,len(pairs),CH)]
    t0=time.time()
    with Pool(W) as pool:
        tot=sum(pool.starmap(work,[(c,B) for c in chunks]))
    dt=time.time()-t0
    print('workers %d  candidates %d  %.1fs  aggregate %.0f/s  per-worker %.0f/s'%(W,tot,dt,tot/dt,tot/dt/W))
