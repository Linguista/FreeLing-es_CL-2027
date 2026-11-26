# freeling_common_README.md

Documents `freeling_common.py` 1.3.0.

## Purpose

What `freeling.py`, `freeling_server.py`, `freeling_analyzer.py` and the
steps of `freeling.py` share, so that every one of them tags a text the
same way:

- where FreeLing is: its programs (`analyze`, `analyzer_client`), its data
  folder and its library, found from `analyze` on the PATH or given with
  `--freeling-bin`, `--share` and `--lib`;
- the kinds of text and the config of each, and the checks of a config
  before any work (its dictionary, name recognizer and user map exist; no
  non-ASCII character; compound analysis off; the LSTM parser's model);
- the checks of the FreeLing library (the changes of `software/patches/`),
  among them that it writes the probability columns `LEX_PROB` and
  `TAG_PROB` when the columns file names them;
- the stand-in tokens, read from the installed `stand-ins.tsv`;
- what is done to a text on the way to FreeLing and to FreeLing's output on
  the way back (`Sender`): the stand-ins lowercased and written back in
  FORM, the three rewritten spellings, the commas of the comma multiwords,
  FreeLing's space-padded CoNLL turned into TAB-separated fields with every
  line checked against the columns;
- the server: started in its own process group, its log in a file, stopped
  with every analyzer it started; orphaned analyzers reaped after a
  timeout;
- the corpus folders: the corpus names refused, `input/`, `informal.txt`
  (paths inside the corpus, existing, not overlapping), the stage folders
  (a link to a folder not yet there has it made, the link read from the
  folder it really is in);
- the files a run rewrites that cannot be replaced, found before anything
  is written, and the command that clears the flag on exactly those files;
- `columns.tsv` and the README of every folder made.

## Usage

A module: it does nothing when run. The scripts beside it import it.

## Platform

Linux and macOS. Python 3.9 or later, standard library only.

## Changelog

- 1.3.0 (261121): two faults found by the first tagging of a whole corpus. A stage link whose folder did not exist yet was read from the path that was typed, so when the corpus folder was itself reached through a link (the release's `corpora`), the folder was made in the wrong place and the step stopped with an error; the link is now read from the folder it really is in, and the step stops with a plain message if the link still does not lead to the folder made. New: `run_blockers`, the corpus folder's README and each step's stage README and `columns.tsv` checked for the immutable flag before anything is written, and `unlock_lines`, the command that clears the flag on exactly the files named, never on a folder.
- 1.2.0 (261121): without `--freeling-bin`, the tools use the release's own FreeLing when there is one: `third-party/freeling/` in the folder that holds the tools, or in the folder two levels above the release folder. Only when there is none is the FreeLing of the PATH used, as before.
- 1.1.0 (261120): when the columns file names `LEX_PROB` or `TAG_PROB`, the
  FreeLing library must have the tag-probabilities change: a run with a
  library without it is refused before any work, naming the columns
  (`freeling.py`, `freeling_server.py` and `freeling_analyzer.py` all get the
  check).
- 1.0.0 (261119): first version, from `freeling_tag_corpus.py` 2.11.0.
