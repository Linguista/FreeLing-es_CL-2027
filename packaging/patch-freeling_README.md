# patch-freeling_README.md

Documents `patch-freeling.sh` 1.2.0.

## Purpose

Applies to an unpacked FreeLing 4.2 source tree every change FreeLing es-CL 2027 is built with: the source fixes current compilers need (C++17, `<cmath>` in five files, the two errors in unused templates), the install fix and Spanish only (the language list limited to `es`, the variants to FreeLing Old `es/es-old` and `es/es-cl`; the English and Portuguese data the source tarball carries, the Argentine variant `es/es-ar` and the configs of every other language deleted from the tree, so nothing of them is built or installed, decided 261112), the fix of the bug that aborts word-sense annotation, the name-class change (`software/patches/freeling-4.2-np-classes.patch`), and the six fixes FreeLing 4.2 needs to build and run on Windows with GCC (MSYS2's UCRT64, the Windows build): each takes effect only there (under `__MINGW32__`, or in a Windows-only part of a `CMakeLists.txt`), so Linux and macOS build exactly as before. The README's section "If you really want to try and build this rather than use a package..." explains each one.

## Usage

```bash
packaging/patch-freeling.sh FreeLing-4.2 software/patches/freeling-4.2-np-classes.patch
```

The first argument is the unpacked source folder of `FreeLing-src-4.2.tar.gz`; the second, the name-class patch.

## What it checks

The three files the name-class patch changes (`np.cc`, `np.h`, `nec.cc`) must be FreeLing 4.2's, by sha256, and every line it edits must be there exactly as in FreeLing 4.2. The language and variant lists must be FreeLing 4.2's, the English, Portuguese and Argentine folders and the fifteen other configs must be there, and afterwards `data/` must hold only `common`, `config` and `es`, and `data/config` only `es-cl.cfg`, `es-old.cfg`, `es.cfg` and `ident.cfg` (FreeLing's language identifier, which `common/lang_ident` serves). Anything else stops it with a message and exit 1, so it never half-patches a different source. Run it once, on a freshly unpacked tree.

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

261113, version 1.1.0, on a freshly unpacked `FreeLing-src-4.2.tar.gz`: every change applied; FreeLing then configured, built and installed with only Spanish (`share/freeling/` holding `common`, `config` and `es`; FreeLing Old and es-cl the only variants), and analyzed with `es-cl.cfg`, `es-cl-19th-century.cfg` and `es-old.cfg`. A first attempt that expected the fourteen other language folders stopped at once, as it should: the source tarball carries only English and Portuguese besides Spanish.

## Changelog

- 1.2.0 (261113): the six Windows fixes (9a to 9f), each effective only on Windows with GCC.
- 1.1.0 (261113): Spanish only: the language list `es`, the variants `es/es-old` and `es/es-cl`; the English and Portuguese data, `es/es-ar` and the configs of the other languages deleted from the source tree.
- 1.0.0 (261112): first version.
