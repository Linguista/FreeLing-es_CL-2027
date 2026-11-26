#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 2.9.0
#
# freeling_escl_deploy.py -- put a FreeLing es-CL 2027 build (made by
# freeling_escl_build.py) where it is used.
#
#   --target user     run as your own user, NOT as root
#       the Chilean grammatical lists
#           <project root>/derived-software/FreeLing_es-CL_2027/data/grammatical-lists/freeling-cl/
#               CL.*.GRAM.txt, and with each list that has one its raw copy
#               source-files/CL.*.txt (the same lines, which other
#               tools read)
#       the FreeLing build tree (FreeLing's own build reads it)
#           <project root>/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/
#               data/es/es-cl/
#               dictionary/entries/CL.*   the Chilean entries
#               remove/CL.removed         the Spanish readings removed
#               probabilitats.dat, locucions.dat, tagset.dat
#       and retires, as replaced files are (below), the entries files the
#       build no longer writes there:
#           dictionary/entries/CL.misspellings  now CL.common-misspellings
#           dictionary/entries/CL.reduced-forms the informal dictionary's
#               own entries (decided 261116): FreeLing's build reads the
#               entries folder whole, and the default dictionary has no
#               reduced forms
#   --target system   run as the owner of the installed data: your own
#                     user for the FreeLing of the product folder, sudo
#                     for one in a system folder (--share)
#       the installed data FreeLing reads, in
#       <project root>/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling/
#           es/es-cl/
#               dicc.src              the default dictionary (contemporary)
#               informal/dicc.src     the informal dictionary: the default
#                                     one with the reduced forms (cansá,
#                                     pescao, he comío), for informal
#                                     writing only (decided 261116)
#               19th-century/dicc.src the 19th-century dictionary (19th-century
#                                     texts only), with its own
#               19th-century/probabilitats.dat, 19th-century/locucions.dat
#               np.dat                the name recognizer, written texts
#               np-speech.dat         the name recognizer, transcribed speech
#               probabilitats.dat, locucions.dat, tagset.dat, quantities.dat
#               usermap-informal.dat  the readings for informal writing only
#                                     (the source of the informal user map)
#               usermap/es-cl.dat, es-cl-informal.dat, es-cl-speech.dat,
#               es-cl-19th-century.dat
#                                     the user map of each config: the
#                                     stand-in tokens, novela, vela and velo
#                                     as nouns, and the kind's own lines
#               stand-ins.tsv         the stand-in tokens and their tags,
#                                     read by the tagger
#           config/es-cl.cfg, es-cl-informal.cfg, es-cl-speech.cfg,
#           es-cl-19th-century.cfg    the configs, one per kind of text
#                                     (modern writing, informal modern
#                                     writing, transcribed speech,
#                                     19th-century writing; decided 261119)
#           config/es-cl-conll-columns.cfg
#                                     the CoNLL columns the configs name
#           common/nec/cities.dat     the classifier's city list (FreeLing's
#                                     two lists merged, with the Chilean
#                                     places)
#           es/nerc/data/gazLOC-c.dat, gazPER-c.dat, gazPER-p.dat
#                                     the classifier's place and person lists
#           es/nerc/nec/nec-ab-poor1.dat
#                                     the classifier's model, with the class
#                                     shares of some names (<ClassShares>)
#           es/afixos.dat             the Spanish affix rules, with the
#                                     clitic rules restricted (decided
#                                     261116: te only after an infinitive,
#                                     a gerund or a tú imperative, os only
#                                     after an infinitive or a gerund or by
#                                     FreeLing's vosotros rules, never te
#                                     twice or te with os); every Spanish
#                                     config reads it but FreeLing Old's
#       and makes es/locucions.dat, the multiword file FreeLing Old
#       (config/es-old.cfg) reads, a link to es-cl/locucions.dat, the
#       Chilean file with FreeLing's general multiwords merged in (decided
#       261113: es-old's own folder stays as FreeLing ships it). FreeLing's
#       own es/locucions.dat is retired like a replaced file.
#       and retires, as replaced files are (below), the FreeLing files the
#       Chilean ones replace and nothing reads any more:
#           common/nec/cities-CL.dat           merged into cities.dat
#           es/nerc/data/gazPER-p.dat.upstream FreeLing's own name parts,
#                                              kept there on 291026
#       and retires the 19th-century files from their former folder,
#       es/es-cl/historical/ (renamed 19th-century/, decided 261119).
#       Since 2.6.0 the release's configs are the configs everything is
#       tagged with (decided 261119), so they are installed here; until
#       then FreeLing's own es-cl.cfg was retired and the corpora were
#       tagged with configs of their own.
#
# Only files whose content differs are replaced. The file replaced is first
# moved to a deprecated/ folder beside it, named
# <name>.DEPRECATED-YYMMDD[letter]<extension>. The entries and remove files'
# copies go to the folder above (dictionary/deprecated/, deprecated/),
# because FreeLing's build reads those folders whole. In the installed data
# (--target system) the copy is also compressed (.xz) and made unreadable
# (mode 000), so that FreeLing can never read a replaced file (decided
# 261109). Nothing is ever deleted.
#
# Every target file is checked BEFORE anything is moved: an immutable
# (chattr +i) or read-only file refuses the whole run and prints the
# command that clears it.
#
# --target system first checks that the installed FreeLing library
# (lib/libfreeling.so beside the data's share/ folder, or --lib) has the
# name-class change:
# FreeLing without it stops with an error on the classifier file's
# <ClassShares> section, so the files are never put where a library that
# cannot read them would use them.
#
# Executes by default. --dry-run lists what would change. Linux. Standard
# library only.

from __future__ import annotations

import argparse
import hashlib
import lzma
import os
import shutil
import sys
import time
from pathlib import Path

VERSION = "2.9.0"

PRODUCT_REL = Path("derived-software/FreeLing_es-CL_2027")
RELEASE_REL = PRODUCT_REL / "dist" / "FreeLing-es_CL-2027"
GRAM_REL = PRODUCT_REL / "data" / "grammatical-lists" / "freeling-cl"
# The raw copy of each list, in FreeLing's own format, which other
# tools read: written with its list so the two never differ.
RAW_DIR = "source-files"
# FreeLing 4.2 in the product folder: its source tree's Chilean data,
# and its installation.
BUILD_REL = (PRODUCT_REL / "third-party" / "FreeLing-4.2" / "data" /
             "es" / "es-cl")
SHARE_REL = PRODUCT_REL / "third-party" / "freeling" / "share" / "freeling"
LIB_REL = PRODUCT_REL / "third-party" / "freeling" / "lib" / "libfreeling.so"
KNOWN_EXT = (".txt", ".dat", ".src", ".tsv", ".md", ".cfg")
# The configs of the release, one per kind of text (decided 261119).
CONFIG_NAMES = ("es-cl", "es-cl-informal", "es-cl-speech",
                "es-cl-19th-century")
# Paths under the release's data/ folder and under the installed share
# folder alike.
SYSTEM_FILES = ["es/es-cl/" + n for n in (
    "dicc.src", "informal/dicc.src", "19th-century/dicc.src",
    "19th-century/probabilitats.dat",
    "19th-century/locucions.dat", "probabilitats.dat", "locucions.dat",
    "tagset.dat", "np.dat", "np-speech.dat", "quantities.dat",
    "usermap-informal.dat", "stand-ins.tsv")] + [
    "es/es-cl/usermap/%s.dat" % c for c in CONFIG_NAMES] + [
    "config/%s.cfg" % c for c in CONFIG_NAMES] + [
    "config/es-cl-conll-columns.cfg"] + [
    "common/nec/cities.dat", "es/nerc/data/gazLOC-c.dat",
    "es/nerc/data/gazPER-c.dat", "es/nerc/data/gazPER-p.dat",
    "es/nerc/nec/nec-ab-poor1.dat", "es/afixos.dat"]
# The link FreeLing Old reads its multiwords through (decided 261113).
OLD_LINK = ("es/locucions.dat", "es-cl/locucions.dat")
# Build-tree files the build no longer writes (--target user).
USER_RETIRE = ["dictionary/entries/CL.misspellings",
               "dictionary/entries/CL.reduced-forms"]
# FreeLing files the Chilean ones replace (decided 261110d): retired from
# the share folder when present.
SYSTEM_RETIRE = ["common/nec/cities-CL.dat",
                 "es/nerc/data/gazPER-p.dat.upstream",
                 # the 19th-century files' former folder (renamed 261119)
                 "es/es-cl/historical/dicc.src",
                 "es/es-cl/historical/probabilitats.dat",
                 "es/es-cl/historical/locucions.dat"]
USER_FILES = ["probabilitats.dat", "locucions.dat", "tagset.dat"]
# What the library with the name-class change holds and FreeLing 4.2 does
# not: the section names it reads and the keep: option of
# <SentenceStartClasses> (wide strings, UTF-32 little-endian on Linux).
LIB_MARKS = ("DictionaryClasses", "FixedClasses", "ClassesAtSentenceStart",
             "SentenceStartClasses", "ClassShares", "keep:")

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


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def deprecated_name(target: Path, stamp: str, compress: bool) -> Path:
    name = target.name
    ext = ""
    for e in KNOWN_EXT:
        if name.endswith(e):
            name, ext = name[:-len(e)], e
            break
    if compress:
        ext += ".xz"
    # FreeLing's build reads the entries and remove folders whole: their
    # deprecated copies go beside them, never inside.
    if target.parent.name in ("entries", "remove"):
        d = target.parent.parent / "deprecated"
    else:
        d = target.parent / "deprecated"
    for letter in [""] + list("bcdefghijklmnopqrstuvwxyz"):
        p = d / ("%s.DEPRECATED-%s%s%s" % (name, stamp, letter, ext))
        if not p.exists():
            return p
    raise SystemExit("REFUSED: too many deprecated copies of %s" % target)


def plan(pairs):
    """pairs: (source, target). Returns the pairs whose content differs."""
    out = []
    for src, dst in pairs:
        if not src.is_file():
            raise SystemExit("REFUSED: the release lacks %s" % src)
        if dst.is_file() and sha(dst) == sha(src):
            continue
        out.append((src, dst))
    return out


def writable(p: Path) -> str | None:
    if p.exists():
        try:
            with p.open("ab"):
                pass
        except OSError as exc:
            return exc.strerror
    d = p.parent
    while not d.exists():
        d = d.parent
    if not os.access(d, os.W_OK):
        return "folder not writable"
    return None


def library_marks_missing(lib: Path):
    """The marks of LIB_MARKS the library lacks (None: no library)."""
    if not lib.is_file():
        return None
    data = lib.resolve().read_bytes()
    return [m for m in LIB_MARKS if m.encode("utf-32-le") not in data]


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_escl_deploy.py",
        description="Deploy a FreeLing es-CL 2027 build. EXECUTES BY DEFAULT.")
    ap.add_argument("--target", required=True, choices=("user", "system"))
    ap.add_argument("--release", default=None, help="the release "
                    "folder (default: <project root>/%s)" % RELEASE_REL)
    ap.add_argument("--root", default=None, help="project root (default: "
                    "found from this script's location by PROJECT_ROOT.txt)")
    ap.add_argument("--build-tree", default=None, help="the Chilean data "
                    "of FreeLing's source tree (default: <project root>/%s)"
                    % BUILD_REL)
    ap.add_argument("--share", default=None,
                    help="FreeLing's installed data (default: <project "
                    "root>/%s)" % SHARE_REL)
    ap.add_argument("--lib", default=None,
                    help="the installed FreeLing library, checked by "
                    "--target system (default: <project root>/%s)" % LIB_REL)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    found = Path(a.root).resolve() if a.root else \
        find_project_root(Path(__file__).resolve().parent)
    if found is None and not (a.release and a.build_tree and a.share
                              and a.lib):
        log("REFUSED: no PROJECT_ROOT.txt above this script; give --root, "
            "or --release, --build-tree, --share and --lib")
        return 2
    rel = Path(a.release) if a.release else found / RELEASE_REL
    a.build_tree = a.build_tree or str(found / BUILD_REL)
    a.share = a.share or str(found / SHARE_REL)
    a.lib = a.lib or str(found / LIB_REL)
    data = rel / "data" / "es" / "es-cl"
    is_root = hasattr(os, "geteuid") and os.geteuid() == 0

    log("=" * 78)
    log("FREELING ES-CL DEPLOY  %s   target: %s%s"
        % (VERSION, a.target, "   (DRY RUN)" if a.dry_run else ""))
    log("=" * 78)
    log("release: %s" % rel)
    if not (rel / "SHA256SUMS").is_file():
        log("REFUSED: not a build of freeling_escl_build.py: %s" % rel)
        return 2
    bad = []
    for line in (rel / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        h, _, r = line.partition("  ")
        p = rel / r
        if r and (not p.is_file() or sha(p) != h):
            bad.append(r)
    if bad:
        for b in bad:
            log("REFUSED: release file missing or changed since the build: %s"
                % b)
        return 2
    lacking = [n for n in SYSTEM_FILES if not (rel / "data" / n).is_file()]
    if lacking:
        for n in lacking:
            log("REFUSED: the release lacks data/%s" % n)
        log("It was made by an older freeling_escl_build.py: rebuild it "
            "with 2.16.0 or later.")
        return 2

    pairs = []
    retire = []
    link = None
    compress = a.target == "system"
    if a.target == "user":
        if is_root:
            log("REFUSED: run --target user as your own user, not with "
                "sudo (the files must stay yours)")
            return 2
        root = Path(a.root).resolve() if a.root else find_project_root(
            Path(__file__).resolve().parent)
        if root is None:
            log("REFUSED: no PROJECT_ROOT.txt above this script; give --root")
            return 2
        gram = root / GRAM_REL
        bt = Path(a.build_tree)
        for d in (gram, bt / "dictionary" / "entries"):
            if not d.is_dir():
                log("REFUSED: not found: %s" % d)
                return 2
        for src in sorted((rel / "grammatical-lists" / "freeling-cl").glob(
                "*.GRAM.txt")):
            pairs.append((src, gram / src.name))
            raw = gram / RAW_DIR / (
                src.name[:-len(".GRAM.txt")] + ".txt")
            if raw.is_file():
                pairs.append((src, raw))
        for src in sorted((data / "dictionary" / "entries").glob("CL.*")):
            pairs.append((src, bt / "dictionary" / "entries" / src.name))
        pairs.append((data / "remove" / "CL.removed",
                      bt / "remove" / "CL.removed"))
        for n in USER_FILES:
            pairs.append((data / n, bt / n))
        retire = [bt / n for n in USER_RETIRE if (bt / n).exists()]
    else:
        share = Path(a.share)
        # The installed data belongs to whoever installed FreeLing: yours
        # in the product folder, root's in a system folder.
        if share.is_dir():
            owner_is_root = share.stat().st_uid == 0
            if owner_is_root and not is_root:
                log("REFUSED: %s is root's; run --target system with sudo"
                    % share)
                return 2
            if is_root and not owner_is_root:
                log("REFUSED: %s is not root's; run --target system as your "
                    "own user, not with sudo (the files must stay yours)"
                    % share)
                return 2
        for d in (share / "es" / "es-cl", share / "common" / "nec",
                  share / "es" / "nerc" / "data",
                  share / "es" / "nerc" / "nec", share / "config"):
            if not d.is_dir():
                log("REFUSED: not found: %s" % d)
                return 2
        lib = Path(a.lib)
        missing = library_marks_missing(lib)
        if missing is None:
            log("REFUSED: not found: %s" % lib)
            return 2
        if missing:
            log("REFUSED: %s lacks the name-class change (no %s). FreeLing "
                "without it stops on the classifier file of this release. "
                "Build and install the library with the change first "
                "(software/patches/freeling-4.2-np-classes_README.md)."
                % (lib, ", ".join(missing)))
            return 2
        log("library: %s has the name-class change" % lib.resolve())
        for n in SYSTEM_FILES:
            pairs.append((rel / "data" / n, share / n))
        retire = [share / n for n in SYSTEM_RETIRE if (share / n).exists()]
        link_p = share / OLD_LINK[0]
        if link_p.is_symlink() and os.readlink(link_p) == OLD_LINK[1]:
            link = None
        else:
            link = link_p
            if link_p.exists() or link_p.is_symlink():
                retire.append(link_p)

    todo = plan(pairs)
    stamp = time.strftime("%y%m%d")
    log("")
    log("%d file(s) checked, %d differ" % (len(pairs), len(todo)))
    moves = []
    for src, dst in todo:
        dep = deprecated_name(dst, stamp, compress) if dst.exists() else None
        moves.append((src, dst, dep))
        log("  %s" % dst)
        log("      %s" % ("old one -> %s%s" % (dep, " (compressed, mode 000)"
                                               if compress else "")
                          if dep else "new file"))
    retires = []
    if retire:
        log("")
        log("%d file(s) no longer read, to retire" % len(retire))
    for old in retire:
        dep = deprecated_name(old, stamp, compress)
        retires.append((old, dep))
        log("  %s" % old)
        log("      -> %s%s" % (dep, " (compressed, mode 000)" if compress
                               else ""))
    if link:
        log("")
        log("link for FreeLing Old: %s -> %s" % (link, OLD_LINK[1]))
    locked = [(dst, why) for _, dst, _ in moves
              for why in [writable(dst)] if why]
    locked += [(old, why) for old, _ in retires
               for why in [writable(old)] if why and not old.is_symlink()]
    if link and not os.access(link.parent, os.W_OK):
        locked.append((link.parent, "folder not writable"))
    if locked:
        log("")
        for dst, why in locked:
            log("PROTECTED: %s (%s)" % (dst, why))
        log("REFUSED: these files cannot be replaced. Clear the flag first:")
        log("   sudo chattr -i %s" % " ".join(str(d) for d, _ in locked))
        log("Nothing was moved or written.")
        return 2
    if a.dry_run:
        log("")
        log("DRY RUN -- nothing moved or written.")
        return 0
    if not moves and not retires and not link:
        log("Nothing to do: every file is already current.")
        return 0
    for src, dst, dep in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_name(dst.name + ".part")
        shutil.copyfile(src, tmp)
        if compress:
            os.chmod(tmp, 0o644)
        if dep:
            dep.parent.mkdir(parents=True, exist_ok=True)
            if compress:
                part = dep.with_name(dep.name + ".part")
                with dst.open("rb") as fi, lzma.open(part, "wb",
                                                     preset=9) as fo:
                    for chunk in iter(lambda: fi.read(1 << 20), b""):
                        fo.write(chunk)
                os.replace(part, dep)
                os.chmod(dep, 0o000)
                os.replace(tmp, dst)
            else:
                os.replace(dst, dep)
                os.replace(tmp, dst)
        else:
            os.replace(tmp, dst)
    for old, dep in retires:
        dep.parent.mkdir(parents=True, exist_ok=True)
        if old.is_symlink():
            # a link elsewhere: nothing to keep but where it pointed
            dep.with_suffix(dep.suffix + ".link").write_text(
                os.readlink(old) + "\n", encoding="utf-8")
            os.unlink(old)
            continue
        if not compress:
            os.replace(old, dep)
            continue
        part = dep.with_name(dep.name + ".part")
        with old.open("rb") as fi, lzma.open(part, "wb", preset=9) as fo:
            for chunk in iter(lambda: fi.read(1 << 20), b""):
                fo.write(chunk)
        os.replace(part, dep)
        os.chmod(dep, 0o000)
        os.unlink(old)
    if link:
        os.symlink(OLD_LINK[1], link)
    log("")
    log("%d file(s) replaced; previous versions kept in deprecated/%s" % (
        sum(1 for m in moves if m[2]),
        " (compressed, mode 000)" if compress else ""))
    log("%d new file(s)" % sum(1 for m in moves if not m[2]))
    if retires:
        log("%d file(s) retired to deprecated/%s" % (
            len(retires), " (compressed, mode 000)" if compress else ""))
    if link:
        log("FreeLing Old reads the Chilean multiwords: %s -> %s"
            % (link, OLD_LINK[1]))
    log("=" * 78)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(130)
