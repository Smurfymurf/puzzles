#!/usr/bin/env python3
# pidpre.py - exploit the para-77 pid as a 128-bit oracle on the exact deviating bytes.
#   pidpre.py dump          phase 1 - raw inner HTML of every mismatch + normalization check
#   pidpre.py tmpl          phase 2a - structured template preimage search (pooled, ~8e7)
#   pidpre.py edit [N]      phase 2b - edit distance <=N search (default 2), pooled, live ETA
#   pidpre.py try <string>  phase 3 - splice a candidate into the certified base, run the pipeline
import re, sys, os, html, hashlib, time
from multiprocessing import Pool, cpu_count

HOME = os.path.expanduser('~')
RAW  = os.path.join(HOME, 'wp_raw.html')
PID  = '8b71bade9685d3388452bc4755b06a0d'
PIDB = bytes.fromhex(PID)
HITS = os.path.join(HOME, 'pidpre_HITS.txt')
ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ?!.,;:'\"()-&/"
CHUNK = 200000

def load():
    raw = open(RAW, encoding='utf-8').read()
    return re.findall(r'<p data-p-id="([0-9a-f]{32})">(.*?)</p>', raw, re.S)

def strip(c):
    return re.sub(r'<[^>]+>', '', c)

def mismatches():
    out = []
    for i, (pid, c) in enumerate(load()):
        if hashlib.md5(strip(c).encode('utf-8')).hexdigest() != pid:
            out.append((i, pid, c))
    return out

def phase1():
    ps = load(); bad = mismatches()
    print('paras', len(ps), 'mismatch', len(bad), flush=True)
    for i, pid, c in bad:
        s = strip(c)
        print('=== idx', i, 'pid', pid, ('TARGET-PID' if pid == PID else ''), flush=True)
        print('  RAW   ', repr(c))
        print('  STRIP ', repr(s))
        print('  UNESC ', repr(html.unescape(s)))
        for nm, v in (('strip', s), ('unescape(strip)', html.unescape(s)), ('raw', c),
                      ('strip(unescape(raw))', strip(html.unescape(c))),
                      ('unescape(raw)', html.unescape(c))):
            h = hashlib.md5(v.encode('utf-8')).hexdigest()
            print('  md5(%-20s) %s %s' % (nm, h, 'MATCH' if h == pid else ''))

def _chk(chunk):
    out = []
    for s in chunk:
        if hashlib.md5(s.encode('utf-8')).digest() == PIDB:
            out.append(s)
    return out

def chunks(it, size):
    buf = []
    for x in it:
        buf.append(x)
        if len(buf) >= size:
            yield buf; buf = []
    if buf: yield buf

def run_stream(it, label, total=None):
    t0 = time.time(); n = 0; hits = []; last = t0
    f = open(HITS, 'a')
    with Pool(cpu_count() - 1) as pool:
        for res in pool.imap_unordered(_chk, chunks(it, CHUNK)):
            n += CHUNK
            for s in res:
                hits.append(s); f.write(repr(s) + '\n'); f.flush()
                print('  HIT', repr(s), flush=True)
            now = time.time()
            if now - last >= 10:
                last = now; r = n / max(now - t0, 1e-9)
                eta = ('ETA %.1f min' % ((total - n) / r / 60)) if total else ''
                print('%s tested %d  %.0f/s  %s' % (label, n, r, eta), flush=True)
    f.close()
    print('%s DONE tested~%d hits=%d %.1fs' % (label, n, len(hits), time.time() - t0), flush=True)
    return hits

LEAD = ['', ' ', '"', '&quot;', '&#34;', '&#x22;', '\u201c', '&ldquo;', '&#8220;',
        "'", '&#39;', '&apos;', '\u2018', '&lsquo;', '&nbsp;', '\u00a0']
TAILQ = ['', '"', '&quot;', '&#34;', '&#x22;', '\u201d', '&rdquo;', '&#8221;',
         "'", '&#39;', '&apos;', '\u2019', '&rsquo;']
PUNCT = ['?', '?!', '!?', '...', '..', '.', '!', '?!?', '??', '?!"', '?!.', '?..']
MID = ['', '&nbsp;', '&#160;', '&#8203;', '&amp;', '\u00a0', ' ', '-', '\u2014']
WSPRE = ['', ' ', '  ', '\n']
WSPOST = ['', ' ', '  ', '\n']
WORDS = ['What', 'what', 'Wait', 'Huh', 'Hey', 'Why', 'Who', 'How', 'Wha',
         'So', 'Oh', 'Ah', 'Yes', 'No', 'Hmm']

def cases(w):
    return set(''.join(ch.upper() if (m >> i) & 1 else ch.lower() for i, ch in enumerate(w))
               for m in range(1 << len(w)))

def gen_tmpl():
    cores = set()
    for w in WORDS: cores |= cases(w)
    for pre in WSPRE:
        for lead in LEAD:
            for c in cores:
                for mid in MID:
                    for p in PUNCT:
                        for tq in TAILQ:
                            for post in WSPOST:
                                yield pre + lead + c + mid + p + tq + post

def tmpl_total():
    cores = set()
    for w in WORDS: cores |= cases(w)
    return len(WSPRE)*len(LEAD)*len(cores)*len(MID)*len(PUNCT)*len(TAILQ)*len(WSPOST)

def gen_edits(s, d, alpha=ALPHA):
    yield s
    if d <= 0: return
    seen = set(); L = len(s); nxt = []
    for i in range(L):
        for c in alpha:
            if c != s[i]: nxt.append(s[:i] + c + s[i+1:])
    for i in range(L + 1):
        for c in alpha:
            nxt.append(s[:i] + c + s[i:])
    for i in range(L):
        nxt.append(s[:i] + s[i+1:])
    for t in nxt:
        if t in seen: continue
        seen.add(t)
        yield from gen_edits(t, d - 1, alpha)

def build(P, idx, repl, join, trail, apply_rule):
    import aoi
    le = '\r\n' if '\r' in join else '\n'
    parts = []
    for i, p in enumerate(P):
        q = repl if i == idx else p
        if apply_rule:
            fl = aoi._first_letter(q, True)
            if fl and fl not in 'itasm': q = aoi._flip(q, 'lowerFirst')
        parts.append(q.replace('\x00', le))
    return join.join(parts) + trail

def phase3(s):
    import aoi, toggle2 as t
    aoi._init(); P = aoi._S['paras']
    bad = mismatches()
    if not bad: raise SystemExit('no mismatch found')
    idx_html, pid, c = bad[0]
    cur = strip(c)
    idx = None
    for i, p in enumerate(P):
        if p == cur or html.unescape(p) == cur or p.strip() == cur.strip():
            idx = i; break
    print('html idx', idx_html, '| aoi idx', idx, '| cur', repr(cur), flush=True)
    if idx is None: raise SystemExit('could not align paragraph into aoi_paras.json')
    cands = []
    for v in (s, html.unescape(s), strip(s), strip(html.unescape(s))):
        if v not in cands: cands.append(v)
    for v in cands:
        for ar in (True, False):
            for jn, j in (('crlf2', '\r\n\r\n'), ('crlf', '\r\n'), ('lf2', '\n\n'), ('lf', '\n')):
                for tr in ('', '\n', '\r\n'):
                    T = build(P, idx, v, j, tr, ar).encode('utf-8')
                    hs = t.derive(hashlib.md5(T).digest())
                    addrs = [t.b58check(b'\x00' + h) for _, h in hs]
                    hit = [a for a in addrs if a in (t.TARGET, t.SUPER)]
                    print('   %-34s md5=%s %s' % ('rule=%s join=%s trail=%r' % (ar, jn, tr),
                          hashlib.md5(T).hexdigest(), ('*** HIT ' + str(hit)) if hit else ''), flush=True)

def main():
    m = sys.argv[1] if len(sys.argv) > 1 else 'dump'
    if m == 'dump': phase1(); return
    if m == 'tmpl':
        tot = tmpl_total(); print('tmpl total', tot, flush=True)
        run_stream(gen_tmpl(), 'tmpl', tot); return
    if m == 'edit':
        d = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 2
        bad = mismatches(); cur = strip(bad[0][2])
        for b in [cur, html.unescape(cur), cur.strip('"\'')]:
            print('base', repr(b), 'd', d, flush=True)
            run_stream(gen_edits(b, d), 'edit', None)
        return
    if m == 'try': phase3(sys.argv[2]); return
    raise SystemExit('usage: pidpre.py dump|tmpl|edit [N]|try <string>')

if __name__ == '__main__': main()
