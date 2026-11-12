# build-freeling_README.md

Documents `build-freeling.sh` 1.0.0.

## Purpose

Builds FreeLing 4.2 with the changes of FreeLing es-CL 2027 (`patch-freeling.sh`), installs it in `/usr/local` with this repository's Chilean data in place of FreeLing's own files, and leaves everything installed ready for packaging. It is what the GitHub workflow `.github/workflows/packages.yml` runs on each distribution.

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

## What it does

1. Checks the tarball's sha256 (`f96afbdb000d7375426644fb2f25baff9a63136dddce6551ea0fd20059bfce3b`) and unpacks it.
2. Applies the changes (`patch-freeling.sh`).
3. Configures with `-DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-Wno-template-body" -DCMAKE_C_FLAGS="-std=gnu17"`, builds and installs.
4. Copies the 13 Chilean data files over FreeLing's (the files and places of `freeling_escl_deploy.py --target system`) and removes `common/nec/cities-CL.dat`, which the Chilean `cities.dat` merges.
5. Checks that `libfreeling.so` has the name-class change (six marks).
6. Finds the distribution packages the programs and libraries need, from their shared-library dependencies, into `pkgdeps.txt`.
7. Moves everything installed into `pkgroot/`, writes `pkgetc/freeling-es-cl.conf` (`/usr/local/lib`, for `/etc/ld.so.conf.d/`) and adds the documents.

The machine needs the en_US.UTF-8 locale: FreeLing's install builds its phonetic dictionaries in it.

## Exit codes

0 built; anything else is the failing step's own code (the script stops at the first error).

## Platform

Linux. bash, CMake, a C++ compiler, Boost, ICU, zlib, patch, file, binutils (readelf, strings), rpm or dpkg.
