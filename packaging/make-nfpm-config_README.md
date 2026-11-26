# make-nfpm-config_README.md

Documents `make-nfpm-config.py` 1.1.0.

## Purpose

Writes the nfpm configuration of the package `freeling-es-cl` from what `build-freeling.sh` left: the files in `pkgroot/`, the library path in `pkgetc/` and the dependencies in `pkgdeps.txt`. The package owns its own files and folders under `/usr/local`, never `/usr/local` itself or its standard folders. Its description says that it carries its own ICU and Boost (`build-freeling.sh`, `bundle-libraries.sh`).

## Usage

From the repository root:

```bash
EXTRA_DEPENDS=glibc-langpack-en packaging/make-nfpm-config.py 261112.fc44 > nfpm-run.yaml
```

The argument is the package release, the distribution included (`261112.fc44`, `261112.tw` for openSUSE Tumbleweed, `261112~debian13`, `261112~ubuntu24.04`, `261112` for Arch Linux), so the packages of different distributions have names of their own. `EXTRA_DEPENDS` adds dependencies that no shared library shows: the package of the en_US.UTF-8 locale (`glibc-langpack-en` on Fedora, `glibc-locale` on openSUSE, `locales` on Debian and Ubuntu; none on Arch Linux, whose glibc carries every locale and whose package generates en_US.UTF-8 when it is installed, with `postinstall-deb.sh`).

## Platform

Python 3, standard library only. Linux and Windows.

## Changelog

- 1.1.0 (261126): the package description says that FreeLing carries its own copies of ICU and Boost, in `/usr/local/lib/freeling-es-cl`; the Arch Linux package runs `postinstall-deb.sh` and `ldconfig.sh`, as the Debian one does.
- 1.0.0 (261112): first version.
