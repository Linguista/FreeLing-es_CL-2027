# freeling_escl_build_README.md

Documents `freeling_escl_build.py` 2.8.1.

Real file: `/home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_build.py`

## Purpose

Builds FreeLing es-CL 2027, the Chilean Spanish data for FreeLing 4.2, into
the release folder
`/home/user/FreeLing_es-CL_2027`.
It builds two dictionaries: the default one, FreeLing es-CL 2027, for contemporary Chilean
Spanish, and the 19th-century one, for historical corpora only, with the 19th-century Chilean spellings, its own probabilities and multiwords, and its own config (see "The 19th-century dictionary"); the Chilean versions of
the name classifier's word lists and its file, under FreeLing's own names;
and the two rule files of the name recognizer, for written texts and for
transcribed speech (decided 261110d, 261110e, 261110f and 261110g). What
the release contains and every change it makes are described in its own
README,
`FreeLing_es-CL_2027_README.md`, which sits next to this script and is
copied into the release as `README.md` at every build.

Nothing is installed: `freeling_escl_deploy.py` does that.

No installed FreeLing file and no archived (deprecated) file is read. The
Spanish base comes from FreeLing's own source files, each checked against
FreeLing 4.2's sha256.

| | |
|---|---|
| reads | `/home/user/build/FreeLing-4.2/data/es/dictionary/header` and `entries/MM.*` (the Spanish dictionary, rebuilt here byte for byte) |
| reads | `/home/user/build/FreeLing-4.2/data/es/np.dat` (the Spanish name recognizer's rules) |
| reads | `/home/user/build/FreeLing-4.2/data/es/quantities.dat` (currencies and measures) |
| reads | `/home/user/build/FreeLing-4.2/data/es/tagset.dat` (to check the Chilean tagset against) |
| reads | `/home/user/build/FreeLing-4.2/data/es/tagger.dat` (only its word frequencies, for `NAME-WEIGHTS.tsv`) |
| reads | `/home/user/build/FreeLing-4.2/data/es/probabilitats.dat` (only the lines of the decided names: the basis of every line the build writes for them) |
| reads | `/home/user/build/FreeLing-4.2/data/es/locucions.dat` (FreeLing's general Spanish multiwords, merged into the Chilean multiword file: see "The multiwords") |
| reads | `/home/user/build/FreeLing-4.2/data/common/nec/cities.dat` and `cities-CL.dat` (FreeLing's city list and its Chilean version, merged here) |
| carries | FreeLing 4.2's `data/config/es-cl.cfg` (sha256 `2934d4320a5690d4fbfb945325a7df20cb99d3e0393e8b8d7e6d3ddb37e8a42c`), the basis of the release's two configs, as text in the script: no `es-cl.cfg` on the machine is read (decided 261113) |
| reads | `/home/user/build/FreeLing-4.2/data/es/nerc/data/gazLOC-c.dat` and `gazPER-c.dat` (the classifier's whole place and person names) |
| reads | `/home/user/build/FreeLing-4.2/data/es/nerc/nec/nec-ab-poor1.dat` (the classifier's file, to which the class shares are added) |
| reads | `/home/user/csld/linguistic-derived/people-names-list/gazPER-p.dat` (the Chilean person-name parts, copied as they are) |
| reads | `/home/user/csld/linguistic-derived/grammatical-lists/individual/contemporary/freeling-cl/CL.{adj,adv,demonyms,int,nom}.GRAM.txt`, `CL.{tanc,vaux,verb}.Vos-V.GRAM.txt`, `CL.{peoplenames,orgnames,cities}.GRAM.txt` |
| reads | `/home/user/csld/linguistic-derived/grammatical-lists/individual/contemporary/freeling-cl/metadata/tagset.dat` (the Chilean tagset) |
| reads | `/home/user/csld/software/10-Infrastructure/freeling/escl-sources/*.tsv` (the build's own sources: the decisions of the COSCACH spelling review that the build reads, and the name decisions: `fixed-name-classes`, `person-name-removals`, `place-only-forms`, `sentence-start-classes`, `name-class-shares`; see "The sources" below) |
| checks | `/home/user/corpora/050-Spelling-normalized/COSCACH/_processing-records/spelling-review/decisions/`: every file there of a kind the build reads must be a link to its file in `escl-sources`, and every file in `escl-sources` must have its link there |
| reads | `/home/user/build/FreeLing-4.2/data/es/es-cl/{probabilitats.dat,locucions.dat}` (the deployed Chilean data) |
| reads | `FreeLing_es-CL_2027_README.md` next to this script |
| copies | into the release's `software/` folder: this script, `freeling_escl_deploy.py`, `freeling_csld_configs.py`, `freeling_escl_sources_move.py`, their READMEs and the release README (all from this script's folder), and `/home/user/MyScripts/linguistics/explode-{ADJECTIVES,ADVERBS,INTERJECTIONS,NOUNS-ALL-GENDERS,NOUNS-ONLY-PLURALIZE,VERBS}-4-FreeLing.pl` with `explode-VERBS-4-FreeLing_README.md` |
| copies | into `sources/escl-sources/`: every `escl-sources` file read, and `escl-sources/README.md`, so the release can be rebuilt from itself |
| copies | into `software/patches/`: the change to FreeLing's name recognizer and classifier, from `/home/user/csld/software/10-Infrastructure/freeling/patches/` (`freeling-4.2-np-classes.patch`, its README, `np.cc`, `np.h`, `nec.cc`) |
| reads | `/home/user/csld/software/10-Infrastructure/freeling/freeling-release-privacy.tsv` (the privacy file: private, never copied into the release; see "The release is public") |
| copies | `agpl-3.0.txt`, next to this script (the GNU AGPL 3.0, checked by sha256), into the release as `LICENSE` |
| copies | the packaging of FreeLing 4.2 with this release for Fedora, Debian and Ubuntu, from `/home/user/csld/software/10-Infrastructure/freeling/packaging/`: the seven scripts and their READMEs into the release's `packaging/` folder, and `packages.yml`, the GitHub workflow that builds and checks the packages, into `.github/workflows/` (see "The packaging") |
| writes | `/home/user/FreeLing_es-CL_2027/` |
| moves | a previous build to `/home/user/software/deprecated/FreeLing_es-CL_2027.DEPRECATED-YYMMDD[letter]` |

## Usage

```bash
freeling_escl_build.py --dry-run
freeling_escl_build.py
```

| Option | Default |
|---|---|
| `--root` | the project root, found from the script's location by `PROJECT_ROOT.txt` |
| `--source-tree` | `/home/user/build/FreeLing-4.2` |
| `--build-tree` | `/home/user/build/FreeLing-4.2/data/es/es-cl` |
| `--decisions` | `<project root>/software/10-Infrastructure/freeling/escl-sources` |
| `--linked-folder` | `/home/user/corpora/050-Spelling-normalized/COSCACH/_processing-records/spelling-review/decisions` (the folder whose links are checked) |
| `--out` | `/home/user/FreeLing_es-CL_2027` |
| `--explode-dir` | `/home/user/MyScripts/linguistics` |
| `--patches` | `../patches` beside this script's folder: `/home/user/csld/software/10-Infrastructure/freeling/patches` |
| `--packaging` | `../packaging` beside this script's folder: `/home/user/csld/software/10-Infrastructure/freeling/packaging` |
| `--privacy` | `freeling-release-privacy.tsv` in the folder above this script's: `/home/user/csld/software/10-Infrastructure/freeling/freeling-release-privacy.tsv` |
| `--dry-run` | build and check everything in memory, write nothing |

The build is written to `FreeLing_es-CL_2027.part` and moved into place only
when complete.

## What it does

1. Rebuilds the Spanish dictionary from FreeLing's entries files exactly as
   FreeLing's own build does, and refuses unless it is FreeLing's installed
   Spanish dictionary byte for byte.
2. Fixes the Chilean lists: the ir paradigm, the voseo readings of vais,
   dais, veis and deis, dai, veís and deís, erih and eríh, habís, the vos
   tag, a malformed tag, capitalized forms; removes every voseo form of erar
   (decided 261101); removes regular forms of irregular verbs, checked
   against the Spanish dictionary's own paradigms.
3. Adds the decided words (`CL.additions`), from the newest
   `dictionary-additions-all-rounds-standardized--*.tsv` (it refuses if a
   per-round additions file is newer):
   - names with their class (person, place, organization, other). A name
     whose lowercase form is also a common noun or a verb gets no
     proper-noun reading (decided 261110b): FreeLing's name recognizer tags
     it when capitalized. A name whose other readings are adjectives,
     adverbs or interjections keeps both readings (decided 261110);
   - nouns with their other number, and the lemma when it is the singular
     or the masculine and not yet a word; adjectives with all their forms;
     diminutives and augmentatives whose lemma is the base word get the
     evaluative value (cantitos, lemma canto: noun, masculine, plural,
     evaluative), superlatives the superlative one (relajadísimo);
   - adverbs and interjections;
   - new verbs with their whole paradigm, voseo included. A verb made of a
     prefix and a known verb is conjugated like it (sobreexigir like
     exigir); any other like the known verbs that share its longest ending,
     taking the pattern at least three of them share, so a regular verb
     never gets a stem change. Forms with attached pronouns are left to
     FreeLing's affix rules; non-standard forms of known verbs (ponido,
     descubrido) get the tags of the regular pattern;
   - the verb forms decided one by one, from the newest
     `verb-form-readings--*.tsv` (decided 261110b): querímos, sirvimos,
     haguís, estéi ... get the decided readings. A form with attached
     pronouns gets its reading on the form it is made from: hace, dice and
     pone are Chilean imperatives (háceme, díceselo, pónete), llevamos is
     the imperative of llevámonos, rootiar the infinitive of rootiarlos.
     A reading marked "nearly impossible" on its own (the four
     imperatives) is nearly impossible in `probabilitats.dat`, so hace
     alone stays the present indicative while FreeLing's affix rules
     analyze háceme from it. What is still untagged is listed in
     `DECISIONS.tsv` and not added.
   A generated form that is already another word is not added.
4. Applies the interjection decisions: the decided lemma, the removals
   (their other readings stay; a form that was only an interjection is no
   longer in the dictionary), and the rare ones (nearly impossible in
   `probabilitats.dat`; a rare multiword becomes ambiguous).
5. Generates the spelling variants of every voseo form (`CL.variants`).
6. Adds the person, place and organization lists (`CL.names`), as before:
   a list name whose lowercase form is an ordinary word is left to the name
   recognizer (decided 261101).
7. Adds the forms kept in the text and read as a standard form
   (`CL.nonstandard`, from `dictionary-variants`), and the misspelt forms
   the text corrects (`CL.misspellings`, decided 261110: the text is
   corrected, and any misspelling that slips through is read as its
   correction). A misspelt form that is itself a word is not added; a split
   or join is corrected in the text only.
8. Applies the standard lemmas (`lemma-standardization`, both sheets
   chained) to every entry of the word class the decision was made for, so
   the name Ala becomes alá and the noun ala (wing) is untouched. Then makes
   every place-only form (`place-only-forms--*.tsv`, decided 261110d: arica;
   261110e: barbados, chanco, pirque) a place and nothing else: its other readings are removed, from
   FreeLing's Spanish dictionary and from the Chilean lists, the place
   reading is added when missing, and in `probabilitats.dat` its lemma
   preference and any line of its own are dropped.
9. Builds the default dictionary (vos with the voseo reading only; an -is
   form with a voseo and a vosotros reading of the same verb and tense keeps
   the voseo one) and the historical one (both readings), and the
   tuteo-tagged dictionary, zipped; writes FreeLing's own entries and remove
   files and refuses unless FreeLing's build-dict would give the same two
   dictionaries.
10. Writes `probabilitats.dat` (the decided names, the rare interjections,
    mm, hm, the four imperatives, the unaccented future, poder over podar,
    the readings kept at the start of a sentence),
    `locucions.dat`
    (FreeLing's general multiwords merged in, ya_poh, the multiword interjections, the decided multiwords: see "The multiwords"), `locucions-MINIMAL.dat` and
    `quantities.dat` (the Chilean peso, UF, UTM, the euro's code, and 56
    unit names removed: see "The units removed" below).
11. Writes the names (decided 261110d and 261110e; section 8 of the release
    README):
    - **the classifier's lists**, under FreeLing's names:
      `data/common/nec/cities.dat` (FreeLing's `cities.dat` and
      `cities-CL.dat` merged, with every place name of the Chilean data),
      `data/es/nerc/data/gazLOC-c.dat` (FreeLing's, with the same),
      `gazPER-c.dat` (FreeLing's, minus `person-name-removals--*.tsv`) and
      `gazPER-p.dat` (the Chilean list). The place names of the Chilean data
      are those of `CL.cities.GRAM.txt`, the Chilean places of
      `cities-CL.dat`, and every place reading of the default dictionary and
      of `locucions.dat`; a single word that is also an ordinary word of the
      dictionary goes on no place list unless it is a fixed place;
    - **the fixed names**: the Chilean places `cities-CL.dat` adds to
      `cities.dat`, the places of `CL.cities.GRAM.txt` in neither of
      FreeLing's lists, and `fixed-name-classes--*.tsv`, which wins (class
      place, person, organization, other, or none: not fixed). Each is
      written as FreeLing writes a name (lower case, words joined by _), and
      a name with del or al also with de_el or a_el;
    - **`np.dat` and `np-speech.dat`**: FreeLing's Spanish `np.dat` with
      every single letter ignored, and the sections `<DictionaryClasses>`
      (place, person, organization, other), `<ClassesAtSentenceStart>` (no
      in `np.dat`, for written texts; yes in `np-speech.dat`, for
      transcribed speech), `<FixedClasses>` and `<SentenceStartClasses>`
      (from `sentence-start-classes--*.tsv`, each line in the file or files
      its row names: a form may have one rule for written texts and another
      for speech), read by FreeLing with the name-class change
      (`software/patches/`);
    - **the readings at the start of a sentence**: a row that keeps the
      word's own readings (yes, or word classes such as verbs) also gets a
      line in `probabilitats.dat` that gives the new reading its share among
      the readings the word has there: `tomé NP-VMI NP 111 VMI 1000` (the
      place 10%); for quito, which keeps its verb readings only, `quito
      AQ-NP-VMI AQ 47040 NP 112 VMI 1008`: the place against the verb is
      10%, and the adjective and the verb keep FreeLing's proportions
      elsewhere. The counts are scaled up until the readings kept add up to
      at least 1,000, so the share is exact;
    - **`data/es/nerc/nec/nec-ab-poor1.dat`**: FreeLing's classifier file
      with the section `<ClassShares>` (from `name-class-shares--*.tsv`,
      the shares as fractions); only FreeLing with the change reads it;
    - `NAME-CLASSES.tsv`, one row per line of the three sections and per
      class share: form, rule (fixed class, at the start of a sentence,
      class share), class, tag, share, files, source, note.
12. Checks the Chilean tagset by its sha256 and against FreeLing's Spanish
    tagset plus the voseo values, and decodes every tag of every file
    written (in the name files, the tags of `<NE_Tag>`,
    `<DictionaryClasses>`, `<FixedClasses>`, `<SentenceStartClasses>` and
    `<ClassShares>`); checks vos and the forms of
    tu in both dictionaries; checks that the Chilean person-name parts are
    lower-case NFC names, one per line.

## The decided names in probabilitats.dat

A decided name that is also a common noun or a verb has no proper-noun
reading (decided 261110b; the classes are `EXEMPT_CLASSES` at the top of the
script), and its line in `probabilitats.dat` is FreeLing's own Spanish
line, or none when FreeLing has none.

A decided name whose other readings are adjectives, adverbs or
interjections keeps both readings. Its line gives the proper noun 80% of
the word's lexical probability for a place (the user's Chilean toponyms:
much higher than the ordinary readings) and 30% for a person, an
organization or another name (moderate), decided 261110; the ordinary
readings share the rest in the proportions FreeLing already gives them. The
two shares are `PLACE_SHARE` and `NAME_SHARE` at the top of the script.
FreeLing's name recognizer still runs.

The lines of the decided names are computed from FreeLing's own Spanish
lines, never from the deployed file, which may hold the lines an earlier
build wrote for them. Every line the build manages (decided names, rare
interjections, the decided verb readings) is written in one block, sorted,
at the end of the FormTagFreq section.

`NAME-WEIGHTS.tsv` lists every weighted name with its ordinary readings, how
often the word occurs in FreeLing's Spanish training corpus (about 418,000
words), and "common word: review" from 20 occurrences up.

## The sources

Decided 261112: the decision files the build reads have one copy, in the
FreeLing tree, in
`/home/user/csld/software/10-Infrastructure/freeling/escl-sources/`.
The COSCACH decisions folder
(`/home/user/corpora/050-Spelling-normalized/COSCACH/_processing-records/spelling-review/decisions/`)
holds a relative link to each of them, so the spelling step
(`coscach_12_spelling_normalize.py`) reads the same files through the links.
`freeling_escl_sources_move.py`, beside this script, made the move and the
links; `freeling_escl_sources_move.py --check` reports their state.

The kinds of file (the part of the name before `--`): `all-corpora-replacements`,
`correction-lemmas`, `dictionary-addition-removals`, `dictionary-additions`,
`dictionary-additions-all-rounds-standardized`, `dictionary-variants`,
`fixed-name-classes`, `interjection-removals`, `interjections`,
`lemma-standardization`, `locution-removals`, `locutions`, `dictionary-words`, `historical-attested-spellings`, `name-class-shares`, `person-name-removals`,
`place-only-forms`, `sentence-start-classes`, `text-correction-removals`,
`text-corrections`, `verb-form-readings`. All are lists of words and forms;
none quotes the interviews.

Every round of every kind is read, and a later round wins for the same expression: the same form, or the same lemma in `lemma-standardization` (decided 261112: per expression, never a whole file). Something is taken out only by a removals kind (`dictionary-addition-removals`, `interjection-removals`, `text-correction-removals`, `locution-removals`, `person-name-removals`), never by leaving it out of a later round. The one exception is `dictionary-additions-all-rounds-standardized`, which is itself every round of additions merged: only the newest is read, and it must be at least as new as the newest round of additions.

`locutions`, `locution-removals`, `dictionary-words` and `historical-attested-spellings` are not decisions of the COSCACH spelling review: they live only in `escl-sources` and need no link in the COSCACH folder; nor does the hand-edit file `dictionary-hand-edits.tsv`. The files that do (the occurrence rulings, the
ir + hacer and sino occurrences) and the COSCACH-only records stay ordinary
files in the COSCACH folder.

Before building, the build checks the links both ways and refuses on any
of these: an ordinary file of one of these kinds in the COSCACH folder (it
would never reach the build: a new round must be saved in `escl-sources`),
a link there that does not lead to its file in `escl-sources`, and a file
in `escl-sources` with no link (the spelling step would never see it).

A new round is saved in the COSCACH folder and moved with
`freeling_escl_sources_move.py`, which copies it into `escl-sources`, checks
it and leaves the link (relative, as every link in the project).

The release carries a copy of every source file read, in
`sources/escl-sources/`, with its README.

## The 19th-century dictionary (decided 261112, 261113)

The historical dictionary is FreeLing es-CL 19th Century: the 2027 dictionary with the vosotros readings of the -is forms and the polite vos (as before), plus:

- **the 19th-century spellings**, generated from every correctly spelled form but the proper nouns (`HIST_RULES`: Bello and García del Río 1823, Sarmiento 1843, the Chilean orthography of 1844, the Chilean neographers): g before e/i as j, x for the j sound as j (a short list, `X_TO_J`), x before a vowel as cs, x before a consonant as s, vowel y as i, c before e/i as s or z, z as s, qu as q or k, c for the k sound as k or q, the silent u of gue/gui dropped, silent h dropped before a vowel, v as b, the trill as rr. Every combination is generated, in that order (g as j before gue loses its u), and a rule changes every place it applies in a word. Accents are never dropped. Each spelling gets the readings of the form it comes from. Into `historical/dictionary/entries/CL.19th-century-spellings`;
- **a spelling that is already a word** is added only when the rules of the 1844 orthography (`BELLO_ADOPTED`: g as j, y as i, x as s) give it; its new readings are nearly impossible on their own in `historical/probabilitats.dat` (a zero count for their short tags, as for the rare interjections), and where they share a short tag with the word's own readings, the word's own lemma is preferred (LemmaPreferences). Any other rule's spelling that is already a word is not added;
- **five words decided one by one** (`HIST_READINGS`, decided 261113): i is y and the letter i, rei is rey only, lei is ley only, hai is hay only, soi is never voseo; and two probabilities (`HIST_PROBS`): i is y 99%, testo is texto 90% and testar 10%. A reading of the Chilean lists one of them drops (rei as a name, the voseo readings of hai and soi) is listed in `historical/CL.removed-from-chilean-entries`, since FreeLing's build-dict applies a remove folder to the Spanish entries only;
- **the attested spellings** of `historical-attested-spellings--*.tsv` (from the CSLD Historic-Word-List and the pre-reform spellings taken out of the contemporary word list on 260811) with an extra or a moved accent get the readings of the one modern form with the same letters; a spelling with several such forms, or one that lacks an accent the modern form has, is not added. Into `CL.19th-century-attested`;
- **vosotros over voseo**: the tag preferences (PosPreferences) of `historical/probabilitats.dat` prefer each vosotros tag to its voseo tag and the polite vos to the voseo one. Both readings have the same short tag, so no share can be given: the preference is absolute;
- **the multiwords** in the 19th-century spellings (`key_variants`; a `<lemma>` token is left alone), when the key is new: `historical/locucions.dat`;
- **its config**, `data/config/es-cl-19th-century.cfg`: FreeLing 4.2's es-cl config (`data/config/es-cl.cfg`, carried in the script and sha256-checked) with the Chilean tagset and currencies, the 19th-century dictionary, probabilities and multiwords, and compound analysis off: FreeLing builds its compound analyzer from every form of the dictionary with foma, whose stack holds 2,097,152 entries, fewer than this dictionary has (FreeLing stops with "Stack full!"). `data/config/es-cl.cfg` is the same for the 2027 data, with compound analysis on. The two files of the 19th-century folder name `../tagset.dat`, the Chilean tagset in the folder above.

The build checks that FreeLing's build-dict would give the 19th-century dictionary from the Spanish entries minus `historical/remove/CL.removed`, the Chilean entries minus `historical/CL.removed-from-chilean-entries`, and the three historical entries files.

## The accented one-syllable forms and the common misspellings (decided 261112)

- `CL.old-accents`: fué, fuí, dió, vió, á, é, ó, ú (`OLD_ACCENTS`), each with every reading of fue, fui, dio, vio, a, e, o, u, in both dictionaries.
- `CL.common-misspellings` (formerly `CL.misspellings`): the misspelt forms of the transcriptions, read as their corrections, as before, and every correctly spelled form with a written accent or a diaeresis, written without them, read as that form, when the result is not already a word and comes from that one form only. A form whose readings all come from the misspelt or the non-standard forms is never a source. After the build, every line of `CL.common-misspellings` and `CL.old-accents` must be in `dicc.src` and in `historical/dicc.src` with exactly its readings, or nothing is written.

## Dictionary words and hand edits (decided 261112, 261113)

- `dictionary-words--YYMMDD.tsv` (form, lemma, category, tag, notes), in `escl-sources` only (no link in the COSCACH folder): with a tag, exactly that reading (a tag the Chilean tagset cannot decode refuses the build); without one, the category's readings, as for a decided addition (nouns and adjectives with their other number and gender, new verbs with their whole paradigm). Every round is read; a later round wins for the same form and lemma.
- `dictionary-hand-edits.tsv` (form, lemma, tag), in `escl-sources`, with no round: edited in place; `#` lines are comments and say what goes in it. Every line is added at every build; a tag the Chilean tagset cannot decode refuses the build. It is copied into the release's `sources/escl-sources/`.

## The multiwords (decided 261112)

FreeLing reads one multiword file, the one the config's `LocutionsFile` names, and the CSLD configs name the Chilean one, `es/es-cl/locucions.dat`. Until 2.7.0 that file held only the Chilean multiwords (2,058), so every general Spanish multiword (o sea, por ejemplo, por lo menos, a pesar de ...) was split into its words in every corpus tagged with it. From 2.7.0 the build merges FreeLing's general file, `data/es/locucions.dat` (sha256-checked against FreeLing 4.2), into the Chilean one:

- every general entry whose key the Chilean file does not have is added, with the same repairs as the Chilean entries (capitalized keys lowercased, duplicate lines merged); each is a row of `CHANGELOG.tsv` (rule "FreeLing's general multiword");
- for a key in both files the Chilean entry wins (ni_fu_ni_fa stays an adjective); a general entry that differs from the Chilean one is logged as "not added";
- FreeLing's general file tags tal y cual as `Fs`, a punctuation mark: it gets `PI0CS00`, as cual has (`LOCUTION_TAG_FIX`);
- on 261112's sources: 2,058 Chilean lines, 1,563 general lines added, 3,613 entries.

The decided multiwords come from two kinds of file in `escl-sources`:

| Kind | Columns | A row means |
|---|---|---|
| `locutions--YYMMDD.tsv` | form, lemma, tag, flag (further columns ignored) | the multiword is joined with this lemma and EAGLES tag. Flag I: always joined; A: ambiguous, FreeLing's tagger decides between the multiword and the separate words. An empty lemma is the form joined by `_`; an empty flag is I. A tag the Chilean tagset cannot decode, or a flag other than I or A, refuses the build. A later round wins for the same multiword; a decided multiword replaces any entry with its key |
| `locution-removals--YYMMDD.tsv` | form, why | the multiword is removed: its words are tagged separately. A removal of a key the file does not have refuses the build |

The form is written as it is said (al final); the build writes the key as FreeLing matches it, splitting al and del (`a_el_final`), as FreeLing splits them before it matches multiwords. A form with a `<lemma>` pattern (`<dar>_lo_mismo`) is taken as written. Every row is a row of `DECISIONS.tsv`.

## The decision files of the names

In `/home/user/csld/software/10-Infrastructure/freeling/escl-sources/`,
tab-separated, one header line, every round read, later rounds winning:

| File | Columns | A row means |
|---|---|---|
| `fixed-name-classes--*.tsv` | name, class, source, ruling | the name always has this class: place, person, organization or other; none: it is not fixed, even if the build would derive it (Navidad). Two different classes for one name in one round refuse the build |
| `person-name-removals--*.tsv` | entry, list, ruling | the entry (as FreeLing writes it, lower case, words joined by _) is removed from the list; the list must be `gazPER-c.dat` |
| `place-only-forms--*.tsv` | form, ruling | the form is a place and nothing else |
| `sentence-start-classes--*.tsv` | form, reading, keep own readings, share, files, ruling | at the start of a sentence the one-word form gets the reading (name: the classifier decides; place, person, organization, other), whatever the other rules say. Keep own readings: no, they are dropped; yes, they stay beside it; or word classes (verbs, nouns, adjectives, adverbs, pronouns, determiners, interjections, prepositions, conjunctions, numerals, separated by commas): only those stay. With readings kept, share is the new reading's percentage among the readings the word has there (above 0, below 100); with no, share is empty. Files: written (`np.dat`), speech (`np-speech.dat`) or both. A form may have one row for written and another for speech (decided 261110g: Pinto); a later file's row replaces the earlier rule for the files it names, and two rows of one file for the same form and file refuse the build. A form with no dictionary reading to keep, with no reading of the classes named, or that already has a proper-noun reading or a probability line of its own refuses the build; so does a form that keeps its own readings in both files with a different reading, share or word classes, as `probabilitats.dat` holds one line for both |
| `name-class-shares--*.tsv` | name, class, share, ruling | when the classifier classifies the name, it takes one of the classes of its rows, by its own weight plus half the log odds of the share (percent). The rows of a name in one file must add up to 100; a later file's rows for the name replace the earlier ones. A name with shares must not also have a fixed class |

## The units removed from quantities.dat (decided 261112)

FreeLing's quantities module joins a number and the unit name after it into
one token (tag `Zu`, lemma `TM_d:2` for dos días). It compares the word in
lower case, and accepts "number de unit". In COSCACH a number followed by an
abbreviation that is also a letter, a word or a false start became a
quantity: "uno tr ..." was 1 unit of weight `tr`, "uno de mi ..." 1 mile
(41 tokens with mi), "uno s ..." 1 second, "sesenta D" 60 days, "los tres
cd" 3 candelas. The full words (días, horas, minutos, metros, pesos) were
all right and stay.

The build removes these lines from `<MeasureNames>`, each of which must be
there exactly once (otherwise it refuses), and records each in
`CHANGELOG.tsv` (list `quantities`, change `removed`, with the reason). The
unit codes in `<Measure>` stay, because the full words use them (milla,
pie, galón, libra, onza, pulgada and the rest are kept, decided 261112),
except a code no name uses once these lines are gone: `WG tr` (decided
261112: tr is not a unit). A code removed while a name still uses it
refuses the build.

- **Abbreviations that collide** (10): tr (false starts, never a unit), mi
  (the possessive), s and d (the letters; false starts), cd (CD), cl and bu
  (false starts), pk (the chat spelling of porque), in (the English word),
  pt (punto, points).
- **Units not written so in Chile, with their compound forms** (46): ft
  (ft2, ft3, ft/s, ft/h, ft/min, ft/s2, ft3/s, ft3/min, ftH2O, fth2o), gal
  (gal/h, gal/min, gal/s, gal/d, gal/ac/d, gal/cap/d, gal/ft2, gal/ft2/d,
  gal/ft2/min), lb (lb/ft2, lb/ft3, lb/in2, lb/milgal, lbf, lbF), oz (floz),
  ac (ac-ft, ac·ft), yd (yd2, yd3), qt, and the compounds of in (in2, in3,
  in/s2, inh20, inH2O, inhg, inHg) and of mi (mi2, mi/h).

Kept, as real units in Chilean writing: g, h (the hour), m, l, ml, w, km,
kg, cm, mm, mg, min, tm, cal, mb, gb, kb and the rest. Still joined in
COSCACH after this: about ten false starts before an ellipsis read as
meters or liters ("dos m ...", "uno l ..."), which the file cannot tell
from the units; they are for the correction layer.

## The release is public (decided 261112)

The release goes to GitHub, so no file in it may hold a private path or
name. The privacy file says what is private:

```text
/home/user/csld/software/10-Infrastructure/freeling/freeling-release-privacy.tsv
```

It is TAB-separated, UTF-8, with the header `private<TAB>public`. A row
with a public text is a replacement (`/home/user<TAB>/home/user`); a row
with none is a term that may appear nowhere (a machine name). The private
text of every replacement is a term too. Empty lines and lines beginning
with `#` are skipped. The file is refused if a public text holds a
private term.

Every file of the release that is not data (`README.md`,
`BUILD-REPORT.md`, `LICENSE`, the tables, `software/`, `sources/`) is
written with the replacements made, longest first. The data
(`data/`, `grammatical-lists/`, `tuteo-tagged-dictionary/`) are never
changed. Then every file, data included (and the dictionary inside
`dicc-0-tags.zip`), is searched for every term, in any case, and every
Python file must still compile. One term found, and nothing is written:
each line is listed as `PRIVATE: file line N: term`, the release folder is
left as it was, and the build exits 1. The dry run checks the files that
are copied as they are (the READMEs, the software, the sources) the same
way and exits 1 if any is not clean.

So the release's copies of the tools and READMEs differ from the ones in
the project in their paths only, and `SHA256SUMS` gives the sha256 of the
copies. The privacy file itself is never copied into the release.

The license: FreeLing 4.2 is under the GNU Affero General Public License,
version 3 or later, and the release, made from its files, is under the same
license. `agpl-3.0.txt`, next to this script, is the text as the Free
Software Foundation publishes it (sha256
`0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0`, checked
before anything else); it goes into the release as `LICENSE`.

## The packaging (decided 261112)

The release folder is the GitHub repository Linguista/FreeLing-es_CL-2027, and GitHub builds from it packages of FreeLing 4.2 with this release (`freeling-es-cl`) for Fedora 43 and 44, Debian 13 and Ubuntu 24.04 and 26.04, each built on its own distribution, installed on a fresh one and checked before it is attached to a release. The scripts that do it are kept in the project, in `software/10-Infrastructure/freeling/packaging/`, each with its README, and the build copies them into every release: the scripts into `packaging/`, the workflow `packages.yml` into `.github/workflows/`, where GitHub looks for it. So a rebuilt release folder is the complete repository.

| File | What it does |
|---|---|
| `patch-freeling.sh` | applies to FreeLing 4.2's source every change it is built with |
| `build-freeling.sh` | builds and installs FreeLing 4.2 with this release's data, and gathers what the package installs and needs |
| `make-nfpm-config.py` | writes the package's configuration for nfpm |
| `postinstall-deb.sh` | Debian and Ubuntu: refreshes the library cache and generates the en_US.UTF-8 locale if it is missing |
| `ldconfig.sh` | refreshes the library cache (Fedora, and removal everywhere) |
| `test-freeling.sh` | checks an installed package |
| `packages.yml` | the GitHub workflow: on a release tagged with a date (YYMMDD, an optional letter for a second release that day), builds, checks and attaches the packages |

A missing packaging file refuses the build, as any other input does.

## Tested

261113, version 2.8.1, a full build on the test tree with no `data/config/es-cl.cfg` in its source tree: every file of the release byte for byte as 2.8.0 built it (both configs and both dictionaries included), except `BUILD-REPORT.md` (its version line and the config's input line), `software/freeling_escl_build.py` and `SHA256SUMS`.

261113, version 2.8.0, full builds on the test tree with the escl-sources of 261113 (and the rounds of 261113: `dictionary-words`, `locutions`, `historical-attested-spellings`, `dictionary-hand-edits.tsv`): 2027 dictionary 937,701 forms; 19th-century dictionary 2,146,645 forms (1,203,611 new spellings, 5,333 attested spellings, 518 words given a Bello reading, 6,539 multiwords); 140,895 unaccented forms, 516 left out; every line of `CL.common-misspellings` and `CL.old-accents` found in both dictionaries; FreeLing's build-dict check passed for both. FreeLing 4.2 compiled from source with `packaging/patch-freeling.sh` 1.1.0 (Spanish only) and this release installed: with `es-cl.cfg`, tenís is tener VMIP2SV, comeriamos is comer, colaboracion is colaboración, tatoo is tatuaje, cesfam and minipimer NCMN000, ponerse las pilas, me pongo las pilas, ponte las pilas and se puso las pilas one multiword each, dulce de leche, de a poco, flor de, buen día and medio pelo as decided; with `es-cl-19th-century.cfg`, jente gente, jeneral general, esplicó explicar, mui muy, hoi hoy, rei rey, i y, lei ley, hai hay, soi soy, á a, fué ser, ménos menos, ántes antes, órden orden, soziedad sociedad, zientífica científico, qeso queso, testo texto ("El testo del libro") and testar ("Testo mi casa a mis hijos"), salís vosotros; with `es-old.cfg` (FreeLing Old, its multiword file the link to the Chilean one), dixo decir, muger mujer, fermosa hermoso. `test-freeling.sh` 1.1.0 passed. Built again on its own output (its `probabilitats.dat` and `locucions.dat` as the deployed build tree's), every data file and both configs byte for byte the same. Memory: about 780 MB with 2027, 930 MB with the 19th century. Without compound analysis off, the 19th-century config stops FreeLing ("Stack full!").

261112, version 2.7.0, full builds on the test tree (FreeLing 4.2's `data/es/locucions.dat` added to its source tree): with no `locutions` file, every data file byte for byte as 2.6.0 built it except `locucions.dat` (2,058 lines in, 3,613 entries out); built again on its own output, every data file byte for byte the same; with two rounds of `locutions` and one of `locution-removals`, a lo mejor and al final (`a_el_final`, flag A) added, sin embargo with the tag of the later round, tal y cual removed, all three files copied into `sources/escl-sources/` and listed in `DECISIONS.tsv`; a round with an undecodable tag refused the dry run (exit 2). Without the general file and the decided multiwords, the multiword step gives the published `locucions.dat` byte for byte.


261112, version 2.6.0, a full build on the test tree: the dictionaries, every data file and the corrected grammatical lists byte for byte as 2.5.0 built them; the packaging copied (scripts executable), the workflow in `.github/workflows/`, `SHA256SUMS` checked, no private line in the 73 copied files. The fixed class of SES, written `organisation` in its decision file, is read as organization and written so in `NAME-CLASSES.tsv`, the one change in the release's tables besides the American spelling of their notes.

261112, version 2.5.1, dry runs on the test tree: with the lists as they
were (three nguillatún lines with the lemma guillatun) the fix was made;
with the build's own written-back lists, which already have nguillatún,
nothing was needed and the build went on, giving the same two dictionaries,
byte for byte; with no nguillat line in the noun list the build refused
(exit 2). The dry run of 2.5.0 on the project's machine had refused the written-back
lists.

261112, version 2.5.0, a full build on a test tree with the privacy file
of 261112: the dry run found the one private line left in this README (the
name of a machine), which was removed; the build then wrote the release,
in which no private term of the list of 261112 was found, `SHA256SUMS`
checked, the copies of the tools compiled and differed from the project's
in the replaced paths only, and `LICENSE` was the AGPL text. With a term
added that is in the data (nguillatún), 58 lines were listed, nothing was
written, the release folder was unchanged and no `.part` folder was left
(exit 1). A privacy file whose public text holds a private term was refused
(exit 2).

261112, the list lemma fix: on the seven nguillatún and guillatun lines
of the noun list, the three with the lemma guillatun get nguillatún, the
two nguillatunes lines become one, and guillatun (lemma guillatún) is
untouched.

261112, the code removal: on the same test file `WG tr` removed, `LN mi`,
`SP mi/h`, `AR mi2` and the milla lines kept; with a name that still uses
the code tr, the build refuses. The lemma of nguillatún: on the decision
files of 261112 with `lemma-standardization--261112.tsv`, the lemma guillatun
maps to nguillatún for nouns.

261112, the unit removals: on a test file holding every name of FreeLing's
`<MeasureNames>` (the 189 plain names of the real file),
all 56 found once and removed, the currency changes made, `WG tr` and the
other codes of `<Measure>` and the name `h` kept; a name missing or present
twice refuses the build.

261112: the link check, on a copy of the COSCACH decisions folder of
261112 after `freeling_escl_sources_move.py` moved its 41 files: no problem;
with one file put back as an ordinary file, one link removed and one
escl-sources file without a link, each refuses the build. The rest of the
build is unchanged; the first run on this machine, `--dry-run`, is its test
on the real inputs.

261110, in a copy of the inputs of this machine (FreeLing
4.2's files of the build tree, the CSLD lists, the decisions of rounds 1 to
8 and of 261110d to 261110g, the Chilean data deployed on 261110 from the
build of 261110f):

- on the decisions up to 261110f it gives the previous version's release
  byte for byte, but for the script itself and the release's checksums;
- with 261110g, two data files change: `np-speech.dat` (`pinto NP00SP0`
  for `pinto NP00SP0 keep:V`) and `gazPER-c.dat` (molina removed: 4,439
  names); `np.dat`, `probabilitats.dat` (pinto's line stays, for written
  texts), the dictionaries and every other file are the same;
- two rows of one file for the same form and rule file, and a form kept
  beside its own readings in both files with different shares, each refuse
  the build;
- with these files and FreeLing with the name-class change, on the
  COSCACH probe of 261110 (22,394 exact place-name tokens in speech mode,
  22,422 in written mode): places 99.6% with `np-speech.dat` and 99.5%
  with `np.dat`; Molina a place 31 times of 32 (the one person, Enrique
  Molina, a school); "Pinto el" at the start of a line a person in speech
  and the verb in written mode. Of the 220,734 tokens, 16 changed their tag
  in speech mode (15 Molina, one Pinto) and 15 in written mode (all
  Molina);
- run again on its own output, the build gives the same data files,
  grammatical lists, `NAME-CLASSES.tsv`, `NAME-WEIGHTS.tsv` and
  `VARIANTS.tsv`, byte for byte.

The previous version was tested the same way on 261110 (section 8.6 of
the release README): the place names of the probe were places 99.5% of the
time with `np-speech.dat` and 99.4% with `np.dat`, against 75.6% before;
Quito, Catar, Tomé and Irán at the start of a written sentence get the
verb 0.90 and the place 0.10 (the 15 test sentences of the share all
right); Pinto the verb 0.70 and the person 0.30 (15 of its 16 test
sentences right, all but "Pinto y dibujo").

## Reproducibility

Every change is conditional, and the probability lines the build manages
are recomputed from the same basis every time, so a build run on its own
deployed output, or on an earlier build's, gives the same dictionaries,
`probabilitats.dat`, `locucions.dat`, name files and grammatical lists,
byte for byte.
The release's `BUILD-REPORT.md` records the sha256 of every input.

## The change log in words

`CHANGELOG.tsv` and `VARIANTS.tsv` give every tag in words (verb, main,
indicative, present, 2nd person, singular, voseo). `DECISIONS.tsv` gives one
row per decision row read: what was decided and what the build did with it.

## Exit codes

0 built (or dry run done), 1 private text left in the release (nothing
written; the dry run exits 1 for the same reason), 2 refused (nothing
written), 130 interrupted.

## Platform

Linux (the FreeLing paths are Linux paths). Standard library only.

## Changelog

- 2.8.1 (261113): FreeLing 4.2's `es-cl.cfg` is carried in the script (`ES_CL_CFG_TEXT`, checked against its sha256) instead of read from the source tree: the CSLD tags only with `csld-es-cl.cfg` and the configs written from it, and every other es-cl config on the machine is retired (decided 261113). The release is otherwise unchanged.

- 2.8.0 (261113): the 19th-century dictionary (decided 261112, 261113): the 19th-century Chilean spellings, the attested old-accent spellings, five words decided one by one, its own probabilities (Bello readings of existing words nearly impossible, vosotros over voseo) and multiwords, and the two configs `data/config/es-cl.cfg` and `es-cl-19th-century.cfg` (FreeLing's `data/config/es-cl.cfg` is a new sha256-checked input); `CL.old-accents` in both dictionaries; `CL.misspellings` becomes `CL.common-misspellings`, with every accented form written without its accents; two new kinds of source, `dictionary-words` and `historical-attested-spellings`, and the hand-edit file `dictionary-hand-edits.tsv`; the packaging's new `install-data.sh` (the Chilean data into an installed FreeLing, for the Linux packages and the macOS tarballs) is copied with the other packaging scripts. See "The 19th-century dictionary", "The accented one-syllable forms and the common misspellings" and "Dictionary words and hand edits".

- 2.7.0 (261112): FreeLing's general Spanish multiwords (`data/es/locucions.dat`, sha256-checked) are merged into the Chilean multiword file, the Chilean entry winning for a key in both; until now every general multiword was split in every CSLD corpus, as the configs name the Chilean file only. tal y cual gets `PI0CS00` (FreeLing's file has `Fs`). Two new kinds of source, `locutions` and `locution-removals`, which need no link in the COSCACH folder. Every kind is now read per expression across all its rounds, later rounds winning (interjections, interjection removals and lemma standardization read only their newest file until now); `dictionary-additions-all-rounds-standardized` stays newest only, being itself every round merged. See "The multiwords".
- 2.6.0 (261112): the packaging of FreeLing 4.2 with the release for Fedora, Debian and Ubuntu (`../packaging/`, `--packaging`) is copied into every release, the scripts into `packaging/` and the GitHub workflow into `.github/workflows/`, so the release folder is the complete GitHub repository (see "The packaging"). The project writes American English (decided 261112): the decision files' class `organisation` is read as `organization` (`CLASS_SPELLING`), as is the category `proper noun, organisation or brand`, and the build's notes, messages and comments use American spelling. The data are unchanged.
- 2.5.1 (261112): a list lemma fix (`LIST_LEMMA_FIXES`) that finds nothing
  to correct no longer refuses the build when the list already has the
  right lemma: the deployed Chilean lists are the build's own corrected
  ones, which already give nguillatún, so 2.5.0 refused them ("no entry
  with the lemma guillatun to correct") and broke the rule that a build
  run on its own output gives the same files. A list with neither lemma
  for the forms still refuses the build.
- 2.5.0 (261112): the release is public (decided 261112). Every file of it
  that is not data is written with the private paths of the privacy file
  (`--privacy`) replaced by public ones, and nothing is written if a
  private term is left in any file, data included (exit 1). The release
  carries FreeLing's license, the GNU AGPL 3.0, as `LICENSE`. See "The
  release is public".
- 2.4.3 (261112): the lemma guillatun of nguillatún, nguillatun and
  nguillatunes is corrected to nguillatún in the Chilean noun list itself
  (`LIST_LEMMA_FIXES`), so the corrected list written back carries it, not
  only the dictionary; the two nguillatunes lines become one. A fix that
  finds nothing to correct refuses the build.
- 2.4.2 (261112): the unit code `WG tr` removed from `<Measure>` (no name
  uses it once tr is removed); a code still in use refuses the build. The
  codes of the kept full words (milla: mi, mi/h, mi2) stay.
- 2.4.1 (261112): 56 unit names removed from `quantities.dat` (decided
  261112): the abbreviations that are also letters, words or false starts
  (tr, mi, s, d, cd, cl, bu, pk, in, pt), and the units not written so in
  Chile with their compound forms (ft, gal, lb, oz, ac, yd, qt and the
  compounds of in and mi). See "The units removed from quantities.dat".
- 2.4.0 (261112): the decision files are read from the FreeLing tree,
  `software/10-Infrastructure/freeling/escl-sources/` (decided 261112: one
  copy, linked from the COSCACH decisions folder). The default was the
  folder `working/coscach-spelling--261101/decisions`, which no longer
  exists since the COSCACH records moved to the stages' `_processing-records`
  (261111), so the build refused. The links are checked both ways before
  anything else (`--linked-folder`), and the release carries the sources it
  was built from, in `sources/escl-sources/`, and `freeling_escl_sources_move.py`
  with the rest of its software.
- 2.3.0 (261110): a form may have one sentence-start rule for written texts
  (`np.dat`) and another for speech (`np-speech.dat`) (decided 261110g:
  Pinto the surname or the verb at the start of a written sentence, the
  surname only at the start of a COSCACH line); two rows of one file for
  the same form and file, or readings kept in both files with a different
  reading, share or word classes, refuse the build; the change log names
  the round that removed a name from `gazPER-c.dat` (molina, 261110g).
- 2.2.0 (261110): the names (decided 261110d, 261110e and 261110f). The
  classifier's lists under FreeLing's own names: `cities.dat` (FreeLing's
  two city lists merged, with the place names of the Chilean data),
  `gazLOC-c.dat`, `gazPER-c.dat` (places removed), `gazPER-p.dat` (the
  Chilean list); the fixed names, and `np.dat` (written texts) and
  `np-speech.dat` (transcribed speech) with the sections of the name-class
  change, the readings at the start of a sentence among them, with their
  lines in `probabilitats.dat`; the classifier's file
  `nec-ab-poor1.dat` with the class shares; `NAME-CLASSES.tsv`; the
  place-only forms (arica, barbados, chanco, pirque); the change to
  FreeLing's name recognizer and classifier copied into
  `software/patches/`; FreeLing's five name files checked by sha256; the
  new decision files (`fixed-name-classes`, `person-name-removals`,
  `place-only-forms`, `sentence-start-classes`, `name-class-shares`);
  `--patches`.
- 2.1.0 (261110): a decided name that is also a common noun or a verb gets
  no proper-noun reading, and FreeLing's own line in `probabilitats.dat`
  (decided 261110b); the verb forms decided one by one
  (`verb-form-readings--*.tsv`), with the Chilean imperatives hace, dice and
  pone, and llevamos, nearly impossible on their own; the decided names'
  probability lines computed from FreeLing's Spanish `probabilitats.dat`
  (checked by sha256), so a build on an earlier build's output gives the
  same file; the managed lines written in one sorted block; a kept form with
  attached pronouns is marked "left to FreeLing" in `DECISIONS.tsv`.
- 2.0.0 (261110): the Spanish base from FreeLing's own source files,
  checked by sha256, never from installed or archived files; the Chilean
  tagset checked by sha256; two dictionaries, default (contemporary) and
  historical; the spelling decisions (additions with paradigms,
  interjections, non-standard forms, misspellings, standard lemmas); the
  decided names weighted in `probabilitats.dat`; ya_poh; the Chileanized
  `quantities.dat`; FreeLing's entries and remove files for both
  dictionaries, checked against FreeLing's build-dict; the tuteo-tagged
  dictionary zipped in its own folder; `DECISIONS.tsv`, `NAME-WEIGHTS.tsv`.
  The minimal multiword set is built in.
- 1.1.0 (261101): removes every voseo form of erar, with its variants and
  the three probability lines that concerned them; writes `np.dat` with
  every single letter on the name recognizer's Ignore list.
- 1.0.0 (261101): first version.
