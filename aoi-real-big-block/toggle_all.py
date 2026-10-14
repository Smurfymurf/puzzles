import hashlib, hmac, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.expanduser('~/puzzles/aoi-real-big-block'))
import aoi
from mnemonic import Mnemonic
MN = Mnemonic('english'); W = MN.wordlist
TGT='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'; PRE='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'; S1='19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN'
LE='\r\n'; JOIN='\r\n\r\n'; H=os.path.expanduser('~')
MODE=os.environ.get('TMODE','pairs')
DONE=os.path.join(H,'toggle_all_done.log'); FOUND=os.path.join(H,'toggle_all_FOUND.txt')
aoi._init(); P=aoi._S['paras']
def fa(p):
    for c in p:
        if c.isalpha(): return c.lower()
    return '.'
def flip(p):
    q=list(p)
    for j,c in enumerate(q):
        if c.isalpha(): q[j]=c.lower(); break
    for j in range(len(q)-1,-1,-1):
        if q[j].isalpha(): q[j]=q[j].upper(); break
    return ''.join(q)
CERT=set(i for i,p in enumerate(P) if fa(p) not in ('a','i','m','s','t'))
TXT=JOIN.join(flip(p.replace('\x00',LE)) if i in CERT else p.replace('\x00',LE) for i,p in enumerate(P))
TB=bytearray(TXT.encode())
POS=[j for j,b in enumerate(TB) if chr(b).isalpha()]
N=len(POS)
ALPHA=[ord(c) for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ']
def mnem(d):
    x=(int.from_bytes(d,'big')<<4)|(hashlib.sha256(d).digest()[0]>>4)
    return ' '.join(W[(x>>(11*(11-i)))&2047] for i in range(12))
def hit(seed):
    d=hmac.new(b"Bitcoin seed",seed,hashlib.sha512).digest()
    k,c=int.from_bytes(d[:32],'big'),d[32:]
    for i in (44,0,0): k,c=aoi._child(k,c,i,True)
    k,c=aoi._child(k,c,0,False)
    for idx in range(6):
        kk,_=aoi._child(k,c,idx,False)
        a=aoi.b58check(b'\x00'+aoi.hash160(aoi._pub(kk.to_bytes(32,'big'),True)))
        if a in (TGT,PRE,S1): return idx,a
    return None
def run(buf):
    d=hashlib.md5(bytes(buf)).digest()
    return hit(hashlib.pbkdf2_hmac('sha512', mnem(d).encode(), b'mnemonic',2048,64))
def work_sub(a):
    p,rep=a; buf=bytearray(TB); buf[p]=rep
    r=run(buf)
    if r:
        with open(FOUND,'a') as f: f.write(f'sub {p} {rep} {r[0]} {r[1]}\n')
        print('*** FOUND sub',p,rep,r,flush=True)
    return p
def work_pair(i):
    buf=bytearray(TB)
    for jj in range(i+1,N):
        a,b=POS[i],POS[jj]; buf[a]^=0x20; buf[b]^=0x20
        r=run(buf)
        if r:
            with open(FOUND,'a') as f: f.write(f'pair {i} {jj} {a} {b} {r[0]} {r[1]}\n')
            print('*** FOUND pair',i,jj,r,flush=True)
        buf[a]^=0x20; buf[b]^=0x20
    with open(DONE,'a') as f: f.write(f'{i}\n')
    return i
def main():
    if MODE=='subs':
        tasks=[(p,c) for p in POS for c in ALPHA if c!=TB[p]]
        print('subs',len(tasks),flush=True); t0=time.time()
        with Pool(23) as pool:
            for n,_ in enumerate(pool.imap_unordered(work_sub,tasks,chunksize=128),1):
                if n%300000==0: print(f'  {n}/{len(tasks)} {n/(time.time()-t0):.0f}/s',flush=True)
        print('subs DONE',round(time.time()-t0),flush=True); return
    done=set()
    if os.path.exists(DONE): done={int(x) for x in open(DONE) if x.strip()}
    todo=[i for i in range(N) if i not in done]
    print(f'pairs todo={len(todo)} total_pairs={sum(N-1-i for i in todo)}',flush=True)
    t0=time.time(); c=0
    with Pool(23) as pool:
        for _ in pool.imap_unordered(work_pair,todo,chunksize=1):
            c+=1
            if c%200==0:
                el=time.time()-t0
                print(f'  i {c}/{len(todo)} {c/el:.2f} i/s ETA {(len(todo)-c)/(c/el)/3600:.2f}h',flush=True)
    print('pairs DONE',flush=True)
if __name__=='__main__': main()
