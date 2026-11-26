# freeling_escl_deploy_README.md

Documents `freeling_escl_deploy.py` 2.9.0.

Real file: `/path/to/project/derived-software/FreeLing_es-CL_2027/tools/freeling_escl_deploy.py`

## Purpose

Puts a FreeLing es-CL 2027 build, made by `freeling_escl_build.py`, where it
is used. The release must be intact: every file must match its
`SHA256SUMS`, or the run is refused.

| Target | Run as | Replaces |
|---|---|---|
| `user` | your own user, not root | the Chilean grammatical lists, `/path/to/project/derived-software/FreeLing_es-CL_2027/data/grammatical-lists/freeling-cl/CL.*.GRAM.txt`; the FreeLing build tree, `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/es-cl/` (`dictionary/entries/CL.*`, `remove/CL.removed`, `probabilitats.dat`, `locucions.dat`, `tagset.dat`) |
| `system` | the owner of the installed data: your own user for the FreeLing of the product folder (sudo only for one in a system folder, given with `--share`) | the installed data FreeLing reads, in `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling/`: `es/es-cl/dicc.src` (the default dictionary), `es/es-cl/informal/dicc.src` (the informal one: the default with the spoken -ao, -á and -ío forms, for informal writing only, decided 261116), `es/es-cl/19th-century/dicc.src` (the 19th-century one, for 19th-century texts) with its `19th-century/probabilitats.dat` and `19th-century/locucions.dat`, `es/es-cl/np.dat` (the name recognizer, written texts), `es/es-cl/np-speech.dat` (the name recognizer, transcribed speech), `es/es-cl/probabilitats.dat`, `locucions.dat`, `tagset.dat`, `quantities.dat`, `usermap-informal.dat` (the readings for informal writing only, the source of the informal user map), `stand-ins.tsv` (the stand-in tokens and their tags, read by the tagger), `usermap/es-cl.dat`, `usermap/es-cl-informal.dat`, `usermap/es-cl-speech.dat`, `usermap/es-cl-19th-century.dat` (the user map of each config); the configs `config/es-cl.cfg` (modern writing, the default), `config/es-cl-informal.cfg` (informal modern writing), `config/es-cl-speech.cfg` (transcribed speech), `config/es-cl-19th-century.cfg` (19th-century writing) and `config/es-cl-conll-columns.cfg` (the CoNLL columns they name); the name classifier's lists `common/nec/cities.dat`, `es/nerc/data/gazLOC-c.dat`, `gazPER-c.dat`, `gazPER-p.dat`; the classifier's file `es/nerc/nec/nec-ab-poor1.dat` (FreeLing's, with the class shares of some names); the affix rules `es/afixos.dat` (FreeLing's, with the clitic rules restricted, decided 261116: te only after an infinitive, a gerund or a tú imperative, os only after an infinitive or a gerund or by FreeLing's vosotros rules, never te twice or te with os; every Spanish config reads it, FreeLing Old's excepted, which has its own). |

Only files whose content differs are replaced. The file replaced is first
moved to a `deprecated/` folder beside it, named
`<name>.DEPRECATED-YYMMDD[letter]<extension>`. The copies of the entries and
remove files go to the folder above (`dictionary/deprecated/`,
`deprecated/`), because FreeLing's build reads those folders whole.

In the installed data (`--target system`) the replaced file is also
compressed (`.xz`) and made unreadable (mode 000), so FreeLing can never
read it (decided 261109). Nothing is ever deleted.

The system target also retires the FreeLing files the Chilean ones replace
(decided 261110d), when present, the same way (into `deprecated/` beside
them, compressed, mode 000):

| File | Why |
|---|---|
| `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling/common/nec/cities-CL.dat` | FreeLing's Chilean city list, which nothing read: merged into `cities.dat` |
| `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling/es/nerc/data/gazPER-p.dat.upstream` | FreeLing's own person-name parts, kept there on 291026: replaced by the Chilean list |
| `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling/es/es-cl/historical/dicc.src`, `probabilitats.dat`, `locucions.dat` | the 19th-century files' former folder: the files are installed in `es/es-cl/19th-century/` since 2.6.0 (decided 261119) |
| `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling/es/locucions.dat` | FreeLing's general multiword file, read only by FreeLing Old (`config/es-old.cfg`): replaced by a relative link to `es-cl/locucions.dat`, the Chilean file, which has FreeLing's general multiwords merged in (decided 261113: FreeLing Old's own folder stays as FreeLing ships it, and its config is unchanged) |

The user target retires the build tree's `dictionary/entries/CL.misspellings` (into `dictionary/deprecated/`, not compressed): the build writes `CL.common-misspellings` in its place, and FreeLing's build reads the entries folder whole. For the same reason it retires `dictionary/entries/CL.reduced-forms`: the reduced forms belong to the informal dictionary only, and their entries file is in the release's `informal/dictionary/entries/`, which is not deployed to the build tree.

The build tree's copies of these FreeLing files (`/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/common/nec/`,
`data/es/nerc/data/`) are not touched: the build reads them, and checks
them against FreeLing 4.2. **`make install` in the FreeLing build tree
reinstalls them over the Chilean ones**; after it, run the system target
again.

Every target file is checked before anything is moved: an immutable
(`chattr +i`) or read-only file refuses the whole run and prints the command
that clears it.

**The library comes first.** The system target refuses to run unless the
installed FreeLing library, `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/lib/libfreeling.so` (or `--lib`),
has the name-class change of `software/patches/`. FreeLing 4.2 without it
stops with an error on the classifier file's `<ClassShares>` section, so
deploying the files before the library would break every Spanish analysis
on the machine. The check looks in the library for what only the changed
one holds: the names of the five sections it reads (`DictionaryClasses`,
`FixedClasses`, `ClassesAtSentenceStart`, `SentenceStartClasses`,
`ClassShares`) and the `keep:` option of `SentenceStartClasses`. A library
with an earlier state of the change is refused too: it would drop the verb
readings of Catar, Irán, Tomé, Quito and Pinto at the start of a sentence. Build
and install the library as `software/patches/freeling-4.2-np-classes_README.md`
says, then deploy.

## Usage

```bash
freeling_escl_deploy.py --target user --dry-run
freeling_escl_deploy.py --target user
sudo /path/to/project/derived-software/FreeLing_es-CL_2027/tools/freeling_escl_deploy.py --target system --dry-run
sudo /path/to/project/derived-software/FreeLing_es-CL_2027/tools/freeling_escl_deploy.py --target system
```

Since 2.6.0 the system target installs the release's configs themselves
(decided 261119): the configs everything is tagged with are the ones in the
release. No config needs writing after the deployment
(`the former config writer` is retired).

| Option | Default |
|---|---|
| `--target` | required: `user` or `system` |
| `--release` | `/path/to/FreeLing-es_CL-2027` |
| `--root` | the project root, found from the script's location by `PROJECT_ROOT.txt` |
| `--build-tree` | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/FreeLing-4.2/data/es/es-cl` |
| `--share` | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/share/freeling` (FreeLing's installed data) |
| `--lib` | `/path/to/project/derived-software/FreeLing_es-CL_2027/third-party/freeling/lib/libfreeling.so` (the library the system target checks) |
| `--dry-run` | list what would change, change nothing |

## Exit codes

0 done (or nothing to do), 2 refused (nothing moved or written), 130
interrupted.

## Platform

Linux. Standard library only.

## Tested

261116, version 2.5.0, with the release of `freeling_escl_build.py` 2.14.0 (built on the test tree): the system target, on an empty copy of the share folders and a library with the name-class change, installed 18 files, `es/es-cl/informal/dicc.src` among them, equal to the release's, and made the link for FreeLing Old; the release of 2.13.0 was refused (no informal dictionary). The user target, run as a non-root user on a build tree holding the `CL.reduced-forms` of 2.13.0, installed the lists and entries and retired `CL.reduced-forms` to `dictionary/deprecated/CL.reduced-forms.DEPRECATED-261116`.

261116, version 2.4.0, on a copy of FreeLing's installed data with the release of `freeling_escl_build.py` 2.11.0 and the library with the name-class and known-roots changes: the dry run listed `es/afixos.dat` as the one file to replace and changed nothing; the real run replaced it, FreeLing's file kept as `es/deprecated/afixos.DEPRECATED-261116.dat.xz` (compressed, mode 000); a second run found the 17 files current and nothing to do. A release of 2.10.0 (no `afixos.dat`) was refused. FreeLing with the installed file read cómetelo as come + te + lo and sáltetelo as one unknown word.

261115, version 2.3.0, on a copy of FreeLing's installed data (`es/es-cl`, `common/nec`, `es/nerc`, `config`) with the release of `freeling_escl_build.py` 2.9.0 and the library with the name-class change: the dry run listed the files to replace, `usermap-informal.dat` as new and the two configs to retire, and changed nothing; the real run replaced 8 files, added `usermap-informal.dat` and retired the configs; a second run found the 16 files current and nothing to do.

261113, version 2.2.1, on a copy of the data deployed by 2.2.0 (with `config/es-cl.cfg` and `config/es-cl-19th-century.cfg`) and the release of `freeling_escl_build.py` 2.8.1: the dry run found the 15 data files current and listed the 2 configs to retire, changing nothing; the real run retired both into `config/deprecated/` (compressed, mode 000), leaving `es-old.cfg` and FreeLing's other configs; a second run found nothing to do.

261113, version 2.2.0, on a copy of FreeLing 4.2's own data (`es/es-cl`, `es/locucions.dat`, `common/nec`, `es/nerc`, `config`) with the release of `freeling_escl_build.py` 2.8.0 and the library with the name-class change: the dry run listed 17 files (8 to replace, 9 new) and 2 to retire (`cities-CL.dat` and `es/locucions.dat`) and the link; the real run replaced, added and retired them (each copy compressed and mode 000; FreeLing's `es-cl.cfg` as `config/deprecated/es-cl.DEPRECATED-YYMMDD.cfg.xz`) and made `es/locucions.dat` a link to `es-cl/locucions.dat`; a second run found nothing to do. FreeLing Old (`es-old.cfg`) then analyzed Old Spanish as before (dixo decir, muger mujer).

261110, on a copy of FreeLing 4.2's own data with an earlier es-CL
deployment in `es/es-cl/`: with a library holding none of the marks, and
with a library of the earlier state of the change (no `keep:`), the system
target refused and changed nothing; with no library at the path given, it
refused. With
the changed library the dry run listed the 13 files (8 to replace, 3 new:
`historical/dicc.src`, `np-speech.dat`, `quantities.dat`) and the 2 files to
retire, and changed nothing; the real run replaced, added and retired them,
each copy in `deprecated/` compressed and mode 000, and every installed file
equal to the release's; a second run found nothing to do. The user target
refuses to run with sudo.

## Changelog

- 2.9.0 (261121): the installed data is `third-party/freeling/share/freeling/` in the product folder, the library `third-party/freeling/lib/libfreeling.so`, the source tree's Chilean data `third-party/FreeLing-4.2/data/es/es-cl/` (FreeLing 4.2 is installed inside the product folder (decided 261121)); `--share`, `--lib` and `--build-tree` default to them, found from the project root. `--target system` is run by the owner of the installed data, so without sudo for the product's own FreeLing; run with sudo there, it refuses, so that no file becomes root's.
- 2.8.0 (261121): `--release` defaults to `dist/FreeLing-es_CL-2027/` in the product folder, found from the project root (moved into the product folder `derived-software/FreeLing_es-CL_2027/` (decided 261121)); the lists are in `data/grammatical-lists/freeling-cl/`. `--target user` also writes each list's raw copy, `source-files/CL.*.txt`, with the list, so the tools that read the raw copies (`grammar_extract_freeling.py`, the dictionary's importers) never see an older state than the build's.
- 2.7.0 (261119): the release folder is `FreeLing-es_CL-2027` (was `FreeLing_es-CL_2027`), the name of the GitHub repository (decided 261119); `--release` defaults to it. Nothing else changes.
- 2.6.0 (261119): the system target installs the configs of the release (`config/es-cl.cfg`, `es-cl-informal.cfg`, `es-cl-speech.cfg`, `es-cl-19th-century.cfg`, `es-cl-conll-columns.cfg`), their user maps (`es/es-cl/usermap/*.dat`) and `es/es-cl/stand-ins.tsv` (`freeling_escl_build.py` 2.16.0, decided 261119), instead of retiring `config/es-cl.cfg` and `config/es-cl-19th-century.cfg`; the 19th-century files go to `es/es-cl/19th-century/` and their former folder's files (`es/es-cl/historical/`) are retired; a release that lacks any file to install is refused, each file named.
- 2.5.0 (261116): the system target also installs `es/es-cl/informal/dicc.src`, the informal dictionary (`freeling_escl_build.py` 2.14.0, decided 261116); a release without it or without `data/config/es-cl-informal.cfg` is refused, as made by an older build; the user target retires the build tree's `dictionary/entries/CL.reduced-forms`.
- 2.4.0 (261116): the system target also installs `es/afixos.dat`, FreeLing's affix rules with the clitic rules restricted (`freeling_escl_build.py` 2.11.0, decided 261116); a release without it is refused, as made by an older build.

- 2.3.0 (261115): the system target also installs `es/es-cl/usermap-informal.dat`, the readings for informal writing only (`freeling_escl_build.py` 2.9.0), which `the former config writer` 1.3.0 puts into the user map of the written corpus's informal config; a release without it is refused, as made by an older build.

- 2.2.2 (261113): the user target's messages and this README name no account: "your own user" (the release is public, and the account name is private).

- 2.2.1 (261113): the system target no longer installs `config/es-cl.cfg` and `config/es-cl-19th-century.cfg`, and retires both from `/usr/local/share/freeling/config/` (compressed, mode 000): the corpus project tags only with `the former base config` and the configs written from it (decided 261113). The release's two configs stay in its `data/config/` and in the packages.

- 2.2.0 (261113): the system target also installs the 19th-century dictionary's `historical/probabilitats.dat` and `historical/locucions.dat` and the configs `config/es-cl.cfg` and `config/es-cl-19th-century.cfg`, and makes `es/locucions.dat` (FreeLing Old's multiword file) a link to `es-cl/locucions.dat`, retiring FreeLing's file; the user target retires `dictionary/entries/CL.misspellings`, now `CL.common-misspellings`; `.cfg` is a known extension for deprecated names; refuses a release without the 19th-century files.

- 2.1.0 (261110): the system target installs `np-speech.dat`, the
  name classifier's lists (`common/nec/cities.dat`,
  `es/nerc/data/gazLOC-c.dat`, `gazPER-c.dat`, `gazPER-p.dat`) and its file
  `es/nerc/nec/nec-ab-poor1.dat`, and retires `common/nec/cities-CL.dat`
  and `es/nerc/data/gazPER-p.dat.upstream`; it refuses unless the installed
  library has the name-class change (`--lib`); `--share` (FreeLing's
  installed data) replaces `--system`; refuses a release without
  `np-speech.dat` or `nec-ab-poor1.dat`.
- 2.0.0 (261110): installs the historical dictionary and `quantities.dat`;
  the user target installs FreeLing's remove file; in the installed data the
  replaced files are compressed and made unreadable; refuses a release
  without the historical dictionary.
- 1.1.0 (261101): the system target also installs `np.dat`.
- 1.0.0 (261101): first version.
