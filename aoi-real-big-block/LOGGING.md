# LOGGING PROTOCOL (standing)
1. NOTHING runs >60s without a RUNLOG.md line BEFORE it starts (status=started).
2. Every run gets a row on completion: result, wall, and a NEGATIVES.md table row if 0.
3. Commit + push after every completed run and at least every 30 min while a job runs.
4. Every new script goes into the repo the moment it runs (no local-only scripts).
5. Every new external fact (author post, tx, address, thread) goes into CLUES.md with a source URL.
6. Never re-run something whose row already says a result; check RUNLOG.md first.
