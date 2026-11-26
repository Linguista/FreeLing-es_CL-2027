# patch-freeling_README.md

Documents `patch-freeling.sh` 1.5.0.

## Purpose

Applies to an unpacked FreeLing 4.2 source tree every change FreeLing es-CL 2027 is built with: the source fixes current compilers need (C++17, `<cmath>` in five files, the two errors in unused templates), the install fix and Spanish only (the language list limited to `es`, the variants to FreeLing Old `es/es-old` and `es/es-cl`; the English and Portuguese data the source tarball carries, the Argentine variant `es/es-ar` and the configs of every other language deleted from the tree, so nothing of them is built or installed, decided 261112), the fix of the bug that aborts word-sense annotation, the name-class change (`software/patches/freeling-4.2-np-classes.patch`), and the six fixes FreeLing 4.2 needs to build and run on Windows with GCC (MSYS2's UCRT64, the Windows build): each takes effect only there (under `__MINGW32__`, or in a Windows-only part of a `CMakeLists.txt`), so Linux and macOS build exactly as before; and the known-roots change of the affix analysis (`software/patches/freeling-4.2-known-roots.patch`, change 10, decided 261116): a word read as a dictionary root and a suffix is not also taken apart into a prefix, another root and a suffix (reírse is no longer reir + se, acompañarlo no longer aacompañar + lo), and a root with the accent of a hiatus keeps it when the word is split (reír + me). The README's section "If you really want to try and build this rather than use a package..." explains each one.

## Usage

```bash
packaging/patch-freeling.sh FreeLing-4.2 software/patches/freeling-4.2-np-classes.patch software/patches/freeling-4.2-known-roots.patch software/patches/freeling-4.2-tag-probabilities.patch software/patches/freeling-4.2-ambiguous-multiwords.patch
```

The first argument is the unpacked source folder of `FreeLing-src-4.2.tar.gz`; the second, the name-class patch; the third, the known-roots patch; the fourth, the tag-probabilities patch (the CoNLL columns `LEX_PROB` and `TAG_PROB`); the fifth, the ambiguous-multiwords patch (multiwords marked `A` decided by the tagger), which builds on the fourth and is applied after it. All five are required.

## Changes 11 and 12

| | Patch | The change |
|---|---|---|
| 11 | `freeling-4.2-tag-probabilities.patch` | two new CoNLL columns: `LEX_PROB`, the probability of the selected reading among the readings of the word, and `TAG_PROB`, the probability the tagger gives the selected tag in its sentence |
| 12 | `freeling-4.2-ambiguous-multiwords.patch` | a defect of FreeLing 4.2 fixed: it reads the `A` (ambiguous) flag of its multiword file and never uses it, so every multiword was always joined; the tagger now decides, and the flag may carry a weight (`A:0.9`) |

Each has a README in `software/patches/`. The twelve files they change (the tagger, the class `word`, the multiword module, the probabilities module and the CoNLL reader and writer) must be FreeLing 4.2's before, by sha256, and have the sha256 the two READMEs give after.

## What it checks

The three files the name-class patch changes (`np.cc`, `np.h`, `nec.cc`) and the two the known-roots patch changes (`suffixes.cc`, `suffixes.h`) must be FreeLing 4.2's, by sha256, and every line it edits must be there exactly as in FreeLing 4.2; after the known-roots patch, `suffixes.cc` and `suffixes.h` must have the sha256 its README gives. The language and variant lists must be FreeLing 4.2's, the English, Portuguese and Argentine folders and the fifteen other configs must be there, and afterwards `data/` must hold only `common`, `config` and `es`, and `data/config` only `es-cl.cfg`, `es-old.cfg`, `es.cfg` and `ident.cfg` (FreeLing's language identifier, which `common/lang_ident` serves). Anything else stops it with a message and exit 1, so it never half-patches a different source. Run it once, on a freshly unpacked tree.

## The Windows fixes

| | File | The fix |
|---|---|---|
| 9a | `src/crfsuite/CMakeLists.txt` | crfsuite no longer defines `_MSC_VER` (only Microsoft's compiler does): with it, MinGW's headers give their inline functions ordinary definitions and the library does not link (multiple definition of `llabs`, `fabs` ...) |
| 9b | `src/crfsuite/crfsuite/crf/vecmath.h`, `lbfgs/arithmetic_sse_double.h`, `lbfgs/arithmetic_sse_float.h` | aligned memory with MinGW's `_aligned_malloc` and `_aligned_free`; MinGW has no `posix_memalign` |
| 9c | `src/libfreeling/CMakeLists.txt` | libfreeling also links ICU's i18n and data libraries under their Windows names (`ICU_IN_LIBRARY`, `ICU_DT_LIBRARY`), without which ICU's collator is not found |
| 9d | `src/libfreeling/util.cc` | the locale: libstdc++ on MinGW knows only "C", and FreeLing's `eng` stops every program; the C runtime gets the UTF-8 locale (it classifies the characters) and the C++ locale stays "C" |
| 9e | `src/libfreeling/util.cc` | the standard streams convert UTF-8 themselves, as on macOS, instead of the C runtime's wide mode (`_O_U8TEXT`), through which only Microsoft's streams write: with it FreeLing reads and writes nothing |
| 9f | `src/libfreeling/util.cc`, `src/libfreeling/dictionary.cc` | upper and lower case through ICU (`u_tolower`, `u_toupper`), which FreeLing already links: MinGW's C runtime changes the case of A to Z only, so the lowercase form of a capitalized Él, Ángel or Ñuñoa kept its capital; FreeLing looks words up in the dictionary by that form, and gives names it as their lemma (`Ñuñoa Ñuñoa NP00SP0` in place of `Ñuñoa ñuñoa NP00SP0`) |

Two more are build options, in the Windows job of `.github/workflows/packages.yml`: Boost linked dynamically (`-DBoost_USE_STATIC_LIBS=OFF`: CMake's default on Windows is static, and FreeLing asks for the dynamic libraries, which Boost refuses to mix), and every symbol of each DLL exported (`-Wl,--export-all-symbols`: dynet marks a few symbols for export, and GNU's linker then exports nothing else).

## Platform

Linux, macOS (with GNU sed first in `PATH`), and Windows in MSYS2's shell. bash, GNU sed, grep, patch, sha256sum.

## Tested

261119, version 1.5.0, on a freshly unpacked `FreeLing-src-4.2.tar.gz`: every change applied, the two new patches included, and the twelve files came out with the sha256 of their READMEs; with the two new patches given in the wrong order it stopped (the second does not apply before the first). The patched files were built into FreeLing with the name-class and known-roots changes (GCC 13) and tested as the two READMEs say. Not yet run by GitHub's workflow.

261116, version 1.3.0, on the source files of a freshly unpacked `FreeLing-src-4.2.tar.gz` (sha256 checked; `CMakeLists.txt`, `src/` and `data/config/`, with the language folders it deletes stood in by empty ones): every change applied, the known-roots patch included, and `suffixes.cc` and `suffixes.h` came out with the sha256 of the known-roots README; run a second time on the same tree, it stopped at once, as it should. The known-roots change was built into `libfreeling` with the name-class change and tested as its README says; the Windows fixes touch other files and are unchanged.

261113, version 1.1.0, on a freshly unpacked `FreeLing-src-4.2.tar.gz`: every change applied; FreeLing then configured, built and installed with only Spanish (`share/freeling/` holding `common`, `config` and `es`; FreeLing Old and es-cl the only variants), and analyzed with `es-cl.cfg`, `es-cl-19th-century.cfg` and `es-old.cfg`. A first attempt that expected the fourteen other language folders stopped at once, as it should: the source tarball carries only English and Portuguese besides Spanish.

261113, version 1.2.0: two fresh source trees patched here, one by 1.1.0 and one by 1.2.0, differ only in the seven files of the six Windows fixes (the three crfsuite headers and its `CMakeLists.txt`, libfreeling's `CMakeLists.txt`, `util.cc` and `dictionary.cc`); the Linux and macOS builds below confirm that none of it changes them. GitHub Actions run 43379595248 (branch windows-package-test, 261113): all 14 jobs passed. Windows (MSYS2 UCRT64, GCC) built with all six Windows fixes, and its package checks and the check of the zip from PowerShell passed; before fix 9f the Windows build lemmatized Ñuñoa as Ñuñoa, after it as ñuñoa, as on Linux and macOS. The five Linux builds and their tests on clean systems, and both macOS builds, passed unchanged. Run 43388088727 (261113), with the two Chilean test sentences, passed all 14 jobs as well.

## Changelog

- 1.5.0 (261119): changes 11 and 12, the probability columns and the ambiguous multiwords, applied from a fourth and a fifth argument after the known-roots change, with their twelve files checked by sha256 before and after.
- 1.4.0 (261119): checks that FreeLing Old's `data/config/es-old.cfg` has compound analysis off, as FreeLing ships it (compound analysis off in every config, decided 261118); nothing in FreeLing Old is changed.
- 1.3.0 (261116): change 10, the known-roots change of the affix analysis, applied from a third argument after the Windows fixes, with `suffixes.cc` and `suffixes.h` checked by sha256 before and after; the patch paths are made absolute before the script changes folder.
- 1.2.0 (261113): the six Windows fixes (9a to 9f), each effective only on Windows with GCC.
- 1.1.0 (261113): Spanish only: the language list `es`, the variants `es/es-old` and `es/es-cl`; the English and Portuguese data, `es/es-ar` and the configs of the other languages deleted from the source tree.
- 1.0.0 (261112): first version.
