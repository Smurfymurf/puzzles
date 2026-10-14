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
