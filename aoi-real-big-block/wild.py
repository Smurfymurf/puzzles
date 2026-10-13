import hashlib, json, os, aoi, toggle2 as t
P=json.load(open(os.path.expanduser('~/aoi_paras.json'),encoding='utf-8'))
def rule(p):
    fl=aoi._first_letter(p,True)
    return aoi._flip(p,"lowerFirst") if (fl and fl not in set("itasm")) else p
def chk(txt,lab):
    hs=t.derive(hashlib.md5(txt.encode('utf-8')).digest())
    a=[t.b58check(b"\x00"+h) for _,h in hs]
    h=[x for x in a if x in (t.TARGET,t.SUPER)]
    if h: print("HIT",lab,h)
R=[rule(p) for p in P]
for j in (""," ","\t","\n","\r\n","\n\n","\r\n\r\n","\n\r","\r\n\n","\n\n\n","\r\n\r\n\r\n"):
    for tr in ("","\n","\r\n"," ","\r\n\r\n"):
        chk(j.join(R)+tr,"join=%r trail=%r"%(j,tr))
        chk("\uFEFF"+j.join(R)+tr,"BOM join=%r"%j)
    b=j.join(R)
    for v in (b,b.replace("WW","UUUU"),b.replace("WW","UU"),b.replace("FFWW","FFUUUU"),b.replace("WW","ww")):
        chk(v,"meta-hint join=%r"%j)
pids=[hashlib.md5(p.strip().encode()).hexdigest() for p in P]
for s in ("".join(pids),"\n".join(pids)," ".join(pids)): chk(s,"pid-join")
print("done")
