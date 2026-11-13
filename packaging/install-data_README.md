# install-data_README.md

Documents `install-data.sh` 1.1.0.

## Purpose

Puts FreeLing es-CL 2027's data into an installed FreeLing 4.2: the 17 Chilean files over FreeLing's own (the 2027 and 19th-century data, the name recognizer and classifier files, the configs `es-cl.cfg` and `es-cl-19th-century.cfg`), removes FreeLing's Chilean city list (`common/nec/cities-CL.dat`, which the Chilean `cities.dat` merges), and makes `es/locucions.dat`, the multiword file FreeLing Old reads, a link to `es-cl/locucions.dat`. On Windows (MSYS2, the Windows build), where the package is a zip and a zip holds no symbolic links, it is a copy of `es-cl/locucions.dat` instead. `build-freeling.sh` (the Linux packages) and the macOS and Windows jobs of `.github/workflows/packages.yml` run it.

## Usage

From anywhere:

```bash
packaging/install-data.sh /usr/local/share/freeling
```

The argument is FreeLing's installed data folder; it must hold `es/es-cl` and `config`.

## Exit codes

0 done; 1 the folder is not FreeLing's data folder; anything else is the failing command's own code (the script stops at the first error).

## Platform

Linux, macOS, and Windows in MSYS2's shell. bash, cp, chmod, ln, uname.

## Tested

261113, version 1.1.0: GitHub Actions run 43379595248 (branch windows-package-test, 261113): all 14 jobs passed. On Windows `es/locucions.dat` was copied from `es-cl/locucions.dat` and checked identical; on Linux and macOS it is a link, as before. Run 43388088727 (261113), with the two Chilean test sentences, passed all 14 jobs as well.

## Changelog

- 1.1.0 (261113): Windows: `es/locucions.dat` is a copy of `es-cl/locucions.dat` (a zip holds no symbolic links).
- 1.0.0 (261113): first version.
