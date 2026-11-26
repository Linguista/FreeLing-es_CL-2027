# freeling-4.2-known-roots_README.md

Documents `freeling-4.2-known-roots.patch`, a change to the affix analysis of FreeLing 4.2, made for FreeLing es-CL 2027 (decided 261116). License: GNU Affero General Public License, version 3 or later, as FreeLing itself.

| File | What it is |
|---|---|
| `freeling-4.2-known-roots.patch` | the change, as a unified diff against FreeLing 4.2 (`FreeLing-src-4.2.tar.gz` of `https://github.com/TALP-UPC/FreeLing/releases/tag/4.2`, the same files as the tag 4.2) |
| `freeling-4.2-known-roots_README.md` | this file |

| File | FreeLing 4.2 (sha256) | With the change (sha256) |
|---|---|---|
| `src/libfreeling/suffixes.cc` | `2955d3d544c942772ed71707a4496f66bc9168cd8d2ee17c4c397cc4173f88ac` | `f867ccfd8d00e8abfd2d003b4c3af4456059ca8d47879a20a0476ab1e1d5f99e` |
| `src/include/freeling/morfo/suffixes.h` | `7895af5c58a98252466736283c30c9a3ebc005cac0bf3507553d9bfa5fa93d33` | `f003ed4307458ffd7f9ea8f9fa7bff02facdb9466c9c406ebd8866152ab02b32` |

The patch itself: `0585fda762872087c35f36da4606a52baa33e0842c6bae1c8ed344a79753aef6`.

## Contents

1. Purpose
2. What it changes
3. How it works in the code
4. Applying, building and installing
5. Verifying
6. Measured effect
7. What it does not change
8. Changelog

## 1. Purpose

FreeLing's affix analysis (`src/libfreeling/suffixes.cc`, configured by `es/afixos.dat`) reads a word the dictionary does not have, and the clitic forms of every verb, in three ways:

1. as a dictionary root and a suffix (acompañarlo: acompañar + lo);
2. as a prefix and a dictionary root (reagendar: re + agendar);
3. as a prefix, a dictionary root and a suffix (reagendarlo: re + agendar + lo).

It keeps every reading the three give, and the lemma of a prefixed reading is the prefix followed by the root's lemma. So a word that the first way reads correctly was also read the third way, as a prefix (`a`, `an`, `des`, `in`, `re` ...) plus another dictionary word, with a lemma that is not a word:

| Word | Wrong reading | Taken apart as | Beside |
|---|---|---|---|
| reírme | reir+me | re + ír + me | reír+me |
| acompañarlo | aacompañar+lo | a + compañar + lo | acompañar+lo |
| invertirla | inverter+lo | in + vertir + la | invertir+lo |
| ablandese | ablandir+se | a + blande + se | ablandar+se |
| aborreguelo | aborrego | a + borrego + uelo | aborregar+lo |

The two readings mostly share the tag, and so the probability. FreeLing then orders them alphabetically (`probabilities::less`), so the wrong lemma came first whenever it sorted first (aacompañar before acompañar, reir before reír). And the tagger splits a clitic form only when a single reading is left (`POS_tagger::retokenize`), so the token came out whole, with the wrong lemma and a joined tag: `acompañarlo aacompañar+lo VMN0000+PP3MSA0`. In the speech corpus, tagged before this change, this gave reir (60 tokens), aacompañar and aadelantar (38), inverter and reverter (7).

A second fault showed once such words were split. The split takes the root's form from the root FreeLing found first, and FreeLing searches the candidate roots in alphabetical order. When the dictionary also reads the spelling without the accent (the es-CL dictionary reads every accented word written without its accents, decided 261112), both reír and reir are found, reir first, and the split was reir + me. FreeLing 4.2 already gave oir + lo, freir + lo, sonreir + le and rehusa + lo this way.

## 2. What it changes

1. **A known root is not taken apart.** When the word is read as a dictionary root and a suffix (way 1), no prefix + root + suffix reading (way 3) is tried. FreeLing already never takes a known word apart into a prefix and another word; this extends that to a word whose root is known. A word with no dictionary root is read as before (reagendarlo: re + agendar + lo), and ways 1 and 2 are as before.

2. **A root written with the accent of a hiatus keeps it.** A candidate root with an accented i or u next to a, e or o (an h between them does not count: rehúsa) is searched first: reír, oír, freír, sonreír, ríe, sonríe, actúa, rehúsa. Split, the word keeps that form: reír + me, oír + lo, rehúsa + lo. Any other root keeps FreeLing's order, so an accent that only the clitic put there goes: dámelo is da + me + lo, dímelo di + me + lo.

## 3. How it works in the code

All in `src/libfreeling/suffixes.cc`, with the declarations in `src/include/freeling/morfo/suffixes.h`:

- `look_for_affixes` keeps a set of the suffixes with which a root was found. `look_for_affixes_in_list` fills it on the suffix pass: a suffix rule that added a reading to the word records its suffix.
- `look_for_combined_affixes` returns at once when that set is not empty.
- `hiatus_accent`, a new static function, says whether a lowercase form has an accented i or u next to a, e or o.
- `SearchRootsList` takes an optional root to search first; the suffix pass gives it the root as written when `hiatus_accent` says so.

FreeLing's traces (`TRACE`, compiled only with `-DVERBOSE`) say when a decomposition is skipped. No data file and no option changes: every config reads words the new way.

## 4. Applying, building and installing

From the top of an unpacked `FreeLing-src-4.2.tar.gz`:

```bash
patch -p1 --forward --batch < freeling-4.2-known-roots.patch
```

The release's `packaging/patch-freeling.sh` (1.3.0) applies it with the name-class change and FreeLing es-CL 2027's other changes, after checking by sha256 that the two files are FreeLing 4.2's, and checks the result by sha256. `packaging/build-freeling.sh` (1.2.0) builds and installs FreeLing with both changes, and the GitHub workflow `packages.yml` does the same for every package. On a machine whose FreeLing was built from source with the name-class change, the corpus project's `freeling_known_roots_install.py` applies this change to that source tree, builds the library alone, installs it and tests it.

The two changes touch different files (`np.cc`, `np.h`, `nec.cc`; `suffixes.cc`, `suffixes.h`) and apply in either order. Only `libfreeling` is rebuilt by them; the programs (`analyzer` and the others) are unchanged.

## 5. Verifying

```bash
echo "Me dio risa reírme." | analyze -f es-cl.cfg --outlv tagged --nonec --sense none
```

With the change: `reír reír VMN0000` and `me me PP1CS00`. Without it, with FreeLing es-CL 2027's lemma preference `reír reir` (since `freeling_escl_build.py` 2.10.0): `reir reír VMN0000` and `me`, the form without its accent (with the corpus project's the speech corpus config, which has `TaggerForceSelect=retok`, one token, `reírme reír+me VMN0000+PP1CS00`). `packaging/test-freeling.sh` (1.3.0) checks for `reír reír VMN0000` and `me me PP1CS00`.

## 6. Measured effect

Tested 261116 with FreeLing 4.2 built with the name-class change, with and without this change, and FreeLing es-CL 2027 as `freeling_escl_build.py` 2.9.0 built it.

**Every infinitive, gerund and imperative of the es-CL dictionary with its pronouns attached and its accent written where Spanish writes it** (299,875 words: cómetelo, comételo, dámelo, diciéndolo, reírse), read with `--outlv morfo`:

| | FreeLing 4.2 | With the change |
|---|---|---|
| words whose first reading has a lemma that is not a dictionary word (aacompañar, reir, ablandir, aborrego) | 688 | 0 |
| words whose first reading is another dictionary verb, through another split of the pronouns | 36 | 17 |
| readings of the word's own verb lost | | 0 |

Of the 17 left, 12 are forms Spanish does not have, which the list of words made by attaching te to an usted imperative (sáltetelo; the tú imperative is sáltatelo); the other 5 are genuinely two words: atenlo (atén + lo, of atener, or aten + lo, of atar, which Spanish writes átenlo), retenlo, táseme, ténseme, vérseme. The change does not touch them; FreeLing still orders such readings alphabetically.

A first measurement of 261116 attached lo and se without writing the accent (cometelo, a misspelling), and its figures (253 and 58 before, 0 and 50 after, of 119,954 words) are replaced by these.

**760,859 tokens of written Chilean Spanish** (the written corpus texts, tagged with a speech config like the speech corpus's and FreeLing es-CL 2027 of 261115): 47 tokens changed.

| Word | Tokens | FreeLing 4.2 | With the change |
|---|---|---|---|
| parasitoide, parasitoides | 26 | lemma parasito | lemma parásito |
| multiplete, multipletes | 12 | lemma multiple, NC | lemma múltiplo; 10 NC, 2 AQ |
| acompañarla, acompañarse, adelantarse, adelantarme, adentrarnos, reirse | 6 | one token, lemma aacompañar, aadelantar, adentrar, reir, joined tag | split: acompañar, adelantar, adentrar, reír and the clitic |
| oír (in oírlo) | 1 | form oir | form oír |
| cobardón | 1 | cobarda NCMS00V | cobarde AQVMS00 |
| apare | 1 | aparir | aparar |

45 are corrections. Two multiplete tokens went from noun to adjective: FreeLing reads multiplete as a diminutive (-ete), before of the non-word multiple and now of múltiplo, as a noun and as an adjective; without the reading of multiple, the adjective is likelier in two contexts. The noun multiplete is in neither.

The patched source builds with GCC 13 (Ubuntu 24.04) as part of the whole library, with the name-class change and C++17, and `libfreeling.so` is the only file built again.

## 7. What it does not change

- Known words: FreeLing gives a dictionary word only the affix rules marked "always" (the clitics), as before; this change applies to them in the same way.
- `afixos.dat`: no rule is added, removed or changed. A word with no dictionary root still gets prefix readings (way 2 and way 3).
- The order of two readings that tie and are both real (the 5 above, and ve as ir and as ver): FreeLing still orders them alphabetically unless `probabilitats.dat` has a lemma preference for them.

## 8. Changelog

- 261116b: the measurement redone on the words with their accents written (section 6); `patch-freeling.sh` 1.3.0, `test-freeling.sh` 1.3.0 and `freeling_known_roots_install.py` named. The patch is unchanged.
- 261116: first version, for FreeLing es-CL 2027 (`freeling_escl_build.py` 2.10.0).
