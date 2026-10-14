#!/usr/bin/env python3
# pidcrack.py - what IS a "wrong" pid the md5 of?  Systematic transform family.
import re, html, hashlib, urllib.request, json, collections
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}
STORY=184148284
CH=" abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?'\"-_&;#<>/\\\n\r\t"
TAGS=['<b>%s</b>','<i>%s</i>','<em>%s</em>','<strong>%s</strong>','<span>%s</span>','%s<br>','<br>%s','<p>%s</p>']
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40).read().decode('utf-8','replace')
def dec(c): return html.unescape(re.sub(r'<[^>]+>','',c))
def strip(c): return re.sub(r'<[^>]+>','',c)
def paras(t): return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>',t,re.S)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()

SUF=set([''])
for a in CH:
    SUF.add(a)
    for b in CH: SUF.add(a+b)
SUF=sorted(SUF)
print('suffix/prefix family size',len(SUF))

def main():
    ids=[p['id'] for p in json.loads(get('https://www.wattpad.com/api/v3/stories/%d?fields=parts(id,title)'%STORY))['parts']]
    rows=[]
    for cid in ids:
        try: t=get('https://www.wattpad.com/amp/%d'%cid)
        except: continue
        for idx,(pid,c) in enumerate(paras(t)): rows.append((cid,idx,pid,c))
    bad=[r for r in rows if md5(dec(r[3]))!=r[2]]
    print('mismatch',len(bad))
    cnt=collections.Counter()
    for cid,idx,pid,c in bad:
        s=dec(c)
        base=[s, c, strip(c), html.unescape(c), strip(html.unescape(c)),
              s.replace('"','&quot;').replace("'",'&apos;'),
              s.strip(), s.rstrip(), s.lstrip(), s+s, s[:-1] or s, s[1:] or s]
        base+= [t % s for t in TAGS]
        base+= [s+str(idx), str(idx)+s, s+str(cid), str(cid)+s]
        done=set()
        for b in base:
            for suf in SUF:
                for v,lab in ((b+suf,'S'),(suf+b,'P')):
                    if v in done: continue
                    done.add(v)
                    if md5(v)==pid: cnt[lab+' '+repr(suf)[:12]+' base='+repr(b)[:30]]+=1
    for k,v in cnt.most_common(25): print(v,k)
    print('resolved', sum(cnt.values()), 'of', len(bad))

    T='8b71bade9685d3388452bc4755b06a0d'
    for cid,idx,pid,c in rows:
        if pid!=T: continue
        s=dec(c)
        base=[s,c,strip(c),html.unescape(c),s.replace('"','&quot;'),s.replace('"','&#34;'),
              '"whaT?"','"What?"','"What?" ','"What?"\n','"What?"\r\n','&quot;What?&quot;']
        base+=[t % s for t in TAGS]
        print('--- target base strings ---')
        for b in base: print('   %-24r md5=%s'%(b[:24],md5(b)))
if __name__=='__main__': main()
