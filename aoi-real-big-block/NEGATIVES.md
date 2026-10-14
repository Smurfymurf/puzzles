# RBB NEGATIVES LEDGER

Every hypothesis tested against the escrows, with space size. A negative is an asset: it
deletes a region of the (where x what-kind-of-change) product. Escrows checked: TARGET
14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W and pre-rehash 1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC.

## A. STRUCTURAL FACTS ESTABLISHED (verified, not assumed)

A1. data-p-id = md5(paragraph text). Verified on 1849/2067 paragraphs of the author's 33
    chapters. 218 mismatches, essentially all at DUPLICATED paragraphs; identical text AND
    identical raw HTML in the same chapter carry DIFFERENT pids. 30 of 33 chapters are 100%
    clean -> Wattpad storage is byte-faithful since 2019, NOT drifted.
A2. The para-77 pid (8b71bade...) is neither md5(raw), md5(decoded), nor any of 6643
    short transforms, tags, entities, neighbours, block-tails, decimal counters, dates or
    epochs. Mechanism unresolved: either pre-edit text (oracle) or paste bookkeeping.
A3. Chapter modifyDate 2019-07-23T23:12:04Z is 7 days BEFORE the 2019-07-30 funding.
A4. Author's own ASCII note: hashed separator is 13 10 13 10 (CRLFCRLF) between paragraphs.
A5. Rule certified: lowercase first alpha / uppercase last alpha for paragraphs whose first
    alpha is not I/T/A/S/M; reproduces Stage One escrow 19TbyN5... byte for byte.
A6. Meta block (III.2.b) decodes: FF/WW paragraphs -> last letters STNM -> "I STNM" /
    "Nm ST"; "WW is UUUU / four U, for you"; a signature device, not an instruction.
A7. Chapter text fully in hand (273 paragraphs, base md5 47ff387425c1a283c22eac15f0268867).

## B. TESTED AND NEGATIVE

| # | Hypothesis | Space | Result |
|---|---|---|---|
| B1 | untwisted bases: 4 joins x 3 trails | 12 | 0 |
| B2 | case toggles <=4 per word, 3 separators | ~1.1e7 | 0 |
| B3 | case toggles 2 per paragraph, crlf2 + crlf | 8.1e6 | 0 |
| B4 | case toggles <=3 at 544 paragraph first/last positions, crlf2 | 2.68e7 | 0 |
| B5 | NBSP subsets, VIrgin/BItcoin, BOM, exotic joins, WW->UUUU | ~1e3 | 0 |
| B6 | whole-string X: x_what2 | 2.08e9 | 0 |
| B7 | whole-string X: x12b (1-5 word topic vocab) | 2.7e10 | 0 |
| B8 | whole-string X: x_tatoeba | 2.04e6 | 0 |
| B9 | whole-string X: x_corpus, xcrack | small | 0 |
| B10 | whole-string X: xbrute <=7 chars over [a-z ] | 1.09e10 | 0 |
| B11 | pid preimage: single-word template grammar (quotes/entities/ws/case) | 4.03e7 | 0 |
| B12 | pid preimage: edit distance <=2 from 3 bases | 3.6e6 | 0 |
| B13 | pid preimage: quote+punct+tail+pretxt grammar + invisibles | 3.68e7 | 0 |
| B14 | pid preimage: multi-word quoted phrases, 139-word chapter vocab, <=4 words | 3.35e9 | 0 |
| B15 | entity-encoded bases (4 encodings x 2 rule orders x joins x trails) | 48 | 0 |
| B16 | 218 wrong pids vs 6643 suffix/prefix/tag/entity/idx transforms | 1.4e6 | 0 |
| B17 | wrong pid = md5(content + counter), numeric 1-7 digits | 2.2e7 | 0 |
| B18 | wrong pid = md5(content + date) / + epoch seconds / + epoch ms | 4.0e8 | 0 |
| B19 | wrong pid = md5(content + neighbour / structural context) | ~4e3 | 0 |
| B20 | wrong pid = md5(content + rest of pasted block, <=14 paras, 6 seps) | 1.8e4 | 0 |
| B21 | serialisation + rule sweep: br mapping, tag handling, joins, lead/trail,
      strip, empty-paragraph retention, entity mode, rule on/off, skip_quotes | 11520 | 0 |
| B22 | 2019 reader-page copy families (12 pages/prefixes, SSR indent, br splits, CRLF) | 1.28e4 | 0 |
| B23 | stored empty <p><br></p> editor-buffer copies, Common Crawl indent | 3030 | 0 |
| B24 | every contiguous span of 2+ paragraphs, 4 joins | 1.47e6 | 0 |
| B25 | bounded 2-edit: every NBSP subset; every pair of joins swapped | 2.2e5 | 0 |
| B26 | every pair of boundary edits on 16 certified bases (invisible chars / case) | 4.84e7 | 0 |
| B27 | every single-character edit across 40 base texts | 2.66e8 | 0 |
| B28 | every subset of 17 candidate paragraphs x 18 serialisations | 2.36e6 | 0 |
| B29 | rule the chapter itself dictates (para 227), 3 modes, both joins, indices 0-5 | 1.2e3 | 0 |
| B30 | Finney-pattern group permutations, first/last N-paragraph chunks | 1.8e4 | 0 |
| B31 | brainwallet readings (hash as privkey, 96 variants) | 96 | 0 |

B22-B30 by floflo777 / AppleLamps, cross-checked against our own base where applicable.

## C. WHAT THE NEGATIVES JOINTLY NARROW TO

- NOT formatting: B1, B21, B22-B26 close serialisation, tags, entities, whitespace,
  empty paragraphs and rule-choice degrees of freedom (including skip_quotes).
- NOT a case-only change: B2-B4 close case toggles at every scope we can define.
- NOT an appended/prepended string: B6-B10 close 3.5e10 whole-string candidates.
- NOT a 1-character edit anywhere: B27.
- NOT a boundary 2-edit: B25, B26.
=> The twist is a CONTENT deviation of >=2 characters, NOT case, NOT at a boundary, and
   NOT formatting. The only content anomaly ever identified is para 77.

## D. OPEN / UNTESTED (ranked)

D1. K paragraphs switched to the other side of the rule, K<=3 (structurally motivated:
    Stage One cannot distinguish "flip all non-sign paras" from "flip this set") | 4.15e6
D2. K=4 of D1 | 1.9e8
D3. 2-character edits at ALL positions (not just boundaries), one base | ~2e9
D4. para 77 pid preimage, >4-word phrases / different vocab | open
D5. Ask the Block 76 solver for the serialisation convention of a final Aoi block | free

- para77.py - 611,137 candidates (every 1- and 2-char edit of para 77 plus case/quote/punct/whitespace variants) spliced into the certified CRLFCRLF base and tested against BOTH escrows. 0 hits, 859.5s at 711/s. Closes the para-77 text axis.
- p77pid.py - 171 md5 variants of the para-77 text (all case combos, straight/curly/entity quotes, lead+trail tab/CR/LF/CRLF/NBSP/ZWSP/thin/narrow space, doubled spaces, escaped quotes, p-tag wrappers). None equals stored pid 8b71bade. Sanity md5('"What?"')=184826be reproduced. Stored bytes are neither a whitespace nor a case variant, so either an invisible codepoint outside the set or a stale pid from a longer pre-edit string. Para 77 reclassified as bookkeeping, deprioritised.

- unflip.py K<=3 - 3,354,168 candidates (up to 3 paragraphs switched to the other side of the rule), base md5 confirmed 47ff387425c1a283c22eac15f0268867. 0 hits, 2329s. Fourth consecutive clean sweep. Paragraph-level/letter-mask model now judged wrong, not under-searched.

- KEY FINDING: finney.txt has 17 paragraphs, exactly 5 flip (first letters F,F,W,W,[). The mask rule 'exclude a,i,m,s,t' is indistinguishable on this text from 'include only f,w' - the post has no other letters. Chapter meta decode already found planted F,F,W,W paragraph groups. Sign is likely content/initial based, not a broad letter mask.

- signs6 - 49,140 combos: 4095 subsets of the 12 FFWW quad paragraphs x 4 modes x 3 granularities, plus content-rule sets (f/w first letters, first-word set, quads+230 block, mirror paras 5/167). 0 hits. Quads are a repeated STNM label, not the sign set.
- NOTE: upperFirst is a near no-op (paragraphs already start upper / end lower); the repeated md5 db11a7fd is the unflipped base.
- OPEN HYPOTHESIS: STRUCT='br'. Author said the extra line breaks are 'needed to solve the block'; chapter has 10 internal br (stored chr(0)) and 6 NBSP. aoi.py has an unrun STRUCT='br' mode that re-segments paragraphs. All 4.19M masks assume STRUCT='p'.

- signs8 - STRUCT='br' (283 paragraphs) with rule x 4 modes: 0 hits. Also p-mode flipping the 10 internal-br paragraphs and the 6 NBSP paragraphs, 4 modes each: 0 hits.
- OBSERVATION: br/NBSP paragraphs carry the author's construction notes ('Satoshi' anagram of 'THOMAS', nonces I and M, HAL=IBM, 'the third nonce'). Semantically loaded, mechanically negative.
- OPEN: rule FORM (which letter of a paragraph is read) has never been swept - only the rule SET (which letters).

- signs7 - all 262,143 subsets of the 18 distinct LAST letters: 0 hits. DISJOINT=False (flipped stnmy vs unflipped egsssgtnsnoy overlap). No single-feature rule can be correct.
- signs9 - only para_first / firstword_first / firstsent_first are separable on Stage One, all giving the same exclude set 'aimst' and identical chapter histograms. Anchor is not the variable.
- OPEN: skip_quotes. Stage One has ZERO quote-initial paragraphs; the chapter has 63. aoi.py hardcodes skip_quotes=True in every COMBOS entry, so the 4.19M sweep covers only one branch.


=== SESSION: rule space closed; pid CONFIRMED REAL; twist style identified ===
NEGATIVES (all 0 hits):
- conj3: OR and XOR of first-letter sets {f,w,e}, {f,w}, {a,i,m,s,t} against ALL
  262,144 last-letter subsets. 6 passes, ~58 s each, clean.
  => the entire boolean {first-letter, last-letter} rule space is now negative
     (single-feature, AND, OR, XOR). mask2 remains the only open member.
- pid-vs-bookkeeping: 40+ schemes (numeric salts, parent pid 184826be, element
  wrappers, curly/straight quote variants, case variants, repeats) -> NONE match
  8b71bade9685d3388452bc4755b06a0d. The para-77 pid is a GENUINE pre-edit md5.
  => para 77 was really edited in place; X is real; the pid is a valid oracle.
  => SUPERSEDES the earlier 'bookkeeping, deprioritised' entry.
- pid matches NO paragraph in any trivial case form -> X is not a moved/duplicated para.

READING (the chapter is the author's own Stage-1 walkthrough):
- paras 226-246 state the rule in prose: signs = I,T,A,S,M as paragraph FIRST letters
  (227-228); flip the paragraphs that DON'T carry them (229); STNM = their last letters
  (235-236); 'I STNM' (238); 'Nm ST ... exactly the same signature' (239); WW =
  'four U, for you' (240).
- Planted geometry: f,f,w,w blocks at 4-7, 92-95, 167-170, each PRECEDED by an 'i'
  paragraph (3, 91, 166) -> 'I STNM' planted three times. Meta's own copy is
  f,f,w,i,w (230-234) = five, with the I IN BETWEEN, per 229.
- Certified rule flips 119 of 273 paras vs 5 of 17 on Stage One. On a bitcointalk post
  'first letter not in signs' == 'the four inserted paragraphs'; on 273 paras of prose
  it is NOT. The rule is a proxy that only holds on Stage One.
- Dialogue at the defect: 76 (Aoi: '...reverse Turing test.') -> 77 '"What?"' ->
  78 (Aoi: 'Of course you know what a Turing test is...'). X was Tom's line.

TWIST STYLE:
- Abnormal mid-word capitals (block 29 style, 'voice'->'vOIce') at: 105/111
  WorldWideAbsoluteCarbonBudget, 106 FUCKFuck.../AndrewYangForPresident (hashtag-
  CamelCase, benign); 127 'VIrgin', 135 'BItcoin', 208 'BITcoin'+'AHScoin'.
  208 is the meta's own BIT/AHS wordplay (cf. para 212).
- OPEN: are the abnormal capitals 'the signs' for the chapter (flip exactly those
  paragraphs/letters) rather than the whole 119?

CONCLUSION: rule almost certainly right; the unknown is X (para 77 original line).

## Block 2 calibration (2026-10-14) — separator WON, address route inconclusive
WON (definitive):
- Span = first "I" .. period after "method", 10 paragraphs, no trailing, LF LF
  -> unchanged md5 = 7759227d7406... = author's published prefix 7759227. EXACT.
- CRLFCRLF gives e9970079..., i.e. WRONG. => separator is LF LF.
- flip FORM confirmed = toggle case of the first and last letter of a selected paragraph
  (matches the author's own description and our certified Stage One).
NOT RESOLVED (time-boxed):
- Solved prefix 3c6 is underdetermined (3 hex): 257 of 1.05e6 paragraph-flip combos match.
- NONE of those 257 reaches the prize address 1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi under
  any of: BIP39->BIP44 idx 0..200, raw privkey, sha256(md5), sha256(text), sha256(md5hex).
- So either the flip space is richer than "paragraph first/last" (author's own example
  flips 'himself' = an INTERIOR letter), or the winner's derivation step is exotic
  (author: "how to go from that to claiming the prize is not [obvious], not even to me").
- Our search text is proven correct by the unchanged-hash match, so this is a
  rule/derivation gap, not a text gap.
