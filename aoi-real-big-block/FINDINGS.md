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
