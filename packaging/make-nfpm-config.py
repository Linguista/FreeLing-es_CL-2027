#!/usr/bin/env python3
# VERSION 1.0.0
#
# make-nfpm-config.py -- writes the nfpm configuration of the FreeLing
# es-CL 2027 package from what build-freeling.sh left in the repository
# root: pkgroot/ (the files), pkgetc/ (the library path for ld.so.conf.d)
# and pkgdeps.txt (the distribution packages it needs).
#
# Usage, from the repository root:
#   packaging/make-nfpm-config.py RELEASE > nfpm-run.yaml
# RELEASE is the package release, distribution included (1.fc44,
# 1~debian13, 1~ubuntu24.04), so that the packages of each distribution
# have names of their own.
#
# Every file and folder FreeLing installs is listed under the folders it
# goes into (/usr/local/bin, /usr/local/lib ...), so the package owns its
# own files and folders, never /usr/local or its standard folders.

import json
import sys
from pathlib import Path

VERSION = "1.0.0"
PREFIX = "usr/local"
# Standard folders that other packages also put files in: the package owns
# only what it puts inside them.
SHARED = {"doc", "man", "info", "pkgconfig", "cmake", "applications"}


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: make-nfpm-config.py RELEASE")
    release = sys.argv[1]
    root = Path("pkgroot")
    deps = [l.strip() for l in Path("pkgdeps.txt").read_text().splitlines() if l.strip()]
    contents = []

    def add(folder):
        for entry in sorted(folder.iterdir()):
            dst = "/" + str(entry.relative_to(root))
            if entry.is_dir() and not entry.is_symlink():
                if entry.name in SHARED:
                    add(entry)
                else:
                    contents.append({"src": "./" + str(entry), "dst": dst, "type": "tree"})
            elif entry.is_symlink():
                contents.append({"src": str(entry.readlink()), "dst": dst, "type": "symlink"})
            else:
                contents.append({"src": "./" + str(entry), "dst": dst})

    for top in sorted((root / PREFIX).iterdir()):
        add(top)
    contents.append({"src": "./pkgetc/freeling-es-cl.conf",
                     "dst": "/etc/ld.so.conf.d/freeling-es-cl.conf",
                     "type": "config", "file_info": {"mode": 0o644}})
    conf = {
        "name": "freeling-es-cl",
        "arch": "amd64",
        "platform": "linux",
        "version": "4.2",
        "release": release,
        "section": "science",
        "priority": "optional",
        "maintainer": "Scott Sadowsky <Linguista@users.noreply.github.com>",
        "vendor": "Scott Sadowsky",
        "homepage": "https://github.com/Linguista/FreeLing-es_CL-2027",
        "license": "AGPL-3.0-or-later",
        "description": (
            "FreeLing 4.2 with FreeLing es-CL 2027, the Chilean Spanish data.\n"
            "FreeLing 4.2 (TALP Research Center, Universitat Politecnica de\n"
            "Catalunya), built with the build fixes current compilers need, a fix\n"
            "for word sense annotation, and the name-class change of FreeLing\n"
            "es-CL 2027, installed in /usr/local with the Chilean dictionaries,\n"
            "probabilities, multiword expressions, tagset, name recognizer rules,\n"
            "currencies and name classifier lists in place of FreeLing's."),
        "conflicts": ["freeling"],
        "depends": deps,
        "contents": contents,
        "scripts": {"postinstall": "./packaging/ldconfig.sh",
                    "postremove": "./packaging/ldconfig.sh"},
    }
    # nfpm reads YAML; JSON is YAML.
    json.dump(conf, sys.stdout, indent=1, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
