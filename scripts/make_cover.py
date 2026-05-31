#!/usr/bin/env python3
"""Render a wide editorial cover image (default 5:2) in the dark
"build in public" style, offline, using bundled/system CJK fonts.

Design anatomy (matches the validated reference):
  - dark base with a blue-grey radial glow toward upper-right
  - faint grid texture + edge vignette
  - top bar: ● TOPBAR (left)  /  ISSUE (right)
  - small gold section LABEL
  - two-line serif headline; mark the gold-highlighted word with a leading '@'
    e.g. --line2 "不是工具，是@数据"  → "数据" is gold
    a '~' marks a dimmed/grey word    e.g. "@不是~ 工具" (optional)
  - bottom-left two-line description
  - bottom-right byline + handle

Usage example:
  python3 make_cover.py \
    --line1 "AI 时代，最该攒的" \
    --line2 "不是工具，是@数据" \
    --label "A PUBLIC THINKING" \
    --topbar "BUILD IN PUBLIC · 2026.05" --issue "NO. 003" \
    --desc1 "关于记录、复盘与 AI 教练的" \
    --desc2 "一篇公开思考与产品共创邀请" \
    --byline "大鱼 DayuBuilds" --handle "@DayuBuilds" \
    --out /mnt/user-data/outputs/cover.png

Marker syntax inside --line1/--line2:
  @word   → render 'word' in gold (the highlight). One per cover is plenty.
  ~       → trailing '~' on a segment dims it to grey (de-emphasis). Optional.
Plain text needs no markers.
"""
import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersample then downscale for crisp edges

GOLD = (216, 180, 120)
GOLD_LABEL = (199, 154, 79)
WHITE = (244, 241, 234)
GREY = (139, 149, 161)
DIM = (120, 130, 142)
DGREY = (126, 136, 147)
TOPGREY = (154, 166, 178)

SERIF_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSerifCJK-Bold.ttc",
]
SANS_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
SANS_MED_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
]
MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]


def first_existing(cands):
    import os
    for c in cands:
        if os.path.exists(c):
            return c
    return cands[0]  # let PIL raise a clear error


def parse_segments(s):
    """Return list of (text, color).
    Markers (consumed, not printed):
      @{...} → gold highlight, e.g. 是@{数据}
      #{...} → dimmed grey,    e.g. #{不是}工具
    Shorthand without braces also works: @数据 highlights the run of
    non-space chars after @ up to the next marker/space. Braces are clearer
    when the highlighted word is followed immediately by more text."""
    if not s:
        return []
    segs = []
    i, n = 0, len(s)
    buf = ''

    def flush(color=WHITE):
        nonlocal buf
        if buf:
            segs.append((buf, color)); buf = ''

    while i < n:
        c = s[i]
        if c in '@#':
            flush()
            color = GOLD if c == '@' else DIM
            i += 1
            if i < n and s[i] == '{':
                j = s.find('}', i)
                if j == -1:
                    j = n
                word = s[i + 1:j]
                i = j + 1
            else:
                j = i
                while j < n and s[j] not in ' @#':
                    j += 1
                word = s[i:j]
                i = j
            segs.append((word, color))
        else:
            buf += c
            i += 1
    flush()
    return segs


def draw_title_line(d, x, y, segments, font):
    for text, col in segments:
        for ch in text:
            d.text((x, y), ch, font=font, fill=col)
            w = d.textlength(ch, font=font)
            # tighten after a full-width comma for a more compact look
            x += (w * 0.55 if ch == '，' else w) + 1 * SS
    return x


def draw_tracked(d, pos, s, font, fill, tracking=0):
    x, y = pos
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tracking * SS
    return x


def build(args):
    W, H = args.width, args.height
    sw, sh = W * SS, H * SS

    # --- background: radial glow upper-right ---
    yy, xx = np.mgrid[0:sh, 0:sw]
    cx, cy = sw * 0.80, sh * 0.40
    maxr = sw * 0.85
    dist = np.clip(np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / maxr, 0, 1)
    glow = np.array([36, 50, 63]); base = np.array([10, 13, 18])
    t = dist ** 1.15
    rgb = glow[None, None] * (1 - t)[..., None] + base[None, None] * t[..., None]
    darkfac = (np.clip((dist - 0.55) / 0.45, 0, 1) * 0.55)[..., None]
    rgb = rgb * (1 - darkfac) + np.array([5, 7, 10])[None, None] * darkfac
    img = Image.fromarray(rgb.astype(np.uint8), "RGB")
    d = ImageDraw.Draw(img, "RGBA")

    # --- grid ---
    step = 34 * SS
    for gx in range(0, sw, step):
        d.line([(gx, 0), (gx, sh)], fill=(255, 255, 255, 10), width=1)
    for gy in range(0, sh, step):
        d.line([(0, gy), (sw, gy)], fill=(255, 255, 255, 10), width=1)

    # --- vignette ---
    vdist = np.clip(np.sqrt((xx - sw / 2) ** 2 + (yy - sh / 2) ** 2) / (sw * 0.72), 0, 1)
    valpha = (np.clip((vdist - 0.58) / 0.42, 0, 1) * 0.5 * 255).astype(np.uint8)
    img = Image.composite(Image.new("RGB", (sw, sh), (0, 0, 0)), img,
                          Image.fromarray(valpha, "L"))
    d = ImageDraw.Draw(img, "RGBA")

    # --- fonts (scaled to canvas height so it works at any size) ---
    scale = H / 480.0
    serif = first_existing(SERIF_CANDIDATES)
    sans = first_existing(SANS_CANDIDATES)
    sans_med = first_existing(SANS_MED_CANDIDATES)
    mono = first_existing(MONO_CANDIDATES)

    def F(path, size):
        return ImageFont.truetype(path, int(size * scale * SS))

    f_title = F(serif, 74)
    f_label = F(mono, 14)
    f_top = F(mono, 13)
    f_desc = F(sans, 15)
    f_sig = F(sans_med, 19)
    f_handle = F(mono, 14)

    M = 56 * scale * SS  # left/right margin
    R = W * SS - 56 * scale * SS

    # top hairline + bar
    d.line([(M, 58 * scale * SS), (R, 58 * scale * SS)], fill=(255, 255, 255, 20), width=1)
    if args.topbar:
        d.ellipse([(M + 3 * SS, 42 * scale * SS), (M + 9.4 * SS, 48.4 * scale * SS)], fill=GOLD)
        draw_tracked(d, (M + 22 * SS, 38 * scale * SS), args.topbar, f_top, TOPGREY, 3)
    if args.issue:
        iw = sum(d.textlength(c, font=f_top) + 3 * SS for c in args.issue)
        draw_tracked(d, (R - iw, 38 * scale * SS), args.issue, f_top, (107, 119, 133), 3)

    # section label
    if args.label:
        draw_tracked(d, (M, 116 * scale * SS), args.label, f_label, GOLD_LABEL, 5)

    # title lines
    draw_title_line(d, M - 2 * SS, 160 * scale * SS, parse_segments(args.line1), f_title)
    if args.line2:
        draw_title_line(d, M - 2 * SS, 258 * scale * SS, parse_segments(args.line2), f_title)

    # description bottom-left
    if args.desc1:
        d.text((M, 405 * scale * SS), args.desc1, font=f_desc, fill=DGREY)
    if args.desc2:
        d.text((M, 429 * scale * SS), args.desc2, font=f_desc, fill=DGREY)

    # byline bottom-right
    if args.byline:
        bw = d.textlength(args.byline, font=f_sig)
        d.text((R - bw, 405 * scale * SS), args.byline, font=f_sig, fill=(232, 228, 220))
    if args.handle:
        hw = sum(d.textlength(c, font=f_handle) + 1 * SS for c in args.handle)
        draw_tracked(d, (R - hw, 431 * scale * SS), args.handle, f_handle, GREY, 1)

    out = img.resize((W, H), Image.LANCZOS)
    out.save(args.out)
    print(f"Saved {args.out} ({W}x{H})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--line1', required=True, help="title line 1; '@word' = gold")
    ap.add_argument('--line2', default='', help="title line 2; '@word' = gold")
    ap.add_argument('--label', default='', help="small gold section label")
    ap.add_argument('--topbar', default='', help="top-left tag")
    ap.add_argument('--issue', default='', help="top-right issue, e.g. NO. 003")
    ap.add_argument('--desc1', default='')
    ap.add_argument('--desc2', default='')
    ap.add_argument('--byline', default='')
    ap.add_argument('--handle', default='')
    ap.add_argument('--width', type=int, default=1200)
    ap.add_argument('--height', type=int, default=480)
    ap.add_argument('--out', default='/mnt/user-data/outputs/cover.png')
    build(ap.parse_args())


if __name__ == '__main__':
    main()
