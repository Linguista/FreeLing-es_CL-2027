# freeling_escl_deploy_README.md

Documents `freeling_escl_deploy.py` 2.1.0.

Real file: `/home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_deploy.py`

## Purpose

Puts a FreeLing es-CL 2027 build, made by `freeling_escl_build.py`, where it
is used. The release must be intact: every file must match its
`SHA256SUMS`, or the run is refused.

| Target | Run as | Replaces |
|---|---|---|
| `user` | usuario | the CSLD grammatical lists, `/home/user/csld/linguistic-derived/grammatical-lists/individual/contemporary/freeling-cl/CL.*.GRAM.txt`; the FreeLing build tree, `/home/user/build/FreeLing-4.2/data/es/es-cl/` (`dictionary/entries/CL.*`, `remove/CL.removed`, `probabilitats.dat`, `locucions.dat`, `tagset.dat`) |
| `system` | sudo | the installed data FreeLing reads, in `/usr/local/share/freeling/`: `es/es-cl/dicc.src` (the default dictionary), `es/es-cl/historical/dicc.src` (the historical one), `es/es-cl/np.dat` (the name recognizer, written texts), `es/es-cl/np-speech.dat` (the name recognizer, transcribed speech), `es/es-cl/probabilitats.dat`, `locucions.dat`, `tagset.dat`, `quantities.dat`; the name classifier's lists `common/nec/cities.dat`, `es/nerc/data/gazLOC-c.dat`, `gazPER-c.dat`, `gazPER-p.dat`; the classifier's file `es/nerc/nec/nec-ab-poor1.dat` (FreeLing's, with the class shares of some names) |

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
