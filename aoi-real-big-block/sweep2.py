import hashlib, os, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.expanduser('~/puzzles/aoi-real-big-block'))
import aoi
from mnemonic import Mnemonic

MN = Mnemonic('english')
TGT    = '14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'          # ESCROW
STAGE1 = '19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN'          # STAGE1
LE = '\r\n'; JOIN = '\r\n\r\n'

aoi._init()
P = aoi._S['paras']
BASE = [p.replace('\x00', LE) for p in P]
N = len(BASE)
def ia(s, rev=False):
    for j in (range(len(s)-1,-1,-1) if rev else range(len(s))):
        if s[j].isalpha(): return j
FI = [ia(p) for p in BASE]; LI = [ia(p, True) for p in BASE]
SINGLES = [(i,j) for i,p in enumerate(BASE) for j,ch in enumerate(p) if ch.isalpha()]

def check(t):
    e = hashlib.md5(t.encode()).digest(); m = MN.to_mnemonic(e)
    seed = hashlib.pbkdf2_hmac('sha512', m.encode(), b'mnemonic', 2048, 64)
    for k in range(3):
        a = aoi.bip44_address(seed, k)
        if a == TGT:    return ('ESCROW', k)
        if a == STAGE1: return ('STAGE1', k)
    return None

def run1(a):
    i,j = a
    q = list(BASE[i]); q[j] = q[j].swapcase()
    ps = BASE[:]; ps[i] = ''.join(q)
    r = check(JOIN.join(ps))
    return ('single', i, j, r) if r else None

def run2(a):
    which,i,j = a
    pos = [(i,FI[i],'l'),(j,LI[j],'u')] if which=='fl' else \
          [(i,FI[i],'l'),(j,FI[j],'l')] if which=='ff' else [(i,LI[i],'u'),(j,LI[j],'u')]
    ps = BASE[:]
    for pi,pp,mode in pos:
        if pp is None: continue
        q = list(ps[pi]); q[pp] = q[pp].lower() if mode=='l' else q[pp].upper(); ps[pi] = ''.join(q)
    r = check(JOIN.join(ps))
    return (which, i, j, r) if r else None

def diag():
    src = open(os.path.expanduser('~/puzzles/aoi-real-big-block/mask2.py')).read()
    for key in ('def addr','def our','def _addr','bip44','def derive'):
        i = src.find(key)
        if i >= 0:
            print('--- mask2:', key, '---'); print(src[i:i+600]); break
    base = JOIN.join(BASE)
    print('base md5', hashlib.md5(base.encode()).hexdigest())
    seed = hashlib.pbkdf2_hmac('sha512', MN.to_mnemonic(hashlib.md5(base.encode()).digest()).encode(), b'mnemonic', 2048, 64)
    print('base addr 0..5 (aoi):', [aoi.bip44_address(seed, k) for k in range(6)])
    print('STAGE1?', STAGE1 in [aoi.bip44_address(seed, k) for k in range(6)])

def main():
    print('singles', len(SINGLES))
    print('=== single sweep ==='); t0 = time.time()
    with Pool(8) as pool:
        for n,r in enumerate(pool.imap_unordered(run1, SINGLES, chunksize=64),1):
            if r: print('*** HIT', r)
            if n % 20000 == 0: print(f'  {n}/{len(SINGLES)} {n/(time.time()-t0):.0f}/s')
    print('single done', round(time.time()-t0))
    pairs = [(w,i,j) for w in ('fl','ff','ll') for i in range(N) for j in range(i,N)]
    print('=== pair sweep ===', len(pairs)); t0 = time.time()
    with Pool(8) as pool:
        for n,r in enumerate(pool.imap_unordered(run2, pairs, chunksize=32),1):
            if r: print('*** HIT', r)
            if n % 40000 == 0: print(f'  {n}/{len(pairs)} {n/(time.time()-t0):.0f}/s')
    print('pair done', round(time.time()-t0))

if __name__ == '__main__':
    diag(); main()
