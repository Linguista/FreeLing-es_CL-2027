# make-nfpm-config_README.md

Documents `make-nfpm-config.py` 1.0.0.

## Purpose

Writes the nfpm configuration of the package `freeling-es-cl` from what `build-freeling.sh` left: the files in `pkgroot/`, the library path in `pkgetc/` and the dependencies in `pkgdeps.txt`. The package owns its own files and folders under `/usr/local`, never `/usr/local` itself or its standard folders.

## Usage

From the repository root:

```bash
EXTRA_DEPENDS=glibc-langpack-en packaging/make-nfpm-config.py 261112.fc44 > nfpm-run.yaml
```

The argument is the package release, the distribution included (`261112.fc44`, `261112~debian13`, `261112~ubuntu24.04`), so the packages of different distributions have names of their own. `EXTRA_DEPENDS` adds dependencies that no shared library shows: the package of the en_US.UTF-8 locale (`glibc-langpack-en` on Fedora, `locales` on Debian and Ubuntu).

## Platform

Python 3, standard library only. Linux and Windows.
