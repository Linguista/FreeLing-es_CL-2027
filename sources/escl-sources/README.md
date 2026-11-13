# escl-sources

The decision files from which FreeLing es-CL 2027, the Chilean Spanish data
for FreeLing 4.2, is built, besides FreeLing's own Spanish files and the
CSLD grammatical lists. `freeling_escl_build.py` reads every file here on
every build, so these files are needed for every new version of the data.

They come from the spelling review of COSCACH (the CSLD spoken corpus) and
from the decisions on names, multiwords and dictionary words made while tagging it and building the 19th-century dictionary, in rounds: the part of a
file name after `--` is its round (a date, YYMMDD, with a letter for a
second round on the same day). Every round is read, and a later round wins for the same expression (the same form, or the same lemma in `lemma-standardization`); something is taken out only by a removals file, never by leaving it out of a later round. `dictionary-additions-all-rounds-standardized` is the exception: it is itself every round merged, so only the newest is read.

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
| `locutions` | form, lemma, tag, flag | a multiword expression joined into one token with this lemma and EAGLES tag; flag I always joined, A ambiguous (the tagger decides); a later round wins for the same multiword |
| `locution-removals` | form, why | a multiword removed: its words are tagged separately |
| `dictionary-words` | form, lemma, category, tag, notes | a word to add: with a tag, exactly that reading; without one, the category's readings (the other number and gender of a noun or an adjective, the whole paradigm of a new verb); a later round wins for the same form and lemma |
| `historical-attested-spellings` | spelling, source | a spelling attested in historical texts (the CSLD Historic-Word-List, and the pre-reform spellings taken out of its contemporary word list on 260811); the 19th-century dictionary gives it the readings of the one modern word with the same letters, when it has an extra or a moved accent |
| `verb-form-readings` | form, lemma, entry, tags, alone, reading in words | the readings of a verb form the build could not tag by itself |
| `fixed-name-classes` | name, class, source, ruling | a name that always has this class (place, person, organization, other), or none: not fixed |
| `person-name-removals` | entry, list, ruling | an entry removed from FreeLing's list of whole person names |
| `place-only-forms` | form, ruling | a form that is a place and nothing else |
| `sentence-start-classes` | form, reading, keep own readings, share, files, ruling | the reading a capitalized form gets at the start of a sentence, for written texts, speech or both |
| `name-class-shares` | name, class, share, ruling | the classes a name may take, with their shares (percent) |

One file has no round: `dictionary-hand-edits.tsv`, words added to the dictionary by hand, one reading per line (form, lemma, tag), edited in place; its comment lines (`#`) say what goes in it and how. Every line is added at every build.

The full meaning of each column, and what the build does with every row,
are in `freeling_escl_build_README.md` (in `software/` of the release) and
in the release's `DECISIONS.tsv`, which has one row per decision row read.

The person names among the additions are the names that occur in COSCACH,
as written by its transcribers; the names of speakers and of anyone they
mentioned in a way that could identify them were redacted from the corpus
before review.
