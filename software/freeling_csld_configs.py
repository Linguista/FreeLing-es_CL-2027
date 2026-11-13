#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.2.0
#
# freeling_csld_configs.py -- write the FreeLing configs the CSLD tags with,
# and the user map of the stand-in tokens.
#
# FreeLing es-CL 2027 has two dictionaries, installed by
# freeling_escl_deploy.py --target system (decided 261109):
#   /usr/local/share/freeling/es/es-cl/dicc.src             the default:
#       contemporary Chilean Spanish (vos always voseo; an -is form with a
#       voseo and a vosotros reading keeps the voseo one)
#   /usr/local/share/freeling/es/es-cl/historical/dicc.src  the 19th-century
#       dictionary, for historical corpora only: older Spanish (vos also
#       polite, the -is forms keep both readings) and the 19th-century
#       spellings (Bello, Sarmiento, the Chilean neographers), with its own
#       probabilities and multiwords (historical/probabilitats.dat,
#       historical/locucions.dat; decided 261112, 261113)
#
# From the base config <project root>/software/10-Infrastructure/freeling/
# csld-es-cl.cfg this writes:
#   coscach/csld-es-cl--coscach.cfg      COSCACH, transcribed speech
#       the default dictionary, the user map, and the Chilean name
#       recognizer for speech, es-cl/np-speech.dat: every Chilean
#       locality, country and continent is a place, at the start of a line
#       too, since a line is an utterance (decided 261110d)
#   coscach/usermap--coscach.dat         its user map
#   codicach/csld-es-cl--codicach.cfg    CODICACH, written texts
#       the default dictionary, the user map, and the Chilean name
#       recognizer for written texts, es-cl/np.dat: the same, inside a
#       sentence only (decided 261110d)
#   codicach/usermap--codicach.dat       its user map
#   historical/csld-es-cl--historical.cfg CORHICACH
#       the 19th-century dictionary, probabilities and multiwords;
#       compound analysis off (FreeLing builds its compound analyzer from
#       every form of the dictionary with foma, whose stack holds 2,097,152
#       entries: fewer than the 19th-century dictionary has, and FreeLing
#       stops with "Stack full!"); the base config's name recognizer
# Both name recognizers are the rule-based one (decided 261030), with a
# spelled-out letter never a name (decided 261101); their name classes are
# read only by FreeLing with the name-class change (FreeLing es-CL 2027,
# software/patches/). In all three: the Chilean tagset and the Chilean
# currencies (es-cl/quantities.dat). Every other line is the base config's.
#
# The config COSCACH and CODICACH shared until 261110,
#   coscach-codicach/csld-es-cl--coscach-codicach.cfg
#   coscach-codicach/usermap--coscach-codicach.dat
# are moved to coscach-codicach/deprecated/ as
# <name>.DEPRECATED-YYMMDD<extension>.
#
# It replaces freeling_build_voseo_dictionary.py, which built a separate
# copy of the dictionary for COSCACH and CODICACH: that copy is now the
# installed default. The old copy,
#   coscach-codicach/dicc.src
# is compressed into coscach-codicach/deprecated/dicc.DEPRECATED-YYMMDD.src.xz
# and made unreadable (mode 000), so nothing can read it by mistake.
#
# THE USER MAP. freeling_tag_corpus.py sends the stand-in tokens to FreeLing
# lowercased (FreeLing's name recogniser would join a capitalised token with
# its neighbours). The user map tags them before any other module runs
# (tags decided by the user, 261030):
#     ^xxxredactedxxx$ xxxredactedxxx Fz                  a redacted identifier
#     ^xxxunintelligiblexxx$ xxxunintelligiblexxx Fla     speech not made out
#     ^xxxnonspeechxxx$ xxxnonspeechxxx Flt               a non-speech event
#
# CHECKS (nothing is written if one fails):
#   * the base config has exactly one line for each key it sets
#   * the installed files the configs name exist, the default dictionary
#     has vos with the voseo reading only, and the historical one has both
#   * np.dat says <ClassesAtSentenceStart> no and np-speech.dat says yes
#   * the new configs are pure ASCII (FreeLing segfaults on anything else)
#   * no output is immutable (chattr +i) or otherwise unwritable, checked
#     before anything is written
#
# Executes by default. --dry-run reports and writes nothing. Linux.
# Standard library only.

from __future__ import annotations

import argparse
import hashlib
import lzma
import os
import sys
import time
from pathlib import Path

VERSION = "1.2.0"

FL_REL = Path("software/10-Infrastructure/freeling")
BASE_CFG = "csld-es-cl.cfg"
SYSTEM = Path("/usr/local/share/freeling/es/es-cl")
USERMAP_TEXT = ("^xxxredactedxxx$ xxxredactedxxx Fz\n"
                "^xxxunintelligiblexxx$ xxxunintelligiblexxx Fla\n"
                "^xxxnonspeechxxx$ xxxnonspeechxxx Flt\n")
# (folder, corpus, name recognizer file, its <ClassesAtSentenceStart>)
CONTEMPORARY = [("coscach", "COSCACH", "np-speech.dat", "yes"),
                ("codicach", "CODICACH", "np.dat", "no")]
OLD_COPY = "coscach-codicach/dicc.src"
# Retired 261110: the config COSCACH and CODICACH shared.
OLD_CONFIGS = ["coscach-codicach/csld-es-cl--coscach-codicach.cfg",
               "coscach-codicach/usermap--coscach-codicach.dat"]

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass


def log(*a):
    print(*a, flush=True)


def find_project_root(start: Path) -> Path | None:
    for d in [start, *start.parents]:
        if (d / "PROJECT_ROOT.txt").is_file():
            return d
    return None


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def vos_tags(dicc: Path):
    """The tags of vos in a dictionary file (read line by line)."""
    with dicc.open("rb") as fh:
        for line in fh:
            if line.startswith(b"vos "):
                t = line.decode("utf-8").split()
                return {t[i + 1] for i in range(1, len(t) - 1, 2)
                        if t[i] == "vos"}
    return set()


def make_config(base_lines, settings, extra, problems, name, drop=()):
    """The base config with each KEY=value of settings replacing the base's
    one line for that key (refused unless there is exactly one), every line
    of a key in drop commented out, and the extra lines added at the
    end."""
    lines = list(base_lines)
    for key in drop:
        lines = [("#" + l) if l.strip().startswith(key + "=") else l
                 for l in lines]
    for key, value in settings:
        hits = [i for i, l in enumerate(lines)
                if l.strip().startswith(key + "=")]
        if len(hits) != 1:
            problems.append("%s: the base config has %d %s lines, not 1"
                            % (name, len(hits), key))
            continue
        lines[hits[0]] = "%s=%s" % (key, value)
    keys = {e.split("=", 1)[0] for e in extra if "=" in e}
    lines = [l for l in lines if l.strip().split("=", 1)[0] not in keys]
    text = "\n".join(lines + extra) + "\n"
    bad = [i + 1 for i, l in enumerate(text.splitlines())
           if any(ord(c) > 126 for c in l)]
    if bad:
        problems.append("%s is not ASCII at line(s) %s"
                        % (name, ", ".join(map(str, bad[:10]))))
    return text


def at_start(np_file: Path) -> str | None:
    """The value of <ClassesAtSentenceStart> in a name recognizer file."""
    lines = [l.strip() for l in np_file.read_text(
        encoding="utf-8", errors="replace").splitlines()]
    if "<ClassesAtSentenceStart>" not in lines:
        return None
    i = lines.index("<ClassesAtSentenceStart>")
    for l in lines[i + 1:]:
        if l == "</ClassesAtSentenceStart>":
            return None
        if l and not l.startswith("##"):
            return l.lower()
    return None


def retire_name(path: Path, stamp: str) -> Path:
    """<folder>/deprecated/<stem>.DEPRECATED-YYMMDD[letter]<suffix>."""
    d = path.parent / "deprecated"
    for letter in [""] + list("bcdefghijklmnopqrstuvwxyz"):
        p = d / ("%s.DEPRECATED-%s%s%s" % (path.stem, stamp, letter,
                                           path.suffix))
        if not p.exists():
            return p
    raise SystemExit("REFUSED: too many deprecated copies of %s" % path)


def deprecated_name(path: Path, stamp: str) -> Path:
    d = path.parent / "deprecated"
    for letter in [""] + list("bcdefghijklmnopqrstuvwxyz"):
        p = d / ("%s.DEPRECATED-%s%s%s.xz" % (path.stem, stamp, letter,
                                               path.suffix))
        if not p.exists():
            return p
    raise SystemExit("REFUSED: too many deprecated copies of %s" % path)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_csld_configs.py",
        description="Write the CSLD FreeLing configs and the user map. "
                    "EXECUTES BY DEFAULT.")
    ap.add_argument("--root", default=None,
                    help="project root (default: found from this script's "
                         "own location by PROJECT_ROOT.txt)")
    ap.add_argument("--system", default=str(SYSTEM),
                    help="the installed es-cl folder (default: %(default)s)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report, write nothing")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else find_project_root(
        Path(__file__).resolve().parent)
    if root is None:
        log("REFUSED: no PROJECT_ROOT.txt above this script; give --root")
        return 2
    fl = root / FL_REL
    sysd = Path(a.system).resolve()
    base_cfg = fl / BASE_CFG
    hi_cfg = fl / "historical" / "csld-es-cl--historical.cfg"
    cont = [(fl / d / ("csld-es-cl--%s.cfg" % d),
             fl / d / ("usermap--%s.dat" % d), corpus, npf, start)
            for d, corpus, npf, start in CONTEMPORARY]
    old_copy = fl / OLD_COPY
    old_configs = [fl / p for p in OLD_CONFIGS if (fl / p).exists()]
    stamp = time.strftime("%y%m%d")

    log("=" * 78)
    log("FREELING CSLD CONFIGS  %s%s" % (VERSION, "   (DRY RUN)"
                                         if a.dry_run else ""))
    log("=" * 78)
    log("base config        : %s" % base_cfg)
    log("installed es-cl    : %s" % sysd)
    for cfg, umap, corpus, npf, _ in cont:
        log("%-19s: %s" % (corpus, cfg))
        log("%-19s  %s" % ("", umap))
    log("CORHICACH          : %s" % hi_cfg)
    problems = []
    needed = [base_cfg, sysd / "dicc.src", sysd / "historical" / "dicc.src",
              sysd / "historical" / "probabilitats.dat",
              sysd / "historical" / "locucions.dat",
              sysd / "tagset.dat", sysd / "quantities.dat",
              sysd / "probabilitats.dat", sysd / "locucions.dat"] + \
        [sysd / npf for _, _, _, npf, _ in cont]
    for p in needed:
        if not p.is_file():
            problems.append("not found: %s%s" % (p, "" if p == base_cfg else
                                                 " (deploy FreeLing es-CL "
                                                 "2027 with "
                                                 "freeling_escl_deploy.py "
                                                 "--target system first)"))
    if problems:
        for p in problems:
            log("REFUSED: %s" % p)
        return 2
    v_c = vos_tags(sysd / "dicc.src")
    v_h = vos_tags(sysd / "historical" / "dicc.src")
    if v_c != {"PP2CS0V"}:
        problems.append("the installed default dictionary has vos %s, not "
                        "the voseo reading only: it is not FreeLing es-CL "
                        "2027's default" % " ".join(sorted(v_c)))
    if v_h != {"PP2CS0P", "PP2CS0V"}:
        problems.append("the installed historical dictionary has vos %s, not "
                        "both readings" % " ".join(sorted(v_h)))
    for _, _, corpus, npf, start in cont:
        got = at_start(sysd / npf)
        if got != start:
            problems.append("%s says <ClassesAtSentenceStart> %s, not %s: it "
                            "is not FreeLing es-CL 2027's name recognizer for "
                            "%s" % (sysd / npf, got or "nothing", start,
                                    corpus))

    base = base_cfg.read_text(encoding="utf-8").splitlines()
    common = [("TagsetFile", sysd / "tagset.dat"),
              ("ProbabilityFile", sysd / "probabilitats.dat"),
              ("LocutionsFile", sysd / "locucions.dat"),
              ("QuantitiesFile", sysd / "quantities.dat")]
    outputs = []
    for cfg, umap, corpus, npf, _ in cont:
        text = make_config(
            base, common + [("DictionaryFile", sysd / "dicc.src"),
                            ("NPDataFile", sysd / npf)],
            ["# Stand-in tokens, see freeling_tag_corpus.py", "UserMap=yes",
             "UserMapFile=%s" % umap], problems, cfg.name)
        outputs += [(cfg, text.encode()), (umap, USERMAP_TEXT.encode())]
    hist_common = [(k, sysd / "historical" / v.name)
                   if k in ("ProbabilityFile", "LocutionsFile") else (k, v)
                   for k, v in common]
    hi_text = make_config(
        base, hist_common + [("DictionaryFile",
                              sysd / "historical" / "dicc.src"),
                             ("CompoundAnalysis", "no")],
        [], problems, hi_cfg.name, drop=("CompoundFile",))
    outputs.append((hi_cfg, hi_text.encode()))
    if problems:
        for p in problems:
            log("REFUSED: %s" % p)
        log("Nothing was written.")
        return 2

    # A protected output is refused before anything is written.
    locked = []
    for path, _ in outputs + ([(old_copy, b"")] if old_copy.exists() else
                              []) + [(p, b"") for p in old_configs]:
        if path.exists():
            try:
                with path.open("ab"):
                    pass
            except OSError as exc:
                locked.append("%s (%s)" % (path, exc.strerror))
    if locked:
        for l in locked:
            log("PROTECTED: %s" % l)
        log("REFUSED: these files cannot be replaced. Clear the flag first:")
        log("   sudo chattr -i %s" % " ".join(l.split(" (")[0]
                                              for l in locked))
        log("Nothing was written.")
        return 2

    log("")
    for path, data in outputs:
        same = path.is_file() and path.read_bytes() == data
        log("%s %s" % ("unchanged" if same else "write    ", path))
    dep = deprecated_name(old_copy, stamp) if old_copy.exists() else None
    if dep:
        log("retire    %s" % old_copy)
        log("       -> %s (compressed, mode 000)" % dep)
    old_moves = [(p, retire_name(p, stamp)) for p in old_configs]
    for p, d in old_moves:
        log("retire    %s" % p)
        log("       -> %s" % d)
    if a.dry_run:
        log("")
        log("DRY RUN -- nothing written.")
        return 0
    for path, data in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and path.read_bytes() == data:
            continue
        if path.exists():
            old = path.parent / "deprecated" / ("%s.DEPRECATED-%s%s" % (
                path.stem, stamp, path.suffix))
            n = 0
            while old.exists():
                n += 1
                old = old.with_name("%s.DEPRECATED-%s%s%s" % (
                    path.stem, stamp, "bcdefghijklmnopqrstuvwxyz"[n - 1],
                    path.suffix))
            old.parent.mkdir(parents=True, exist_ok=True)
            os.replace(path, old)
        tmp = path.with_name(path.name + ".part")
        tmp.write_bytes(data)
        os.replace(tmp, path)
    if dep:
        dep.parent.mkdir(parents=True, exist_ok=True)
        tmp = dep.with_name(dep.name + ".part")
        with old_copy.open("rb") as src, lzma.open(tmp, "wb",
                                                     preset=9) as dst:
            for chunk in iter(lambda: src.read(1 << 20), b""):
                dst.write(chunk)
        os.replace(tmp, dep)
        os.chmod(dep, 0o000)
        old_copy.unlink()
    for p, d in old_moves:
        d.parent.mkdir(parents=True, exist_ok=True)
        os.replace(p, d)
    log("")
    for path, data in outputs:
        log("%s  %s" % (sha(data), path.name))
    log("=" * 78)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.stderr.write("\ninterrupted\n")
        sys.exit(130)
