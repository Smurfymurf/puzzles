import re, hashlib
raw=open('/Users/steve/wp_raw.html',encoding='utf-8').read()
ps=re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>', raw, re.S)
print('paras',len(ps))
ok=0; bad=[]
for pid,c in ps:
    cc=re.sub(r'<[^>]+>','',c)
    if hashlib.md5(cc.encode('utf-8')).hexdigest()==pid: ok+=1
    else: bad.append((pid,repr(cc[:50])))
print('pid match',ok,'mismatch',len(bad))
for b in bad[:6]: print(b)
