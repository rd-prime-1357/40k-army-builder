#!/usr/bin/env python3
"""
faction_pack_transform.py — convert GW faction pack PDFs to markdown text.

Usage, from the directory holding the PDFs:

    py faction_pack_transform.py

With no arguments it converts every *.pdf in the current directory, writing one
.md file per PDF with the same base name. Existing .md files are overwritten
only when --force is given, so a re-run is safe by default.

    py faction_pack_transform.py --force
    py faction_pack_transform.py --dir some/other/folder
    py faction_pack_transform.py thousand_sons.pdf      # one named file

WHY THIS EXISTS
GW faction packs are two-column documents. Running `pdftotext -layout` on them
welds the left and right columns onto shared lines, producing fragments like
"attempt Rituals from those listed on the right. To do so, select one
SCINTILLATING LEGIONS unit." — two unrelated sentences spliced together. That is
worse than useless because it looks like valid prose, so a downstream parser
ingests it without complaint.

This script detects the layout per page and crops columns before extracting, so
reading order is preserved. Layout is decided per page, not per document,
because these packs mix two-column rules text with single-column datasheet
pages and full-width banner headings.

SCOPE
The converter transcribes; it does not interpret. It never drops content it
cannot classify, and never rewrites a faction keyword. Assigning content to a
faction is the parser's job. Anomalies that a parser would want to know about
are reported to stdout and recorded in a comment block at the top of the .md.

Output is deterministic: the same PDF yields byte-identical markdown on every
run, so this can sit inside the repro-check discipline like any other pipeline
stage.
"""

import argparse
import os
import re
import sys

try:
    import pdfplumber
except ImportError:
    sys.exit(
        "pdfplumber is required. Install it with:\n"
        "    Windows:        py -m pip install pdfplumber\n"
        "    macOS / Linux:  python3 -m pip install pdfplumber\n"
        "(If pip reports an externally-managed environment, add "
        "--break-system-packages.)\n"
        "Use `-m pip` rather than a bare `pip` so the install lands in the "
        "same Python that runs this script."
    )


# A word is treated as crossing the page's centre line if it straddles the
# gutter by more than this many points. Small overlaps happen with italic
# glyphs and kerning, so a bare > 0 test produces false single-column calls.
GUTTER_TOLERANCE = 4.0

# A candidate gutter must be at least this wide (points) to count as a real
# column break. Inter-word gaps inside a full-width table are narrower than
# this; a genuine two-column gutter in these packs is far wider.
MIN_GUTTER_WIDTH = 11

# Words within this many points of each other vertically are the same text row.
ROW_TOLERANCE = 3.0

# An x position counts as clear if no more than this share of rows has content
# there. Non-zero so that centred headings spanning a few rows cannot close a
# gutter that is otherwise clear down the whole page.
ROW_OCCUPANCY_LIMIT = 0.04

# A text row spanning at least this share of the page width, and crossing the
# centre, is full-width furniture rather than column content.
FULL_WIDTH_SHARE = 0.6

# A portrait page with at least this many words that was still classified
# single-column is probably a missed two-column page.
SUSPECT_WORD_COUNT = 150

# Words this close to the top or bottom edge are page furniture.
MARGIN_TRIM = 28.0

FACTION_KEYWORD_RE = re.compile(
    r"FACTION\s+KEYWORDS?\s*:?\s*(.+?)(?:\s{2,}|$)", re.IGNORECASE
)


def _words(page):
    """Body words on the page, with page furniture trimmed off."""
    out = []
    for w in page.extract_words(use_text_flow=False, keep_blank_chars=False):
        if w["top"] < MARGIN_TRIM:
            continue
        if w["bottom"] > page.height - MARGIN_TRIM:
            continue
        out.append(w)
    return out


def _rows(words):
    """Cluster words into text rows by vertical position."""
    rows = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        placed = False
        for r in rows:
            if abs(r[0]["top"] - w["top"]) <= ROW_TOLERANCE:
                r.append(w)
                placed = True
                break
        if not placed:
            rows.append([w])
    return rows


def _spans_centre(row, page):
    """True if this text row runs across the middle of the page."""
    x0 = min(w["x0"] for w in row)
    x1 = max(w["x1"] for w in row)
    mid = page.width / 2.0
    return (x1 - x0) >= page.width * FULL_WIDTH_SHARE and x0 < mid < x1


def _layout(page, words):
    """
    Work out the page's structure: a full-width band at the top, an optional
    two-column body, and a full-width band at the bottom.

    Returns (banner_bottom, gutter, footer_top). gutter is None when the body is
    single-column.

    Stripping the full-width bands before looking for the gutter is the whole
    point. Page 7 of the Death Guard pack opens with a full-width title and a
    full-width intro paragraph, then switches to two columns. Measuring
    occupancy across the whole page lets those few full-width rows close the
    gutter, the page gets treated as single-column, and the two columns are
    welded together mid-sentence: "Each time a PLAGUE LEGIONS unit from your
    this PSYKER) and roll one D6". Since that page carries the keyword changes
    this project depends on, silently mangling it is not acceptable.
    """
    rows = _rows(words)
    if not rows:
        return 0.0, None, page.height

    rows.sort(key=lambda r: min(w["top"] for w in r))
    flags = [_spans_centre(r, page) for r in rows]

    first = 0
    while first < len(rows) and flags[first]:
        first += 1
    last = len(rows)
    while last > first and flags[last - 1]:
        last -= 1

    banner_bottom = (
        max(w["bottom"] for r in rows[:first] for w in r) if first else 0.0
    )
    footer_top = (
        min(w["top"] for r in rows[last:] for w in r) if last < len(rows) else page.height
    )

    body = rows[first:last]
    if not body:
        return banner_bottom, None, footer_top

    width = int(page.width) + 2
    hits = [0] * width
    for r in body:
        touched = set()
        for w in r:
            lo = max(0, int(w["x0"]))
            hi = min(width - 1, int(w["x1"]) + 1)
            touched.update(range(lo, hi + 1))
        for x in touched:
            hits[x] += 1

    limit = int(len(body) * ROW_OCCUPANCY_LIMIT)
    lo_bound = int(page.width * 0.25)
    hi_bound = int(page.width * 0.75)

    best = None
    run_start = None
    for x in range(lo_bound, hi_bound + 2):
        clear = x <= hi_bound and hits[x] <= limit
        if clear:
            if run_start is None:
                run_start = x
        elif run_start is not None:
            span = x - run_start
            if best is None or span > best[0]:
                best = (span, run_start, x)
            run_start = None

    if best is None or best[0] < MIN_GUTTER_WIDTH:
        return banner_bottom, None, footer_top
    return banner_bottom, (best[1] + best[2]) / 2.0, footer_top


def _extract(page, crop=None):
    target = page.crop(crop) if crop else page
    text = target.extract_text(x_tolerance=1.5, y_tolerance=2.5) or ""
    return text


def _page_text(page):
    """Extract one page in correct reading order. Returns (text, layout)."""
    words = _words(page)
    if not words:
        return "", "empty"

    banner_bottom, gutter, footer_top = _layout(page, words)

    if gutter is None:
        # Portrait pages carrying this much text are two-column throughout
        # these packs. If detection says otherwise, say so loudly rather than
        # emitting interleaved text that reads like valid prose.
        suspect = page.height > page.width and len(words) >= SUSPECT_WORD_COUNT
        return _extract(page), ("single-SUSPECT" if suspect else "single")

    parts = []
    if banner_bottom > 0:
        head = _extract(page, (0, 0, page.width, banner_bottom + 2))
        if head.strip():
            parts.append(head)

    top = max(0.0, banner_bottom)
    bottom = min(page.height, footer_top)
    for box in ((0, top, gutter, bottom), (gutter, top, page.width, bottom)):
        chunk = _extract(page, box)
        if chunk.strip():
            parts.append(chunk)

    if footer_top < page.height:
        foot = _extract(page, (0, footer_top - 2, page.width, page.height))
        if foot.strip():
            parts.append(foot)

    return "\n\n".join(parts), "two-column"


def _tidy(text):
    """Normalise whitespace without altering wording."""
    text = text.replace("\u0007", "").replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", ln).rstrip() for ln in text.split("\n")]
    out, blanks = [], 0
    for ln in lines:
        if ln:
            out.append(ln)
            blanks = 0
        else:
            blanks += 1
            if blanks == 1 and out:
                out.append("")
    return "\n".join(out).strip()


def _find_anomalies(pages):
    """Flag things a parser should be told about rather than left to guess."""
    notes = []
    factions = {}
    for num, text, _ in pages:
        for m in FACTION_KEYWORD_RE.finditer(text):
            name = m.group(1).strip()
            if 0 < len(name) < 60:
                factions.setdefault(name, []).append(num)
                # B85 diagnostic (not yet fixed — see note below): print the raw
                # text immediately before the match so the next real run shows
                # exactly what precedes "FACTION KEYWORDS" on the source page,
                # rather than guessing at the bleed pattern without a PDF to
                # check it against.
                ctx_start = max(0, m.start() - 30)
                print(
                    f"      B85-CONTEXT p{num}: ...{text[ctx_start:m.start()]!r}"
                    f"[{m.group(0)}]"
                )
    if len(factions) > 1:
        listed = "; ".join(
            f"{name} (p{', p'.join(str(p) for p in pgs)})"
            for name, pgs in sorted(factions.items())
        )
        notes.append(
            "Multiple faction keywords appear in this pack: "
            + listed
            + ". GW packs sometimes carry a datasheet page copied from another "
              "faction's pack. Content was transcribed as-is; the parser should "
              "assign it to this pack's faction and ignore the stray keyword."
        )
    bad_glyphs = sum(t.count("\ufffd") for _, t, _ in pages)
    if bad_glyphs:
        notes.append(
            f"{bad_glyphs} character(s) could not be decoded from the PDF's embedded "
            "fonts and appear as U+FFFD. These are GW's decorative bullet and "
            "full-stop glyphs. They are left as-is rather than guessed at, so a "
            "parser should treat U+FFFD as punctuation, not content."
        )
    suspect = [str(n) for n, t, layout in pages if layout == "single-SUSPECT"]
    if suspect:
        notes.append(
            "KNOWN LIMITATION — page(s) " + ", ".join(suspect)
            + " could not be resolved into columns and were extracted full-width. "
              "Text on those pages is very likely INTERLEAVED between the two "
              "columns and must not be parsed without checking it by eye."
        )
    empty = [str(n) for n, t, layout in pages if layout == "empty"]
    if empty:
        notes.append(
            "No extractable text on page(s) " + ", ".join(empty)
            + ". These are probably image-only and may need OCR if they carry rules."
        )
    return notes


def convert(pdf_path, force=False):
    md_path = os.path.splitext(pdf_path)[0] + ".md"
    if os.path.exists(md_path) and not force:
        print(f"SKIP  {os.path.basename(md_path)} exists (use --force to overwrite)")
        return False

    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text, layout = _page_text(page)
            pages.append((i, _tidy(text), layout))

    notes = _find_anomalies(pages)

    body = [
        f"<!-- source: {os.path.basename(pdf_path)}",
        f"     converted by faction_pack_transform.py — transcription only, no interpretation",
        f"     pages: {len(pages)}",
    ]
    for n in notes:
        body.append(f"     NOTE: {n}")
    body.append("-->")
    body.append("")

    for num, text, layout in pages:
        body.append(f"## Page {num}")
        body.append(f"<!-- layout: {layout} -->")
        body.append("")
        body.append(text if text else "_(no extractable text)_")
        body.append("")

    with open(md_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(body).rstrip() + "\n")

    counts = {}
    for _, _, layout in pages:
        counts[layout] = counts.get(layout, 0) + 1
    shape = ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
    print(f"OK    {os.path.basename(md_path)}  ({len(pages)} pages: {shape})")
    for n in notes:
        print(f"      NOTE: {n}")
    return True


def main():
    ap = argparse.ArgumentParser(
        description="Convert GW faction pack PDFs to markdown, one .md per PDF."
    )
    ap.add_argument("pdfs", nargs="*", help="specific PDFs; default is every PDF in --dir")
    ap.add_argument("--dir", default=".", help="folder to scan (default: current)")
    ap.add_argument("--force", action="store_true", help="overwrite existing .md files")
    args = ap.parse_args()

    if args.pdfs:
        targets = args.pdfs
    else:
        targets = sorted(
            os.path.join(args.dir, f)
            for f in os.listdir(args.dir)
            if f.lower().endswith(".pdf")
        )

    if not targets:
        print(f"No PDFs found in {os.path.abspath(args.dir)}")
        return 0

    print(f"Converting {len(targets)} PDF(s)")
    done = 0
    for p in targets:
        if not os.path.exists(p):
            print(f"MISS  {p} not found")
            continue
        try:
            if convert(p, force=args.force):
                done += 1
        except Exception as exc:
            print(f"FAIL  {os.path.basename(p)}: {exc}")
    print(f"Converted {done} of {len(targets)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
