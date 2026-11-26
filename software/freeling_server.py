#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.0.0
#
# freeling_server.py -- starts FreeLing's analyzer as a server with the
# FreeLing es-CL 2027 config for a kind of text, and keeps it up until
# Ctrl-C, then stops it with every analyzer it started. While it is up,
# freeling_analyzer.py --port N sends texts to it, and freeling.py --freeling
# --use-running-server tags a corpus through it. Loading FreeLing takes
# minutes and about 2 GB (the dictionary, the name classifier, the LSTM
# parser, UKB); a server pays that once.
#
#     freeling_server.py --kind speech
#     freeling_server.py --kind written-modern --informal --port 50006
#     freeling_server.py --stop --port 50005
#
# It runs in the foreground: start it in its own terminal (or tmux, byobu,
# screen tab). Linux and macOS. Python 3.9 or later, standard library only.

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import freeling_common as fc                                # noqa: E402

VERSION = "1.0.0"
__version__ = VERSION


def server_groups(port):
    """The process groups of the FreeLing servers on port: every analyze or
    analyzer process started with --server and --port PORT (FreeLing's own
    "analyze stop" wants the process id, not the port)."""
    r = subprocess.run(["ps", "-axo", "pid=,pgid=,command="],
                       capture_output=True, text=True)
    groups = set()
    for line in r.stdout.splitlines():
        f = line.split(None, 2)
        if len(f) < 3:
            continue
        words = f[2].split()
        if not any(Path(w).name in ("analyze", "analyzer") for w in words[:2]):
            continue
        if "--server" in words and "--port" in words:
            i = words.index("--port")
            if i + 1 < len(words) and words[i + 1] == str(port):
                groups.add(int(f[1]))
    return sorted(groups)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_server.py",
        description="Start FreeLing's analyzer as a server with the FreeLing "
                    "es-CL 2027 config of a kind of text; Ctrl-C stops it.")
    ap.add_argument("--kind", choices=fc.KINDS,
                    help="the kind of text: %s" % ", ".join(fc.KINDS))
    ap.add_argument("--informal", action="store_true",
                    help="informal modern writing (chat, forums, e-mail): "
                         "the config es-cl-informal.cfg; written-modern only")
    ap.add_argument("--port", type=int, default=50005)
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 8,
                    help="analyzers working at once (default: every logical "
                         "CPU, %(default)s here)")
    ap.add_argument("--dep", default="lstm", choices=("lstm", "treeler", "txala"))
    ap.add_argument("--startup-timeout", type=int, default=600)
    ap.add_argument("--stop", action="store_true",
                    help="stop the FreeLing server on --port, with every "
                         "analyzer it started")
    ap.add_argument("--log", metavar="FILE",
                    help="the server's log (default: freeling-server--PORT.log "
                         "in the current folder)")
    ap.add_argument("--freeling-bin")
    ap.add_argument("--share")
    ap.add_argument("--lib")
    ap.add_argument("--dry-run", action="store_true",
                    help="check the config and print the command; start nothing")
    ap.add_argument("--version", action="version",
                    version="freeling_server.py " + VERSION)
    a = ap.parse_args(argv)
    fc.set_colour(sys.stdout.isatty() and os.environ.get("NO_COLOR") is None)
    fl = fc.FreeLing(a.freeling_bin, a.share, a.lib)
    for p in fl.problems():
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    if a.stop:
        if not fc.port_open(a.port):
            fc.log("nothing is listening on port %d" % a.port)
            return 0
        groups = server_groups(a.port)
        if not groups:
            fc.log(fc.red("port %d is in use, but not by a FreeLing server "
                          "(no analyze or analyzer with --server --port %d)"
                          % (a.port, a.port)))
            return 1
        for sig, wait in ((signal.SIGTERM, 30), (signal.SIGKILL, 10)):
            for g in groups:
                try:
                    os.killpg(g, sig)
                except (ProcessLookupError, PermissionError):
                    pass
            t0 = time.time()
            while time.time() - t0 < wait and fc.port_open(a.port):
                time.sleep(0.5)
            if not fc.port_open(a.port):
                break
        if fc.port_open(a.port):
            fc.log(fc.red("port %d is still in use" % a.port))
            return 1
        fc.log(fc.green("stopped the server on port %d" % a.port))
        return 0
    if not a.kind:
        fc.log(fc.red("REFUSED: --kind is required (%s)" % ", ".join(fc.KINDS)))
        return 2
    if a.informal and a.kind != "written-modern":
        fc.log(fc.red("REFUSED: --informal is for written-modern only"))
        return 2
    cfg = fc.INFORMAL_CONFIG if a.informal else fc.CONFIGS[a.kind]
    sender, problems, notes = fc.make_sender(fl, HERE, [cfg], a.dep)
    for n in notes:
        fc.log(n)
    p2, n2 = fc.library_checks(fl.lib, cfg in fc.NP_FILES)
    for n in n2:
        fc.log("library: %s" % n)
    for p in problems + p2:
        fc.log(fc.red("REFUSED: %s" % p))
    if problems or p2:
        return 2
    if fc.port_open(a.port):
        fc.log(fc.red("REFUSED: port %d is already in use" % a.port))
        return 2
    cmd = fc.server_command(fl, cfg, a.dep, a.port, a.workers)
    fc.log("server : %s" % " ".join(cmd))
    if a.dry_run:
        fc.log(fc.orange("DRY RUN -- nothing started."))
        return 0
    logp = Path(a.log) if a.log else Path.cwd() / ("freeling-server--%d.log" % a.port)
    fc.log("log    : %s" % logp)
    proc, problem = fc.start_server(cmd, logp, a.port, a.startup_timeout)
    if problem:
        fc.log(fc.red("STOPPED: %s" % problem))
        return 3
    fc.log(fc.green("up on port %d with %d worker(s). Send texts with:" % (a.port, a.workers)))
    fc.log("   freeling_analyzer.py --kind %s%s --port %d TEXT.txt"
           % (a.kind, " --informal" if a.informal else "", a.port))
    fc.log("Ctrl-C stops the server.")
    done = threading.Event()

    def _stop(sig, frm):                                    # noqa: ARG001
        done.set()
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    while not done.is_set():
        if proc.poll() is not None:
            fc.log(fc.red("STOPPED: the server exited; see %s" % logp))
            return 3
        done.wait(2.0)
    fc.log("stopping ...")
    fc.stop_server(proc)
    if fc.port_open(a.port):
        fc.log(fc.red("port %d is still in use" % a.port))
        return 1
    fc.log(fc.green("stopped"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
