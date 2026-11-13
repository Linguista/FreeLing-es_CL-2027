# install-data_README.md

Documents `install-data.sh` 1.0.0.

## Purpose

Puts FreeLing es-CL 2027's data into an installed FreeLing 4.2: the 17 Chilean files over FreeLing's own (the files and places of `freeling_escl_deploy.py --target system`: the 2027 and 19th-century data, the name recognizer and classifier files, the configs `es-cl.cfg` and `es-cl-19th-century.cfg`), removes FreeLing's Chilean city list (`common/nec/cities-CL.dat`, which the Chilean `cities.dat` merges), and makes `es/locucions.dat`, the multiword file FreeLing Old reads, a link to `es-cl/locucions.dat`. `build-freeling.sh` (the Linux packages) and the macOS job of `.github/workflows/packages.yml` run it.

## Usage

From anywhere:

```bash
packaging/install-data.sh /usr/local/share/freeling
```

The argument is FreeLing's installed data folder; it must hold `es/es-cl` and `config`.

## Exit codes

0 done; 1 the folder is not FreeLing's data folder; anything else is the failing command's own code (the script stops at the first error).

## Platform

Linux and macOS. bash, cp, chmod, ln.
