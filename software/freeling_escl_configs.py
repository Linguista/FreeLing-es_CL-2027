#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 2.1.0
#
# freeling_escl_configs.py -- the FreeLing configs of FreeLing es-CL 2027,
# one per kind of text, with their user maps and their CoNLL columns file.
# freeling_escl_build.py calls it to write them into the release. Run on its
# own, it reads a release folder (--release) and writes the same files into
# another folder (--out), to inspect them or to test a change before a
# rebuild; the release itself is only ever written by the build, whose
# SHA256SUMS the deploy checks.
#
# A FreeLing config is the one file FreeLing's analyzer reads to know which
# modules to run and which data file each one reads. The kinds of text
# differ in five things only, so every config is FreeLing 4.2's own es-cl
# config with the same changes, and then the five that set the kinds apart:
#
#   config                      kind of text            dictionary       name recognizer  user map adds
#   es-cl.cfg (the default)     modern writing          es-cl            np.dat           -
#   es-cl-informal.cfg          informal modern writing es-cl/informal   np.dat           the chat readings
#   es-cl-speech.cfg            transcribed speech      es-cl            np-speech.dat    nn as a hesitation
#   es-cl-19th-century.cfg      19th-century writing    es-cl/19th-century (with its own  FreeLing's own   -
#                                                       probabilities and multiwords)
#
# Old Spanish (medieval and Golden Age texts) is FreeLing Old, es-old.cfg, as
# FreeLing ships it (its compound analysis is already off); it is not
# written here.
#
# THE CHANGES MADE TO FREELING'S es-cl CONFIG IN EVERY CONFIG
#   TagsetFile, QuantitiesFile    the Chilean tagset (voseo V) and currencies
#   CompoundAnalysis=no           FreeLing's compound module splits a word
#                                 missing from the dictionary into two that
#                                 are in it; on real corpora nearly all it
#                                 built was wrong (pentecostal as pente +
#                                 costal, veinti as ver + inti, down as do +
#                                 huevón). The CompoundFile line is
#                                 commented out.
#   AlwaysFlush=yes               every line end ends a sentence: give the
#                                 text one sentence or utterance per line
#   OutputLevel=dep, OutputFormat=conll, OutputConllConfig
#                                 dependency parses, as CoNLL with the
#                                 columns of es-cl-conll-columns.cfg (FreeLing
#                                 4.2's analyzer ignores OutputLevel; pass
#                                 --outlv dep)
#   NEClassification=yes          names classed as person, place,
#                                 organisation or other
#   SenseAnnotation=ukb           word senses ranked by UKB over the Spanish
#                                 WordNet
#   TaggerForceSelect=retok       the tagger may retokenize
#   DependencyParser=lstm, DepLSTMFile
#                                 FreeLing's LSTM parser (chosen by
#                                 agreement between parsers: head agreement
#                                 with treeler 87.4%, against 71.7% for
#                                 txala)
#   UserMap=yes, UserMapFile      the kind's user map (below)
#
# THE USER MAPS (es/es-cl/usermap/<config name>.dat). FreeLing's user map
# fixes a word's readings before any other module runs. Every map holds:
#   - the stand-in tokens of es/es-cl/stand-ins.tsv, lowercased (the tagger
#     sends them lowercased), each tagged as that file says;
#   - novela, vela and velo, always common nouns (FreeLing read velo as
#     ver + lo and novela as novar + la).
# The speech map adds nn and nnn as the hesitation (an interjection); the
# informal map adds every line of es/es-cl/usermap-informal.dat (the chat
# readings: q as que, x as por, tas as estás ...).
#
# Python 3.9 or later, standard library only. Linux, macOS and Windows.

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

VERSION = "2.1.0"

COLUMNS_NAME = "es-cl-conll-columns.cfg"
COLUMNS_TEXT = ("<Columns>\n"
                "ID SPAN_BEGIN SPAN_END FORM LEMMA TAG SENSE ALL_SENSES "
                "DEPHEAD DEPREL LEX_PROB TAG_PROB\n"
                "</Columns>\n")
STANDINS_NAME = "stand-ins.tsv"
INFORMAL_READINGS = "usermap-informal.dat"
STANDIN_FORM = re.compile(r"^XXX[A-Z]+XXX$")

# name: (kind, dictionary folder, probabilities/multiwords folder,
#        name recognizer data file, extra user-map lines key)
CONFIGS = {
    "es-cl.cfg": ("modern writing", "es/es-cl", "es/es-cl",
                  "es/es-cl/np.dat", None),
    "es-cl-informal.cfg": ("informal modern writing", "es/es-cl/informal",
                           "es/es-cl", "es/es-cl/np.dat", "informal"),
    "es-cl-speech.cfg": ("transcribed speech", "es/es-cl", "es/es-cl",
                         "es/es-cl/np-speech.dat", "speech"),
    "es-cl-19th-century.cfg": ("19th-century writing", "es/es-cl/19th-century",
                               "es/es-cl/19th-century",
                               "es/nerc/nerc/nerc.dat", None),
}

LOCKS_ALL = ("^(novela|NOVELA)$ novela NCFS000\n"
             "^(vela|VELA)$ vela NCFS000\n"
             "^(velo|VELO)$ velo NCMS000\n")
LOCKS_SPEECH = ("^(nn|NN)$ nn I\n"
                "^(nnn|NNN)$ nn I\n")

SHARE = "$FREELINGSHARE"


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def read_stand_ins(text: str, problems):
    """[(form, tag, meaning)] from stand-ins.tsv."""
    rows, header = [], False
    seen = set()
    for n, raw in enumerate(nfc(text).split("\n"), 1):
        line = raw.rstrip("\r")
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if not header:
            if f != ["form", "tag", "meaning"]:
                problems.append("%s line %d: the header must be "
                                "form<TAB>tag<TAB>meaning" % (STANDINS_NAME, n))
                return []
            header = True
            continue
        if len(f) != 3 or not all(x.strip() for x in f):
            problems.append("%s line %d: not form<TAB>tag<TAB>meaning"
                            % (STANDINS_NAME, n))
            continue
        form, tag, meaning = f
        if not STANDIN_FORM.match(form):
            problems.append("%s line %d: %s is not XXX + capital letters + XXX"
                            % (STANDINS_NAME, n, form))
            continue
        if form in seen:
            problems.append("%s line %d: %s twice" % (STANDINS_NAME, n, form))
            continue
        seen.add(form)
        rows.append((form, tag, meaning))
    if not rows and not problems:
        problems.append("%s: no stand-in listed" % STANDINS_NAME)
    return rows


def user_maps(stand_ins, informal_text: str):
    """{config name: user map text}."""
    base = "".join("^%s$ %s %s\n" % (f.lower(), f.lower(), t)
                   for f, t, _ in stand_ins) + LOCKS_ALL
    extra = {None: "", "speech": LOCKS_SPEECH,
             "informal": "".join(l + "\n" for l in nfc(informal_text).split("\n")
                                 if l.strip())}
    return {name: base + extra[spec[4]] for name, spec in CONFIGS.items()}


def set_key(lines, key, value, problems, name, required=False):
    """Set key=value on the uncommented line of key, or add it at the end."""
    hits = [i for i, x in enumerate(lines)
            if x.strip().startswith(key + "=")]
    if len(hits) > 1:
        problems.append("%s: %s is set more than once in FreeLing's config"
                        % (name, key))
        return
    if hits:
        lines[hits[0]] = "%s=%s" % (key, value)
    elif required:
        problems.append("%s: FreeLing's config has no %s line" % (name, key))
    else:
        lines.append("%s=%s" % (key, value))


def make_config(stock: str, name: str, problems) -> str:
    """One config, from FreeLing 4.2's es-cl config."""
    kind, dicc, probloc, npdata, _ = CONFIGS[name]
    lines = stock.rstrip("\n").split("\n")
    req = [("TagsetFile", SHARE + "/es/es-cl/tagset.dat"),
           ("QuantitiesFile", SHARE + "/es/es-cl/quantities.dat"),
           ("DictionaryFile", "%s/%s/dicc.src" % (SHARE, dicc)),
           ("ProbabilityFile", "%s/%s/probabilitats.dat" % (SHARE, probloc)),
           ("LocutionsFile", "%s/%s/locucions.dat" % (SHARE, probloc)),
           ("NPDataFile", "%s/%s" % (SHARE, npdata)),
           ("CompoundAnalysis", "no"),
           ("AlwaysFlush", "yes"),
           ("OutputLevel", "dep"),
           ("NEClassification", "yes"),
           ("SenseAnnotation", "ukb"),
           ("TaggerForceSelect", "retok"),
           ("DependencyParser", "lstm")]
    for k, v in req:
        set_key(lines, k, v, problems, name, required=True)
    comp = [i for i, x in enumerate(lines)
            if x.strip().startswith("CompoundFile=")]
    for i in comp:
        lines[i] = "#" + lines[i].strip()
    lines += ["",
              "#### FreeLing es-CL 2027: %s (written by freeling_escl_configs.py)"
              % kind]
    for k, v in (("DepLSTMFile", SHARE + "/es/dep_lstm/params-es.dat"),
                 ("OutputFormat", "conll"),
                 ("OutputConllConfig", "%s/config/%s" % (SHARE, COLUMNS_NAME)),
                 ("UserMap", "yes"),
                 ("UserMapFile", "%s/es/es-cl/usermap/%s.dat"
                  % (SHARE, name[:-len(".cfg")]))):
        set_key(lines, k, v, problems, name)
    text = "\n".join(lines) + "\n"
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        problems.append("%s: not pure ASCII (FreeLing stops on any other "
                        "character in a config)" % name)
    return text


def all_files(stock: str, stand_ins_text: str, informal_text: str, problems):
    """{path under the release's data/ folder: text}: the four configs, the
    columns file and the four user maps."""
    stand_ins = read_stand_ins(stand_ins_text, problems)
    out = {}
    for name in CONFIGS:
        out["config/" + name] = make_config(stock, name, problems)
    out["config/" + COLUMNS_NAME] = COLUMNS_TEXT
    for name, text in user_maps(stand_ins, informal_text).items():
        out["es/es-cl/usermap/%s.dat" % name[:-len(".cfg")]] = text
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_escl_configs.py",
        description="Write the FreeLing es-CL 2027 configs, user maps and "
                    "CoNLL columns file, from a release folder, into another "
                    "folder. EXECUTES BY DEFAULT.")
    ap.add_argument("--release", required=True,
                    help="the release folder whose data/ is read")
    ap.add_argument("--out", required=True,
                    help="the folder written (never the release itself)")
    ap.add_argument("--dry-run", action="store_true",
                    help="check everything and write nothing")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    rel = Path(a.release)
    data = rel / "data"
    out = Path(a.out)
    if out.resolve() == rel.resolve() or rel.resolve() in out.resolve().parents:
        print("REFUSED: --out must be outside the release (the build writes "
              "the release)")
        return 2
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    try:
        from freeling_escl_build import stock_es_cl_cfg
    except ImportError as exc:
        print("REFUSED: freeling_escl_build.py must sit beside this script "
              "(%s)" % exc)
        return 2
    print("=" * 78)
    print("FREELING ES-CL CONFIGS  %s%s" % (VERSION,
                                           "   (DRY RUN)" if a.dry_run else ""))
    print("=" * 78)
    print("release: %s" % rel)
    print("out    : %s" % out)
    need = [data / "es" / "es-cl" / STANDINS_NAME,
            data / "es" / "es-cl" / INFORMAL_READINGS]
    for p in need:
        if not p.is_file():
            print("REFUSED: not found: %s" % p)
            return 2
    problems = []
    files = all_files(stock_es_cl_cfg(),
                      need[0].read_text(encoding="utf-8"),
                      need[1].read_text(encoding="utf-8"), problems)
    if problems:
        for p in problems:
            print("PROBLEM: %s" % p)
        print("Nothing written.")
        return 1
    for rel_, text in files.items():
        print("  %s" % (out / rel_))
    if a.dry_run:
        print("DRY RUN -- nothing written.")
        return 0
    for rel_, text in files.items():
        p = out / rel_
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(p.name + ".part")
        tmp.write_text(text, encoding="utf-8", newline="\n")
        tmp.replace(p)
    print("%d file(s) written" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
