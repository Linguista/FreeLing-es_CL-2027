# patch-freeling_README.md

Documents `patch-freeling.sh` 1.1.0.

## Purpose

Applies to an unpacked FreeLing 4.2 source tree every change FreeLing es-CL 2027 is built with: the source fixes current compilers need (C++17, `<cmath>` in five files, the two errors in unused templates), the install fix and Spanish only (the language list limited to `es`, the variants to FreeLing Old `es/es-old` and `es/es-cl`; the English and Portuguese data the source tarball carries, the Argentine variant `es/es-ar` and the configs of every other language deleted from the tree, so nothing of them is built or installed, decided 261112), the fix of the bug that aborts word-sense annotation, and the name-class change (`software/patches/freeling-4.2-np-classes.patch`). The README's section "If you really want to try and build this rather than use a package..." explains each one.

## Usage

```bash
packaging/patch-freeling.sh FreeLing-4.2 software/patches/freeling-4.2-np-classes.patch
```

The first argument is the unpacked source folder of `FreeLing-src-4.2.tar.gz`; the second, the name-class patch.

## What it checks

The three files the name-class patch changes (`np.cc`, `np.h`, `nec.cc`) must be FreeLing 4.2's, by sha256, and every line it edits must be there exactly as in FreeLing 4.2. The language and variant lists must be FreeLing 4.2's, the English, Portuguese and Argentine folders and the fifteen other configs must be there, and afterwards `data/` must hold only `common`, `config` and `es`, and `data/config` only `es-cl.cfg`, `es-old.cfg`, `es.cfg` and `ident.cfg` (FreeLing's language identifier, which `common/lang_ident` serves). Anything else stops it with a message and exit 1, so it never half-patches a different source. Run it once, on a freshly unpacked tree.

## Platform

Linux. bash, sed, patch, sha256sum.

## Tested

261113, version 1.1.0, on a freshly unpacked `FreeLing-src-4.2.tar.gz`: every change applied; FreeLing then configured, built and installed with only Spanish (`share/freeling/` holding `common`, `config` and `es`; FreeLing Old and es-cl the only variants), and analyzed with `es-cl.cfg`, `es-cl-19th-century.cfg` and `es-old.cfg`. A first attempt that expected the fourteen other language folders stopped at once, as it should: the source tarball carries only English and Portuguese besides Spanish.

## Changelog

- 1.1.0 (261113): Spanish only: the language list `es`, the variants `es/es-old` and `es/es-cl`; the English and Portuguese data, `es/es-ar` and the configs of the other languages deleted from the source tree.
- 1.0.0 (261112): first version.
