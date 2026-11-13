#!/usr/bin/env bash
# VERSION 1.0.0
#
# install-data.sh -- puts FreeLing es-CL 2027's data into an installed
# FreeLing 4.2: the Chilean files over FreeLing's own (the files and places
# of freeling_escl_deploy.py --target system), FreeLing's Chilean city list
# removed (the Chilean cities.dat merges it), and es/locucions.dat, the
# multiword file FreeLing Old reads, made a link to es-cl/locucions.dat.
# build-freeling.sh (Linux packages) and the macOS job of
# .github/workflows/packages.yml run it.
#
# Usage: packaging/install-data.sh SHARE
#   SHARE  FreeLing's installed data folder, e.g. /usr/local/share/freeling

set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(dirname "$here")"
share="${1:?the installed FreeLing data folder, e.g. /usr/local/share/freeling}"
[ -d "$share/es/es-cl" ] && [ -d "$share/config" ] || { echo "install-data.sh: $share is not FreeLing's data folder" >&2; exit 1; }

files="es/es-cl/dicc.src es/es-cl/historical/dicc.src es/es-cl/historical/probabilitats.dat
es/es-cl/historical/locucions.dat es/es-cl/probabilitats.dat
es/es-cl/locucions.dat es/es-cl/tagset.dat es/es-cl/np.dat es/es-cl/np-speech.dat
es/es-cl/quantities.dat common/nec/cities.dat es/nerc/data/gazLOC-c.dat
es/nerc/data/gazPER-c.dat es/nerc/data/gazPER-p.dat es/nerc/nec/nec-ab-poor1.dat
config/es-cl.cfg config/es-cl-19th-century.cfg"
n=0
for f in $files; do
    mkdir -p "$(dirname "$share/$f")"
    cp "$repo/data/$f" "$share/$f"
    chmod 644 "$share/$f"
    n=$((n + 1))
done
rm -f "$share/common/nec/cities-CL.dat"
rm -f "$share/es/locucions.dat"
ln -s es-cl/locucions.dat "$share/es/locucions.dat"
echo "install-data.sh: $n Chilean files in $share; es/locucions.dat -> es-cl/locucions.dat"
