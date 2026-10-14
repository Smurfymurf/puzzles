#!/usr/bin/env python3
"""Calibrate the author's exact convention against Grycoin Block 2 (known answers:
unchanged prefix 7759227, solved prefix 3c6).  Span = first 'I' .. period after 'method'."""
import hashlib

P = [
 "I thought I would write a bit about the format for block 77, giving a simple example for that.",
 "As is already clear from the reference to block 29, people are supposed to keep the whole long text and change only a couple of letters in their capitalization.",
 'For example, if the letter "n" at the end of the last paragraph was part of the solution, you would be expected to change it to "N" and write "capitalizatioN".',
 'For what it\'s worth, that "n" is not part of the solution, which is obvious to anyone able to recognize the signs.',
 "I expected otherwise, but actually not many people do recognize the signs in Satoshi's Bitcointalk post outing himself. Even after I explained the method used and the result in detail.",
 'On the other hand, if you were able to recognize the signs and thought that the "I" at the beginning of the previous paragraph was one of them, you would be expected to change that "I" as well to a "i".',
 'When you do that, you would end up changing "I" to "i" and "himself" to "himselF".',
 "Which would be the solution, once you do that for all the paragraphs where you recognize the signs. And keep the rest completely unchanged.",
 "I think this easy example should be enough to completely clear up the remaining problems with finding the correct format for both stages of block 77. Should not take too long until someone sees the light now. At least for the first stage...",
 "And it should be someone mining with the mind. While it may be possible to write a script for this, it should be faster to solve by the thinking only method.",
]

def flip(p):
    a = list(p); idx = [i for i,c in enumerate(a) if c.isalpha()]
    a[idx[0]] = a[idx[0]].lower(); a[idx[-1]] = a[idx[-1]].upper()
    return "".join(a)

seps = {"LF2": "\n\n", "CRLF2": "\r\n\r\n", "LF": "\n", "CRLF": "\r\n"}
for name, s in seps.items():
    raw = s.join(P)
    print(f"{name:6} len={len(raw):5} md5={hashlib.md5(raw.encode()).hexdigest()[:12]}")
    for i in range(len(P)):
        f = list(P); f[i] = flip(f[i])
        h = hashlib.md5(s.join(f).encode()).hexdigest()[:12]
        print(f"       flip[{i:2}] md5={h}   {P[i][:45]!r}")
