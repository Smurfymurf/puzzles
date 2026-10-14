#!/usr/bin/env python3
"""
aoi.py -- Real Big Block (Aoi Nakamoto Quizchain) solver.

Model (certified on the solved sibling Block 77 Stage One):
    text --MD5--> 128-bit entropy --BIP39--> mnemonic --BIP44 m/44'/0'/0'/0/i--> P2PKH
    compared against the escrow 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W  (i = 0..5)

Novel axis: the case-flip keep-set is a FITTED parameter. The flip decision is per
FIRST LETTER, so sweeping every keep-set = 2^d texts, exhaustively. That dimension
has only ever been sampled (~1,200 texts); this closes it.

  python3 aoi.py fetch                      # download chapter -> aoi_paras.txt
  python3 aoi.py selftest                   # certify the derivation pipeline
  python3 aoi.py size                       # show the exact space
  python3 aoi.py run --combo-set core       # ~2^d texts
  python3 aoi.py run --combo-set wide       # x conventions
  python3 aoi.py run --combo-set core --resume

Resumable: finished units are appended to aoi_done.log; rerun skips them.
A hit is written to AOI_HIT.txt.
Deps: pip install coincurve mnemonic pycryptodome
"""
from __future__ import annotations
import argparse, hashlib, hmac, html, os, re, sys, time, multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
PARAS = os.path.join(HERE, "aoi_paras.json")
LOG   = os.path.join(HERE, "aoi_done.log")
HIT   = os.path.join(HERE, "AOI_HIT.txt")

TARGET = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"
STAGE1_MD5 = "9dd2efb9bc976c2095bd534d7b8d431c"      # certified Stage One value
NB = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BLOCK = 4096                                          # masks per work unit

# ---------------------------------------------------------------- primitives
def ripemd(d):
    try: return hashlib.new("ripemd160", d).digest()
    except Exception:
        from Crypto.Hash import RIPEMD160; return RIPEMD160.new(d).digest()

def hash160(b): return ripemd(hashlib.sha256(b).digest())

def b58check(payload):
    d = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(d, "big"); s = ""
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return "1" * (len(d) - len(d.lstrip(b"\x00"))) + s

from coincurve import PublicKey
def _pub(k, comp): return PublicKey.from_secret(k).format(comp)

def _child(k, c, index, hard):
    data = (b"\x00" + k.to_bytes(32, "big")) if hard else _pub(k.to_bytes(32, "big"), True)
    data += (index | (0x80000000 if hard else 0)).to_bytes(4, "big")
    d = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(d[:32], "big") + k) % NB, d[32:]

def bip44_address(seed, idx):
    d = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = int.from_bytes(d[:32], "big"), d[32:]
    for i in (44, 0, 0): k, c = _child(k, c, i, True)     # m/44'/0'/0'/0
    k, c = _child(k, c, 0, False)
    k, _ = _child(k, c, idx, False)                          # /i
    return b58check(b"\x00" + hash160(_pub(k.to_bytes(32, "big"), True)))

def entropy_to_mnemonic(e):
    bits = (int.from_bytes(e, "big") << 4) | (hashlib.sha256(e).digest()[0] >> 4)
    from mnemonic import Mnemonic
    W = Mnemonic("english").wordlist
    return " ".join(W[(bits >> (11 * (11 - i))) & 0x7FF] for i in range(12))

def check(text):
    e = hashlib.md5(text.encode("utf-8")).digest()
    seed = hashlib.pbkdf2_hmac("sha512", entropy_to_mnemonic(e).encode(), b"mnemonic", 2048, 64)
    for i in range(6):
        if bip44_address(seed, i) == TARGET:
            return i
    return None

# ---------------------------------------------------------------- text variants
def _first_letter(p, skip_quotes=True):
    for ch in p:
        if ch.isalpha(): return ch.lower()
        if not skip_quotes and ch not in "\"'\u201c\u201d\u2018\u2019": return None
    return None

def _flip(p, mode):
    ch = list(p); L = [i for i, c in enumerate(ch) if c.isalpha()]
    if not L: return p
    if mode == "lowerFirst":  ch[L[0]] = ch[L[0]].lower(); ch[L[-1]] = ch[L[-1]].upper()
    elif mode == "upperFirst": ch[L[0]] = ch[L[0]].upper(); ch[L[-1]] = ch[L[-1]].lower()
    elif mode == "firstOnly": ch[L[0]] = ch[L[0]].lower()
    elif mode == "lastOnly": ch[L[-1]] = ch[L[-1]].upper()
    return "".join(ch)

# combo table: (join, trailing, flip_mode, skip_quotes)
_MODES = ["lowerFirst", "upperFirst", "firstOnly", "lastOnly"]
_JOINS = [("\r\n\r\n", ""), ("\n\n", ""), ("\r\n\r\n", "\r\n"), ("\n\n", "\n"), ("\r\n", ""), ("\n", "")]
COMBOS = [(j, t, m, True) for m in _MODES for (j, t) in _JOINS]

_S = {}
STRUCT = ["p"]

def _load():
    import json
    P = json.load(open(PARAS, encoding="utf-8"))
    if STRUCT[0] == "br":
        P = [q for p in P for q in p.split(chr(0))]
    P = [p for p in P if p.strip()]
    letters = sorted(set(_first_letter(p, True) or "" for p in P))
    return {"paras": P, "letters": letters,
            "li": [{c: i for i, c in enumerate(letters)} for _ in P],
            "flipped": [[_flip(p, m) for p in P] for m in ("lowerFirst", "upperFirst", "firstOnly", "lastOnly")],
            "fl": [(_first_letter(p, True) or "") for p in P]}

def _init():
    _S.update(_load())

def _text(mask, combo):
    P, F, FL, li = _S["paras"], _S["flipped"], _S["fl"], _S["li"]
    fi = ("lowerFirst", "upperFirst", "firstOnly", "lastOnly").index(combo[2])
    sep, trail = combo[0], combo[1]
    le = chr(13) + chr(10) if chr(13) in sep else chr(10)
    parts = []
    for i in range(len(P)):
        src = F[fi][i] if (mask and (mask >> li[i][FL[i]]) & 1) else P[i]
        parts.append(src.replace(chr(0), le))
    return sep.join(parts) + trail

def _unit(uid):
    combo = COMBOS[uid % len(COMBOS)]
    mask = uid // len(COMBOS)
    for m in range(mask, mask + BLOCK):
        if m >= 2 ** len(_S["letters"]): break
        idx = check(_text(m, combo))
        if idx is not None:
            return uid, m, combo, idx
    return uid, None, combo, None

# ---------------------------------------------------------------- commands
def cmd_fetch(a):
    import urllib.request, gzip, json
    def get(url):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "*/*"})
        r = urllib.request.urlopen(req, timeout=60)
        d = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            d = gzip.decompress(d)
        return d.decode("utf-8", "replace")
    for url in ("https://www.wattpad.com/apiv2/storytext?id=720888559",
                "https://www.wattpad.com/apiv2/?m=storytext&id=720888559"):
        try:
            raw = get(url)
        except Exception as e:
            print("  " + url + " -> " + str(e)); continue
        body = raw
        if body.lstrip().startswith("{"):
            try:
                body = json.loads(body).get("text", body)
            except Exception:
                pass
        for tag in ("<br>", "<br/>", "<br />", "<br  />", "<br\t/>"):
            body = body.replace(tag, chr(0))
        paras = []
        for m in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S):
            t = html.unescape(re.sub(r"<[^>]+>", "", m)).strip()
            if t:
                paras.append(t)
        if len(paras) > 20:
            json.dump(paras, open(PARAS, "w", encoding="utf-8"), ensure_ascii=False)
            print("wrote " + str(len(paras)) + " paragraphs -> " + PARAS)
            return 0
    print("fetch failed"); return 1

def cmd_selftest(a):
    ok = True
    M = "abandon " * 11 + "about"
    seed = hashlib.pbkdf2_hmac("sha512", M.encode(), b"mnemonic", 2048, 64)
    addr = bip44_address(seed, 0)
    good = addr == "1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA"
    print(f"canonical vector -> {addr}  {'OK' if good else 'FAIL'}")
    ok &= good
    if a.finney and os.path.exists(a.finney):
        _ftxt = open(a.finney, encoding="utf-8").read().rstrip("\n")
        P = [x for x in _ftxt.split("\n\n") if x.strip()]
        txt = "\n\n".join(p if p[0] in set("ITASM") else _flip(p, "lowerFirst") for p in P)
        h = hashlib.md5(txt.encode("utf-8")).hexdigest()
        good = h == STAGE1_MD5
        print(f"Stage One reproduction MD5 {h}  {'OK' if good else 'FAIL'}")
        ok &= good
        e = bytes.fromhex(h)
        M1 = entropy_to_mnemonic(e)
        s1 = hashlib.pbkdf2_hmac("sha512", M1.encode(), b"mnemonic", 2048, 64)
        hits = [bip44_address(s1, i) for i in range(6)]
        good = "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN" in hits
        print(f"Stage One addresses {hits}  {'OK' if good else 'FAIL'}")
        ok &= good
    else:
        print("Stage One not checked (pass --finney <topic155054 first post as one paragraph per line>)")
    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1

def cmd_size(a):
    _S.update(_load())
    d = len(_S["letters"])
    combos = len(COMBOS) if a.combo_set == "wide" else 1
    units = (2 ** d * combos + BLOCK - 1) // BLOCK
    print(f"paragraphs            : {len(_S['paras'])}")
    print(f"distinct first letters: {d}")
    print(f"flip patterns         : 2^{d} = {2**d:,}")
    print(f"convention combos     : {combos}")
    print(f"TOTAL texts           : {2**d * combos:,}")
    print(f"work units            : {units:,}")
    return 0

def cmd_run(a):
    _init()
    d = len(_S["letters"])
    combos = range(len(COMBOS)) if a.combo_set == "wide" else range(1)
    total_units = ((2 ** d) + BLOCK - 1) // BLOCK
    units = [ci * total_units + u for ci in combos for u in range(total_units)]
    done = set()
    if a.resume and os.path.exists(LOG):
        done = {int(x) for x in open(LOG) if x.strip()}
    todo = [u for u in units if u not in done]
    print(f"units={len(units):,} pending={len(todo):,} workers={a.workers}")
    t0 = time.time(); n = 0
    with mp.Pool(a.workers, initializer=_init) as pool, open(LOG, "a") as log:
        for uid, m, combo, idx in pool.imap_unordered(_unit, todo, chunksize=1):
            log.write(f"{uid}\n"); log.flush(); n += 1
            if m is not None:
                txt = _text(m, combo)
                open(HIT, "w", encoding="utf-8").write(f"mask={m} combo={combo} index={idx}\n{txt}\n")
                print(f"\n*** MATCH  mask={m} combo={combo} index={idx} -> {HIT}")
                pool.terminate(); return 0
            if n % 5 == 0 or n == len(todo):
                el = time.time() - t0
                print(f"\r{n:,}/{len(todo):,} units  {n/el:.1f} u/s  eta {(len(todo)-n)/max(n/el,1e-9)/60:.0f} min", end="")
    print("\nfinished, no match"); return 1

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    s = sub.add_parser("selftest"); s.add_argument("--finney")
    s = sub.add_parser("size"); s.add_argument("--combo-set", choices=["core", "wide"], default="core"); s.add_argument("--structure", choices=["p", "br"], default="p")
    r = sub.add_parser("run")
    r.add_argument("--combo-set", choices=["core", "wide"], default="core")
    r.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    r.add_argument("--resume", action="store_true")
    r.add_argument("--structure", choices=["p", "br"], default="p")
    a = ap.parse_args()
    STRUCT[0] = getattr(a, "structure", "p")
    mp.freeze_support()
    return {"fetch": cmd_fetch, "selftest": cmd_selftest, "size": cmd_size, "run": cmd_run}[a.cmd](a)

if __name__ == "__main__":
    sys.exit(main())
