# test-freeling_README.md

Documents `test-freeling.sh` 1.2.0.

## Purpose

Checks an installed FreeLing es-CL 2027 package: the library (`libfreeling.so`, `libfreeling.dylib` on macOS, `libfreeling.dll` on Windows) has the name-class change; the 17 Chilean files are this release's (their sha256 as in `SHA256SUMS`); `cities-CL.dat` is gone; `es/locucions.dat` is a link to `es-cl/locucions.dat` (on Windows, a copy of it); no English, Portuguese or Argentine data is installed; FreeLing analyzes "Vos tenís que venir a Arica." with `es-cl.cfg` (tenís is a voseo form of tener, `VMIP2SV`), "Él llegó a Ñuñoa." with `es-cl.cfg` (a capital other than A to Z is lowercased: Él has the lemma él, Ñuñoa ñuñoa), "La jente i el rei." with `es-cl-19th-century.cfg` (jente is gente, i is y) and "Et dixo el rey." with `es-old.cfg` (dixo is decir). It prints FreeLing's output.

## Usage

From the repository root, on a machine where the package is installed:

```bash
packaging/test-freeling.sh
```

With another install prefix than `/usr/local` (the macOS tarballs install into `/usr/local/freeling-es-cl-2027`):

```bash
PREFIX=/usr/local/freeling-es-cl-2027 packaging/test-freeling.sh
```

On macOS the library is `libfreeling.dylib`, and GNU coreutils and binutils (`sha256sum`, `strings -e L`) must come first in `PATH`, as the macOS job of `.github/workflows/packages.yml` sets them.

On Windows it runs in MSYS2's UCRT64 shell, with `PREFIX` the folder FreeLing is installed in, and runs `analyzer.exe` itself, with `FREELINGSHARE` set to the installed data folder as `analyze.bat` sets it and the full path of each config; the library's wide strings are 16-bit there (`strings -e l`).

## Exit codes

0 every check passed (it prints ALL CHECKS PASSED); 1 a check failed (it prints FAIL and what failed).

## Platform

Linux, macOS, and Windows in MSYS2's UCRT64 shell. bash, binutils (strings), sha256sum; on Windows also cygpath and cmp.

## Tested

261113, version 1.1.0, against FreeLing 4.2 built with `patch-freeling.sh` 1.1.0 and the release of `freeling_escl_build.py` 2.8.0 installed (the prefix changed for the test): ALL CHECKS PASSED.

## Changelog

- 1.2.0 (261113): the lowercasing check (Él, Ñuñoa), which found the Windows build leaving Ñ and accented capitals uncased; Windows: `libfreeling.dll`, its 16-bit wide strings, `analyzer.exe` run with `FREELINGSHARE` set, and `es/locucions.dat` a copy of `es-cl/locucions.dat`.
- 1.1.0 (261113): the 19th-century files and the two configs among the files checked; the link for FreeLing Old; only Spanish installed; the 19th-century and FreeLing Old analyses; `PREFIX` for another install prefix, and `libfreeling.dylib` (macOS).
- 1.0.0 (261112): first version.
