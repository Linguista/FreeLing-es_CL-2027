#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.0.0
#
# freeling_ud.py -- step 070 of freeling.py (FreeLing es-CL 2027):
# Universal Dependencies part of speech (UPOS) and features (FEATS) for
# every token, translated rule by rule from FreeLing's EAGLES tag as the
# es-cl tagset defines it. Run it through freeling.py:
#
#     freeling.py CORPUS --ud
#
# Reads 060-FreeLing-Tagged, writes 070-Universal-Dependency-Tagged: the
# same files with two more columns, UPOS and FEATS; every column of 060 is
# copied byte for byte, and each NAME.times.tsv is copied beside its
# NAME.conll (the sidecar first, the .conll last). The columns are found by
# name, from the columns.tsv of 060.
#
# Features of this project, besides UD's own (UD allows a corpus its own):
#   Voseo=Yes                             voseo verb forms and vos
#   Evaluative=Dim|Aug|Pej|Approx|Yes     nouns and adjectives FreeLing
#                                         marks evaluative
#   MWE=Yes                               a FreeLing multiword kept whole
#   Clitic=Yes                            a verb still joined to its clitic
#   StandIn=<name>                        a stand-in token (UPOS X)
#
# A module of freeling.py: it does nothing when run on its own.

from __future__ import annotations

import filecmp
import os
import time
from collections import Counter
from pathlib import Path

import freeling_common as fc

VERSION = "1.0.0"
__version__ = VERSION

GENDER = {"F": "Fem", "M": "Masc"}
NUMBER = {"S": "Sing", "P": "Plur"}
PERSON = {"1": "1", "2": "2", "3": "3"}
PRONTYPE = {"A": "Art", "D": "Dem", "E": "Exc", "I": "Ind", "P": "Prs",
            "R": "Rel", "T": "Int"}
CASE = {"N": "Nom", "A": "Acc", "D": "Dat"}
MOOD = {"I": "Ind", "S": "Sub", "M": "Imp"}
TENSE = {"P": "Pres", "I": "Imp", "F": "Fut", "S": "Past"}
VERBFORM = {"P": "Part", "G": "Ger", "N": "Inf"}
PUNCT = {
    "Fc": ("Comm", None), "Fp": ("Peri", None), "Fs": ("Elip", None),
    "Fd": ("Colo", None), "Fx": ("Semi", None), "Fg": ("Dash", None),
    "Fh": ("Slsh", None), "Fe": ("Quot", None), "Ft": ("Pct", None),
    "Fia": ("Qest", "Ini"), "Fit": ("Qest", "Fin"),
    "Faa": ("Excl", "Ini"), "Fat": ("Excl", "Fin"),
    "Fpa": ("Brck", "Ini"), "Fpt": ("Brck", "Fin"),
    "Fca": ("Brck", "Ini"), "Fct": ("Brck", "Fin"),
    "Fla": ("Brck", "Ini"), "Flt": ("Brck", "Fin"),
    "Fra": ("Quot", "Ini"), "Frc": ("Quot", "Fin"),
}
# The StandIn value of a stand-in: its name between the XXXs; these names
# are written as UD writes a value (NonSpeech, not Nonspeech).
STANDIN_VALUES = {"REDACTED": "Redacted", "UNINTELLIGIBLE": "Unintelligible",
                  "NONSPEECH": "NonSpeech", "URL": "Url",
                  "EMAILADDR": "EmailAddr"}

# Evaluative suffixes. Sources: RAE, Glosario de terminos gramaticales,
# "sufijo apreciativo" and "sufijo diminutivo" (NGLE 9.1 to 9.6); RAE,
# "Clases de apreciativos. Los diminutivos" and "Aumentativos y
# despectivos". -uelo and -zuelo are pejorative. -iento forms adjectives
# (hambre > hambriento) and is not appreciative, except in peliento and
# upeliento, which are pejorative. Matched on the singular form, longest
# suffix first; a form that matches none gets Evaluative=Yes.
EVAL_SUFFIXES = [
    ("Dim", "ito"), ("Dim", "ita"), ("Dim", "íto"), ("Dim", "íta"),
    ("Dim", "illo"), ("Dim", "illa"),
    ("Dim", "ico"), ("Dim", "ica"), ("Dim", "ín"), ("Dim", "ina"),
    ("Dim", "ino"), ("Dim", "ete"), ("Dim", "eta"), ("Dim", "ingo"),
    ("Dim", "inga"), ("Dim", "iño"), ("Dim", "iña"), ("Dim", "uco"),
    ("Dim", "uca"),
    ("Aug", "ón"), ("Aug", "ona"), ("Aug", "azo"), ("Aug", "aza"),
    ("Aug", "ote"), ("Aug", "ota"), ("Aug", "azas"),
    ("Pej", "ucho"), ("Pej", "ucha"), ("Pej", "acho"), ("Pej", "acha"),
    ("Pej", "aco"), ("Pej", "aca"), ("Pej", "ajo"), ("Pej", "aja"),
    ("Pej", "ejo"), ("Pej", "eja"), ("Pej", "astro"), ("Pej", "astra"),
    ("Pej", "orrio"), ("Pej", "orro"), ("Pej", "orra"), ("Pej", "ute"),
    ("Pej", "uza"), ("Pej", "uzo"), ("Pej", "ales"), ("Pej", "uelo"),
    ("Pej", "uela"),
    ("Approx", "uzco"), ("Approx", "uzca"), ("Approx", "usco"),
    ("Approx", "usca"),
]
EVAL_SUFFIXES.sort(key=lambda x: -len(x[1]))
EVAL_WORDS = {"peliento": "Pej", "pelienta": "Pej",
              "upeliento": "Pej", "upelienta": "Pej"}
NOT_EVALUATIVE_ENDINGS = ("iento", "ienta")


def singular_candidates(form):
    f = form.lower()
    out = [f]
    if f.endswith("ones"):
        out.append(f[:-4] + "ón")
    if f.endswith("ines"):
        out.append(f[:-4] + "ín")
    if f.endswith("es"):
        out.append(f[:-2])
    if f.endswith("s"):
        out.append(f[:-1])
    return out


def evaluative_word(form):
    cands = singular_candidates(form)
    for c in cands:
        if c in EVAL_WORDS:
            return EVAL_WORDS[c]
    for c in cands:
        if c.endswith(NOT_EVALUATIVE_ENDINGS):
            return None
    for kind, suf in EVAL_SUFFIXES:
        for c in cands:
            if c.endswith(suf) and len(c) > len(suf) + 1:
                return kind
    return "Yes"


def evaluative(form):
    """A multiword is matched part by part, head first (autitos_chocadores:
    Dim)."""
    parts = [p for p in form.split("_") if p]
    if len(parts) < 2:
        return evaluative_word(form)
    values = [evaluative_word(p) for p in parts]
    for v in values:
        if v not in ("Yes", None):
            return v
    return None if None in values else "Yes"


def feats_str(d):
    if not d:
        return "_"
    return "|".join("%s=%s" % (k, d[k]) for k in sorted(d, key=str.lower))


def pos(tag, i):
    return tag[i] if len(tag) > i else "0"


def map_tag(tag, form, lemma):
    """(UPOS, features) from one EAGLES tag."""
    f = {}
    c = tag[:1]
    if tag in PUNCT or c == "F":
        pt = PUNCT.get(tag)
        if pt:
            f["PunctType"] = pt[0]
            if pt[1]:
                f["PunctSide"] = pt[1]
        if any(ch.isalpha() for ch in form):
            return "ADV", {}
        return ("SYM" if tag == "Fz" else "PUNCT"), f
    if c == "N":
        upos = "PROPN" if pos(tag, 1) == "P" else "NOUN"
        if pos(tag, 2) in GENDER:
            f["Gender"] = GENDER[pos(tag, 2)]
        if pos(tag, 3) in NUMBER:
            f["Number"] = NUMBER[pos(tag, 3)]
        if pos(tag, 6) == "V":
            f["Evaluative"] = evaluative(form)
        return upos, f
    if c == "A":
        t = pos(tag, 1)
        if t == "P":
            f["Poss"] = "Yes"
            f["PronType"] = "Prs"
            if pos(tag, 5) in PERSON:
                f["Person"] = pos(tag, 5)
            if pos(tag, 6) in NUMBER:
                f["Number[psor]"] = NUMBER[pos(tag, 6)]
            upos = "DET"
        else:
            upos = "ADJ"
            if t == "O":
                f["NumType"] = "Ord"
            if pos(tag, 2) == "S":
                f["Degree"] = "Abs"
            elif pos(tag, 2) == "V":
                f["Evaluative"] = evaluative(form)
        if pos(tag, 3) in GENDER:
            f["Gender"] = GENDER[pos(tag, 3)]
        if pos(tag, 4) in NUMBER:
            f["Number"] = NUMBER[pos(tag, 4)]
        return upos, f
    if c == "D":
        t = pos(tag, 1)
        if t in PRONTYPE:
            f["PronType"] = PRONTYPE[t]
        if t == "A":
            f["Definite"] = "Def"
        if t == "I" and lemma == "uno":
            f["PronType"] = "Art"
            f["Definite"] = "Ind"
        if t == "P":
            f["Poss"] = "Yes"
            f["PronType"] = "Prs"
            if pos(tag, 5) in NUMBER:
                f["Number[psor]"] = NUMBER[pos(tag, 5)]
        if pos(tag, 2) in PERSON:
            f["Person"] = pos(tag, 2)
        if pos(tag, 3) in GENDER:
            f["Gender"] = GENDER[pos(tag, 3)]
        if pos(tag, 4) in NUMBER:
            f["Number"] = NUMBER[pos(tag, 4)]
        return "DET", f
    if c == "P":
        t = pos(tag, 1)
        if t in PRONTYPE:
            f["PronType"] = PRONTYPE[t]
        elif t == "0":
            f["PronType"] = "Prs"
            f["Reflex"] = "Yes"
        if pos(tag, 2) in PERSON:
            f["Person"] = pos(tag, 2)
        if pos(tag, 3) in GENDER:
            f["Gender"] = GENDER[pos(tag, 3)]
        if pos(tag, 4) in NUMBER:
            f["Number"] = NUMBER[pos(tag, 4)]
        cs = pos(tag, 5)
        if cs in CASE:
            f["Case"] = CASE[cs]
        elif cs == "O":
            f["PrepCase"] = "Pre"
        pl = pos(tag, 6)
        if pl == "P":
            f["Polite"] = "Form"
        elif pl == "V":
            f["Voseo"] = "Yes"
            f["Person"] = "2"
            f["Number"] = "Sing"
        return "PRON", f
    if c == "V":
        mood, tense = pos(tag, 2), pos(tag, 3)
        if mood in VERBFORM:
            f["VerbForm"] = VERBFORM[mood]
            if mood == "P":
                f["Tense"] = "Past"
        else:
            f["VerbForm"] = "Fin"
            if tense == "C":
                f["Mood"] = "Cnd"
            else:
                if mood in MOOD:
                    f["Mood"] = MOOD[mood]
                if tense in TENSE:
                    f["Tense"] = TENSE[tense]
        if pos(tag, 4) in PERSON:
            f["Person"] = pos(tag, 4)
        if pos(tag, 5) in NUMBER:
            f["Number"] = NUMBER[pos(tag, 5)]
        g = pos(tag, 6)
        if g == "V":
            f["Voseo"] = "Yes"
            f["Person"] = "2"
            f["Number"] = "Sing"
        elif g in GENDER:
            f["Gender"] = GENDER[g]
        return "VERB", f
    if c == "R":
        if pos(tag, 1) == "N":
            f["Polarity"] = "Neg"
        return "ADV", f
    if c == "S":
        f["AdpType"] = "Prep"
        return "ADP", f
    if c == "C":
        return ("SCONJ" if pos(tag, 1) == "S" else "CCONJ"), f
    if c == "I":
        return "INTJ", f
    if c == "Z":
        f["NumType"] = "Card"
        return "NUM", f
    if c == "W":
        return "NOUN", f
    return None, f


class Columns:
    def __init__(self, names):
        self.n = len(names)
        ix = {c: i for i, c in enumerate(names)}
        self.id = ix.get("ID")
        self.form = ix["FORM"]
        self.lemma = ix["LEMMA"]
        self.tag = ix["TAG"]
        self.head = ix.get("DEPHEAD")
        self.rel = ix.get("DEPREL")


def aux_or_verb(tok, cols, lemma, tag, has_atr_child, head_tag):
    """ser: always AUX. haber: AUX when tagged auxiliary or attached as
    auxiliary (v) to a participle; otherwise VERB (existential hay, hay
    que). estar: AUX when tagged auxiliary, attached as auxiliary to a
    gerund or participle, or governing an atr (copula); otherwise VERB."""
    t = tag[1] if len(tag) > 1 else ""
    if t == "S" or lemma == "ser":
        return "AUX"
    if lemma not in ("haber", "estar"):
        return "VERB"
    if t == "A":
        return "AUX"
    if cols.rel is None:
        return "VERB"
    ht = head_tag or ""
    if tok[cols.rel] == "v" and ht[:1] == "V" and ht[2:3] in (
            ("P",) if lemma == "haber" else ("P", "G")):
        return "AUX"
    if lemma == "estar" and has_atr_child:
        return "AUX"
    return "VERB"


def convert_sentence(toks, cols, standins, stats):
    have_parse = cols.head is not None and cols.rel is not None and cols.id is not None
    atr_heads = {t[cols.head] for t in toks if t[cols.rel] == "atr"} if have_parse else set()
    tag_of = {t[cols.id]: t[cols.tag] for t in toks} if have_parse else {}
    out = []
    for t in toks:
        form, lemma, tag = t[cols.form], t[cols.lemma], t[cols.tag]
        parts = tag.split("+")
        upos, f = map_tag(parts[0], form, lemma)
        if upos is None:
            stats["unmapped"][tag] += 1
            upos, f = "X", {}
        if upos == "VERB":
            upos = aux_or_verb(t, cols, lemma, parts[0],
                               have_parse and t[cols.id] in atr_heads,
                               tag_of.get(t[cols.head]) if have_parse else None)
        if len(parts) > 1:
            f["Clitic"] = "Yes"
        st = None
        for k, v in standins.items():
            if k in form:
                st = v
                break
        if st:
            f["StandIn"] = st
            if form in standins:
                upos = "X"
                f.pop("PunctType", None)
                f.pop("PunctSide", None)
        if "_" in form and form not in standins:
            f["MWE"] = "Yes"
        if "Evaluative" in f:
            if f["Evaluative"] is None:
                del f["Evaluative"]
                stats["evaluative"][("none (-iento, adjective-forming)",
                                     form.lower(), tag)] += 1
            else:
                stats["evaluative"][(f["Evaluative"], form.lower(), tag)] += 1
        stats["upos"][upos] += 1
        out.append(t + [upos, feats_str(f)])
    return out


def convert_file(src, cols, standins, stats):
    lines_out, sent = [], []
    with open(src, encoding="utf-8", newline="") as fh:
        for n, raw in enumerate(fh, 1):
            line = raw.rstrip("\n").rstrip("\r")
            if not line:
                if sent:
                    lines_out.extend("\t".join(x) for x in
                                     convert_sentence(sent, cols, standins, stats))
                    sent = []
                lines_out.append("")
                continue
            fields = line.split("\t")
            if len(fields) != cols.n:
                raise ValueError("line %d has %d fields, not %d"
                                 % (n, len(fields), cols.n))
            sent.append(fields)
            stats["tokens"] += 1
    if sent:
        lines_out.extend("\t".join(x) for x in
                         convert_sentence(sent, cols, standins, stats))
    return "\n".join(lines_out) + "\n"


STAGE_README = """# 070-Universal-Dependency-Tagged / {name}

Made by `freeling.py` {fversion} with `freeling_ud.py` {version}
(FreeLing es-CL 2027) on {date}, from 060-FreeLing-Tagged. Documents in
this stage: {docs}.

## What is in it

The files of 060-FreeLing-Tagged, with two more TAB-separated columns per
token (all columns are listed in `columns.tsv`):

- `UPOS`: the Universal Dependencies part of speech;
- `FEATS`: the UD features, `Name=Value`, sorted by name and joined by
  vertical bars; `_` when there are none.

Both are translated rule by rule from FreeLing's tag, as the es-cl tagset
defines it; nothing is tagged again. Every column of 060 is copied byte for
byte, and each `NAME.times.tsv` beside a `NAME.conll`.

Features of this project, besides UD's own: `Voseo=Yes`,
`Evaluative=Dim|Aug|Pej|Approx|Yes`, `MWE=Yes` (a FreeLing multiword kept
whole), `Clitic=Yes` (a verb still joined to its clitic), and
`StandIn=<name>` on the stand-in tokens ({standins}), whose UPOS is X. The
full mapping is in `freeling_ud_README.md` in the release's `software/`.

## How it was made

`{command}`

## What it is used for next

`freeling.py {name} --perkins` (080-Perkins-Tagged; not for written-old)
and `freeling.py {name} --parquet` (400-Parquet).

## Records

`_processing-records/` holds the evaluative report of each run (every
evaluative form with its value and count) and the failure list of a run
that had failures.
"""


def run(ctx):
    a = ctx.a
    src_root, dst_root = ctx.stage("060"), ctx.stage("070")
    fc.log("")
    fc.log("STEP 070  %s" % fc.STAGES["070"][0])
    rows, p = fc.read_columns(src_root)
    if p:
        if a.dry_run:
            fc.log("would read %s once --freeling has made it" % src_root)
            return 0
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    names = [r[0] for r in rows]
    for need in ("FORM", "LEMMA", "TAG"):
        if need not in names:
            fc.log(fc.red("REFUSED: %s has no %s column" % (src_root, need)))
            return 2
    if "UPOS" in names:
        fc.log(fc.red("REFUSED: %s has a UPOS column already" % src_root))
        return 2
    standins, p = fc.load_standins(ctx.fl)
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    sti = {f: STANDIN_VALUES.get(f[3:-3], f[3:-3].capitalize())
           for f, _, _ in standins}
    cols = Columns(names)
    files = fc.corpus_files(src_root, ".conll")
    if a.only:
        files = [f for f in files
                 if f.relative_to(src_root).parts[:len(Path(a.only.strip("/")).parts)]
                 == Path(a.only.strip("/")).parts]
    if not files:
        fc.log(fc.red("REFUSED: no .conll files under %s" % src_root))
        return 2
    why = [(p, fc.locked(p)) for p in (dst_root / "README.md",
                                       dst_root / fc.COLUMNS_TSV)]
    why = [(p, w) for p, w in why if w]
    if why:
        for p, w in why:
            fc.log(fc.red("REFUSED: cannot be replaced (%s): %s" % (w, p)))
        return 2
    fc.log("from   : %s" % src_root)
    fc.log("to     : %s" % dst_root)
    todo, skipped, failures, restored = [], 0, [], 0
    for f in files:
        rel = f.relative_to(src_root)
        out = dst_root / rel
        side = f.with_name(f.name[:-len(".conll")] + fc.SIDECAR)
        dside = out.with_name(out.name[:-len(".conll")] + fc.SIDECAR)
        if out.exists() and not a.redo:
            skipped += 1
            if side.is_file() and not dside.exists() and not a.dry_run:
                try:
                    fc.put_file(side, dside)
                    restored += 1
                    fc.log("sidecar restored: %s" % dside)
                except OSError as exc:
                    failures.append(("cannot restore %s: %s" % (dside.name, exc), f))
            elif side.is_file() and dside.exists() and \
                    not filecmp.cmp(side, dside, shallow=False):
                failures.append(("%s differs from the one in 060; --redo "
                                 "rewrites it" % dside.name, f))
            continue
        todo.append((f, out, side, dside))
        if a.limit and len(todo) >= a.limit:
            break
    fc.log("%d to do, %d already done" % (len(todo), skipped))
    if not a.dry_run:
        fc.ensure_stage(ctx.cdir, "070")
        fc.ensure_records(dst_root)
    stats = {"tokens": 0, "unmapped": Counter(), "evaluative": Counter(),
             "upos": Counter()}
    done = 0
    t0 = time.time()
    for i, (f, out, side, dside) in enumerate(todo, 1):
        fstats = {"tokens": 0, "unmapped": Counter(), "evaluative": Counter(),
                  "upos": Counter()}
        try:
            text = convert_file(f, cols, sti, fstats)
        except (ValueError, UnicodeDecodeError, OSError) as exc:
            failures.append((str(exc), f))
            fc.log("FAILED  %s  %s" % (exc, f))
            continue
        if not a.dry_run:
            try:
                if side.is_file():
                    fc.put_file(side, dside)
                fc.put_file(text, out)
            except OSError as exc:
                failures.append(("cannot write: %s" % exc, f))
                fc.log("FAILED  %s  %s" % (exc, out))
                continue
        for k in stats:
            stats[k] += fstats[k]
        done += 1
        el = max(time.time() - t0, 0.001)
        fc.log("%6d/%d  %11s tok  %7.0f tok/s  %s"
               % (i, len(todo), f"{stats['tokens']:,}", stats["tokens"] / el,
                  f.relative_to(src_root)))
    fc.log("-" * 78)
    fc.log("converted %d, already done %d, failed %d; %s tokens"
           % (done, skipped, len(failures), f"{stats['tokens']:,}"))
    if restored:
        fc.log("sidecars restored: %d" % restored)
    fc.log("UPOS: " + ("  ".join("%s %s" % (k, f"{v:,}")
                                 for k, v in stats["upos"].most_common()) or "none"))
    if stats["unmapped"]:
        fc.log(fc.orange("tags not mapped (written as X): " + "  ".join(
            "%s %d" % kv for kv in stats["unmapped"].most_common())))
    if a.dry_run:
        return 1 if failures else 0
    rec = dst_root / fc.RECORDS
    if done:
        ev = fc.free_name(rec, "ud-evaluative--%s" % ctx.stamp)
        fc.put_file("value\tform\ttag\tcount\n" + "".join(
            "%s\t%s\t%s\t%d\n" % (v, form, tag, n)
            for (v, form, tag), n in sorted(stats["evaluative"].items(),
                                            key=lambda kv: (kv[0][0], -kv[1]))), ev)
        fc.log("evaluative report: %s" % ev)
    if failures:
        fp = fc.free_name(rec, "ud-FAILED--%s" % ctx.stamp)
        fc.put_file("reason\tfile\n" + "".join("%s\t%s\n" % (r, p)
                                               for r, p in failures), fp)
        fc.log(fc.orange("failure list: %s" % fp))
    program = "freeling_ud.py %s (freeling.py %s)" % (VERSION, ctx.version)
    fc.write_columns(dst_root, list(rows) + [
        ("UPOS", "--ud", "UD part of speech from TAG", program),
        ("FEATS", "--ud", "UD features from TAG", program)])
    if not ((a.only or a.limit) and (dst_root / "README.md").is_file()):
        docs = len(fc.corpus_files(dst_root, ".conll"))
        fc.write_readme(dst_root, STAGE_README.format(
            name=ctx.name, fversion=ctx.version, version=VERSION,
            date=time.strftime("%Y-%m-%d"), docs=f"{docs:,}",
            standins=", ".join(sorted(sti)), command=ctx.command))
        fc.log("stage README: %s" % (dst_root / "README.md"))
    return 1 if failures else 0


if __name__ == "__main__":
    print("freeling_ud.py is step 070 of freeling.py: freeling.py CORPUS --ud")
