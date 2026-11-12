# escl-sources

The decision files from which FreeLing es-CL 2027, the Chilean Spanish data
for FreeLing 4.2, is built, besides FreeLing's own Spanish files and the
CSLD grammatical lists. `freeling_escl_build.py` reads every file here on
every build, so these files are needed for every new version of the data.

They come from the spelling review of COSCACH (the CSLD spoken corpus) and
from the decisions on names made while tagging it, in rounds: the part of a
file name after `--` is its round (a date, YYMMDD, with a letter for a
second round on the same day). Later rounds win where they disagree.

Every file is UTF-8 NFC, tab-separated, with one header line. None quotes
the interviews: they are lists of words, forms and names, each with what
was decided about it.

| Kind | Columns | A row means |
|---|---|---|
| `dictionary-additions` | form, lemma, category, sheet, count | a word to add, with its lemma and category, as decided in that round (sheet: the review sheet it came from; count: its tokens in COSCACH) |
| `dictionary-additions-all-rounds-standardized` | form, lemma, category, round, lemma as entered | every round's additions merged, with the standard lemma; the build reads only the newest of these, which must be at least as new as the newest round of additions |
| `dictionary-addition-removals` | form, lemma, category, round removed, why | an addition withdrawn |
| `dictionary-variants` | form, standard form, sheet, count | a form kept in the text that gets the readings of its standard form (haiga with haya) |
| `text-corrections` | form, correction, how, sheet, count | a misspelling corrected in the text: replace, split (the correction has a space), or join with the word before |
| `text-correction-removals` | form, correction, round removed, why | a correction withdrawn |
| `correction-lemmas` | form, correction, lemma, category, sheet, count | the lemma and category of a corrected form, so that the misspelling is read as its correction |
| `all-corpora-replacements` | form, replacement, how, corpora, COSCACH 040 tokens | a replacement made in every CSLD corpus |
| `lemma-standardization` | lemma, standard lemma, sheet, group | the one lemma used for the spellings of a word |
| `interjections` | form, lemma, probability, multiword, interjection in FreeLing es-CL 2027 now, sheet | an interjection or discourse marker, with its lemma; RARE ones are seldom chosen; multiword ones go to the multiword list |
| `interjection-removals` | form, why | an interjection reading removed |
| `verb-form-readings` | form, lemma, entry, tags, alone, reading in words | the readings of a verb form the build could not tag by itself |
| `fixed-name-classes` | name, class, source, ruling | a name that always has this class (place, person, organization, other), or none: not fixed |
| `person-name-removals` | entry, list, ruling | an entry removed from FreeLing's list of whole person names |
| `place-only-forms` | form, ruling | a form that is a place and nothing else |
| `sentence-start-classes` | form, reading, keep own readings, share, files, ruling | the reading a capitalized form gets at the start of a sentence, for written texts, speech or both |
| `name-class-shares` | name, class, share, ruling | the classes a name may take, with their shares (percent) |

The full meaning of each column, and what the build does with every row,
are in `freeling_escl_build_README.md` (in `software/` of the release) and
in the release's `DECISIONS.tsv`, which has one row per decision row read.

The person names among the additions are the names that occur in COSCACH,
as written by its transcribers; the names of speakers and of anyone they
mentioned in a way that could identify them were redacted from the corpus
before review.
