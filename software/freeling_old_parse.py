#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.0.0
#
# freeling_old_parse.py -- parses Old Spanish (medieval and Golden Age)
# texts through a temporary modernization. FreeLing Old (es-old.cfg) tags
# each text; every word it knows gets its modern form, from its lemma and
# tag and the modern Spanish dictionary (dixo, decir VMIS3S0: dijo; muger:
# mujer; fermosa: hermosa); the modernized text is parsed by FreeLing's
# modern parser (es-cl.cfg, the LSTM parser), which reads it far better
# than the rule-based parser reads the old forms; and the parse is written
# back onto the original words, token for token. The modernization is
# thrown away, or kept beside the result as a sidecar (--sidecar).
#
#     freeling_old_parse.py poema.txt
#     freeling_old_parse.py --tags modern --sidecar a.txt b.txt --out-dir parsed
#     echo "Et dixo el rey que la muger era fermosa." | freeling_old_parse.py
#
# --tags old (the default) keeps FreeLing Old's lemmas and tags: the parser
# sees the modern forms with FreeLing Old's tags. --tags modern lets the
# modern tagger tag the modernized text too, and those lemmas and tags go
# into the result (era, which FreeLing Old may tag as 1st person, comes out
# 3rd where the sentence needs it); FreeLing Old's own stay in the sidecar.
#
# Linux and macOS, and Windows with the zip's analyze.bat on the PATH.
# Python 3.9 or later, standard library only.

from __future__ import annotations

import argparse
import difflib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import freeling_common as fc                                # noqa: E402

VERSION = "1.0.0"
__version__ = VERSION

OLD_CFG = "es-old.cfg"
MODERN_CFG = "es-cl.cfg"
COLUMNS_CFG = fc.COLUMNS_CFG          # the release's 12 CoNLL columns
# Dictionaries the modern forms are taken from, in order: FreeLing's own
# Spanish dictionary (standard spellings only), then the Chilean one.
DICTIONARIES = (("es", "es/dicc.src"), ("es-cl", "es/es-cl/dicc.src"))
# Tags whose words keep their form: punctuation, numbers, dates, names.
KEEP_TAG_PREFIXES = ("F", "Z", "W", "NP")
# Modules switched off in the modern pass, so that it keeps the tokens it
# is given: multiwords, retokenizing, numbers, dates, quantities, names.
MODERN_KEEP_TOKENS = ["--noloc", "--nortk", "--nortkcon", "--nonumb",
                      "--nodate", "--noquant", "--noner", "--nonec",
                      "--sense", "none"]
OUT_COLUMNS = ["ID", "SPAN_BEGIN", "SPAN_END", "FORM", "LEMMA", "TAG",
               "SENSE", "ALL_SENSES", "DEPHEAD", "DEPREL", "LEX_PROB",
               "TAG_PROB"]
SIDECAR_COLUMNS = ["ID", "PART", "FORM", "MODERN_FORM", "OLD_LEMMA",
                   "OLD_TAG", "MODERN_LEMMA", "MODERN_TAG", "SOURCE"]


def run(cmd, data: bytes, timeout):
    """(stdout, problem)."""
    try:
        r = subprocess.run(cmd, input=data, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timeout after %ds" % timeout
    except OSError as exc:
        return None, "cannot run %s: %s" % (cmd[0], exc)
    if r.returncode != 0:
        err = " ".join((r.stderr or b"").decode("utf-8", "replace").split())
        return None, "%s exit %d: %s" % (Path(cmd[0]).name, r.returncode,
                                        err[-300:])
    return r.stdout, None


def sentences(text: str, ncols: int):
    """The token rows of FreeLing's CoNLL output, sentence by sentence.
    FreeLing pads its columns with spaces and never puts one in a field."""
    out, cur = [], []
    for line in text.split("\n"):
        f = line.split()
        if not f:
            if cur:
                out.append(cur)
                cur = []
            continue
        if len(f) != ncols:
            raise ValueError("a line of %d fields where %d were asked for: %s"
                             % (len(f), ncols, line[:120]))
        cur.append(f)
    if cur:
        out.append(cur)
    return out


def keep_form(tag: str) -> bool:
    return tag.startswith(KEEP_TAG_PREFIXES)


def load_forms(fl, wanted):
    """(lemma, tag) -> [(form, source)] for every pair wanted, from the
    modern dictionaries, in their order."""
    forms = {}
    for source, rel in DICTIONARIES:
        path = fl.share / rel
        if not path.is_file():
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                f = line.split()
                if len(f) < 3 or len(f) % 2 == 0:
                    continue
                form = f[0]
                for i in range(1, len(f) - 1, 2):
                    key = (f[i], f[i + 1])
                    if key in wanted:
                        forms.setdefault(key, []).append((form, source))
    return forms


def choose(old: str, cands):
    """(form, source): the old form itself if it is a candidate, else the
    candidate closest to it in spelling (fuesse: fuese, not fuera), from
    the first dictionary that has any."""
    first = cands[0][1]
    pool = [c for c in cands if c[1] == first]
    low = old.lower()
    for c in pool:
        if c[0] == low:
            return c
    return max(pool, key=lambda c: (difflib.SequenceMatcher(None, low, c[0]).ratio(),
                                    -len(c[0]), c[0]))


def recase(old: str, new: str) -> str:
    if len(old) > 1 and old.isupper():
        return new.upper()
    if old[:1].isupper():
        return new[:1].upper() + new[1:]
    return new


def modernize(sents, forms):
    """For each sentence, its parts: one per word, or one per piece of a
    word FreeLing Old left joined (dixole: decir+le, VMIS3S0+PP3CSD0)."""
    out = []
    for sent in sents:
        parts = []
        for r in sent:
            form, lemmas, tags = r[3], r[4].split("+"), r[5].split("+")
            if len(lemmas) != len(tags):
                lemmas, tags = [r[4]], [r[5]]
            for k, (lem, tag) in enumerate(zip(lemmas, tags)):
                if keep_form(tag):
                    modern, src = (form if len(tags) == 1 else lem), "kept"
                else:
                    cands = forms.get((lem, tag))
                    if cands:
                        modern, src = choose(form if len(tags) == 1 else lem, cands)
                        modern = recase(form, modern) if k == 0 else modern
                    else:
                        modern, src = (form if len(tags) == 1 else lem), "kept"
                parts.append({"id": r[0], "part": k + 1, "form": form,
                              "modern": modern, "lemma": lem, "tag": tag,
                              "source": src if len(tags) == 1 else src + "+split"})
        out.append(parts)
    return out


def write_tmp(lines) -> str:
    fd, p = tempfile.mkstemp(suffix=".cfg")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write("<Columns>\n%s\n</Columns>\n" % " ".join(lines))
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_old_parse.py",
        description="Parse Old Spanish texts through a temporary "
                    "modernization: FreeLing Old tags them, the words get "
                    "their modern forms, FreeLing's modern parser parses "
                    "them, and the parse is written onto the original words.")
    ap.add_argument("texts", nargs="*", help="text files (UTF-8); none: "
                    "standard input")
    ap.add_argument("--tags", choices=("old", "modern"), default="old",
                    help="the lemmas and tags of the result: FreeLing Old's "
                    "(old, the default) or the modern tagger's, on the "
                    "modernized text (modern)")
    ap.add_argument("--sidecar", action="store_true", help="keep the "
                    "modernization: NAME.modern.tsv beside each result")
    ap.add_argument("--flush", action="store_true", help="every line end "
                    "ends a sentence (verse, one line per sentence)")
    ap.add_argument("--out", help="write here (one text only); default: "
                    "standard output")
    ap.add_argument("--out-dir", help="write NAME.conll for each NAME.txt")
    ap.add_argument("--timeout", type=int, default=3600, help="per FreeLing "
                    "run, in seconds (default 3600)")
    ap.add_argument("--freeling-bin", help="the folder of FreeLing's analyze")
    ap.add_argument("--share", help="FreeLing's data folder")
    ap.add_argument("--lib", help="the FreeLing library")
    ap.add_argument("--dry-run", action="store_true", help="check FreeLing, "
                    "the configs and the texts, and say what would be "
                    "written; write nothing")
    ap.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    fc.set_colour(sys.stderr.isatty())

    fl = fc.FreeLing(a.freeling_bin, a.share, a.lib)
    problems = fl.problems()
    for cfg in (OLD_CFG, MODERN_CFG, COLUMNS_CFG):
        if not fl.config(cfg).is_file():
            problems.append("not found: %s" % fl.config(cfg))
    if not (fl.share / DICTIONARIES[0][1]).is_file():
        problems.append("not found: %s" % (fl.share / DICTIONARIES[0][1]))
    texts = [Path(t) for t in a.texts]
    for t in texts:
        if not t.is_file():
            problems.append("not a file: %s" % t)
    if a.out and len(texts) > 1:
        problems.append("--out takes one text; give --out-dir for several")
    if a.sidecar and not (a.out or a.out_dir):
        problems.append("--sidecar needs --out or --out-dir")
    if problems:
        for p in problems:
            fc.log(fc.red("REFUSED: " + p))
        return 2

    def target(t):
        if a.out_dir:
            return Path(a.out_dir) / (t.stem + ".conll")
        return Path(a.out) if a.out else None

    if a.dry_run:
        fc.log("FreeLing: %s" % fl.analyze)
        for t in texts or [Path("-")]:
            dst = target(t) if texts else (Path(a.out) if a.out else None)
            fc.log("would write: %s" % (dst or "standard output"))
            if a.sidecar and dst:
                fc.log("would write: %s" % dst.with_suffix(".modern.tsv"))
        fc.log("dry run: nothing written")
        return 0

    inputs = [(t, t.read_bytes()) for t in texts] if texts else \
        [(None, sys.stdin.buffer.read())]

    # 1. FreeLing Old tags each text (the 12 columns: spans, probabilities).
    ncols = len(fc.conll_columns(fl.config(COLUMNS_CFG))[0])
    tagged = []
    for t, data in inputs:
        cmd = [fl.analyze, "-f", str(fl.config(OLD_CFG)), "--outlv", "tagged",
               "--output", "conll", "--oconll", str(fl.config(COLUMNS_CFG)),
               "--nonec", "--sense", "none"] + (["--flush"] if a.flush else [])
        out, p = run(cmd, data, a.timeout)
        if p:
            fc.log(fc.red("FAILED: FreeLing Old on %s: %s" % (t or "standard input", p)))
            return 1
        tagged.append(sentences(out.decode("utf-8"), ncols))
        fc.log("tagged : %d sentences, FreeLing Old: %s" % (len(tagged[-1]), t or "standard input"))

    # 2. The modern form of every word FreeLing Old knows.
    wanted = set()
    for sents in tagged:
        for s in sents:
            for r in s:
                ls, ts = r[4].split("+"), r[5].split("+")
                if len(ls) == len(ts):
                    wanted.update(zip(ls, ts))
    forms = load_forms(fl, wanted)
    modern = [modernize(sents, forms) for sents in tagged]

    # 3. With --tags modern, the modern tagger tags the modernized text; a
    # word that kept its old form (no modern form was found: et, ca) keeps
    # FreeLing Old's lemma and tag, which the modern tagger cannot know.
    allparts = [s for doc in modern for s in doc]
    if a.tags == "modern":
        lines = "\n\n".join("\n".join(p["modern"] for p in s) for s in allparts) + "\n\n"
        colfile = write_tmp(["ID", "FORM", "LEMMA", "TAG", "LEX_PROB", "TAG_PROB"])
        try:
            cmd = [fl.analyze, "-f", str(fl.config(MODERN_CFG)), "--input", "freeling",
                   "--inplv", "splitted", "--outlv", "tagged", "--output", "conll",
                   "--oconll", colfile] + MODERN_KEEP_TOKENS
            out, p = run(cmd, lines.encode("utf-8"), a.timeout)
        finally:
            fc.unlink_quietly(Path(colfile))
        if p:
            fc.log(fc.red("FAILED: the modern tagger: %s" % p))
            return 1
        retag = sentences(out.decode("utf-8"), 6)
        if len(retag) != len(allparts):
            fc.log(fc.red("FAILED: %d sentences sent to the modern tagger, %d came back"
                          % (len(allparts), len(retag))))
            return 1
        kept = 0
        for parts, rows in zip(allparts, retag):
            if len(rows) != len(parts):
                continue           # the old tags stay for the whole sentence
            for pt, r in zip(parts, rows):
                pt["old_lemma"], pt["old_tag"] = pt["lemma"], pt["tag"]
                if pt["source"].startswith("kept") and not keep_form(pt["tag"]):
                    kept += 1
                    continue
                pt["lemma"], pt["tag"], pt["lexp"], pt["tagp"] = r[2], r[3], r[4], r[5]
        fc.log("tagged : the modernized text, the modern tagger (%d words with no "
               "modern form keep FreeLing Old's tag)" % kept)

    # 4. The modern parser, on every sentence of every text at once.
    lines = "\n\n".join("\n".join("%s %s %s 1" % (p["modern"], p["lemma"], p["tag"])
                                  for p in s) for s in allparts) + "\n\n"
    cols = ["ID", "FORM", "LEMMA", "TAG", "DEPHEAD", "DEPREL"]
    colfile = write_tmp(cols)
    try:
        cmd = [fl.analyze, "-f", str(fl.config(MODERN_CFG)), "--input", "freeling",
               "--inplv", "tagged", "--outlv", "dep", "--output", "conll",
               "--oconll", colfile, "--nonec", "--sense", "none"]
        out, p = run(cmd, lines.encode("utf-8"), a.timeout)
    finally:
        fc.unlink_quietly(Path(colfile))
    if p:
        fc.log(fc.red("FAILED: the modern parser: %s" % p))
        return 1
    parsed = sentences(out.decode("utf-8"), len(cols))
    if len(parsed) != len(allparts):
        fc.log(fc.red("FAILED: %d sentences sent to the parser, %d came back"
                      % (len(allparts), len(parsed))))
        return 1
    fc.log("parsed : %d sentences, the modern parser (%s tags)" % (len(parsed), a.tags))

    # 5. The parse onto the original words.
    k = 0
    mismatched = 0
    for (t, _data), sents, mdoc in zip(inputs, tagged, modern):
        rows_out, side = [], []
        for sent, parts in zip(sents, mdoc):
            prow = parsed[k]
            k += 1
            if len(prow) != len(parts):
                mismatched += 1
                prow = None
            # the part index (1-based) -> the original token's ID
            host = {i + 1: parts[i]["id"] for i in range(len(parts))}
            first = {}
            for i, pt in enumerate(parts):
                first.setdefault(pt["id"], i)
            byid = {r[0]: r for r in sent}
            for r in sent:
                i = first[r[0]]
                head, rel, lemma, tag = "-", "-", r[4], r[5]
                lexp, tagp = r[10], r[11]
                if prow:
                    h = prow[i][4]
                    head = "0" if h == "0" else host.get(int(h), "-") if h.isdigit() else "-"
                    if head == r[0]:
                        head = "-"
                    rel = prow[i][5]
                    if a.tags == "modern":
                        ids = [j for j, pt in enumerate(parts) if pt["id"] == r[0]]
                        lemma = "+".join(parts[j]["lemma"] for j in ids)
                        tag = "+".join(parts[j]["tag"] for j in ids)
                        lexp = parts[i].get("lexp", lexp)
                        tagp = parts[i].get("tagp", tagp)
                rows_out.append([r[0], r[1], r[2], r[3], lemma, tag, "-", "-",
                                 head, rel, lexp, tagp])
            for pt in parts:
                if a.tags == "modern" and "old_lemma" in pt:
                    ol, ot, ml, mt = pt["old_lemma"], pt["old_tag"], pt["lemma"], pt["tag"]
                else:
                    ol, ot, ml, mt = pt["lemma"], pt["tag"], "-", "-"
                side.append([pt["id"], str(pt["part"]), pt["form"], pt["modern"],
                             ol, ot, ml, mt, pt["source"]])
            rows_out.append(None)
            side.append(None)
        text = "".join("\t".join(r) + "\n" if r else "\n" for r in rows_out)
        dst = target(t) if t else (Path(a.out) if a.out else None)
        if dst:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text, encoding="utf-8")
            fc.log("written: %s" % dst)
            if a.sidecar:
                sc = dst.with_suffix(".modern.tsv")
                sc.write_text("\t".join(SIDECAR_COLUMNS) + "\n" +
                              "".join("\t".join(r) + "\n" for r in side if r),
                              encoding="utf-8")
                fc.log("written: %s" % sc)
        else:
            sys.stdout.write(text)
    if mismatched:
        fc.log(fc.orange("%d sentences came back from the parser with another "
                         "number of tokens: written without a parse (DEPHEAD and "
                         "DEPREL -)" % mismatched))
    return 0


if __name__ == "__main__":
    sys.exit(main())
