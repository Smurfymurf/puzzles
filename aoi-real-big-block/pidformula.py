#!/usr/bin/env python3
"""Verify Wattpad's duplicate-p-id formula over every paragraph of chapter 720888559.
first occurrence: md5(text) ; nth duplicate: md5(hex(md5(text)) + str(n)), n from 1."""
import hashlib, re, pathlib

html = pathlib.Path.home().joinpath("chapter.html").read_text("utf-8", "replace")
paras = re.findall(r'<p\s+data-p-id="([0-9a-f]{32})">(.*?)</p>', html, re.S)
if not paras:
    print("no <p data-p-id> found; len=", len(html), " has data-p-id:", "data-p-id" in html)
    raise SystemExit

seen, ok, bad = {}, 0, 0
for pid, body in paras:
    text = re.sub(r"<[^>]+>", "", body)
    for a, b in (("&quot;", '"'), ("&#39;", "'"), ("&amp;", "&")):
        text = text.replace(a, b)
    h = hashlib.md5(text.encode("utf-8")).hexdigest()
    n = seen.get(text, 0); seen[text] = n + 1
    exp = h if n == 0 else hashlib.md5((h + str(n)).encode()).hexdigest()
    if exp == pid: ok += 1
    else:
        bad += 1
        if bad <= 10: print(f"MISMATCH dup#{n} exp={exp} got={pid} {text[:50]!r}")
print(f"\nparagraphs={len(paras)}  formula_ok={ok}  mismatches={bad}")
print("VERDICT:", "FORMULA CONFIRMED (general)" if bad == 0 else "formula incomplete")
