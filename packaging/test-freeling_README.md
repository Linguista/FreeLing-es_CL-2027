# test-freeling_README.md

Documents `test-freeling.sh` 1.7.0.

## Purpose

Checks an installed FreeLing es-CL 2027 package: the library (`libfreeling.so`, `libfreeling.dylib` on macOS, `libfreeling.dll` on Windows) has the name-class change, the probability columns (`LEX_PROB`, `TAG_PROB`) and the ambiguous-multiwords change (every token of "Bueno, yo creo que es bueno." has both probabilities; `a_ver` is marked `A`, "Voy a ver la película." gives a + ver and "A ver, dime qué pasó." keeps a_ver); the 20 Chilean files are this release's (`es/afixos.dat`, `es/es-cl/informal/dicc.src` and `config/es-cl-informal.cfg` among them) (their sha256 as in `SHA256SUMS`); `cities-CL.dat` is gone; `es/locucions.dat` is a link to `es-cl/locucions.dat` (on Windows, a copy of it); no English, Portuguese or Argentine data is installed; FreeLing analyzes "Cachái que mi vecina, la Javi, no está ni ahí con voh, conchetumare. Dice que soi cuartero y que no te bañai nunca." with `es-cl.cfg` (cachái, soi and bañai are voseo forms, `VMIP2SV` and `VSIP2SV`; voh is vos, `PP2CS0V`; no está ni ahí is the multiword no_estar_ni_ahí and conchetumare the interjection concha_de_tu_madre), "Él llegó a Ñuñoa." with `es-cl.cfg` (a capital other than A to Z is lowercased: Él has the lemma él, Ñuñoa ñuñoa), "Me dio risa reírme." with `es-cl.cfg` (reírme split into reír + me: the known-roots change of the affix analysis, since 1.3.0), "Sáltetelo." with `es-cl.cfg` (not read as sal + te + te + lo, lemma salir: the clitic rules of `es/afixos.dat`, decided 261116), "Estoy cansá." with `es-cl-informal.cfg` (cansá cansar VMP00SF: the informal dictionary) and with `es-cl.cfg` (not cansar VMP00SF: the reduced forms are for informal writing only, decided 261116), "La jente i el rei." with `es-cl-19th-century.cfg` (jente is gente, i is y) and "Et dixo el rey." with `es-old.cfg` (dixo is decir). It prints FreeLing's output.

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

261119, version 1.7.0, run against FreeLing 4.2 built with the four changes (name classes, known roots, tag probabilities, ambiguous multiwords; GCC 13) and the release of `freeling_escl_build.py` 2.18.0 (built on the test tree) installed by `install-data.sh` into another prefix: ALL CHECKS PASSED. "Voy a ver la película." gave a a SP and ver ver VMN0000, "A ver, dime qué pasó." A_ver a_ver I, and every token of "Bueno, yo creo que es bueno." had a `LEX_PROB` and a `TAG_PROB` from 0 to 1. Not yet run by GitHub's workflow.

261116, version 1.5.0, its new check run by hand against FreeLing 4.2 with the name-class and known-roots changes and the release of `freeling_escl_build.py` 2.14.0 (built on the test tree): "Estoy cansá." gave cansá cansar VMP00SF with the informal dictionary and cansá VMIF3S0 (guessed) with the default one. Not yet run by GitHub's workflow.

261116, version 1.4.0, its two new checks run by hand against FreeLing 4.2 with the name-class and known-roots changes and the release of `freeling_escl_build.py` 2.11.0: the 18 files of a data folder installed by `install-data.sh` 1.2.0 matched `SHA256SUMS`; "Sáltetelo." gave one unknown word with FreeLing's clitic rules restricted and salir+te+te+lo with FreeLing's own `afixos.dat`. Not yet run by GitHub's workflow.

261113, version 1.1.0, against FreeLing 4.2 built with `patch-freeling.sh` 1.1.0 and the release of `freeling_escl_build.py` 2.8.0 installed (the prefix changed for the test): ALL CHECKS PASSED.

261113, version 1.2.0: GitHub Actions run 43379595248 (branch windows-package-test, 261113): all 14 jobs passed. ALL CHECKS PASSED on Fedora 43 and 44, Debian 13, Ubuntu 24.04 and 26.04, macOS 15 (Apple silicon and Intel) and Windows; on every one "Él llegó a Ñuñoa." gave Él él PP3MS00 and Ñuñoa ñuñoa NP00G00. The lowercasing check failed on the Windows build before fix 9f, as it should.

261113, version 1.2.0 with the two Chilean sentences: GitHub Actions run 43388088727 (branch windows-package-test, 261113): all 14 jobs passed. In every run of this script (the five Linux tests on clean systems, both macOS builds and the Windows build) the six patterns of "Cachái que mi vecina, la Javi, no está ni ahí con voh, conchetumare. Dice que soi cuartero y que no te bañai nunca." matched, among them Cachái cachar VMIP2SV and bañai bañar VMIP2SV, and so did the case-sensitive check of the Windows zip from PowerShell.

## Changelog

- 1.7.0 (261119): the library must have the probability columns and the ambiguous-multiwords change; every token of "Bueno, yo creo que es bueno." must have a `LEX_PROB` and a `TAG_PROB` from 0 to 1 (a CoNLL columns file written for the check); `a_ver` must be marked `A` in `es/es-cl/locucions.dat`, "Voy a ver la película." must give a + ver and "A ver, dime qué pasó." must keep a_ver.
- 1.6.0 (261119): the 27 files of `freeling_escl_build.py` 2.16.0 (the 19th-century files in `es/es-cl/19th-century/`, the speech config, the CoNLL columns file, the four user maps, `stand-ins.tsv`); every analysis asks for `--output freeling`, since the configs now write CoNLL; the speech config must read nn as the hesitation and xxxredactedxxx as Fz; compound analysis must be off in every config, FreeLing Old's `es-old.cfg` included.
- 1.5.0 (261116): the informal dictionary and its config are checked with the other Chilean files (20); "Estoy cansá." must give cansar VMP00SF with `es-cl-informal.cfg` and must not with `es-cl.cfg` (decided 261116).
- 1.4.0 (261116): `es/afixos.dat` is checked with the other Chilean files (18); "Sáltetelo." must not be read as sal + te + te + lo (salir): the clitic rules of `afixos.dat` (decided 261116).
- 1.3.0 (261116): checks that FreeLing reads "Me dio risa reírme." as reír + me (`reír reír VMN0000`, `me me PP1CS00`): the known-roots change of the affix analysis; without it FreeLing gives the form reir.
- 1.2.0 (261113): the Chilean check on two real Chilean sentences (cachái, voh, no está ni ahí, conchetumare, soi, bañai) in place of one short sentence (user, 261113); the lowercasing check (Él, Ñuñoa), which found the Windows build leaving Ñ and accented capitals uncased; Windows: `libfreeling.dll`, its 16-bit wide strings, `analyzer.exe` run with `FREELINGSHARE` set, and `es/locucions.dat` a copy of `es-cl/locucions.dat`.
- 1.1.0 (261113): the 19th-century files and the two configs among the files checked; the link for FreeLing Old; only Spanish installed; the 19th-century and FreeLing Old analyses; `PREFIX` for another install prefix, and `libfreeling.dylib` (macOS).
- 1.0.0 (261112): first version.
