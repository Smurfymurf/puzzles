import aoi, inspect
print("signature:", inspect.signature(aoi.bip44_address))
src = inspect.getsource(aoi.bip44_address)
print("source:\n", src[:600])
print("---- stage1 sanity ----")
e = bytes.fromhex(aoi.STAGE1_MD5)
for i in range(0, 6):
    try: print(i, aoi.bip44_address(e, i))
    except Exception as ex: print(i, "ERR", ex)
print("expected idx0 = 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN")
