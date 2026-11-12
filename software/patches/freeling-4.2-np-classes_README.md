# freeling-4.2-np-classes_README.md

Documents `freeling-4.2-np-classes.patch`, a change to the name recognizer
(`np`) and the name classifier (`nec`) of FreeLing 4.2, made for FreeLing
es-CL 2027 (261110). License: GNU Affero General Public License, version 3
or later, as FreeLing itself.

| File | What it is |
|---|---|
| `freeling-4.2-np-classes.patch` | the change, as a unified diff against the tag 4.2 of FreeLing (`https://github.com/TALP-UPC/FreeLing`) |
| `np.cc` | `src/libfreeling/np.cc` of FreeLing 4.2 with the change applied |
| `np.h` | `src/include/freeling/morfo/np.h` of FreeLing 4.2 with the change applied |
| `nec.cc` | `src/libfreeling/nec.cc` of FreeLing 4.2 with the change applied |
| `freeling-4.2-np-classes_README.md` | this file |

| File | FreeLing 4.2 (sha256) | With the change (sha256) |
|---|---|---|
| `src/libfreeling/np.cc` | `2934779917d1041111f9750effb78500a8bfbba9057bfbf43c1cc22cac51a622` | `76d097ac967c502b181836e6e191b2332f87f53deb8de83d65abe4f9e42c4d0e` |
| `src/include/freeling/morfo/np.h` | `f09274b49e0c72f99ced11ff386c0473dec8a692bed1c29c41e3dd5832550f7b` | `0f77cc4869a3fd0aee0db27157b606cd35f3d21a47f8a3688ac8be9722546eb4` |
| `src/libfreeling/nec.cc` | `1e04d9fafb3423d41803030b3b29a5e14cf80e0f2dc18f1b50d458ba07525a5f` | `fc71feb87d40314cffa83b2677151104c6574848526ec04029b0142d5d568a4f` |

The patch itself: `69542743afc056043aefa58483672a5f583b5df37346c8f7af109cb34ecc713d`.

## Contents

1. Purpose
2. What it adds
3. The rule file of the recognizer: four sections
4. The classifier's file: one section
5. Compatibility
6. How it works in the code
7. Applying, building and installing
8. Verifying
9. Examples
10. Measured effect
11. What it does not decide
12. Changelog

## 1. Purpose

FreeLing decides whether a word is a proper name, and which kind, in two
steps:

1. **The name recognizer** (`np`, configured by `np.dat`) decides which
   words are a name. Inside a sentence, a capitalized word becomes a new
   name with the tag "proper noun, unclassified" (`NP00000`), and every
   reading the dictionary gave it is dropped. At the start of a sentence,
   where every word is capitalized, a word becomes a name only if the
   dictionary also knows it as a common noun or an adjective (or it is on the
   `<Names>` list); its dictionary readings are then kept beside the name
   reading, and the tagger chooses.
2. **The name classifier** (`nec`, an AdaBoost model, configured by
   `nec-ab-poor1.dat`) gives every unclassified name a class: person, place,
   organization or other. Its features include word lists: whole names and
   name parts of each class (`es/nerc/data/gaz*.dat`) and a city list
   (`common/nec/cities.dat`).

Measured on Chilean Spanish (section 10), this goes wrong in ways that no
data file can fix:

- **A place the dictionary knows is still guessed.** Inside a sentence the
  dictionary's place reading is dropped before the classifier runs. España
  was classified as a person 459 times, Antofagasta 193 times, Perú as an
  organization 231 times, although the dictionary has each of them as a
  place. Concepción, a city that is also a given name, was a person 322
  times, Castro (also a surname) 61 times.
- **There is no way to fix a class.** A name whose class is known for
  certain (every commune of Chile is a place; SES is an organization) can
  only be pushed through the classifier's word lists, which are features,
  not rules.
- **At the start of a sentence the recognizer's rule is all or nothing.** A
  word whose only dictionary readings are verbs is never a name there: Arica
  is read as a form of the verb aricar, Tomé as a form of tomar, Catar and
  Irán as the verbs catar and ir. A word that is also a common noun is a
  name or the noun, by the tagger's odds alone. There is no way to say
  "Tomé, at the start of a sentence, is usually the verb, sometimes the
  city", nor "Molina, at the start of a sentence, is a name, never the
  verb molinar".
- **There is no way to weigh a name's classes.** Asunción is a capital and
  a given name; the classifier decides from its features alone, and its
  features said person in "Viajamos a Asunción en enero".

## 2. What it adds

Four optional sections in the recognizer's rule file (`np.dat`), read by
`src/libfreeling/np.cc`:

| Section | Content | Effect |
|---|---|---|
| `<DictionaryClasses>` | proper-noun tags, in order of preference | a one-word name whose dictionary entry has one of these tags keeps that class, with the dictionary's lemma, instead of becoming an unclassified name; the classifier does not see it |
| `<FixedClasses>` | one `form tag` per line | the name always takes this tag, whatever the classifier would say |
| `<ClassesAtSentenceStart>` | `yes` or `no` (default `no`) | whether the two rules above also apply to a one-word name at the start of a sentence that is also a common noun or an adjective |
| `<SentenceStartClasses>` | one `form tag [keep or keep:prefixes]` per line | at the start of a sentence the one-word name gets this reading, whatever the other rules say; with `keep`, its dictionary readings stay beside it, and with `keep:V` only those whose tags begin with V; the tagger chooses |

One optional section in the classifier's file (`nec-ab-poor1.dat`), read
by `src/libfreeling/nec.cc`:

| Section | Content | Effect |
|---|---|---|
| `<ClassShares>` | one `form tag share [tag share ...]` per line | the name takes one of the classes listed, chosen by the classifier's weight for each plus half the log odds of its share |

Nothing in the change is specific to Spanish or to Chile.

## 3. The rule file of the recognizer: four sections

The tags are those of FreeLing's Spanish tagset: `NP00G00` proper noun,
place; `NP00SP0` person; `NP00O00` organization; `NP00V00` other; `NP00000`
unclassified (the classifier decides). A form is written in lower case, the
words of a multiword name joined by `_`. FreeLing writes `del` and `al`
inside a multiword name as `de_el` and `a_el` (Viña del Mar becomes
`Viña_de_el_Mar`), so a fixed name holding one is listed both ways.

### 3.1. DictionaryClasses

```text
<DictionaryClasses>
NP00G00 NP00SP0 NP00O00 NP00V00
</DictionaryClasses>
```

A one-word name whose dictionary analyses include one of these tags takes
the first of them that it has, with the dictionary's lemma, and the
analysis is locked: the tagger keeps it and the classifier does not see it.
Without the section, FreeLing drops the dictionary's proper-noun reading
inside a sentence and asks the classifier.

### 3.2. FixedClasses

```text
<FixedClasses>
concepción NP00G00
viña_del_mar NP00G00
viña_de_el_mar NP00G00
lima NP00G00
pinto NP00SP0
ses NP00O00
judejut NP00V00
dr._house NP00SP0
</FixedClasses>
```

A recognized name (one word or several) whose lowercase form is listed
takes the tag, with its lowercase form as lemma, and the analysis is
locked. This rule is checked before `<DictionaryClasses>`.

### 3.3. ClassesAtSentenceStart

```text
<ClassesAtSentenceStart>
yes
</ClassesAtSentenceStart>
```

With `no` (the default), a one-word name at the start of a sentence that
the dictionary also knows as a common noun or an adjective keeps FreeLing's
own treatment: its dictionary readings and an unclassified name reading,
and the tagger chooses. This suits written texts, where a capital at the
start of a sentence says nothing. With `yes`, the two rules above apply
there too, and a word listed in `<FixedClasses>` is a name at the start of
a sentence whatever its dictionary readings (a verb included). This suits
transcribed speech, where a line is an utterance and a capitalized word at
its start is a name.

### 3.4. SentenceStartClasses

```text
<SentenceStartClasses>
catar NP00G00 keep:V
irán NP00G00 keep:V
molina NP00000
pinto NP00SP0 keep:V
quito NP00G00 keep:V
tomé NP00G00 keep:V
</SentenceStartClasses>
```

At the start of a sentence a one-word name listed here gets the reading
given, and the other rules do not apply to it. The third field:

| Third field | The word's dictionary readings | Result |
|---|---|---|
| none | dropped | the reading given, alone: `molina NP00000` is a name the classifier classifies, never the verb molinar |
| `keep` | all kept beside the reading given | the tagger chooses among them |
| `keep:V` | only those whose tags begin with `V` are kept (several prefixes are separated by commas: `keep:V,N`) | the tagger chooses among them: `tomé NP00G00 keep:V` is the verb tomar or the place, `pinto NP00SP0 keep:V` the verb pintar or the surname |

A word listed here becomes a name candidate at the start of a sentence
whatever its dictionary readings, including a word whose only readings are
verbs, which FreeLing never treats as a name there.

**The odds.** With `keep`, the tagger chooses by the lexical probabilities
of `probabilitats.dat` and the context. FreeLing looks a word up there by
its lowercase form, and counts by short tag (the first characters of a tag:
`VMI`, `AQ`, `NP`). A line for the word gives the proper noun its share:

```text
quito AQ-NP-VMI AQ 47040 NP 112 VMI 1008
tomé NP-VMI NP 111 VMI 1000
```

At the start of a sentence, `Quito` has the readings kept (the verb quitar,
`VMI`) and the place (`NP`): 112 against 1,008, the place 10%. Elsewhere,
`quito` has its dictionary readings only, the adjective and the verb, in
FreeLing's own proportions (47,040 to 1,008); the line's `NP` count is never
used there, because the proper-noun reading exists only at the start of a
sentence. `keep:V` is what makes this possible for Quito: with `keep`, its
rare adjective reading (quito, "exempt") would stay at the start of a
sentence too, with 98% of the word's lexical probability, and the verb would
be left with 2%. FreeLing smooths the counts (Lidstone, lambda 0.1), which
is negligible at these sizes: the morphological analysis gives Quito the
verb 0.8999 and the place 0.1001.

**Which share.** The share was chosen on 15 test sentences in which the
word is the place or the verb (Catar es un país pequeño / Catar el vino
requiere práctica, Tomé tiene playas / Tomé un café, Irán es un país grande
/ Irán con nosotros, Quito es la capital / Quito la tapa ...), written
texts, the place's share set to each value in turn:

| Share of the place | Right | Wrong |
|---|---|---|
| 2% | 13 of 15 | Catar es un país pequeño; Quito es la capital (verbs) |
| 5% | 14 of 15 | Catar es un país pequeño |
| 10% | 15 of 15 | none |
| 20% | 15 of 15 | none |
| 30% | 15 of 15 | none |
| 50% | 14 of 15 | Catar vinos es su trabajo (place) |

FreeLing es-CL 2027 uses 10%: the lowest share that gets every test
sentence right.

Pinto, a surname that is also the verb pintar, is the other way round: the
person is added beside the verb (`pinto NP-VMI NP 429 VMI 1000`, the person
30%). On 16 test sentences, eight with the verb (Pinto la casa todos los
años, Pinto cuadros al óleo, Pinto paisajes, Pinto y dibujo ...) and eight
with the surname (Pinto dijo que no vendría, Pinto la vio ayer, Pinto no
vino ...):

| Share of the person | Right | Wrong |
|---|---|---|
| 5% | 15 of 16 | Pinto la vio ayer (the verb) |
| 10% | 14 of 16 | Pinto la vio ayer (the verb); Pinto y dibujo (the surname) |
| 20%, 30%, 50% | 15 of 16 | Pinto y dibujo (the surname) |
| 70% | 12 of 16 | Pinto cuadros al óleo, Pinto con acuarelas, Pinto paisajes, Pinto y dibujo (the surname) |

"Pinto y dibujo" reads like "Pinto y Molina" up to its last word. FreeLing
es-CL 2027 uses 30%, the middle of the shares that tested best, in written
texts (`np.dat`). In transcribed speech (`np-speech.dat`) its line is
`pinto NP00SP0`, the surname alone: a COSCACH line starts with a
lower-case letter unless its first word is a name, so a speaker's pinto is
written in lower case and stays the verb (decided 261110g). The two files
may give a word different readings; the share in `probabilitats.dat` is
read with both, so it matters only where the word's own readings are
kept.

## 4. The classifier's file: one section

```text
<ClassShares>
asunción NP00G00 0.8000 NP00SP0 0.2000
molina NP00G00 0.7500 NP00SP0 0.2500
san_josé NP00G00 0.8000 NP00SP0 0.2000
san_juan NP00G00 0.8000 NP00SP0 0.2000
sucre NP00G00 0.9500 NP00SP0 0.0500
</ClassShares>
```

A name listed here, when the classifier classifies it, takes one of the
classes listed, never another. For each class the classifier computes its
weight (`pred`, AdaBoost's score, a half log-odds estimate); the change adds
half the log odds of the share:

```text
score(class) = pred(class) + 0.5 * ln(share / (1 - share))
```

and the class with the highest score wins. A share of 0.8 adds +0.69, a
share of 0.2 adds -0.69, so the person class wins only where the
classifier's own evidence for it is clearly stronger. Each share must lie
strictly between 0 and 1; another value is ignored. The shares need not add
up to 1, but FreeLing es-CL 2027 always makes them do.

The section applies only to names the classifier classifies, that is,
unclassified names (`NP00000`). A fixed class (section 3.2) comes first:
a name must not have both.

The same test, before (FreeLing 4.2's classifier, the same lists) and after:

| Sentence | Before | After |
|---|---|---|
| Viajamos a Asunción en enero. | person | place |
| La señora Asunción vive al lado. | person | person |
| Doña Asunción me trajo el pan. | person (Doña_Asunción, one name) | person |
| Viví dos años en San José. | place | place |
| Mi tío San José es carpintero. | place | place |
| Mi amigo San Juan llegó tarde. | place | place |
| El general Sucre ganó la batalla. | place | place |
| Llegamos a Sucre en bus. | place | place |

Where the classifier sees little evidence for a person (Mi tío San José, El
general Sucre), the share keeps the place: the shares weigh the classes,
they do not detect the person. The reverse held too while FreeLing's list
of whole person names had molina: the classifier's own weight for the
person was strong, and Molina's shares (place 0.75, person 0.25) turned
only some places around ("Allá en Molina hace calor" became a place, "Vivo
en Molina" stayed a person). FreeLing es-CL 2027 takes molina off that
list (decided 261110g), and both sentences are places.

## 5. Compatibility

- **A rule file without the four sections works exactly as before.** Every
  rule is skipped when its section is absent or empty.
- **FreeLing without the change reads a rule file with the sections**: its
  configuration reader skips unknown sections in `np.dat` silently.
- **FreeLing without the change stops on a classifier file with
  `<ClassShares>`**: the classifier's configuration reader does not skip an
  unknown section, and FreeLing ends with an error. A classifier file with
  the section must only be installed with a library that has the change.
- Only the basic recognizer (`np`) reads the four sections. FreeLing's
  statistical recognizers (`bioner`, `crf_nerc`, chosen by pointing
  `NPDataFile` at `es/nerc/nerc/*.dat`) are not changed.
- **Binary compatibility.** The classifier (class `nec`) keeps FreeLing
  4.2's size: its shares are kept outside the class, in a table keyed by
  the classifier object. Programs built against FreeLing 4.2's headers that
  create a classifier themselves (`threaded_analyzer` in the sample
  programs) keep working with this library. The recognizer (class `np`)
  grows, but it is only ever created inside the library (by `ner`), so the
  programs `analyze`, `analyzer` and `analyzer_client` need not be rebuilt.
  The header `np.h` is installed with the library for programs built later.

## 6. How it works in the code

### 6.1. `src/include/freeling/morfo/np.h`

Members of class `np`:

```cpp
std::vector<std::wstring> dict_classes;              // <DictionaryClasses>
std::map<std::wstring,std::wstring> fixed_classes;   // <FixedClasses>
bool classes_at_start;                               // <ClassesAtSentenceStart>
struct start_reading {                               // <SentenceStartClasses>
  std::wstring tag;                  // the reading added
  bool keep;                         // whether dictionary readings stay
  std::vector<std::wstring> only;    // if not empty: only readings whose tags begin so
};
std::map<std::wstring,start_reading> start_classes;
```

### 6.2. `src/libfreeling/np.cc`

- **The constructor** registers the four sections with the configuration
  reader and fills the members. `classes_at_start` is false unless the
  section says `yes`. A `<SentenceStartClasses>` line's third field is
  `keep`, or `keep:` followed by tag prefixes separated by commas; anything
  else means the dictionary readings are dropped.
- **`np::ComputeToken`**, at the start of a sentence: a capitalized word is
  a name candidate if it is in `start_classes`, or if `classes_at_start` is
  true and it is in `fixed_classes`, or by FreeLing's own condition (not a
  closed-class word, and a common noun, an adjective or on `<Names>`).
- **`np::SetMultiwordAnalysis`**, where a recognized name gets its
  analysis, in this order:
  1. at the start of a sentence, a one-word name in `start_classes` gets
     its dictionary readings (all, some or none, by the third field) and the
     reading given; nothing else applies, and the analysis is not locked,
     so the tagger chooses;
  2. the rules below apply always inside a sentence, and at the start of a
     sentence to a one-word name that is also a common noun or an adjective
     (FreeLing's `initialNoun` state) only when `classes_at_start` is true;
  3. a name in `fixed_classes` gets the analysis (its lowercase form, the
     fixed tag);
  4. otherwise a one-word name whose dictionary analyses hold one of the
     `dict_classes` tags (the first in the list that it has) gets the
     analysis (the dictionary's lemma, that tag);
  5. otherwise FreeLing goes on as before (an unclassified name).

  In cases 3 and 4 the analysis is locked, so the tagger keeps it, and
  marked as made by the recognizer. The classifier classifies only
  unclassified names, so it does not see these.

### 6.3. `src/libfreeling/nec.cc`

- A static table, `class_shares`, maps each classifier object (its
  address) to its shares: name, then class, then share. A mutex guards it,
  since several analyzers may run in threads.
- **The constructor** registers `<ClassShares>` with the configuration
  reader, reads its lines (a share outside 0 to 1 is ignored), and, if any,
  stores them in the table under the new object.
- **The destructor** removes the object's entry.
- **`nec::analyze`** looks up the object's shares once per sentence. For
  each unclassified name, after FreeLing's own choice (the class with the
  highest weight, or the default class when none is positive), a name
  listed in the shares takes, among its listed classes, the one with the
  highest `pred + 0.5 * ln(share / (1 - share))`.

## 7. Applying, building and installing

FreeLing's build folder holds the compiled objects only while they are
kept; if it was emptied (only `CMakeCache.txt` and `install_manifest.txt`
left, no `src/` folder), the library is built from scratch, which needs the
same configuration as the first build. Here the source tree is
`/home/user/build/FreeLing-4.2` (the tag 4.2, with the fixes it needs to
compile with GCC 16 already made, among them `CMAKE_CXX_STANDARD 17` in
`CMakeLists.txt` and the missing `#include <cmath>` in four files; each
changed file has its `.orig` beside it), installed in `/usr/local`.

Apply the change (or copy `np.cc`, `np.h` and `nec.cc` over the originals,
after checking the originals' sha256 above):

```bash
patch -d /home/user/build/FreeLing-4.2 -p1 --dry-run < /home/user/csld/software/10-Infrastructure/freeling/patches/freeling-4.2-np-classes.patch
patch -d /home/user/build/FreeLing-4.2 -p1 < /home/user/csld/software/10-Infrastructure/freeling/patches/freeling-4.2-np-classes.patch
```

Configure the build folder (the old cache, if any, moved aside first, so
that nothing of a removed build is reused), with the options of the first
build:

```bash
mkdir -p /home/user/build/FreeLing-4.2/build/deprecated
mv -n /home/user/build/FreeLing-4.2/build/CMakeCache.txt /home/user/build/FreeLing-4.2/build/deprecated/CMakeCache.DEPRECATED-261110.txt
cmake -S /home/user/build/FreeLing-4.2 -B /home/user/build/FreeLing-4.2/build -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-Wno-template-body" -DCMAKE_C_FLAGS="-std=gnu17" >| /home/user/build/fl-np-classes-cmake.log 2>&1; echo "exit $?"
tail -3 /home/user/build/fl-np-classes-cmake.log
```

| Option | Why |
|---|---|
| `-DCMAKE_INSTALL_PREFIX=/usr/local` | where FreeLing is installed |
| `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` | CMake 4 no longer accepts the old minimum version FreeLing's build files declare |
| `-DCMAKE_CXX_FLAGS="-Wno-template-body"` | GCC 14 and later reject errors in template bodies that are never instantiated, which FreeLing's code has |
| `-DCMAKE_C_FLAGS="-std=gnu17"` | the bundled C code does not all build under C23, the default C standard since GCC 15 |

Build the library alone (the target `freeling`; it also builds the
libraries it links to, foma, treeler, dynet and crfsuite, which are not
installed again):

```bash
make -C /home/user/build/FreeLing-4.2/build -j16 freeling >| /home/user/build/fl-np-classes-make.log 2>&1; echo "exit $?"
grep -c "error:" /home/user/build/fl-np-classes-make.log
```

Install the library and the header (copy the installed ones aside first,
if they are to be kept):

```bash
sudo cmake -P /home/user/build/FreeLing-4.2/build/src/libfreeling/cmake_install.cmake
sudo chmod 755 /usr/local/lib/libfreeling.so
sudo install -m 644 /home/user/build/FreeLing-4.2/src/include/freeling/morfo/np.h /usr/local/include/freeling/morfo/np.h
sudo ldconfig
```

The library folder's install script (`build/src/libfreeling/cmake_install.cmake`)
installs `libfreeling.so` and nothing else, and sets its run path to
`/usr/local/lib`; the library in the build folder points at the build
folder's libraries, so it must not be copied by hand. Only the library
changes: the programs (`analyze`, `analyzer`, `analyzer_client`) load it at
run time and need not be reinstalled. **`make install` is not needed, and
with FreeLing es-CL 2027 it does harm**: it also reinstalls FreeLing's own
data files over the Chilean ones in `/usr/local/share/freeling`. After any
`make install`, deploy FreeLing es-CL 2027 again
(`freeling_escl_deploy.py --target system`).

Install the library before the data. The classifier file with
`<ClassShares>` stops a FreeLing without the change, so
`freeling_escl_deploy.py --target system` refuses to install it unless the
installed library has the change.

## 8. Verifying

The library holds the names of the five sections and the `keep:` option
(as 32-bit strings):

```bash
strings -e L /usr/local/lib/libfreeling.so | grep -c -x -E "DictionaryClasses|FixedClasses|ClassesAtSentenceStart|SentenceStartClasses|ClassShares|keep:"
```

| Result | The library |
|---|---|
| 6 | has this change |
| 5 | has the first state of the change (no `keep:` prefixes): it would drop the verb readings of a `keep:V` line |
| 3 | has the first version (the three recognizer sections only): it stops on the classifier file |
| 0 | is FreeLing 4.2 without the change |

`freeling_escl_deploy.py` (system target) and `freeling_tag_corpus.py`
(COSCACH and CODICACH) make the same check and refuse anything but 6.

## 9. Examples

With the configs of FreeLing es-CL 2027: CODICACH (written texts, `np.dat`,
`<ClassesAtSentenceStart>` no) and COSCACH (transcribed speech,
`np-speech.dat`, yes). Before: FreeLing 4.2 without the change, with the
same data (the four sections are skipped) and FreeLing's own classifier
file.

| Sentence | Before | After, written | After, speech |
|---|---|---|---|
| Castro tiene palafitos. | castro: common noun | castro: common noun | Castro: place |
| Vivo en Castro desde marzo. | place | place | place |
| Arica es la ciudad de la eterna primavera. | place (the dictionary has arica as a place only) | place | place |
| Fuimos a Valdivia y a Concepción. | Concepción: place | place | place |
| Molina queda cerca de Talca. | molina: verb molinar | Molina: person (the classifier) | person (the classifier) |
| Allá en Molina hace calor. | Molina: place | place | place |
| Vivo en Molina. | Molina: place | place | place |
| Pinto la casa todos los años. | pinto: verb pintar | the verb | Pinto: person |
| pinto la casa todos los años. | verb | verb | verb |
| Pinto dijo que no vendría. | pinto: verb pintar | Pinto: person | person |
| Vivo en María Pinto. | place | place | place |
| Barbados es una isla. | place (the dictionary has barbados as a place only) | place | place |
| Catar es un país pequeño. | catar: verb | Catar: place | place |
| Catar el vino requiere práctica. | verb | verb | place |
| Tomé es una ciudad costera. | tomé: verb tomar | Tomé: place | place |
| Tomé un café. | verb | verb | place |
| Irán tiene mucho petróleo. | irán: verb ir | Irán: place | place |
| Irán con nosotros. | verb | verb | place |
| Quito es la capital del Ecuador. | quito: adjective | Quito: place | place |
| Quito la tapa. | verb quitar | verb | place |
| Yo quito la tapa. | verb | verb | verb |
| Lima es la capital del Perú. | lima: common noun | lima: common noun | Lima: place |
| Fui a Lima y a Caracas. | place, place | place, place | place, place |
| Viajamos a Asunción en enero. | person | place | place |
| La señora Asunción vive al lado. | person | person | person |
| La SES organizó los JUDEJUT. | SES: organization, JUDEJUT: organization | SES: organization, JUDEJUT: other | the same |
| Vimos al Dr. House. | Dr._House: other | Dr._House: person | person |

In transcribed speech a capitalized word at the start of a line is taken
for a name, so the verbs there (Tomé un café) become places and Pinto the
surname; in COSCACH such lines are rare, and nearly every capital at the
start of a line is a name (section 10): a speaker's verb is written in
lower case (pinto la casa).

## 10. Measured effect

On 21,366 lines of COSCACH (Chilean Spanish, transcribed speech) holding a
place name of the Chilean data: 24,408 occurrences of a place name, 22,422
of them a token of exactly the name (the others are part of a longer name,
such as Hospital de Puerto Montt). The class each exact token got:

| FreeLing | Place | Person | Organization | Other | Not a name |
|---|---|---|---|---|---|
| 4.2 with FreeLing es-CL 2027 until 261110 | 16,940 (75.6%) | 3,666 (16.4%) | 1,573 (7.0%) | 162 (0.7%) | 81 (0.4%) |
| the same, with the Chilean place and person lists of the classifier | 21,641 (96.5%) | 71 (0.3%) | 600 (2.7%) | 29 (0.1%) | 81 (0.4%) |
| with this change, speech mode (`np-speech.dat`) | 22,304 of 22,394 (99.6%) | 17 (0.1%) | 46 (0.2%) | 14 (0.1%) | 13 (0.1%) |
| with this change, written mode (`np.dat`) | 22,302 (99.5%) | 16 (0.1%) | 49 (0.2%) | 15 (0.1%) | 40 (0.2%) |

The word lists alone give most of the gain; the rest needs the fixed
classes: with the lists only, Concepción was still an organization 20 times,
and every place at the start of a line that is also a common noun or a verb
(Castro 14 times) was still that word.

In speech mode 28 occurrences at the start of a line are joined to the
next capitalized word, so there are 22,394 exact tokens. What is left, in
speech mode: Pinto a person 4 times (a surname by decision; in written
mode its one occurrence at the start of a line is the verb), Alameda 9 and
Corona 7 times an organization, Navidad 7 times another name (not fixed),
Molina once a person (Enrique Molina, a school named after a person;
section 11). In written mode also Castro 14 times the common noun at the
start of a line (section 3.3). Before the rulings of 261110g (molina on
FreeLing's list of whole person names, Pinto also the verb at the start of
a COSCACH line) speech mode gave 22,289 places (99.5%) and 31 persons,
written mode 22,287 (99.4%) and 31.

Of the 2,306 other names in the same lines (not place names of the Chilean
data), 459 changed class, most of them for the better: 255 from
organization to place (Chile, Argentina, Estados Unidos, Cuba), 71 given
names from organization to person (Diego, Camila, Ignacio), 37 from person
to place (San Martín, Viña). Some went the other way: 27 from place to
person (Florencia, Errázuriz), 14 from place to organization (Inacap,
Cepal, Huachipato, which are not places either).

## 11. What it does not decide

- **A whole name that holds a place.** "con Santiago Pérez" is one name,
  Santiago_Pérez, and the classifier still calls it a place; a fixed class
  applies to the whole name only. Likewise two places in a row are joined
  into one name ("Caracas Venezuela" becomes Caracas_Venezuela), which the
  classifier classifies.
- **A place left to the classifier.** Molina (a commune and a common
  surname) and Navidad (a commune and the holiday) are not fixed. Of
  Molina's 32 occurrences as a single word in the probe, all but one of
  them the commune, the classifier read 25 as a person; with its class
  shares (place 0.75, person 0.25) it read 16. What held the person up was
  FreeLing's own list of whole person names, which had molina: with molina
  taken off that list (FreeLing es-CL 2027, decided 261110g), the
  classifier reads 31 of the 32 as a place, the one person left being
  Enrique Molina, a school named after a person. A share weighs the
  evidence the classifier has; it does not remove it. At the start of a
  sentence the classifier can still call Molina a person ("Molina queda
  cerca de Talca").
- **A dictionary that knows a name with one class only.** Florencia, the
  Italian city, is a person: the dictionary has the given name only.
- **The share of a class is a weight, not a detector** (section 4).

## 12. Changelog

- 261110, revised the same day, before it was installed: the recognizer's
  `<SentenceStartClasses>` (a reading at the start of a sentence, with
  `keep` and `keep:` prefixes), and the classifier's `<ClassShares>`
  (`src/libfreeling/nec.cc`); the classifier keeps FreeLing 4.2's size.
- 261110: first version: the recognizer's `<DictionaryClasses>`,
  `<FixedClasses>` and `<ClassesAtSentenceStart>`.
