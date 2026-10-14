#!/usr/bin/env python3
# pidrule.py - is a wrong pid md5(content + <counter>)?  Numeric brute force.
import re, html, hashlib, urllib.request, json, collections
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
STORY=184148284
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def dec(c): return html.unescape(re.sub(r'<[^>]+>','',c))
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()

def main():
    ids=[p['id'] for p in json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))['parts']]
    rows=[]
    for cid in ids:
        try: t=get('https://www.wattpad.com/amp/%d'%cid)
        except: continue
        for idx,(pid,c) in enumerate(paras(t)): rows.append((cid,idx,pid,c,dec(c)))
    # collect: for each (content) the ordered list of (cid,idx,pid)
    g=collections.defaultdict(list)
    for cid,idx,pid,c,s in rows: g[s].append((cid,idx,pid))
    print('=== duplicate groups: occurrence k -> pid, and does md5(s+str(k)) match? ===')
    for s,v in g.items():
        if len(v)<3: continue
        for k,(cid,idx,pid) in enumerate(v,1):
            print('  %-14r k=%d cid=%d idx=%d pid=%s  md5(s+str(k))=%s  md5(s+str(idx))=%s'%(
                s[:14],k,cid,idx,pid[:10],md5(s+str(k))[:10],md5(s+str(idx))[:10]))
        break
    # target + a few: numeric brute force
    print('=== numeric suffix/prefix brute force (len 1..7) ===')
    def brute(pid,base):
        for L in range(1,8):
            for n in range(10**L//10**(L-1)*1, 10**L):
                x=str(n)
                if md5(base+x)==pid: return 'suffix '+x
                if md5(x+base)==pid: return 'prefix '+x
        return None
    T='8b71bade9685d3388452bc4755b06a0d'
    for cid,idx,pid,c,s in rows:
        if pid==T:
            print('target: content=%r raw=%r idx=%d cid=%d'%(s,c,idx,cid))
            for b in (s,c,'&quot;What?&quot;'):
                print('   base=%-20r -> %s'%(b[:20],brute(pid,b)))
    # also try the 'Block 1' family
    for cid,idx,pid,c,s in rows:
        if s=='Block 1' and md5(s)!=pid:
            print('Block 1 cid=%d idx=%d pid=%s -> %s'%(cid,idx,pid[:10],brute(pid,s)))
if __name__=='__main__': main()
