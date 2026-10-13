import hashlib, json, os, re
PID="8b71bade9685d3388452bc4755b06a0d"
P=json.load(open(os.path.expanduser('~/aoi_paras.json'),encoding='utf-8'))
def m(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
c=set()
for p in P:
    for s in [p, p.strip(), p.lower(), p.upper()]:
        c.add(s)
    for s in re.split(r'(?<=[.!?])\s+', p):
        if s.strip(): c.add(s.strip())
for s in list(c):
    for w in ('"%s"',"'%s'",'%s\n','%s ',' %s','%s!','%s.'):
        c.add(w%s)
hit=[s for s in c if m(s)==PID]
print('cands',len(c),'HIT',hit)
for w in ['"What?"','"what?"','"WHAT?"','"What?"\n','"What?" ','"What?"']:
    print(repr(w), m(w)==PID)
