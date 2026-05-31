#!/usr/bin/env python3
"""Convert half-width punctuation to full-width when it sits in a Chinese
context, while leaving English/code spans untouched.

Why: when writing Chinese prose it's easy to emit half-width , : ; ? ! ( )
next to Chinese characters, which renders cramped and looks unprofessional.
This fixes leftovers in a finished essay without harming English terms like
"Know-how", "Build in Public", or number ranges like "500-1000".

Usage:
    python3 fix_cjk_punctuation.py path/to/essay.md
    python3 fix_cjk_punctuation.py path/to/essay.md --dry-run   # report only
"""
import sys
import argparse


def is_cjk(c: str) -> bool:
    if not c:
        return False
    return ('\u4e00' <= c <= '\u9fff') or c in '“”‘’《》、，。！？；：（）「」'


PAIRS = {
    ',': '，',
    ':': '：',
    ';': '；',
    '?': '？',
    '!': '！',
}


def convert(text: str):
    out = []
    n = len(text)
    changes = 0
    for i, c in enumerate(text):
        prev = text[i - 1] if i > 0 else ''
        nxt = text[i + 1] if i + 1 < n else ''
        if c in PAIRS and (is_cjk(prev) or is_cjk(nxt)):
            out.append(PAIRS[c]); changes += 1
        elif c == '(' and is_cjk(nxt):
            out.append('（'); changes += 1
        elif c == ')' and is_cjk(prev):
            out.append('）'); changes += 1
        else:
            out.append(c)
    return ''.join(out), changes


def remaining_issues(text: str):
    """Report any half-width punct still adjacent to CJK (sanity check).
    Note: half-width punctuation INSIDE an English span like 'Know-how' is
    fine — we only flag cases where a CJK char is immediately adjacent."""
    issues = []
    n = len(text)
    for i, c in enumerate(text):
        if c in PAIRS or c in '()':
            prev = text[i - 1] if i > 0 else ''
            nxt = text[i + 1] if i + 1 < n else ''
            if is_cjk(prev) or is_cjk(nxt):
                issues.append(text[max(0, i - 1):i + 2])
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--dry-run', action='store_true',
                    help='report changes without writing')
    args = ap.parse_args()

    with open(args.path, 'r', encoding='utf-8') as f:
        text = f.read()

    fixed, changes = convert(text)
    leftover = remaining_issues(fixed)

    if args.dry_run:
        print(f"Would convert {changes} punctuation mark(s).")
    else:
        with open(args.path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print(f"Converted {changes} punctuation mark(s) → full-width.")

    if leftover:
        print(f"Note: {len(leftover)} half-width mark(s) still adjacent to CJK "
              f"(likely inside English terms — verify these are intentional):")
        for s in leftover[:20]:
            print("   ", repr(s))


if __name__ == '__main__':
    main()
