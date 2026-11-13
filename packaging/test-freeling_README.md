# test-freeling_README.md

Documents `test-freeling.sh` 1.1.0.

## Purpose

Checks an installed FreeLing es-CL 2027 package: `libfreeling.so` has the name-class change; the 17 Chilean files are this release's (their sha256 as in `SHA256SUMS`); `cities-CL.dat` is gone; `es/locucions.dat` is a link to `es-cl/locucions.dat`; no English, Portuguese or Argentine data is installed; FreeLing analyzes "Vos tenís que venir a Arica." with `es-cl.cfg` (tenís is a voseo form of tener, `VMIP2SV`), "La jente i el rei." with `es-cl-19th-century.cfg` (jente is gente, i is y) and "Et dixo el rey." with `es-old.cfg` (dixo is decir). It prints FreeLing's output.

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

## Exit codes

0 every check passed (it prints ALL CHECKS PASSED); 1 a check failed (it prints FAIL and what failed).

## Platform

Linux and macOS. bash, binutils (strings), sha256sum.

## Tested

261113, version 1.1.0, against FreeLing 4.2 built with `patch-freeling.sh` 1.1.0 and the release of `freeling_escl_build.py` 2.8.0 installed (the prefix changed for the test): ALL CHECKS PASSED.

## Changelog

- 1.1.0 (261113): the 19th-century files and the two configs among the files checked; the link for FreeLing Old; only Spanish installed; the 19th-century and FreeLing Old analyses; `PREFIX` for another install prefix, and `libfreeling.dylib` (macOS).
- 1.0.0 (261112): first version.
