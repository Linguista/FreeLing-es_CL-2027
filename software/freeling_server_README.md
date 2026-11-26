# freeling_server_README.md

Documents `freeling_server.py` 1.0.0.

## Purpose

Starts FreeLing's analyzer as a server with the FreeLing es-CL 2027 config
of a kind of text, and keeps it up until Ctrl-C; then stops it with every
analyzer it started. Loading FreeLing takes minutes and about 2 GB (the
dictionary, the name classifier, the LSTM parser, UKB); a server pays that
once, and then answers `freeling_analyzer.py --port N` and `freeling.py
--freeling --use-running-server` as often as needed.

## Usage

```bash
freeling_server.py --kind speech
freeling_server.py --kind written-modern --informal --port 50006 --workers 8
freeling_server.py --stop --port 50005
```

It runs in the foreground: start it in a terminal of its own (or a tmux,
byobu or screen window). `--stop` stops a server started elsewhere, found by
its port (FreeLing's own `analyze stop` wants the process id).

| Option | |
|---|---|
| `--kind` | speech, written-modern, written-19th-century or written-old |
| `--informal` | informal modern writing: `es-cl-informal.cfg` (written-modern only) |
| `--port N` | default 50005 |
| `--workers N` | analyzers at once (default: every logical CPU) |
| `--dep` | lstm (default), treeler, txala |
| `--log FILE` | the server's log (default: `freeling-server--PORT.log` in the current folder) |
| `--startup-timeout S` | default 600 |
| `--stop` | stop the server on `--port` |
| `--freeling-bin DIR`, `--share DIR`, `--lib FILE` | where FreeLing is (as for `freeling.py`) |
| `--dry-run` | check the config and print the command; start nothing |

The server is started exactly as `freeling.py` starts it: the config of the
kind, `--flush` (every line end ends a sentence), CoNLL output with the
columns of `es-cl-conll-columns.cfg`, `--outlv dep` and the parser (FreeLing
Old: `--outlv tagged`, no parser). Every check `freeling.py` makes of the
config and the library is made first.

## Exit codes

0 stopped cleanly; 1 the port is still in use after stopping; 2 refused; 3
the server exited or did not start.

## Platform

Linux and macOS. Python 3.9 or later, standard library only.

## Changelog

- 1.0.0 (261119): first version.
