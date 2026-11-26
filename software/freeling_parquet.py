#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 1.1.0
#
# freeling_parquet.py -- step 400 of freeling.py (FreeLing es-CL 2027): a
# Parquet token store of the last stage made, 080-Perkins-Tagged, else
# 070-Universal-Dependency-Tagged, else 060-FreeLing-Tagged. Run it through
# freeling.py:
#
#     freeling.py CORPUS --parquet
#
# One Parquet file per folder of the stage (tokens.parquet, in the same
# folders under 400-Parquet), not one per document: a corpus of a million
# documents would otherwise be a million small files. Every column of the
# stage, as listed in its columns.tsv, plus DOCUMENT (the text's path from
# the corpus root, without its extension) and SENTENCE (its number in the
# document, from 1). ID, SPAN_BEGIN, SPAN_END and DEPHEAD are integers;
# LEX_PROB and TAG_PROB are numbers (empty where the stage has -); every
# other column is text, exactly as in the stage. Compressed with
# zstd; strings dictionary-encoded, so a column of a few hundred tags over
# billions of rows costs a few bytes a row.
#
# A folder whose tokens.parquet is newer than every .conll in it is skipped
# (--redo rebuilds it). Each file is written to .part and renamed.
#
# Why Parquet: a column store read by DuckDB, Python (pandas, polars) and R
# (arrow) without an import step, and with no cap on the number of tokens
# (CWB, the engine of CQPweb, counts corpus positions in 32 bits: 2^31 - 1
# tokens at most).
#
# A module of freeling.py: it does nothing when run on its own. Needs
# pyarrow (pip install pyarrow).

from __future__ import annotations

import time
from pathlib import Path

import freeling_common as fc

VERSION = "1.1.0"
__version__ = VERSION
INT_COLUMNS = ("ID", "SPAN_BEGIN", "SPAN_END", "DEPHEAD")
FLOAT_COLUMNS = ("LEX_PROB", "TAG_PROB")
OUT = "tokens.parquet"

STAGE_README = """# 400-Parquet / {name}

Made by `freeling.py` {fversion} with `freeling_parquet.py` {version}
(FreeLing es-CL 2027) on {date}, from {source}. Folders: {nfolders};
tokens: {ntokens}.

## What is in it

One `tokens.parquet` per folder of {source}, in the same folders: one row
per token of every document in that folder. The columns are listed in
`columns.tsv`: `DOCUMENT` (the text's path from the corpus root, without
its extension), `SENTENCE` (its number in the document, from 1), then
every column of {source}. `ID`, `SPAN_BEGIN`, `SPAN_END` and `DEPHEAD` are
integers; `LEX_PROB` and `TAG_PROB` are numbers from 0 to 1 (empty where the
stage has `-`); every other column is text exactly as in the stage (FreeLing
writes `-` for an empty field, the later stages `_`).

## How it was made

`{command}`

## What it is used for next

Queries, without importing anything first. DuckDB:

    SELECT LEMMA, COUNT(*) AS n, COUNT(DISTINCT DOCUMENT) AS documents
    FROM read_parquet('{glob}')
    WHERE TAG LIKE 'N%'
    GROUP BY LEMMA ORDER BY n DESC LIMIT 50;

Python: `pandas.read_parquet` or `polars.scan_parquet` on the same files;
R: `arrow::open_dataset`. Your own tables (frequency lists, analyses,
metadata) go in 500-Database, beside this folder.
"""


def source_stage(ctx):
    """The last stage made: 080, 070 or 060, or None."""
    for num in ("080", "070", "060"):
        if fc.stage_made(ctx.cdir, num):
            return num
    return None


def read_conll(path, ncols):
    sent, have = 1, False
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if not line:
                if have:
                    sent += 1
                    have = False
                continue
            f = line.split("\t")
            if len(f) != ncols:
                raise ValueError("%s line %d has %d fields, not %d"
                                 % (path, n, len(f), ncols))
            have = True
            yield sent, f


def to_int(v):
    try:
        return int(v)
    except ValueError:
        return None


def to_float(v):
    try:
        return float(v)
    except ValueError:
        return None


def field_type(pa, name):
    if name in INT_COLUMNS:
        return pa.int64()
    if name in FLOAT_COLUMNS:
        return pa.float64()
    return pa.string()


def field_value(name, v):
    if name in INT_COLUMNS:
        return to_int(v)
    if name in FLOAT_COLUMNS:
        return to_float(v)
    return v


def run(ctx):
    a = ctx.a
    fc.log("")
    fc.log("STEP 400  %s" % fc.STAGES["400"][0])
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:
        fc.log(fc.red("REFUSED: the Parquet step needs pyarrow: "
                      "pip install pyarrow"))
        return 2
    num = source_stage(ctx)
    if num is None:
        if a.dry_run:
            fc.log("would read the last stage made in this run")
            return 0
        fc.log(fc.red("REFUSED: no stage made yet: --parquet needs %s"
                      % fc.STAGES["060"][0]))
        return 2
    src_root, dst_root = ctx.stage(num), ctx.stage("400")
    rows, p = fc.read_columns(src_root)
    if p:
        fc.log(fc.red("REFUSED: %s" % p))
        return 2
    names = [r[0] for r in rows]
    fc.log("from   : %s (%d columns)" % (src_root, len(names)))
    fc.log("to     : %s" % dst_root)
    folders = {}
    for f in fc.corpus_files(src_root, ".conll"):
        rel = f.relative_to(src_root)
        if a.only and rel.parts[:len(Path(a.only.strip("/")).parts)] != \
                Path(a.only.strip("/")).parts:
            continue
        folders.setdefault(rel.parent, []).append(f)
    if not folders:
        fc.log(fc.red("REFUSED: no .conll files under %s" % src_root))
        return 2
    todo, skipped = [], 0
    for rel, files in sorted(folders.items()):
        out = dst_root / rel / OUT
        if out.exists() and not a.redo and \
                out.stat().st_mtime >= max(f.stat().st_mtime for f in files):
            skipped += 1
            continue
        todo.append((rel, files, out))
        if a.limit and len(todo) >= a.limit:
            break
    fc.log("%d folder(s) to write, %d up to date" % (len(todo), skipped))
    if a.dry_run:
        for rel, files, out in todo[:15]:
            fc.log("  %6d file(s)  %s" % (len(files), rel))
        return 0
    fc.ensure_stage(ctx.cdir, "400")
    fc.ensure_records(dst_root)
    schema = [pa.field("DOCUMENT", pa.string()), pa.field("SENTENCE", pa.int32())]
    for n in names:
        schema.append(pa.field(n, field_type(pa, n)))
    schema = pa.schema(schema)
    t0, total, failures = time.time(), 0, []
    for i, (rel, files, out) in enumerate(todo, 1):
        cols = {n: [] for n in ["DOCUMENT", "SENTENCE"] + names}
        try:
            for f in files:
                doc = str((rel / f.name[:-len(".conll")]).as_posix())
                for sent, fields in read_conll(f, len(names)):
                    cols["DOCUMENT"].append(doc)
                    cols["SENTENCE"].append(sent)
                    for n, v in zip(names, fields):
                        cols[n].append(field_value(n, v))
        except (ValueError, UnicodeDecodeError, OSError) as exc:
            failures.append((str(exc), str(rel)))
            fc.log("FAILED  %s" % exc)
            continue
        ntok = len(cols["DOCUMENT"])
        table = pa.table({n: pa.array(cols[n], type=schema.field(n).type)
                          for n in schema.names}, schema=schema)
        out.parent.mkdir(parents=True, exist_ok=True)
        part = out.with_name(out.name + ".part")
        try:
            pq.write_table(table, part, compression="zstd", compression_level=9,
                           use_dictionary=True)
            part.replace(out)
        except BaseException:
            fc.unlink_quietly(part)
            raise
        total += ntok
        el = max(time.time() - t0, 0.001)
        fc.log("%6d/%d  %11s tok  eta %s  %s"
               % (i, len(todo), f"{ntok:,}", fc.hms((len(todo) - i) * el / i),
                  rel.as_posix() or "."))
    fc.log("-" * 78)
    fc.log("%s token(s) written in %d folder(s), %s"
           % (f"{total:,}", len(todo) - len(failures), fc.hms(time.time() - t0)))
    if failures:
        fp = fc.free_name(dst_root / fc.RECORDS, "parquet-FAILED--%s" % ctx.stamp)
        fc.put_file("reason\tfolder\n" + "".join("%s\t%s\n" % f for f in failures), fp)
        fc.log(fc.orange("failure list: %s" % fp))
    program = "freeling_parquet.py %s (freeling.py %s), pyarrow %s" % (
        VERSION, ctx.version, pa.__version__)
    out_rows = [("DOCUMENT", "--parquet", "the text's path from the corpus root, "
                 "without its extension", program),
                ("SENTENCE", "--parquet", "the sentence's number in the document",
                 program)]
    out_rows += [(r[0], r[1], r[2], r[3]) for r in rows]
    fc.write_columns(dst_root, out_rows)
    if not ((a.only or a.limit) and (dst_root / "README.md").is_file()):
        parts = fc.corpus_files(dst_root, ".parquet")
        n_all = len(parts)
        n_tok = sum(pq.ParquetFile(str(x)).metadata.num_rows for x in parts)
        fc.write_readme(dst_root, STAGE_README.format(
            name=ctx.name, fversion=ctx.version, version=VERSION,
            date=time.strftime("%Y-%m-%d"), source=src_root.name,
            nfolders=f"{n_all:,}", ntokens=f"{n_tok:,}",
            command=ctx.command, glob=str(dst_root / "**" / OUT)))
        fc.log("stage README: %s" % (dst_root / "README.md"))
    return 1 if failures else 0


if __name__ == "__main__":
    print("freeling_parquet.py is step 400 of freeling.py: freeling.py CORPUS --parquet")
