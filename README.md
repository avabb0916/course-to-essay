# course-to-essay

A Claude [Agent Skill](https://code.claude.com/docs/en/skills) that turns a
course / lecture PDF (especially image-based "slide-deck" exports, Chinese or
English) into **one polished long-form essay** written in a chosen creator's
voice — and, optionally, a matching wide cover image.

It is built for the case where you've taken a course, internalized it, and want
to publish your *own* thinking based on it. The skill includes a dedicated
"authorial layer" step so the output reads as original work, not a reworded
deck.

## What it does

1. **Reads image-based PDFs** by rasterizing pages (ordinary text extraction
   returns nothing for slide/scan exports). Supports **multiple PDFs** on the
   same topic — synthesizes them into one essay.
2. **Digests** the material into thesis, the mainstream view it corrects,
   frameworks, cases, lines, and action steps.
3. **Adds your authorial layer** — your angle, your agreement/pushback, your
   first-person texture — so the essay is original rather than derivative.
4. **Writes** a complete essay in a creator's voice (default: Dan Koe /
   `thedankoe`), as a Markdown file ready for X / Substack / 公众号.
5. **(Optional) fills personal experience** — if you upload a career/bio
   document, the skill uses it to replace `【可替换…】` placeholders with real
   anecdotes, identity-obscured (company names, people, numbers all blurred).
6. **(Optional) generates a 5:2 cover image** in a dark editorial style.

## Validated on

This skill has been tested and iterated on real course PDFs:

- **AI 数据第一课** (一堂直播, 60p image-based PDF) → essay + cover NO.003
- **AI 上手第一课** (一堂直播, 49p image-based PDF) → essay + cover NO.004
- **机会预判** (3 PDFs combined, 114p total) → essay with real personal
  experience filled in + cover NO.005

## Install (Claude Code)

Clone this repo *as the skill folder itself* — do not nest it one level deeper.

```bash
# Personal install (available in all your projects)
git clone https://github.com/avabb0916/course-to-essay.git ~/.claude/skills/course-to-essay

# OR project install (committed with a repo, shared with teammates)
git clone https://github.com/avabb0916/course-to-essay.git .claude/skills/course-to-essay
```

The structure must be `…/.claude/skills/course-to-essay/SKILL.md` (SKILL.md
directly inside the `course-to-essay` folder). Then start a **new** Claude Code
session and run `/skills` to confirm it loaded. Claude will load it
automatically when you ask to turn a course PDF into an essay, or you can invoke
it directly.

## Optional: cover-image dependencies

The essay pipeline needs no extra packages. The **cover-image generator**
(`scripts/make_cover.py`) needs Pillow, numpy, and Noto CJK fonts:

```bash
pip install -r requirements.txt
# Chinese fonts (Debian/Ubuntu): sudo apt-get install fonts-noto-cjk
# macOS: install "Noto Serif CJK SC" + "Noto Sans CJK SC" via Font Book
```

If fonts are missing the script falls back through a candidate list; if all
fail, the essay is unaffected — only the cover step is.

## How to use

Upload or point to a course PDF and ask, e.g.:

- "把这份课程提炼成一篇 thedankoe 风格的推特长文"
- "turn this lecture PDF into a long-form essay"
- "这三份 PDF 是同一个主题的课程，帮我综合成一篇长文" (multi-PDF)
- "基于我的经历，模糊身份后充实文章里的真实经历部分" (personal experience)

The skill produces the essay, flags any `【可替换为你的真实经历：…】` placeholders
for you to fill with real personal detail (or fill them automatically if you
provide a bio document), and offers a cover image.

## Layout

```
course-to-essay/
├── SKILL.md                       # entry point: 5-phase workflow
├── README.md                      # this file
├── references/
│   ├── reading-course-pdfs.md     # Phase 1: how to read image-based PDFs
│   ├── extraction.md              # Phase 2: what to pull from the course
│   ├── authorial-layer.md         # Phase 2.5: how to make it original
│   ├── styles/
│   │   └── thedankoe.md           # default voice (add more here)
│   └── cover-image.md             # Phase 4: cover design + generator usage
├── scripts/
│   ├── fix_cjk_punctuation.py     # full-width punctuation cleanup
│   └── make_cover.py              # 5:2 cover image generator
├── requirements.txt               # pip deps for cover generator
└── .gitignore
```

## Adding another voice

Drop a new file in `references/styles/<name>.md` modeled on `thedankoe.md`
(voice thesis, structure, sentence habits, do/don't, one worked example). The
skill will use it when you ask for that creator's style.

## License

Personal project. Add a license file if you intend others to reuse it.
