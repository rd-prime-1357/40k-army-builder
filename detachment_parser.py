#!/usr/bin/env python3
"""
Detachment parser (E1a) -> detachments.json

Builds the detachment catalogue for every built army block, keyed by the app army
names used in units.json / faction_taxonomy.json.

NUMBERS PRECEDENCE
------------------
The MFM faction files are 11th Edition v1.0 and are authoritative for *structure and
numbers*: which detachments exist, their Detachment Point cost, their force
disposition, their Unique tag, and the enhancement list with points and (Upgrade)
tags. The Wahapedia CSV dump is 10th Edition and contributes prose only. An
enhancement that appears in a text source but not in MFM is dropped, not carried --
it is a stale leftover and showing it would put a phantom option at a wrong price in
front of the player.

TEXT PRECEDENCE (three-tier ladder, highest first)
--------------------------------------------------
  1. faction_pack   -- current-edition faction packs and digests:
                       Space_Marines_Faction_Pack_v1_0.md   (15 SM detachment spreads)
                       Dark_Angels_Faction_Pack_June_2026.md (5 DA detachments)
                       chaos_daemons_reference.md            (9 CD detachments, digest)
  2. wahapedia_10e  -- Detachment_abilities.csv / Enhancements.csv / Stratagems.csv,
                       used only where no tier-1 text exists.
  3. none           -- name, DP, disposition, unique tag and enhancement names/points only.

`text_source` records the tier that supplied the *detachment rule*. Enhancement
descriptions carry their own `description_source` because a tier-1 digest can be
thinner than the tier-2 text for the same enhancement.

Stdlib only.  python3 detachment_parser.py --help
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict

# ---------------------------------------------------------------------------
# Army mapping
# ---------------------------------------------------------------------------

# app army name (units.json "army") -> MFM detachment file supplying its list.
# The six Codex: Space Marines chapters with no MFM file of their own take the
# generic Space Marines list of 22 in full (E1 scope doc section 3, D192).
ARMY_TO_MFM = OrderedDict([
    ("Adeptus Astartes", "MFM_Space_Marines_v1_0.txt"),
    ("Black Templars",   "MFM_Black_Templars_v1_0.txt"),
    ("Blood Angels",     "MFM_Blood_Angels_v1_0.txt"),
    ("Dark Angels",      "MFM_Dark_Angels_v1_0.txt"),
    ("Deathwatch",       "MFM_Death_Watch_v1_0.txt"),
    ("Imperial Fists",   "MFM_Space_Marines_v1_0.txt"),
    ("Iron Hands",       "MFM_Space_Marines_v1_0.txt"),
    ("Raven Guard",      "MFM_Space_Marines_v1_0.txt"),
    ("Salamanders",      "MFM_Space_Marines_v1_0.txt"),
    ("Space Wolves",     "MFM_Space_Wolves_v1_0.txt"),
    ("Ultramarines",     "MFM_Space_Marines_v1_0.txt"),
    ("White Scars",      "MFM_Space_Marines_v1_0.txt"),
    ("Chaos Daemons",    "MFM_Chaos_Daemons_v1_0.txt"),
    ("Death Guard",      "MFM_Death_Guard_v1_0.txt"),
])

# Human-readable name of the MFM source list, for the source_faction field.
MFM_SOURCE_NAME = {
    "MFM_Space_Marines_v1_0.txt":  "Space Marines",
    "MFM_Black_Templars_v1_0.txt": "Black Templars",
    "MFM_Blood_Angels_v1_0.txt":   "Blood Angels",
    "MFM_Dark_Angels_v1_0.txt":    "Dark Angels",
    "MFM_Death_Watch_v1_0.txt":    "Deathwatch",
    "MFM_Space_Wolves_v1_0.txt":   "Space Wolves",
    "MFM_Chaos_Daemons_v1_0.txt":  "Chaos Daemons",
    "MFM_Death_Guard_v1_0.txt":    "Death Guard",
}

# Wahapedia faction_id supplying tier-2 prose for each app army. The 10th Edition
# dump folds every Space Marine Chapter into SM.
ARMY_TO_WAHA_FACTION = {
    "Adeptus Astartes": "SM", "Black Templars": "SM", "Blood Angels": "SM",
    "Dark Angels": "SM", "Deathwatch": "SM", "Imperial Fists": "SM",
    "Iron Hands": "SM", "Raven Guard": "SM", "Salamanders": "SM",
    "Space Wolves": "SM", "Ultramarines": "SM", "White Scars": "SM",
    "Chaos Daemons": "CD", "Death Guard": "DG",
}

FORCE_DISPOSITIONS = (
    "PRIORITY ASSETS", "TAKE AND HOLD", "PURGE THE FOE", "DISRUPTION", "RECONNAISSANCE",
)

# Lines inside an MFM DETACHMENTS block that are known extraction noise rather than
# detachment data. Anything not matched by a known line shape and not listed here is
# a hard error, so a future MFM revision that adds a real field cannot slip past.
MFM_BLOCK_NOISE = re.compile(r"^LEADER:")

# ---------------------------------------------------------------------------
# Small text helpers
# ---------------------------------------------------------------------------

def clean_chars(s):
    """Normalise the punctuation and stray control characters PDF extraction leaves."""
    if s is None:
        return None
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2011", "-").replace("\u2010", "-")
    s = s.replace("\u00a0", " ")
    # Record/group separators and other C0 controls are ligature debris.
    s = "".join(" " if (ord(c) < 32 and c not in "\n\t") else c for c in s)
    s = s.replace("\u200b", "").replace("\ufeff", "")
    return s


def norm_key(s):
    """Join key: case-folded, punctuation-stripped, parentheticals removed."""
    if s is None:
        return ""
    s = clean_chars(s)
    s = re.sub(r"\([^)]*\)", " ", s)          # drop (Aura), (Upgrade), ...
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9]+", " ", s)
    return " ".join(s.split()).upper()


_SMALL = {"of", "the", "and", "to", "in", "a", "an", "for", "unto", "with", "on"}


def title_case(s):
    """Title-case an all-caps MFM name for display without mangling apostrophes."""
    s = clean_chars(s).strip()
    words = s.split(" ")
    out = []
    for i, w in enumerate(words):
        if not w:
            continue
        parts = re.split(r"(-)", w)
        rebuilt = []
        for p in parts:
            if p == "-" or not p:
                rebuilt.append(p)
                continue
            low = p.lower()
            if i > 0 and low in _SMALL and rebuilt == []:
                rebuilt.append(low)
            else:
                # Keep the tail of an apostrophe contraction lower ("Emperor's").
                m = re.match(r"^([A-Za-z]+)'([A-Za-z]+)$", p)
                if m:
                    rebuilt.append(m.group(1).capitalize() + "'" + m.group(2).lower())
                else:
                    rebuilt.append(p[:1].upper() + p[1:].lower())
        out.append("".join(rebuilt))
    if out:
        out[0] = out[0][:1].upper() + out[0][1:]
    return " ".join(out)


HTML_BR = re.compile(r"<\s*br\s*/?\s*>", re.I)
HTML_LI = re.compile(r"<\s*li\s*>", re.I)
HTML_TAG = re.compile(r"<[^>]+>")


def strip_html(s):
    if not s:
        return None
    s = HTML_BR.sub("\n", s)
    s = HTML_LI.sub("\n\u25aa ", s)
    # Wahapedia embeds real tables (battle-size bands, doctrine lists). Stripping the
    # tags without separators fuses the cells into unreadable runs like
    # "BATTLE SIZEUNITSIncursionUp to 1 units", so give rows and cells a boundary.
    s = re.sub(r"<\s*/\s*(tr|thead|tbody|table)\s*>", "\n", s, flags=re.I)
    s = re.sub(r"<\s*/\s*(td|th)\s*>", " \u2014 ", s, flags=re.I)
    s = HTML_TAG.sub("", s)
    s = re.sub(r"(?:\s*\u2014\s*)+\n", "\n", s)
    s = re.sub(r"(?:\s*\u2014\s*)+$", "", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
    s = clean_chars(s)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    lines = [ln for ln in lines if ln]
    out = "\n".join(lines).strip()
    return out or None


def reflow(lines):
    """Join a run of wrapped body lines into paragraphs.

    A blank line and a leading bullet both start a new paragraph; everything else
    is a soft wrap and gets joined with a space.
    """
    paras = []
    cur = []
    for raw in lines:
        ln = clean_chars(raw).strip()
        if not ln:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if ln[0] in "\u25aa\u25a0\u2022":
            if cur:
                paras.append(" ".join(cur))
            cur = [ln]
            continue
        cur.append(ln)
    if cur:
        paras.append(" ".join(cur))
    paras = [re.sub(r"\s+", " ", p).strip() for p in paras]
    return "\n".join(p for p in paras if p) or None


# ---------------------------------------------------------------------------
# 1. MFM -- structure and numbers (authoritative)
# ---------------------------------------------------------------------------

MFM_DP_RE = re.compile(r"^(.*?[A-Za-z\u2019'])\s*(\d)DP$")
MFM_ENH_RE = re.compile(r"^[\u2022\-\*]\s*(.+?)\s*(\d+)\s*pts$", re.I)
MFM_UNIQUE_RE = re.compile(r"^UNIQUE:\s*(.+)$")


def parse_mfm_detachments(path):
    """Return the ordered detachment list printed in one MFM faction file.

    Block shape, per the MFM_Instructions.txt legend:

        <NAME><n>DP
        <FORCE DISPOSITION>
        [UNIQUE: <tag>]                 -- only one detachment per tag may be taken
        ENHANCEMENTS
        - <Enhancement Name>[ (Upgrade)]<n> pts   (repeated)
    """
    with open(path, encoding="utf-8-sig") as f:
        lines = [clean_chars(ln).rstrip("\n").rstrip("\r").strip() for ln in f]

    try:
        start = lines.index("DETACHMENTS")
    except ValueError:
        raise SystemExit("no DETACHMENTS section in %s" % path)

    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j] == "LEGENDS":
            end = j
            break

    out = []
    cur = None
    for lineno, ln in enumerate(lines[start + 1:end], start + 2):
        if not ln:
            continue
        m = MFM_DP_RE.match(ln)
        if m:
            cur = {
                "name_raw": m.group(1).strip(),
                "dp": int(m.group(2)),
                "force_disposition": None,
                "unique_tag": None,
                "enhancements": [],
            }
            out.append(cur)
            continue
        if cur is None:
            raise SystemExit("%s:%d stray line before first detachment: %r" % (path, lineno, ln))
        if ln in FORCE_DISPOSITIONS:
            if cur["force_disposition"] is not None:
                raise SystemExit("%s:%d second disposition for %s" % (path, lineno, cur["name_raw"]))
            cur["force_disposition"] = ln
            continue
        mu = MFM_UNIQUE_RE.match(ln)
        if mu:
            cur["unique_tag"] = mu.group(1).strip()
            continue
        if ln == "ENHANCEMENTS":
            continue
        me = MFM_ENH_RE.match(ln)
        if me:
            raw = me.group(1).strip()
            is_upgrade = bool(re.search(r"\(Upgrade\)", raw, re.I))
            display = re.sub(r"\s*\(Upgrade\)\s*", " ", raw, flags=re.I).strip()
            cur["enhancements"].append({
                "name": display,
                "name_raw": raw,
                "points": int(me.group(2)),
                "is_upgrade": is_upgrade,
            })
            continue
        if MFM_BLOCK_NOISE.match(ln):
            continue
        raise SystemExit("%s:%d unrecognised line in DETACHMENTS block: %r" % (path, lineno, ln))

    for d in out:
        if d["force_disposition"] is None:
            raise SystemExit("%s: %s has no force disposition" % (path, d["name_raw"]))
    return out


# ---------------------------------------------------------------------------
# 2. Wahapedia -- tier-2 prose
# ---------------------------------------------------------------------------

def read_pipe_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f, delimiter="|"))
    if not rows:
        return []
    header = [h.strip() for h in rows[0]]
    out = []
    for r in rows[1:]:
        if not any(x.strip() for x in r):
            continue
        out.append({header[i]: (r[i] if i < len(r) else "") for i in range(len(header))})
    return out


def load_wahapedia(root):
    dets = read_pipe_csv(os.path.join(root, "Detachments.csv"))
    abils = read_pipe_csv(os.path.join(root, "Detachment_abilities.csv"))
    enhs = read_pipe_csv(os.path.join(root, "Enhancements.csv"))
    strats = read_pipe_csv(os.path.join(root, "Stratagems.csv"))

    by_id = {}
    for d in dets:
        by_id[d["id"]] = {"faction": d["faction_id"], "name": d["name"],
                          "rules": [], "enh": [], "strat": []}
    for a in abils:
        did = a.get("detachment_id", "")
        if did in by_id:
            by_id[did]["rules"].append((a.get("name", ""), a.get("description", "")))
    for e in enhs:
        did = e.get("detachment_id", "")
        if did in by_id:
            by_id[did]["enh"].append(e)
    for s in strats:
        did = s.get("detachment_id", "")
        if did in by_id:
            by_id[did]["strat"].append(s)

    # faction -> normalised detachment name -> merged record. Wahapedia carries a
    # duplicate row for at least one detachment (CD Daemonic Incursion); merge on
    # the normalised name and keep the row that actually has text.
    idx = {}
    for rec in by_id.values():
        fac = rec["faction"]
        key = norm_key(rec["name"])
        slot = idx.setdefault(fac, {}).get(key)
        score = (len(rec["rules"]), len(rec["enh"]), len(rec["strat"]))
        if slot is None or score > slot["_score"]:
            rec = dict(rec)
            rec["_score"] = score
            idx[fac][key] = rec
    return idx


def waha_text(rec):
    if not rec:
        return None, None, {}, []
    rule_name = None
    rule_bits = []
    for nm, desc in rec["rules"]:
        body = strip_html(desc)
        if not body:
            continue
        if rule_name is None:
            rule_name = clean_chars(nm).strip() or None
        rule_bits.append(("%s\n%s" % (clean_chars(nm).strip(), body)).strip()
                         if len(rec["rules"]) > 1 else body)
    rule_text = "\n\n".join(rule_bits) if rule_bits else None

    enh = {}
    for e in rec["enh"]:
        enh[norm_key(e.get("name", ""))] = strip_html(e.get("description", ""))

    strat = []
    for s in rec["strat"]:
        cp = s.get("cp_cost", "").strip()
        strat.append({
            "name": title_case(clean_chars(s.get("name", "")).strip()),
            "cp": int(cp) if cp.isdigit() else None,
            "type": clean_chars(s.get("type", "")).strip() or None,
            "description": strip_html(s.get("description", "")),
        })
    strat.sort(key=lambda x: x["name"])
    return rule_name, rule_text, enh, strat


# ---------------------------------------------------------------------------
# 3. Faction packs -- tier-1 prose
# ---------------------------------------------------------------------------
# Every pack parser returns:
#   { norm_key(detachment name): {
#        "rule_name": str|None, "rule_text": str|None, "restrictions": str|None,
#        "enh": {norm_key(name): description}, "strat": [ {name, cp, description} ] } }

CP_TOKEN = re.compile(r"^\s*(\d)\s*CP\s*$", re.I)
STRAT_TAG = re.compile(r"^(.*?)\s*[-\u2013]\s*(.*?STRATAGEM)\s*$", re.I)
STRAT_TAG_PLAIN = re.compile(r"^(.*?)\s+STRATAGEM$", re.I)


def _is_upper_head(s):
    t = s.strip()
    if not t or len(t) < 3:
        return False
    letters = [c for c in t if c.isalpha()]
    if len(letters) < 3:
        return False
    return sum(c.isupper() for c in letters) / len(letters) > 0.9


# ---- 3a. Dark Angels pack (single column, linear) --------------------------

DA_SECTION = {"DETACHMENT RULE", "DETACHMENT RULES", "ENHANCEMENTS", "RESTRICTIONS"}


def parse_da_pack(path, wanted_keys):
    if not os.path.exists(path):
        return {}
    raw = clean_chars(open(path, encoding="utf-8").read())
    pages = re.split(r"(?m)^#\s*Page\s+\d+\s*$", raw)
    out = OrderedDict()
    cur = None
    for page in pages[1:]:
        lines = [ln.rstrip() for ln in page.split("\n")]
        lines = [ln for ln in lines if ln.strip() != ""]
        if not lines:
            continue
        # A page opens a new detachment when its leading all-caps run (one or two
        # lines) resolves to one of the MFM names we are looking for.
        head = []
        i = 0
        while i < len(lines) and _is_upper_head(lines[i]) and len(head) < 2:
            head.append(lines[i].strip())
            cand = norm_key(" ".join(head))
            if cand in wanted_keys:
                break
            i += 1
        cand = norm_key(" ".join(head)) if head else ""
        if cand in wanted_keys:
            cur = out.setdefault(cand, {"rule_name": None, "rule_text": None,
                                        "restrictions": None, "enh": OrderedDict(),
                                        "strat": []})
            body = lines[len(head):]
        else:
            if cur is None:
                continue
            body = lines
        _da_consume(body, cur)
    return out


def _da_consume(lines, det):
    """Walk one page of Dark-Angels-shaped body text into the detachment record."""
    mode = None          # None | rule | enh | restrict | strat
    buf = []
    pending_name = None
    strat_cur = None

    def flush():
        nonlocal buf, pending_name, strat_cur, mode
        text = reflow(buf)
        buf = []
        if mode == "rule":
            if text:
                det["rule_text"] = (det["rule_text"] + "\n\n" + text) if det["rule_text"] else text
        elif mode == "restrict":
            if text:
                det["restrictions"] = (det["restrictions"] + "\n" + text) if det["restrictions"] else text
        elif mode == "enh" and pending_name:
            key = norm_key(pending_name)
            prev = det["enh"].get(key)
            det["enh"][key] = ((prev + "\n" + text) if (prev and text) else (text or prev))
        elif mode == "strat" and strat_cur is not None:
            if text:
                strat_cur["description"] = ((strat_cur["description"] + "\n" + text)
                                            if strat_cur["description"] else text)
        pending_name = pending_name

    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i].strip()
        bare = re.sub(r"[\s\u2022\u25aa\u25a0.]+$", "", ln).strip()
        up = bare.upper()

        if up in ("DETACHMENT RULE", "DETACHMENT RULES"):
            flush(); mode = "rule"; pending_name = None
            # the next non-blank all-caps line is the rule's name
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and _is_upper_head(lines[j]):
                det["rule_name"] = det["rule_name"] or title_case(lines[j].strip())
                i = j + 1
                continue
            i += 1
            continue
        if up == "ENHANCEMENTS":
            flush(); mode = "enh"; pending_name = None; i += 1; continue
        if up in ("RESTRICTIONS", "RESTRICTIONS:"):
            flush(); mode = "restrict"; pending_name = None; i += 1; continue
        if up.startswith("RESTRICTIONS:") and mode != "strat":
            flush(); mode = "restrict"; buf = [bare.split(":", 1)[1]]; i += 1; continue

        # A stratagem opens as NAME / nCP / "<DETACHMENT> STRATAGEM" in either order.
        if _is_upper_head(bare) and i + 2 < n:
            nxt1 = lines[i + 1].strip()
            nxt2 = lines[i + 2].strip()
            cp = None
            tag = None
            if CP_TOKEN.match(nxt1) and re.search(r"STRATAGEM\s*$", nxt2, re.I):
                cp, tag = int(CP_TOKEN.match(nxt1).group(1)), nxt2
                skip = 3
            elif re.search(r"STRATAGEM\s*$", nxt1, re.I) and CP_TOKEN.match(nxt2):
                cp, tag = int(CP_TOKEN.match(nxt2).group(1)), nxt1
                skip = 3
            else:
                skip = 0
            if skip:
                flush(); mode = "strat"
                strat_cur = {"name": title_case(bare), "cp": cp,
                             "type": title_case(tag), "description": None}
                det["strat"].append(strat_cur)
                i += skip
                continue

        if mode == "enh" and _is_upper_head(bare):
            flush()
            nm = bare
            is_up = bool(re.search(r"\bUPGRADE\b\s*$", nm))
            nm = re.sub(r"\s*\bUPGRADE\b\s*$", "", nm).strip()
            pending_name = nm
            det["enh"].setdefault(norm_key(nm), None)
            i += 1
            continue

        if mode is None:
            i += 1
            continue

        buf.append(ln)
        i += 1

    flush()


# ---- 3b. Chaos Daemons condensed digest ------------------------------------

CD_HEAD = re.compile(r"^###\s*\d+\.\s*(.+?)\s*$")


def parse_cd_reference(path, wanted_keys):
    if not os.path.exists(path):
        return {}
    raw = clean_chars(open(path, encoding="utf-8").read())
    m = re.search(r"(?m)^##\s*DETACHMENTS SUMMARY\s*$", raw)
    if not m:
        return {}
    tail = raw[m.end():]
    stop = re.search(r"(?m)^##\s+", tail)
    if stop:
        tail = tail[:stop.start()]

    out = OrderedDict()
    cur = None
    for ln in tail.split("\n"):
        h = CD_HEAD.match(ln)
        if h:
            key = norm_key(h.group(1))
            cur = out.setdefault(key, {"rule_name": None, "rule_text": None,
                                       "restrictions": None, "enh": OrderedDict(),
                                       "strat": []}) if key in wanted_keys else None
            continue
        if cur is None:
            continue
        s = ln.strip()
        if s.startswith("Rule:"):
            body = s[len("Rule:"):].strip()
            nm = re.match(r"^(.+?)\s+[-\u2013]\s+", body)
            if nm:
                cur["rule_name"] = title_case(nm.group(1))
            cur["rule_text"] = body
        elif s.startswith("Keywords:"):
            cur["rule_text"] = ((cur["rule_text"] or "") + "\n" + s).strip()
        elif s.startswith("Enhancements:"):
            for part in _split_top_level(s[len("Enhancements:"):].strip().rstrip(".")):
                part = part.strip()
                if not part:
                    continue
                nm = re.sub(r"\s*\(.*$", "", part).strip()
                cur["enh"][norm_key(nm)] = part
        elif s.startswith("Stratagems:"):
            for part in s[len("Stratagems:"):].strip().rstrip(".").split(","):
                part = part.strip()
                sm = re.match(r"^(.*?)\s+(\d)\s*CP$", part, re.I)
                if sm:
                    cur["strat"].append({"name": title_case(sm.group(1)),
                                         "cp": int(sm.group(2)),
                                         "type": None, "description": None})
    return out


def strat_list_is_complete(strat):
    """Is a tier-1 stratagem list good enough to displace the tier-2 text?

    Stated as an invariant rather than a per-source switch, so that a source which
    improves -- a re-extraction of a pack, say -- starts winning automatically, and
    one that is only a summary keeps losing without anyone having to remember it.
    Every entry must name itself, price itself, and carry a body.
    """
    if not strat:
        return False
    for s in strat:
        if not s.get("name") or s.get("cp") is None or not s.get("description"):
            return False
    return True


def _split_top_level(s):
    """Split on ';' first, falling back to ',' outside parentheses."""
    if ";" in s:
        return s.split(";")
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


# ---- 3c. Space Marines pack (two-column extraction) ------------------------

def _fenced_pages(path):
    """Yield (page_number, [lines]) for each fenced page block in a pack."""
    raw = clean_chars(open(path, encoding="utf-8").read())
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^##\s*p(\d+)\s*[-\u2014]", lines[i])
        if not m:
            i += 1
            continue
        pno = int(m.group(1))
        j = i + 1
        while j < len(lines) and not lines[j].startswith("```"):
            j += 1
        k = j + 1
        while k < len(lines) and not lines[k].startswith("```"):
            k += 1
        yield pno, lines[j + 1:k]
        i = k + 1


def _find_gutter(lines):
    """Locate the column where the right-hand text column starts.

    Body lines respect the columns; only full-width headings and the floating CP
    badges cross them. The gutter is the modal start position of the second text
    run across all lines that have one.
    """
    votes = {}
    for ln in lines:
        for m in re.finditer(r"\s{4,}", ln):
            start = m.end()
            if start < 30 or start >= len(ln):
                continue
            if m.start() < 20:
                continue
            votes[start] = votes.get(start, 0) + 1
    if not votes:
        return None
    best = max(votes.items(), key=lambda kv: (kv[1], kv[0]))
    if best[1] < 4:
        return None
    return best[0]


TRAILING_CP = re.compile(r"\s{3,}(\d)\s*CP\s*$", re.I)
LEADING_CP = re.compile(r"^\s*(\d)\s*CP\s{3,}")


GUTTER_TOLERANCE = 6


def _split_columns(lines):
    """Return the page's two text columns as separate streams.

    The extraction preserves column geometry for body text; only full-width
    headings and the floating CP badges cross the gutter, and the gutter itself
    drifts by a character or two between lines. So the split point is taken per
    line: the whitespace run nearest the page's modal gutter, within tolerance.
    A line with no such run has a word straddling the gutter and is full-width.

    The columns are returned separately rather than concatenated because a
    fragment of full-width intro text can land at the head of the right column,
    ahead of that column's first section heading. Read as one stream it would be
    absorbed into whatever section the left column ended in; read as two, it sits
    ahead of any heading and is discarded.
    """
    gutter = _find_gutter(lines)
    if gutter is None:
        return [[ln.strip() for ln in lines]]
    left, right = [], []
    for ln in lines:
        ln = ln.rstrip()
        if not ln.strip():
            left.append(""); right.append(""); continue
        # A folio number sits in column 0, ahead of the left column's own indent.
        # Blank it in place so the gutter geometry is untouched.
        mf = re.match(r"^(\d{1,3})(\s{2,})", ln)
        if mf:
            ln = " " * mf.end(1) + ln[mf.end(1):]
        runs = [(m.start(), m.end()) for m in re.finditer(r"\s{2,}", ln)]
        cut = None
        for s, e in runs:
            if s <= gutter <= e:
                cut = (s, e)
                break
        if cut is None:
            near = [(abs(e - gutter), s, e) for s, e in runs
                    if abs(e - gutter) <= GUTTER_TOLERANCE]
            if near:
                near.sort()
                cut = (near[0][1], near[0][2])
        if cut is None:
            # a word straddles the gutter: full-width line
            left.append(ln.strip()); right.append("")
            continue
        left.append(ln[:cut[0]].strip())
        right.append(ln[cut[1]:].strip())
    # A bare folio number sits alone in a column and is not content.
    left = ["" if re.match(r"^\d{1,3}$", x) else x for x in left]
    right = ["" if re.match(r"^\d{1,3}$", x) else x for x in right]
    while left and not left[-1]:
        left.pop()
    while right and not right[-1]:
        right.pop()
    return [left, right]


SM_SECTION_RE = re.compile(r"^(DETACHMENT RULES?|ENHANCEMENTS|RESTRICTIONS)$")


def parse_sm_pack(path, wanted_keys, first_page=2, last_page=28):
    if not os.path.exists(path):
        return {}
    out = OrderedDict()
    cur = None
    for pno, lines in _fenced_pages(path):
        if pno < first_page or pno > last_page:
            continue
        columns = _split_columns(lines)
        first = True
        for body in columns:
            if first:
                # Does this page open a detachment? Its leading all-caps run names one.
                head = []
                idx = 0
                while idx < len(body) and len(head) < 2:
                    s = body[idx].strip()
                    if not s:
                        idx += 1
                        continue
                    if not _is_upper_head(s):
                        break
                    head.append(s)
                    if norm_key(" ".join(head)) in wanted_keys:
                        idx += 1
                        break
                    idx += 1
                key = norm_key(" ".join(head)) if head else ""
                if key in wanted_keys:
                    cur = out.setdefault(key, {"rule_name": None, "rule_text": None,
                                               "restrictions": None, "enh": OrderedDict(),
                                               "strat": []})
                    body = body[idx:]
                first = False
            if cur is None:
                continue
            _sm_consume(body, cur)
    return out


def _sm_consume(lines, det):
    mode = None
    buf = []
    pending = None
    strat_cur = None

    def flush():
        nonlocal buf
        text = reflow(buf)
        buf = []
        if mode == "rule" and text:
            det["rule_text"] = (det["rule_text"] + "\n\n" + text) if det["rule_text"] else text
        elif mode == "restrict" and text:
            det["restrictions"] = (det["restrictions"] + "\n" + text) if det["restrictions"] else text
        elif mode == "enh" and pending:
            k = norm_key(pending)
            prev = det["enh"].get(k)
            det["enh"][k] = ((prev + "\n" + text) if (prev and text) else (text or prev))
        elif mode == "strat" and strat_cur is not None and text:
            strat_cur["description"] = ((strat_cur["description"] + "\n" + text)
                                        if strat_cur["description"] else text)

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        ln = raw.strip()
        if not ln:
            buf.append("")
            i += 1
            continue

        # Pull a floating CP badge off the line before anything else.
        cp_here = None
        m = TRAILING_CP.search(ln)
        if m:
            cp_here = int(m.group(1)); ln = ln[:m.start()].rstrip()
        m = LEADING_CP.match(ln)
        if m:
            cp_here = int(m.group(1)); ln = ln[m.end():].strip()
        if CP_TOKEN.match(ln):
            cp_here = int(CP_TOKEN.match(ln).group(1)); ln = ""
        if cp_here is not None and strat_cur is not None and strat_cur["cp"] is None:
            strat_cur["cp"] = cp_here
        if not ln:
            i += 1
            continue

        sm = SM_SECTION_RE.match(ln.upper())
        if sm:
            flush()
            head = sm.group(1)
            if head.startswith("DETACHMENT RULE"):
                mode = "rule"; pending = None
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and _is_upper_head(lines[j]):
                    det["rule_name"] = det["rule_name"] or title_case(lines[j].strip())
                    i = j + 1
                    continue
            elif head == "ENHANCEMENTS":
                mode = "enh"; pending = None
            else:
                mode = "restrict"; pending = None
            i += 1
            continue

        # "<DETACHMENT> - <TYPE> STRATAGEM" marks the line above as a stratagem name.
        if re.search(r"STRATAGEM\s*$", ln, re.I) and _is_upper_head(ln):
            name = None
            for back in range(len(buf) - 1, -1, -1):
                cand = buf[back].strip()
                if cand:
                    if _is_upper_head(cand):
                        name = cand
                        buf = buf[:back]
                    break
            flush()
            mode = "strat"
            strat_cur = {"name": title_case(name) if name else None, "cp": cp_here,
                         "type": title_case(ln), "description": None}
            det["strat"].append(strat_cur)
            i += 1
            continue

        if mode == "enh" and _is_upper_head(ln):
            flush()
            pending = re.sub(r"\s*\bUPGRADE\b\s*$", "", ln).strip()
            det["enh"].setdefault(norm_key(pending), None)
            i += 1
            continue

        if mode is None:
            i += 1
            continue

        buf.append(ln)
        i += 1

    flush()


# ---------------------------------------------------------------------------
# 4. Build
# ---------------------------------------------------------------------------

def _tally(rows, keyfn):
    out = {}
    for r in rows:
        k = keyfn(r)
        out[k] = out.get(k, 0) + 1
    return out


def build(root, out_path, report_path=None):
    mfm_cache = {}
    for fn in set(ARMY_TO_MFM.values()):
        mfm_cache[fn] = parse_mfm_detachments(os.path.join(root, fn))

    wanted = set()
    for fn, dets in mfm_cache.items():
        for d in dets:
            wanted.add(norm_key(d["name_raw"]))

    waha = load_wahapedia(root)
    packs = {}
    packs.update({k: ("Space Marines Faction Pack v1.0", v)
                  for k, v in parse_sm_pack(os.path.join(root, "Space_Marines_Faction_Pack_v1_0.md"), wanted).items()})
    # Later packs win on key collision only when they are faction-specific; the DA
    # and CD sources cover names the SM pack does not, so simple update is safe.
    da = parse_da_pack(os.path.join(root, "Dark_Angels_Faction_Pack_June_2026.md"), wanted)
    cd = parse_cd_reference(os.path.join(root, "chaos_daemons_reference.md"), wanted)

    pack_by_army = {}
    for army in ARMY_TO_MFM:
        m = dict(packs)
        if army == "Dark Angels":
            m.update({k: ("Dark Angels Faction Pack June 2026", v) for k, v in da.items()})
        if army == "Chaos Daemons":
            m = {k: ("Chaos Daemons Faction Reference (condensed)", v) for k, v in cd.items()}
        pack_by_army[army] = m

    armies = OrderedDict()
    gaps = []
    tier_counts = {"faction_pack": 0, "wahapedia_10e": 0, "none": 0}
    desc_counts = {"faction_pack": 0, "wahapedia_10e": 0, "none": 0}
    n_det = n_enh = n_upg = 0
    disp_counts = {d: 0 for d in FORCE_DISPOSITIONS}
    dropped_waha_enh = 0

    for army, mfm_file in ARMY_TO_MFM.items():
        fac = ARMY_TO_WAHA_FACTION[army]
        recs = []
        for d in mfm_cache[mfm_file]:
            key = norm_key(d["name_raw"])
            pack_name, pack = pack_by_army[army].get(key, (None, None))
            w = waha.get(fac, {}).get(key)
            w_rule_name, w_rule_text, w_enh, w_strat = waha_text(w)

            if pack and (pack.get("rule_text") or pack.get("enh")):
                text_source = "faction_pack"
                rule_name = pack.get("rule_name") or w_rule_name
                rule_text = pack.get("rule_text") or None
                restrictions = pack.get("restrictions")
                strat = pack.get("strat") or []
                if strat and strat_list_is_complete(strat):
                    strat_source = "faction_pack"
                elif w_strat:
                    strat = w_strat
                    strat_source = "wahapedia_10e"
                elif strat:
                    strat_source = "faction_pack"
                else:
                    strat_source = "none"
                src_label = pack_name
            elif w_rule_text:
                text_source = "wahapedia_10e"
                rule_name = w_rule_name
                rule_text = w_rule_text
                restrictions = None
                strat = w_strat
                strat_source = "wahapedia_10e" if strat else "none"
                src_label = "Wahapedia 10th Edition"
            else:
                text_source = "none"
                rule_name = None
                rule_text = None
                restrictions = None
                strat = []
                strat_source = "none"
                src_label = None
                gaps.append({"key": "%s|%s" % (MFM_SOURCE_NAME[mfm_file], d["name_raw"]),
                             "source_faction": MFM_SOURCE_NAME[mfm_file],
                             "detachment": title_case(d["name_raw"]),
                             "dp": d["dp"]})

            tier_counts[text_source] += 1
            disp_counts[d["force_disposition"]] += 1

            enh_out = []
            pack_enh = (pack or {}).get("enh") or {}
            for e in d["enhancements"]:
                ek = norm_key(e["name"])
                desc = pack_enh.get(ek)
                dsrc = "faction_pack" if desc else None
                if not desc:
                    desc = w_enh.get(ek)
                    dsrc = "wahapedia_10e" if desc else "none"
                desc_counts[dsrc] += 1
                enh_out.append({
                    "name": e["name"],
                    "name_raw": e["name_raw"],
                    "points": e["points"],
                    "is_upgrade": e["is_upgrade"],
                    "description": desc,
                    "description_source": dsrc,
                })

            mfm_keys = {norm_key(e["name"]) for e in d["enhancements"]}
            dropped_waha_enh += len([k for k in w_enh if k not in mfm_keys])

            recs.append(OrderedDict([
                ("name", title_case(d["name_raw"])),
                ("name_raw", d["name_raw"]),
                ("dp", d["dp"]),
                ("force_disposition", d["force_disposition"]),
                ("unique_tag", d["unique_tag"]),
                ("key", "%s|%s" % (MFM_SOURCE_NAME[mfm_file], d["name_raw"])),
                ("source_faction", MFM_SOURCE_NAME[mfm_file]),
                ("text_source", text_source),
                ("text_source_detail", src_label),
                ("rule_name", rule_name),
                ("rule_text", rule_text),
                ("restrictions", restrictions),
                ("enhancements", enh_out),
                ("stratagems", strat),
                ("stratagem_source", strat_source),
            ]))
            n_det += 1
        recs.sort(key=lambda r: r["name"])
        armies[army] = recs

    # The six Codex: Space Marines chapters with no MFM file of their own take the
    # generic Space Marines list, so seven armies were each carrying a byte-identical
    # copy of the same 22 records -- 132 of 275 records were duplicates and slightly
    # over half the file. Emit one record per distinct detachment and let each army
    # index it by key. Deduplication is by content, so if a faction pack ever gives one
    # chapter its own text for a shared detachment, the records diverge and separate
    # entries reappear on their own.
    catalogue = OrderedDict()
    army_index = OrderedDict()
    for army, recs in armies.items():
        keys = []
        for r in recs:
            k = r["key"]
            if k in catalogue:
                if catalogue[k] != r:
                    raise SystemExit("key collision with differing content: %s" % k)
            else:
                catalogue[k] = r
            keys.append(k)
        army_index[army] = keys

    doc = OrderedDict([
        ("_meta", OrderedDict([
            ("generator", "detachment_parser.py"),
            ("numbers_source", "MFM faction files, 11th Edition v1.0"),
            ("text_sources", ["faction_pack", "wahapedia_10e", "none"]),
            ("armies", len(armies)),
            ("detachment_records", len(catalogue)),
            ("army_detachment_slots", n_det),
            ("enhancements", sum(len(r["enhancements"]) for r in catalogue.values())),
            ("upgrade_enhancements", sum(1 for r in catalogue.values()
                                         for e in r["enhancements"] if e["is_upgrade"])),
            ("force_disposition_counts", OrderedDict(sorted(
                _tally(catalogue.values(), lambda r: r["force_disposition"]).items()))),
            ("text_source_counts", OrderedDict(sorted(
                _tally(catalogue.values(), lambda r: r["text_source"]).items()))),
            ("enhancement_description_source_counts", OrderedDict(sorted(
                _tally([e for r in catalogue.values() for e in r["enhancements"]],
                       lambda e: e["description_source"]).items()))),
            ("wahapedia_only_enhancements_dropped", dropped_waha_enh),
            ("text_gap_manifest", sorted(
                {g["key"]: g for g in gaps}.values(), key=lambda g: g["key"])),
        ])),
        ("detachments", catalogue),
        ("armies", army_index),
    ])

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")

    if report_path:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("detachments: %d\nenhancements: %d\nupgrade: %d\n" % (n_det, n_enh, n_upg))
            f.write("text_source: %s\n" % tier_counts)
            f.write("enh desc source: %s\n" % desc_counts)
            f.write("dispositions: %s\n" % disp_counts)
            f.write("gaps (%d):\n" % len(gaps))
            for g in gaps:
                f.write("  %-18s %s (%dDP)\n" % (g["army"], g["detachment"], g["dp"]))
    return doc


def main():
    ap = argparse.ArgumentParser(description="Build detachments.json from MFM + text sources.")
    ap.add_argument("--root", default=".", help="directory holding the source files")
    ap.add_argument("--out", default="detachments.json")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    doc = build(a.root, a.out, a.report)
    m = doc["_meta"]
    print("detachments.json: %d armies, %d distinct detachments across %d army slots, "
          "%d enhancements (%d Upgrade)"
          % (m["armies"], m["detachment_records"], m["army_detachment_slots"],
             m["enhancements"], m["upgrade_enhancements"]))
    print("text_source: %s" % dict(m["text_source_counts"]))
    print("gaps: %d" % len(m["text_gap_manifest"]))


if __name__ == "__main__":
    main()
