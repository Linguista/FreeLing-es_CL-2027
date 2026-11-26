# build-freeling_README.md

Documents `build-freeling.sh` 1.4.0.

## Purpose

Builds FreeLing 4.2 with the changes of FreeLing es-CL 2027 (`patch-freeling.sh`), installs it in `/usr/local` with this repository's Chilean data in place of FreeLing's own files and with its own copies of the ICU and Boost libraries it was built against (`bundle-libraries.sh`), and leaves everything installed ready for packaging. It is what the GitHub workflow `.github/workflows/packages.yml` runs on each distribution.

## Usage

```bash
packaging/build-freeling.sh FreeLing-src-4.2.tar.gz
```

Run it as root, on a fresh, disposable machine or container: FreeLing's own `make install` writes straight into `/usr/local` (its install step builds the dictionaries there, ignoring `DESTDIR`), and the script then moves everything the install added out of `/usr/local` into `pkgroot/`. Files that were in `/usr/local` before are left alone and never packaged.

| Variable | Effect |
|---|---|
| `JOBS` | parallel compile jobs (default: the number of processors) |
| `WORK` | the build folder (default `/tmp/freeling-build`) |
| `REMOVE_TARBALL=yes` | delete the source tarball once unpacked (saves disk on GitHub's machines) |
| `PREFIX` | the install prefix (default `/usr/local`); the generic Linux tarball uses `/opt/freeling-es-cl-2027` |
| `RELOCATABLE=yes` | run paths relative to each file, so the prefix can be moved (the generic Linux tarball; `bundle-libraries.sh`) |

## What it does

1. Checks the tarball's sha256 (`f96afbdb000d7375426644fb2f25baff9a63136dddce6551ea0fd20059bfce3b`) and unpacks it.
2. Applies the changes (`patch-freeling.sh`, with the four patches of `software/patches/`: the name classes, the known roots, the probability columns and the ambiguous multiwords).
3. Configures with `-DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-Wno-template-body" -DCMAKE_C_FLAGS="-std=gnu17"`, builds and installs.
4. Runs `install-data.sh`, which copies the 17 Chilean files over FreeLing's (the files and places of `freeling_escl_deploy.py --target system`: the 2027 and 19th-century data and the configs `config/es-cl.cfg` and `config/es-cl-19th-century.cfg`), removes `common/nec/cities-CL.dat`, which the Chilean `cities.dat` merges, and makes `es/locucions.dat`, FreeLing Old's multiword file, a link to `es-cl/locucions.dat`.
5. Checks that `libfreeling.so` has the name-class change (six marks).
6. Runs `bundle-libraries.sh /usr/local`: the ICU and Boost libraries FreeLing was built against are copied into `/usr/local/lib/freeling-es-cl/`, and every program and library of FreeLing finds them there first, so an upgrade of the system cannot break it.
7. Finds the distribution packages the programs and libraries need, from their shared-library dependencies, into `pkgdeps.txt`. The bundled libraries are FreeLing's own, so the package needs no ICU or Boost package; it still needs what they and FreeLing need (the C and C++ runtimes, zlib).
8. Moves everything installed into `pkgroot/`, writes `pkgetc/freeling-es-cl.conf` (`/usr/local/lib`, for `/etc/ld.so.conf.d/`) and adds the documents.

The machine needs the en_US.UTF-8 locale: FreeLing's install builds its phonetic dictionaries in it.

## Exit codes

0 built; anything else is the failing step's own code (the script stops at the first error).

## Platform

Linux: Fedora, openSUSE, the Red Hat family (the generic tarball is built on AlmaLinux 9), Debian, Ubuntu, Arch Linux. bash, CMake, a C++ compiler, Boost, ICU, zlib, patch, patchelf, file, binutils (readelf, strings), and rpm, dpkg or pacman.

## Changelog

- 1.4.0 (261126): `PREFIX` and `RELOCATABLE` (the generic Linux tarball); the packages of the libraries found with pacman too (Arch Linux). FreeLing carries its own copies of the ICU and Boost libraries it was built against (`bundle-libraries.sh` 1.0.0), so the package no longer depends on the distribution's ICU and Boost and an upgrade of the system cannot break it; the libraries in `/usr/local/lib/freeling-es-cl/` count as FreeLing's own when the dependencies are found.
- 1.3.0 (261119): passes the tag-probabilities and the ambiguous-multiwords patches (`software/patches/freeling-4.2-tag-probabilities.patch`, `software/patches/freeling-4.2-ambiguous-multiwords.patch`) to `patch-freeling.sh` 1.5.0.
- 1.2.0 (261116): passes the known-roots patch (`software/patches/freeling-4.2-known-roots.patch`) to `patch-freeling.sh` 1.3.0.
- 1.1.0 (261113): the Chilean data are installed by `install-data.sh` (shared with the macOS build): the 19th-century dictionary's probabilities and multiwords and the two configs too, and `es/locucions.dat` linked to the Chilean multiword file for FreeLing Old; only Spanish is built (`patch-freeling.sh` 1.1.0).
- 1.0.0 (261112): first version.
