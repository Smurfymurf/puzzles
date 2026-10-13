import hashlib, itertools, sys, os
from multiprocessing import Pool
PID="8b71bade9685d3388452bc4755b06a0d"
A=sys.argv[2].encode() if len(sys.argv)>2 else b"abcdefghijklmnopqrstuvwxyz "
MAXL=int(sys.argv[1]) if len(sys.argv)>1 else 7
def work(first):
    pre=bytes([first])
    for k in range(0,MAXL):
        for tail in itertools.product(A, repeat=k):
            if hashlib.md5(pre+bytes(tail)).hexdigest()==PID: return pre+bytes(tail)
    return None
if __name__=="__main__":
    with Pool(os.cpu_count()-1) as p:
        for r in p.map(work, list(A)):
            if r: print("FOUND", r)
    print("done")
