# Cover image (optional)

A wide editorial cover in the dark "build in public" style. Default 5:2
(1200×480). Rendered with Pillow + bundled CJK fonts — no network required.

## When to make one

Only when the user wants it. Produce the essay first, then offer. If the user
already has a cover style they like, ask them to upload it and match its layout
rather than imposing this one.

## Design anatomy

```
┌──────────────────────────────────────────────────────────┐
│ ● BUILD IN PUBLIC · 2026.05                       NO. 003 │  top bar
│ A PUBLIC THINKING                                          │  gold label
│                                                            │
│ AI 时代，最该攒的                                           │  serif headline
│ 不是工具，是 数据                                           │  (gold keyword)
│                                                            │
│ 关于记录、复盘与 AI 教练的            大鱼 DayuBuilds        │  desc / byline
│ 一篇公开思考与产品共创邀请              @DayuBuilds          │
└──────────────────────────────────────────────────────────┘
```

- Dark base, blue-grey radial glow toward upper-right, faint grid, edge vignette.
- Serif headline (Noto Serif CJK Bold) with exactly ONE gold-highlighted word.
- Everything else muted grey/off-white. Restraint is the look.

## Running it

```bash
python3 scripts/make_cover.py \
  --line1 "AI 时代，最该攒的" \
  --line2 "不是工具，是@数据" \
  --label "A PUBLIC THINKING" \
  --topbar "BUILD IN PUBLIC · 2026.05" \
  --issue "NO. 003" \
  --desc1 "关于记录、复盘与 AI 教练的" \
  --desc2 "一篇公开思考与产品共创邀请" \
  --byline "大鱼 DayuBuilds" \
  --handle "@DayuBuilds" \
  --out "/mnt/user-data/outputs/cover.png"
```

## Marker syntax (inside --line1 / --line2)

- `@{word}` → render `word` in gold. The highlight — use it on the single most
  important word (usually the core noun from the thesis). One gold word per
  cover. Shorthand `@word` also works when followed by a space.
- `#{word}` → dim `word` to grey (de-emphasis). Optional; the validated cover
  dims "不是" with `#{不是}工具，是@{数据}`. Most covers don't need this.
- plain text needs no markers.
- braces are recommended (`@{数据}`) so the marker doesn't accidentally swallow
  the following characters.

## Choosing the headline

Pull it FROM the essay — the thesis line or the closer — not a generic phrase.
A good cover headline is short (two lines, ≤ ~9 Chinese chars per line), with the
gold word carrying the core noun. Examples that worked:

- `AI 时代，最该攒的` / `不是工具，是@数据`
- `所有短期红利` / `都是@假的`  (closer-derived)

## Sizes

- X / Twitter article header: 1200×480 (default, 5:2) works well.
- Other ratios: pass `--width`/`--height`; fonts auto-scale to height. Keep it
  wide-editorial (between 2:1 and 5:2) for this layout to look right.

## Matching an existing reference image

If the user uploads a cover they want matched: `view` it, identify the elements
(tag bar text, label, headline font feel, which word is highlighted and in what
color, byline placement), and map them onto the flags above. If their highlight
color isn't gold, the script currently fixes gold — note that to the user, or
edit `GOLD` in `make_cover.py` for a one-off.

## Fonts

Uses Noto Serif/Sans CJK and DejaVu Sans Mono, which are present in the standard
environment. If a font path is missing, the script falls back through a
candidate list; if all fail, install `fonts-noto-cjk` or point the candidate
lists at available fonts.

## Validated examples (copy-paste-ready)

These are real covers produced and approved by the user, listed as a reference
for consistent series style. Increment `--issue` for each new essay.

```bash
# NO.003
--line1 "AI 时代，最该攒的" --line2 "#{不是}工具，是@{数据}" --issue "NO. 003"
--desc1 "关于记录、复盘与 AI 教练的" --desc2 "一篇公开思考与产品共创邀请"

# NO.004
--line1 "你缺的从来不是知识" --line2 "是先动起来的@{勇气}" --issue "NO. 004"
--desc1 "关于 AI 学习、启动成本与" --desc2 "不设限的勇气的一篇公开思考"

# NO.005
--line1 "你不是没机会" --line2 "只是在用胆量代替@{预判}" --issue "NO. 005"
--desc1 "关于创业决策、机会识别与" --desc2 "先胜而后求战的一篇公开思考"
```

Pattern: line1 is the setup (≤8 Chinese chars), line2 is the payoff with ONE
`@{gold_word}` at the end. desc1+desc2 together form "关于X、Y与Z的一篇公开思考".
