# freeling-4.2-ambiguous-multiwords_README.md

Documents `freeling-4.2-ambiguous-multiwords.patch`, a change to FreeLing 4.2 made for FreeLing es-CL 2027 (decided 261119): multiwords marked ambiguous in the multiword file are decided by the tagger, as the file format promises. License: GNU Affero General Public License, version 3 or later, as FreeLing itself.

| File | What it is |
|---|---|
| `freeling-4.2-ambiguous-multiwords.patch` | the change, as a unified diff against FreeLing 4.2 with `freeling-4.2-tag-probabilities.patch` applied |
| `freeling-4.2-ambiguous-multiwords_README.md` | this file |

"Before" is the file with `freeling-4.2-tag-probabilities.patch` applied (for `locutions.h`, `locutions.cc` and `probabilities.cc`, which that patch does not touch, FreeLing 4.2's own file).

| File | Before (sha256) | With the change (sha256) |
|---|---|---|
| `src/include/freeling/morfo/hmm_tagger.h` | `10fbab5708e37ef00100ca260798ab02ee4735d14f7680f648ea2bc3ee748c43` | `223b224c5f20bd9b9387a6d1b165ab386bc41a7da806deacd030892a8bdb75e2` |
| `src/include/freeling/morfo/language.h` | `b7967cf30bb9eb623fb87e7ef2212138824fe3bbc75d37ceee7b05169316a07a` | `c4f4233b9eb74c59772108829906b90c7934e710604243ce86f19aae460cb269` |
| `src/include/freeling/morfo/locutions.h` | `e436437c78d493f24069adb1a657e253150a721468cb8ff36d1266cc3cab196c` | `547da73c035100344842967cfef639f909b10c8f145c733558a14bad7ca5e339` |
| `src/libfreeling/hmm_tagger.cc` | `bff13efc5a12ed7c3f19d0af98f5831b134176e666afaef3d335c75a1371a37e` | `784e9b9106c77fa53841ac004b22f8e8ddefd14cf04891ab37f85ba1c7f45c03` |
| `src/libfreeling/language.cc` | `17521b2f47ad8786281d49b6a550e2143221c7927b6889a70bd0026d1bba9b35` | `8733ac79e99a0042b5c6e263a06d631b9bcb6a9b54f4d227c7c1177e20667d4b` |
| `src/libfreeling/locutions.cc` | `3fff73d9a5d9fcf1c3cedea563bad0fda60eab0a8ab11321d535d4f0bffbd40f` | `0ffa8faefbf5ce14f9a0f63b72780015f25dc2851bfc581ec9901d9f8137a5f1` |
| `src/libfreeling/probabilities.cc` | `7923f95f77ee956ec7f9866d96bbde83bbebf6ece4b018e273446fbe0a9bce92` | `aa0ebeb97a329cf9dd7ad9b26a698cff287f51144fc65ce7f720b98edb5177ab` |

The patch itself: `7aac61cb5290d29f3ab2bdd0531fbabd8be99acd8f03dbda36aad7f2b2b624c0`.

## Contents

1. The defect in FreeLing 4.2
2. What it changes
3. How the tagger decides
4. The weight: A:0.9
5. How it works in the code
6. Applying, building and installing
7. Verifying
8. Measured effect, and its limits
9. What it does not change
10. Changelog

## 1. The defect in FreeLing 4.2

Every line of FreeLing's multiword file (`locucions.dat`) ends in a flag: `I`, the words are always joined into one token, or `A`, ambiguous: the words may be the multiword or just words that happen to stand together.

```text
o_sea o_sea CC I
es_que es_que CS A
```

FreeLing 4.2 reads the flag, stores it in the token (`word::set_ambiguous_mw`), and never looks at it again: nothing in the library calls `word::is_ambiguous_mw`. So `A` does nothing. Every multiword in the file is joined every time its words meet, whatever the sentence. All 1,573 entries of FreeLing's own Spanish file are `I`, so the defect does not show until a user marks an entry `A` and nothing happens.

What that costs, with entries a user would reasonably mark `A`:

| Text | FreeLing 4.2, whatever the flag | What the words are |
|---|---|---|
| Voy **a ver** la película. | `a_ver`, an interjection | a (preposition) + ver (verb) |
| Lo que pasa **es que** no tengo plata. | `es_que`, a conjunction | es (verb ser) + que (conjunction) |
| Ya sea en la casa **o sea** en el colegio. | `o_sea`, a conjunction | o (conjunction) + sea (verb ser) |
| **Puede ser** hoy. | `puede_ser` | puede (verb) + ser (verb) |

The tokens are wrong, and so are the lemmas, the tags, the parse and every count made from them (a verb ser that never appears, a marker counted where there is none).

## 2. What it changes

A multiword marked `A` is joined only when the tagger finds that the sentence reads better with it than with its words apart. A multiword marked `I` is joined as before. A file with no `A` entry gives exactly the output it gave before.

```text
Ya sea en la casa o sea en el colegio. -> ... casa o CC sea ser VSSP1S0 en ...
O sea, yo creo que no. -> O_sea o_sea CC , yo ...
Lo que pasa es que no tengo plata. -> ... pasa es ser VSIP3S0 que que CS no ...
```

(Real output, with `o_sea` and `es_que` marked `A` in FreeLing's own Spanish multiword file.) The words taken apart keep their own character positions, and the dependency parser parses them as any other words.

## 3. How the tagger decides

For each ambiguous multiword in a sentence, left to right, the HMM tagger tags the sentence twice: with the multiword as one token, and with the words it was made from in its place (with all their dictionary readings). Each way has a best sequence of tags, and each best sequence has a score: the probabilities of its transitions, and for each token the probability of its tag given the word divided by the probability of the tag (what the word tells about its tag). The probability of the word itself is left out: it is the same whatever the tags, and it would otherwise decide alone between one long token and several short ones. The way with the higher score is kept.

A multiword is taken apart only if every word it was made from has a reading. With several ambiguous multiwords in a sentence, each is decided with the ones before it already decided and the ones after it still joined.

The decision rests on tags alone: the tagger knows that a conjunction followed by a subjunctive verb fits after a noun, and cannot know that a "sea" a few words earlier makes "o sea" the second half of "ya sea ... o sea". Section 8 shows what that is worth.

## 4. The weight: A:0.9

New with this change: the flag may carry a weight, the confidence that the words are the multiword when nothing else is known.

```text
o_sea o_sea CC A:0.9
es_que es_que CS A
```

`A` alone is `A:0.5`: no preference, the scores decide. With `A:0.9`, the joined reading starts with odds of 9 to 1: the words are taken apart only when their score beats the multiword's by that much. `A:0.1` favours taking them apart. The weight must be above 0 and below 1; anything else stops FreeLing with an error naming the entry.

The weight is the lever for tuning an entry on judged examples of a corpus. A file with weights must not be read by a FreeLing without this change: FreeLing 4.2 takes any flag that is not exactly `A` for `I`, so the entry is simply always joined, as before.

## 5. How it works in the code

- `src/libfreeling/locutions.cc`, `src/include/freeling/morfo/locutions.h`: the flag `A:<weight>` is read; the token gets the weight (`word::set_mw_prob`) with the flag.
- `src/include/freeling/morfo/language.h`, `src/libfreeling/language.cc`: the class `word` has a new member, `mw_prob` (0.5 by default), with `get_mw_prob()` and `set_mw_prob()`, and a second `get_words_mw()` that lets the words of a multiword be annotated.
- `src/libfreeling/probabilities.cc`: the words of an ambiguous multiword get their probabilities too, as the parts of a contraction already did, so that the tagger can tag them.
- `src/libfreeling/hmm_tagger.cc`, `src/include/freeling/morfo/hmm_tagger.h`: `annotate` first calls the new `resolve_ambiguous_mw`, which makes the two taggings and compares them with the new `SegmentationScore_log`, then tags the sentence as it stands.

The relax tagger (`Tagger=relax`) does not decide: with it an ambiguous multiword stays joined, as before.

A sentence with an ambiguous multiword is tagged up to three times instead of once; the others cost nothing more.

## 6. Applying, building and installing

From the top of an unpacked `FreeLing-src-4.2.tar.gz`, after `freeling-4.2-tag-probabilities.patch`, on which it builds:

```bash
patch -p1 --forward --batch < freeling-4.2-ambiguous-multiwords.patch
```

The release's `packaging/patch-freeling.sh` applies both in order with FreeLing es-CL 2027's other changes, checking every file by sha256 before and after. As with the tag-probabilities change, the class `word` grows, so every program built against FreeLing's headers is built again with the library.

## 7. Verifying

```bash
echo "Voy a ver la película." | analyze -f es-cl.cfg --outlv tagged --output freeling --nonec --sense none
```

With the change (`a_ver` is marked `A` in FreeLing es-CL 2027): the lines `a a SP` and `ver ver VMN0000`. Without it: one line, `a_ver a_ver I`. `packaging/test-freeling.sh` checks for the two lines, and that "A ver, dime qué pasó." keeps `A_ver a_ver I`.

## 8. Measured effect, and its limits

Tested 261119 with FreeLing 4.2 built with the name-class and the tag-probabilities changes, on FreeLing's own Spanish data, with `o_sea` and `es_que` marked `A` and no weight. These are sentences written for the test, not a sample of a corpus:

| Multiword | Decided as a reader would | Wrong |
|---|---|---|
| es que | 6 of 8 | "Es que no sé." and "Pero es que no puedo." taken apart |
| o sea | 5 of 9 | "No sé, o sea, es difícil." taken apart; "Quiero que sea feliz o sea rico.", "Puede ser hoy o sea mañana." and "No importa que sea grande o sea chico." kept joined |

With FreeLing es-CL 2027's own data (`es-cl-speech.cfg`, built by `freeling_escl_build.py` 2.18.0), also on sentences written for the test:

| Multiword, as marked in FreeLing es-CL 2027 | Decided as a reader would | Wrong |
|---|---|---|
| a ver (A) | 3 of 3 | |
| puede ser (A) | 2 of 2 | |
| la verdad (A) | 2 of 2 | |
| está bien (A) | 2 of 2 | |
| por eso (A) | 1 of 2 | "Por eso no fui." taken apart |
| y todo (A) | 1 of 2 | "Y todo el mundo lo sabe." kept joined |
| al final (A) | 0 of 1 | "Al final no fuimos." taken apart |
| es que (A) | 6 of 10 with no weight; 8 of 10 with `A:0.8`; 6 of 10 with `A:0.9` | the marker at the start of an utterance taken apart ("Es que no sé."), or the verb and conjunction kept joined |
| o sea (tested as A; it is I in the release) | 4 of 8, with no weight and with every weight from 0.7 to 0.98 | no better than chance |

So the change makes the flag work, and the tagger's judgment is good where the multiword and its words apart are different kinds of thing (a ver, an interjection, against a preposition and a verb; puede ser; está bien; la verdad), and weak where they are not (o sea, whose two readings differ by a word seen earlier in the sentence, which a tagger that sees only neighbouring tags cannot use; es que at the start of an utterance). For that reason `o_sea` stays `I` in FreeLing es-CL 2027. Before relying on an `A` entry, judge a sample of its occurrences in the corpus at hand, and set its weight, or its flag, from that.

With no `A` entry in the multiword file, the output of the test sentences is byte for byte what it was before the change.

## 9. What it does not change

- Entries marked `I`, and files without `A` entries.
- How a multiword is recognized: the same words, in the same order, as before. Only whether a recognized ambiguous one is kept.
- The relax tagger.

## 10. Changelog

- 261119: first version, for FreeLing es-CL 2027 (`freeling_escl_build.py` 2.18.0).
