# FINDINGS


## SESSION — Wattpad corpus + author's own method (2-letter mid-word case change)

### HARD FACTS ESTABLISHED
1. Story 184148284 "Second" = 33 parts; our chapter 720888559 is a COMPILATION.
   All 33 parts scraped -> parts/*.html, ~/second_parts.json (2067 paras, ~150 KB).
2. Para-77 dialogue is UNIQUE to the chapter; absent from all other 32 parts, whole
   or as fragment. X never existed outside the chapter.
3. AUTHOR'S OWN METHOD (compilation 720895205):
   'Solution: just change the o and i in "voice" in the second sentence to "O" and
    "I", same method as in Block 2. Only two letters changed ...'
   => twist = change the CASE OF ~2 LETTERS, MID-WORD. Not a whole-paragraph flip.
   => consistent with the stated format: 'change only a couple of letters'.
4. Block 2 method = flip n->N and I->i = 2 letters on ONE paragraph = exactly our
   certified flip() (lower first / upper last) applied to a SINGLE paragraph.
5. Mid-word caps are an author HABIT across many parts (720895205:29, 742662804:8,
   761570746:15) and appear in questions too ('naMe'). Possible sign channel; not
   unique to our chapter.

### NEGATIVES (all clean)
- conj3: OR/XOR x {fwe,fw,aismt} x all 262144 last-letter subsets, 6 passes = 0.
  Entire boolean {first,last}-letter rule space now negative. mask2 = only open member.
- normalize family (8 rows: norm all/anom x {none,cert,quads}): all 0.
- pid = GENUINE pre-edit md5 (40+ schemes, no match) => X real, pid valid oracle.
- pid matches no paragraph anywhere, whole or as fragment.

### REFRAME (from fact 3/4)
- If the real op changes ~2 letters, our paragraph-flip sweeps OVER-flip (119 paras).
- Candidate: ONE target paragraph (or one letter pair), selected by the signs/STNM
  geometry, not by a first-letter mask.

### ARTIFACTS
parts/*.html, ~/second_parts.json, author_examples.txt, FINDINGS.md, NEGATIVES.md

## E1 — meta block (0-based 224-247) read as literal instructions
Operation stated by the author: flip FIRST letter (lower) + LAST letter (upper) of the
paragraphs that LACK a sign; the message appears in the flipped LAST letters.
signs = "I, T, A, S, and M as first letters of each paragraph OF THIS POST" (= the Finney
post). Message: STNM, + adjacent I = "I STNM"; matched to the genesis "Nm ST" signature.
FFWW = dedication (WW = UUUU = "four U, for you"; FF left open).
Technique stated: first four + last four words of the hint paragraph -> "Today, I".
CHAPTER REPLICATES THE DEVICE 3x (I + FFWW, last letters s t n m): 0-based 3-7, 91-95,
~167-172.
CRACK: the sign-set is defined against the Finney post, not the chapter. Using
{I,T,A,S,M} on a 273-para chapter is an ASSUMPTION (already shown underdetermined on
Stage One). Prime suspect for the remaining twist.

## X IS DEAD — para-77 pid is a duplicate-p-id artefact (2026-10-14)
Reproduced locally: md5('"What?"') = 184826be0ea6837abb5851807f7a9e2b and
md5('184826be0ea6837abb5851807f7a9e2b' + '1') = 8b71bade9685d3388452bc4755b06a0d = the
stored pid of 0-based para 77. Para 77 is the SECOND occurrence of '"What?"' (first is
0-based 33). Wattpad stamps nth duplicates as md5(hex(md5(text)) + n), n from 1 - which
matches our own NEGATIVES A1 observation that duplicated paragraphs carry different pids.
=> para 77 was never edited; the "missing sentence X" theory is DEAD.
=> the hashed text contains '"What?"'. Retire X leads: old B6-B14, x_what2, x12b, xbrute,
   xcrack, p77pid, para77 splice, pidphrase, hunt_x*.
Source: diginen43 comment 2026-10-13 (r/Grycoin/cgkpbb); independently reproduced here.

## X PERMANENTLY CLOSED — duplicate-pid formula verified general (2026-10-14)
pidformula.py: all 273 paragraphs of chapter 720888559 reproduce their stored pids with
  first occurrence: md5(raw content)   [NOTE: raw, NOT stripped]
  nth duplicate:    md5(hex(md5(text)) + str(n)), n from 1
RESULT: paragraphs=273  formula_ok=273  mismatches=0  -> FORMULA CONFIRMED (general)
Also re-confirms: 13 paragraphs carry a TRAILING SPACE that is part of the hashed bytes
(these were the 13 initial "mismatches" while we were wrongly .strip()ing). Trailing
spaces are load-bearing - keep them in the canonical hash input.
=> para 77 ('"What?"', 2nd occurrence; first is 0-based 33) was NEVER edited.

## CALIBRATION: separator is LF LF, NOT CRLFCRLF (2026-10-14)
block2cal.py, span = first "I" .. period after "method" (10 paragraphs, exactly as the
author specified), no trailing:
  LF2   len=1549  md5=7759227d7406  <-- MATCHES the author's published unchanged prefix
  CRLF2 len=1567  md5=e997007971f6  <-- does NOT
=> Grycoin Block 2 was hashed with "\n\n". The author's "13 10 13 10" note reflects his
   TOOL's display, not his input bytes.
=> our 2026-10-13 correction to CRLFCRLF is WRONG. Re-run key sweeps on LF LF.
Span + separator + no-trailing now all pinned against a known-good digest.
