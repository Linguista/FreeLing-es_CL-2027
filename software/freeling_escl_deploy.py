#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 2.2.2
#
# freeling_escl_deploy.py -- put a FreeLing es-CL 2027 build (made by
# freeling_escl_build.py) where it is used.
#
#   --target user     run as your own user, NOT as root
#       the CSLD grammatical lists
#           <project root>/linguistic-derived/grammatical-lists/individual/
#               contemporary/freeling-cl/CL.*.GRAM.txt
#       the FreeLing build tree (FreeLing's own build reads it)
#           /home/user/build/FreeLing-4.2/data/es/es-cl/
#               dictionary/entries/CL.*   the Chilean entries
#               remove/CL.removed         the Spanish readings removed
#               probabilitats.dat, locucions.dat, tagset.dat
#       and retires, as replaced files are (below), the entries file the
#       build no longer writes:
#           dictionary/entries/CL.misspellings  now CL.common-misspellings
#   --target system   run with sudo
#       the installed data FreeLing reads, in /usr/local/share/freeling/
#           es/es-cl/
#               dicc.src              the default dictionary (contemporary)
#               historical/dicc.src   the 19th-century dictionary (historical
#                                     corpora only), with its own
#               historical/probabilitats.dat, historical/locucions.dat
#               np.dat                the name recognizer, written texts
#               np-speech.dat         the name recognizer, transcribed speech
#               probabilitats.dat, locucions.dat, tagset.dat, quantities.dat
#           common/nec/cities.dat     the classifier's city list (FreeLing's
#                                     two lists merged, with the Chilean
#                                     places)
#           es/nerc/data/gazLOC-c.dat, gazPER-c.dat, gazPER-p.dat
#                                     the classifier's place and person lists
#           es/nerc/nec/nec-ab-poor1.dat
#                                     the classifier's model, with the class
#                                     shares of some names (<ClassShares>)
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
#       and retires the es-cl configs from config/ (es-cl.cfg, installed
#       by FreeLing's own install, and es-cl-19th-century.cfg): the CSLD
#       tags only with csld-es-cl.cfg and the configs written from it, so
#       no other es-cl config is kept where it could be used by mistake
#       (decided 261113). The release's two configs are in its data/config/
#       folder and in the packages, not installed here.
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
# (/usr/local/lib/libfreeling.so, or --lib) has the name-class change:
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

VERSION = "2.2.2"

RELEASE = Path("/home/user/software/"
               "FreeLing_es-CL_2027")
GRAM_REL = Path("linguistic-derived/grammatical-lists/individual/"
                "contemporary/freeling-cl")
BUILD_TREE = Path("/home/user/build/FreeLing-4.2/data/es/es-cl")
SHARE = Path("/usr/local/share/freeling")
KNOWN_EXT = (".txt", ".dat", ".src", ".tsv", ".md", ".cfg")
# Paths under the release's data/ folder and under the installed share
# folder alike.
SYSTEM_FILES = ["es/es-cl/" + n for n in (
    "dicc.src", "historical/dicc.src", "historical/probabilitats.dat",
    "historical/locucions.dat", "probabilitats.dat", "locucions.dat",
    "tagset.dat", "np.dat", "np-speech.dat", "quantities.dat")] + [
    "common/nec/cities.dat", "es/nerc/data/gazLOC-c.dat",
    "es/nerc/data/gazPER-c.dat", "es/nerc/data/gazPER-p.dat",
    "es/nerc/nec/nec-ab-poor1.dat"]
# The link FreeLing Old reads its multiwords through (decided 261113).
OLD_LINK = ("es/locucions.dat", "es-cl/locucions.dat")
# Build-tree files the build no longer writes (--target user).
USER_RETIRE = ["dictionary/entries/CL.misspellings"]
# FreeLing files the Chilean ones replace (decided 261110d): retired from
# the share folder when present.
SYSTEM_RETIRE = ["common/nec/cities-CL.dat",
                 "es/nerc/data/gazPER-p.dat.upstream",
                 # decided 261113: the CSLD tags only with csld-es-cl.cfg
                 # and the configs written from it
                 "config/es-cl.cfg", "config/es-cl-19th-century.cfg"]
USER_FILES = ["probabilitats.dat", "locucions.dat", "tagset.dat"]
LIBFREELING = Path("/usr/local/lib/libfreeling.so")
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
    ap.add_argument("--release", default=str(RELEASE))
    ap.add_argument("--root", default=None, help="project root (default: "
                    "found from this script's location by PROJECT_ROOT.txt)")
    ap.add_argument("--build-tree", default=str(BUILD_TREE))
    ap.add_argument("--share", default=str(SHARE),
                    help="FreeLing's installed data (default: %(default)s)")
    ap.add_argument("--lib", default=str(LIBFREELING),
                    help="the installed FreeLing library, checked by "
                    "--target system (default: %(default)s)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    rel = Path(a.release)
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
    if not (data / "historical" / "dicc.src").is_file() or \
            not (data / "historical" / "probabilitats.dat").is_file() or \
            not (rel / "data" / "config" / "es-cl-19th-century.cfg").is_file() \
            or not (data / "np-speech.dat").is_file() or \
            not (rel / "data" / "es" / "nerc" / "nec" /
                 "nec-ab-poor1.dat").is_file():
        log("REFUSED: the release has no 19th-century dictionary and "
            "config, no np-speech.dat or no nec-ab-poor1.dat: it was made by "
            "an older freeling_escl_build.py")
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
        for src in sorted((data / "dictionary" / "entries").glob("CL.*")):
            pairs.append((src, bt / "dictionary" / "entries" / src.name))
        pairs.append((data / "remove" / "CL.removed",
                      bt / "remove" / "CL.removed"))
        for n in USER_FILES:
            pairs.append((data / n, bt / n))
        retire = [bt / n for n in USER_RETIRE if (bt / n).exists()]
    else:
        if not is_root:
            log("REFUSED: --target system writes /usr/local; run it with sudo")
            return 2
        share = Path(a.share)
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
