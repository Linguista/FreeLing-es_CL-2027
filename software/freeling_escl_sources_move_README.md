# freeling_escl_sources_move_README.md

Documents `freeling_escl_sources_move.py` 1.0.0.

Real file: `/home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_sources_move.py`

## Purpose

Gives the decision files that the FreeLing es-CL build reads one home, in
the FreeLing tree (decided 261112). It moves them out of the COSCACH
decisions folder into `escl-sources`, and leaves a relative link in each
one's old place. There is then one copy of each file, so nothing can drift:
`freeling_escl_build.py` reads it in `escl-sources`, and the COSCACH spelling
step (`coscach_12_spelling_normalize.py`) reads it through the link.

| | |
|---|---|
| from | `/home/user/corpora/050-Spelling-normalized/COSCACH/_processing-records/spelling-review/decisions/` |
| to | `/home/user/csld/software/10-Infrastructure/freeling/escl-sources/` |
| log | `/home/user/csld/working/freeling/freeling_escl_sources_move--YYMMDD_HHMMSS.tsv` |

## Usage

```bash
freeling_escl_sources_move.py --dry-run
freeling_escl_sources_move.py
freeling_escl_sources_move.py --check
```

| Option | |
|---|---|
| `--dry-run` | report what would be done; change nothing (the log is written, with `--DRY-RUN` in its name) |
| `--check` | move nothing; report every file of a kind the build reads: `linked`, `ORDINARY FILE` (in the COSCACH folder, not moved), `WRONG LINK`, or `NO LINK` (in escl-sources, with no link in the COSCACH folder). Exit 1 if any is not linked |
| `--from DIR` | the COSCACH decisions folder |
| `--to DIR` | escl-sources (default: `<project root>/software/10-Infrastructure/freeling/escl-sources`) |
| `--root DIR` | the project root (default: found from the script's location by `PROJECT_ROOT.txt`) |

## What it moves

Only the 17 kinds of file the build reads (the part of the name before
`--`, the same list as `BUILD_STEMS` in `freeling_escl_build.py`):
`all-corpora-replacements`, `correction-lemmas`,
`dictionary-addition-removals`, `dictionary-additions`,
`dictionary-additions-all-rounds-standardized`, `dictionary-variants`,
`fixed-name-classes`, `interjection-removals`, `interjections`,
`lemma-standardization`, `name-class-shares`, `person-name-removals`,
`place-only-forms`, `sentence-start-classes`, `text-correction-removals`,
`text-corrections`, `verb-form-readings`. On 261112 that is 41 files.

Everything else in the COSCACH folder stays an ordinary file there: the
files that quote the interviews (`occurrence-corrections`,
`ir-hacer-occurrences`, `sino-si-no`), the other COSCACH-only files
(`markers`, `kept-as-is`, `perkins-respellings`, `foreign-words`,
`ir-hacer-decisions`, `sino-si-no-rules`, `final-fixes`, `learned-proposals`,
`check-answers`, `to-check`, `resolved-from-earlier-decisions`), its
`README.md` and the `deprecated/` folder, which is not touched.

## How each file is moved

1. Copied into escl-sources as `NAME.part`, flushed to disk, its sha256
   checked against the original, its modification time kept, renamed to
   `NAME`.
2. The original replaced by a relative link to it (made as
   `NAME.link-part`, then renamed over the original, so the name always
   exists).
3. The link checked: it must lead to the file in escl-sources, with the
   original's sha256.

A file already linked is left alone, so the tool can be run again at any
time: a new round saved in the COSCACH folder is moved and linked, and
nothing else changes. A file of the same name already in escl-sources is
only linked if it is byte for byte the same; otherwise it is reported and
neither is touched. A file that cannot be written or removed (an immutable
flag, permissions) is reported and never forced.

## Output

One line per file, the action first and the file name last; at the end the
count of each action and the log's path. The log is TAB-separated: action,
sha256, detail, file.

## Tested

261112, on a copy of the COSCACH decisions folder as uploaded on 261112: the
dry run listed the 41 files; the run moved and linked them, each link
leading to a file with the original's sha256; a second run left all 41
alone; `--check` reported 41 linked; `freeling_escl_build.py`'s own link
check found no problem.

## Exit codes

0 done, 1 a problem with at least one file (or, with `--check`, a file not
linked), 2 refused (no project root, no COSCACH folder), 130 interrupted.

## Platform

Linux. On Windows the links need Developer Mode or administrator rights.
Standard library only.

## Changelog

- 1.0.0 (261112): first version.
