#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.3.0
#
# freeling_common.py -- what freeling.py, freeling_server.py,
# freeling_analyzer.py and the steps of freeling.py share (FreeLing es-CL
# 2027): where FreeLing and its data are, the kinds of text and their
# configs, the corpus folders, the stand-in tokens, the spellings rewritten
# on the way to FreeLing, the server, and the files every stage carries
# (README.md and columns.tsv). It is a module: it does nothing when run.
#
# Linux and macOS. Python 3.9 or later, standard library only.

from __future__ import annotations

import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import threading
import time
import unicodedata
from pathlib import Path

VERSION = "1.3.0"
__version__ = VERSION
RELEASE = "FreeLing es-CL 2027"

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8", line_buffering=True)
        except Exception:                                   # noqa: BLE001
            pass

# ---------------------------------------------------------------------------
# The kinds of text, and the config each is tagged with. Old Spanish is
# FreeLing Old (es-old.cfg) exactly as FreeLing ships it.
KINDS = ("speech", "written-modern", "written-19th-century", "written-old")
KIND_TEXT = {
    "speech": "transcribed speech, one utterance per line",
    "written-modern": "modern writing (informal writing too: see informal.txt)",
    "written-19th-century": "19th-century writing",
    "written-old": "Old Spanish (medieval and Golden Age texts), FreeLing Old",
}
CONFIGS = {"speech": "es-cl-speech.cfg", "written-modern": "es-cl.cfg",
           "written-19th-century": "es-cl-19th-century.cfg",
           "written-old": "es-old.cfg"}
INFORMAL_CONFIG = "es-cl-informal.cfg"
# The name recognizer each FreeLing es-CL 2027 config must name.
NP_FILES = {"es-cl-speech.cfg": "es/es-cl/np-speech.dat",
            "es-cl.cfg": "es/es-cl/np.dat",
            "es-cl-informal.cfg": "es/es-cl/np.dat"}
# The configs written by FreeLing es-CL 2027 (they have its user maps);
# es-old.cfg is FreeLing's own and has none.
ESCL_CONFIGS = ("es-cl.cfg", "es-cl-informal.cfg", "es-cl-speech.cfg",
                "es-cl-19th-century.cfg")
COLUMNS_CFG = "es-cl-conll-columns.cfg"
STANDINS_FILE = "es/es-cl/stand-ins.tsv"
INFORMAL_USERMAP = "es/es-cl/usermap-informal.dat"
COMMA_MULTIWORDS = "freeling_comma_multiwords.txt"

# ---------------------------------------------------------------------------
# The corpus folders. corpora/ beside software/ and data/ in the release
# folder (it may be a real folder or a link to one); one folder per corpus.
CORPORA = "corpora"
RESERVED_NAMES = ("data", "software", "packaging", "corpora")
INPUT = "input"
INFORMAL_LIST = "informal.txt"
RECORDS = "_processing-records"
COLUMNS_TSV = "columns.tsv"
SIDECAR = ".times.tsv"

# The stages: number, folder, the option of freeling.py that makes it, what
# it is, and the stages it needs. Fixed for every corpus.
STAGES = {
    "060": ("060-FreeLing-Tagged", "--freeling",
            "FreeLing 4.2 with FreeLing es-CL 2027: lemma, part of speech, "
            "word sense and dependency parse of every token"),
    "070": ("070-Universal-Dependency-Tagged", "--ud",
            "Universal Dependencies part of speech (UPOS) and features "
            "(FEATS), translated from FreeLing's tags"),
    "080": ("080-Perkins-Tagged", "--perkins",
            "Perkins: phonological transcriptions of every token, one "
            "column per set of Perkins options (not for written-old)"),
    "400": ("400-Parquet", "--parquet",
            "a Parquet token store of the last stage made (080, 070 or "
            "060), for DuckDB, Python or R"),
}
REQUIRES = {"060": (), "070": ("060",), "080": ("060", "070"),
            "400": ("060",)}
STEP_ORDER = ("060", "070", "080", "400")
RESERVED_STAGES = (
    ("090", "topic analyses"),
    ("100", "sentiment analyses"),
    ("110", "emotion analyses"),
    ("120, 130, 140 ...", "further analyses"),
    ("500-Database", "your own database tables and their Parquet copies"),
)

_C = [False]


def set_colour(on: bool):
    _C[0] = bool(on)


def red(t):
    return "\033[1;31m%s\033[0m" % t if _C[0] else str(t)


def orange(t):
    return "\033[1;33m%s\033[0m" % t if _C[0] else str(t)


def green(t):
    return "\033[32m%s\033[0m" % t if _C[0] else str(t)


def log(*a):
    print(*a, flush=True)          # every line flushed: this runs behind tee


def hms(sec):
    sec = int(max(sec, 0))
    return "%d:%02d:%02d" % (sec // 3600, (sec % 3600) // 60, sec % 60)


def human(n):
    for u in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or u == "TB":
            return "%.1f %s" % (n, u)
        n /= 1024.0
    return "%d B" % n


def unlink_quietly(path):
    try:
        path.unlink()
    except OSError:
        pass


def put_file(text_or_src, dst: Path):
    """Write text (str) or copy a file (Path) to dst through dst.part,
    renamed into place: a stopped run leaves no half file."""
    part = dst.with_name(dst.name + ".part")
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(text_or_src, Path):
            shutil.copy2(text_or_src, part)
        else:
            with open(part, "w", encoding="utf-8", newline="\n") as w:
                w.write(text_or_src)
        os.replace(part, dst)
    except BaseException:
        unlink_quietly(part)
        raise


def free_name(folder: Path, stem: str, ext: str = ".tsv") -> Path:
    """folder/stem.tsv, or stem-2.tsv, stem-3.tsv ... if that is taken."""
    path, n = folder / (stem + ext), 2
    while path.exists():
        path, n = folder / ("%s-%d%s" % (stem, n, ext)), n + 1
    return path


def locked(path: Path):
    """Why path cannot be replaced (immutable or read-only), or None.
    Opening for append changes nothing and fails where a rename would."""
    if not path.exists():
        return None
    try:
        with open(path, "ab"):
            pass
    except OSError as exc:
        return exc.strerror or str(exc)
    return None


def run_blockers(cdir: Path, steps):
    """[(path, why)]: the files a run of these steps rewrites that cannot be
    replaced (immutable or read-only): the corpus folder's README, and the
    README and columns.tsv of each step's stage. Checked by the dry run and
    by the run, before anything is written."""
    paths = [cdir / "README.md"]
    for num in steps:
        st = stage_path(cdir, num)
        paths += [st / "README.md", st / COLUMNS_TSV]
    out = []
    for p in paths:
        why = locked(p)
        if why:
            out.append((p, why))
    return out


def unlock_lines(paths, where=None):
    """The lines that say how the flag is cleared: one command that names
    each file, never a folder. Past 50 files, the command that lists them."""
    paths = [str(p) for p in paths]
    lines = ["   This tool never clears the flag. If these files are to be "
             "replaced, clear it on exactly them:"]
    if len(paths) <= 50:
        lines.append("   sudo chattr -i %s" % " ".join('"%s"' % p for p in paths))
    else:
        lines.append("   (%d files; list them with:  find -L \"%s\" -type f "
                     "-exec lsattr {} + | grep -- \"----i\")"
                     % (len(paths), where if where else Path(paths[0]).parent))
    return lines


# ---------------------------------------------------------------------------
# Where things are.
def release_home(script: Path, override=None):
    """The release folder: --home, or the folder holding the software/
    folder this script is in. None if neither."""
    if override:
        return Path(override).expanduser().resolve()
    here = script.resolve().parent
    if here.name == "software":
        return here.parent
    return None


def own_freeling():
    """The bin folder of a FreeLing installed for this release alone: in
    third-party/freeling/ of the folder that holds these tools, or that
    holds the release folder's parent. None when there is none."""
    here = Path(__file__).resolve().parent
    for base in (here.parent, here.parent.parent.parent):
        b = base / "third-party" / "freeling" / "bin"
        if (b / "analyze").is_file():
            return b
    return None


class FreeLing:
    """The installed FreeLing: its programs, its data folder and library.
    Without --freeling-bin, the release's own FreeLing when there is one
    (own_freeling), else the one on the PATH."""

    def __init__(self, bindir=None, share=None, lib=None):
        if bindir:
            b = Path(bindir).expanduser().resolve()
            self.analyze = str(b / "analyze")
            self.client = str(b / "analyzer_client")
        elif own_freeling():
            self.analyze = str(own_freeling() / "analyze")
            self.client = str(own_freeling() / "analyzer_client")
        else:
            self.analyze = shutil.which("analyze") or "/usr/local/bin/analyze"
            self.client = (shutil.which("analyzer_client")
                           or "/usr/local/bin/analyzer_client")
        prefix = Path(self.analyze).resolve().parent.parent
        self.share = (Path(share).expanduser().resolve() if share
                      else prefix / "share" / "freeling")
        if lib:
            self.lib = Path(lib).expanduser().resolve()
        else:
            self.lib = prefix / "lib" / "libfreeling.so"
            for cand in (prefix / "lib64" / "libfreeling.so",
                         prefix / "lib" / "libfreeling.dylib"):
                if not self.lib.exists() and cand.exists():
                    self.lib = cand

    def config(self, name: str) -> Path:
        return self.share / "config" / name

    def expand(self, value: str) -> Path:
        """A path from a config, with $FREELINGSHARE expanded."""
        v = value.split("#", 1)[0].strip()
        return Path(v.replace("$FREELINGSHARE", str(self.share)))

    def problems(self):
        out = []
        for p in (self.analyze, self.client):
            if not Path(p).exists():
                out.append("not found: %s (give --freeling-bin DIR)" % p)
        if not (self.share / "config").is_dir():
            out.append("not a FreeLing data folder: %s (give --share DIR)"
                       % self.share)
        return out


def config_values(cfg: Path):
    """The settings of a FreeLing config: name -> value (the last one)."""
    vals = {}
    for line in cfg.read_text(encoding="utf-8", errors="replace").splitlines():
        t = line.strip()
        if not t or t.startswith(("#", "<", "[")) or "=" not in t:
            continue
        k, v = t.split("=", 1)
        vals[k.strip()] = v.strip()
    return vals


def conll_columns(path: Path):
    """(names, problem): the <Columns> list of a CoNLL columns file."""
    if not path.is_file():
        return None, "the CoNLL columns file is missing: %s" % path
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"<Columns>(.*?)</Columns>", text, re.S)
    if not m or not m.group(1).split():
        return None, ("no <Columns> section in %s (FreeLing would silently "
                      "use its default columns)" % path)
    return m.group(1).split(), None


# What the library with the name-class change holds and FreeLing 4.2 does
# not: the section names it reads and the keep: option of
# <SentenceStartClasses> (wide strings, UTF-32 little-endian on Linux).
NP_CLASS_MARKS = [s.encode("utf-32-le") for s in
                  ("DictionaryClasses", "FixedClasses",
                   "ClassesAtSentenceStart", "SentenceStartClasses",
                   "ClassShares", "keep:")]
# What the library with the known-roots change exports: the affix methods
# with their new parameters.
KNOWN_ROOTS_MARKS = [
    re.compile(rb"_ZNK8freeling7affixes25look_for_combined_affixes"
               rb"[A-Za-z0-9_]*RNS_4wordERKSt3set"),
    re.compile(rb"_ZNK8freeling7affixes15SearchRootsList"
               rb"[A-Za-z0-9_]*RNS_4wordESE_")]


# What the library with the tag-probabilities change holds: the names of
# its two CoNLL columns.
PROBABILITY_COLUMNS = ("LEX_PROB", "TAG_PROB")
TAG_PROB_MARKS = [s.encode("utf-32-le") for s in PROBABILITY_COLUMNS]


def probability_columns_check(lib: Path, columns):
    """(problem, note), either None: when the columns file names LEX_PROB or
    TAG_PROB, the FreeLing library must have the tag-probabilities change
    (software/patches/). FreeLing without it does not know the two names."""
    named = [c for c in columns if c in PROBABILITY_COLUMNS]
    if not named or not lib.is_file():
        return None, None
    data = lib.resolve().read_bytes()
    missing = [m.decode("utf-32-le") for m in TAG_PROB_MARKS if m not in data]
    if missing:
        return ("%s does not write the probability columns (no %s), which "
                "the columns file names (%s): install FreeLing with the "
                "changes in software/patches/"
                % (lib, ", ".join(missing), ", ".join(named))), None
    return None, "%s writes the probability columns" % lib


def library_checks(lib: Path, need_names: bool):
    """(problems, notes): the FreeLing library has the changes of FreeLing
    es-CL 2027 (software/patches/): the known roots of the affix analysis
    always; the name classes when need_names."""
    if not lib.is_file():
        return ["the FreeLing library is not there: %s (give --lib FILE)"
                % lib], []
    data = lib.resolve().read_bytes()
    problems, notes = [], []
    if all(m.search(data) for m in KNOWN_ROOTS_MARKS):
        notes.append("%s has the known-roots change" % lib)
    else:
        problems.append("%s has not the known-roots change of the affix "
                        "analysis (reirse would be read reir + se): install "
                        "FreeLing with the changes in software/patches/" % lib)
    if need_names:
        missing = [m.decode("utf-32-le") for m in NP_CLASS_MARKS
                   if m not in data]
        if missing:
            problems.append("%s does not read the name classes (no %s): "
                            "install FreeLing with the changes in "
                            "software/patches/" % (lib, ", ".join(missing)))
        else:
            notes.append("%s reads the name classes" % lib)
    return problems, notes


# ---------------------------------------------------------------------------
# The stand-in tokens.
STANDIN_SHAPE = re.compile(r"XXX[A-Z]+XXX")


def load_standins(fl: FreeLing):
    """(standins, problem): [(form, tag, meaning)] from the installed
    stand-ins.tsv."""
    path = fl.share / STANDINS_FILE
    if not path.is_file():
        return None, ("%s is missing: FreeLing es-CL 2027 is not installed "
                      "(or an older release is)" % path)
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f = line.split("\t")
        if not rows and f[:3] == ["form", "tag", "meaning"]:
            rows.append(None)                # the header
            continue
        if len(f) < 3 or not STANDIN_SHAPE.fullmatch(f[0]) or not f[1]:
            return None, "%s line %d: form<TAB>tag<TAB>meaning expected" % (
                path, n)
        rows.append((f[0], f[1], f[2]))
    rows = [r for r in rows if r]
    if not rows:
        return None, "%s lists no stand-in" % path
    return rows, None


def usermap_problem(fl: FreeLing, cfg: Path, standins):
    """What is wrong with the user map of a FreeLing es-CL 2027 config, or
    None: it must be on and map every stand-in, lowercased."""
    v = config_values(cfg)
    if v.get("UserMap", "").lower() != "yes" or "UserMapFile" not in v:
        return "no UserMap=yes and UserMapFile in %s" % cfg
    path = fl.expand(v["UserMapFile"])
    if not path.is_file():
        return "the user map is missing: %s" % path
    keys = {l.split()[0] for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.lstrip().startswith("#")}
    missing = [f.lower() for f, _, _ in standins if "^%s$" % f.lower() not in keys]
    if missing:
        return "%s does not map %s" % (path, ", ".join(missing))
    return None


def informal_problem(fl: FreeLing, cfg: Path):
    """The informal config's user map must hold every line of the
    installed usermap-informal.dat (a config older than the data would tag
    with old informal readings)."""
    installed = fl.share / INFORMAL_USERMAP
    if not installed.is_file():
        return "%s is missing" % installed
    v = config_values(cfg)
    path = fl.expand(v.get("UserMapFile", ""))
    if not path.is_file():
        return "the user map of %s is missing: %s" % (cfg, path)
    want = [l for l in installed.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    have = set(path.read_text(encoding="utf-8").splitlines())
    lack = [l for l in want if l not in have]
    if lack:
        return ("%s lacks %d of the %d line(s) of %s (the first: %s): "
                "redeploy FreeLing es-CL 2027" % (path, len(lack), len(want),
                                                   installed, lack[0]))
    return None


def check_config(fl: FreeLing, cfg_name: str, standins, dep: str,
                 informal=False):
    """(problems, notes) for one config, before any work."""
    cfg = fl.config(cfg_name)
    if not cfg.is_file():
        return ["the config is missing: %s" % cfg], []
    problems, notes = [], ["config : %s" % cfg]
    text = cfg.read_text(encoding="utf-8", errors="replace")
    # A non-ASCII character anywhere in a config makes FreeLing segfault,
    # with a stack trace naming neither file nor line.
    bad = [i for i, l in enumerate(text.splitlines(), 1)
           if any(ord(c) > 126 for c in l)]
    if bad:
        problems.append("non-ASCII character in %s at line(s) %s: FreeLing "
                        "stops on it" % (cfg, ", ".join(map(str, bad[:10]))))
    v = config_values(cfg)
    d = v.get("DictionaryFile")
    if not d or not fl.expand(d).is_file():
        problems.append("the dictionary of %s is missing: %s"
                        % (cfg, fl.expand(d) if d else "no DictionaryFile"))
    else:
        notes.append("dict   : %s" % fl.expand(d))
    if cfg_name in NP_FILES:
        want = NP_FILES[cfg_name]
        np_ = v.get("NPDataFile", "")
        if not np_.endswith(want):
            problems.append("%s names the name recognizer %s, not %s"
                            % (cfg, np_ or "(none)", want))
        elif not fl.expand(np_).is_file():
            problems.append("the name recognizer is missing: %s"
                            % fl.expand(np_))
    if cfg_name in ESCL_CONFIGS:
        p = usermap_problem(fl, cfg, standins)
        if p:
            problems.append(p)
        if v.get("CompoundAnalysis", "").lower() != "no":
            problems.append("%s has compound analysis on: FreeLing es-CL "
                            "2027 turns it off" % cfg)
    if informal:
        p = informal_problem(fl, cfg)
        if p:
            problems.append(p)
    if dep == "lstm" and cfg_name != "es-old.cfg" and "DepLSTMFile" not in v:
        problems.append("%s has no DepLSTMFile: the LSTM parser would give "
                        "no parse and no error" % cfg)
    return problems, notes


def server_command(fl: FreeLing, cfg_name: str, dep: str, port: int,
                   workers: int):
    """The command that starts FreeLing's server for a config. Every
    setting the output depends on is on the command line: FreeLing 4.2's
    analyzer ignores OutputLevel in a config."""
    cmd = [fl.analyze, "-f", str(fl.config(cfg_name)), "--flush",
           "--output", "conll", "--oconll", str(fl.config(COLUMNS_CFG))]
    if cfg_name == "es-old.cfg":
        cmd += ["--outlv", "tagged"]         # FreeLing Old has no parser
    else:
        cmd += ["--outlv", "dep", "--dep", dep]
    if port:
        cmd += ["--server", "--port", str(port), "--workers", str(workers),
                "--queue", str(workers * 4)]
    return cmd


# ---------------------------------------------------------------------------
# What is done to a text on the way to FreeLing. The text files are never
# changed; every replacement keeps the text's length, so every character
# offset FreeLing reports is an offset in the source.
_NOT_AFTER_WORD = r"(?<![^\W_])"
_NOT_BEFORE_WORD = r"(?![^\W_])"


def _weon(m):
    t = m.group(0)
    if all(c.isupper() for c in t if c.isalpha()):
        return "WEÓN"
    return "Weón" if t[0].isupper() else "weón"


PREFILTERS = [
    ("Bs. As.", re.compile(_NOT_AFTER_WORD + r"[Bb][Ss]\.[ \t]?[Aa][Ss]\."),
     lambda m: "BsAs"),
    ("wo'n", re.compile(_NOT_AFTER_WORD + "[Ww][Ee]?[Oo]['’´`][Nn]"
                        + _NOT_BEFORE_WORD), _weon),
    ("pa'l", re.compile(_NOT_AFTER_WORD + "([Pp])([Aa])['’´`]([Ll])"
                        + _NOT_BEFORE_WORD),
     lambda m: m.group(1) + m.group(2) + m.group(3)),
]
COMMA_NAME = "comma multiwords"


def load_comma_multiwords(path: Path):
    """((name, pattern, replacement), number of phrases), or (None,
    problem): the commas of the multiwords written with one, sent to
    FreeLing as blanks."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return None, "%s: %s" % (path, exc)
    phrases = []
    for n, line in enumerate(lines, 1):
        t = unicodedata.normalize("NFC", line.strip())
        if not t or t.startswith("#"):
            continue
        if "," not in t:
            return None, "%s line %d has no comma: %s" % (path, n, t)
        phrases.append(t)
    if not phrases:
        return None, "%s lists no phrase" % path
    alts = []
    for t in sorted(set(phrases), key=len, reverse=True):
        parts = [p.split() for p in re.split(r"\s*,\s*", t)]
        alts.append(r"[ \t]*,[ \t]*".join(
            r"[ \t]+".join(re.escape(w) for w in p) for p in parts))
    pat = re.compile(_NOT_AFTER_WORD + "(?:" + "|".join(alts) + ")"
                     + _NOT_BEFORE_WORD, re.IGNORECASE)
    return (COMMA_NAME, pat, lambda m: m.group(0).replace(",", " ")), len(phrases)


class Sender:
    """Turns a source text into what FreeLing is sent, and FreeLing's
    output back into the stage's CoNLL: the stand-ins, the rewritten
    spellings, the commas of the comma multiwords, and the tabs."""

    def __init__(self, standins, filters, columns, usermap: bool):
        self.standins = sorted(((f, f.lower()) for f, _, _ in standins),
                               key=lambda x: -len(x[0]))
        self.filters = filters
        self.columns = columns
        self.ncols = len(columns)
        self.srl_last = columns[-1] == "SRL"
        self.form_i = columns.index("FORM")
        self.span_i = tuple(columns.index(c) if c in columns else -1
                            for c in ("SPAN_BEGIN", "SPAN_END"))
        self.usermap = usermap
        self.counts = {name: 0 for name, _, _ in filters}
        self.lock = threading.Lock()

    def prepare(self, data: bytes):
        """(bytes to send, state, problem)."""
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            return None, None, "the source is not UTF-8: %s" % exc
        want = {}
        for form, low in self.standins:
            if low in text:
                return None, None, ("the source already holds %s in lower "
                                    "case: it could not be told from the "
                                    "stand-in %s" % (low, form))
        for form, low in self.standins:
            n = text.count(form)
            if n:
                want[form] = n
                text = text.replace(form, low)
        unknown = sorted(set(STANDIN_SHAPE.findall(text)))
        if unknown:
            return None, None, ("unknown stand-in(s) %s: add each to "
                                "stand-ins.tsv (see the README) or take it "
                                "out of the text" % ", ".join(unknown))
        if want and not self.usermap:
            return None, None, ("the source holds stand-ins (%s) and the "
                                "config has no user map for them"
                                % ", ".join(sorted(want)))
        fixes, counts = {}, {}
        for name, pat, new in self.filters:
            def sub(m, name=name, new=new):
                r = new(m)
                n = m.end() - m.start()
                if len(r) > n:
                    return m.group(0)
                fixes[m.start()] = (len(r), m.end())
                counts[name] = counts.get(name, 0) + 1
                return r + " " * (n - len(r))
            text = pat.sub(sub, text)
        return text.encode("utf-8"), (want, fixes, counts), None

    def finish(self, out: bytes, state):
        """(tab-separated CoNLL, tokens, problem). FreeLing pads its
        columns with spaces and never puts one inside a field."""
        want, fixes, counts = state
        lines, ntok = [], 0
        got = {form: 0 for form, _ in self.standins}
        ends = {s + n: (s, e) for s, (n, e) in fixes.items()}
        try:
            raw_lines = out.decode("utf-8").split("\n")
        except UnicodeDecodeError as exc:
            return None, 0, "FreeLing's output is not UTF-8: %s" % exc
        for n, raw in enumerate(raw_lines, 1):
            f = raw.split()
            if not f:
                lines.append("")
                continue
            if len(f) != self.ncols and not (self.srl_last and len(f) >= self.ncols):
                return None, 0, ("line %d has %d fields, the columns file "
                                 "lists %d" % (n, len(f), self.ncols))
            fi = self.form_i
            for form, low in self.standins:
                if low in f[fi]:
                    got[form] += f[fi].count(low)
                    f[fi] = f[fi].replace(low, form)
            b_i, e_i = self.span_i
            if ends and b_i >= 0 and e_i >= 0:
                try:
                    b, e = int(f[b_i]), int(f[e_i])
                except ValueError:
                    b = e = -1
                if e in ends and ends[e][0] <= b < e:
                    f[e_i] = str(ends[e][1])
            lines.append("\t".join(f))
            ntok += 1
        for form, _ in self.standins:
            if got[form] != want.get(form, 0):
                return None, 0, ("%s: %d in the source, %d in FreeLing's FORM "
                                 "column" % (form, want.get(form, 0), got[form]))
        while lines and lines[-1] == "":
            lines.pop()
        if counts:
            with self.lock:
                for k, v in counts.items():
                    self.counts[k] += v
        return ("\n".join(lines) + "\n\n").encode("utf-8"), ntok, None


def make_sender(fl: FreeLing, script_dir: Path, cfg_names, dep: str):
    """(sender, problems, notes) for the configs a run uses (they must
    share their columns)."""
    problems, notes = [], []
    standins, p = load_standins(fl)
    if p:
        return None, [p], notes
    comma, n = load_comma_multiwords(script_dir / COMMA_MULTIWORDS)
    if comma is None:
        return None, ["the comma multiwords: %s" % n], notes
    columns, p = conll_columns(fl.config(COLUMNS_CFG))
    if p:
        return None, [p], notes
    if "FORM" not in columns:
        return None, ["the CoNLL columns have no FORM"], notes
    pr, nt = probability_columns_check(fl.lib, columns)
    if pr:
        problems.append(pr)
    if nt:
        notes.append("library: %s" % nt)
    for name in cfg_names:
        pr, nt = check_config(fl, name, standins, dep,
                              informal=(name == INFORMAL_CONFIG))
        problems += pr
        notes += nt
    usermap = all(n in ESCL_CONFIGS for n in cfg_names)
    notes.append("columns: %s" % " ".join(columns))
    notes.append("stand-ins: %s (%s)" % (", ".join(f for f, _, _ in standins),
                                         fl.share / STANDINS_FILE))
    notes.append("comma multiwords: %d (%s)" % (n, script_dir / COMMA_MULTIWORDS))
    return Sender(standins, PREFILTERS + [comma], columns, usermap), problems, notes


# ---------------------------------------------------------------------------
# The server.
def port_open(port, host="127.0.0.1"):
    with socket.socket() as s:
        s.settimeout(1.0)
        return s.connect_ex((host, port)) == 0


def start_server(cmd, log_path: Path, port: int, timeout: int):
    """Start FreeLing's server in its own process group (analyze is a
    wrapper that starts the real analyzer as a child: the whole group is
    stopped at the end), its stderr to a file (a full pipe blocks the
    analyzer). Returns (process, problem)."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    errf = open(log_path, "wb")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=errf,
                            start_new_session=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        if proc.poll() is not None:
            return None, "the server exited during startup; see %s" % log_path
        if port_open(port):
            log("server : up after %.0f s, models loaded" % (time.time() - t0))
            return proc, None
        time.sleep(1.0)
    stop_server(proc)
    return None, "the server did not open port %d within %d s" % (port, timeout)


def stop_server(proc):
    for sig, wait in ((signal.SIGTERM, 30), (signal.SIGKILL, 10)):
        try:
            os.killpg(proc.pid, sig)
        except ProcessLookupError:
            break
        t0 = time.time()
        gone = False
        while time.time() - t0 < wait:
            try:
                os.killpg(proc.pid, 0)
            except ProcessLookupError:
                gone = True
                break
            time.sleep(0.5)
        if gone:
            break
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass


SS = shutil.which("ss") or "ss"


def reap_orphan_analyzers(port, quiet=False):
    """Kill analyzers still holding a connection whose client is gone
    (CLOSE-WAIT on our port). A document that hangs the LSTM parser leaves
    its forked analyzer running after the client times out; left alone, the
    worker pool drains away."""
    try:
        r = subprocess.run([SS, "-tnp"], capture_output=True, text=True,
                           timeout=15)
    except (OSError, subprocess.SubprocessError):
        return 0
    if r.returncode != 0:
        return 0
    killed = 0
    for line in r.stdout.splitlines():
        if "CLOSE-WAIT" not in line:
            continue
        parts = line.split()
        if len(parts) < 4 or not parts[3].endswith(":%d" % port):
            continue
        m = re.search(r'\(\("analyzer",pid=(\d+),', line)
        if not m:
            continue
        try:
            os.kill(int(m.group(1)), signal.SIGKILL)
            killed += 1
        except (ProcessLookupError, PermissionError):
            pass
    if killed and not quiet:
        log(orange("reaped %d orphaned analyzer(s)" % killed))
    return killed


def analyze_through_server(fl: FreeLing, host, port, data: bytes, timeout):
    """(output, problem): one document through a running server."""
    try:
        proc = subprocess.run([fl.client, "%s:%d" % (host, port)], input=data,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        reaped = reap_orphan_analyzers(port, quiet=True)
        return None, ("timeout after %ds (reaped %d analyzer(s))"
                      % (timeout, reaped))
    if proc.returncode != 0:
        err = " ".join((proc.stderr or b"").decode("utf-8", "replace").split())
        return None, ("analyzer_client exit %d: %s" % (proc.returncode, err[:160])
                      if err else "analyzer_client exit %d" % proc.returncode)
    return proc.stdout, None


# ---------------------------------------------------------------------------
# The corpus folders.
def name_problem(name: str):
    """Why a corpus may not have this name, or None."""
    if not name or name in (".", "..") or "/" in name or "\\" in name:
        return "a corpus name is one folder name: %r" % name
    if name.startswith((".", "_")):
        return "a corpus name may not start with . or _: %s" % name
    if name.lower() in RESERVED_NAMES:
        return ("%s is reserved: no corpus may be called %s (case "
                "ignored)" % (name, ", ".join(RESERVED_NAMES)))
    return None


def corpora_dir(home: Path) -> Path:
    return home / CORPORA


def corpus_input(cdir: Path):
    """(kind, input path, problem): the one entry of input/, named after
    its kind, a link to the corpus root or the folder itself."""
    idir = cdir / INPUT
    if not idir.is_dir():
        return None, None, ("%s is missing: make it, with a link named after "
                            "the kind of text to the corpus root (see the "
                            "README)" % idir)
    entries = [p for p in idir.iterdir() if p.name != "README.md"]
    names = sorted(p.name for p in entries)
    unknown = [n for n in names if n not in KINDS]
    if unknown:
        return None, None, ("%s holds %s; only one of %s may be there"
                            % (idir, ", ".join(unknown), ", ".join(KINDS)))
    if len(names) != 1:
        return None, None, ("%s must hold exactly one of %s; it holds %s"
                            % (idir, ", ".join(KINDS),
                               ", ".join(names) or "nothing"))
    p = idir / names[0]
    if not p.is_dir():
        return None, None, ("%s does not lead to a folder (a broken link?)"
                            % p)
    return names[0], p, None


def stage_path(cdir: Path, num: str) -> Path:
    return cdir / STAGES[num][0]


def stage_made(cdir: Path, num: str) -> bool:
    """A stage is made when its folder holds columns.tsv."""
    return (stage_path(cdir, num) / COLUMNS_TSV).is_file()


def ensure_stage(cdir: Path, num: str):
    """The stage folder, made if missing. A link to a folder that does not
    exist yet has that folder made. The link is read from the folder it
    really is in: the corpus folder may itself be reached through a link,
    and a relative target counts from the real place, not from the path
    that was typed."""
    p = stage_path(cdir, num)
    if p.is_symlink() and not p.exists():
        target = Path(os.path.join(str(p.parent.resolve()), os.readlink(str(p))))
        target = Path(os.path.normpath(str(target)))
        target.mkdir(parents=True, exist_ok=True)
        if not p.is_dir():
            raise OSError("the link %s does not lead to the folder made for "
                          "it, %s" % (p, target))
        log("made the folder the link %s points to: %s" % (p, target))
    elif not p.exists():
        p.mkdir(parents=True)
    return p


def load_informal(cdir: Path, root: Path):
    """(rules, problem): informal.txt, one path per line, absolute or from
    the corpus root; # starts a comment. Every path must be inside the
    corpus and exist, and none may be inside another."""
    path = cdir / INFORMAL_LIST
    if not path.is_file():
        return [], None
    rules = []
    real_root = root.resolve()
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        t = unicodedata.normalize("NFC", line.strip())
        if not t or t.startswith("#"):
            continue
        p = Path(t)
        if p.is_absolute():
            rp = Path(os.path.normpath(t))
            rel = None
            for base in (root, real_root):
                try:
                    rel = rp.relative_to(base)
                    break
                except ValueError:
                    pass
            if rel is None:
                try:
                    rel = rp.resolve().relative_to(real_root)
                except ValueError:
                    return None, ("%s line %d: %s is not inside the corpus "
                                  "(%s)" % (path, n, t, root))
        else:
            rel = Path(os.path.normpath(t))
            if rel.parts and rel.parts[0] == "..":
                return None, "%s line %d: %s leaves the corpus" % (path, n, t)
        if str(rel) in ("", "."):
            return None, ("%s line %d: %s is the whole corpus; for a corpus "
                          "that is all informal, list its folders"
                          % (path, n, t))
        if not (root / rel).exists():
            return None, "%s line %d: not found in the corpus: %s" % (path, n, rel)
        rules.append((rel.parts, n, t))
    for i, (a, na, ta) in enumerate(rules):
        for b, nb, tb in rules[i + 1:]:
            short, long_ = (a, b) if len(a) <= len(b) else (b, a)
            if long_[:len(short)] == short:
                return None, ("%s lines %d and %d overlap: %s and %s (one is "
                              "inside the other, or they are the same)"
                              % (path, na, nb, ta, tb))
    return [r[0] for r in rules], None


def is_informal(rel: Path, rules) -> bool:
    parts = rel.parts
    return any(parts[:len(r)] == r for r in rules)


def branches(tree):
    """The shallowest folders whose texts are all tagged the same way:
    (folder, how, texts). tree maps each folder (a tuple of parts) to
    [formal texts, informal texts] below it."""
    kids = {}
    for k in tree:
        if k:
            kids.setdefault(k[:-1], []).append(k)
    out = []

    def walk(k):
        std, inf = tree[k]
        if not std or not inf:
            out.append(("/".join(k) or ".", "informal" if inf else "formal",
                        std + inf))
            return
        below = [0, 0]
        for c in sorted(kids.get(k, [])):
            below[0] += tree[c][0]
            below[1] += tree[c][1]
            walk(c)
        for reg, n in (("formal", std - below[0]), ("informal", inf - below[1])):
            if n:
                out.append((("/".join(k) or ".") + " (the texts in the folder "
                            "itself)", reg, n))
    if () in tree:
        walk(())
    return out


def corpus_files(folder: Path, suffix: str):
    """The files ending in suffix under folder, never a record, sorted."""
    out = []
    for p in folder.rglob("*" + suffix):
        if not p.is_file():
            continue
        rel = p.relative_to(folder)
        if RECORDS in rel.parts or rel.name == COLUMNS_TSV:
            continue
        out.append(p)
    return sorted(out)


# ---------------------------------------------------------------------------
# columns.tsv: one row per column of the stage's .conll files.
COLUMNS_HEADER = ("position", "name", "step", "option", "program")


def write_columns(stage: Path, rows):
    """rows: (name, step, option, program), in column order."""
    text = "\t".join(COLUMNS_HEADER) + "\n" + "".join(
        "%d\t%s\n" % (i, "\t".join(str(x) for x in r))
        for i, r in enumerate(rows, 1))
    put_file(text, stage / COLUMNS_TSV)


def read_columns(stage: Path):
    """(rows, problem): [(name, step, option, program)] in column order."""
    path = stage / COLUMNS_TSV
    if not path.is_file():
        return None, "%s is missing" % path
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or tuple(lines[0].split("\t")) != COLUMNS_HEADER:
        return None, "%s: the header must be %s" % (path, "\t".join(COLUMNS_HEADER))
    rows = []
    for n, line in enumerate(lines[1:], 2):
        f = line.split("\t")
        if len(f) != 5 or f[0] != str(len(rows) + 1):
            return None, "%s line %d is not readable" % (path, n)
        rows.append(tuple(f[1:]))
    return rows, None


# ---------------------------------------------------------------------------
# README.md in every folder this tool makes.
def write_readme(folder: Path, text: str):
    put_file(text.rstrip("\n") + "\n", folder / "README.md")
    return folder / "README.md"


CORPORA_README = """# corpora

The corpora tagged with FreeLing es-CL 2027, one folder each. Made by
`freeling.py`; every folder in it is described by its own README.md.

A corpus folder holds:

- `input/`, with one link named after the kind of text (`speech`,
  `written-modern`, `written-19th-century` or `written-old`) that leads to
  the corpus root, the folder holding its texts;
- `informal.txt` (written-modern only, optional): the informal texts;
- one folder per stage made, numbered as in every corpus: 060, 070, 080,
  400 ... (a stage may be a link to a folder elsewhere);
- `_processing-records/`: the logs of each run of `freeling.py`.

No corpus may be called {reserved}. This folder may itself be a link to a
folder elsewhere (a larger disk, say).
"""

CORPUS_README = """# {name}

A corpus tagged with FreeLing es-CL 2027 by `freeling.py`. Kind of text:
{kind} ({kind_text}).

- `input/{kind}` leads to the corpus root: {root}
{informal}- The stages made so far, and what each is used for next, are described by
  the README.md in each stage folder. Stages not made have no folder.
- `_processing-records/` holds the log of every run of `freeling.py` on
  this corpus.

The stages, in order (a stage needs the ones before it that it lists):

{stages}
"""

INPUT_README = """# input

Holds one link, named after the kind of text, that leads to the corpus
root: the folder holding the corpus texts, in any number of subfolders.

The texts: plain text, UTF-8, ending in `.txt` (or the extension given
with `--ext`), one sentence or utterance per line (every line end ends a
sentence), no markup. Stand-in tokens (XXXREDACTEDXXX and the others in
stand-ins.tsv) may appear; any other XXX...XXX form fails its text.

Made by `freeling.py --new`, or by hand:

    ln -s ../../../path/to/the/corpus/root {kind}

Used next by `freeling.py --freeling` (stage 060).
"""

RECORDS_README = """# _processing-records

The records of the folder above: logs, failure lists and reports of each
run, named with the date and time of the run. It holds no corpus files and
is never read as texts. Made by `freeling.py`; nothing reads these files
again except people.
"""


def stages_listing():
    lines = []
    for num in STEP_ORDER:
        folder, opt, what = STAGES[num]
        req = REQUIRES[num]
        lines.append("- `%s` (`%s`): %s.%s" % (
            folder, opt, what,
            (" Needs %s." % ", ".join(STAGES[r][0] for r in req)) if req else ""))
    for num, what in RESERVED_STAGES:
        lines.append("- %s: reserved for %s." % (num, what))
    return "\n".join(lines)


def ensure_corpus_readmes(home: Path, cdir: Path, kind: str, root: Path,
                          informal_rules):
    cr = corpora_dir(home)
    if not (cr / "README.md").exists():
        write_readme(cr, CORPORA_README.format(reserved=", ".join(RESERVED_NAMES)))
    inf = ""
    if informal_rules:
        inf = ("- `informal.txt` lists the informal texts (%d path(s)), tagged "
               "with the\n  informal config; every other text is formal.\n"
               % len(informal_rules))
    write_readme(cdir, CORPUS_README.format(
        name=cdir.name, kind=kind, kind_text=KIND_TEXT[kind], root=root.resolve(),
        informal=inf, stages=stages_listing()))
    if not (cdir / INPUT / "README.md").exists():
        write_readme(cdir / INPUT, INPUT_README.format(kind=kind))
    ensure_records(cdir)


def ensure_records(folder: Path) -> Path:
    r = folder / RECORDS
    r.mkdir(parents=True, exist_ok=True)
    if not (r / "README.md").exists():
        write_readme(r, RECORDS_README)
    return r
