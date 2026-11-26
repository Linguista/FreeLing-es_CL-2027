#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.2.0
#
# freeling.py -- tags a corpus with FreeLing es-CL 2027, step by step, into
# numbered stage folders: 060 FreeLing, 070 Universal Dependencies, 080
# Perkins, 400 Parquet. Only the steps named on the command line run, at
# least one; with none, or with -h, it lists them.
#
# Every corpus has its folder, corpora/<corpus>/, beside software/ and data/
# in the release folder (corpora/ may be a link to a folder elsewhere):
#
#   corpora/<corpus>/input/<kind>     a link to the corpus root; the kind is
#                                     speech, written-modern,
#                                     written-19th-century or written-old
#   corpora/<corpus>/informal.txt     written-modern only, optional: the
#                                     informal texts, one path per line
#   corpora/<corpus>/060-FreeLing-Tagged/ ... one folder per stage made,
#                                     made here or a link to a folder
#   corpora/<corpus>/_processing-records/  the log of every run
#
# Every stage folder holds README.md (what is in it, how it was made, what
# it is used for next), columns.tsv (one row per column: position, name,
# step, option, program and version) and its own _processing-records/.
# A stage is made when its folder holds columns.tsv; a step whose earlier
# stage is not made is refused, naming the stages it needs.
#
# The stand-in tokens (XXXREDACTEDXXX and the others) are those of the
# installed stand-ins.tsv: each is sent to FreeLing in lower case and
# written back in FORM; any other XXX...XXX form fails its text. Three
# spellings are rewritten on the way to FreeLing (Bs. As., weo'n, pa'l) and
# the commas of the comma multiwords are sent as blanks; the texts are
# never changed and every character offset stays exact.
#
# EXECUTES BY DEFAULT. --dry-run checks everything and writes nothing.
# Linux and macOS. Python 3.9 or later; the Parquet step needs pyarrow and
# the Perkins step the perkins program.

from __future__ import annotations

import argparse
import os
import queue
import shutil
import signal
import sys
import textwrap
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import freeling_common as fc                                # noqa: E402

VERSION = "1.2.0"
__version__ = VERSION
PROG = "freeling.py"
STOP = threading.Event()

HELP = """usage: freeling.py CORPUS STEP... [options]
       freeling.py --new CORPUS --kind KIND --input DIR [--link-stage NNN=DIR]...
       freeling.py CORPUS --link-stage NNN=DIR
       freeling.py --list

Tags a corpus with FreeLing es-CL 2027 into numbered stage folders under
corpora/CORPUS/. Only the steps named run; at least one is required. Each
step needs the stages listed with it, made earlier or in the same run.

THE STEPS
{steps}

  Reserved stage numbers (no step yet):
{reserved}

THE KINDS OF TEXT (the name of the link in corpora/CORPUS/input/)
{kinds}

SETTING UP A CORPUS
  --new CORPUS --kind KIND --input DIR
                      make corpora/CORPUS/ with input/KIND, a link to DIR
  --link-stage NNN=DIR
                      make the stage folder NNN a link to DIR (an existing
                      stage, or a folder on another disk); with --new, or
                      with CORPUS alone
  --list              list the corpora and their stages

THE OPTIONS
  --dry-run           check everything, write nothing (the default is to run)
  --redo              redo documents already done (the default is to resume)
  --limit N           at most N documents per step
  --only FOLDER       only the texts under this folder of the corpus root
  --ext EXT           the extension of the texts (default .txt)
  --home DIR          the release folder (default: the folder above software/)
  --freeling-bin DIR  the folder of analyze and analyzer_client (default: PATH)
  --share DIR         FreeLing's data folder (default: share/freeling beside
                      the bin folder)
  --lib FILE          the FreeLing library (default: lib/libfreeling.so there)
  --version
  060: --workers N --dep lstm|treeler|txala --port N --host HOST
       --use-running-server --doc-timeout S --startup-timeout S
       --max-consecutive-failures N --allow-shrink --redo-before YYMMDD_HHMM
       --require-sidecars
  080: --perkins-columns="OPTIONS" (repeat: one column each; write the =,
       as options that begin with - are otherwise read as freeling.py's own)
       --perkins-word-alone="OPTIONS" (repeat) --perkins-bin FILE --jobs N

The full description is in freeling_README.md beside this script.
"""


def help_text():
    ind = " " * 15
    steps = "\n".join(
        "  %-12s %s\n%s\n%s" % (
            fc.STAGES[n][1], fc.STAGES[n][0],
            textwrap.fill(fc.STAGES[n][2] + ".", 78, initial_indent=ind,
                          subsequent_indent=ind),
            ("%sneeds: %s\n" % (ind, ", ".join(fc.STAGES[r][0]
                                              for r in fc.REQUIRES[n])))
            if fc.REQUIRES[n] else "")
        for n in fc.STEP_ORDER)
    reserved = "\n".join("    %-22s %s" % r for r in fc.RESERVED_STAGES)
    kinds = "\n".join("  %-22s %s" % (k, fc.KIND_TEXT[k]) for k in fc.KINDS)
    return HELP.format(steps=steps.rstrip("\n"), reserved=reserved, kinds=kinds)


def parse(argv):
    ap = argparse.ArgumentParser(prog=PROG, add_help=False)
    ap.add_argument("corpus", nargs="?")
    ap.add_argument("-h", "--help", action="store_true")
    ap.add_argument("--version", action="store_true")
    for num in fc.STEP_ORDER:
        ap.add_argument(fc.STAGES[num][1], action="store_true",
                        dest="step_" + num)
    ap.add_argument("--new", metavar="CORPUS")
    ap.add_argument("--kind", choices=fc.KINDS)
    ap.add_argument("--input", metavar="DIR")
    ap.add_argument("--link-stage", action="append", default=[],
                    metavar="NNN=DIR")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--redo", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", metavar="FOLDER")
    ap.add_argument("--ext", default=".txt")
    ap.add_argument("--home")
    ap.add_argument("--freeling-bin")
    ap.add_argument("--share")
    ap.add_argument("--lib")
    ap.add_argument("--no-colour", "--no-color", action="store_true",
                    dest="no_colour")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 8)
    ap.add_argument("--dep", default="lstm", choices=("lstm", "treeler", "txala"))
    ap.add_argument("--port", type=int, default=50005)
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--use-running-server", action="store_true")
    ap.add_argument("--doc-timeout", type=int, default=3600)
    ap.add_argument("--startup-timeout", type=int, default=600)
    ap.add_argument("--max-consecutive-failures", type=int, default=5)
    ap.add_argument("--allow-shrink", action="store_true")
    ap.add_argument("--redo-before", metavar="YYMMDD_HHMM")
    ap.add_argument("--require-sidecars", action="store_true")
    ap.add_argument("--perkins-columns", action="append", default=[],
                    metavar="OPTIONS")
    ap.add_argument("--perkins-word-alone", action="append", default=[],
                    metavar="OPTIONS")
    ap.add_argument("--perkins-bin", default="perkins")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 8)
    return ap.parse_args(argv)


# ---------------------------------------------------------------------------
class Ctx:
    """What every step of a run knows."""

    def __init__(self, a, home, cdir, kind, root, fl, rules):
        self.a = a
        self.home = home
        self.cdir = cdir
        self.name = cdir.name
        self.kind = kind
        self.root = root
        self.fl = fl
        self.rules = rules
        self.script_dir = HERE
        self.stamp = time.strftime("%y%m%d_%H%M")
        self.command = " ".join([PROG] + sys.argv[1:])
        self.version = VERSION
        self.branches = []

    def stage(self, num):
        return fc.stage_path(self.cdir, num)


def rel_link(target: Path, link: Path):
    """Make link a relative link to target."""
    link.parent.mkdir(parents=True, exist_ok=True)
    rel = os.path.relpath(str(target), str(link.parent))
    os.symlink(rel, str(link))
    return rel


def do_setup(a, home):
    """--new and --link-stage. Returns an exit code."""
    name = a.new or a.corpus
    p = fc.name_problem(name or "")
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    cdir = fc.corpora_dir(home) / name
    links = []
    for item in a.link_stage:
        num, _, d = item.partition("=")
        if num not in fc.STAGES or not d:
            fc.log(fc.red("REFUSED: --link-stage wants NNN=DIR, NNN one of %s: %s"
                          % (", ".join(fc.STEP_ORDER), item)))
            return 2
        links.append((num, Path(d).expanduser().absolute()))
    if a.new:
        if not a.kind or not a.input:
            fc.log(fc.red("REFUSED: --new needs --kind and --input"))
            return 2
        target = Path(a.input).expanduser().absolute()
        if not target.is_dir():
            fc.log(fc.red("REFUSED: --input is not a folder: %s" % target))
            return 2
        if cdir.exists() or cdir.is_symlink():
            fc.log(fc.red("REFUSED: the corpus folder exists already: %s" % cdir))
            return 2
    elif not cdir.is_dir():
        fc.log(fc.red("REFUSED: no such corpus: %s (make it with --new)" % cdir))
        return 2
    for num, d in links:
        sp = fc.stage_path(cdir, num)
        if sp.exists() or sp.is_symlink():
            fc.log(fc.red("REFUSED: the stage folder exists already: %s" % sp))
            return 2
    fc.log("corpus : %s" % cdir)
    if a.new:
        fc.log("input  : %s/%s -> %s" % (fc.INPUT, a.kind, target))
    for num, d in links:
        fc.log("stage  : %s -> %s%s" % (fc.STAGES[num][0], d,
                                        "" if d.exists() else
                                        "  (made when the step first runs)"))
    if a.dry_run:
        fc.log(fc.orange("DRY RUN -- nothing made."))
        return 0
    if a.new:
        rel_link(target, cdir / fc.INPUT / a.kind)
        fc.ensure_corpus_readmes(home, cdir, a.kind, cdir / fc.INPUT / a.kind, [])
    for num, d in links:
        rel_link(d, fc.stage_path(cdir, num))
    fc.log(fc.green("OK"))
    return 0


def do_list(home):
    cr = fc.corpora_dir(home)
    fc.log("corpora: %s%s" % (cr, "  (a link to %s)" % cr.resolve()
                              if cr.is_symlink() else ""))
    if not cr.is_dir():
        fc.log("   none yet")
        return 0
    for c in sorted(p for p in cr.iterdir() if p.is_dir()):
        kind, root, p = fc.corpus_input(c)
        fc.log("%s  %s" % (kind or "?", c.name))
        for num in fc.STEP_ORDER:
            sp = fc.stage_path(c, num)
            if sp.exists() or sp.is_symlink():
                fc.log("     %s %s%s" % ("made    " if fc.stage_made(c, num)
                                         else "not made",
                                         sp.name, "  -> %s" % sp.resolve()
                                         if sp.is_symlink() else ""))
    return 0


# ---------------------------------------------------------------------------
# Step 060: FreeLing.
STAGE_060_README = """# 060-FreeLing-Tagged / {name}

Made by `freeling.py` {version} (FreeLing es-CL 2027) on {date}, with
FreeLing 4.2's analyzer. Documents in this stage: {docs}.

## What is in it

One `NAME.conll` per text `NAME{ext}` of the corpus root, in the same
folders: one token per line, TAB-separated columns (listed in
`columns.tsv`), a blank line after each sentence. Every line of a text is
one sentence or utterance. `SPAN_BEGIN` and `SPAN_END` are each token's
character offsets in the text. `LEX_PROB` is the probability of the
selected reading among the readings of the word, out of context, and
`TAG_PROB` the probability the tagger gives the selected tag in its
sentence (both from 0 to 1): a low `TAG_PROB` marks a word the tagger
hesitated over. Where a text has a `NAME.times.tsv` beside
it (the times of each utterance of a recording), it is copied beside its
`NAME.conll`, unchanged.

## How it was made

- Kind of text: {kind}. Config: `{config}`.
{informal}- Parser: {dep}. Every line end ends a sentence (`--flush`).
- The stand-in tokens of `stand-ins.tsv` ({standins}) are sent to FreeLing
  in lower case, tagged by the config's user map, and written back in
  `FORM`; `LEMMA` has them in lower case.
- `Bs. As.` is sent as `BsAs`, `weo'n` and `wo'n` as `weón`, `pa'l` as
  `pal` (para + el); the commas of the comma multiwords
  are sent as blanks. The texts are not changed and every span is exact.
- The command: `{command}`

## What it is used for next

`freeling.py {corpus} --ud` (070-Universal-Dependency-Tagged) and
`freeling.py {corpus} --parquet` (400-Parquet).

## Records

`_processing-records/` holds the server log of each run, the list of the
documents that failed (only when one did) and the document count of the
last full scan.
"""


def tag_one(src, dst, sender, a, fl, port):
    """(ok, bytes written, tokens, note)."""
    side = src.with_name(src.name[:-len(a.ext)] + fc.SIDECAR)
    dside = dst.with_name(dst.name[:-len(".conll")] + fc.SIDECAR)
    if a.require_sidecars and not side.is_file():
        return False, 0, 0, "no %s beside the source" % side.name
    try:
        data = src.read_bytes()
    except OSError as exc:
        return False, 0, 0, "cannot read the source: %s" % exc
    send, state, problem = sender.prepare(data)
    if problem:
        return False, 0, 0, problem
    out, problem = fc.analyze_through_server(fl, a.host, port, send,
                                             a.doc_timeout)
    if problem:
        return False, 0, 0, problem
    if not out.strip() and data.strip():
        return False, 0, 0, "EMPTY output from a non-empty source"
    conll, ntok, problem = sender.finish(out, state)
    if problem:
        return False, 0, 0, problem
    # The sidecar first, the .conll last: the .conll marks a document done.
    tmp = dst.with_name(dst.name + ".part")
    sidetmp = dside.with_name(dside.name + ".part")
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_bytes(conll)
        if side.is_file():
            shutil.copy2(side, sidetmp)
            os.replace(sidetmp, dside)
        os.replace(tmp, dst)
    except BaseException:
        fc.unlink_quietly(tmp)
        fc.unlink_quietly(sidetmp)
        raise
    return True, len(conll), ntok, ""


def worker(q, sender, a, fl, port, stats, lock, failfh, proc):
    while not STOP.is_set():
        try:
            src, dst, insize = q.get_nowait()
        except queue.Empty:
            return
        try:
            ok, n, ntok, note = tag_one(src, dst, sender, a, fl, port)
        except Exception as exc:                            # noqa: BLE001
            ok, n, ntok, note = False, 0, 0, "%s: %s" % (type(exc).__name__, exc)
        with lock:
            stats["done"] += 1
            stats["inbytes"] += insize
            stats["tokens"] += ntok
            if ok:
                stats["bytes"] += n
                stats["streak"] = 0
            else:
                stats["failed"] += 1
                stats["streak"] += 1
                failfh.write("%s\t%s\n" % (note, src))
                failfh.flush()
                k = a.max_consecutive_failures
                if k and stats["streak"] % k == 0:
                    dead = (proc.poll() is not None) if proc is not None \
                        else not fc.port_open(port)
                    if dead:
                        stats["server_died"] = True
                        STOP.set()
                        fc.log(fc.red("STOPPED: the server is gone after %d "
                                      "failures in a row." % stats["streak"]))
                    else:
                        fc.log(fc.orange("WARNING: %d failures in a row, but the "
                                         "server is up: continuing."
                                         % stats["streak"]))
            el = time.time() - stats["t0"]
            tps = stats["tokens"] / el if el else 0
            bps = stats["inbytes"] / el if el else 0
            left = (stats["inbytes_total"] - stats["inbytes"]) / bps if bps else 0
            fc.log("%7d/%d  %s tok  %6.0f tok/s  %4.1f%%  eta %s  %s%s"
                   % (stats["done"], stats["total"], f"{stats['tokens']:,}", tps,
                      100.0 * stats["inbytes"] / max(stats["inbytes_total"], 1),
                      fc.hms(left), fc.red("FAILED ") if not ok else "",
                      src.name))
            if not ok:
                fc.log("         %s" % fc.orange(note))
        q.task_done()


def step_freeling(ctx: Ctx):
    a, fl = ctx.a, ctx.fl
    stage_name = fc.STAGES["060"][0]
    base_cfg = fc.CONFIGS[ctx.kind]
    cfgs = [base_cfg] + ([fc.INFORMAL_CONFIG] if ctx.rules else [])
    fc.log("")
    fc.log("STEP 060  %s" % stage_name)
    sender, problems, notes = fc.make_sender(fl, HERE, cfgs, a.dep)
    for n in notes:
        fc.log(n)
    p2, n2 = fc.library_checks(fl.lib, any(c in fc.NP_FILES for c in cfgs))
    for n in n2:
        fc.log("library: %s" % n)
    problems += p2
    if problems:
        for p in problems:
            fc.log(fc.red("REFUSED: %s" % p))
        return 2
    if ctx.kind == "written-old":
        fc.log(fc.orange("WARNING: written-old is tagged by FreeLing Old as "
                         "FreeLing ships it; texts holding stand-ins fail "
                         "(it has no user map)."))
    out_root = ctx.stage(num="060")
    scan_root = ctx.root
    if a.only:
        scan_root = (ctx.root / a.only.strip("/"))
        if not scan_root.is_dir():
            fc.log(fc.red("REFUSED: --only: not a folder of the corpus: %s"
                          % scan_root))
            return 2
    redo_before = None
    if a.redo_before:
        try:
            redo_before = time.mktime(time.strptime(a.redo_before, "%y%m%d_%H%M"))
        except ValueError:
            fc.log(fc.red("REFUSED: --redo-before wants YYMMDD_HHMM"))
            return 2
    fc.log("scanning %s ..." % scan_root)
    todo, skipped, seen = [], 0, 0
    nosidecar, restore = [], []
    tree = {}
    for src in sorted(scan_root.rglob("*" + a.ext)):
        if not src.is_file():
            continue
        rel = src.relative_to(ctx.root)
        if fc.RECORDS in rel.parts:
            continue
        seen += 1
        inf = fc.is_informal(rel, ctx.rules) if ctx.rules else False
        for i in range(len(rel.parts)):
            tree.setdefault(rel.parts[:i], [0, 0])[1 if inf else 0] += 1
        dst = out_root / rel.with_name(rel.name[:-len(a.ext)] + ".conll")
        side = src.with_name(src.name[:-len(a.ext)] + fc.SIDECAR)
        dside = dst.with_name(dst.name[:-len(".conll")] + fc.SIDECAR)
        if a.require_sidecars and not side.is_file():
            nosidecar.append(src)
        if dst.exists() and not a.redo:
            if redo_before is None or dst.stat().st_mtime >= redo_before:
                skipped += 1
                if side.is_file() and not dside.is_file():
                    restore.append((side, dside))
                continue
        todo.append((src, dst, src.stat().st_size, inf))
        if a.limit and len(todo) >= a.limit:
            break
    fc.log("%s document(s) to tag%s" % (
        f"{len(todo):,}", ", %s already done (resuming)" % f"{skipped:,}"
        if skipped else ""))
    ctx.branches = fc.branches(tree)
    if ctx.rules:
        fc.log("how the corpus is tagged (texts found, done or not):")
        for folder, how, n in ctx.branches:
            fc.log("   %-8s  %9s  %s" % (how, f"{n:,}", folder))
    if not seen:
        fc.log(fc.red("REFUSED: no %s texts under %s: an empty corpus is not a "
                      "finished job (is the disk mounted? is --ext right?)"
                      % (a.ext, scan_root)))
        return 2
    records = out_root / fc.RECORDS
    count_file = records / "corpus-count.txt"
    if not a.limit and not a.only:
        try:
            before = int(count_file.read_text(encoding="utf-8").split()[0])
        except (OSError, ValueError, IndexError):
            before = 0
        if before and seen < before * 0.9 and not a.allow_shrink:
            fc.log(fc.red("REFUSED: the corpus has shrunk: %s texts, %s at the "
                          "last full scan (a disk not mounted?); "
                          "--allow-shrink goes on" % (f"{seen:,}", f"{before:,}")))
            return 2
    if nosidecar:
        fc.log(fc.red("REFUSED: %d text(s) have no %s beside them "
                      "(--require-sidecars):" % (len(nosidecar), fc.SIDECAR)))
        for s in nosidecar[:20]:
            fc.log("   %s" % s)
        return 2
    lockd = []
    for src, dst, _, _ in todo:
        for p in (dst, dst.with_name(dst.name[:-len(".conll")] + fc.SIDECAR)):
            why = fc.locked(p)
            if why:
                lockd.append((p, why))
    for p in (out_root / "README.md", out_root / fc.COLUMNS_TSV) + \
            (() if a.limit or a.only else (count_file,)):
        why = fc.locked(p)
        if why:
            lockd.append((p, why))
    if lockd:
        fc.log(fc.red("REFUSED: %d file(s) cannot be replaced (immutable or "
                      "read-only):" % len(lockd)))
        for p, why in lockd[:10]:
            fc.log("   %s  %s" % (why, p))
        if len(lockd) > 10:
            fc.log("   ... and %s more" % f"{len(lockd) - 10:,}")
        for line in fc.unlock_lines([p for p, _ in lockd], out_root):
            fc.log(line)
        return 2
    if a.dry_run:
        for src, dst, _, inf in todo[:20]:
            fc.log("  would tag  %s%s" % ("(informal)  " if inf else "", src))
            fc.log("          -> %s" % dst)
        if len(todo) > 20:
            fc.log("  ... and %s more" % f"{len(todo) - 20:,}")
        if restore:
            fc.log("  %d sidecar(s) would be copied beside finished documents"
                   % len(restore))
        return 0
    fc.ensure_stage(ctx.cdir, "060")
    fc.ensure_records(out_root)
    if not a.limit and not a.only:
        fc.put_file("%d\t%s\n" % (seen, ctx.stamp), count_file)
    restore_failed = 0
    for side, dside in restore:
        try:
            fc.put_file(side, dside)
            fc.log("sidecar restored: %s" % dside)
        except OSError as exc:
            restore_failed += 1
            fc.log(fc.red("NOT RESTORED (%s): %s" % (exc.strerror, dside)))
    rc = 0
    if todo:
        rc = run_passes(ctx, sender, todo, base_cfg)
    if rc in (0, 1):
        write_060(ctx, sender, base_cfg, out_root)
    return 1 if (rc == 0 and restore_failed) else rc


def run_passes(ctx, sender, todo, base_cfg):
    a, fl = ctx.a, ctx.fl
    passes = [(cfg, [t[:3] for t in todo if t[3] == inf])
              for cfg, inf in ((base_cfg, False), (fc.INFORMAL_CONFIG, True))]
    passes = [p for p in passes if p[1]]
    if a.use_running_server:
        if len(passes) > 1:
            fc.log(fc.red("REFUSED: --use-running-server, but the texts need "
                          "two configs (formal and informal), one server each"))
            return 2
        if not fc.port_open(a.port):
            fc.log(fc.red("REFUSED: --use-running-server, but nothing is on "
                          "port %d" % a.port))
            return 2
    elif fc.port_open(a.port):
        fc.log(fc.red("REFUSED: port %d is already in use (a server left from "
                      "an earlier run?). Stop it, give --port, or attach to it "
                      "with --use-running-server." % a.port))
        return 2

    def _stop(sig, frm):                                    # noqa: ARG001
        if not STOP.is_set():
            fc.log(fc.orange("\nstopping after the documents in flight; the "
                             "same command resumes."))
            STOP.set()
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    records = ctx.stage("060") / fc.RECORDS
    failpath = records / ("freeling-FAILED--%s.tsv" % ctx.stamp)
    failfh = open(failpath, "a", encoding="utf-8")
    stats = {"done": 0, "failed": 0, "bytes": 0, "total": len(todo),
             "tokens": 0, "inbytes": 0, "inbytes_total": sum(t[2] for t in todo),
             "t0": time.time(), "streak": 0, "server_died": False}
    lock = threading.Lock()
    fc.log("%s of text to tag" % fc.human(stats["inbytes_total"]))
    for cfg, items in passes:
        if STOP.is_set():
            break
        fc.log("")
        fc.log("PASS: %s, %s document(s)" % (cfg, f"{len(items):,}"))
        proc = None
        if not a.use_running_server:
            cmd = fc.server_command(fl, cfg, a.dep, a.port, a.workers)
            fc.log("server : %s" % " ".join(cmd))
            slog = records / ("freeling-server--%s--%s.log"
                              % (ctx.stamp, cfg[:-4]))
            proc, problem = fc.start_server(cmd, slog, a.port, a.startup_timeout)
            if problem:
                fc.log(fc.red("STOPPED: %s" % problem))
                stats["server_died"] = True
                break
        stats["streak"] = 0
        q = queue.Queue()
        for item in items:
            q.put(item)
        threads = [threading.Thread(target=worker, daemon=True,
                                    args=(q, sender, a, fl, a.port, stats,
                                          lock, failfh, proc))
                   for _ in range(a.workers)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        if proc is not None:
            fc.stop_server(proc)
            if fc.port_open(a.port):
                fc.log(fc.red("WARNING: port %d is still in use after the "
                              "server was stopped" % a.port))
        if stats["server_died"]:
            break
    failfh.close()
    if not stats["failed"]:
        fc.unlink_quietly(failpath)
    el = time.time() - stats["t0"]
    tagged = stats["done"] - stats["failed"]
    fc.log("-" * 78)
    fc.log("%s tagged, %s failed, %s token(s), %s, %s"
           % (fc.green(f"{tagged:,}"), fc.red(f"{stats['failed']:,}")
              if stats["failed"] else "0", f"{stats['tokens']:,}",
              fc.human(stats["bytes"]), fc.hms(el)))
    if el and stats["failed"] <= tagged:
        fc.log("%.0f tok/s with at most %d of %d worker(s) busy"
               % (stats["tokens"] / el, min(a.workers, stats["total"]), a.workers))
    for name, n in sender.counts.items():
        if n:
            fc.log("rewritten on the way to FreeLing: %s %s" % (f"{n:,}", name))
    if stats["failed"]:
        fc.log(fc.orange("WARNING: the failures are listed in %s; nothing was "
                         "written for them. The same command resumes." % failpath))
    if stats["total"] - stats["done"] and not stats["server_died"]:
        fc.log(fc.orange("WARNING: %s document(s) not reached; the same command "
                         "resumes." % f"{stats['total'] - stats['done']:,}"))
    if stats["server_died"]:
        return 3
    if STOP.is_set():
        return 130
    return 1 if stats["failed"] else 0


# What the two probability columns hold, for columns.tsv.
COLUMN_NOTES = {
    "LEX_PROB": "FreeLing CoNLL column LEX_PROB: the probability of the "
                "selected reading among the readings of the word, out of "
                "context (0 to 1)",
    "TAG_PROB": "FreeLing CoNLL column TAG_PROB: the probability the tagger "
                "gives the selected tag in its sentence (0 to 1; - when the "
                "tagger did not compute it)",
}


def write_060(ctx, sender, base_cfg, out_root):
    a, fl = ctx.a, ctx.fl
    program = "FreeLing 4.2 analyze, config %s; freeling.py %s" % (base_cfg, VERSION)
    rows = [(c, "--freeling", COLUMN_NOTES.get(c, "FreeLing CoNLL column %s" % c),
             program) for c in sender.columns]
    fc.write_columns(out_root, rows)
    informal = ""
    if ctx.rules:
        informal = ("- Informal writing (the paths of `informal.txt`) is "
                    "tagged with `%s`, whose\n  user map adds the chat "
                    "readings (q as que, x as por, tas as estás ...).\n  How "
                    "the texts are tagged:\n\n" % fl.config(fc.INFORMAL_CONFIG))
        informal += "".join("  - %s, %s text(s): `%s`\n" % (how, f"{n:,}", f)
                            for f, how, n in ctx.branches) + "\n"
    if a.only or a.limit:
        if (out_root / "README.md").is_file():
            fc.log("stage README kept as it was (--only and --limit see only "
                   "part of the corpus)")
            return
    docs = len(fc.corpus_files(out_root, ".conll"))
    fc.write_readme(out_root, STAGE_060_README.format(
        name=ctx.name, version=VERSION, date=time.strftime("%Y-%m-%d"),
        docs=f"{docs:,}", ext=a.ext, kind=ctx.kind,
        config=fl.config(base_cfg), informal=informal, dep=a.dep,
        standins=", ".join(f for f, _ in sender.standins),
        command=ctx.command, corpus=ctx.name))
    fc.log("stage README: %s" % (out_root / "README.md"))


# ---------------------------------------------------------------------------
def main(argv=None):
    a = parse(sys.argv[1:] if argv is None else argv)
    fc.set_colour(not a.no_colour and sys.stdout.isatty()
                  and os.environ.get("NO_COLOR") is None)
    if a.version:
        print("%s %s" % (PROG, VERSION))
        return 0
    steps = [n for n in fc.STEP_ORDER if getattr(a, "step_" + n)]
    setup = bool(a.new or a.link_stage)
    if a.help or (not steps and not setup and not a.list):
        print(help_text())
        if not a.help and a.corpus:
            fc.log(fc.red("REFUSED: name at least one step"))
            return 2
        return 0
    home = fc.release_home(Path(__file__), a.home)
    if home is None:
        fc.log(fc.red("REFUSED: this script is not in the software/ folder of "
                      "the release; give --home DIR"))
        return 2
    if a.list:
        return do_list(home)
    if setup:
        if steps:
            fc.log(fc.red("REFUSED: set the corpus up first (--new, "
                          "--link-stage), then run the steps"))
            return 2
        return do_setup(a, home)
    p = fc.name_problem(a.corpus or "")
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    cdir = fc.corpora_dir(home) / a.corpus
    W = 78
    fc.log("=" * W)
    fc.log("FREELING  %s  (%s)%s" % (VERSION, fc.RELEASE,
                                     "   DRY RUN" if a.dry_run else ""))
    fc.log("=" * W)
    fc.log("corpus : %s" % cdir)
    if not cdir.is_dir():
        fc.log(fc.red("REFUSED: no such corpus folder (make it: freeling.py "
                      "--new %s --kind KIND --input DIR)" % a.corpus))
        return 2
    kind, root, p = fc.corpus_input(cdir)
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    fc.log("kind   : %s (%s)" % (kind, fc.KIND_TEXT[kind]))
    fc.log("input  : %s -> %s" % (root, root.resolve()))
    if (cdir / fc.INFORMAL_LIST).exists() and kind != "written-modern":
        fc.log(fc.red("REFUSED: %s is there, but informal writing is only "
                      "for written-modern; this corpus is %s. Take the file "
                      "away." % (cdir / fc.INFORMAL_LIST, kind)))
        return 2
    rules, p = fc.load_informal(cdir, root)
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    if rules:
        fc.log("informal: %d path(s) in %s; every other text is formal"
               % (len(rules), cdir / fc.INFORMAL_LIST))
    if "080" in steps and kind == "written-old":
        fc.log(fc.red("REFUSED: --perkins is not for written-old: Perkins "
                      "transcribes modern Spanish"))
        return 2
    # Every step needs its earlier stages, made before or in this run.
    missing = []
    for n in steps:
        need = [r for r in fc.REQUIRES[n]
                if r not in steps and not fc.stage_made(cdir, r)]
        if need:
            missing.append((n, need))
    if missing:
        for n, need in missing:
            fc.log(fc.red("REFUSED: %s (%s) needs %s, not made yet. Make %s "
                          "first, or name %s in the same run."
                          % (fc.STAGES[n][1], fc.STAGES[n][0],
                             ", ".join(fc.STAGES[r][0] for r in fc.REQUIRES[n]),
                             ", ".join(fc.STAGES[r][0] for r in need),
                             " ".join(fc.STAGES[r][1] for r in need))))
        return 2
    fl = fc.FreeLing(a.freeling_bin, a.share, a.lib)
    if "060" in steps:
        probs = fl.problems()
        if probs:
            for p in probs:
                fc.log(fc.red("REFUSED: %s" % p))
            return 2
    ctx = Ctx(a, home, cdir, kind, root, fl, rules)
    fc.log("steps  : %s" % " ".join(fc.STAGES[n][1] for n in steps))
    blockers = fc.run_blockers(cdir, steps)
    if blockers:
        fc.log(fc.red("REFUSED: %d file(s) this run rewrites cannot be "
                      "replaced (immutable or read-only):" % len(blockers)))
        for p, why in blockers:
            fc.log("   %s  %s" % (why, p))
        for line in fc.unlock_lines([p for p, _ in blockers]):
            fc.log(line)
        return 2
    if not a.dry_run:
        fc.ensure_corpus_readmes(home, cdir, kind, root, rules)
    results = []
    rc = 0
    for n in steps:
        if n == "060":
            r = step_freeling(ctx)
        elif n == "070":
            import freeling_ud
            r = freeling_ud.run(ctx)
        elif n == "080":
            import freeling_perkins
            r = freeling_perkins.run(ctx)
        else:
            import freeling_parquet
            r = freeling_parquet.run(ctx)
        results.append((n, r))
        rc = max(rc, r) if r != 130 else 130
        if r not in (0, 1) or STOP.is_set():
            break
        if a.dry_run and n != steps[-1]:
            fc.log(fc.orange("DRY RUN: the steps after %s are checked against "
                             "the stages as they are now" % fc.STAGES[n][1]))
    fc.log("=" * W)
    for n, r in results:
        fc.log("%-10s %s  exit %d" % (fc.STAGES[n][1], fc.STAGES[n][0], r))
    if not a.dry_run:
        rec = fc.ensure_records(cdir)
        fc.put_file("command\t%s\nversion\t%s\n" % (ctx.command, VERSION) +
                    "".join("%s\t%s\texit %d\n" % (fc.STAGES[n][1],
                                                   fc.STAGES[n][0], r)
                            for n, r in results),
                    fc.free_name(rec, "freeling-run--%s" % ctx.stamp))
    else:
        fc.log(fc.orange("DRY RUN -- nothing written."))
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.stderr.write("\ninterrupted\n")
        sys.exit(130)
