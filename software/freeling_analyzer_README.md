# freeling_analyzer_README.md

Documents `freeling_analyzer.py` 1.0.0.

## Purpose

Analyzes texts with FreeLing es-CL 2027 and writes the same TAB-separated
CoNLL as `freeling.py --freeling`: the stand-in tokens sent in lower case
and written back in FORM, the three rewritten spellings (Bs. As., weo'n,
pa'l), the commas of the comma multiwords sent as blanks, every character
offset exact. For a few texts, or to try a sentence; for a corpus, use
`freeling.py`.

## Usage

```bash
freeling_analyzer.py --kind speech interview.txt
freeling_analyzer.py --kind written-modern --informal chat.txt --out chat.conll
echo "¿Cachái lo que te digo?" | freeling_analyzer.py --kind written-modern
freeling_analyzer.py --kind speech --port 50005 a.txt b.txt --out-dir tagged
```

On its own it starts FreeLing for the run, which takes minutes for the
models. With `--port N` it sends each text to a server started with
`freeling_server.py`; give the same `--kind` (and `--informal`) the server
was started with.

| Option | |
|---|---|
| texts | text files, UTF-8, one sentence or utterance per line; none: standard input |
| `--kind` | speech, written-modern, written-19th-century or written-old (required) |
| `--informal` | informal modern writing (written-modern only) |
| `--port N`, `--host HOST` | through a running server |
| `--out FILE` | write here (one text only); default: standard output |
| `--out-dir DIR` | write `NAME.conll` for each `NAME.txt` |
| `--dep` | lstm (default), treeler, txala |
| `--timeout S` | per text (default 3600) |
| `--freeling-bin DIR`, `--share DIR`, `--lib FILE` | where FreeLing is |

A text that fails (an unknown stand-in, not UTF-8, FreeLing's output not
matching the columns) is reported on standard error and skipped; the others
are written.

## Exit codes

0 done; 1 a text failed; 2 refused.

## Platform

Linux and macOS. Python 3.9 or later, standard library only.

## Tested

261119: standalone on standard input (speech), and through a server on
port 50007 (written-modern, informal): the output through the server is
byte-identical to what `freeling.py --freeling` wrote for the same text.

## Changelog

- 1.0.0 (261119): first version.
