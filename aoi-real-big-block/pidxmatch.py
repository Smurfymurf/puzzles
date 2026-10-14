#!/usr/bin/env python3
# pidxmatch.py - do mismatching pids resolve to OTHER paragraphs' text (or vice versa)?
import re, html, hashlib, urllib.request, json
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
STORY=184148284
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def dec(c): return html.unescape(re.sub(r'<[^>]+>','',c))
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()

def main():
    ids=[p['id'] for p in json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))['parts']]
    md5map={}; pidmap={}
    for cid in ids:
        try: t=get('https://www.wattpad.com/amp/%d'%cid)
        except Exception as e: print('skip',cid,e); continue
        for idx,(pid,c) in enumerate(paras(t)):
            s=dec(c)
            md5map.setdefault(md5(s),[]).append((cid,idx))
            pidmap[pid]=(cid,idx,s)
    print('paragraphs',len(pidmap))
    bad=[(pid,v) for pid,v in pidmap.items() if md5(v[2])!=pid]
    print('mismatches',len(bad))
    res=0
    for pid,(cid,idx,s) in bad:
        if pid in md5map:
            res+=1
            print('RESOLVED pid=%s  at cid=%d idx=%d  text ALSO at %s'%(pid,cid,idx,md5map[pid][:4]))
    print('resolved %d of %d'%(res,len(bad)))
    print('--- unresolved (first 25) ---')
    for pid,(cid,idx,s) in bad:
        if pid not in md5map: print('  cid=%d idx=%d content=%r'%(cid,idx,s[:70]))
    T='8b71bade9685d3388452bc4755b06a0d'
    print('TARGET pid found as an md5 in corpus:', md5map.get(T))
    print('md5 of our para77 text is a pid elsewhere:', pidmap.get(md5('"What?"')))
if __name__=='__main__': main()
