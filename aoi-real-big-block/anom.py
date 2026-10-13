import hashlib, json, os, aoi, toggle2 as t
P=json.load(open(os.path.expanduser('~/aoi_paras.json'),encoding='utf-8'))
def build(paras,join):
    parts=[]
    for p in paras:
        fl=aoi._first_letter(p,True)
        parts.append(aoi._flip(p,"lowerFirst") if (fl and fl not in set("itasm")) else p)
    return join.join(parts)
def chk(txt,lab):
    hs=t.derive(hashlib.md5(txt.encode()).digest())
    a=[t.b58check(b"\x00"+h) for _,h in hs]
    h=[x for x in a if x in (t.TARGET,t.SUPER)]
    if h: print("HIT",lab,h)
for jn,j in (("crlf2","\r\n\r\n"),("crlf","\r\n"),("lf2","\n\n")):
    for v in (0,1):
        for b in (0,1):
            ps=list(P)
            if v: ps=[q.replace("VIrgin","Virgin") for q in ps]
            if b: ps=[q.replace("BItcoin","Bitcoin") for q in ps]
            chk(build(ps,j),"%s caps v%d b%d"%(jn,v,b))
    idx=[i for i,ch in enumerate(build(P,j)) if ch=='\u00a0']
    for k in range(1<<len(idx)):
        ps="".join((' ' if (k>>n)&1 else ch) for n,ch in enumerate(build(P,j)) if True)
        # rebuild by flipping only NBSP positions
        x=list(build(P,j))
        for n,i in enumerate(idx):
            if (k>>n)&1: x[i]=' '
        chk("".join(x),"%s nbsp %d"%(jn,k))
    print(jn,"done nbsp",len(idx))
