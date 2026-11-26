# freeling_perkins_README.md

Documents `freeling_perkins.py` 1.0.0, step 080 of `freeling.py`.

## Purpose

Adds the phonological transcriptions of Perkins, the Spanish phonological
transcriber (https://github.com/Linguista/Perkins, GNU AGPL 3.0, used as the
compiled program `perkins`), to every token: one column per set of Perkins
options, named after the options. Writes beside each document a
transcription of every utterance or line as running text. Not for
written-old: Perkins transcribes modern Spanish.

## Usage

```bash
freeling.py CORPUS --perkins
freeling.py CORPUS --perkins --perkins-columns=-oa --perkins-columns="-nt -oa" --perkins-word-alone="-nt -oa"
freeling.py CORPUS --perkins --perkins-bin /opt/perkins/perkins --jobs 8
```

Reads `070-Universal-Dependency-Tagged`, writes `080-Perkins-Tagged`.
Write the `=` after `--perkins-columns` and `--perkins-word-alone`.

## The columns

Each set of options given with `--perkins-columns` is one column, the
sentence transcribed as a whole (`perkins -nocfg -b -tok OPTIONS`). Each
set given with `--perkins-word-alone` is one column with every word
transcribed on its own. The name is `PERKINS_` and the options in capitals,
the dashes dropped and anything else that is not a letter or a digit made
`_`; a word-alone column ends in `_WORD`:

| Options | Column |
|---|---|
| `-oa` | `PERKINS_OA` |
| `-csc` | `PERKINS_CSC` |
| `-nt -oa` | `PERKINS_NT_OA` |
| `-f=MANNER -oa` | `PERKINS_F_MANNER_OA` |
| `-nt -oa`, word alone | `PERKINS_NT_OA_WORD` |

With the set `-oa` (phonemic, stress as an apostrophe) come two more
columns after it:

- `NSYL`: the number of syllables that have a vowel or a syllabic
  consonant;
- `STRESS`: the stressed syllable counted from the end (1 the last); a
  monosyllable 1; 0 for a one-syllable function word (articles,
  possessive determiners, prepositions, conjunctions, relatives other than
  cual, reflexive and clitic pronouns). A word whose syllables all lack a
  vowel (brbrbr) is stressed on its last.

The default, with neither option: `-oa` (with NSYL and STRESS), `-csc`,
`-nt -oa`, `-nt -oa` word alone, `-f=MANNER -oa`, `-f=PLACE -oa`,
`-f=V -oa`: 9 columns. There may be one column or many; their names,
options and the Perkins version are in `columns.tsv`.

## How tokens are read

- **In context**: each sentence goes to Perkins as one line, so the rules
  that apply across words do, and a pause (punctuation, a stand-in) blocks
  them.
- **A FreeLing multiword** stays one row, its words separated by single
  spaces in every Perkins column (o_sea: `o 'se.a`, NSYL `1 2`, STRESS
  `0 2`). `_` in a Perkins column only ever means an empty field.
- **del, al and pal**, which FreeLing splits into de + el, a + el and
  para + el, are read as the one word they are, on de, a or para; el has
  `_` in every Perkins column.
- **A stand-in** is sent to Perkins as a full stop: a pause in every
  column, `_` in NSYL and STRESS.
- **A false start** (a token without a vowel right before an ellipsis: no
  s ... no logró) is read as its sounds, with NSYL and STRESS 0.
- **Nothing is lost to a misalignment**: Perkins must return one field per
  token. A sentence for which it does not is sent again alone, then token
  by token; a token that still fails gets `?`. Every fallback is listed.

## The utterance and line files

Beside each `NAME.conll`, with a header and one row per utterance or line:

- `NAME.utterances.tsv`, when `NAME.times.tsv` is there (speech): one row
  per row of it, numbered by its `interval`;
- otherwise `NAME.lines.tsv`: one row per non-empty line of the text, read
  from the corpus root, numbered by its line.

Each holds every in-context set that is not a feature set (`-f=`) as running
text, so that syllables run across words (del año `d̪e.'la.ɲo`). The text of
a row is rebuilt from the tokens whose span begins inside it.

## Writing and resuming

The `.times.tsv`, the utterance or line file, then the `.conll`, each
through a `.part` file renamed into place. A finished document is skipped
(`--redo` rewrites it); a missing sidecar beside one is copied, and one that
differs from 070's is listed. `--jobs N` documents at once (default: every
logical CPU).

## Refused

Perkins missing or older than 2.0.41; 070 not made; a column of 070 missing
(SPAN_BEGIN, SPAN_END, FORM, TAG) or already there; two sets of options
giving the same name; a README or `columns.tsv` that cannot be replaced.
Every Perkins run is `perkins -nocfg -b ...`, so no `perkins.ini` changes the
result.

## Records

In the stage's `_processing-records/`, when there is something in them:
`perkins-fallbacks--YYMMDD_HHMM.tsv`,
`perkins-vowelless-syllables--YYMMDD_HHMM.tsv` (tokens in which Perkins wrote
a syllable without a vowel: a misspelling, or a word that is not Spanish),
`perkins-FAILED--YYMMDD_HHMM.tsv`.

## Exit codes

0 done; 1 a document failed; 2 refused; 130 interrupted (the documents in
progress write nothing; the same command resumes).

## Platform

Linux and macOS. Python 3.9 or later and the `perkins` program.

## Changelog

- 1.0.0 (261119): first version, from the per-corpus Perkins script
  2.0.6: the columns chosen on the command line and named after their
  options (1 to any number); the columns of 070 found by name; a text
  without a `.times.tsv` gets `NAME.lines.tsv`, one row per line; the
  stand-ins of `stand-ins.tsv` sent to Perkins as a pause (Perkins spelled
  out the letters of a stand-in it did not know).
