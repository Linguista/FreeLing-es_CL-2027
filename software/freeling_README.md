# freeling_README.md

Documents `freeling.py` 1.2.0, the tagging command of FreeLing es-CL 2027.

## Purpose

Tags a corpus with FreeLing es-CL 2027, step by step, into numbered stage
folders, the same for every corpus:

| Stage | Step | What it adds | Needs |
|---|---|---|---|
| `060-FreeLing-Tagged` | `--freeling` | FreeLing 4.2: lemma, part of speech, word sense and dependency parse of every token | the texts |
| `070-Universal-Dependency-Tagged` | `--ud` | Universal Dependencies part of speech (UPOS) and features (FEATS), translated from FreeLing's tags | 060 |
| `080-Perkins-Tagged` | `--perkins` | Perkins: phonological transcriptions, one column per set of Perkins options (not for written-old) | 060, 070 |
| `400-Parquet` | `--parquet` | a Parquet token store of the last stage made (080, 070 or 060) | 060 |

Stage numbers kept for later steps: 090 topic analyses, 100 sentiment
analyses, 110 emotion analyses, 120, 130, 140 ... further analyses, and
500-Database for your own database tables and their Parquet copies. A step
not run leaves no folder.

**Only the steps named on the command line run, and at least one is
required.** With none, or with `-h` or `--help`, it lists the steps. Steps
named together run in the order of the table, whatever the order on the
command line. A step whose earlier stage has not been made is refused, and
the refusal names the stages it needs:

```text
REFUSED: --perkins (080-Perkins-Tagged) needs 060-FreeLing-Tagged, 070-Universal-Dependency-Tagged, not made yet. Make 060-FreeLing-Tagged, 070-Universal-Dependency-Tagged first, or name --freeling --ud in the same run.
```

A stage is made when its folder holds `columns.tsv`.

## Usage

Set a corpus up once, then run the steps:

```bash
freeling.py --new INTERVIEWS --kind speech --input /data/interviews/text
freeling.py INTERVIEWS --freeling --dry-run
freeling.py INTERVIEWS --freeling --ud --perkins --parquet
freeling.py --list
```

Executes by default; `--dry-run` checks everything and writes nothing.

## The corpus folders

The release folder (the folder holding `software/` and `data/`) has a
folder `corpora/`, with one folder per corpus. `corpora/` may be a real
folder or a link to a folder elsewhere (a larger disk, say); either way the
build of the release carries it over and never uploads it.

```text
FreeLing-es_CL-2027/
  corpora/
    README.md
    INTERVIEWS/
      README.md
      input/
        README.md
        speech -> /data/interviews/text        the corpus root
      informal.txt                             written-modern only, optional
      060-FreeLing-Tagged/                     made by --freeling
        README.md  columns.tsv  _processing-records/  ...the .conll files
      070-Universal-Dependency-Tagged/         made by --ud
      080-Perkins-Tagged/                      made by --perkins, or a link
      400-Parquet/                             made by --parquet
      _processing-records/                     the record of every run
```

- **`input/`** holds exactly one link, named after the kind of text, that
  leads to the corpus root: the folder holding the corpus texts, in any
  number of subfolders. `--new` makes it, as a relative link. By hand:

  ```bash
  mkdir -p /path/to/FreeLing-es_CL-2027/corpora/INTERVIEWS/input
  ln -s ../../../../../data/interviews/text /path/to/FreeLing-es_CL-2027/corpora/INTERVIEWS/input/speech
  ```

  A real folder of texts in place of the link works too.
- **The stage folders** are made by the steps, inside the corpus folder.
  To keep a stage on another disk, or to use a stage made earlier, make the
  stage folder a link before the step runs: `--link-stage 060=/big/disk/060`
  (with `--new`, or with the corpus name alone). A link to a folder that
  does not exist yet has that folder made when the step first runs.
- **No corpus may be called** `data`, `software`, `packaging` or `corpora`
  (in any capitalization), nor start with `.` or `_`: `--new` refuses it.
- **Every folder made here has a README.md**: what is in it, how it was
  made (the command, the programs and their versions), and what it is used
  for next. The folders inside a stage mirror the folders of the corpus
  root and hold only the tagged files.
- **`_processing-records/`**, in the corpus folder and in each stage,
  holds the logs, failure lists and reports of each run, named with its
  date and time. It holds no corpus files and is never read as texts.

## The texts

Plain text, UTF-8, ending in `.txt` (or the extension given with `--ext`),
**one sentence or utterance per line**: every line end ends a sentence, so
a sentence broken across two lines is read as two. No markup: a tag such as
`<p>` is read as words and punctuation. Blank lines are fine. A text that is
not UTF-8 fails, with nothing written for it.

For speech, a `NAME.times.tsv` beside `NAME.txt` (the times of each
utterance, with the columns `interval`, `char_start` and `char_end` at
least) is copied beside each tagged `NAME.conll`, and Perkins writes one row
of running transcription per utterance from it. `--require-sidecars`
refuses a run in which any text lacks one.

The texts are never changed.

## The kinds of text and their configs

| Kind (the link in `input/`) | Text | Config |
|---|---|---|
| `speech` | transcribed speech, one utterance per line | `es-cl-speech.cfg`: a capitalized word at the start of an utterance can be a name; nn and nnn are hesitations |
| `written-modern` | modern writing | `es-cl.cfg`; the informal texts `es-cl-informal.cfg` |
| `written-19th-century` | 19th-century writing | `es-cl-19th-century.cfg`: the old Chilean spellings (jente, i, rei), vos also polite, the -is forms also vosotros |
| `written-old` | Old Spanish (medieval and Golden Age) | FreeLing Old, `es-old.cfg`, as FreeLing ships it: no parse, no user map |

The configs are those installed with FreeLing es-CL 2027 in FreeLing's
`config/` folder (written by `freeling_escl_configs.py`; see its README for
what each setting does). Compound analysis is off in every one of them.

**Not yet tested on real corpora:** 19th-century writing and Old Spanish.
Both work on test texts; neither has been run on a whole corpus and
checked.

## Informal writing (written-modern only)

Chat spellings such as q (que), x (por), d (de), tas (estás) and tar
(estar) are read as those words only in informal writing: chat, forums,
e-mail, newsgroups, social media. Elsewhere q is a letter (la letra q) or a
false start (q... qué). So a written-modern corpus may name its informal
texts in `informal.txt`, in the corpus folder:

```text
# informal.txt: the informal texts of this corpus
Pers/Chat
Pers/Forums/Pelotillehue
Pers/Mail/2004-11-08.txt
/data/corpus/root/Usenet
```

- One path per line: a folder (every text under it) or a single text.
- Relative to the corpus root, or absolute (inside the corpus root).
- Lines starting with `#` are comments; blank lines are ignored.
- **Every text not listed is formal**, and is tagged with `es-cl.cfg`.
- **No two paths may overlap**: a path inside another listed path, or the
  same path twice, refuses the run, naming both lines.
- A path that does not exist refuses the run.
- A corpus of another kind with an `informal.txt` is refused.

**Be careful.** A folder of chat left out of `informal.txt` is tagged as
formal writing, and its q, x and tas are read as letters and nouns; a
newspaper folder listed by mistake has its q read as que. The start of every
run, and the stage README, list how each branch of the corpus is tagged:

```text
how the corpus is tagged (texts found, done or not):
   informal       1204  Pers/Chat
   formal        38512  Prof
```

Check it before tagging. A folder added to `informal.txt` after it was
tagged keeps its old files (a finished document is skipped): tag it again
with `freeling.py CORPUS --freeling --only Pers/Chat --redo`.

## The stand-in tokens

A stand-in token stands for something removed from a text or not written
in it. FreeLing es-CL 2027 knows five, listed in its `stand-ins.tsv`
(installed as `es/es-cl/stand-ins.tsv` in FreeLing's data folder):

| Form | Tag | Meaning |
|---|---|---|
| XXXREDACTEDXXX | Fz | a redacted identifier: a name, a number, an address |
| XXXUNINTELLIGIBLEXXX | Fla | speech that could not be made out |
| XXXNONSPEECHXXX | Flt | a non-speech event: laughter, a cough, a noise |
| XXXURLXXX | Fz | a web address, removed |
| XXXEMAILADDRXXX | Fz | an e-mail address, removed |

**How FreeLing treats them.** Every stand-in is sent to FreeLing in lower
case (`xxxredactedxxx`): FreeLing's name recognizer joins a capitalized one
with the words around it (`XXXREDACTEDXXX_poh`) and the words vanish into a
false name. The config's user map tags the lowercase form with the tag
above, before any other module, and the original form is written back in
`FORM`; `LEMMA` keeps the lowercase form. Fz is FreeLing's "other symbol";
Fla and Flt are its tags for { and }, which plain text rarely holds. In
070, every stand-in has UPOS X and a feature `StandIn` (Redacted,
Unintelligible, NonSpeech, Url, EmailAddr); in 080, Perkins reads it as a
pause.

**Any other form of that shape** (XXX, capital letters, XXX) fails its
text, naming the form, so that a new stand-in never goes through untagged.
A text that already holds a stand-in in lower case fails too.

**To add a stand-in**, add a line to `stand-ins.tsv` in the build's sources
(`sources/escl-sources/stand-ins.tsv`): the form, a tab, its tag, a tab,
what it means. Then rebuild the release and install it again
(`freeling_escl_build.py`, `freeling_escl_deploy.py`): every config's user
map is written from that file. Without FreeLing es-CL 2027's tools, add the
line `^xxxnewnamexxx$ xxxnewnamexxx Fz` to each user map in
`es/es-cl/usermap/` and the line to the installed `stand-ins.tsv`.

The FreeLing Old config (written-old) has no user map: a written-old text
holding a stand-in fails.

## Spellings rewritten on the way to FreeLing

In every kind of text, and the texts are never changed:

| In the text | Sent to FreeLing | Becomes |
|---|---|---|
| `Bs. As.`, `Bs.As.` | `BsAs` | buenos_aires, a place |
| `wo'n`, `weo'n` (any apostrophe) | `weón` | huevón |
| `pa'l` (any apostrophe) | `pal` | para + el, split like del and al |
| the comma of a comma multiword (te conozco, mosco; igual, pascual) | a blank | the multiword without the comma (te_conozco_mosco) |

Each is followed by blanks up to the length of the original, so every
token keeps its exact `SPAN_BEGIN` and `SPAN_END`; the last token made from
a rewritten spelling ends where the original ended. The comma multiwords
are listed in `freeling_comma_multiwords.txt`, beside this script.

## Tagging is iterative

FreeLing es-CL 2027 tags Chilean Spanish far better than FreeLing alone,
but no tagger knows every word of a corpus. Tag a sample, read it, and
correct what is wrong where it is decided: a missing word or reading in the
dictionary sources, a multiword, a name class, a probability. Rebuild,
install, and tag again (`--redo`). Each round makes the next better; the
lists in `_processing-records/` (failures, Perkins fallbacks, words with a
syllable without a vowel, the evaluative report of 070) show where to look.

## columns.tsv

Every stage folder holds `columns.tsv`, one row per column of its files:

| Field | |
|---|---|
| `position` | the column's number, from 1 |
| `name` | its name (`FORM`, `UPOS`, `PERKINS_NT_OA` ...) |
| `step` | the step that added it (`--freeling`, `--ud`, `--perkins`, `--parquet`) |
| `option` | what it holds: the FreeLing column, the UD rule, the Perkins options |
| `program` | the program and script, with their versions |

## The steps

### 060: `--freeling`

One server per config, loaded once (the models take minutes and about
2 GB), with `--workers` analyzers (default: every logical CPU) and as many
texts sent at once; a written-modern corpus with informal texts has two
passes, one server each. One `NAME.conll` per text, TAB-separated, a blank
line after each sentence; the columns are those of FreeLing es-CL 2027's
`es-cl-conll-columns.cfg`: `ID SPAN_BEGIN SPAN_END FORM LEMMA TAG SENSE
ALL_SENSES DEPHEAD DEPREL LEX_PROB TAG_PROB`. `LEX_PROB` is the probability
of the selected reading among the readings of the word, out of context;
`TAG_PROB` the probability the tagger gives the selected tag in its
sentence (0 to 1; `-` when the tagger did not compute it). A low `TAG_PROB`
marks a word the tagger hesitated over: such words are where to look for
tagging errors first. Each output is written to `.part` and renamed;
the `.times.tsv` goes in before the `.conll`, which marks a document done.

Refused before any work: a missing FreeLing program, config, dictionary,
name recognizer or user map; a config with a non-ASCII character (FreeLing
stops on it) or compound analysis on; a FreeLing library without the
changes of `software/patches/` (the name classes for speech and modern
writing, the known roots of the affix analysis for every kind, the
probability columns when the columns file names them); an empty
corpus; a corpus that has shrunk by more than a tenth since the last full
scan (`--allow-shrink` goes on); a port already in use; an output, the
corpus folder's README, a stage README, a `columns.tsv` or the document
count that cannot be replaced (immutable or read-only). The dry run makes
the same check for every step named, so a run that passes its dry run does
not stop on such a file. The message names each file and gives the command
that clears the flag on exactly those files; this tool never clears it.

A failed document (an unknown stand-in, FreeLing's output not matching the
columns, a timeout, a non-UTF-8 text) is listed in
`_processing-records/freeling-FAILED--YYMMDD_HHMM.tsv` and nothing is
written for it. After `--max-consecutive-failures` failures in a row the
server is checked, and a dead server stops the run (exit 3). The same
command resumes: finished documents are skipped.

Options: `--workers N`, `--dep lstm|treeler|txala` (default lstm),
`--port N` (default 50005), `--host`, `--use-running-server` (tag through a
server started with `freeling_server.py`), `--doc-timeout S` (3600),
`--startup-timeout S` (600), `--max-consecutive-failures N` (5),
`--allow-shrink`, `--redo-before YYMMDD_HHMM` (redo only outputs older than
that), `--require-sidecars`.

### 070: `--ud`

Described in `freeling_ud_README.md`.

### 080: `--perkins`

Described in `freeling_perkins_README.md`. Needs the `perkins` program
(https://github.com/Linguista/Perkins, GNU AGPL 3.0), version 2.0.41 or
later, on the PATH or given with `--perkins-bin`. The columns are named
after their Perkins options and can be chosen:

```bash
freeling.py INTERVIEWS --perkins --perkins-columns=-oa --perkins-columns="-nt -oa" --perkins-word-alone="-nt -oa"
```

Write the `=`: an option that begins with `-` is otherwise read as one of
`freeling.py`'s own.

### 400: `--parquet`

Described in `freeling_parquet_README.md`. Needs pyarrow.

## The options for every step

| Option | |
|---|---|
| `--dry-run` | check everything, write nothing |
| `--redo` | redo documents already done (default: resume) |
| `--limit N` | at most N documents (folders for 400) per step |
| `--only FOLDER` | only the texts under this folder of the corpus root |
| `--ext EXT` | the extension of the texts (default `.txt`) |
| `--home DIR` | the release folder (default: the folder above `software/`) |
| `--freeling-bin DIR` | the folder of FreeLing's `analyze` and `analyzer_client` (default: on the PATH) |
| `--share DIR` | FreeLing's data folder (default: `share/freeling` beside that bin folder) |
| `--lib FILE` | the FreeLing library (default: `lib/libfreeling.so` there) |
| `--no-colour` | no colours |
| `--version` | print the version |

A run with `--only` or `--limit` sees part of the corpus and leaves an
existing stage README as it was.

## Exit codes

0 done; 1 some documents failed (listed in `_processing-records/`); 2
refused before any work; 3 stopped, the FreeLing server died; 130
interrupted (the same command resumes).

## Platform

Linux and macOS. Python 3.9 or later; FreeLing 4.2 with FreeLing es-CL
2027; pyarrow for `--parquet`; Perkins for `--perkins`. Needs
`freeling_common.py`, `freeling_ud.py`, `freeling_perkins.py`,
`freeling_parquet.py` and `freeling_comma_multiwords.txt` beside it.

## Tested

261119, on test corpora of the four kinds, with FreeLing 4.2 built with the
changes of `software/patches/` and the data of FreeLing es-CL 2027:

- speech (a `.times.tsv` beside the text): stand-ins written back in FORM
  and tagged Fz and Flt; `nn` an interjection; `pa'l` as para + el with the
  spans of `pa'l`; `weo'n` as weón (huevón); `igual, pascual` joined; 060,
  070, 080 (with the utterance file) and 400 made; the Parquet store read
  by DuckDB;
- written-modern with an `informal.txt` (relative, then absolute): two
  passes; q as que and tas as estar in the informal text; XXXURLXXX and
  XXXEMAILADDRXXX tagged Fz; `Bs. As.` as BsAs (buenos_aires); a text
  holding XXXFOOXXX failed, naming it, and was the only one to tag on the
  rerun; Perkins with chosen columns writes `NAME.lines.tsv`;
- 19th-century: jente as gente, i as y, rei as rey; Old Spanish: tagged by
  FreeLing Old, 070 made from it, `--perkins` refused;
- refused: a reserved corpus name (data, Corpora); a step without its
  earlier stage; overlapping informal paths; an `informal.txt` in a
  19th-century corpus; no step named.

- 261120, version 1.1.0, same four test corpora, FreeLing 4.2 with the
  tag-probabilities change: speech 060 with 12 columns, 070 with 14, 080
  with 23; the first ten columns of 060 and every UD and Perkins column
  byte for byte as 1.0.0 with the ten-column file; written-modern (both
  passes), 19th-century and Old Spanish with two probabilities from 0 to 1
  on every token line; the Parquet store holds both as numbers; with a
  library without the change, refused, naming `LEX_PROB` and `TAG_PROB`.

261121, on a test corpus whose folder is reached through a link, as
the release's `corpora` is: with the immutable flag on the corpus folder's
README, the dry run and the run both refuse (exit 2), name the file and
give the command for it, and leave no `.part` file; with the flag on the
READMEs of two stages named in one run, both are named at once; with a
stage link whose folder does not exist yet, the folder is made where the
link leads and nothing is made beside the release.

## Changelog

- 1.2.0 (261121): the dry run and the run check, before anything is
  written, every file the run rewrites outside the documents: the corpus
  folder's README, and the README and `columns.tsv` of every step named
  (the dry run of 1.1.0 checked only the first step's, and the run then
  ended with a Python error on the corpus folder's README); the document
  count of 060 is checked too. The message names each file and gives the
  command for exactly those files, where 1.1.0 suggested clearing the flag
  on the whole stage folder. With `freeling_common.py` 1.3.0, a stage link
  whose folder does not exist yet has it made where the link really leads.
- 1.1.0 (261120): the two probability columns. The release's columns file
  names `LEX_PROB` and `TAG_PROB` after its ten earlier columns
  (`freeling_escl_configs.py` 2.1.0), so 060 has twelve columns, 070
  fourteen, and 080 two more than before; `columns.tsv` and the 060 README
  say what the two hold; a FreeLing library without the tag-probabilities
  change is refused before any work (`freeling_common.py` 1.1.0); the
  Parquet step stores them as numbers (`freeling_parquet.py` 1.1.0). The
  first ten columns of 060 and the columns of 070 and 080 are byte for
  byte what 1.0.0 wrote. A stage tagged before this has ten columns: tag
  it again with `--redo`.
- 1.0.0 (261119): first version, replacing `freeling_tag_corpus.py`
  2.11.0 and the per-corpus scripts of the UD, Perkins and Parquet steps
  with one command for every corpus: the corpus folders under `corpora/`,
  the kinds of text, `informal.txt` with any number of paths (absolute or
  from the corpus root, no overlap), the stand-ins read from the installed
  `stand-ins.tsv` (XXXURLXXX and XXXEMAILADDRXXX are new, and any other
  XXX...XXX form now fails its text), the fixed stage numbers, the steps
  named on the command line, `columns.tsv` and a README in every folder.
  Not carried over: mounting a corpus image (`--sqfs`, `--verify`,
  `--no-mount`) and gzip output.
