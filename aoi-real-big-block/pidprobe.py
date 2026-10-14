#!/usr/bin/env python3
# pidprobe.py - wide structured probe of the para-77 pid (original-text preimage).
import re, os, html, hashlib
HOME=os.path.expanduser('~')
RAW=os.path.join(HOME,'wp_raw.html')
PID='8b71bade9685d3388452bc4755b06a0d'
PIDB=bytes.fromhex(PID)

def load():
    raw=open(RAW,encoding='utf-8').read()
    return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>', raw, re.S)

def strip(c): return re.sub(r'<[^>]+>','',c)

INV=['\u00a0','\u200b','\u200c','\u200d','\ufeff','\u00ad','\u2009','\u200a','\u202f','\t','\n','\r\n',' ','  ','\u2013','\u2014','\u2060']
PREQ=['','"','\u201c','&quot;','&#34;',"'",'\u2018']
SUFQ=['','"','\u201d','&quot;',"'",'\u2019']
WORDS=['What','Wait','Wha','Huh','Hey','Why','Who','How','Oh','So','Ah']
PUN=['?','?!','!?','??','?!"','...','?!?','.','!']
MID=['',' ','\u00a0','\u200b','-','\u2014','...']
PRETXT=['','He said, ','She said, ','The voice said, ','He asked, ','A voice said, ','Someone said, ']
TAIL=['',' he said.',' he asked.',' he said',' he asked',' she said.',' she said',' said the voice.',
      ' he repeated.',' he whispered.',' he replied.',' he answered.',' came the reply.',' the voice said.',
      ' he said quietly.',' he asked quietly.',' he said, surprised.',' he asked, surprised.',
      ' the man said.',' the woman said.',' he muttered.',' he thought.']

def casings(w):
    for m in range(1<<len(w)):
        yield ''.join(ch.upper() if (m>>i)&1 else ch.lower() for i,ch in enumerate(w))

def main():
    ps=load()
    bad=[i for i,(p,c) in enumerate(ps) if hashlib.md5(strip(c).encode()).hexdigest()!=p]
    print('mismatch idx',bad,'of',len(ps))
    print('--- context 68..88 raw inner html ---')
    for j in range(68,89):
        if j<len(ps): print('[%d]%s %r'%(j,'  <-- MISMATCH' if j in bad else '', ps[j][1][:200]))
    raw=open(RAW,encoding='utf-8').read()
    print('--- pid literal occurrences in page:', raw.count(PID))
    C=set()
    base='"What?"'
    C.add(base)
    for c in INV:
        for i in range(len(base)+1): C.add(base[:i]+c+base[i:])
        C.add(c+base); C.add(base+c); C.add(c+base+c)
    for w in WORDS:
        for v in casings(w):
            for pre in PREQ:
                for mid in MID:
                    for pu in PUN:
                        for suf in SUFQ:
                            core=pre+v+mid+pu+suf
                            C.add(core)
                            for t in TAIL:
                                C.add(core+t)
                                for pt in PRETXT: C.add(pt+core+t)
    print('candidates', len(C), flush=True)
    hits=[]
    for s in C:
        if hashlib.md5(s.encode('utf-8')).digest()==PIDB:
            hits.append(s); print('  *** PID HIT', repr(s), flush=True)
    print('probe done', len(C), 'hits', len(hits))
    for h in hits: print('HIT', repr(h))

if __name__=='__main__': main()
