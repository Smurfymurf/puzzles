#!/usr/bin/env python3
# entbase.py - test HTML-entity-encoded bases (the live page's own form) against both escrows.
import re, os, html, hashlib
import aoi, toggle2 as t
HOME=os.path.expanduser('~')
raw=open(os.path.join(HOME,'wp_raw.html'),encoding='utf-8').read()
ps=re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>', raw, re.S)
P=[html.unescape(re.sub(r'<[^>]+>','',c)) for _,c in ps]
P=[p for p in P if p.strip()]
print('paras',len(P))
aoi._init()

def enc(s,q,a):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"',q).replace("'",a)

def ruled(p, encode_first, q, a):
    if encode_first: p=enc(p,q,a)
    fl=aoi._first_letter(p,True)
    if fl and fl not in 'itasm': p=aoi._flip(p,'lowerFirst')
    if not encode_first: p=enc(p,q,a)
    return p

def build(encode_first,q,a,join,trail):
    le='\r\n' if '\r' in join else '\n'
    return join.join(ruled(p.replace('\x00',le),encode_first,q,a) for p in P)+trail

for q,a in (('&quot;','&apos;'),('&#34;','&#39;'),('&quot;','&#39;'),('&#x22;','&#x27;')):
    for ef in (True,False):
        for jn,j in (('crlf2','\r\n\r\n'),('crlf','\r\n'),('lf2','\n\n')):
            for tr in ('','\r\n'):
                T=build(ef,q,a,j,tr).encode('utf-8')
                hs=t.derive(hashlib.md5(T).digest())
                addrs=[t.b58check(b'\x00'+h) for _,h in hs]
                hit=[x for x in addrs if x in (t.TARGET,t.SUPER)]
                print('%-9s enc_first=%-5s join=%-5s trail=%-4r md5=%s %s'%(q,ef,jn,tr,hashlib.md5(T).hexdigest(),('*** HIT '+str(hit)) if hit else ''),flush=True)
