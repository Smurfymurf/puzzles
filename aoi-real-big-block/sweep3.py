import hashlib, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.expanduser('~/puzzles/aoi-real-big-block'))
import aoi
from mnemonic import Mnemonic
MN = Mnemonic('english')
TGT    = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
STAGE1 = '19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN'
LE = '\r\n'; JOIN = '\r\n\r\n'
MODE = os.environ.get('BASE_MODE', 'raw')
aoi._init(); P = aoi._S['paras']
def fa(p):
    for c in p:
        if c.isalpha(): return c.lower()
    return '.'
def flip(p):
    q = list(p)
    for j,c in enumerate(q):
        if c.isalpha(): q[j] = c.lower(); break
    for j in range(len(q)-1,-1,-1):
        if q[j].isalpha(): q[j] = q[j].upper(); break
    return ''.join(q)
CERT = set(i for i,p in enumerate(P) if fa(p) not in ('a','i','m','s','t'))
BASE = [(flip(p.replace('\x00',LE)) if (MODE=='cert' and i in CERT) else p.replace('\x00',LE))
        for i,p in enumerate(P)]
N = len(BASE)
def ia(s, rev=False):
    for j in (range(len(s)-1,-1,-1) if rev else range(len(s))):
        if s[j].isalpha(): return j
FI = [ia(p) for p in BASE]; LI = [ia(p, True) for p in BASE]
SINGLES = [(i,j) for i,p in enumerate(BASE) for j,ch in enumerate(p) if ch.isalpha()]
def check(t):
    e = hashlib.md5(t.encode()).digest(); m = MN.to_mnemonic(e)
    seed = hashlib.pbkdf2_hmac('sha512', m.encode(), b'mnemonic', 2048, 64)
    for k in range(6):
        a = aoi.bip44_address(seed, k)
        if a == TGT:    return ('ESCROW', k)
        if a == STAGE1: return ('STAGE1', k)
    return None
def run1(a):
    i,j = a; q = list(BASE[i]); q[j] = q[j].swapcase(); ps = BASE[:]; ps[i] = ''.join(q)
    r = check(JOIN.join(ps)); return ('single', i, j, r) if r else None
def run2(a):
    w,i,j = a
    pos = [(i,FI[i],'l'),(j,LI[j],'u')] if w=='fl' else [(i,FI[i],'l'),(j,FI[j],'l')] if w=='ff' else [(i,LI[i],'u'),(j,LI[j],'u')]
    ps = BASE[:]
    for pi,pp,mode in pos:
        if pp is None: continue
        q = list(ps[pi]); q[pp] = q[pp].lower() if mode=='l' else q[pp].upper(); ps[pi] = ''.join(q)
    r = check(JOIN.join(ps)); return (w, i, j, r) if r else None
def main():
    b = JOIN.join(BASE)
    print(f'### MODE={MODE}  base md5={hashlib.md5(b.encode()).hexdigest()}')
    seed = hashlib.pbkdf2_hmac('sha512', MN.to_mnemonic(hashlib.md5(b.encode()).digest()).encode(), b'mnemonic', 2048, 64)
    print('   addr0..5', [aoi.bip44_address(seed, k) for k in range(6)])
    print('   singles', len(SINGLES)); t0 = time.time()
    with Pool(8) as pool:
        for n,r in enumerate(pool.imap_unordered(run1, SINGLES, chunksize=64),1):
            if r: print('   *** HIT', r)
    print('   single done', round(time.time()-t0))
    pairs = [(w,i,j) for w in ('fl','ff','ll') for i in range(N) for j in range(i,N)]
    t0 = time.time()
    with Pool(8) as pool:
        for n,r in enumerate(pool.imap_unordered(run2, pairs, chunksize=32),1):
            if r: print('   *** HIT', r)
    print('   pair done', round(time.time()-t0))
if __name__ == '__main__': main()
