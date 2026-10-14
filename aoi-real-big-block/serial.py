#!/usr/bin/env python3
# serial.py - exhaustive sweep of every serialisation/rule choice around the certified base.
import re, os, html, hashlib, time
import aoi, toggle2 as t
HOME=os.path.expanduser('~')
RAW=open(os.path.join(HOME,'wp_raw.html'),encoding='utf-8').read()
PS=re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>', RAW, re.S)
aoi._init()
BR   = ['', '\n', '\r\n', ' ', '\r\n\r\n']
TAG  = ['strip','keep']
JOIN = ['\r\n\r\n','\n\n','\r\n','\n']
TRAIL= ['', '\n', '\r\n']
LEAD = ['', '\n', '\r\n']
SW   = [True, False]
EMP  = [True, False]
RULE = [True, False]
ENT  = ['dec','raw']
SQ   = [True, False]

def build(br,tag,join,trail,lead,sw,emp,rule,ent,sq):
    le = '\r\n' if '\r' in join else '\n'
    parts=[]
    for pid,c in PS:
        s = re.sub(r'<br\s*/?>', '\x01', c)
        if tag=='strip': s = re.sub(r'<[^>]+>','', s)
        s = s.replace('\x01', br)
        if ent=='dec': s = html.unescape(s)
        if sw: s = s.strip()
        if (not emp) and s=='': continue
        if rule:
            fl = aoi._first_letter(s, sq)
            if fl and fl not in 'itasm': s = aoi._flip(s,'lowerFirst')
        parts.append(s.replace('\x00', le))
    return lead + join.join(parts) + trail

def main():
    combos=list(__import__('itertools').product(BR,TAG,JOIN,TRAIL,LEAD,SW,EMP,RULE,ENT,SQ))
    print('combos',len(combos),flush=True)
    t0=time.time(); n=0; hit=0
    for cb in combos:
        T=build(*cb).encode('utf-8')
        hs=t.derive(hashlib.md5(T).digest())
        addrs=[t.b58check(b'\x00'+h) for _,h in hs]
        m=[a for a in addrs if a in (t.TARGET,t.SUPER)]
        n+=1
        if m:
            hit+=1
            print('*** HIT', m, 'md5=%s'%hashlib.md5(T).hexdigest(), dict(zip(
                'br tag join trail lead strip empty rule ent skipq'.split(), map(repr,cb))), flush=True)
        if n%1500==0:
            r=n/max(time.time()-t0,1e-9)
            print('  %d/%d %.0f/s ETA %.1f min'%(n,len(combos),r,(len(combos)-n)/r/60),flush=True)
    print('DONE %d combos, %d hits, %.1fs'%(n,hit,time.time()-t0))

if __name__=='__main__': main()
