# freeling-4.2-tag-probabilities_README.md

Documents `freeling-4.2-tag-probabilities.patch`, a change to FreeLing 4.2 made for FreeLing es-CL 2027 (decided 261119): two new columns for the CoNLL output, `LEX_PROB` and `TAG_PROB`. License: GNU Affero General Public License, version 3 or later, as FreeLing itself.

| File | What it is |
|---|---|
| `freeling-4.2-tag-probabilities.patch` | the change, as a unified diff against FreeLing 4.2 (`FreeLing-src-4.2.tar.gz` of `https://github.com/TALP-UPC/FreeLing/releases/tag/4.2`, the same files as the tag 4.2) |
| `freeling-4.2-tag-probabilities_README.md` | this file |

| File | Before (sha256) | With the change (sha256) |
|---|---|---|
| `src/include/freeling/morfo/hmm_tagger.h` | `3e920ac0cf914aaf0a763c6ad6e9c18efa27c6a22ba9e0c582f1f087f8560695` | `10fbab5708e37ef00100ca260798ab02ee4735d14f7680f648ea2bc3ee748c43` |
| `src/include/freeling/morfo/language.h` | `a98bc53ffcfa5cef0f332ecf600567adb12296c90e78d7aed149326887e7e3c2` | `b7967cf30bb9eb623fb87e7ef2212138824fe3bbc75d37ceee7b05169316a07a` |
| `src/include/freeling/output/conll_handler.h` | `1adca7e4a5a70328d9d96b14ae99f137d584701bb69cefbba3b9a7f16551ab12` | `2714c1e553274b7c967c12f538450aa413f20a2c467821d6b7fda38ef65a7d6a` |
| `src/libfreeling/hmm_tagger.cc` | `c44940523019c65f76c6e031f127ea2d77ce8e92840860935f9bfc522265ccff` | `bff13efc5a12ed7c3f19d0af98f5831b134176e666afaef3d335c75a1371a37e` |
| `src/libfreeling/language.cc` | `0df9c9db2152627cc3acf1bbdbfbd9d8e1a36799ee0597a663520fd6afe5310f` | `17521b2f47ad8786281d49b6a550e2143221c7927b6889a70bd0026d1bba9b35` |
| `src/libfreeling/output/conll_handler.cc` | `fa599770eda1a36b56edbb995985fe6c4717725c36e6d54322d7840cd15b71bf` | `9333892e4868c55b984452f9f745b9b58c06fcb8174e47eeaab31057d8aec32e` |
| `src/libfreeling/output/input_conll.cc` | `4bbe7ee6c0a81f03cad338c461ae3164d468e5f46fe634ea49316c859df79680` | `2065b9dcf2285944e3770bad1daf2e9b477c1a7678ce5e7050ef3e5eb38f7bed` |
| `src/libfreeling/output/output_conll.cc` | `06e654f6d7c8582e7a3603bc378f9db8a11c9c03d46e9d0ad785d8a4a9395002` | `985a429a175ef470e1eae87055452aa45c8a2f6f137eb7f6f06ef5084d2a5e37` |
| `src/libfreeling/tagger.cc` | `659ac7e2ac65e43ce4763d314726e6dcfdaffa74fb425a98f4156c0f3b7d6d44` | `ce27745a27d280f2c6995397f7d308963d45c11e9b1ae1a28675d343747e753d` |

The patch itself: `d4f1c0a8fee20743f06c9adc62728477d06c7a4c15937c0834775352e7f29897`.

## Contents

1. Purpose
2. The two columns
3. How TAG_PROB is computed
4. How it works in the code
5. Applying, building and installing
6. Using the columns
7. Verifying
8. What it does not change
9. Changelog

## 1. Purpose

FreeLing's tagger chooses one tag for each word and says nothing about how sure it is. The only number FreeLing 4.2 can print for a word is the probability its `probabilities` module gave the chosen reading before tagging: how often that word has that reading in general, whatever the sentence. Only FreeLing's own output format prints it (`--output freeling`), and only at the tagging level: the CoNLL writer has no column for it, and a parsed sentence is printed as a tree without it.

That number does not say how sure the tagger was. In "Bueno, yo creo que es bueno" FreeLing's Spanish data gives the first word as an interjection a probability of 0.175, because the word is mostly an adjective; the tagger is all but certain that here it is an interjection. A corpus builder who wants to find the words most likely to be mistagged needs the second number, and FreeLing did not compute it.

This change adds both numbers as CoNLL columns, available at every output level.

## 2. The two columns

| Column | What it is | Range |
|---|---|---|
| `LEX_PROB` | the probability of the selected reading among the readings of the word, out of context: what the `probabilities` module assigned (from `probabilitats.dat` and its smoothing). It is the number FreeLing's own format already printed. | 0 to 1 |
| `TAG_PROB` | the probability the tagger gives the selected tag given the whole sentence: of all the tag sequences the sentence may have, the share of probability held by those in which this word has this tag | 0 to 1; `-` when the tagger did not compute it |

A real run with FreeLing 4.2's own Spanish data (`es.cfg`), columns `ID FORM LEMMA TAG LEX_PROB TAG_PROB`:

```text
1 Bueno bueno I 0.175325 0.999095
2 , , Fc 1.000000 1.000000
3 yo yo PP1CSN0 1.000000 1.000000
4 creo creer VMIP1S0 0.500000 1.000000
5 que que CS 0.449861 0.949196
6 es ser VSIP3S0 1.000000 1.000000
7 bueno bueno AQ0MS00 0.824675 0.995829
8 . . Fp 1.000000 1.000000
```

How to read them:

- A low `TAG_PROB` marks a word the tagger hesitated over: its other tags fit the sentence nearly as well.
- A low `LEX_PROB` with a high `TAG_PROB` marks a word used in one of its rarer readings, which the context made clear (the first Bueno above).
- A word with one reading in the dictionary has both at 1, right or wrong: neither number can show a reading the dictionary lacks, or one that `probabilitats.dat` makes nearly impossible.
- `TAG_PROB` is the model's own estimate, not a measured accuracy. Whether words below some value are really wrong more often has to be measured on judged examples of the corpus at hand.

## 3. How TAG_PROB is computed

FreeLing's HMM tagger scores a sequence of tags with three kinds of probability: of the first state, of each transition between states (a state is the pair of the previous tag and the current one), and of each word given its state. To choose the tags it finds the single best sequence (the Viterbi algorithm).

`TAG_PROB` uses the same states and the same three probabilities, with the forward-backward algorithm: for each word and each of its states, the summed probability of every sequence that passes through that state, divided by the summed probability of all sequences. The probability of a tag is the sum over the states that end in it. Nothing is trained or estimated anew, and no data file changes.

The tags are FreeLing's short tags, the ones the tagger works with (2 letters for nouns and adjectives, 3 for verbs, 1 for interjections, as `tagset.dat` defines them): `TAG_PROB` is the probability of the short tag of the selected reading. When two readings of a word share a short tag, the tagger picks between them by `LEX_PROB`.

The value is computed before the tagger selects anything, over every reading the word had. A sentence in which no sequence has a probability above zero (every path forbidden) gets `-`.

## 4. How it works in the code

- `src/include/freeling/morfo/language.h`, `src/libfreeling/language.cc`: the class `word` has a new member, `tag_prob` (-1: not computed), with `get_tag_prob()` and `set_tag_prob()`; it is copied with the word.
- `src/libfreeling/hmm_tagger.cc`, `src/include/freeling/morfo/hmm_tagger.h`: the body of `annotate` is now `tag_sentence(sentence, bool)`; `annotate` calls it. With the flag, it calls the new `TagPosteriors` (forward-backward, in log space, over the states `FindStates` gives) before selecting, and stores each word's value after selecting.
- `src/libfreeling/tagger.cc`: a word the tagger splits after tagging (a contraction kept whole until then) passes its value to its parts.
- `src/include/freeling/output/conll_handler.h`, `src/libfreeling/output/conll_handler.cc`: the two column names.
- `src/libfreeling/output/output_conll.cc`: writes them. `src/libfreeling/output/input_conll.cc`: reads them back (a CoNLL file given as input).

The relax tagger (`Tagger=relax`) does not compute `TAG_PROB`: the column is `-` with it.

Because `word` has a new member, every program built against FreeLing's headers must be built again with the library (`analyzer`, `threaded_analyzer`, FreeLing's API bindings); a program built before this change must not be run with a library built after it.

## 5. Applying, building and installing

From the top of an unpacked `FreeLing-src-4.2.tar.gz`:

```bash
patch -p1 --forward --batch < freeling-4.2-tag-probabilities.patch
```

It touches no file the name-class and known-roots changes touch, and applies before or after them. `freeling-4.2-ambiguous-multiwords.patch` builds on it and applies after it. The release's `packaging/patch-freeling.sh` applies all of them in order, checking every file by sha256 before and after; `packaging/build-freeling.sh` and the GitHub workflow `packages.yml` build and install FreeLing with them.

## 6. Using the columns

The CoNLL writer prints the columns its columns file names (`--output conll --oconll FILE`, or `OutputConllConfig` in a config). Add the names where they are wanted:

```text
<Columns>
ID SPAN_BEGIN SPAN_END FORM LEMMA TAG LEX_PROB TAG_PROB SENSE ALL_SENSES DEPHEAD DEPREL
</Columns>
```

Since 261120 the columns file of the release, `es-cl-conll-columns.cfg`, names them after its ten earlier columns (`ID SPAN_BEGIN SPAN_END FORM LEMMA TAG SENSE ALL_SENSES DEPHEAD DEPREL LEX_PROB TAG_PROB`), so every text tagged with the release's configs has them; the ten earlier columns are unchanged.

## 7. Verifying

```bash
printf '<Columns>\nID FORM LEMMA TAG LEX_PROB TAG_PROB\n</Columns>\n' > columns.cfg
```

```bash
echo "Bueno, yo creo que es bueno." | analyze -f es-cl.cfg --outlv tagged --output conll --oconll columns.cfg --nonec --sense none
```

Every token line has six fields, the last two numbers from 0 to 1. `packaging/test-freeling.sh` checks exactly that.

Tested 261119 with FreeLing 4.2 built with the name-class change, with and without this change, on FreeLing's own Spanish data: the tags, lemmas and tokens of the test sentences are the same with and without it (the output in FreeLing's own format is byte for byte the same), at the tagging level and with the LSTM dependency parser. The patched source builds with GCC 13 as part of the whole library.

## 8. What it does not change

- Which tag is chosen: the Viterbi search is as before. The probabilities are computed beside it.
- Any data file or option.
- FreeLing's own output format, and every other format.

## 9. Changelog

- 261119: first version, for FreeLing es-CL 2027 (`freeling_escl_build.py` 2.18.0).
