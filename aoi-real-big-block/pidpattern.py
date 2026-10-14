#!/usr/bin/env python3
# pidpattern.py - is a pid always md5(own text)?  Group duplicates; find the pattern.
import re, html, hashlib, urllib.request, json, collections
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
STORY=184148284
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def dec(c): return html.unescape(re.sub(r'<[^>]+>','',c))
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
BAT=['',' ','  ','\n','\r\n','\r','\t','\u00a0','\u200b','&nbsp;','<br>','<br/>','<br />','<p>','</p>','.','!','&quot;','&#160;']

def main():
    ids=[p['id'] for p in json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))['parts']]
    rows=[]
    for cid in ids:
        try: t=get('https://www.wattpad.com/amp/%d'%cid)
        except: continue
        for idx,(pid,c) in enumerate(paras(t)): rows.append((cid,idx,pid,dec(c)))
    print('paragraphs',len(rows))
    bad=[r for r in rows if md5(r[3])!=r[2]]
    print('mismatch',len(bad))
    # A) duplicate content: do duplicates share a pid?
    g=collections.defaultdict(list)
    for cid,idx,pid,s in rows: g[s].append((cid,idx,pid))
    dup=[(s,v) for s,v in g.items() if len(v)>1]
    print('duplicate-content groups:',len(dup))
    same=diff=0
    for s,v in dup:
        pids={x[2] for x in v}
        if len(pids)==1: same+=1
        else: diff+=1
    print('  groups where all pids identical:',same,' where pids differ:',diff)
    for s,v in dup[:5]:
        print('   dup %r x%d pids=%s'%(s[:45],len(v),sorted({x[2][:8] for x in v})))
    # B) does the battery explain the mismatches?
    print('--- battery on mismatching paragraphs ---')
    hits=collections.Counter()
    for cid,idx,pid,s in bad:
        for X in BAT:
            if md5(s+X)==pid: hits['suffix '+repr(X)]+=1
            if md5(X+s)==pid: hits['prefix '+repr(X)]+=1
    print(hits.most_common(20))
    # C) show 12 mismatches in full
    for cid,idx,pid,s in bad[:12]:
        print('cid=%d idx=%d pid=%s len=%d content=%r'%(cid,idx,pid[:10],len(s),s))
    T='8b71bade9685d3388452bc4755b06a0d'
    print('occurrences of target pid:',sum(1 for r in rows if r[2]==T))
    print('occurrences of content "What?":',sum(1 for r in rows if r[3]=='"What?"'))
    for cid,idx,pid,s in rows:
        if s=='"What?"': print('   cid=%d idx=%d pid=%s md5(content)=%s match=%s'%(cid,idx,pid[:10],md5(s)[:10],md5(s)==pid))
if __name__=='__main__': main()
