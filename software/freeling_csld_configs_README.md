# freeling_csld_configs_README.md

Documents `freeling_csld_configs.py` 1.2.0.

Real file: `/home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_csld_configs.py`

## Purpose

Writes the FreeLing configs the CSLD tags with, and the user map of the
stand-in tokens. It replaces `freeling_build_voseo_dictionary.py`, which
built a separate copy of the dictionary for COSCACH and CODICACH: that copy
is now FreeLing es-CL 2027's installed default dictionary.

FreeLing es-CL 2027 has two dictionaries (decided 261109), installed by
`freeling_escl_deploy.py --target system`:

| Dictionary | For | vos | -is forms (salís, comís) |
|---|---|---|---|
| `/usr/local/share/freeling/es/es-cl/dicc.src`, the default | contemporary Chilean Spanish: COSCACH, CODICACH | voseo only | voseo only |
| `/usr/local/share/freeling/es/es-cl/historical/dicc.src`, the 19th-century one, with its own `historical/probabilitats.dat` and `historical/locucions.dat` | historical corpora: older Spanish and the 19th-century Chilean spellings (Bello, the 1844 orthography, Sarmiento, the neographers) | voseo and polite, read as polite | voseo and vosotros, read as vosotros |

From the base config
`/home/user/csld/software/10-Infrastructure/freeling/csld-es-cl.cfg`
it writes, in
`/home/user/csld/software/10-Infrastructure/freeling/`:

| File | For | What differs from the base config |
|---|---|---|
| `coscach/csld-es-cl--coscach.cfg` | COSCACH, transcribed speech | the default dictionary; the Chilean name recognizer for speech, `es-cl/np-speech.dat`; the user map |
| `coscach/usermap--coscach.dat` | its user map | |
| `codicach/csld-es-cl--codicach.cfg` | CODICACH, written texts | the default dictionary; the Chilean name recognizer for written texts, `es-cl/np.dat`; the user map |
| `codicach/usermap--codicach.dat` | its user map | |
| `historical/csld-es-cl--historical.cfg` | CORHICACH | the 19th-century dictionary, probabilities and multiwords; compound analysis off |

All three use the Chilean tagset, probabilities, multiwords and currencies
(`es-cl/quantities.dat`: the peso is the Chilean peso, UF and UTM). Every
other line is the base config's. `freeling_tag_corpus.py` picks the config
by `--set`; CORHICACH also needs `--historical`.

**The two name recognizers** (decided 261110d; section 8 of
`FreeLing_es-CL_2027_README.md`). Both are the rule-based recognizer
(decided 261030), on which a spelled-out letter is never a name (decided
261101), with the name classes of FreeLing es-CL 2027: every Chilean
commune and locality, country and continent is a place, and SES, JUDEJUT,
Dr. House and Dr. Simi have their decided class. They differ at the start
of a sentence:

| | `np.dat`, CODICACH | `np-speech.dat`, COSCACH |
|---|---|---|
| `<ClassesAtSentenceStart>` | no: a word at the start of a sentence that is also a common noun or an adjective (Castro) is left to FreeLing | yes: a line of speech is an utterance, and a capitalized word at its start is a name |

Each also gives a few names their own reading at the start of a sentence
(`<SentenceStartClasses>`: Catar, Irán, Tomé and Quito the verb with a
10% chance of the place in `np.dat`; Molina a name in both; Pinto the
verb with a 30% chance of the surname in `np.dat`, and the surname only in
`np-speech.dat`, where a speaker's pinto is written in lower case (decided
261110g); Asunción and Sucre in `np-speech.dat`). The classifier file the
configs name (`NECFile`, the installed `es/nerc/nec/nec-ab-poor1.dat`)
holds the class shares of Asunción, Molina, San José, San Juan and Sucre
(decided 261110e and 261110f).

The classes are read only by FreeLing with the name-class change
(`software/patches/` of the release); `freeling_tag_corpus.py` refuses to
tag COSCACH or CODICACH without it, and FreeLing without it stops on the
classifier file.

**Retired.** Until 261110 COSCACH and CODICACH shared one config:
`coscach-codicach/csld-es-cl--coscach-codicach.cfg` and
`coscach-codicach/usermap--coscach-codicach.dat`. Both are moved to
`coscach-codicach/deprecated/`, as
`<name>.DEPRECATED-YYMMDD<extension>`. The old copy of the dictionary,
`coscach-codicach/dicc.src`, is compressed into
`coscach-codicach/deprecated/dicc.DEPRECATED-YYMMDD.src.xz` and made
unreadable (mode 000). A config that is replaced goes to `deprecated/` beside
it.

## The user map

`freeling_tag_corpus.py` sends the stand-in tokens to FreeLing lowercased
(FreeLing's name recognizer would join a capitalized token with its
neighbors). The user map tags them before any other module runs (tags
decided 261030):

| Token | Tag |
|---|---|
| `xxxredactedxxx` | `Fz`, a redacted identifier |
| `xxxunintelligiblexxx` | `Fla`, speech not made out |
| `xxxnonspeechxxx` | `Flt`, a non-speech event |

## Checks

Nothing is written if one fails:

- the base config has exactly one line for each key set;
- the installed files the configs name exist, the 19th-century probabilities and multiwords among them (deploy first), the default
  dictionary has vos with the voseo reading only and the historical one has
  both;
- `np.dat` says `<ClassesAtSentenceStart>` no and `np-speech.dat` says yes;
- the new configs are pure ASCII (FreeLing segfaults on anything else);
- no output is immutable (`chattr +i`) or read-only, checked before
  anything is written.

## Usage

```bash
freeling_csld_configs.py --dry-run
freeling_csld_configs.py
```

| Option | Default |
|---|---|
| `--root` | the project root, found from the script's location by `PROJECT_ROOT.txt` |
| `--system` | `/usr/local/share/freeling/es/es-cl` |
| `--dry-run` | report, write nothing |

## Tested

261113, version 1.2.0, with the base config of 261113 and FreeLing es-CL 2027 as `freeling_escl_deploy.py` 2.2.0 installs it: the historical config differs from the base config in the tagset, quantities, dictionary, probabilities and multiwords (the 19th-century ones), `CompoundAnalysis=no` and the `CompoundFile` line commented out; the COSCACH and CODICACH configs are as 1.1.0 wrote them. FreeLing 4.2 with the historical config (the CoNLL column file left out) read jente as gente, i as y, rei as rey and salís (after vosotros) as vosotros.

261110, on a copy of the project's FreeLing folder and of the installed
data as FreeLing es-CL 2027 is deployed since 261110: the dry run listed the five
files to write and the two to retire, and wrote nothing; the real run wrote
them and moved the two shared files to `coscach-codicach/deprecated/`; a
second run found every file unchanged. The two new configs differ from the
shared config only in the name recognizer (`np-speech.dat` for COSCACH) and
the user map's path.

## Exit codes

0 done, 2 refused (nothing written), 130 interrupted.

## Platform

Linux. Standard library only.

## Changelog

- 1.2.0 (261113): the historical config reads the 19th-century dictionary's own probabilities and multiwords (`historical/probabilitats.dat`, `historical/locucions.dat`) and turns compound analysis off (`CompoundAnalysis=no`, the `CompoundFile` line commented out): FreeLing builds its compound analyzer from every form of the dictionary with foma, whose stack holds 2,097,152 entries, fewer than the 19th-century dictionary has, and stops with "Stack full!". Refuses if those two files are not installed.

- 1.1.0 (261110): separate configs for COSCACH (`coscach/`, the name
  recognizer for speech, `es-cl/np-speech.dat`) and CODICACH (`codicach/`,
  `es-cl/np.dat`), each with its user map; the 1.0.0 config of both
  retired; checks `<ClassesAtSentenceStart>` of both name recognizers.
- 1.0.0 (261110): first version, replacing `freeling_build_voseo_dictionary.py`.
