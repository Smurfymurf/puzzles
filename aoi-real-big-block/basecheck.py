import hashlib, aoi, toggle2 as t
aoi._init(); S=aoi._S; m=0
for i,c in enumerate(S["letters"]):
    if c not in set("itasm"): m|=1<<i
for jn,j in (("crlf2","\r\n\r\n"),("crlf","\r\n"),("lf2","\n\n"),("lf","\n")):
    for tr in ("","\n","\r\n"):
        T=aoi._text(m,(j,tr,"lowerFirst",True)).encode()
        hs=t.derive(hashlib.md5(T).digest())
        addrs=[t.b58check(b"\x00"+h) for _,h in hs]
        hit=[a for a in addrs if a in (t.TARGET,t.SUPER)]
        print("%-6s %-5r len=%d md5=%s %s"%(jn,tr,len(T),hashlib.md5(T).hexdigest(),("HIT "+str(hit)) if hit else ""))
