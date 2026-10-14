#!/usr/bin/env python3
# pidnb.py - is a wrong pid md5(content + neighbour / structural context)?
import re, html, hashlib, urllib.request, json, collections
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
STORY=184148284
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def dec(c): return html.unescape(re.sub(r'<[^>]+>','',c))
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()

def main():
    ids=[p['id'] for p in json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))['parts']]
    per={}
    for cid in ids:
        try: t=get('https://www.wattpad.com/amp/%d'%cid)
        except: continue
        per[cid]=[(pid,dec(c)) for pid,c in paras(t)]
    cnt=collections.Counter()
    tot=0
    for cid,ps in per.items():
        for i,(pid,s) in enumerate(ps):
            if md5(s)==pid: continue
            tot+=1
            prev=ps[i-1][1] if i>0 else ''
            nxt=ps[i+1][1] if i+1<len(ps) else ''
            prevp=ps[i-1][0] if i>0 else ''
            nextp=ps[i+1][0] if i+1<len(ps) else ''
            cands={
             's+nl+nxt':s+'\n'+nxt, 'prev+nl+s':prev+'\n'+s,
             's+nxt':s+nxt, 'prev+s':prev+s,
             's+nlnl+nxt':s+'\n\n'+nxt, 'prev+nlnl+s':prev+'\n\n'+s,
             's+prevp':s+prevp, 'prevp+s':prevp+s,
             's+nextp':s+nextp, 'nextp+s':nextp+s,
             's+sp+nxt':s+' '+nxt, 'prev+sp+s':prev+' '+s,
             's+self':s+s, 's+nl':s+'\n', 's+nlnl':s+'\n\n', 'nl+s':'\n'+s,
             'crlf_s':s+'\r\n', 's_crlfcrlf':s+'\r\n\r\n',
            }
            for k,v in cands.items():
                if v and md5(v)==pid: cnt[k]+=1
    print('mismatches',tot)
    print('hits:',cnt.most_common(20))
    # full pid of the two Block 1 second-copies, for later use
    for cid,ps in per.items():
        for i,(pid,s) in enumerate(ps):
            if s=='Block 1' and md5(s)!=pid:
                print('Block1 cid=%d idx=%d FULLPID=%s'%(cid,i,pid))
            if s=='"What?"' and md5(s)!=pid:
                print('WHAT  cid=%d idx=%d FULLPID=%s'%(cid,i,pid))
if __name__=='__main__': main()
