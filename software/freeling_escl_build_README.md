# freeling_escl_build_README.md

Documents `freeling_escl_build.py` 2.21.1.

Real file: `/path/to/project/derived-software/FreeLing_es-CL_2027/tools/freeling_escl_build.py`

## Purpose

Builds FreeLing es-CL 2027, the Chilean Spanish data for FreeLing 4.2, into
the release folder
`/path/to/FreeLing-es_CL-2027`
(named so since 2.17.0; it was `FreeLing_es-CL_2027`). It builds three dictionaries: the default one, FreeLing es-CL 2027, for contemporary Chilean
Spanish; the informal one, the default with the spoken reduced forms (cansá, pescao, he comío), for informal writing only, with its config `data/config/es-cl-informal.cfg` (see "The reduced forms"); and the 19th-century one, for 19th-century texts only, with the 19th-century Chilean spellings, its own probabilities and multiwords, and its own config (see "The 19th-century dictionary"); the Chilean versions of
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
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/dictionary/header` and `entries/MM.*` (the Spanish dictionary, rebuilt here byte for byte) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/np.dat` (the Spanish name recognizer's rules) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/quantities.dat` (currencies and measures) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/afixos.dat` (the Spanish affix rules, whose clitic rules are restricted: see "The attached pronouns") |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/tagset.dat` (to check the Chilean tagset against) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/tagger.dat` (only its word frequencies, for `NAME-WEIGHTS.tsv`) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/probabilitats.dat` (only the lines of the decided names: the basis of every line the build writes for them) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/locucions.dat` (FreeLing's general Spanish multiwords, merged into the Chilean multiword file: see "The multiwords") |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/common/nec/cities.dat` and `cities-CL.dat` (FreeLing's city list and its Chilean version, merged here) |
| carries | FreeLing 4.2's `data/config/es-cl.cfg` (sha256 `2934d4320a5690d4fbfb945325a7df20cb99d3e0393e8b8d7e6d3ddb37e8a42c`), the basis of the release's configs (written by `freeling_escl_configs.py`), as text in the script: no `es-cl.cfg` on the machine is read (decided 261113) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/nerc/data/gazLOC-c.dat` and `gazPER-c.dat` (the classifier's whole place and person names) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/nerc/nec/nec-ab-poor1.dat` (the classifier's file, to which the class shares are added) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/data/people-names-list/gazPER-p.dat` (the Chilean person-name parts, copied as they are) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/data/grammatical-lists/freeling-cl/CL.{adj,adv,demonyms,int,nom}.GRAM.txt`, `CL.{tanc,vaux,verb}.Vos-V.GRAM.txt`, `CL.{peoplenames,orgnames,cities}.GRAM.txt` |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/data/grammatical-lists/freeling-cl/metadata/tagset.dat` (the Chilean tagset) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/data/escl-sources/*.tsv` (the build's own sources: the decisions of the spelling reviews that the build reads, and the name decisions: `fixed-name-classes`, `person-name-removals`, `place-only-forms`, `sentence-start-classes`, `name-class-shares`; see "The sources" below) |
| reads | `escl-sources/stand-ins.tsv` (the stand-in tokens every user map tags; see "The configs and user maps") |
| checks | the linked decisions folder (`--linked-folder`), when it exists: every file there of a kind the build reads must be a link to its file in `escl-sources`, and every file in `escl-sources` must have its link there. Without the folder the check is skipped and the log says so |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/es-cl/{probabilitats.dat,locucions.dat}` (the deployed Chilean data) |
| reads | `FreeLing_es-CL_2027_README.md` next to this script |
| copies | into the release's `software/` folder: this script, `freeling_escl_deploy.py`, `freeling_escl_configs.py`, their READMEs and the release README (all from this script's folder), and the explode scripts `explode-{ADJECTIVES,ADVERBS,INTERJECTIONS,NOUNS-ALL-GENDERS,NOUNS-ONLY-PLURALIZE,VERBS}-4-FreeLing.pl` with `explode-VERBS-4-FreeLing_README.md`, from `--explode-dir` or, when that folder lacks them, from this script's folder |
| calls | `freeling_escl_configs.py`, beside this script, to write the configs, their user maps and the CoNLL columns file (see "The configs and user maps") |
| copies | into `sources/escl-sources/`: every `escl-sources` file read, and `escl-sources/README.md`, so the release can be rebuilt from itself |
| copies | into `software/patches/`: the changes to FreeLing's code, from `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/patches/`: the name classes of the name recognizer and classifier (`freeling-4.2-np-classes.patch`, its README, `np.cc`, `np.h`, `nec.cc`) and, since 2.10.0, the known-roots change of the affix analysis (`freeling-4.2-known-roots.patch` and its README) and, since 2.18.0, the probability columns (`freeling-4.2-tag-probabilities.patch` and its README) and the ambiguous multiwords (`freeling-4.2-ambiguous-multiwords.patch` and its README) |
| reads | `/path/to/project/derived-software/FreeLing_es-CL_2027/config/freeling-release-privacy.tsv` (the privacy file: private, never copied into the release; see "The release is public") |
| copies | `agpl-3.0.txt`, next to this script (the GNU AGPL 3.0, checked by sha256), into the release as `LICENSE` |
| copies | the packaging of FreeLing 4.2 with this release for Fedora, Debian and Ubuntu, from `/path/to/project/derived-software/FreeLing_es-CL_2027/packaging/`: the seven scripts and their READMEs into the release's `packaging/` folder, and `packages.yml`, the GitHub workflow that builds and checks the packages, into `.github/workflows/` (see "The packaging") |
| writes | `/path/to/FreeLing-es_CL-2027/`, with `.gitignore` (`corpora/`) |
| moves | a previous build to `/path/to/software/deprecated/FreeLing-es_CL-2027.DEPRECATED-YYMMDD[letter]`, and a build under the former name, `FreeLing_es-CL_2027`, to `deprecated/FreeLing_es-CL_2027.DEPRECATED-YYMMDD[letter]` |
| carries over | the `corpora/` folder (or link) of the previous build, unread and unchanged, into the new one (see "The corpus folders") |
| copies | into `software/`: the tagging tools, `freeling.py`, `freeling_common.py`, `freeling_ud.py`, `freeling_perkins.py`, `freeling_parquet.py`, `freeling_server.py`, `freeling_analyzer.py`, their READMEs and `freeling_comma_multiwords.txt`, from this script's folder |

## Usage

```bash
freeling_escl_build.py --dry-run
freeling_escl_build.py
```

| Option | Default |
|---|---|
| `--root` | the project root, found from the script's location by `PROJECT_ROOT.txt` |
| `--source-tree` | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2` |
| `--build-tree` | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/es-cl` |
| `--decisions` | `<project root>/derived-software/FreeLing_es-CL_2027/data/escl-sources` |
| `--linked-folder` | `/path/to/corpus/decisions` (the folder whose links are checked, when it exists) |
| `--out` | `/path/to/FreeLing-es_CL-2027` |
| `--explode-dir` | this script's folder, where the explode scripts are |
| `--patches` | `../patches` beside this script's folder: `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/patches` |
| `--packaging` | `../packaging` beside this script's folder: `/path/to/project/derived-software/FreeLing_es-CL_2027/packaging` |
| `--privacy` | `freeling-release-privacy.tsv` in the folder above this script's: `/path/to/project/derived-software/FreeLing_es-CL_2027/config/freeling-release-privacy.tsv` |
| `--dry-run` | build and check everything in memory, write nothing |

The build is written to `FreeLing-es_CL-2027.part` and moved into place only
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
   R8 (final s dropped: tenís > tení) adds the voseo reading beside the
   preterite, 1st person, of the same verb when the -í form is one (salís >
   salí, comís > comí: decided 261116); otherwise it adds only new forms.
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
   the voseo one) and the 19th-century one (both readings), and the
   tuteo-tagged dictionary, zipped; writes FreeLing's own entries and remove
   files and refuses unless FreeLing's build-dict would give the same two
   dictionaries.
10. Writes `probabilitats.dat` (the decided names, the rare interjections,
    mm, hm, the four imperatives, the unaccented future, poder over podar,
    reír over reir (2.10.0), the readings kept at the start of a sentence),
    `locucions.dat`
    (FreeLing's general multiwords merged in, ya_poh, the multiword interjections, the decided multiwords: see "The multiwords"), `locucions-MINIMAL.dat` and
    `quantities.dat` (the Chilean peso, UF, UTM, the euro's code, and 56
    unit names removed: see "The units removed" below), and
    `data/es/afixos.dat`, FreeLing's affix rules with the clitic rules
    restricted (2.11.0: see "The attached pronouns" below).
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
      (every proper-noun tag of the dictionary: place, person,
      organization, other, each also with gender and number; a dictionary
      with a proper-noun tag that is not in the list refuses the build),
      `<ClassesAtSentenceStart>` (no
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
`/path/to/project/derived-software/FreeLing_es-CL_2027/data/escl-sources/`.
The decisions folder of a speech corpus
(`/path/to/corpus/decisions/`)
holds a relative link to each of them, so the spelling step
(`the spelling step of a speech corpus`) reads the same files through the links.
`freeling_escl_sources_move.py` made the move and the links on 261112 and is
retired (2.16.0); the build's own link check reports their state.

The kinds of file (the part of the name before `--`): `all-corpora-replacements`,
`correction-lemmas`, `dictionary-addition-removals`, `dictionary-additions`,
`dictionary-additions-all-rounds-standardized`, `dictionary-variants`,
`fixed-name-classes`, `interjection-removals`, `interjections`,
`lemma-standardization`, `locution-removals`, `locutions`, `dictionary-words`, `19th-century-attested-spellings`, `name-class-shares`, `person-name-removals`,
`place-only-forms`, `sentence-start-classes`, `text-correction-removals`,
`text-corrections`, `verb-form-readings`, and since 2.9.0 `reading-removals`,
`form-probabilities`, `informal-readings`. All are lists of words and forms;
none quotes the interviews.

Every round of every kind is read, and a later round wins for the same expression: the same form, or the same lemma in `lemma-standardization` (decided 261112: per expression, never a whole file). Something is taken out only by a removals kind (`dictionary-addition-removals`, `interjection-removals`, `text-correction-removals`, `locution-removals`, `person-name-removals`, `reading-removals`), never by leaving it out of a later round. The one exception is `dictionary-additions-all-rounds-standardized`, which is itself every round of additions merged: only the newest is read, and it must be at least as new as the newest round of additions.

`locutions`, `locution-removals`, `dictionary-words`, `19th-century-attested-spellings`, `reading-removals`, `form-probabilities` and `informal-readings` are not decisions of the speech corpus spelling review: they live only in `escl-sources` and need no link in the speech corpus's folder; nor does the hand-edit file `dictionary-hand-edits.tsv`. The files that do (the occurrence rulings, the
ir + hacer and sino occurrences) and a speech corpus-only records stay ordinary
files in the speech corpus's folder.

Before building, the build checks the links both ways and refuses on any
of these: an ordinary file of one of these kinds in the speech corpus's folder (it
would never reach the build: a new round must be saved in `escl-sources`),
a link there that does not lead to its file in `escl-sources`, and a file
in `escl-sources` with no link (the spelling step would never see it).

A new round is saved in `escl-sources` and linked from the speech corpus's folder
with a relative link (as every link in the project).

The release carries a copy of every source file read, in
`sources/escl-sources/`, with its README.

## The 19th-century dictionary (decided 261112, 261113)

The 19th-century dictionary is FreeLing es-CL 19th Century: the 2027 dictionary with the vosotros readings of the -is forms and the polite vos (as before), plus:

- **the 19th-century spellings**, generated from every correctly spelled form but the proper nouns (`HIST_RULES`: Bello and García del Río 1823, Sarmiento 1843, the Chilean orthography of 1844, the Chilean neographers): g before e/i as j, x for the j sound as j (a short list, `X_TO_J`), x before a vowel as cs, x before a consonant as s, vowel y as i, c before e/i as s or z, z as s, qu as q or k, c for the k sound as k or q, the silent u of gue/gui dropped, silent h dropped before a vowel, v as b, the trill as rr. Every combination is generated, in that order (g as j before gue loses its u), and a rule changes every place it applies in a word. Accents are never dropped. Each spelling gets the readings of the form it comes from. Into `19th-century/dictionary/entries/CL.19th-century-spellings`;
- **a spelling that is already a word** is added only when the rules of the 1844 orthography (`BELLO_ADOPTED`: g as j, y as i, x as s) give it; its new readings are nearly impossible on their own in `19th-century/probabilitats.dat` (a zero count for their short tags, as for the rare interjections), and where they share a short tag with the word's own readings, the word's own lemma is preferred (LemmaPreferences). Any other rule's spelling that is already a word is not added;
- **five words decided one by one** (`HIST_READINGS`, decided 261113): i is y and the letter i, rei is rey only, lei is ley only, hai is hay only, soi is never voseo; and two probabilities (`HIST_PROBS`): i is y 99%, testo is texto 90% and testar 10%. A reading of the Chilean lists one of them drops (rei as a name, the voseo readings of hai and soi) is listed in `19th-century/CL.removed-from-chilean-entries`, since FreeLing's build-dict applies a remove folder to the Spanish entries only;
- **the attested spellings** of `19th-century-attested-spellings--*.tsv` (from a word list of 19th-century spellings and the pre-reform spellings taken out of the contemporary word list on 260811) with an extra or a moved accent get the readings of the one modern form with the same letters; a spelling with several such forms, or one that lacks an accent the modern form has, is not added. Into `CL.19th-century-attested`;
- **vosotros over voseo**: the tag preferences (PosPreferences) of `19th-century/probabilitats.dat` prefer each vosotros tag to its voseo tag and the polite vos to the voseo one. Both readings have the same short tag, so no share can be given: the preference is absolute;
- **the multiwords** in the 19th-century spellings (`key_variants`; a `<lemma>` token is left alone), when the key is new: `19th-century/locucions.dat`;
- **its config**, `data/config/es-cl-19th-century.cfg`: FreeLing 4.2's es-cl config (`data/config/es-cl.cfg`, carried in the script and sha256-checked) with the Chilean tagset and currencies, the 19th-century dictionary, probabilities and multiwords, and compound analysis off: FreeLing builds its compound analyzer from every form of the dictionary with foma, whose stack holds 2,097,152 entries, fewer than this dictionary has (FreeLing stops with "Stack full!"). `data/config/es-cl.cfg` is the same for the 2027 data, and since 2.15.0 has compound analysis off too (see "Compound analysis off in every config"). The two files of the 19th-century folder name `../tagset.dat`, the Chilean tagset in the folder above.

The build checks that FreeLing's build-dict would give the 19th-century dictionary from the Spanish entries minus `19th-century/remove/CL.removed`, the Chilean entries minus `19th-century/CL.removed-from-chilean-entries`, and the three 19th-century entries files.

## The configs and user maps (2.16.0, decided 261119)

The build calls `freeling_escl_configs.py` (beside it) to write, into the
release's `data/` folder, one config per kind of text, the CoNLL columns
file and one user map per config:

| File | Kind of text | Dictionary | Name recognizer | User map adds |
|---|---|---|---|---|
| `config/es-cl.cfg` (the default) | modern writing | `es/es-cl/dicc.src` | `es/es-cl/np.dat` | - |
| `config/es-cl-informal.cfg` | informal modern writing | `es/es-cl/informal/dicc.src` | `es/es-cl/np.dat` | the chat readings of `usermap-informal.dat` |
| `config/es-cl-speech.cfg` | transcribed speech | `es/es-cl/dicc.src` | `es/es-cl/np-speech.dat` | nn and nnn as the hesitation |
| `config/es-cl-19th-century.cfg` | 19th-century writing | `es/es-cl/19th-century/dicc.src`, with its own probabilities and multiwords | FreeLing's own (`es/nerc/nerc/nerc.dat`) | - |
| `config/es-cl-conll-columns.cfg` | the CoNLL columns every config names | | | |

Every config is FreeLing 4.2's es-cl config (carried in this script) with
the Chilean tagset and currencies, compound analysis off, one sentence per
line (`AlwaysFlush=yes`), CoNLL output with the columns file, name
classification, UKB word senses, the retokenizing tagger and the LSTM
parser (`DepLSTMFile`), and its user map: the settings the corpora have been
tagged with since 261110. Old Spanish is FreeLing Old (`es-old.cfg`, as
FreeLing ships it, compound analysis already off); it is not written here.

Every user map (`data/es/es-cl/usermap/<config>.dat`) holds the stand-in
tokens of `escl-sources/stand-ins.tsv` (form, tag, meaning; copied into the
release's `sources/escl-sources/` and `data/es/es-cl/stand-ins.tsv`),
lowercased, then novela, vela and velo as common nouns. A stand-in is XXX +
capital letters + XXX; a malformed line, a repeated form or an empty file
refuses the build. The five stand-ins: XXXREDACTEDXXX (Fz), XXXUNINTELLIGIBLEXXX
(Fla), XXXNONSPEECHXXX (Flt), XXXURLXXX (Fz), XXXEMAILADDRXXX (Fz).

Until 2.15.0 the release had three thin configs (FreeLing's es-cl config with
the dictionary swapped, no name recognizer of its own, no user map, so the
informal readings were never read), and the corpora were tagged with
separate configs written by `the former config writer`. That script is
retired: the configs of the release are the configs everything is tagged
with.

## Compound analysis off in every config (2.15.0, decided 261118)

Every config of the release, `es-cl.cfg` and `es-cl-informal.cfg` as well as `es-cl-19th-century.cfg`, says `CompoundAnalysis=no` and comments out the `CompoundFile` line. FreeLing's compound module splits a word it does not find in the dictionary into two words it does know, by the patterns of `es/compounds.dat` (verb + noun, noun + noun, adjective + adjective). In the interviews of a speech corpus, where the unknown words are mostly fragments, misspellings and foreign words, nearly everything it built was wrong: 458 compound lemmas, 1,039 tokens, among them pentecostal as pente + costal (the lemma repente_costal), veinti as ve + inti, toballa as toba + ll, down as do + huevón (the speech corpus HOWTO, Section 13.14). The user (261118): "Compound analysis is disastrous", and it is to be off everywhere, the public release on GitHub included. With it off, an unknown word goes to FreeLing's guesser and keeps its own form as its lemma. Your corpus's own configs are written by `the former config writer` (1.6.0), which turns it off in all of them.

## The accented one-syllable forms and the common misspellings (decided 261112)

- `CL.old-accents`: fué, fuí, dió, vió, á, é, ó, ú (`OLD_ACCENTS`), each with every reading of fue, fui, dio, vio, a, e, o, u, in both dictionaries.
- `CL.common-misspellings` (formerly `CL.misspellings`): the misspelt forms of the transcriptions, read as their corrections, as before, and every correctly spelled form with a written accent or a diaeresis, written without them, read as that form, when the result is not already a word and comes from that one form only. A form whose readings all come from the misspelt or the non-standard forms is never a source. After the build, every line of `CL.common-misspellings` and `CL.old-accents` must be in `dicc.src` and in `19th-century/dicc.src` with exactly its readings, or nothing is written.

## Dictionary words and hand edits (decided 261112, 261113)

- `dictionary-words--YYMMDD.tsv` (form, lemma, category, tag, notes), in `escl-sources` only (no link in the speech corpus's folder): with a tag, exactly that reading (a tag the Chilean tagset cannot decode refuses the build); without one, the category's readings, as for a decided addition (nouns and adjectives with their other number and gender, new verbs with their whole paradigm). Every round is read; a later round wins for the same form, lemma and tag (since 2.9.0; until then a form with several readings of one lemma, such as sr with señor AQ0MS00, I and NCMS000, kept only its last row). A form or lemma with a space refuses the build: a multiword goes in `locutions`. A contraction is written as al and del are: lemma `para+el`, tag `SP+DA` (pal, decided 261115), one tag part per lemma part. A reading decided with its exact tag keeps it: neither the exemption of names that are also common nouns or verbs (decided 261110b) nor the standard lemmas of `lemma-standardization` change it (2.9.0: the nicknames, whose lemma is the nickname itself; until then the exemption took the proper-noun reading of ale, pancho or pato away again, and the standard lemmas turned the nickname jose into josé).
- `dictionary-hand-edits.tsv` (form, lemma, tag), in `escl-sources`, with no round: edited in place; `#` lines are comments and say what goes in it. Every line is added at every build; a tag the Chilean tagset cannot decode refuses the build. It is copied into the release's `sources/escl-sources/`.

## The multiwords (decided 261112)

FreeLing reads one multiword file, the one the config's `LocutionsFile` names, and your corpus configs name the Chilean one, `es/es-cl/locucions.dat`. Until 2.7.0 that file held only the Chilean multiwords (2,058), so every general Spanish multiword (o sea, por ejemplo, por lo menos, a pesar de ...) was split into its words in every corpus tagged with it. From 2.7.0 the build merges FreeLing's general file, `data/es/locucions.dat` (sha256-checked against FreeLing 4.2), into the Chilean one:

- every general entry whose key the Chilean file does not have is added, with the same repairs as the Chilean entries (capitalized keys lowercased, duplicate lines merged); each is a row of `CHANGELOG.tsv` (rule "FreeLing's general multiword");
- for a key in both files the Chilean entry wins (ni_fu_ni_fa stays an adjective); a general entry that differs from the Chilean one is logged as "not added";
- FreeLing's general file tags tal y cual as `Fs`, a punctuation mark: it gets `PI0CS00`, as cual has (`LOCUTION_TAG_FIX`);
- on 261112's sources: 2,058 Chilean lines, 1,563 general lines added, 3,613 entries.

The decided multiwords come from two kinds of file in `escl-sources`:

| Kind | Columns | A row means |
|---|---|---|
| `locutions--YYMMDD.tsv` | form, lemma, tag, flag (further columns ignored) | the multiword is joined with this lemma and EAGLES tag. Since 2.9.0 the tag column may hold several tags separated by spaces (la_muerte: `NCFS000 AQ0CN00 RG`), and the lemma column one lemma for all of them or one per tag, in the same order; a `$1:NC` tag copies the tag of word 1 (`<plaza>_de_armas`). Flag I: always joined; A: ambiguous, FreeLing's tagger decides between the multiword and the separate words (only with the ambiguous-multiwords change to FreeLing's code, `freeling-4.2-ambiguous-multiwords.patch`: FreeLing 4.2 itself reads the flag and never uses it); since 2.18.0, A with a weight above 0 and below 1 (`A:0.9`), the weight given to the words being the multiword (A alone gives none). An empty lemma is the form joined by `_`; an empty flag is I. A tag the Chilean tagset cannot decode, a flag other than I, A or A with such a weight, or a number of lemmas that is neither one nor the number of tags refuses the build. A later round wins for the same multiword; a decided multiword replaces any entry with its key |
| `locution-removals--YYMMDD.tsv` | form, why | the multiword is removed: its words are tagged separately. A removal of a key the file does not have is logged in `CHANGELOG.tsv` as already removed (since 2.9.0: every round is read at every build, and the deployed file a build starts from no longer has a key an earlier build removed, so 2.8.1 refused every build after the first that removed a multiword) |

The form is written as it is said (al final); the build writes the key as FreeLing matches it, splitting al and del (`a_el_final`), as FreeLing splits them before it matches multiwords. A form with a `<lemma>` pattern (`<dar>_lo_mismo`) is taken as written. Every row is a row of `DECISIONS.tsv`.

## Reading removals, probabilities and readings for informal writing (decided 261115)

Three kinds of file in `escl-sources`, none linked in the speech corpus's folder:

| Kind | Columns | A row means |
|---|---|---|
| `reading-removals--YYMMDD.tsv` | form, lemma, tag, why | that reading is taken out of every dictionary (the reduced forms of the informal one included), whatever list it came from, FreeLing's Spanish dictionary included (it then goes to `remove/CL.removed`): hueva as fish roe, pal as a noun, aki as a name, the common-gender readings of garúa and taima. It is applied after every other step, so its lemma is the final one (hoc, a variant of ok, has ok's readings with the lemma okay). A form left with no reading is not in the dictionaries: FreeLing guesses it like any unknown word. A reading neither dictionary has is listed in `DECISIONS.tsv` as not present, not refused |
| `contemporary-reading-removals--YYMMDD.tsv` | form, lemma, tag, why | that reading is taken out of the default dictionary, and so out of the informal one built from it, and kept in the 19th-century one: an old spelling that FreeLing's Spanish dictionary lists as modern. The first round, `contemporary-reading-removals--261126.tsv`, takes carácteres (the old plural of carácter; the modern one is caracteres) and cánon (canon). The reading goes to `remove/CL.removed` and not to `19th-century/remove/CL.removed`. It is applied after `reading-removals`. A reading the default dictionary does not have is listed in `DECISIONS.tsv` as not present |
| `form-probabilities--YYMMDD.tsv` | form, tag, share | the share (percent) of that reading of the form, for a word or a multiword. The shares are summed by FreeLing's short tag (2 letters for nouns and adjectives, 3 for verbs, 1 for interjections); the short tags not named share what is left equally, with at least one count each; a short tag with two readings has its share split between them. The line, scaled to 1000, replaces any line the build would write for the form. A word's readings are those of the default dictionary plus its informal readings (`probabilitats.dat` is read by every config); a multiword's are those of its `locutions` row. A tag the form does not have refuses the build. Two readings with the same short tag cannot get different shares (santiago as a place and as a name are both NP): FreeLing's probabilities know only short tags |
| `informal-readings--YYMMDD.tsv` | form, lemma, tag, why | a reading for informal writing only (mb as muy bien, t as te, tas as estás). It goes into no dictionary: the build writes `data/es/es-cl/usermap-informal.dat`, one line per form with all its readings, the default dictionary's and the informal ones, because FreeLing's user map locks a word's readings and the dictionary is then not read for it. Each key matches the form in any capitalization, letter by letter (`^[mM][bB]$`), as the user map matches case-sensitively. Only the configs for informal writing read it (`the former config writer` 1.3.0: the informal writing of a written corpus), never a speech corpus or formal writing |

An interjection that `interjections` decides keeps only the lemma given there: a change of its lemma goes into a later `interjections` round (ok, okey, okay, oki and oka with the lemma okay, decided 261115), not into `dictionary-words`, whose interjection reading of another lemma the interjection step would take out.

## Readings left out of the informal user map (2.17.0, decided 261119)

`informal-reading-removals--YYMMDD.tsv` in `escl-sources` (form, lemma,
tag, why): a reading of the default dictionary that the informal user map
leaves out, so that informal writing reads the form only as its other
readings. The dictionaries keep it, so formal writing and speech still have
it. The first file, `informal-reading-removals--261119.tsv`, takes the
nouns out of tas (tas NCMN000) and tar (tar NCMS000): in informal writing
tas is estás and tar is estar, and nothing else. A row naming a reading the
informal user map does not have (a form without an informal reading, or a
reading the dictionary lacks) refuses the build. Listed in `DECISIONS.tsv`
as `informal reading removed`.

## The corpus folders (2.17.0, decided 261119)

The tagging tools (`freeling.py` and the rest, copied into `software/`)
keep one folder per corpus in `corpora/` in the release folder: a real
folder or a link. The build never reads it, never lists it in `SHA256SUMS`
and never checks it for private text; it moves it, as it is, from the
previous build (or from a build under the former name) into the new one,
after the new one is complete and before the previous one goes to
`deprecated/`. `.gitignore` holds `corpora/`, so it is never uploaded. Two
`corpora/` (in the previous build and under the former name) refuse the
write; a `corpora/` left in `FreeLing-es_CL-2027.part` by a build that
stopped refuses the next build until it is moved back.

## The decision files of the names

In `/path/to/project/derived-software/FreeLing_es-CL_2027/data/escl-sources/`,
tab-separated, one header line, every round read, later rounds winning:

| File | Columns | A row means |
|---|---|---|
| `fixed-name-classes--*.tsv` | name, class, source, ruling | the name always has this class: place, person, organization or other; none: it is not fixed, even if the build would derive it (Navidad). Two different classes for one name in one round refuse the build |
| `person-name-removals--*.tsv` | entry, list, ruling | the entry (as FreeLing writes it, lower case, words joined by _) is removed from the list; the list must be `gazPER-c.dat` |
| `place-only-forms--*.tsv` | form, ruling | the form is a place and nothing else |
| `sentence-start-classes--*.tsv` | form, reading, keep own readings, share, files, ruling | at the start of a sentence the one-word form gets the reading (name: the classifier decides; place, person, organization, other), whatever the other rules say. Keep own readings: no, they are dropped; yes, they stay beside it; or word classes (verbs, nouns, adjectives, adverbs, pronouns, determiners, interjections, prepositions, conjunctions, numerals, separated by commas): only those stay. With readings kept, share is the new reading's percentage among the readings the word has there (above 0, below 100); with no, share is empty. Files: written (`np.dat`), speech (`np-speech.dat`) or both. A form may have one row for written and another for speech (decided 261110g: Pinto); a later file's row replaces the earlier rule for the files it names, and two rows of one file for the same form and file refuse the build. A form with no dictionary reading to keep, with no reading of the classes named, or that already has a proper-noun reading or a probability line of its own refuses the build; so does a form that keeps its own readings in both files with a different reading, share or word classes, as `probabilitats.dat` holds one line for both |
| `name-class-shares--*.tsv` | name, class, share, ruling | when the classifier classifies the name, it takes one of the classes of its rows, by its own weight plus half the log odds of the share (percent). The rows of a name in one file must add up to 100; a later file's rows for the name replace the earlier ones. A name with shares must not also have a fixed class |

## The attached pronouns (afixos.dat, decided 261116)

FreeLing's clitic rules (the rules of `<Suffixes>` in `data/es/afixos.dat` whose last field splits the word into the verb and its pronouns, `$$+te+lo:$$+PP+PP`) attach every pronoun to any imperative (`^V.[GNM]`), so te was attached to the usted, ustedes and nosotros imperatives too (sáltetelo as salte + te + lo, which Spanish does not have), and the rules for te twice gave sal + te + te + lo. The user's rule (261116): te and os attach only to tú and vosotros imperatives, infinitives and gerunds, and never twice. The build writes FreeLing's file (sha256-checked) with these changes only, each a row of `CHANGELOG.tsv` (list `afixos`):

| Rules | Count | Change |
|---|---|---|
| a clitic rule with te twice, or with te and os (tetelo, teoslo and their forms) | 8 | removed: tú and vosotros pronouns together are not Spanish either (user, 261116) |
| a clitic rule with te attached to any imperative (te, telo, sete, setelo, temelo, tenoslo and their forms) | 18 | attached to an infinitive, a gerund or a tú imperative only: `^(V.[GN]|V.M02S)` (sé + te + lo, the tú imperative of ser, included) |
| a clitic rule with os attached to any imperative (oslo, osle, seos, seoslo and their forms) | 11 | attached to an infinitive or a gerund only: `^V.[GN]`; os after a vosotros imperative is FreeLing's own rules, which drop the d (sentad + os: sentaos) |

The counts are `AFFIX_COUNTS` at the top of the script; another count refuses the build. The file goes into the release as `data/es/afixos.dat`, and `freeling_escl_deploy.py` (2.4.0) and the packaging's `install-data.sh` (1.2.0) put it over FreeLing's `es/afixos.dat`, which every Spanish config reads (FreeLing Old has its own, `es/es-old/afixos.dat`). FreeLing's build tree keeps FreeLing's own file, which the build reads.

## The reduced forms (CL.reduced-forms, the informal dictionary, decided 261116)

Chilean speech drops the d of -ado, -ada, -ido and -ida (cansá, pescao, la cagá, he comío, el marío, ha sío), and informal writing (Reddit, YouTube, forums, Usenet, IRC, email) writes the forms so. They are for informal writing only (user, 261116: "All the -ado = -ao, -ido = ío, etc. forms are for INFORMAL SPEECH only"; "Never [the speech corpus] - that was transcribed using standard orthography"; the -ido forms: "yes, -ido should have -ío forms"). A speech corpus's text is normalized to standard spelling instead (cansá to cansada, pescao to pescado; the speech corpus HOWTO, Section 13.12). After the common misspellings (step 9d), every word of the dictionary in -ado, -ada, -ados, -adas, -ido, -ida, -idos or -idas with a participle, adjective or noun reading (`REDUCED_CLASSES`: VMP, VAP, VSP, AQ, NC) gets its reduced form, -ao, -á, -aos, -ás, -ío, -ía, -íos or -ías (`REDUCED_ENDINGS`), with those readings and their lemmas; the readings of the misspelt and non-standard forms are not copied. They go into `informal/dictionary/entries/CL.reduced-forms` and the informal dictionary, `data/es/es-cl/informal/dicc.src`, which is the default dictionary with these lines added (the build checks that FreeLing's build-dict gives it from the default entries and remove files and this file). They are in neither the default nor the 19th-century dictionary, and the entries file is outside the default `dictionary/entries/` folder, which FreeLing's own build reads whole. The informal config, `data/config/es-cl-informal.cfg`, is `es-cl.cfg` with that dictionary; it shares the default probabilities and multiwords. The informal user map, `usermap-informal.dat`, lists each form's readings from the informal dictionary.

- A word with a closed-class or adverb reading (nada, cada, demasiado) gives no reduced form.
- A word stressed before its ending gives no reduced form ("stressed before the ending"): década no décá, nómada no nómá, rápido no rápío, sábado no sábao, hígado no hígao (user, 261116: "Neither of these forms exist").
- A reduced form that is already another word is not added (`CHANGELOG.tsv`, list `reduced-forms`, "not added"): papá, mamá, además, jamás, amará, está, vía, garantía, manía, lío.
- A reduced form already in the dictionary whose lemmas are all those of the full form, or the full form itself (volaos, volado; apuraos, apurado: added in the spelling rounds), gets the readings it lacks: comío (comer VMIS3S0, a common misspelling of comió) gets the participle of he comío, cachá (cachar VMIP2SV) that of la tengo cachá; `REDUCED_UNION` (callao, callaos) gets them beside its own.
- Except an imperfect, a conditional or a 3rd person present ("already an imperfect, conditional or 3rd person present"): comía, salía, sentía, quería, podría (from comida, salida, sentida, querida, podrida) and dá keep their own readings and get no participle. These are 1,655 forms; giving each a participle reading would have the tagger choose between the imperfect and the participle in every sentence with comía or quería, and the imperfect is far the commoner. A spoken la pera está podría is therefore tagged as the conditional; write it in a decision round (`dictionary-words`) if a corpus needs it.
- A form written without its accents (rapido) is a common misspelling, and the readings of the common misspellings are never reduced.
- `reading-removals` take readings out of the reduced forms too: andá, mirá, caminá and cantá are Argentine only (user, 261116), so `reading-removals--261116b.tsv` takes out their participle and noun readings and `dictionary-words--261116d.tsv` gives them the Argentine voseo imperative, VMM02SV, in every dictionary.
- The probabilities file is shared: a form whose probabilities are decided (`form-probabilities`) has them over its default readings; a reading the informal dictionary adds to it (cachá, cachar, participle) gets FreeLing's smallest share.
- No 19th-century spelling is generated from a reduced form.

## The units removed from quantities.dat (decided 261112)

FreeLing's quantities module joins a number and the unit name after it into
one token (tag `Zu`, lemma `TM_d:2` for dos días). It compares the word in
lower case, and accepts "number de unit". In a speech corpus a number followed by an
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
a speech corpus after this: about ten false starts before an ellipsis read as
meters or liters ("dos m ...", "uno l ..."), which the file cannot tell
from the units; they are for the correction layer.

## The release is public (decided 261112)

The release goes to GitHub, so no file in it may hold a private path or
name. The privacy file says what is private:

```text
/path/to/project/derived-software/FreeLing_es-CL_2027/config/freeling-release-privacy.tsv
```

It is TAB-separated, UTF-8, with the header `private<TAB>public`. A row
with a public text is a replacement (`/path/to/home<TAB>/home/user`); a row
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

The release folder is the GitHub repository Linguista/FreeLing-es_CL-2027, and GitHub builds from it packages of FreeLing 4.2 with this release (`freeling-es-cl`) for Fedora 43 and 44, Debian 13 and Ubuntu 24.04 and 26.04, each built on its own distribution, installed on a fresh one and checked before it is attached to a release. The scripts that do it are kept in the project, in `derived-software/FreeLing_es-CL_2027/packaging/`, each with its README, and the build copies them into every release: the scripts into `packaging/`, the workflow `packages.yml` into `.github/workflows/`, where GitHub looks for it. So a rebuilt release folder is the complete repository.

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

261119, version 2.18.0, full builds on the test tree with the escl-sources of 261119, without and with the round of 261119 (`interjections--261119.tsv`, `dictionary-words--261119.tsv`, `form-probabilities--261119.tsv`). Without it, every data file as 2.17.0 built it. With it: `probabilitats.dat` has `bueno AQ-I AQ 700 I 300` (was `AQ 10000 I 0`) and `ok AQ-I-RG AQ 500 I 200 RG 300`, the same for okey and okay; the lines of listo and exacto, which an earlier build wrote with the interjection at 0, are removed (FreeLing has none for them), and vamos has FreeLing's own line again (`vamos I-VMI-VMM I 1 VMI 33 VMM 0`); `dicc.src` has `ok okay AQ0CN00 okay I okay RG`, and the same three readings for okey and okay. A round marking a multiword `A:0.9` is written with that flag to `locucions.dat`, and a build on its own output keeps it. The four patches and their READMEs are copied into `software/patches/`. The release was then installed over FreeLing 4.2 built with the four changes, and `packaging/test-freeling.sh` 1.7.0 passed.

261118, version 2.15.0, the config writer run on FreeLing 4.2's carried es-cl config against 2.14.0: `es-cl.cfg` differs in exactly two lines, `CompoundAnalysis=no` and `#CompoundFile=$FREELINGSHARE/es/compounds.dat` (so does `es-cl-informal.cfg`, which is written from it); `es-cl-19th-century.cfg` is byte for byte the same; no problem reported. The data files are not touched by this change.

261116, version 2.14.0, a full build on the test tree of 2.13.0 with the rounds `reading-removals--261116b.tsv` and `dictionary-words--261116d.tsv`: `CL.reduced-forms` 41,547 lines (36,969 forms; not added: already a word 110, an imperfect, conditional or 3rd person present 1,655, stressed before the ending 863, each listed), in the informal dictionary only; 939,427 forms in the default dictionary, 976,371 in the informal one and 2,148,107 in the 19th-century one; FreeLing's build-dict gives all three. FreeLing 4.2 with the name-class and known-roots changes, with the default and with the informal dictionary: estoy super cansá cansá VMIF3S0 (guessed) and cansar VMP00SF; el pescao estaba helao pescado NCMS000 in both (a word of the spelling rounds, in every dictionary) and helao guessed, and helar VMP00SM; ya ha sío mucho sío guessed, and ser VSP00SM; he comío comer VMIS3S0 (the common misspelling of comió), and comer VMP00SM; mirá mirar VMM02SV in both; el sábao unknown in both. `the former config writer` 1.5.0 on the release's data: only the informal config names the informal dictionary.

261116, version 2.13.0, a full build on the test tree of 2.12.0 with the rounds `text-corrections--261116.tsv`, `correction-lemmas--261116.tsv` and `dictionary-words--261116c.tsv`: `CL.reduced-forms` 41,583 lines (37,041 forms; 2,787 lines of -ío, -ía, -íos, -ías; not added: already a word 110, already an imperfect, conditional or 3rd person present 1,655, stressed before the ending 837, each listed), 976,397 forms in the default dictionary and 2,184,741 in the 19th-century one; against 2.12.0, the -ado forms the same but 49 (the -á and -ás of 48 words stressed before the ending, décá, nómá, tríá, and the participle of dá). FreeLing 4.2 with the name-class and known-roots changes and this release: ya ha sío mucho ser VSP00SM, el marío marido NCMS000, he comío comer VMP00SM, estaba re dormío dormir VMP00SM, el vestío vestido NCMS000, la tengo cachá (the multiword tener_cachado), ella comía pan comer VMII3S0, la década pasada década NCFS000; poné poner VMM02SV; leélo has lost the name reading it had through the name Leelo.

261116, version 2.12.0, a full build on the test tree of 2.11.0 with the rounds `dictionary-words--261116b.tsv` and `form-probabilities--261116.tsv` (cachá): `CL.reduced-forms` 38,847 lines (34,686 forms; 87 not added, each listed), R8 850 forms beside the preterite (864 had been left out, 14 still are: nouns and names), 974,057 forms in the default dictionary (939,422 before) and 2,182,424 in the 19th-century one (2,148,101); FreeLing's build-dict check passed for both. FreeLing 4.2 with the name-class and known-roots changes and this release, against 2.11.0: estoy super cansá cansar VMP00SF (was cansá VMIF3S0), la cagá cagada NCFS000 (was VMIF3S0), la casa embarrá embarrar VMP00SF, el pescao pescado NCMS000, bien helao helar VMP00SM (was an unknown adjective), muy pesá pesado AQ0FS00, qué volá volada NCFS000, estaba callá callar VMP00SF (was an adverb), ¿cachá Lovecraft? cachar VMIP2SV; ayer salí temprano and yo comí pescado still the preterite.

261116, version 2.11.0, a full build on the test tree of 2.10.0 with FreeLing 4.2's `data/es/afixos.dat` added to its source tree: against the build of 2.10.0, every data file the same, byte for byte, and `data/es/afixos.dat` new (FreeLing's file with the 8 rules removed and 29 restricted, each in `CHANGELOG.tsv`); the report lists the new input and the 29 and 8 changes. FreeLing 4.2 with the name-class and known-roots changes and the new file, on the 299,875 forms of the known-roots test (infinitives, gerunds and imperatives with their pronouns, accents written): 33,536 lost a reading, all of them te after an usted, ustedes, nosotros or vosotros imperative or te twice; none after a tú imperative, an infinitive or a gerund. cómetelo come + te + lo, siéntete siente + te, írsete ir + se + te, dándotelo dar + te + lo, háztelo haz + te + lo, sentaos and sentaosla sentad + os (+ la), sételo sé (ser) + te + lo, as before; sáltetelo, which was salir + te + te + lo, one unknown word.

261116, version 2.10.0, full builds on the test tree with the escl-sources of 261115 and the rounds of 261116 (`reading-removals--261116.tsv`: compañar, delantar and vertir; `dictionary-words--261116.tsv`: ándale): against the build of 2.9.0, `dicc.src` lost `compañar acompañar VMN0000`, `delantar adelantar VMN0000` and `vertir verter VMN0000` and gained `ándale ándale I` and, as a common misspelling, `andale ándale I`; the 19th-century `dicc.src` the same five lines; both `probabilitats.dat` files gained the lemma preference `reír reir`; every other data file was the same, byte for byte. The 112 lines of `form-probabilities` were unchanged by counting per reading (none of their forms has two readings with one short tag). Built again on its own output, every data file byte for byte the same. FreeLing 4.2 with the name-class change, with and without the known-roots change, with this release: acompañarlo, adelantarse, revertirlo and invertirla split into acompañar, adelantar, revertir, invertir and the clitic; reírme, reírse lemma reír (with the known-roots change also split, as reír + me); ándale and ándate I in "vamos, ándale, ándate, calla", and ándate in "ándate para allá" the verb, ándate split as anda + te.

261115, version 2.9.0, full builds on the test tree with the escl-sources of 261115 (the rounds of 261115: 2,244 `dictionary-words` rows, 735 `locutions`, 4 `locution-removals`, 76 `reading-removals`, 112 `form-probabilities` rows, 72 `informal-readings`, 32 `interjections`, 2 `lemma-standardization`): every row found as decided in the release (each dictionary word in `dicc.src`, no removed reading left, each interjection with its lemma only, each multiword as written, each informal reading in `usermap-informal.dat` with all the form's dictionary readings); built again on its own output (its `probabilitats.dat` and `locucions.dat` as the deployed build tree's), every data file byte for byte the same. FreeLing 4.2 with the name-class change and this release tagged all 2,174 texts of a speech corpus with no error, and with the user map of informal writing: mb megabyte in speech and muy_bien in informal writing, t the letter in speech and te in informal writing, la muerte RG in "lo pasamos la muerte", pal para + el, pongámosle pongamos + le, la hueva huevada, hueá huevada, quique lemma quique and kike lemma kike, Kike NPMSSP0 and Codelco NPMSO00 when capitalized (NP00000 before the class list held the gendered tags), porfis porfiar after no, aveces a_veces, what the fuck one interjection, concha_de_tu_madre and mijitas_ricas (mijito_rico NCFP000) as decided, caso de and lo que más left as separate words.

261113, version 2.8.1, a full build on the test tree with no `data/config/es-cl.cfg` in its source tree: every file of the release byte for byte as 2.8.0 built it (both configs and both dictionaries included), except `BUILD-REPORT.md` (its version line and the config's input line), `software/freeling_escl_build.py` and `SHA256SUMS`.

261113, version 2.8.0, full builds on the test tree with the escl-sources of 261113 (and the rounds of 261113: `dictionary-words`, `locutions`, `19th-century-attested-spellings`, `dictionary-hand-edits.tsv`): 2027 dictionary 937,701 forms; 19th-century dictionary 2,146,645 forms (1,203,611 new spellings, 5,333 attested spellings, 518 words given a Bello reading, 6,539 multiwords); 140,895 unaccented forms, 516 left out; every line of `CL.common-misspellings` and `CL.old-accents` found in both dictionaries; FreeLing's build-dict check passed for both. FreeLing 4.2 compiled from source with `packaging/patch-freeling.sh` 1.1.0 (Spanish only) and this release installed: with `es-cl.cfg`, tenís is tener VMIP2SV, comeriamos is comer, colaboracion is colaboración, tatoo is tatuaje, cesfam and minipimer NCMN000, ponerse las pilas, me pongo las pilas, ponte las pilas and se puso las pilas one multiword each, dulce de leche, de a poco, flor de, buen día and medio pelo as decided; with `es-cl-19th-century.cfg`, jente gente, jeneral general, esplicó explicar, mui muy, hoi hoy, rei rey, i y, lei ley, hai hay, soi soy, á a, fué ser, ménos menos, ántes antes, órden orden, soziedad sociedad, zientífica científico, qeso queso, testo texto ("El testo del libro") and testar ("Testo mi casa a mis hijos"), salís vosotros; with `es-old.cfg` (FreeLing Old, its multiword file the link to the Chilean one), dixo decir, muger mujer, fermosa hermoso. `test-freeling.sh` 1.1.0 passed. Built again on its own output (its `probabilitats.dat` and `locucions.dat` as the deployed build tree's), every data file and both configs byte for byte the same. Memory: about 780 MB with 2027, 930 MB with the 19th century. Without compound analysis off, the 19th-century config stops FreeLing ("Stack full!").

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

261112: the link check, on a copy of the decisions folder of a speech corpus of
261112 after `freeling_escl_sources_move.py` moved its 41 files: no problem;
with one file put back as an ordinary file, one link removed and one
escl-sources file without a link, each refuses the build. The rest of the
build is unchanged; the first run on this machine, `--dry-run`, is its test
on the real inputs.

261110, in a copy of the inputs of this machine (FreeLing
4.2's files of the build tree, your corpus lists, the decisions of rounds 1 to
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
  a speech corpus probe of 261110 (22,394 exact place-name tokens in speech mode,
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

- 2.21.1 (261126): an attested 19th-century spelling loses a reading that a `reading-removals` file takes out. The attested spellings took their readings from the modern word before the removals ran, so ménos still carried the noun reading meno NCMP000 that menos had lost, and the build refused (the 19th-century dictionary would not have matched FreeLing's own build-dict).
- 2.21.0 (261126): a new kind of decision file, `contemporary-reading-removals`: a reading taken out of the default and informal dictionaries and kept in the 19th-century one, for the old spellings FreeLing's Spanish dictionary lists as modern (carácteres, cánon; decided 261126). The first round of `reading-removals` of the same day takes out the misspellings that dictionary lists as words (alemána, alemánes, inmediaciónes, remuneraciónes, varónes, mísiles, póstula, cópec, hólding, súpera), réclama, and the noun meno with the false plural reading it gave menos and ménos.
- 2.20.0 (261121): the FreeLing 4.2 source tree is `third-party/FreeLing-4.2/` in the product folder (FreeLing 4.2 is installed inside the product folder (decided 261121)); `--source-tree` and `--build-tree` default to it, found from the project root. The data built is unchanged.
- 2.19.0 (261121): the build is part of the product folder: it reads the Chilean lists from `data/grammatical-lists/freeling-cl/`, the decisions from `data/escl-sources/`, the person-name parts from `data/people-names-list/`, the changes to FreeLing's code from `third-party/patches/`, the privacy file from `config/` and the explode scripts from its own folder, and writes the release to `dist/FreeLing-es_CL-2027/`, earlier builds going to `dist/deprecated/` (moved into the product folder `derived-software/FreeLing_es-CL_2027/` (decided 261121)). `--out` defaults to that folder, found from the project root. The release's `.gitignore` names `corpora` so that it holds whether `corpora` is a folder or a link. The data built is unchanged.
- 2.18.0 (261119): the two new changes to FreeLing's code are copied into the release (`freeling-4.2-tag-probabilities.patch`, `freeling-4.2-ambiguous-multiwords.patch` and their READMEs). An interjection that was RARE in an earlier round and is not in the newest (bueno, listo, exacto, vamos, ok, okey, okay; decided 261119) loses the line an earlier build wrote for it in `probabilitats.dat`, with the interjection at 0: FreeLing's own line comes back, or none (until now the line stayed, so the word stayed RARE whatever the newest round said). The flag of a multiword may be A with a weight (`A:0.9`), in `locutions--*.tsv` and in the multiword file a build starts from.
- 2.17.0 (261119): the release folder is `FreeLing-es_CL-2027` (was `FreeLing_es-CL_2027`, which a build moves to `deprecated/`); the tagging tools (`freeling.py`, `freeling_common.py`, `freeling_ud.py`, `freeling_perkins.py`, `freeling_parquet.py`, `freeling_server.py`, `freeling_analyzer.py`, their READMEs, `freeling_comma_multiwords.txt`) are copied into `software/`; `corpora/` is carried over from build to build and `.gitignore` keeps it off GitHub; the new source kind `informal-reading-removals` (the nouns tas and tar out of the informal user map). See "Readings left out of the informal user map" and "The corpus folders".
- 2.16.0 (261119): the configs are written by `freeling_escl_configs.py` (called by the build; copied into the release in place of `the former config writer`): `es-cl.cfg`, `es-cl-informal.cfg`, the new `es-cl-speech.cfg` and `es-cl-19th-century.cfg`, each with the settings the corpora are tagged with and its own user map, and `es-cl-conll-columns.cfg`; the user maps tag the stand-in tokens of the new source `escl-sources/stand-ins.tsv`, copied into the release. Everything 19th-century is named so: the folder `data/es/es-cl/19th-century/` (was `historical/`), `CL.19th-century` (was `CL.historical`), the source kind `19th-century-attested-spellings` (was `historical-attested-spellings`). The linked-folder check runs only when the folder exists; the explode scripts are taken from this script's folder when `--explode-dir` lacks them; a private term is matched as a whole word where it begins or ends with a letter (a corpus name no longer matches the Chilean verb whose letters contain it). `freeling_escl_sources_move.py` is retired and no longer copied into the release. See "The configs and user maps".
- 2.15.0 (261118): compound analysis off in every config of the release (`CompoundAnalysis=no`, `CompoundFile` commented out): `es-cl.cfg` and `es-cl-informal.cfg` now as `es-cl-19th-century.cfg` was. Decided by the user after the compound module was found to have built 458 false lemmas in a speech corpus. The data are unchanged. See "Compound analysis off in every config".
- 2.14.0 (261116): a third dictionary, the informal one (`data/es/es-cl/informal/dicc.src`, the default with `CL.reduced-forms`, and its config `data/config/es-cl-informal.cfg`): the reduced forms are for informal writing only (decided 261116), and the default and 19th-century dictionaries no longer have them; no reduced form at all of a word stressed before its ending (no sábao, hígao); `reading-removals` apply to the reduced forms; the informal user map lists the informal dictionary's readings. See "The reduced forms".
- 2.13.0 (261116): the reduced forms of -ido, -ida, -idos and -idas (-ío, -ía, -íos, -ías: he comío, el marío, decided 261116), and of the participles of haber and ser (ha sío); no accented reduced form of a word stressed before its ending (2.12.0 gave décá, nómá, tríá: 48 words); no participle given to an imperfect, a conditional or a 3rd person present (comía, quería, podría, dá). See "The reduced forms".
- 2.12.0 (261116): the reduced forms, -ao, -á, -aos and -ás, of every -ado, -ada, -ados and -adas word with a participle, adjective or noun reading (`CL.reduced-forms`, decided 261116; see "The reduced forms"); R8 adds the voseo reading beside the preterite of the same verb (salí, comí); the reduced forms give no 19th-century spellings.
- 2.11.0 (261116): `data/es/afixos.dat`, FreeLing's affix rules (a new sha256-checked input) with the clitic rules restricted (decided 261116): te only after an infinitive, a gerund or a tú imperative, os only after an infinitive or a gerund (or by FreeLing's vosotros rules), never te twice or te with os. See "The attached pronouns".
- 2.10.0 (261116): `form-probabilities` counts a form's readings by lemma and tag, as FreeLing does: a short tag held by two readings (ve as ir and as ver, both VMM02S0) has its share split between them, as this README already said (until now a tag was counted once, whatever its lemmas); the lemma preference reír over reir (decided 261116: FreeLing 4.2 also reads reírme as re + ír, lemma reir, with the same tag and probability, and ordered the two alphabetically); the known-roots change of FreeLing's affix analysis (`freeling-4.2-known-roots.patch` and its README) copied into `software/patches/` with the name-class change.
- 2.9.0 (261115): three new kinds of source, `reading-removals` (a reading taken out of both dictionaries), `form-probabilities` (the shares of a word's or a multiword's readings) and `informal-readings` (readings for informal writing only, written to the new `data/es/es-cl/usermap-informal.dat`); `locutions` rows may hold several tags, with one lemma or one per tag; `dictionary-words` rows are kept per form, lemma and tag, refuse a form with a space, and accept contractions (`para+el SP+DA`); a reading decided with its exact tag is exempt from the 261110b exemption and from the standard lemmas; a `locution-removals` key already removed is logged instead of refusing the build; `<DictionaryClasses>` holds every proper-noun tag of the dictionary (NPMSSP0, NPFSSP0, NPMSO00, NPFSO00, NPMS000 and NPMP000 were missing, so a capitalized Kike or Codelco came out as NP00000), and a dictionary with a proper-noun tag outside the list refuses the build. See "Reading removals, probabilities and readings for informal writing" and "Dictionary words and hand edits".

- 2.8.1 (261113): FreeLing 4.2's `es-cl.cfg` is carried in the script (`ES_CL_CFG_TEXT`, checked against its sha256) instead of read from the source tree: your corpus tags only with `the former base config` and the configs written from it, and every other es-cl config on the machine is retired (decided 261113). The release is otherwise unchanged.

- 2.8.0 (261113): the 19th-century dictionary (decided 261112, 261113): the 19th-century Chilean spellings, the attested old-accent spellings, five words decided one by one, its own probabilities (Bello readings of existing words nearly impossible, vosotros over voseo) and multiwords, and the two configs `data/config/es-cl.cfg` and `es-cl-19th-century.cfg` (FreeLing's `data/config/es-cl.cfg` is a new sha256-checked input); `CL.old-accents` in both dictionaries; `CL.misspellings` becomes `CL.common-misspellings`, with every accented form written without its accents; two new kinds of source, `dictionary-words` and `19th-century-attested-spellings`, and the hand-edit file `dictionary-hand-edits.tsv`; the packaging's new `install-data.sh` (the Chilean data into an installed FreeLing, for the Linux packages and the macOS tarballs) is copied with the other packaging scripts. See "The 19th-century dictionary", "The accented one-syllable forms and the common misspellings" and "Dictionary words and hand edits".

- 2.7.0 (261112): FreeLing's general Spanish multiwords (`data/es/locucions.dat`, sha256-checked) are merged into the Chilean multiword file, the Chilean entry winning for a key in both; until now every general multiword was split in every one of your corpora, as the configs name the Chilean file only. tal y cual gets `PI0CS00` (FreeLing's file has `Fs`). Two new kinds of source, `locutions` and `locution-removals`, which need no link in the speech corpus's folder. Every kind is now read per expression across all its rounds, later rounds winning (interjections, interjection removals and lemma standardization read only their newest file until now); `dictionary-additions-all-rounds-standardized` stays newest only, being itself every round merged. See "The multiwords".
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
  `derived-software/FreeLing_es-CL_2027/data/escl-sources/` (decided 261112: one
  copy, linked from the decisions folder of a speech corpus). The default was the
  folder `working/speech-corpus-spelling--261101/decisions`, which no longer
  exists since a speech corpus records moved to the stages' `_processing-records`
  (261111), so the build refused. The links are checked both ways before
  anything else (`--linked-folder`), and the release carries the sources it
  was built from, in `sources/escl-sources/`, and `freeling_escl_sources_move.py`
  with the rest of its software.
- 2.3.0 (261110): a form may have one sentence-start rule for written texts
  (`np.dat`) and another for speech (`np-speech.dat`) (decided 261110g:
  Pinto the surname or the verb at the start of a written sentence, the
  surname only at the start of a speech corpus line); two rows of one file for
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
  19th-century; the spelling decisions (additions with paradigms,
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
