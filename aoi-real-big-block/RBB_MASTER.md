################################################################################
# REAL BIG BLOCK — MASTER DIARY  (single source of truth, HANDOVER-READY)
# Puzzle : Aoi Nakamoto "Real Big Block" (Quizchain2 block 77, STAGE 2)
# Target : 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W   0.777 BTC   STATUS: OPEN
# Updated: 2026-10-13   (machine being restarted; NOTHING RUNNING after boot)
################################################################################

========================= 0. CURRENT STATE / READ FIRST =========================
TWIST IS LOCATED. X IS NOT FOUND.

- Mechanism is airtight: Wattpad para 78's data-p-id does NOT match md5(its text),
  and it is the SOLE mismatch in 273 paragraphs -> para 78 was edited after its id
  was stamped; the pid is md5(original para 78 = X). md5(X)=8b71bade9685d3388455b06a0d.
- X itself is UNFOUND. ALL word-shaped X hypotheses are DEAD (see section 8).
- x12 (5-word topic model) was RUNNING on the BUGGY script (~15% done, ~13h total).
  A machine restart KILLED it; that script has NO resume. It did NOT complete.
- Two scripts are WRITTEN + READY, NOT YET RUN:  ~/x_what2.py ,  ~/hunt_x12b.py

NEXT ACTIONS, IN THIS ORDER (do NOT run them together):
  1) ~/x_what2.py   ~10 min, needs ALL cores. Tests if X is a What?-family string.
       nohup ~/venv312/bin/python3 -u ~/x_what2.py > ~/x_what2.out 2>&1 &
       tail -f ~/x_what2.out
     -> if "FOUND" appears, jump to section 11-FOUND.
  2) if no match: ~/hunt_x12b.py   ~1.6 h, uses cores-1, live ETA + resume.
       nohup ~/venv312/bin/python3 -u ~/hunt_x12b.py > ~/x12b.out 2>&1 &
       tail -f ~/x12b.out
  3) if both empty -> work OPEN LEADS B/C/D/E (section 9).

============================= 1. OBJECTIVE ======================================
Recover the exact source string the author hashed 2019-07-30, run the certified
pipeline, get the key, sweep 0.777 BTC. Author = AoiNakamoto (pseudonymous),
~90 self-funded blocks Apr-Oct 2019 on r/bitcoinpuzzles + r/Grycoin. All solved
except two; Block 76 swept 2026-08-17; only Real Big Block remains.

============================= 2. ADDRESSES & CONSTANTS ==========================
TARGET      14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W   (stage 2, OPEN, funded-unspent)
SUPERSEDED  1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC   (pre-rehash 2019-07-24, empty)
STAGE1 REF  19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN   (solved 2019-08-03)
STAGE1_MD5  9dd2efb9bc976c2095bd534d7b8d431c
BLOCK76     13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd   (0.077 BTC, SWEPT 2026-08-17)
CLECZC_ESC  1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi   (separate solved block; convention probe)
P78_PID     8b71bade9685d3388455b06a0d            (md5 of the ORIGINAL para 78 = X)
md5('"What?"') = 184826be0ea6837abb5851807f7a9e2b (current para 78; NOT the pid)

============================= 3. CERTIFIED PIPELINE ============================
source bytes -> MD5 -> 16-byte digest (128-bit entropy) -> BIP39 12 words ->
PBKDF2-HMAC-SHA512("mnemonic",2048,64) -> BIP44 m/44'/0'/0'/0/i (i=0..5) ->
compressed pubkey -> HASH160 -> Base58Check P2PKH.
RULE (certified Stage 1): for each paragraph whose FIRST letter is NOT in
{I,T,A,S,M}: lowercase first letter, uppercase LAST letter; then join paragraphs.
Stage-1 join = "\n\n". Reproduces 19TbyN5 at idx 0 exactly.
CERT: ~/aoi.py selftest -> "SELFTEST OK". Also certified vs author's vector
entropy 2941774a2abec9f30c7d6777d1d53d91 -> WIF L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex idx 1.
IMPL NOTES: MD5 over UTF-8; Stage-1 source was ISO-8859-1 HTML, para break "<br><br>"
(a lone "<br>" is NOT a break); flip uses first/last ALPHABETIC char (skips quotes).

============================= 4. SOURCE TEXT (CANONICAL BYTES) ==================
Source = Wattpad chapter "Second" id 720888559 by AoiNakamoto.
URL https://www.wattpad.com/720888559-second  modifyDate 2019-07-23 (< funding 2019-07-30).
Canonical bytes: API storytext, split on <p>, NO per-para strip,
"\n\n".join + trailing "\n" == 45,451 chars (== API declared length).
273 paras; 6 NBSP (paras 90,125,126,196,257); 10 internal <br> (paras 63,73,121,124,
146,160,184,189,193,213); straight quotes; no entities.
LOCAL FILES: ~/aoi_paras.json + ~/second.json = these bytes (rebuilt by ~/fix_paras.py).
Wattpad stores <p data-p-id="<32hex>">content</p>; id == md5(stripped content).
BUG FIXED: earlier fetches stripped 13 trailing spaces -> 45,438 not 45,451.

============================= 5. AUTHOR QUOTES ==================================
2019-07-25 "When I posted the real big block at the Wattpad site, I added extra line
  breaks between paragraphs. This information is needed to solve the block."
2019-07-28 "...The solution you need to hash with has only one line break between
  paragraphs, which is one 13 and one 10 in ASCII." (PRE-rehash escrow 1EFojc)
2019-07-30/31 "Took back the funds ... because I wanted to remove one of the twists I
  had. The block is now slightly easier. It is also hashed with two line breaks
  between paragraphs now."  => current text still carries >=1 twist.
2019-08 "I have lost any information on the solution of that one."
2019-08-01 confirms layout = "13 10 13 10".
Style: twists are small CASE CHANGES (block 29 "voice"->"vOIce"). NO md5 prefix for RBB.

============================= 6. CHAPTER SELF-DESCRIPTION (paras 226-246) =======
228 "the letters I,T,A,S,M as first letters"; 229 "All paragraphs except for four,
which start with F F and W W"; 230 points at the four = Finney quote (231-235,
F F W I W); 236 "look at the last letter of each of these" -> STNM (237); 241 "WW
obviously is UUUU or 'four U, for you'". FFWW groups at 5-8, 93-96, 168-171.
Anomalies: "VIrgin"(128), "BItcoin"(136), NBSPs, meta block.

============================= 7. *** BREAKTHROUGH: para 78 *** ==================
Wattpad data-p-id == md5(stripped para content) for 272/273 paras (incl <b> headings).
ONLY mismatch = para 78:
  line 78 = <p data-p-id="8b71bade9685d3388455b06a0d">"What?"</p>
  md5('"What?"') = 184826be0ea6837abb5851807f7a9e2b  (NOT the pid)
=> para 78 EDITED after its id was stamped; pid = md5 of the ORIGINAL sentence X;
   md5(X)=8b71bade9685d3388455b06a0d.
Corroborated: e1976g, repo issue #39: "The only anomaly in the 'Second' chapter is
line 78 ... we need to find the sentence that unlocks this MD5 hash."
Cross-check: entropy 8b71bade... does NOT derive to target (idx 0..200000, aoi + bip_utils).
KEY INFERENCE (elevates lead C): chapter modifyDate 2019-07-23 PREDATES the 2019-07-30
hash. A data-p-id is stamped once at creation and never updated, so the mismatch only
proves para 78 was edited AT SOME POINT. Since the last edit predates the hash, the
text the author actually hashed very likely contained the CURRENT "What?" -> the pid
may be a STALE-EDIT ARTIFACT / red herring, not the twist.
X HUNT STATUS: NOT FOUND. Archives empty (Wayback/Common Crawl/archive.today) -> X is
a pure preimage, not recoverable from the web.

============================= 8. DEAD ENDS (CHECK FIRST) ========================
REPO (all 0 match): unmodified/serializations(~150k); rule on groups+quote(16);
2^17 subsets x18(2.36M); selectors/browser-copy/invisible/encodings(~1.83M);
2019 reader-copy(12,848); Common Crawl indent(3,030); EVERY contiguous span>=2 paras
(1,469,908); bounded 2-edit NBSP+join(221,520); 2-edits invisible@2joins/insert+case
16 bases(48,379,696); Finney-group perms + N-chunks(17,921); chapter-dictated rule
(~1,200); brainwallet(96); ALL single-char edits 40 bases(266,038,400).
US (all 0): keep-set core 2^22; subset24 2^24; paragraph spans; char sentence-spans;
group/quote keep-flip; rule subsets; 1-char edits; NBSP/CR/quote/dash norm; unit
variants; br-structure on CORRECT bytes; wide on CORRECT bytes; drop/dup/empty78;
cleczc span+flip.
X PREIMAGE (all 0): every chapter sentence; every run of 1-5 sentences; every char
substring (len 3..140); every paragraph (raw/flip/noquote); Finney sentences(236);
author Wattpad sentences(6026/35 parts); author Reddit sentences(3626); 370k wordlist
"W?"; What-templates+decorations; 1-3 word combos full vocab (hunt_x9); drop/dup/empty78;
4-word top600 (hunt_x10b); Tatoeba 2,038,719 sentences; p-id-as-entropy idx0..200000;
What?-decorations (old, single-thread).
B76 (all 0): author-vocab 1-2 word solution x tomi pairs (1.8e10); slice-1 correct bytes.

============================= 9. OPEN LEADS (ranked) ===========================
A. x12b = X as 1..5-word topic-model sentence (READY, ~1.6h)  [also x_what2 first]
B. char-level X preimage (only path if X is out-of-vocab >=5 words)
C. p-id RED-HERRING re-attack: assume hashed text = current "What?"; hunt the REAL
   twist in byte/case/join space -> lead E (2-char edits INSIDE a paragraph) untested.
D. Block 76 deeper: 3-word solutions x tomi (free md5 filters 1d / f8e).
E. 2-char edits INSIDE a paragraph (never swept).

============================= 10. SCRIPT POLICY (STANDING) =====================
ALWAYS write the OPTIMAL version FIRST TIME. Every runner must:
  - parallelise across (cpu_count-1) workers (mp.Pool), chunksize tuned
  - STREAM (never materialise giant Python sets -> x_what's set = 2.13e9 str = ~230GB)
  - be RESUME-capable (append done-units to a *_done.log; skip on restart)
  - print a LIVE progress + ETA line every 15s with flush=True; run under python3 -u
  - print total work up front; write FOUND to a *_FOUND.txt
LESSONS: hunt_x12.py had a DEAD outer SEP loop -> 8x redundant work (2.159e11 iters
instead of 2.708e10). x_what.py materialised 2.13e9 strings -> OOM. Clean per-iter
cost measured = 4.48e-6 s (4 md5 + join), i.e. 1.15e6 md5/s/core.

============================= 11. NEXT-RUN SCRIPTS (full source) ===============
--- ~/x_what2.py  (X = What?-family string; streaming + parallel; ~10 min all cores) ---
bases: what/what?/what!/what./what../what.../what?!/what!?/what??/what now?/what is
it?/what is this?/what is going on?/what happened?/what do you mean?/what did you
say?/what are you doing?/what the.../what's going on?/what's this?/huh?/so what?/what for?
Expands each to ALL case variants (131,616 words) x 7 pre x 8 post x 289 decoration
suffixes = 2,130,073,344 candidates; md5 each + md5(flip). Source is on disk.

--- ~/hunt_x12b.py  (X = 1..5-word topic-model sentence; fixed 8x; ~1.6h; resume+ETA) ---
V = 70 words (what/whats/is/are/a/an/the/that/this/it/you/do/does/mean/how/why/so/then/
and/of/to/in/for/about/exactly/really/now/turing/test/reverse/artificial/intelligence/
human/humanity/singularity/pass/fail/adopt/solution/problem/ways/make/sure/adoption/
opportunity/use/will/i/am/no/big/deal/already/familiar/most/one/back/mirror/fun/
experiment/know/course/oh/well/ok/okay/huh/say/again/wait)
SEP=[" ", ", "]; WRAP=[('"','?"'),('"','"'),('"','!'),('','?')]; 1..5 words; TOTAL
27,082,862,170 inner iters. Source is on disk.

--- 11-FOUND ---
If either prints FOUND <string>: substitute it as para 78, rebuild the canonical
45,451-byte text, and run the certified pipeline (~/aoi.py) sweeping idx 0..5.
Check the resulting addresses against TARGET 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W.

============================= 12. SCRIPTS INVENTORY ============================
~/aoi.py (certified solver)  ~/fix_paras.py (rebuild canonical bytes)
~/aoi_subset24.py  ~/hunt_x9.py  ~/hunt_x10b.py  ~/hunt_x11.py  ~/hunt_x12.py (buggy, killed)
~/x_what.py (buggy/OOM)  ~/x_what2.py (READY)  ~/hunt_x12b.py (READY)
~/b76.py  ~/b76_search.py  ~/x_tatoeba.py  ~/x_corpus.py  ~/x_wide.py

============================= 13. RUN LOG ======================================
2026-10-12  fixed base-byte bug -> canonical 45,451 ; keep-set/subset24 -> 0
2026-10-12  found para-78 p-id anomaly ; X hunt begun ; hunt_x9 miss ; x10b launched
2026-10-12  wide on CORRECT bytes -> 0
2026-10-13  br-structure on CORRECT bytes -> 0 ; hunt_x10b (X<=4 words) -> 0
2026-10-13  confirmed pid=md5(stripped content) incl headings ; archives empty
2026-10-13  Tatoeba 2.04M sentences -> 0 ; p-id-as-entropy idx0..200000 -> 0
2026-10-13  b76 author-vocab 1-2 word pairs (1.8e10) -> 0
2026-10-13  clean cost 4.48e-6 -> OLD x12 13h total (~15% done, 10h left)
2026-10-13  found 8x dead-loop bug in hunt_x12 ; wrote hunt_x12b (fixed, resume, ETA)
2026-10-13  found OOM risk in x_what (2.13e9-str set) ; wrote x_what2 (stream+parallel)
2026-10-13  MACHINE RESTART -> x12 killed (no resume) ; nothing running on reboot
2026-10-13  NEXT: run x_what2 (~10m) then hunt_x12b (~1.6h) ; then leads B/C/D/E
################################################################################

### [2026-10-13 12:20:11] MASTER DOC rewritten as clean handover; restart kills x12; next = x_what2 then x12b
rbbrun: command not found: MASTER DOC rewritten as clean handover; restart kills x12; next = x_what2 then x12b

### [2026-10-13 14:40:33] x12b (1..5-word topic vocab, 27.08e9 iters) -> NO MATCH. x_what2 (2.08e9 What?-family) -> NO MATCH.
rbbrun: command not found: x12b (1..5-word topic vocab, 27.08e9 iters) -> NO MATCH. x_what2 (2.08e9 What?-family) -> NO MATCH.

### [2026-10-13 14:40:39] A-paths EXHAUSTED. Next = Lead C (p-id red-herring; modifyDate predates hash) + Lead E (2-char edits inside a paragraph; untested, single-char already 0). BEWARE: 2-char full-pipeline ~6e8 cands = ~15h; design for optimal-first-time.
rbbrun: command not found: A-paths EXHAUSTED. Next = Lead C (p-id red-herring; modifyDate predates hash) + Lead E (2-char edits inside a paragraph; untested, single-char already 0). BEWARE: 2-char full-pipeline ~6e8 cands = ~15h; design for optimal-first-time.

### [2026-10-13 14:42:47] x_what2 -> 0 (2.08e9) ; x12b -> 0 (27.08e9) ; A-paths exhausted ; NEXT = Lead C/E 2-char edits (design-first)
rbbrun: no such file or directory: x_what2 -> 0 (2.08e9) ; x12b -> 0 (27.08e9) ; A-paths exhausted ; NEXT = Lead C/E 2-char edits (design-first)
