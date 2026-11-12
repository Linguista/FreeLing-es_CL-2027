# patch-freeling_README.md

Documents `patch-freeling.sh` 1.0.0.

## Purpose

Applies to an unpacked FreeLing 4.2 source tree every change FreeLing es-CL 2027 is built with: the source fixes current compilers need (C++17, `<cmath>` in five files, the two errors in unused templates), the install fix (only the Spanish variants), the fix of the bug that aborts word-sense annotation, and the name-class change (`software/patches/freeling-4.2-np-classes.patch`). The README's section "If you really want to try and build this rather than use a package..." explains each one.

## Usage

```bash
packaging/patch-freeling.sh FreeLing-4.2 software/patches/freeling-4.2-np-classes.patch
```

The first argument is the unpacked source folder of `FreeLing-src-4.2.tar.gz`; the second, the name-class patch.

## What it checks

The three files the name-class patch changes (`np.cc`, `np.h`, `nec.cc`) must be FreeLing 4.2's, by sha256, and every line it edits must be there exactly as in FreeLing 4.2. Anything else stops it with a message and exit 1, so it never half-patches a different source. Run it once, on a freshly unpacked tree.

## Platform

Linux. bash, sed, patch, sha256sum.
