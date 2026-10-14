# PARKED WORK — do NOT re-derive. Run only on its TRIGGER.

## P1. toggle_all — 2-toggle case sweep  (PARKED 2026-10-14 13:08Z)
WHY PARKED: ETA ~6h; wanted the machine free for clue/insight work.
WHAT: every pair of case-flips over the ~35,825 flippable positions, certified base,
crlf2, no trailing.  Space C(35825,2) = 641,697,400.
MARGINAL VALUE: the ONLY uncovered case space left is "2 flips in DIFFERENT paragraphs"
 (2 flips inside one paragraph = already 0 / B3; <=3 at sign positions = already 0 /
 sign3; 1 non-case char anywhere = already 0 / B27).
SUPPORT: author says the format is "change only a couple of letters in their
 capitalization" (cleczc); block 29 solution changed exactly 2 letters.
STATE: ~/toggle_all_done.log = 736 units; resumable, nothing re-done. Script is NOT in
 the repo (local-only) - find its real path first.
RESUME:
    find ~ -maxdepth 3 -name "toggle_all.py"
    cd <that dir>
    nohup ~/venv312/bin/python3 -u ./toggle_all.py >> ~/toggle_all.out 2>&1 &
    tail -3 ~/toggle_all.out        # expect a live progress + ETA line
    ~/rlog T1 "toggle_all RESUME" "6.417e8" "running" "from 736 units"
FOUND -> ~/toggle_all_FOUND.txt -> feed to ~/aoi.py, sweep idx 0..5.
TRIGGER: run it IF (a) the E1-E6 insight tests are all negative AND (b) a free 6h window
 (overnight). Do NOT start it before finishing the cheap E-tests.
