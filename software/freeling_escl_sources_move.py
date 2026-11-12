#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.0.0
#
# freeling_escl_sources_move.py -- move the decision files that the FreeLing
# es-CL build reads out of the COSCACH decisions folder into the FreeLing
# tree (software/10-Infrastructure/freeling/escl-sources/), leaving a
# relative link in each one's old place (decided 261112). There is then one
# copy of each file: the build reads it in escl-sources, and the COSCACH
# spelling step reads it through the link.
#
# Only the kinds of file the build reads are moved (BUILD_STEMS, the same
# list as in freeling_escl_build.py). Everything else in the COSCACH folder
# stays an ordinary file there: the occurrence rulings and the other files
# that quote the interviews, the markers, kept-as-is, Perkins respellings,
# foreign words and the records. The deprecated/ folder is not touched.
#
# For each file: copied into escl-sources under a temporary name, its
# sha256 checked against the original, renamed into place, and the original
# replaced by a relative link whose target is checked again by sha256. A
# file already linked is left alone. A file of the same name already in
# escl-sources is linked only if it is byte for byte the same; otherwise it
# is reported and nothing is done to either. A file that cannot be written
# or removed (an immutable flag, permissions) is reported, never forced.
#
# --check moves nothing and reports the state of every file the build
# reads, as the build checks it.
#
# EXECUTES BY DEFAULT; --dry-run reports what would be done. Linux (the
# links need a file system with symlinks; on Windows they need Developer
# Mode or administrator rights). Standard library only.

from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import sys
from pathlib import Path

VERSION = "1.0.0"

DST_REL = Path("software/10-Infrastructure/freeling/escl-sources")
SRC = Path("/home/user/corpora/050-Spelling-normalized/"
           "COSCACH/_processing-records/spelling-review/decisions")
LOG_REL = Path("working/freeling")
BUILD_STEMS = (
    "all-corpora-replacements", "correction-lemmas",
    "dictionary-addition-removals", "dictionary-additions",
    "dictionary-additions-all-rounds-standardized", "dictionary-variants",
    "fixed-name-classes", "interjection-removals", "interjections",
    "lemma-standardization", "name-class-shares", "person-name-removals",
    "place-only-forms", "sentence-start-classes", "text-correction-removals",
    "text-corrections", "verb-form-readings",
)


def log(*a):
    print(*a, flush=True)


def find_project_root(start: Path) -> Path | None:
    for d in [start, *start.parents]:
        if (d / "PROJECT_ROOT.txt").is_file():
            return d
    return None


def stem_of(name: str) -> str | None:
    if not name.endswith(".tsv") or "--" not in name:
        return None
    return name.split("--", 1)[0]


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def link_ok(link: Path, target: Path) -> bool:
    return link.is_symlink() and link.resolve() == target.resolve() \
        and target.is_file()


def move_one(src: Path, dst_dir: Path, dry: bool):
    """(action, detail) for one file of the COSCACH folder."""
    dst = dst_dir / src.name
    if src.is_symlink():
        if link_ok(src, dst):
            return "already linked", ""
        return "PROBLEM", "a link to %s, not to %s" % (os.readlink(src), dst)
    h = sha_file(src)
    if dst.exists():
        if dst.is_symlink() or not dst.is_file():
            return "PROBLEM", "%s exists and is not an ordinary file" % dst
        if sha_file(dst) != h:
            return "PROBLEM", ("%s exists with other content (sha256 %s, "
                               "here %s): nothing done" % (dst, sha_file(dst), h))
        copied = False
    else:
        copied = True
    rel = os.path.relpath(dst, src.parent)
    if dry:
        return ("would move and link" if copied else "would link (same file "
                "already in escl-sources)"), h
    try:
        if copied:
            part = dst_dir / (src.name + ".part")
            with open(src, "rb") as fi, open(part, "wb") as fo:
                for b in iter(lambda: fi.read(1 << 20), b""):
                    fo.write(b)
                fo.flush()
                os.fsync(fo.fileno())
            if sha_file(part) != h:
                part.unlink()
                return "PROBLEM", "the copy does not match the original"
            st = src.stat()
            os.utime(part, ns=(st.st_atime_ns, st.st_mtime_ns))
            os.replace(part, dst)
        tmp = src.with_name(src.name + ".link-part")
        if tmp.is_symlink() or tmp.exists():
            tmp.unlink()
        os.symlink(rel, tmp)
        os.replace(tmp, src)
    except OSError as e:
        return "PROBLEM", "%s: %s (an immutable flag or permissions: " \
            "nothing forced)" % (type(e).__name__, e)
    if not link_ok(src, dst) or sha_file(src) != h:
        return "PROBLEM", "the link does not lead to a file with the " \
            "original content"
    return ("moved and linked" if copied else "linked"), h


def check(src_dir: Path, dst_dir: Path):
    rows = []
    for p in sorted(src_dir.iterdir()):
        if stem_of(p.name) not in BUILD_STEMS:
            continue
        if link_ok(p, dst_dir / p.name):
            rows.append(("linked", p.name))
        elif p.is_symlink():
            rows.append(("WRONG LINK", p.name))
        else:
            rows.append(("ORDINARY FILE", p.name))
    for p in sorted(dst_dir.iterdir()) if dst_dir.is_dir() else []:
        if stem_of(p.name) in BUILD_STEMS and not (src_dir / p.name).is_symlink():
            rows.append(("NO LINK", p.name))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_escl_sources_move.py",
        description="Move the decision files the FreeLing es-CL build reads "
        "into escl-sources and link them back. EXECUTES BY DEFAULT.")
    ap.add_argument("--root", default=None, help="project root (default: "
                    "found from this script's location by PROJECT_ROOT.txt)")
    ap.add_argument("--from", dest="src", default=str(SRC),
                    help="the COSCACH decisions folder (default: %(default)s)")
    ap.add_argument("--to", dest="dst", default=None,
                    help="escl-sources (default: <project root>/%s)" % DST_REL)
    ap.add_argument("--check", action="store_true",
                    help="move nothing; report the state of every file")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be done, change nothing")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    here = Path(__file__).resolve().parent
    root = Path(a.root).resolve() if a.root else find_project_root(here)
    if root is None:
        log("REFUSED: no PROJECT_ROOT.txt above this script; give --root")
        return 2
    src_dir = Path(a.src)
    dst_dir = Path(a.dst) if a.dst else root / DST_REL
    log("=" * 78)
    log("FREELING ES-CL SOURCES MOVE  %s%s" % (
        VERSION, "   CHECK" if a.check else "   DRY RUN" if a.dry_run else ""))
    log("=" * 78)
    log("COSCACH decisions : %s" % src_dir)
    log("escl-sources      : %s" % dst_dir)
    if not src_dir.is_dir():
        log("REFUSED: not found: %s" % src_dir)
        return 2

    if a.check:
        rows = check(src_dir, dst_dir)
        for state, name in rows:
            log("%-13s  %s" % (state, name))
        bad = [r for r in rows if r[0] != "linked"]
        log("")
        log("%d linked, %d not in order" % (len(rows) - len(bad), len(bad)))
        return 1 if bad else 0

    if not a.dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)
    todo = [p for p in sorted(src_dir.iterdir())
            if stem_of(p.name) in BUILD_STEMS
            and (p.is_file() or p.is_symlink())]
    stamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    out = ["action\tsha256\tdetail\tfile"]
    counts = {}
    for p in todo:
        action, detail = move_one(p, dst_dir, a.dry_run)
        counts[action] = counts.get(action, 0) + 1
        h = detail if len(detail) == 64 else ""
        d = "" if h else detail
        log("%-22s  %s" % (action, p.name))
        if d:
            log("    %s" % d)
        out.append("\t".join([action, h, d, p.name]))
    log("")
    for k in sorted(counts):
        log("%5d  %s" % (counts[k], k))
    logdir = root / LOG_REL
    logdir.mkdir(parents=True, exist_ok=True)
    base = "freeling_escl_sources_move--%s%s" % (
        stamp, "--DRY-RUN" if a.dry_run else "")
    lp = logdir / (base + ".tsv")
    n = 0
    while lp.exists():
        n += 1
        lp = logdir / ("%s%s.tsv" % (base, chr(ord("a") + n)))
    lp.write_text("\n".join(out) + "\n", encoding="utf-8")
    log("log: %s" % lp)
    return 1 if counts.get("PROBLEM") else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(130)
