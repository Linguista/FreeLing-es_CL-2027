# freeling_escl_deploy_README.md

Documents `freeling_escl_deploy.py` 2.2.1.

Real file: `/home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_deploy.py`

## Purpose

Puts a FreeLing es-CL 2027 build, made by `freeling_escl_build.py`, where it
is used. The release must be intact: every file must match its
`SHA256SUMS`, or the run is refused.

| Target | Run as | Replaces |
|---|---|---|
| `user` | usuario | the CSLD grammatical lists, `/home/user/csld/linguistic-derived/grammatical-lists/individual/contemporary/freeling-cl/CL.*.GRAM.txt`; the FreeLing build tree, `/home/user/build/FreeLing-4.2/data/es/es-cl/` (`dictionary/entries/CL.*`, `remove/CL.removed`, `probabilitats.dat`, `locucions.dat`, `tagset.dat`) |
| `system` | sudo | the installed data FreeLing reads, in `/usr/local/share/freeling/`: `es/es-cl/dicc.src` (the default dictionary), `es/es-cl/historical/dicc.src` (the 19th-century one, for historical corpora) with its `historical/probabilitats.dat` and `historical/locucions.dat`, `es/es-cl/np.dat` (the name recognizer, written texts), `es/es-cl/np-speech.dat` (the name recognizer, transcribed speech), `es/es-cl/probabilitats.dat`, `locucions.dat`, `tagset.dat`, `quantities.dat`; the name classifier's lists `common/nec/cities.dat`, `es/nerc/data/gazLOC-c.dat`, `gazPER-c.dat`, `gazPER-p.dat`; the classifier's file `es/nerc/nec/nec-ab-poor1.dat` (FreeLing's, with the class shares of some names). No config: see below |

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
| `/usr/local/share/freeling/common/nec/cities-CL.dat` | FreeLing's Chilean city list, which nothing read: merged into `cities.dat` |
| `/usr/local/share/freeling/es/nerc/data/gazPER-p.dat.upstream` | FreeLing's own person-name parts, kept there on 291026: replaced by the Chilean list |
| `/usr/local/share/freeling/config/es-cl.cfg` | FreeLing's es-cl config, put there by FreeLing's own install: the CSLD tags only with `csld-es-cl.cfg` and the configs `freeling_csld_configs.py` writes from it, so no other es-cl config is kept where it could be used by mistake (decided 261113) |
| `/usr/local/share/freeling/config/es-cl-19th-century.cfg` | the same, if a deployment put it there |
| `/usr/local/share/freeling/es/locucions.dat` | FreeLing's general multiword file, read only by FreeLing Old (`config/es-old.cfg`): replaced by a relative link to `es-cl/locucions.dat`, the Chilean file, which has FreeLing's general multiwords merged in (decided 261113: FreeLing Old's own folder stays as FreeLing ships it, and its config is unchanged) |

The user target retires the build tree's `dictionary/entries/CL.misspellings` (into `dictionary/deprecated/`, not compressed): the build writes `CL.common-misspellings` in its place, and FreeLing's build reads the entries folder whole.

The build tree's copies of these FreeLing files (`/home/user/build/FreeLing-4.2/data/common/nec/`,
`data/es/nerc/data/`) are not touched: the build reads them, and checks
them against FreeLing 4.2. **`make install` in the FreeLing build tree
reinstalls them over the Chilean ones**; after it, run the system target
again.

Every target file is checked before anything is moved: an immutable
(`chattr +i`) or read-only file refuses the whole run and prints the command
that clears it.

**The library comes first.** The system target refuses to run unless the
installed FreeLing library, `/usr/local/lib/libfreeling.so` (or `--lib`),
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
sudo /home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_deploy.py --target system --dry-run
sudo /home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_deploy.py --target system
freeling_csld_configs.py
```

After the system deployment, `freeling_csld_configs.py` writes the configs
that use the new data.

| Option | Default |
|---|---|
| `--target` | required: `user` or `system` |
| `--release` | `/home/user/FreeLing_es-CL_2027` |
| `--root` | the project root, found from the script's location by `PROJECT_ROOT.txt` |
| `--build-tree` | `/home/user/build/FreeLing-4.2/data/es/es-cl` |
| `--share` | `/usr/local/share/freeling` (FreeLing's installed data) |
| `--lib` | `/usr/local/lib/libfreeling.so` (the library the system target checks) |
| `--dry-run` | list what would change, change nothing |

## Exit codes

0 done (or nothing to do), 2 refused (nothing moved or written), 130
interrupted.

## Platform

Linux. Standard library only.

## Tested

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

- 2.2.1 (261113): the system target no longer installs `config/es-cl.cfg` and `config/es-cl-19th-century.cfg`, and retires both from `/usr/local/share/freeling/config/` (compressed, mode 000): the CSLD tags only with `csld-es-cl.cfg` and the configs written from it (decided 261113). The release's two configs stay in its `data/config/` and in the packages.

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
