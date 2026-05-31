---
name: course-to-essay
description: >-
  Turn a course/lecture PDF (especially image-based or "slide-deck" exports,
  Chinese or English) into a single polished long-form essay written in a chosen
  creator's voice (default: Dan Koe / thedankoe), optionally with a matching
  wide cover image. Use this skill WHENEVER the user uploads a course, lecture,
  webinar, training, or "直播/课程" PDF and wants an article, essay, newsletter,
  Twitter/X long-form post, blog post, 公众号 article, or "推特长文" out of it —
  even if they don't name a style. Also trigger when the user says things like
  "提炼成一篇文章", "写成 thedankoe 风格", "turn this lecture into an essay",
  "make a newsletter from this PDF", or asks for a cover image for such an
  essay. Do NOT use for simple "summarize this PDF" requests where the user just
  wants bullet points.
---

# Course PDF → long-form essay (creator voice)

This skill converts a course/lecture PDF into ONE complete, publishable
long-form essay in a named creator's voice, and (optionally) a matching cover
image. It exists because course PDFs are usually **image-based exports** that
ordinary text extraction can't read, and because a good essay is not a summary —
it is the author's own thinking, built on the course as input. The published
piece carries no attribution to the source, so it must read as genuinely
original work, not a reworded deck.

The job runs in phases: **read → digest → add your authorial layer → write →
(optional) cover.** Work through them in order. Two non-obvious phases carry the
quality: reading (rasterize — these PDFs hide text in page images) and the
authorial layer (Phase 2.5 — the step that makes the essay original rather than
derivative). Don't skip either.

---

## Phase 0 — Clarify intent (only if genuinely unclear)

Most of the time the upload + request is enough. Only ask if something material
is missing. Sensible defaults, so you rarely need to ask:

- **Voice/style**: default to Dan Koe (`thedankoe`). If the user names another
  creator, use `references/styles/<name>.md` if it exists, otherwise research
  that creator's structure first (see "Adding a new voice" below).
- **Language**: default to the **dominant language of the PDF**. If the PDF is
  Chinese, write Chinese; if English, English. Honor an explicit request to
  switch (e.g. "翻成英文版").
- **Cover image**: offer it, don't assume. Produce the essay first, then ask
  "要不要配一张封面图？" — unless the user already asked for one.
- **Length**: default ~1500–2500 words (Chinese) / ~1200–1800 words (English).
  A long-form essay, not a thread.

One question at a time, and only if it actually blocks you.

---

## Phase 1 — Read the PDF (rasterize, don't trust text extraction)

Course PDFs (exported from slides, Notion, jsPDF, scans) usually have **no real
text layer** — the words live inside page images. Verify, then read visually.

```bash
# 1. Inventory
pdfinfo "input.pdf"            # page count, producer (jsPDF/Canva/scan → image-based)
pdffonts "input.pdf" | head    # if fonts are "no/no" embedded or list is empty → image-based

# 2. Try text; if it returns ~nothing, the content is in images
pdftotext -layout "input.pdf" /tmp/t.txt; wc -l /tmp/t.txt
```

If text extraction is empty or garbled (the common case), **rasterize and read
the pages as images** in batches:

```bash
# Render pages N..M at 150 DPI (good balance of legibility vs tokens)
pdftoppm -jpeg -r 150 -f 1 -l 10 "input.pdf" /tmp/pg
ls /tmp/pg-*.jpg
```

Then `view` each rendered page. Read **every** page — the gold is scattered:
the framework diagrams, the case studies, and the punchy one-liners ("敲黑板说
重点", highlighted/colored text) are what make the essay good. Token budget:
~1,600 tokens/page at 150 DPI, so a 60-page deck ≈ 100K tokens if you read all
of it. For very long decks, read in batches of ~10–15 pages and take notes as
you go so you can release earlier pages from working memory.

Full PDF-reading tactics (scanned docs, garbled fonts, embedded images,
choosing DPI) live in `references/reading-course-pdfs.md` — read it if the PDF
fights back.

**Multiple PDFs on the same topic:** if the user uploads 2–5 PDFs covering the
same subject (e.g. different lectures in a series, or different speakers on the
same theme), read all of them and synthesize into ONE essay. Diagnose and
rasterize each PDF separately, then digest all the material together in Phase 2.
The authorial layer (Phase 2.5) becomes even more important here — with multiple
sources, you have more raw material to reorganize under your own angle rather
than following any single source's structure.

---

## Phase 2 — Digest the raw material (input, not content to relay)

As you read, capture (in a scratch note) the things you'll build an essay from.
Do not start writing until you have these. Mental model: the course is **input
you are learning from**, not a source you will summarize. The published essay is
the author's own thinking — the course's fingerprints (its section order, its
naming, its phrasing) must NOT be visible in the output. Capturing the material
faithfully here is what lets you depart from it deliberately later.

Capture:

1. **The core thesis** — the one belief the course argues for. (You will later
   decide whether you fully agree — see Phase 2.5.)
2. **The "wrong" mainstream view it pushes against** — almost every good course
   opens by correcting a widely-held assumption. A candidate tension for the
   essay. (Validated example: "people think they already understand data".)
3. **The frameworks / models** — named structures, step lists, "N不变M巨变",
   acronym models (e.g. ADAPTED 6+1), matrices. Capture them to *understand*
   them — NOT to reproduce them verbatim. See the rewrite rule in Phase 2.5.
4. **The concrete cases / stories** — examples, before/after, numbers, named
   people. Note which are course-specific (and thus traceable) vs. general.
5. **The quotable lines** — the punchlines the instructor emphasized. Treat
   these as someone else's words: paraphrase or transform, don't lift.
6. **The action steps** — what the course tells people to actually DO.

Detailed guidance + a checklist: `references/extraction.md`.

---

## Phase 2.5 — Build the authorial layer (the originality step)

**This is the step that turns a polished summary into the author's own essay.**
Skipping it produces competent-but-derivative writing that a reader (or the
course's creator) could fairly call a repackage. Do this before you write.

After digesting, step back and add YOUR layer on top of the material. Write a
few scratch notes answering:

1. **What do I actually think about this?** Where do I agree, and where would I
   push back, add a caveat, or sharpen? An essay with a spine takes a position —
   it doesn't just relay. Even mild, reasoned disagreement ("the course frames
   X as the cause; I'd argue it's a symptom of Y") creates real originality.
2. **What's my own angle / organizing idea?** Find a frame the course did NOT
   use. Re-derive the insight from your angle so the essay's architecture is
   yours, not the syllabus's. (A course taught 怕/远/乱 as three pain points →
   the essay can reframe the whole thing as "you're missing a ladder, not
   intelligence" and let the three points fall out of that.)
3. **Where do MY experiences / observations connect?** First-person texture is
   the strongest originality signal. Add lived observation: "I've watched smart
   people freeze at exactly this point." Where a *specific personal fact* would
   land best (a number, a named project, a personal anecdote), insert a clearly
   marked placeholder like `【可替换为你的真实经历：…】` rather than inventing a
   verifiable-sounding fact. Tell the user about these at the end so they fill
   them with real experience. NEVER fabricate specific checkable facts (fake
   company names, stats, events) and present them as the author's own.
4. **What can I add that the course didn't?** A connection to another domain, a
   counter-example, a sharper metaphor, a "here's the part nobody mentions."
   This is the clearest proof you metabolized the idea rather than moved it.

Full method, with worked before/after examples: `references/authorial-layer.md`.

Output of this phase: a short note stating your thesis-in-your-words, your
organizing angle, your 1–2 points of agreement/pushback, and where personal
texture goes. THAT note — not the course outline — is what you write from.

---

## Phase 3 — Write the essay in the chosen voice

Read the relevant voice file FIRST, then write. Default:
`references/styles/thedankoe.md`. The voice file is authoritative for structure,
sentence rhythm, and dos/don'ts.

**Write from your Phase 2.5 note, not from the course outline.** If you find
yourself walking the course's sections in order, stop — that's the derivative
trap. Your organizing angle drives the structure; the course material is dropped
in where it serves your argument.

The essay must be a **standalone artifact** (a file the user will publish), not
an inline chat answer. Create it as a Markdown file in `/mnt/user-data/outputs/`
so the user can paste it into X / Substack / 公众号.

Universal rules regardless of voice:

- **One essay, not a thread.** No "1/12" numbering. It reads top to bottom.
- **Originality is non-negotiable** (the user publishes this as their own
  thinking, with no attribution to the course):
  - Lead with YOUR angle from Phase 2.5, not the course's framing.
  - **Rewrite every framework in your own words and ideally your own structure.**
    Don't reproduce a named model's exact labels/order as-is. Rename, re-group,
    or re-derive it. If the course's "3不变3巨变" is the skeleton, your essay
    should not visibly have a "3-and-3" skeleton.
  - **Never lift the instructor's signature lines verbatim.** Transform them, or
    write your own. A memorable course line is the single most recognizable
    fingerprint — paraphrase it into your own voice.
  - **Carry a real point of view** — at least one place where the author agrees-
    and-extends or pushes back, so the piece argues rather than relays.
  - **Add something the course didn't** — an outside connection, counter-example,
    or sharper metaphor. (See `references/authorial-layer.md`.)
- **Lead with a relatable problem + lived experience**, not a definition.
- **Translate jargon into plain language.** A course says "DIKW模型"; the essay
  explains the idea in plain words and may not even keep the term.
- **Drop all classroom scaffolding.** Cut "【互动】大家猜猜", "预热思考题",
  "扫码", page references, "今天我会讲4个话题" — none of it belongs in an essay.
- **Don't fabricate.** First-person texture is great, but specific checkable
  facts the author would have to own (named projects, numbers, events) go in as
  `【可替换为你的真实经历：…】` placeholders for the user to fill, never invented.
- **Punctuation discipline (CRITICAL for Chinese):** in Chinese prose use
  full-width punctuation （，。：；？！（）「」） consistently. A frequent failure
  is emitting half-width `,` `:` `?` `(` `)` next to Chinese characters, which
  looks cramped. Keep half-width punctuation ONLY inside English/code spans
  (e.g. `Know-how`, `Build in Public`, `500-1000`). Run
  `scripts/fix_cjk_punctuation.py` on the finished file to catch leftovers.
- **End on a memorable single line** — the closer the reader screenshots. Make
  it yours, not the instructor's.

After writing, run the punctuation fixer, then do the **derivative check**: skim
the draft beside your course notes and ask "could the course's creator point at
any paragraph and say 'that's just my slide reworded'?" If yes, rewrite that
paragraph from your angle. Then re-read once for rhythm.

```bash
python3 scripts/fix_cjk_punctuation.py "/mnt/user-data/outputs/<essay>.md"
```

When you `present_files`, also tell the user where the `【可替换…】` placeholders
are so they can drop in real personal experience.

---

## Phase 3.5 — (Optional) Fill placeholders with the user's real experience

If the user has uploaded a **personal experience document** (resume, career
timeline, memoir, or any biographical text), use it to fill the `【可替换…】`
placeholders with real, identity-obscured anecdotes. This is optional but
dramatically increases the essay's authenticity and persuasion.

**Process:**

1. Read the experience document fully.
2. For each placeholder, find the life episode that best matches the essay's
   argument at that point. Prioritize episodes with a **clear decision moment**
   and a **visible consequence** — these make the strongest stories.
3. **Obscure identity:** company names → "某SaaS公司" / "一家行业明星公司";
   personal names → "一位前辈" / "当时的负责人"; specific salary/compensation
   numbers → vague descriptions; dates → omit or round to "几年前". The rule:
   a reader who doesn't know the author should NOT be able to identify the
   specific companies or people involved.
4. **Keep the emotional truth:** the feelings, the stakes, the lesson learned —
   these are what make it real. Strip identifying details, keep the human core.
5. Replace the placeholder text entirely (remove the `【可替换…】` brackets too).
   Then confirm to the user what you used and how you obscured it, so they can
   verify before publishing.

**Never** add details from the experience document that the user didn't ask you
to use. The document is a private input — only draw from it when explicitly
filling placeholders or when the user asks you to "充实真实经历".

---

## Phase 4 — (Optional) Matching cover image

Only if the user wants one. Default format is **5:2** (e.g. 1200×480), the
"build in public" dark editorial style we validated. If the user has an existing
cover they like, ask them to upload it and match its layout (top tag bar,
serif headline with one gold-highlighted keyword, byline bottom-right).

The generator is `scripts/make_cover.py` — it renders with Pillow (no network
needed) using the bundled CJK fonts. Read `references/cover-image.md` for the
full parameter list, the design anatomy, and how to match a reference image.

```bash
python3 scripts/make_cover.py \
  --line1 "AI 时代，最该攒的" \
  --line2 "#{不是}工具，是@{数据}" \
  --label "A PUBLIC THINKING" \
  --topbar "BUILD IN PUBLIC · 2026.05" \
  --issue "NO. 003" \
  --desc1 "关于记录、复盘与 AI 教练的" \
  --desc2 "一篇公开思考与产品共创邀请" \
  --byline "大鱼 DayuBuilds" \
  --handle "@DayuBuilds" \
  --out "/mnt/user-data/outputs/cover.png"
```

`@{word}` marks the gold-highlighted word in a title line; `#{word}` dims a word
to grey. Pick a title line FROM the essay (a thesis line or the closer), not a
generic phrase.

---

## Adding a new voice

If the user wants a creator the skill doesn't have yet:

1. Search the web for that creator's writing structure, signature moves, and a
   couple of representative pieces (their own site/newsletter beats secondhand
   summaries).
2. Distill into `references/styles/<name>.md` following the shape of
   `thedankoe.md`: thesis-about-the-voice, the structure they use, sentence-level
   habits, a short do/don't list, and one worked mini-example.
3. Then write the essay using it. The new file is reusable next time.

---

## Quick reference

| Phase | You do | Read |
|-------|--------|------|
| 1 Read | rasterize PDF pages, view each (supports multiple PDFs on same topic) | `references/reading-course-pdfs.md` |
| 2 Digest | thesis, wrong-view, frameworks, cases, lines, steps | `references/extraction.md` |
| 2.5 Author | your angle, agree/push-back, personal texture, what to add | `references/authorial-layer.md` |
| 3 Write | essay from YOUR note in chosen voice; rewrite frameworks; derivative check; fix punctuation | `references/styles/<voice>.md` |
| 3.5 Personal | (optional) fill `【可替换…】` with real experience from user's bio doc, identity-obscured | SKILL.md Phase 3.5 |
| 4 Cover | optional 5:2 image | `references/cover-image.md` |
