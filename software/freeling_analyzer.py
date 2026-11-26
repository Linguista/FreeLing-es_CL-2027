#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.0.0
#
# freeling_analyzer.py -- analyzes texts with FreeLing es-CL 2027, on its
# own or through a server started by freeling_server.py, and writes the
# same TAB-separated CoNLL as freeling.py: the stand-in tokens sent in lower
# case and written back in FORM, the three rewritten spellings, the commas
# of the comma multiwords sent as blanks, every character offset exact.
#
#     freeling_analyzer.py --kind speech interview.txt
#     freeling_analyzer.py --kind written-modern --informal chat.txt --out chat.conll
#     echo "¿Cachái lo que te digo?" | freeling_analyzer.py --kind written-modern
#     freeling_analyzer.py --kind speech --port 50005 a.txt b.txt --out-dir tagged
#
# On its own it starts FreeLing for each run (minutes, for the models); for
# many texts start freeling_server.py once and give --port. The kind must be
# the one the server was started with.
#
# Linux and macOS. Python 3.9 or later, standard library only.

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import freeling_common as fc                                # noqa: E402

VERSION = "1.0.0"
__version__ = VERSION


def analyze_alone(fl, cfg, dep, data, timeout):
    cmd = fc.server_command(fl, cfg, dep, 0, 0)
    try:
        r = subprocess.run(cmd, input=data, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timeout after %ds" % timeout
    if r.returncode != 0:
        err = " ".join((r.stderr or b"").decode("utf-8", "replace").split())
        return None, "analyze exit %d: %s" % (r.returncode, err[-300:])
    return r.stdout, None


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_analyzer.py",
        description="Analyze texts with FreeLing es-CL 2027, on its own or "
                    "through freeling_server.py (--port).")
    ap.add_argument("texts", nargs="*", help="text files (UTF-8, one sentence "
                    "or utterance per line); none: standard input")
    ap.add_argument("--kind", choices=fc.KINDS, required=True)
    ap.add_argument("--informal", action="store_true",
                    help="informal modern writing: es-cl-informal.cfg")
    ap.add_argument("--port", type=int, default=0,
                    help="send to the server on this port instead of starting "
                         "FreeLing")
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--out", metavar="FILE",
                    help="write here (one text only; default: standard output)")
    ap.add_argument("--out-dir", metavar="DIR",
                    help="write NAME.conll for each NAME.txt into this folder")
    ap.add_argument("--dep", default="lstm", choices=("lstm", "treeler", "txala"))
    ap.add_argument("--timeout", type=int, default=3600)
    ap.add_argument("--freeling-bin")
    ap.add_argument("--share")
    ap.add_argument("--lib")
    ap.add_argument("--version", action="version",
                    version="freeling_analyzer.py " + VERSION)
    a = ap.parse_args(argv)
    fc.set_colour(sys.stderr.isatty() and os.environ.get("NO_COLOR") is None)
    if a.informal and a.kind != "written-modern":
        sys.stderr.write("REFUSED: --informal is for written-modern only\n")
        return 2
    if a.out and len(a.texts) > 1:
        sys.stderr.write("REFUSED: --out takes one text; give --out-dir\n")
        return 2
    fl = fc.FreeLing(a.freeling_bin, a.share, a.lib)
    probs = fl.problems()
    cfg = fc.INFORMAL_CONFIG if a.informal else fc.CONFIGS[a.kind]
    sender, p2, notes = fc.make_sender(fl, HERE, [cfg], a.dep)
    p3, _n = fc.library_checks(fl.lib, cfg in fc.NP_FILES)
    for p in probs + p2 + p3:
        sys.stderr.write("REFUSED: %s\n" % p)
    if probs or p2 or p3:
        return 2
    if a.port and not fc.port_open(a.port):
        sys.stderr.write("REFUSED: nothing is listening on port %d (start "
                         "freeling_server.py --kind %s --port %d)\n"
                         % (a.port, a.kind, a.port))
        return 2
    inputs = [(Path(t), Path(t).read_bytes()) for t in a.texts] if a.texts \
        else [(None, sys.stdin.buffer.read())]
    rc = 0
    for path, data in inputs:
        send, state, problem = sender.prepare(data)
        if not problem:
            if a.port:
                out, problem = fc.analyze_through_server(fl, a.host, a.port, send,
                                                         a.timeout)
            else:
                out, problem = analyze_alone(fl, cfg, a.dep, send, a.timeout)
        if not problem:
            conll, _ntok, problem = sender.finish(out, state)
        if problem:
            sys.stderr.write("FAILED %s: %s\n" % (path or "standard input", problem))
            rc = 1
            continue
        if a.out_dir and path is not None:
            dst = Path(a.out_dir) / (path.stem + ".conll")
            fc.put_file(conll.decode("utf-8"), dst)
            sys.stderr.write("%s\n" % dst)
        elif a.out:
            fc.put_file(conll.decode("utf-8"), Path(a.out))
        else:
            sys.stdout.buffer.write(conll)
            sys.stdout.flush()
    return rc


if __name__ == "__main__":
    sys.exit(main())
