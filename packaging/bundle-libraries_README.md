# bundle-libraries_README.md

Documents `bundle-libraries.sh` 1.0.0.

## Purpose

Makes an installed FreeLing carry its own copies of the ICU and Boost libraries it was built against, so that a later upgrade of the system cannot break it: Fedora 44 to 45 replaces ICU 77 with ICU 78, a Homebrew upgrade of icu4c or boost replaces them on macOS, and a FreeLing linked against the system's copies then stops loading. With its own copies it keeps working, whatever the system's versions become.

- The libraries go into `PREFIX/lib/freeling-es-cl/`, under the names FreeLing asks for (`libicuuc.so.77`, `libboost_regex.so.1.90.0`; `libicuuc.78.dylib` on macOS), with every ICU and Boost library they need in turn.
- Linux: every program and library of FreeLing (the ELF files in `PREFIX/bin` and `PREFIX/lib`) gets the run path `PREFIX/lib/freeling-es-cl:PREFIX/lib` (patchelf), and each copy the run path `$ORIGIN`, so FreeLing finds its copies first. The folder is not in the system's library path, so no other program sees them. With `RELOCATABLE=yes` the run paths are relative to each file (`$ORIGIN/../lib/freeling-es-cl:$ORIGIN/../lib` for the programs, `$ORIGIN/freeling-es-cl:$ORIGIN` for the libraries), so the whole folder can be moved: the generic Linux tarball, which is unpacked anywhere.
- macOS: every reference to a Homebrew ICU or Boost library, in FreeLing's programs and libraries and in the copies, is changed to the copy's full path (`install_name_tool`), and every changed file is signed again, ad hoc (`codesign --sign -`), which Apple silicon requires.
- Where a distribution ships ICU's data as a separate file and `libicudata` as an empty stub (openSUSE: `/usr/share/icu/VERSION/icudtNNl.dat`), the stub alone would leave FreeLing without ICU's data once that file's package is gone ("Could not initialize ICU resources"). The copy of `libicudata` is then made, as ICU's own build makes it, from the data file: a library whose symbol `icudtNN_dat` holds the whole file (gcc, `.incbin`).
- Every other library stays the system's: the C and C++ runtimes and zlib, which a newer system keeps compatible.
- `PREFIX/share/doc/freeling-es-cl/BUNDLED-LIBRARIES.tsv` lists each copy: its name, the file it came from, the package (Homebrew formula on macOS), its version and the copy's sha256. The license files of those packages are copied into `PREFIX/share/doc/freeling-es-cl/licenses/` (ICU's license asks for its notice to go with every copy). A missing license file never stops it: for Boost (Homebrew's keg has none) it writes the Boost Software License's text, and for anything else a note saying where the license is, with a warning.
- At the end it checks that every ICU and Boost library that FreeLing and the copies load comes from the copies, and stops if one does not.

Windows needs none of this: the Windows zip already carries every library it needs in its `bin` folder.

The copies may be older than the system's own ICU and Boost. FreeLing uses its copies; putting the system's in their place may break it, and ICU's fixes reach the copies only with a new release of FreeLing es-CL 2027.

## Usage

After FreeLing and the Chilean data are installed, before the package or tarball is made:

```bash
packaging/bundle-libraries.sh /usr/local
packaging/bundle-libraries.sh /usr/local/freeling-es-cl-2027
```

`build-freeling.sh` runs it for the Linux packages, and the macOS job of `.github/workflows/packages.yml` for the tarballs. The argument is the install prefix; its `bin` and `lib` folders must hold FreeLing's programs and libraries and nothing else.

## Exit codes

0 the libraries are bundled (it prints the list); 1 something could not be done (it says what): no program or library in the prefix, no ICU or Boost library needed, a library not found, an empty `libicudata` stub with no data file to fill it, or a library still loaded from outside the copies.

## Platform

Linux (bash, patchelf, binutils' readelf, ldd, ldconfig, file, gcc where ICU's data is a separate file, and rpm, dpkg or pacman) and macOS (bash 3.2 or later, otool, install_name_tool, codesign, file, Homebrew). Not Windows.

## Tested

261126, version 1.0.0, on Ubuntu 24.04, on a copy of the programs and libraries of the release 261126c's Ubuntu 24.04 package: five libraries copied (ICU 74's three and two of Boost 1.83, 36 MB); `ldd` showed every one loading from the copies; with `RELOCATABLE=yes`, the folder moved elsewhere and the installed `libfreeling.so` hidden as well, FreeLing ran from the moved folder; a `libicudata` built from ICU 74's data file (taken out of Ubuntu's own `libicudata`) in place of the copy lowercased Él and Ñuñoa with the system's ICU hidden; with the system's ICU and Boost files hidden (bind-mounted over by an empty file), FreeLing tagged "Vos tenís que venir." correctly from the copies, while the installed package, unbundled, stopped: "libboost_program_options.so.1.83.0: file too short". The Linux packages and the macOS tarballs are checked by the GitHub workflow.

## Changelog

- 1.0.0 (261126): first version: Linux (rpm, dpkg, pacman) and macOS; `RELOCATABLE=yes`; an empty `libicudata` stub filled from ICU's data file (openSUSE); a missing license file never stops it.
