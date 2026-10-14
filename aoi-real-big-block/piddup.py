#!/usr/bin/env python3
# piddup.py - dump duplicate groups with differing pids in full; big battery on mismatches.
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
    print('paras',len(rows),'mismatch',sum(1 for r in rows if md5(r[4])!=r[2]))
    g=collections.defaultdict(list)
    for cid,idx,pid,c,s in rows: g[s].append((cid,idx,pid,c))
    shown=0
    for s,v in g.items():
        if len(v)<2: continue
        if len({x[2] for x in v})<2: continue
        if shown>=6: break
        shown+=1
        print('=== dup content len=%d %r'%(len(s),s[:70]))
        for cid,idx,pid,c in v:
            print('   cid=%d idx=%d pid=%s md5(dec)=%s RAW=%r'%(cid,idx,pid[:10],md5(dec(c))[:10],c[:90]))
    print('--- battery v2 on all mismatches ---')
    cnt=collections.Counter()
    for cid,idx,pid,c,s in rows:
        if md5(s)==pid: continue
        r=re.sub(r'<[^>]+>','',c)
        cands={'raw_inner':r,'strip_noesc':r,'enc_quot':s.replace('"','&quot;').replace("'",'&apos;'),
               'sp2nbsp':s.replace(' ','\u00a0'),'sp2tab':s.replace(' ','\t'),
               'strip()':s.strip(),'rstrip()':s.rstrip(),'lstrip()':s.lstrip(),
               'plus_self':s+s,'minus_last':s[:-1],'plus_first':s+s[0],
               'idx':s+str(idx),'idx_pre':str(idx)+s,'nl_idx':s+'\n'+str(idx)}
        for k,v in cands.items():
            if md5(v)==pid: cnt[k]+=1
    print(cnt.most_common(20))
    T='8b71bade9685d3388452bc4755b06a0d'
    print('--- target ---')
    for cid,idx,pid,c,s in rows:
        if pid==T:
            print('cid=%d idx=%d pid=%s RAW=%r DEC=%r len=%d'%(cid,idx,pid,c,s,len(s)))
            print('  md5(raw)=%s md5(dec)=%s'%(md5(re.sub(r'<[^>]+>','',c)),md5(s)))
if __name__=='__main__': main()
