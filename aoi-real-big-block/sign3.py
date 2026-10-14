#!/usr/bin/env python3
# sign3.py - RBB <=3 case-TOGGLE sweep over paragraph FIRST/LAST alpha positions.
# usage: sign3.py selftest | sign3.py debug | sign3.py run [jCRLF2|jCRLF|jLF2|jLF] [tNL|tCRLF]
import sys, os, hashlib, hmac, time
from multiprocessing import Pool, cpu_count

HOME=os.path.expanduser('~')
TARGET='14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W'
SUPER ='1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC'
B58='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
HARD=1<<31

def b58d(s):
    n=0
    for ch in s: n=n*58+B58.index(ch)
    b=n.to_bytes((n.bit_length()+7)//8,'big')
    return b'\x00'*(len(s)-len(s.lstrip('1')))+b
def b58e(p):
    n=int.from_bytes(p,'big'); s=''
    while n: n,r=divmod(n,58); s=B58[r]+s
    return '1'*(len(p)-len(p.lstrip(b'\x00')))+s
def b58check(p):
    return b58e(p+hashlib.sha256(hashlib.sha256(p).digest()).digest()[:4])
def h160(b):
    d=hashlib.sha256(b).digest()
    try: return hashlib.new('ripemd160',d).digest()
    except Exception: pass
    try:
        from Crypto.Hash import RIPEMD160
        x=RIPEMD160.new(); x.update(d); return x.digest()
    except Exception: pass
    from ripemd.ripemd160 import ripemd160
    return ripemd160(d)
TH=b58d(TARGET)[1:21]; SH=b58d(SUPER)[1:21]

_WL=None
def WL():
    global _WL
    if _WL: return _WL
    for fn in ('bip39.txt','bip39_english.txt','bip39-wordlist.txt'):
        p=os.path.join(HOME,fn)
        if os.path.exists(p):
            w=[x.strip() for x in open(p,encoding='utf-8') if x.strip()]
            if len(w)==2048: _WL=w; return w
    try:
        from mnemonic import Mnemonic; _WL=Mnemonic('english').wordlist; return _WL
    except Exception: pass
    raise SystemExit('need 2048-word bip39 list at ~/bip39.txt')

from coincurve import PublicKey
def _pub(k): return PublicKey.from_valid_secret(k.to_bytes(32,'big')).format(compressed=True)
def _mnem(ent):
    w=WL(); h=hashlib.sha256(ent).digest()
    bits=(int.from_bytes(ent,'big')<<4)|(h[0]>>4)
    return ' '.join(w[(bits>>(11*(11-i)))&2047] for i in range(12))
def derive(ent):
    seed=hashlib.pbkdf2_hmac('sha512',_mnem(ent).encode(),b'mnemonic',2048,64)
    I=hmac.new(b'Bitcoin seed',seed,hashlib.sha512).digest()
    k=int.from_bytes(I[:32],'big'); c=I[32:]
    for idx in (44|HARD,HARD,HARD):
        I=hmac.new(c,b'\x00'+k.to_bytes(32,'big')+idx.to_bytes(4,'big'),hashlib.sha512).digest()
        k=(k+int.from_bytes(I[:32],'big'))%N; c=I[32:]
    pub=_pub(k)
    I=hmac.new(c,pub+(0).to_bytes(4,'big'),hashlib.sha512).digest()
    k0=(k+int.from_bytes(I[:32],'big'))%N; c0=I[32:]
    pub0=_pub(k0)
    out=[]
    for i in range(6):
        Ii=hmac.new(c0,pub0+i.to_bytes(4,'big'),hashlib.sha512).digest()
        ki=(k0+int.from_bytes(Ii[:32],'big'))%N
        out.append((ki,h160(_pub(ki))))
    return out

def selftest():
    d=derive(bytes.fromhex('2941774a2abec9f30c7d6777d1d53d91'))
    wif=b58d('L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex')
    assert d[1][0].to_bytes(32,'big')==wif[1:33], 'entropy->WIF vector FAILED'
    a=b58check(b'\x00'+derive(bytes.fromhex('9dd2efb9bc976c2095bd534d7b8d431c'))[0][1])
    assert a=='19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN', 'Stage-1 md5 vector FAILED: '+a
    print('SELFTEST OK')

def _paras(b,sep=b'\n\n'):
    res=[];cur=[];i=0;n=len(b);L=len(sep)
    while i<n:
        if b[i:i+L]==sep: res.append(cur); cur=[]; i+=L
        else:
            if 65<=b[i]<=90 or 97<=b[i]<=122: cur.append(i)
            i+=1
    res.append(cur); return res

def _signpos(b,sep):
    pos=[]
    for u in _paras(b,sep):
        if not u: continue
        pos.append(u[0])
        if u[-1]!=u[0]: pos.append(u[-1])
    return pos

def _base(join,trail):
    import aoi
    aoi._init(); S=aoi._S; mask=0
    for i,ch in enumerate(S["letters"]):
        if ch not in set("itasm"): mask|=(1<<i)
    T0=aoi._text(mask,(join,trail,"lowerFirst",True))
    return T0,T0.encode('utf-8'),mask

_B=None;_POS=None
def _init(b,pos):
    global _B,_POS; _B=b; _POS=pos
def _hit(b):
    for ki,h in derive(hashlib.md5(b).digest()):
        if h==TH or h==SH: return (bytes(b), b58check(b'\x00'+h), hex(ki))
    return None
def _process(ui):
    B=_B; POS=_POS; L=len(POS); n=0; hits=[]
    i=POS[ui]
    b=bytearray(B); b[i]^=0x20
    h=_hit(b); n+=1
    if h: hits.append(h)
    for jj in range(ui+1,L):
        j=POS[jj]
        b=bytearray(B); b[i]^=0x20; b[j]^=0x20
        h=_hit(b); n+=1
        if h: hits.append(h)
        for kk in range(jj+1,L):
            b2=bytearray(b); b2[POS[kk]]^=0x20
            h=_hit(b2); n+=1
            if h: hits.append(h)
    return ui,n,hits

def debug():
    selftest()
    T0,T0b,mask=_base("\r\n\r\n","")
    POS=_signpos(T0b,b'\r\n\r\n')
    import aoi
    print('paras',len(aoi._S["paras"]),'sign positions',len(POS))
    print('base md5',hashlib.md5(T0b).hexdigest(),'bytes',len(T0b),'mask',mask)
    for p in POS[:24]:
        print(p, repr(chr(T0b[p])), repr(T0b[max(0,p-7):p+8]))

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'selftest'
    if mode=='selftest': selftest(); return
    if mode=='debug': debug(); return
    if mode!='run': raise SystemExit('usage: sign3.py selftest|debug|run [join] [trail]')
    join="\r\n\r\n" if "jCRLF2" in sys.argv else ("\r\n" if "jCRLF" in sys.argv else ("\n\n" if "jLF2" in sys.argv else ("\n" if "jLF" in sys.argv else "\r\n\r\n")))
    trail="\r\n" if "tCRLF" in sys.argv else ("\n" if "tNL" in sys.argv else "")
    jk="crlf2" if join=="\r\n\r\n" else "crlf" if join=="\r\n" else "lf2" if join=="\n\n" else "lf"
    tk="tcrlf" if trail=="\r\n" else "tnl" if trail=="\n" else "t0"
    tag=jk+"_"+tk
    T0,T0b,mask=_base(join,trail)
    print('base join=%r trail=%r tag=%s mask=%d chars=%d md5=%s'%(join,trail,tag,mask,len(T0),hashlib.md5(T0b).hexdigest()),flush=True)
    POS=_signpos(T0b,join.encode()); L=len(POS)
    total=L+L*(L-1)//2+L*(L-1)*(L-2)//6
    print('sign positions',L,'TOTAL',total,flush=True)
    print('ETA est %.1f min at 19k/s'%(total/19000/60),flush=True)
    dlog=os.path.join(HOME,'sign3_%s_done.log'%tag)
    done=set(int(x) for x in open(dlog)) if os.path.exists(dlog) else set()
    todo=[i for i in range(L) if i not in done]
    print('todo',len(todo),flush=True)
    f=open(dlog,'a'); t0=time.time(); cd=0; last=t0
    with Pool(cpu_count()-1,initializer=_init,initargs=(T0b,POS)) as pool:
        for ui,n,hits in pool.imap_unordered(_process,todo,chunksize=1):
            cd+=n; f.write('%d\n'%ui); f.flush()
            if hits:
                open(os.path.join(HOME,'sign3_FOUND.txt'),'a').write(repr(hits)+'\n')
                print('FOUND',hits,flush=True)
            now=time.time()
            if now-last>=10:
                last=now; r=cd/max(now-t0,1e-9)
                print('done %d/%d (%.3f%%) %.0f/s ETA %.1f min'%(cd,total,100*cd/total,r,(total-cd)/r/60 if r else 0),flush=True)
    print('END sign',cd,flush=True)

if __name__=='__main__': main()
