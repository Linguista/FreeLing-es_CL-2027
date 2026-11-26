#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.0.0
#
# freeling_perkins.py -- step 080 of freeling.py (FreeLing es-CL 2027): the
# phonological transcriptions of Perkins for every token, one column per
# set of Perkins options, and a transcription of every utterance or line.
# Run it through freeling.py:
#
#     freeling.py CORPUS --perkins
#     freeling.py CORPUS --perkins --perkins-columns "-oa" --perkins-columns "-nt -oa"
#
# Reads 070-Universal-Dependency-Tagged, writes 080-Perkins-Tagged: the same
# files with one more column per set of options, named after the options
# (-nt -oa gives PERKINS_NT_OA). With the set -oa (phonemic, stress as ')
# come NSYL and STRESS. A set given with --perkins-word-alone transcribes
# each word on its own instead of the sentence as a whole (PERKINS_NT_OA_WORD).
# The default sets: -oa, -csc, -nt -oa, -f=MANNER -oa, -f=PLACE -oa,
# -f=V -oa, and -nt -oa word by word.
#
# In context: each sentence goes to perkins -tok as one line, so the rules
# that apply across words do, and a pause (punctuation, a stand-in) blocks
# them. A FreeLing multiword stays one row, its words separated by single
# spaces. A stand-in token is sent as a full stop, a pause in every column.
# del, al and pal, which FreeLing splits into de + el, a + el and
# para + el, are read as one word on de, a or para; el has "_". A false
# start (a token without a vowel right before an ellipsis) is read as its
# sounds. NOTHING IS LOST TO A MISALIGNMENT: a sentence Perkins does not
# return field for field is sent again alone, then token by token; a token
# that still fails gets "?"; every fallback is listed in the run's records.
#
# Beside each NAME.conll: NAME.utterances.tsv, one row per row of
# NAME.times.tsv (speech), or NAME.lines.tsv, one row per line of the text
# (read from the corpus root), with every set of options that is not a
# feature set (-f=) as running text.
#
# Every Perkins run is "perkins -nocfg -b ...", so no perkins.ini changes the
# result; Perkins older than 2.0.41 is refused. Perkins:
# https://github.com/Linguista/Perkins (GNU AGPL 3.0).
#
# A module of freeling.py: it does nothing when run on its own.

from __future__ import annotations

import concurrent.futures as cf
import filecmp
import re
import shutil
import subprocess
import tempfile
import threading
import time
import unicodedata
from pathlib import Path

import freeling_common as fc

VERSION = "1.0.0"
__version__ = VERSION

MIN_PERKINS = (2, 0, 41)
DEFAULT_COLUMNS = ["-oa", "-csc", "-nt -oa", "-f=MANNER -oa", "-f=PLACE -oa",
                   "-f=V -oa"]
DEFAULT_WORD_ALONE = ["-nt -oa"]
STRESS_SET = "-oa"
UTTERANCES = ".utterances.tsv"
LINES = ".lines.tsv"
PAUSES = {"|", "‖", "||", "(.)", "(...)", "##", "###"}
ELLIPSIS = re.compile(r"^\s*(?:\.{2,}|…+)\s*$")
VOWELS = set("aeiouáéíóúAEIOUÁÉÍÓÚɛɔəɨʉæɐɑɒøœ")
SYLLABIC_MARKS = ("̩", "̍")
VOWELLESS = "syllable-without-vowel"
FUNCTION_TAGS = ("DA", "DP", "SP", "CC", "CS", "PR", "P0")
STRESSED_RELATIVES = {"cual", "cuales"}
CLITICS = {"me", "te", "se", "lo", "la", "le", "nos", "os", "los", "las", "les"}
FUNCTION_FORMS = {
    "el", "la", "lo", "los", "las", "mi", "mis", "tu", "tus", "su", "sus",
    "a", "al", "de", "del", "pal", "en", "con", "por", "sin", "so", "tras",
    "y", "e", "o", "u", "ni", "que", "si", "quien",
    "me", "te", "se", "nos", "os", "le", "les",
}
CONTRACTIONS = {"de": ("del", (1,)), "a": ("al", (1,)), "para": ("pal", (2, 3))}
STOP = threading.Event()
C_SB = C_SE = C_FORM = C_TAG = 0           # set from columns.tsv by run()
# The stand-in tokens (stand-ins.tsv, set by run()): each is sent to
# Perkins as a full stop, so that every column has the pause there; Perkins
# would otherwise spell out the letters of any it does not know.
STANDIN_FORMS = set()
PAUSE_TEXT = "."


class Interrupted(Exception):
    pass


def nfc(s):
    return unicodedata.normalize("NFC", s)


def column_name(opts: str, alone=False):
    parts = [re.sub(r"[^A-Za-z0-9]+", "_", t.lstrip("-")).strip("_").upper()
             for t in opts.split()]
    return "PERKINS_" + "_".join(p for p in parts if p) + ("_WORD" if alone else "")


def layout(columns, word_alone):
    """The output columns in order: (name, kind, options), kind one of
    context, word, nsyl, stress."""
    out, placed = [], set()
    for o in columns:
        out.append((column_name(o), "context", o))
        if o == STRESS_SET:
            out.append(("NSYL", "nsyl", o))
            out.append(("STRESS", "stress", o))
        if o in word_alone:
            out.append((column_name(o, True), "word", o))
            placed.add(o)
    for o in word_alone:
        if o not in placed:
            out.append((column_name(o, True), "word", o))
    return out


# ---------------------------------------------------------------------------
def read_document(text, ncols):
    sents, cur = [], []
    for n, line in enumerate(text.split("\n"), 1):
        if line == "":
            if cur:
                sents.append(cur)
                cur = []
            continue
        f = line.split("\t")
        if len(f) != ncols:
            return None, "line %d has %d fields, not %d" % (n, len(f), ncols)
        if not (f[C_SB].isdigit() and f[C_SE].isdigit()):
            return None, "line %d: the spans are not numbers" % n
        cur.append(f)
    if cur:
        sents.append(cur)
    return sents, None


def contraction_word(prev, tok):
    if prev is None or tok[C_FORM].lower() != "el" or not prev[C_TAG].startswith("SP"):
        return None
    c = CONTRACTIONS.get(prev[C_FORM].lower())
    if c is None or int(tok[C_SB]) != int(prev[C_SE]):
        return None
    if int(tok[C_SE]) - int(tok[C_SB]) not in c[1]:
        return None
    if prev[C_FORM].lower() == "para" and int(prev[C_SE]) - int(prev[C_SB]) != 1:
        return None
    word = c[0]
    return prev[C_FORM][0] + word[1:] if prev[C_FORM][:1].isupper() else word


def is_contraction_el(prev, tok):
    return contraction_word(prev, tok) is not None


def multiword_parts(tok):
    parts = tok[C_FORM].split("_")
    short = len(" ".join(parts)) - (int(tok[C_SE]) - int(tok[C_SB]))
    i = 0
    while short >= 2 and i < len(parts) - 1:
        low, nxt = parts[i].lower(), parts[i + 1].lower()
        if low in ("de", "a") and nxt == "el":
            parts[i:i + 2] = [parts[i] + "l"]
            short -= 2
        elif low == "para" and nxt == "el" and short >= 3:
            parts[i:i + 2] = [parts[i][0] + "al"]
            short -= 4 if short >= 4 else 3
        else:
            i += 1
    return [p for p in parts if p]


def plan_sentence(sent):
    out, prev = [], None
    for i, tok in enumerate(sent):
        nxt = sent[i + 1] if i + 1 < len(sent) else None
        form = tok[C_FORM]
        if form in STANDIN_FORMS:
            out.append(("word", PAUSE_TEXT))
        elif is_contraction_el(prev, tok):
            out.append(("el", ""))
        elif nxt is not None and is_contraction_el(tok, nxt):
            out.append(("word", contraction_word(tok, nxt)))
        elif "_" in form and len(form.strip("_")) > 0:
            parts = multiword_parts(tok)
            out.append(("mwe", " ".join(parts)) if len(parts) > 1 else ("word", parts[0]))
        else:
            out.append(("word", form))
        prev = tok
    return out


# ---------------------------------------------------------------------------
def run_perkins(perkins, opts, text, tmp, tokens=True):
    if STOP.is_set():
        raise Interrupted()
    inp, out = tmp / "in.txt", tmp / "out.txt"
    inp.write_text(text, encoding="utf-8")
    fc.unlink_quietly(out)
    cmd = [perkins, "-nocfg", "-b"] + (["-tok"] if tokens else []) + opts.split() + \
        ["-i=%s" % inp, "-o=%s" % out]
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                       timeout=7200)
    if STOP.is_set():
        raise Interrupted()
    if r.returncode != 0 or not out.is_file():
        err = " ".join((r.stderr or b"").decode("utf-8", "replace").split())
        return None, "perkins %s exit %d: %s" % (opts, r.returncode, err[:160])
    return out.read_text(encoding="utf-8"), None


def perkins_lines(perkins, opts, lines, tmp, tokens=True):
    out, err = run_perkins(perkins, opts, "".join(l + "\n" for l in lines), tmp, tokens)
    if err:
        return None, err
    got = out.split("\n")
    if got and got[-1] == "":
        got.pop()
    if len(got) != len(lines):
        return None, "%d line(s) for %d" % (len(got), len(lines))
    return ([g.split("\t") for g in got] if tokens else got), None


def token_column(perkins, name, opts, lines, ntoks, tmp, notes):
    res, err = perkins_lines(perkins, opts, lines, tmp)
    if res is None:
        notes.append(("document-redone-by-sentence", name, "", "", err))
        res = [None] * len(lines)
    result = []
    for i, line in enumerate(lines):
        fields = res[i]
        if fields is not None and len(fields) == ntoks[i]:
            result.append(fields)
            continue
        if fields is not None:
            notes.append(("sentence-redone", name, i + 1, "",
                          "%d field(s) for %d token(s)" % (len(fields), ntoks[i])))
        one, err = perkins_lines(perkins, opts, [line], tmp)
        if one is not None and len(one[0]) == ntoks[i]:
            result.append(one[0])
            continue
        notes.append(("sentence-by-token", name, i + 1, "",
                      err or "%d field(s) for %d token(s)" % (len(one[0]), ntoks[i])))
        texts = line.split("\t")
        row = []
        each, err = perkins_lines(perkins, opts, texts, tmp)
        for j, t in enumerate(texts):
            if each is not None and len(each[j]) == 1:
                row.append(each[j][0])
                continue
            single, e2 = perkins_lines(perkins, opts, [t], tmp)
            if single is not None and len(single[0]) == 1:
                row.append(single[0][0])
            else:
                row.append("?")
                notes.append(("token-unresolved", name, i + 1, t, e2 or "no single field"))
        result.append(row)
    return result


def words_of(field):
    return nfc(field).split()


def joined(field):
    w = words_of(field)
    return " ".join(w) if w else "_"


def syllables(word):
    return [s for s in word.split(".") if s]


def has_nucleus(syl):
    return any(ch in VOWELS for ch in syl) or any(m in syl for m in SYLLABIC_MARKS)


def stress_of(word, function):
    syl = syllables(word)
    real = [s for s in syl if has_nucleus(s)]
    vowelless = len(real) != len(syl)
    n = len(real)
    if n == 0:
        return "0", "0", vowelless, False
    if n == 1:
        return "1", ("0" if function else "1"), vowelless, False
    marked = [i for i, s in enumerate(real) if "'" in s]
    if not marked and not any(ch in VOWELS for s in real for ch in s):
        return str(n), "1", vowelless, False
    if not marked:
        return str(n), "?", vowelless, True
    return str(n), str(n - marked[0]), vowelless, False


def nsyl_stress(phon, tok, kind, notes, sent_no, before_ellipsis=False):
    words = words_of(phon)
    if not words or all(w in PAUSES for w in words):
        return "_", "_"
    if kind == "mwe" or len(words) > 1:
        ns, st, vl, um = [], [], False, False
        for w in words:
            if w in PAUSES:
                ns.append("-")
                st.append("-")
                continue
            n, s, v, u = stress_of(w, False)
            ns.append(n)
            st.append(s)
            vl, um = vl or v, um or u
        if kind == "mwe":
            forms = multiword_parts(tok)
            if len(forms) == len(words):
                st = [("0" if n == "1" and f.lower() in FUNCTION_FORMS else s)
                      for f, n, s in zip(forms, ns, st)]
        nsyl, stress = " ".join(ns), " ".join(st)
    else:
        tag = tok[C_TAG]
        form = tok[C_FORM].lower()
        function = (tag[:2] in FUNCTION_TAGS
                    and not (tag.startswith("PR") and form in STRESSED_RELATIVES)) \
            or (tag.startswith("PP") and form in CLITICS)
        nsyl, stress, vl, um = stress_of(words[0], function)
    if vl and not (before_ellipsis and nsyl == "0"):
        notes.append((VOWELLESS, sent_no, tok[C_FORM], tok[C_TAG],
                      " ".join(words), nsyl, stress))
    if um:
        notes.append(("stress-not-found", "STRESS", sent_no, tok[C_FORM],
                      "%s %s" % (STRESS_SET, " ".join(words))))
    return nsyl, stress


# ---------------------------------------------------------------------------
# The utterance or line file.
def read_times(path):
    rows = []
    lines = path.read_text(encoding="utf-8").split("\n")
    head = lines[0].split("\t") if lines else []
    try:
        ii, si, ei = head.index("interval"), head.index("char_start"), head.index("char_end")
    except ValueError:
        return None, "%s has no interval, char_start and char_end columns" % path.name
    for n, line in enumerate(lines[1:], 2):
        if not line:
            continue
        f = line.split("\t")
        try:
            rows.append((f[ii], int(f[si]), int(f[ei])))
        except (IndexError, ValueError):
            return None, "%s line %d is not readable" % (path.name, n)
    return rows, None


def text_lines(path):
    """[(line number, start, end)] of the non-empty lines of a text, in
    characters, as FreeLing counts them."""
    text = path.read_text(encoding="utf-8")
    rows, pos = [], 0
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip():
            rows.append((str(n), pos, pos + len(line)))
        pos += len(line) + 1
    return rows


def unit_texts(sents, rows):
    toks = []
    for s in sents:
        for tok, (kind, text) in zip(s, plan_sentence(s)):
            if kind == "el":
                sb, _se, t = toks[-1]
                toks[-1] = (sb, int(tok[C_SE]), t)
                continue
            toks.append((int(tok[C_SB]), int(tok[C_SE]), text))
    toks.sort()
    texts, k, used = [], 0, 0
    for _iv, a, b in rows:
        while k < len(toks) and toks[k][0] < a:
            k += 1
        parts, last_end = [], None
        while k < len(toks) and toks[k][0] < b:
            sb, se, text = toks[k]
            if parts and last_end is not None and sb > last_end:
                parts.append(" ")
            parts.append(text)
            last_end = se
            k += 1
            used += 1
        texts.append("".join(parts))
    return texts, len(toks) - used


def unit_file(perkins, sents, rows, head, sets, tmp, notes):
    texts, stray = unit_texts(sents, rows)
    if stray:
        notes.append(("tokens-outside-rows", head, "", "",
                      "%d token(s) in no row" % stray))
    cols = []
    for name, opts in sets:
        got, err = perkins_lines(perkins, opts, texts, tmp, tokens=False)
        if got is None:
            notes.append(("rows-one-by-one", name, "", "", err))
            got = []
            for t in texts:
                one, e2 = perkins_lines(perkins, opts, [t], tmp, tokens=False)
                if one is None:
                    notes.append(("row-unresolved", name, "", t, e2))
                got.append(one[0] if one else "?")
        cols.append([nfc(" ".join(g.split())) or "_" for g in got])
    out = ["\t".join([head] + [n for n, _ in sets])]
    for i, (iv, _a, _b) in enumerate(rows):
        out.append("\t".join([iv] + [c[i] for c in cols]))
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
def convert(src, source_text, ncols, cols_layout, perkins, tmp, notes):
    sents, err = read_document(src.read_text(encoding="utf-8"), ncols)
    if err:
        raise ValueError(err)
    plans = [plan_sentence(s) for s in sents]
    lines = ["\t".join(t for _k, t in p) for p in plans]
    ntoks = [len(s) for s in sents]
    raw = {}
    for name, kind, opts in cols_layout:
        if kind == "context":
            raw[name] = token_column(perkins, name, opts, lines, ntoks, tmp, notes)
    for name, kind, opts in cols_layout:
        if kind != "word":
            continue
        units, unit_n, owners = [], [], []
        for si, p in enumerate(plans):
            s = sents[si]
            for ti, (k, t) in enumerate(p):
                if k == "el":
                    continue
                if k == "mwe":
                    for part in t.split(" "):
                        units.append(part)
                        unit_n.append(1)
                        owners.append((si, ti))
                    continue
                nxt = s[ti + 1][C_FORM] if ti + 1 < len(s) else ""
                if t and ELLIPSIS.match(nxt):
                    units.append(t + "\t" + nxt.strip())
                    unit_n.append(2)
                else:
                    units.append(t)
                    unit_n.append(1)
                owners.append((si, ti))
        alone = token_column(perkins, name, opts, units, unit_n, tmp, notes) if units else []
        got = [[[] for _ in s] for s in sents]
        for (si, ti), f in zip(owners, alone):
            got[si][ti].append(f[0] if f else "")
        raw[name] = got
    stress_col = column_name(STRESS_SET)
    out_lines = []
    for si, s in enumerate(sents):
        for ti, tok in enumerate(s):
            kind = plans[si][ti][0]
            if kind == "el":
                out_lines.append("\t".join(tok + ["_"] * len(cols_layout)))
                continue
            nxt = s[ti + 1][C_FORM] if ti + 1 < len(s) else ""
            ns_st = None
            fields = []
            for name, ck, _o in cols_layout:
                if ck == "context":
                    fields.append(joined(raw[name][si][ti]))
                elif ck == "word":
                    ws = [joined(x) for x in raw[name][si][ti]]
                    ws = [w for w in ws if w != "_"]
                    fields.append(" ".join(ws) if ws else "_")
                else:
                    if ns_st is None:
                        ns_st = nsyl_stress(raw[stress_col][si][ti], tok, kind,
                                            notes, si + 1, bool(ELLIPSIS.match(nxt)))
                    fields.append(ns_st[0] if ck == "nsyl" else ns_st[1])
            out_lines.append("\t".join(tok + fields))
        out_lines.append("")
    sets = [(n, o) for n, k, o in cols_layout if k == "context" and "-f=" not in o]
    unit = None
    side = src.with_name(src.name[:-len(".conll")] + fc.SIDECAR)
    if side.is_file():
        rows, err = read_times(side)
        if err:
            raise ValueError(err)
        unit = (UTTERANCES, unit_file(perkins, sents, rows, "INTERVAL", sets, tmp, notes))
    elif source_text is not None and source_text.is_file():
        unit = (LINES, unit_file(perkins, sents, text_lines(source_text), "LINE",
                                 sets, tmp, notes))
    elif sets:
        notes.append(("no-line-file", "LINES", "", "",
                      "the text is not in the corpus root: %s" % source_text))
    return "\n".join(out_lines) + "\n", unit, sum(ntoks)


def process(src, out, source_text, ncols, cols_layout, perkins):
    notes = []
    try:
        with tempfile.TemporaryDirectory(prefix="freeling-perkins-") as td:
            conll, unit, ntok = convert(src, source_text, ncols, cols_layout,
                                        perkins, Path(td), notes)
        stem = out.name[:-len(".conll")]
        side = src.with_name(src.name[:-len(".conll")] + fc.SIDECAR)
        if side.is_file():
            fc.put_file(side, out.with_name(stem + fc.SIDECAR))
        if unit is not None:
            fc.put_file(unit[1], out.with_name(stem + unit[0]))
        fc.put_file(conll, out)
        return "done", ntok, "", notes
    except Interrupted:
        return "interrupted", 0, "", notes
    except (ValueError, UnicodeDecodeError, OSError, subprocess.SubprocessError) as exc:
        return "failed", 0, "%s: %s" % (type(exc).__name__, exc), notes


STAGE_README = """# 080-Perkins-Tagged / {name}

Made by `freeling.py` {fversion} with `freeling_perkins.py` {version}
(FreeLing es-CL 2027) on {date}, from 070-Universal-Dependency-Tagged, with
{perkins} (https://github.com/Linguista/Perkins, GNU AGPL 3.0). Documents
in this stage: {docs}.

## What is in it

The files of 070-Universal-Dependency-Tagged, with one more TAB-separated
column per set of Perkins options, named after the options; every column is
listed, with its options, in `columns.tsv`:

{columns}

- In context: each sentence is transcribed whole, so the rules that apply
  across words do, and a pause (punctuation, a stand-in) blocks them. A
  column ending in `_WORD` has each word transcribed on its own.
- A FreeLing multiword stays one row, its words separated by single spaces
  in every Perkins column; `_` only ever means an empty field. del, al and
  pal (split by FreeLing into de + el, a + el, para + el) are read as one
  word on de, a or para; el has `_`.
- `NSYL` and `STRESS` (with the set -oa): the number of syllables, and the
  stressed syllable counted from the end (1 the last; 0 for a one-syllable
  function word).
- Beside each `NAME.conll`: `NAME.utterances.tsv` (one row per row of
  `NAME.times.tsv`, numbered by its interval) or `NAME.lines.tsv` (one row
  per line of the text, numbered by its line), with the transcriptions of
  the whole utterance or line as running text. `NAME.times.tsv` is copied
  from 070.

## How it was made

`{command}`

## What it is used for next

`freeling.py {name} --parquet` (400-Parquet).

## Records

`_processing-records/` holds, for each run that had any, the fallback list
(sentences Perkins did not return field for field, sent again alone or
token by token), the list of tokens in which Perkins wrote a syllable
without a vowel (a misspelling, or a word that is not Spanish), and the
failure list.
"""


def perkins_version(perkins):
    r = subprocess.run([perkins, "-h"], capture_output=True, text=True)
    ver = next((l.strip(" |") for l in (r.stdout + r.stderr).splitlines()
                if "Perkins v" in l), "version not reported")
    ver = " ".join(ver.split())
    m = re.search(r"Perkins v(\d+)\.(\d+)\.(\d+)", ver)
    ok = m is not None and tuple(int(x) for x in m.groups()) >= MIN_PERKINS
    return ver, ok


def run(ctx):
    global C_SB, C_SE, C_FORM, C_TAG, STANDIN_FORMS
    a = ctx.a
    src_root, dst_root = ctx.stage("070"), ctx.stage("080")
    fc.log("")
    fc.log("STEP 080  %s" % fc.STAGES["080"][0])
    sets = a.perkins_columns or DEFAULT_COLUMNS
    alone = a.perkins_word_alone if a.perkins_columns else (
        a.perkins_word_alone or DEFAULT_WORD_ALONE)
    cols_layout = layout(sets, alone)
    names = [n for n, _, _ in cols_layout]
    if len(set(names)) != len(names):
        fc.log(fc.red("REFUSED: two sets of options give the same column: %s"
                      % ", ".join(names)))
        return 2
    for n, k, o in cols_layout:
        fc.log("column : %-22s perkins -tok %s%s" % (n, o, "  (each word alone)"
                                                      if k == "word" else
                                                      "  (from %s)" % o if k in
                                                      ("nsyl", "stress") else ""))
    standins, p = fc.load_standins(ctx.fl)
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    STANDIN_FORMS = {f for f, _, _ in standins}
    perkins = shutil.which(a.perkins_bin)
    if perkins is None:
        fc.log(fc.red("REFUSED: perkins not found: %s (https://github.com/"
                      "Linguista/Perkins; give --perkins-bin FILE)" % a.perkins_bin))
        return 2
    ver, ok = perkins_version(perkins)
    fc.log("perkins: %s  (%s)" % (perkins, ver))
    if not ok:
        fc.log(fc.red("REFUSED: Perkins %s or later is needed"
                      % ".".join(map(str, MIN_PERKINS))))
        return 2
    rows, p = fc.read_columns(src_root)
    if p:
        if a.dry_run:
            fc.log("would read %s once --ud has made it" % src_root)
            return 0
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    cn = [r[0] for r in rows]
    for need in ("SPAN_BEGIN", "SPAN_END", "FORM", "TAG"):
        if need not in cn:
            fc.log(fc.red("REFUSED: %s has no %s column" % (src_root, need)))
            return 2
    clash = [n for n in names if n in cn]
    if clash:
        fc.log(fc.red("REFUSED: %s has the column(s) %s already"
                      % (src_root, ", ".join(clash))))
        return 2
    C_SB, C_SE, C_FORM, C_TAG = (cn.index(c) for c in
                                 ("SPAN_BEGIN", "SPAN_END", "FORM", "TAG"))
    docs = fc.corpus_files(src_root, ".conll")
    if a.only:
        o = Path(a.only.strip("/")).parts
        docs = [d for d in docs if d.relative_to(src_root).parts[:len(o)] == o]
    if not docs:
        fc.log(fc.red("REFUSED: no .conll files under %s" % src_root))
        return 2
    for p_ in (dst_root / "README.md", dst_root / fc.COLUMNS_TSV):
        w = fc.locked(p_)
        if w:
            fc.log(fc.red("REFUSED: cannot be replaced (%s): %s" % (w, p_)))
            return 2
    failures, todo, skipped, restored = [], [], 0, 0
    for d in docs:
        rel = d.relative_to(src_root)
        out = dst_root / rel
        stem = out.name[:-len(".conll")]
        side = d.with_name(stem + fc.SIDECAR)
        dside = out.with_name(stem + fc.SIDECAR)
        source = ctx.root / rel.with_name(stem + a.ext)
        if out.exists() and not a.redo:
            skipped += 1
            if side.is_file() and not dside.exists() and not a.dry_run:
                try:
                    fc.put_file(side, dside)
                    restored += 1
                except OSError as exc:
                    failures.append(("cannot restore %s: %s" % (dside.name, exc), str(d)))
            elif side.is_file() and dside.exists() and \
                    not filecmp.cmp(side, dside, shallow=False):
                failures.append(("%s differs from the one in 070; --redo "
                                 "rewrites it" % dside.name, str(d)))
            continue
        todo.append((d, out, source))
        if a.limit and len(todo) >= a.limit:
            break
    fc.log("%d to do, %d already done" % (len(todo), skipped))
    if a.dry_run:
        bad = 0
        for d, out, source in todo:
            _s, err = read_document(d.read_text(encoding="utf-8"), len(cn))
            if err:
                bad += 1
                fc.log("FAILED  %s  %s" % (err, d))
        return 1 if bad or failures else 0
    fc.ensure_stage(ctx.cdir, "080")
    rec = fc.ensure_records(dst_root)
    t0 = time.time()
    done = failed = tokens = 0
    falls, vowelless = [], []
    interrupted = False
    ex = cf.ThreadPoolExecutor(max_workers=max(1, a.jobs))
    try:
        futs = {ex.submit(process, d, out, source, len(cn), cols_layout, perkins): d
                for d, out, source in todo}
        for fut in cf.as_completed(futs):
            d = futs[fut]
            status, n, msg, notes = fut.result()
            if status == "interrupted":
                continue
            nfall = 0
            for note in notes:
                if note[0] == VOWELLESS:
                    vowelless.append("\t".join(str(x) for x in note[1:] + (d,)))
                else:
                    falls.append("\t".join(str(x) for x in note + (d,)))
                    nfall += 1
            done += 1
            tokens += n
            if status == "failed":
                failed += 1
                failures.append((msg, str(d)))
            el = max(time.time() - t0, 0.001)
            fc.log("%6d/%d  %11s tok  %6.0f tok/s  %s%s%s"
                   % (done, len(todo), f"{tokens:,}", tokens / el,
                      "FAILED  " if status == "failed" else "",
                      "%d fallback(s)  " % nfall if nfall else "",
                      d.relative_to(src_root)))
            if status == "failed":
                fc.log("          %s" % msg)
    except KeyboardInterrupt:
        interrupted = True
        STOP.set()
        fc.log("interrupted: the documents in progress write nothing; the same "
               "command resumes")
    finally:
        ex.shutdown(wait=True, cancel_futures=True)
    if falls:
        fp = fc.free_name(rec, "perkins-fallbacks--%s" % ctx.stamp)
        fc.put_file("rule\tcolumn\tsentence\ttoken\tdetail\tfile\n" + "\n".join(falls) + "\n", fp)
        fc.log("fallback list: %s" % fp)
    if vowelless:
        vp = fc.free_name(rec, "perkins-vowelless-syllables--%s" % ctx.stamp)
        fc.put_file("sentence\ttoken\ttag\ttranscription\tNSYL\tSTRESS\tfile\n"
                    + "\n".join(vowelless) + "\n", vp)
        fc.log("vowelless-syllables list: %s" % vp)
    if failures:
        fp = fc.free_name(rec, "perkins-FAILED--%s" % ctx.stamp)
        fc.put_file("reason\tfile\n" + "".join("%s\t%s\n" % f for f in failures), fp)
        fc.log(fc.orange("failure list: %s" % fp))
    fc.log("-" * 78)
    fc.log("converted %d, failed %d, already done %d; %s tokens; %s"
           % (done - failed, failed, skipped, f"{tokens:,}", fc.hms(time.time() - t0)))
    if restored:
        fc.log("sidecars restored: %d" % restored)
    if interrupted:
        return 130
    program = "%s; freeling_perkins.py %s (freeling.py %s)" % (ver, VERSION, ctx.version)
    out_rows = list(rows)
    for n, k, o in cols_layout:
        opt = {"context": "perkins -nocfg -b -tok %s" % o,
               "word": "perkins -nocfg -b -tok %s, each word alone" % o,
               "nsyl": "syllables with a vowel or a syllabic consonant, from %s"
                       % column_name(o),
               "stress": "the stressed syllable from the end, from %s"
                         % column_name(o)}[k]
        out_rows.append((n, "--perkins", opt, program))
    fc.write_columns(dst_root, out_rows)
    if not ((a.only or a.limit) and (dst_root / "README.md").is_file()):
        ndocs = len(fc.corpus_files(dst_root, ".conll"))
        fc.write_readme(dst_root, STAGE_README.format(
            name=ctx.name, fversion=ctx.version, version=VERSION,
            date=time.strftime("%Y-%m-%d"), perkins=ver, docs=f"{ndocs:,}",
            columns="\n".join("- `%s`: %s" % (r[0], r[2]) for r in out_rows[len(rows):]),
            command=ctx.command))
        fc.log("stage README: %s" % (dst_root / "README.md"))
    return 1 if failures else 0


if __name__ == "__main__":
    print("freeling_perkins.py is step 080 of freeling.py: freeling.py CORPUS --perkins")
