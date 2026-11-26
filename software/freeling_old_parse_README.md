# freeling_old_parse_README.md

Documents `freeling_old_parse.py` 1.0.0.

## Purpose

Parses Old Spanish texts (medieval and Golden Age) through a temporary modernization. FreeLing Old (`es-old.cfg`) has only FreeLing's rule-based parser, written for modern Spanish, and it reads the old forms badly: in "Et dixo el rey que la muger era fermosa." it took "que la muger era fermosa" for a relative clause on "rey" and left "muger" unattached. FreeLing's modern parser (the LSTM parser of `es-cl.cfg`) reads the same sentence written in modern forms correctly. So:

1. FreeLing Old tags each text, with its own dictionary and tagger: every word gets a lemma and a tag ("dixo", "decir" VMIS3S0; "muger", "mujer" NCFS000; "fermosa", "hermoso" AQ0FS00), with its character span and the two probability columns.
2. Every word FreeLing Old knows gets its modern form, from its lemma and tag and the modern Spanish dictionary: "decir" VMIS3S0 is "dijo", "mujer" NCFS000 "mujer", "hermoso" AQ0FS00 "hermosa". FreeLing's own Spanish dictionary (standard spellings only) is asked first, the Chilean one second. Where the dictionary has several forms for one lemma and tag, the old form itself is kept if it is one of them, else the form closest to it in spelling ("fuesse": "fuese", not "fuera"). Punctuation, numbers, dates and names keep their form, and so does a word with no modern form ("et", "ca"). A word FreeLing Old left joined ("dixole": "decir+le", VMIS3S0+PP3CSD0) is given to the parser as its pieces ("dijo", "le").
3. FreeLing's modern parser parses the modernized text, every sentence of every text in one run (the parser takes about half a minute to load).
4. The parse is written onto the original words, token for token: the result has the original forms and spans. A joined word gets the head and relation of its first piece.

The modernization is thrown away, or kept beside the result (`--sidecar`).

**The tags.** With `--tags old` (the default) the result has FreeLing Old's lemmas and tags, and the parser sees the modern forms with those tags. With `--tags modern` the modern tagger tags the modernized text too, and its lemmas, tags and probabilities go into the result: "era", which FreeLing Old tags as 1st person in "la muger era fermosa", comes out 3rd person. A word with no modern form keeps FreeLing Old's lemma and tag even then (the modern tagger read "et" as a noun). FreeLing Old's own lemmas and tags are in the sidecar.

Measured on nothing yet: how well the modern parser parses modernized old texts has not been checked on a corpus.

## Usage

```bash
freeling_old_parse.py poema.txt
freeling_old_parse.py --sidecar cantar.txt --out cantar.conll
freeling_old_parse.py --tags modern --sidecar a.txt b.txt --out-dir parsed
echo "Et dixo el rey que la muger era fermosa." | freeling_old_parse.py
```

| Option | |
|---|---|
| texts | text files, UTF-8; none: standard input |
| `--tags old`, `--tags modern` | the lemmas and tags of the result: FreeLing Old's (default) or the modern tagger's on the modernized text |
| `--sidecar` | keep the modernization: `NAME.modern.tsv` beside each result (needs `--out` or `--out-dir`) |
| `--flush` | every line end ends a sentence (verse with one sentence per line) |
| `--out FILE` | write here (one text only); default: standard output |
| `--out-dir DIR` | write `NAME.conll` for each `NAME.txt` |
| `--timeout S` | per FreeLing run (default 3600) |
| `--freeling-bin DIR`, `--share DIR`, `--lib FILE` | where FreeLing is (as for `freeling.py`) |
| `--dry-run` | check FreeLing, the configs and the texts, say what would be written, write nothing |

The result has the release's twelve CoNLL columns, separated by tabs: `ID SPAN_BEGIN SPAN_END FORM LEMMA TAG SENSE ALL_SENSES DEPHEAD DEPREL LEX_PROB TAG_PROB` (no word senses: the two sense columns are `-`).

The sidecar has one row per piece of a word: `ID` (the word's), `PART` (1, or 2 and on for the pieces of a joined word), `FORM`, `MODERN_FORM`, `OLD_LEMMA` and `OLD_TAG` (FreeLing Old's), `MODERN_LEMMA` and `MODERN_TAG` (the modern tagger's, with `--tags modern`; else `-`), and `SOURCE`: `es` or `es-cl`, the dictionary the modern form came from, or `kept`; `+split` for a piece of a joined word.

A sentence the parser gives back with another number of tokens is written without a parse (`DEPHEAD` and `DEPREL` `-`), and the run says how many there were; none did in the tests.

## Exit codes

0 done; 1 FreeLing failed (it says where); 2 refused before any work (FreeLing, a config or a text not found, or options that do not go together).

## Platform

Linux and macOS; Windows with the zip's `analyze.bat` on the PATH (not tested there). Python 3.9 or later, standard library only. FreeLing 4.2 with FreeLing es-CL 2027, and `freeling_common.py` beside it. It does not need FreeLing Old's parser (change 13 of `packaging/patch-freeling.sh`): FreeLing Old only tags.

## Tested

261126, version 1.0.0, on Ubuntu 24.04 with the 261126c package: "Et dixo el rey que la muger era fermosa. Dixole entonces que fuesse a la cibdad." With `--tags old`: "dixo" the root, "rey" its subject, "muger" the subject of "era", "fermosa" its predicate, "cibdad" ("ciudad") under the preposition "a"; "Dixole" written back as one token with the head and relation of "dijo". With `--tags modern`: the same tree, "era" 3rd person (VSII3S0), "et" kept as FreeLing Old's conjunction. Run twice with `--tags old`, the results were byte for byte the same.

## Changelog

- 1.0.0 (261126): first version.
