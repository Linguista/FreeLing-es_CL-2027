# freeling_escl_configs_README.md

Documents `freeling_escl_configs.py` 2.0.0.

## Purpose

Writes the FreeLing configs of FreeLing es-CL 2027, one per kind of text,
their user maps and their CoNLL columns file. `freeling_escl_build.py` calls
it at every build, so the configs in the release, the configs the packages
install and the configs every corpus is tagged with are the same files.

It replaces `the former config writer` (1.6.0, retired 261119), which wrote
separate configs for the corpora while the release carried three thin ones
(FreeLing's es-cl config with the dictionary swapped: no Chilean name
recognizer, no user map, so the chat readings of informal writing were never
read).

## What a config is

FreeLing's analyzer reads one config file per run. It is a list of settings:
which modules run (multiwords, numbers, dates, the name recognizer, the
tagger, the parser ...) and which data file each one reads. The kinds of
text differ in five settings only: the dictionary, the probabilities and
multiwords, the name recognizer, the user map, and whether every line end
ends a sentence. So every config is FreeLing 4.2's own es-cl config with the
same changes, and then the few that set its kind apart.

| Config | Kind of text | Dictionary | Probabilities and multiwords | Name recognizer | Its user map adds |
|---|---|---|---|---|---|
| `es-cl.cfg` (the default) | modern writing | `es/es-cl/dicc.src` | `es/es-cl/` | `es/es-cl/np.dat` | nothing |
| `es-cl-informal.cfg` | informal modern writing (chat, forums, e-mail, social media) | `es/es-cl/informal/dicc.src` (the default with the spoken reduced forms: cansá, pescao, he comío) | `es/es-cl/` | `es/es-cl/np.dat` | every line of `es/es-cl/usermap-informal.dat`, the chat readings (q as que, x as por, tas as estás ...) |
| `es-cl-speech.cfg` | transcribed speech, one utterance per line | `es/es-cl/dicc.src` | `es/es-cl/` | `es/es-cl/np-speech.dat` (a capitalized word at the start of an utterance is a name) | nn and nnn as the hesitation (an interjection) |
| `es-cl-19th-century.cfg` | 19th-century writing | `es/es-cl/19th-century/dicc.src` (the old Chilean spellings, vos also polite, the -is forms as vosotros) | `es/es-cl/19th-century/` | FreeLing's own, `es/nerc/nerc/nerc.dat` | nothing |

Old Spanish (medieval and Golden Age texts) is FreeLing Old, `es-old.cfg`,
installed exactly as FreeLing ships it; its compound analysis is already off.
It is not written here.

### The settings every config has

| Setting | Value | Why |
|---|---|---|
| `TagsetFile` | `es/es-cl/tagset.dat` | the Chilean tagset: FreeLing's, plus a final V for voseo |
| `QuantitiesFile` | `es/es-cl/quantities.dat` | the peso is the Chilean peso; UF and UTM added |
| `CompoundAnalysis` | `no` (and `CompoundFile` commented out) | FreeLing's compound module splits a word missing from the dictionary into two that are in it. On real corpora nearly everything it built was wrong: pentecostal as pente + costal (the lemma repente_costal), veinti as ver + inti, noso as no + so, fami as fa + mi, toballa as toba + ll, docientos as do + ciento, down as do + huevón, face as fa + ce, resort as re + sor, fashion as flash + ion |
| `AlwaysFlush` | `yes` | every line end ends a sentence: give the text one sentence or utterance per line |
| `OutputLevel`, `OutputFormat`, `OutputConllConfig` | `dep`, `conll`, `config/es-cl-conll-columns.cfg` | dependency parses, as CoNLL with twelve columns (the ten of the parse and the two probability columns, `LEX_PROB` and `TAG_PROB`). FreeLing 4.2's analyzer ignores `OutputLevel`: pass `--outlv dep`. For FreeLing's own format, pass `--output freeling` |
| `NEClassification` | `yes` | names are classed as person, place, organisation or other |
| `SenseAnnotation` | `ukb` | word senses ranked by UKB over the Spanish WordNet |
| `TaggerForceSelect` | `retok` | the tagger may retokenize |
| `DependencyParser`, `DepLSTMFile` | `lstm`, `es/dep_lstm/params-es.dat` | FreeLing's LSTM parser, chosen by agreement between parsers (head agreement with treeler 87.4%, against 71.7% for txala) |
| `UserMap`, `UserMapFile` | `yes`, `es/es-cl/usermap/<config>.dat` | the config's user map |

Every other line is FreeLing 4.2's es-cl config as FreeLing ships it. A
config must be pure ASCII: FreeLing stops on any other character in one.

## The user maps and the stand-in tokens

A user map fixes a word's readings before any other module runs: no later
module adds a reading, and the dictionary is not read for that word. Every
map holds:

- **The stand-in tokens** of `es/es-cl/stand-ins.tsv`, lowercased, each with
  its tag and itself as its lemma.
- **novela, vela and velo**, always common nouns. FreeLing read velo as ver
  + lo and novela as novar + la.

A stand-in token stands for something removed from a text or not written in
it. The tagger (`freeling_tag_corpus.py`) sends every one to FreeLing in
lowercase, because FreeLing's name recognizer joins a capitalized stand-in
with the words around it (XXXURLXXX_poh). It then writes the original form
back into the FORM column; LEMMA keeps the lowercase form.

| Form | Tag | Meaning |
|---|---|---|
| XXXREDACTEDXXX | Fz | a redacted identifier: a name, a number, an address |
| XXXUNINTELLIGIBLEXXX | Fla | speech that could not be made out |
| XXXNONSPEECHXXX | Flt | a non-speech event: laughter, a cough, a noise |
| XXXURLXXX | Fz | a web address, removed |
| XXXEMAILADDRXXX | Fz | an e-mail address, removed |

Fz is FreeLing's "other symbol"; Fla and Flt are its tags for { and }, which
plain text does not otherwise contain.

**To add a stand-in**, add a line to `stand-ins.tsv` in the build's sources:
the form (XXX, a name in capital letters A to Z, XXX), a tab, the tag, a tab,
and what it means. Then rebuild and redeploy. The tagger refuses a text that
holds a form of that shape not listed in the file, and names the form, so a
new stand-in can never pass through untagged.

## Usage

The build calls it; nothing else needs to. On its own, it reads a release
folder and writes the same files into another folder, to inspect them or to
test a change before a rebuild:

```bash
freeling_escl_configs.py --release /path/to/FreeLing-es_CL-2027 --out /path/to/a/test/folder --dry-run
freeling_escl_configs.py --release /path/to/FreeLing-es_CL-2027 --out /path/to/a/test/folder
```

| Option | |
|---|---|
| `--release DIR` | the release folder whose `data/es/es-cl/stand-ins.tsv` and `usermap-informal.dat` are read |
| `--out DIR` | the folder written: `config/` and `es/es-cl/usermap/` under it. It must be outside the release: the release is written only by the build, whose `SHA256SUMS` the deploy checks |
| `--dry-run` | check everything, write nothing |
| `--version` | print the version |

It needs `freeling_escl_build.py` beside it, which carries FreeLing 4.2's
es-cl config.

Executes by default. Exit codes: 0 done (or the dry run passed), 1 a problem
in the inputs (each listed, nothing written), 2 refused.

## The files it writes

Under the release's `data/` folder (by the build) or under `--out`:

- `config/es-cl.cfg`, `config/es-cl-informal.cfg`, `config/es-cl-speech.cfg`,
  `config/es-cl-19th-century.cfg`
- `config/es-cl-conll-columns.cfg`: `ID SPAN_BEGIN SPAN_END FORM LEMMA TAG
  SENSE ALL_SENSES DEPHEAD DEPREL LEX_PROB TAG_PROB` (the last two need
  FreeLing with `freeling-4.2-tag-probabilities.patch`: FreeLing without it
  does not know the names)
- `es/es-cl/usermap/es-cl.dat`, `es-cl-informal.dat`, `es-cl-speech.dat`,
  `es-cl-19th-century.dat`

## Checks

- `stand-ins.tsv`: the header is `form`, `tag`, `meaning`; every line has
  the three fields; every form is XXX + capital letters + XXX; no form twice;
  at least one stand-in.
- Every setting it changes must be in FreeLing's config exactly once.
- Every config is pure ASCII.

Any failure: the problems are listed and nothing is written (the build
refuses).

## Tested

261119, version 2.0.0, on FreeLing 4.2's es-cl config as the build carries
it, the `stand-ins.tsv` of 261119 and the chat readings of the informal user
map in use: four configs, the columns file and four user maps written with no
problem. Against the release's `es-cl.cfg` of 261118, `es-cl-speech.cfg`
differs in exactly the settings above (OutputLevel, AlwaysFlush,
NPDataFile, NEClassification, SenseAnnotation, TaggerForceSelect,
DependencyParser, and the five lines added at the end). The informal user map
holds every line of the informal user map the corpora were tagged with, plus
XXXURLXXX and XXXEMAILADDRXXX. The speech user map: the five stand-ins,
novela, vela, velo, nn and nnn. Not yet run by FreeLing: that is the check
after the next build and deployment.

## Platform

Linux, macOS and Windows. Python 3.9 or later, standard library only.

## Changelog

- 2.1.0 (261120): the columns file names `LEX_PROB` and `TAG_PROB` after its ten earlier columns, so every text tagged with the release's configs has the probability of the selected reading and the probability the tagger gives the selected tag. The ten earlier columns are unchanged. Tested with FreeLing 4.2 built with the tag-probabilities change, on the four kinds of text.
- 2.0.0 (261119): first version under this name, replacing `the former config writer` 1.6.0: one config per kind of text for everyone (the release, the packages, the corpora), written by the build; the speech config is new in the release; the user maps tag the stand-in tokens of `stand-ins.tsv` (new: XXXURLXXX and XXXEMAILADDRXXX); the 19th-century files in `es/es-cl/19th-century/`.
