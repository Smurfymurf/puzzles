#!/usr/bin/env python3
# toggle2.py - RBB case-TOGGLE sweep. modes: selftest | debug | word | para | all
#   word [K] : <=K toggles inside one word (default K=4)
import sys, os, json, hashlib, hmac, time
from math import comb
from itertools import combinations
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
    try:
        from bip_utils import Bip39WordsListGetter, Bip39Languages
        try: _WL=list(Bip39WordsListGetter(Bip39Languages.ENGLISH).GetList())
        except Exception: _WL=list(Bip39WordsListGetter.GetBip39WordsListByLanguage(Bip39Languages.ENGLISH))
        return _WL
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
        pk=_pub(ki)
        out.append((ki,h160(pk)))
    return out

def selftest():
    d=derive(bytes.fromhex('2941774a2abec9f30c7d6777d1d53d91'))
    wif=b58d('L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex')
    assert d[1][0].to_bytes(32,'big')==wif[1:33], 'entropy->WIF vector FAILED'
    for ki,h in d: assert h160(_pub(ki))==h, 'pub/priv mismatch'
    a=b58check(b'\x00'+derive(bytes.fromhex('9dd2efb9bc976c2095bd534d7b8d431c'))[0][1])
    assert a=='19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN', 'Stage-1 md5 vector FAILED: '+a
    print('SELFTEST OK')

def load_canonical():
    c=[]
    for fn in ('second.json','aoi_paras.json','second.txt','aoi_text.txt'):
        p=os.path.join(HOME,fn)
        if not os.path.exists(p): continue
        if fn.endswith('.json'):
            j=json.load(open(p,encoding='utf-8'))
            if isinstance(j,str): c.append(j)
            elif isinstance(j,list) and all(isinstance(x,str) for x in j): c.append('\n\n'.join(j)+'\n')
        else: c.append(open(p,encoding='utf-8').read())
    for t in c:
        if len(t)==45451: return t
    if c: return c[0]
    raise SystemExit('no canonical source')

def rule(text):
    out=[]
    for p in text.split('\n\n'):
        idx=[i for i,ch in enumerate(p) if ch.isalpha()]
        if idx and p[idx[0]] not in 'ITASM':
            f,l=idx[0],idx[-1]
            if f==l: p=p[:f]+p[f].upper()+p[f+1:]
            else:
                p=p[:f]+p[f].lower()+p[f+1:]
                p=p[:l]+p[l].upper()+p[l+1:]
        out.append(p)
    return '\n\n'.join(out)

def _alpha(b): return [i for i,ch in enumerate(b) if 65<=ch<=90 or 97<=ch<=122]
def _words(b):
    ws=[];cur=[]
    for i,ch in enumerate(b):
        if 65<=ch<=90 or 97<=ch<=122: cur.append(i)
        elif cur: ws.append(cur); cur=[]
    if cur: ws.append(cur)
    return ws
def _paras(b,sep=b'\n\n'):
    res=[];cur=[];i=0;n=len(b);L=len(sep)
    while i<n:
        if b[i:i+L]==sep: res.append(cur); cur=[]; i+=L
        else:
            if 65<=b[i]<=90 or 97<=b[i]<=122: cur.append(i)
            i+=1
    res.append(cur); return res

_B=None;_POS=None;_MODE=None;_UNITS=None;_K=4
def _init(b,pos,mode,units,K):
    global _B,_POS,_MODE,_UNITS,_K; _B=b;_POS=pos;_MODE=mode;_UNITS=units;_K=K
def _hit(b):
    for ki,h in derive(hashlib.md5(b).digest()):
        if h==TH or h==SH: return (bytes(b), b58check(b'\x00'+h), hex(ki))
    return None
def _process(ui):
    B=_B; n=0; hits=[]
    if _MODE=='all':
        pi=_POS[ui]; L=len(_POS)
        for j in range(ui+1,L):
            b=bytearray(B); b[pi]^=0x20; b[_POS[j]]^=0x20
            h=_hit(b); n+=1
            if h: hits.append(h)
    else:
        unit=_UNITS[ui]
        if _MODE=='para':
            for poss in unit:
                b=bytearray(B)
                for p in poss: b[p]^=0x20
                h=_hit(b); n+=1
                if h: hits.append(h)
        else:
            L=len(unit)
            for k in range(1,min(_K,L)+1):
                for c in combinations(unit,k):
                    b=bytearray(B)
                    for p in c: b[p]^=0x20
                    h=_hit(b); n+=1
                    if h: hits.append(h)
    return ui,n,hits

def debug():
    selftest()
    e=bytes.fromhex('9dd2efb9bc976c2095bd534d7b8d431c')
    print('STAGE1 md5 idx0..5:', [b58check(b'\x00'+h) for _,h in derive(e)])
    T0=rule(load_canonical())
    print('T0 chars',len(T0),'bytes',len(T0.encode()))
    print('T0 (no toggle) idx0..5:', [b58check(b'\x00'+h) for _,h in derive(hashlib.md5(T0.encode()).digest())])
    print('TARGET', TARGET, '| SUPER', SUPER)

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'selftest'
    if mode=='selftest': selftest(); return
    if mode=='debug': debug(); return
    K=next((int(a) for a in sys.argv[2:] if a.isdigit()),4)
    import aoi
    aoi._init(); _S=aoi._S; _mask=0
    for _i,_ch in enumerate(_S["letters"]):
        if _ch not in set("itasm"): _mask|=(1<<_i)
    _join = "\r\n\r\n" if "jCRLF2" in sys.argv else ("\r\n" if "jCRLF" in sys.argv else ("\n\n" if "jLF2" in sys.argv else ("\n" if "jLF" in sys.argv else "\r\n\r\n")))
    _trail = "\r\n" if "tCRLF" in sys.argv else ("\n" if "tNL" in sys.argv else "")
    _jk = "crlf2" if _join=="\r\n\r\n" else "crlf" if _join=="\r\n" else "lf2" if _join=="\n\n" else "lf"
    _tk = "tcrlf" if _trail=="\r\n" else "tnl" if _trail=="\n" else "t0"
    _tag = _jk+"_"+_tk
    T0=aoi._text(_mask,(_join,_trail,"lowerFirst",True)); T0b=T0.encode('utf-8')
    print('base join=%r trail=%r tag=%s mask=%d chars=%d md5=%s'%(_join,_trail,_tag,_mask,len(T0),hashlib.md5(T0b).hexdigest()),flush=True)
    print('T0 chars',len(T0),'bytes',len(T0b),flush=True)
    pos=_alpha(T0b)
    if mode=='all':
        units=pos; total=len(pos)*(len(pos)-1)//2
    elif mode=='para':
        units=[list(combinations(u,2)) for u in _paras(T0b,_join.encode()) if len(u)>=2]; total=sum(len(u) for u in units)
    elif mode=='word':
        units=[u for u in _words(T0b) if len(u)>=2]
        total=sum(sum(comb(len(u),k) for k in range(1,min(K,len(u))+1)) for u in units)
    else: raise SystemExit('mode?')
    print('mode',mode,'K',K,'units',len(units),'TOTAL',total,flush=True)
    dlog=os.path.join(HOME,'toggle2_%s_%s_done.log'%(mode,_tag))
    done=set(int(x) for x in open(dlog)) if os.path.exists(dlog) else set()
    todo=[i for i in range(len(units)) if i not in done]
    print('todo',len(todo),flush=True)
    f=open(dlog,'a'); t0=time.time(); cd=0; last=t0
    with Pool(cpu_count()-1,initializer=_init,initargs=(T0b,pos,mode,units,K)) as pool:
        for ui,n,hits in pool.imap_unordered(_process,todo,chunksize=1):
            cd+=n; f.write('%d\n'%ui); f.flush()
            if hits:
                open(os.path.join(HOME,'toggle2_FOUND.txt'),'a').write(repr(hits)+'\n')
                print('FOUND',hits,flush=True)
            now=time.time()
            if now-last>=15:
                last=now; r=cd/max(now-t0,1e-9)
                print('done %d/%d (%.3f%%) %.0f/s ETA %.1f min'%(cd,total,100*cd/total,r,(total-cd)/r/60 if r else 0),flush=True)
    print('END',mode,'candidates',cd,flush=True)

if __name__=='__main__': main()
