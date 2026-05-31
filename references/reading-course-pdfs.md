# Reading course PDFs

Course/lecture PDFs are the hard case: they're usually **image-based**, so text
extraction returns nothing useful. This file covers how to read them reliably.

## Step 1: Diagnose

```bash
pdfinfo "input.pdf"        # Producer field is a tell: jsPDF, Canva, Keynote,
                           # "Mac OS X Quartz", or a scanner → likely image-based
pdffonts "input.pdf"       # empty table, or all fonts "emb: no" → image-based
pdftotext -layout "input.pdf" /tmp/t.txt && wc -l /tmp/t.txt
head -40 /tmp/t.txt        # empty or garbled → must rasterize
```

If `pdftotext` gives clean, complete prose, you can read that directly and skip
rasterizing. This is rare for course decks but common for plain article PDFs.

## Step 2: Rasterize and view

```bash
# 150 DPI is the sweet spot. Bump to 200 only if small text is unreadable.
pdftoppm -jpeg -r 150 -f 1 -l 12 "input.pdf" /tmp/pg
ls /tmp/pg-*.jpg          # filenames are zero-padded by total page count
```

Then `view` each `/tmp/pg-*.jpg`. Read **all** pages — frameworks, case studies,
and the emphasized one-liners are exactly what make the essay good, and they're
scattered throughout.

## Token budget

- ~1,600 tokens per page at 150 DPI.
- A 60-page deck read fully ≈ ~100K tokens. Fine, but for very long decks read
  in **batches of 10–15 pages**, jot extraction notes after each batch, and let
  earlier pages drop out of working memory. You don't need every page in context
  simultaneously — you need your notes.

## What to look at on each page

Course decks signal importance visually. Pay attention to:

- **Colored / highlighted text** (red, yellow highlight, "敲黑板说重点") — these
  are the punchlines.
- **Diagrams and models** — the named frameworks. Read the labels carefully;
  they're the essay's skeleton.
- **Tables** (e.g. stage-by-stage progressions) — these are often the clearest
  statement of a process.
- **Screenshots / photos with captions** — usually anchor a case study.

## Edge cases

- **Truly scanned (handwritten or photographed):** `pdftotext` gives nothing and
  even rasterized text may be noisy. Rasterize at 200 DPI and read visually;
  OCR is usually unnecessary since you're reading the image yourself.
- **Garbled extraction (wrong characters):** the font has a broken encoding.
  Ignore the text layer entirely and rasterize.
- **Vector diagrams:** `pdfimages` won't extract them (they're drawn, not
  embedded). Rasterize the whole page instead.
- **Mixed PDF (some real text, some images):** rasterize regardless — it's
  simpler than reconciling two sources, and you won't miss image-only content.

## Filename gotcha

`pdftoppm` zero-pads based on total page count: a 60-page PDF yields `pg-01.jpg`,
a 200-page PDF yields `pg-001.jpg`. Don't guess — `ls /tmp/pg-*.jpg` to see the
actual names before viewing.
