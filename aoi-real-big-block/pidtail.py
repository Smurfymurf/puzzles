#!/usr/bin/env python3
# pidtail.py - wrong pid = md5(content + rest of the pasted block)?
import re, html, hashlib, urllib.request, json, collections
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
STORY=184148284
SEP=['','\n','\n\n','\r\n','\r\n\r\n',' ']
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def dec(c): return html.unescape(re.sub(r'<[^>]+>','',c))
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode()).hexdigest()
def main():
    ids=[p['id'] for p in json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))['parts']]
    hits=collections.Counter(); tot=0
    for cid in ids:
        try: t=get('https://www.wattpad.com/amp/%d'%cid)
        except: continue
        ps=[(pid,dec(c)) for pid,c in paras(t)]
        for i,(pid,s) in enumerate(ps):
            if md5(s)==pid: continue
            tot+=1
            for j in range(i+1, min(i+15,len(ps))):
                for sep in SEP:
                    if md5(sep.join(ps[k][1] for k in range(i,j+1)))==pid: hits['tail sep=%r j-i=%d'%(sep,j-i)]+=1
                    if md5(sep.join(ps[k][1] for k in range(j,i-1,-1)))==pid: hits['head sep=%r j-i=%d'%(sep,j-i)]+=1
    print('mismatches',tot); print(hits.most_common(15))
    # context of the two "What?" paragraphs
    t=get('https://www.wattpad.com/amp/720888559'); ps=[dec(c) for _,c in paras(t)]
    for i in (33,77):
        print('=== around idx %d ==='%i)
        for k in range(max(0,i-3), min(len(ps),i+4)):
            print(('  >>' if k==i else '    '), repr(ps[k][:80]))
if __name__=='__main__': main()
