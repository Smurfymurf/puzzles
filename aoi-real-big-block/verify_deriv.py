import hashlib, os, sys
D = os.path.expanduser("~/puzzles/aoi-real-big-block")
sys.path.insert(0, D)
import aoi, mask2
aoi._init()
h0 = hashlib.md5(aoi._text(3796477, ("\r\n\r\n", "", "lowerFirst", True)).encode("utf-8")).hexdigest()
seed = mask2.seed_of(h0)
k, c = mask2.master(seed)
for j in (44 + 2**31, 2**31, 2**31, 0):
    k, c = mask2.ckd(k, c, j)
ok = True
for idx in range(6):
    ours = mask2.addr(mask2.ckd(k, c, idx)[0])
    theirs = aoi.bip44_address(seed, idx)
    same = ours == theirs
    ok = ok and same
    print(idx, ours, theirs, "OK" if same else "MISMATCH")
print("DERIVATION", "VERIFIED" if ok else "BROKEN - mask2 results void")
