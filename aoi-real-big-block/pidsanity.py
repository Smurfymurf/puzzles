#!/usr/bin/env python3
# pidsanity.py - does Wattpad's stored paragraph text still match its own data-p-id?
# Drift (any paragraph whose pid is md5 of content +/- whitespace) => a 2019 copy is decisive.
import re, sys, hashlib, urllib.request, json

UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
IDS=[717956015,720888559,720895205,742662804,759761389,760378354]
WS=[' ','\u00a0','\t','\n','\r\n','\u200b','\ufeff','\u2009','\u2002']
STORY=184148284

def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def strip(c): return re.sub(r'<[^>]+>','',c)
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()

def ws_explain(s,pid):
    for a in WS:
        if md5(s+a)==pid: return 'suffix '+repr(a)
        if md5(a+s)==pid: return 'prefix '+repr(a)
    for a in WS:
        for b in WS:
            if md5(s+a+b)==pid: return 'suffix '+repr(a+b)
            if md5(a+b+s)==pid: return 'prefix '+repr(a+b)
    for a in WS:
        for b in WS:
            for c in WS:
                if md5(s+a+b+c)==pid: return 'suffix '+repr(a+b+c)
    return None

def fetch_parts():
    try:
        j=json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))
        return [p['id'] for p in j.get('parts',[])]
    except Exception as e:
        print('story api failed:',e); return []

def main():
    ids=[int(a) for a in sys.argv[1:] if a.isdigit()] or IDS
    sp=fetch_parts()
    if sp:
        print('story parts found:',len(sp))
        ids=sp+[i for i in ids if i not in sp]
    tot=0; bad=0; drift=0
    for cid in ids:
        txt=None
        for u in ('https://www.wattpad.com/%d'%cid,'https://www.wattpad.com/amp/%d'%cid):
            try:
                t=get(u)
                if paras(t): txt=t; break
            except Exception as e: pass
        if txt is None:
            print('%d  no pids'%cid); continue
        ps=paras(txt); m=0; det=[]
        for pid,c in ps:
            s=strip(c)
            if md5(s)==pid: m+=1
            else:
                ex=ws_explain(s,pid)
                if ex: drift+=1
                det.append((pid,repr(s[:70]),ex))
        tot+=len(ps); bad+=len(ps)-m
        print('%d paras=%d match=%d MISMATCH=%d'%(cid,len(ps),m,len(ps)-m))
        for d in det[:10]:
            print('    pid=%s content=%s ws_explains=%s'%d)
    print('---')
    print('TOTAL paras=%d mismatch=%d (%.3f%%) whitespace-explained=%d'%(tot,bad,100.0*bad/max(tot,1),drift))

if __name__=='__main__': main()
