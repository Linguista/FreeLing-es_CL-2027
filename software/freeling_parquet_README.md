# freeling_parquet_README.md

Documents `freeling_parquet.py` 1.0.0, step 400 of `freeling.py`.

## Purpose

Makes a Parquet token store of the last stage made, `080-Perkins-Tagged`,
else `070-Universal-Dependency-Tagged`, else `060-FreeLing-Tagged`, in
`400-Parquet`. Parquet is a column store read directly by DuckDB, Python
(pandas, polars, pyarrow) and R (arrow), with no import step and no cap on
the number of tokens. (CWB, the engine of CQPweb, counts corpus positions
in 32 bits: 2,147,483,647 tokens at most.)

## Usage

```bash
freeling.py CORPUS --parquet
freeling.py CORPUS --ud --parquet
```

Needs pyarrow: `pip install pyarrow`.

## What it writes

One `tokens.parquet` per folder of the stage, in the same folders under
`400-Parquet` (one per folder, not per document: a corpus of a million
documents would otherwise be a million small files). One row per token:

| Column | Type | |
|---|---|---|
| `DOCUMENT` | text | the text's path from the corpus root, without its extension |
| `SENTENCE` | integer | the sentence's number in the document, from 1 |
| every column of the stage, as in its `columns.tsv` | text | exactly as in the stage |
| `ID`, `SPAN_BEGIN`, `SPAN_END`, `DEPHEAD` | integer | |
| `LEX_PROB`, `TAG_PROB` | number (double) | from 0 to 1; empty where the stage has `-` |

Compressed with zstd; text columns dictionary-encoded, so a column of a few
hundred tags over billions of rows costs a few bytes a row. Each file is
written to `.part` and renamed. A folder whose `tokens.parquet` is newer
than every `.conll` in it is skipped; `--redo` writes it again.

## Querying it

DuckDB, with no server:

```sql
SELECT LEMMA, COUNT(*) AS n, COUNT(DISTINCT DOCUMENT) AS documents
FROM read_parquet('/path/to/FreeLing-es_CL-2027/corpora/CORPUS/400-Parquet/**/tokens.parquet')
WHERE TAG LIKE 'N%'
GROUP BY LEMMA ORDER BY n DESC LIMIT 50;
```

Your own tables (frequency lists, analyses, metadata) go in
`500-Database`, beside `400-Parquet`.

## Exit codes

0 done; 1 a folder failed; 2 refused (no stage made, pyarrow missing).

## Platform

Linux, macOS and Windows wherever pyarrow installs. Python 3.9 or later.

## Changelog

- 1.1.0 (261120): `LEX_PROB` and `TAG_PROB` are stored as numbers, so they
  can be compared and averaged without a cast (`WHERE TAG_PROB < 0.9`).
- 1.0.0 (261119): first version, replacing `conll_to_parquet.py` 1.0.0:
  reads the columns from `columns.tsv` instead of a fixed list; one file
  per folder in a mirror of the stage's folders instead of one flat folder
  of long names; DOCUMENT and SENTENCE; every column kept as written.
