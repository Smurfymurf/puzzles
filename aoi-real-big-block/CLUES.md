# RBB CLUES — the author's own words (single source of truth)

READ THIS BEFORE RUNNING ANYTHING. NEGATIVES.md records what has already been tried;
this file records what the author actually said. Every row carries a source.

Puzzle : Aoi Nakamoto "Real Big Block" = Quizchain2 block 77, STAGE 2
Target : 14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W  (0.777 BTC, funded 2019-07-30, OPEN)
Source : https://www.wattpad.com/720888559-second  (chapter "Second", 273 paragraphs)
Author : pseudonymous; claims to be an AI ("Artificial Omnipotent Intelligence");
         ~90 self-funded blocks Apr-Oct 2019; all solved except this one.

## C0. THE FORMAT — author's own words (MOST IMPORTANT)
Grycoin block 2 was posted explicitly "to give a simple example for the format used
in both phases of block 77".  SRC: reddit.com/r/Grycoin/comments/cleczc/grycoin_block_2
- "people are supposed to keep the whole long text and change only a couple of letters
   in their capitalization."
- "if the letter 'n' at the end of the last paragraph was part of the solution, you
   would be expected to change it to 'N' and write 'capitalizatioN'."
- "if ... the 'I' at the beginning of the previous paragraph was one of them, you would
   be expected to change that 'I' as well to a 'i'."
- "you would end up changing 'I' to 'i' and 'himself' to 'himselF'."
- "do that for all the paragraphs where you recognize the signs. And keep the rest
   completely unchanged."
- "Start with the first 'I' and stop with the period after 'method', with no spaces or
   line breaks before or after that included in the hash."
- "First three digits of MD5 hash are 3c6."  /  unchanged-text hash: 7759227 (first 7)
=> FORMAT = flip first+last letter of the paragraphs that DO NOT carry a "sign".
   Hash span with NOTHING before/after.

## C1. WHAT A "SIGN" IS — stated in the puzzle text itself
Chapter Part III ("Second Identity") IS the author's Stage One walkthrough, in prose:
- "The letters I, T, A, S, and M as first letters of each paragraph of this post."
- "All paragraphs except for four, which start with F F and W W."
- "we are directed to look at the last letter of each of these"  -> STNM
- "I STNM."  /  "Nm ST ... Exactly the same signature."
- "WW obviously is UUUU or 'four U, for you'. I leave it as an exercise ... who FF is."
- "The first four and last four words of the paragraph hinting at the solution." -> "Today, I"
Stage One pointer (author, r/Grycoin ca6jxv): the post's own line "I recognize the signs."

## C2. THE CHAPTER REPLICATES THE DEVICE
- 0-based 19  : "I recognize the signs."   (same pointer line as the Finney post)
- 0-based 41  : "...Did anyone recognize the signs?"
- 3 planted FFWW quads: 0-based 4-7, 92-95, 167-170, each PRECEDED by an 'i' para
  (3, 91, 166) -> "I STNM" planted x3
- meta / spec block: 0-based 225-246
- mid-word capital anomalies: 127 "VIrgin", 135 "BItcoin", 208 "BITcoin"/"AHScoin",
  105 "WorldWideAbsoluteCarbonBudget"

## C3. LINE BREAKS / SEPARATOR
SRC: r/Grycoin chn8un + cgkpbb
- "When I posted the real big block at the Wattpad site, I added extra line breaks
   between paragraphs. This information is needed to solve the block."
- (pre-rehash) "...has only one line break between paragraphs, which is one 13 and one 10."
- update: "Took back the funds ... because I wanted to remove one of the twists I had.
   The block is now slightly easier. It is also hashed with two line breaks between
   paragraphs now."
- "I mean the second one. Hit enter twice. This displays in Ascii as 13 10 13 10."
=> HASHED separator = 13 10 13 10 (CRLFCRLF), nothing before/after.
   Pre-rehash escrow used 13 10. Removed twist is NOT the separator.

## C4. DIFFICULTY / HINTS
- "It is unlikely that anyone would be able to solve the real big block without hints."
- "You are on your own completely with this one."
- "Once someone figures out the format for the first stage, they will also have a big
   hint for the format of this second stage."
- solve odds rated "lower than that of humanity passing the reverse Turing test"
- expiry: charity + solution disclosure at 2022-07-07 or 200dMA $100/mbtc (never ran)

## C5. WALLET / INDEX
- chn8un #4: "I just noticed that the 7th private key in the list for this wallet
   contains the number 7 three times ... Maybe should have sent the funds to that
   address. But the first one also has some amazing properties..."
- author part 731219798: "I highlighted the '7' in the address... at the 7th digit
   counted from the end... this digit '7' is one of the keys to break this code."
- cgkpbb: lucky address 1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC - "a lucky number 7 close
   to the middle and the other numbers 2 and 8 are Fibonacci numbers ... two numbers 7
   in the private key ... letters Ao at digits six and seven"

## C6. PARA 77 / X
- Wattpad data-p-id = md5(paragraph). SOLE mismatch = 0-based 77 = `"What?"`
  pid 8b71bade9685d3388452bc4755b06a0d ; md5('"What?"') = 184826be0ea6837abb5851807f7a9e2b
- context: 76 "...I will use the opportunity to do a reverse Turing test." -> 77 `"What?"`
  -> 78 "Of course you know what a Turing test is..."
- 0-based 72 is malformed: two dialogue lines fused by NUL (<br>) + stray trailing
  apostrophe ("...can't change the past'")
- chapter modifyDate 2019-07-23 PREDATES funding 2019-07-30

## C7. AUTHOR'S OWN HASHING MISTAKES (documented)
- part 724275249: "I did not notice an extra line break when copypasting my string for
   hashing. An extra line break or an extra space completely messes up the hash."
   "Just make absolutely sure there is nothing before or after the string you are hashing."
- other documented: MD5/SHA256 algo confusion (tablet restart); TOMI field rename;
   wrong link taken for hashing

## C8. CONSTANTS
TARGET        14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W
SUPERSEDED    1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC
STAGE1 REF    19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN   STAGE1_MD5 9dd2efb9bc976c2095bd534d7b8d431c
raw chapter md5 db11a7fdba7b4867a24445a7a30709b8   certified base md5 47ff387425c1a283c22eac15f0268867
funding tx    a1916e7ed9eac3fcc56a55056328cb09d06925e2694f2e6720de12b228514d1f
P78_PID       8b71bade9685d3388452bc4755b06a0d

## C9. SOURCES (public)
- wattpad.com/720888559-second
- reddit.com/r/Grycoin/comments/cgkpbb/777_mbtc_quizchain_last_block
- reddit.com/r/Grycoin/comments/chn8un/real_big_block_discussion
- reddit.com/r/Grycoin/comments/cleczc/grycoin_block_2
- reddit.com/r/Grycoin/comments/ca6jxv/77_mbtc_quizchain2_block_77_stage_one
- reddit.com/r/bitcoinpuzzles/comments/chf8k2/very_hard_777_mbtc_quizchain_real_big_block
- transcripts archived: github.com/agntn/puzzles/tree/main/assets/sources/real-big-block
- Stage One md5 reproduced: github.com/floflo777/open-crypto-puzzles/issues/1

## C10. OPEN (see NEGATIVES.md D1-D5)
- the remaining twist (>=1) and X (para 77 preimage) are the only unknowns
- 2-char non-case edits at all positions (D3) never swept
