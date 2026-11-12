#!/usr/bin/env bash
# VERSION 1.0.0
#
# test-freeling.sh -- checks an installed FreeLing es-CL 2027 package: the
# library has the name-class change, the Chilean files are FreeLing es-CL
# 2027's (their sha256 as in this repository's SHA256SUMS), and FreeLing
# analyzes a Chilean sentence with the Chilean dictionary: tenís is a
# voseo form of tener.
#
# Usage, from the repository root: packaging/test-freeling.sh

set -euo pipefail
prefix=/usr/local
share="$prefix/share/freeling"

n=$(strings -e L "$prefix/lib/libfreeling.so" | grep -c -x -E "DictionaryClasses|FixedClasses|ClassesAtSentenceStart|SentenceStartClasses|ClassShares|keep:" || true)
[ "$n" -eq 6 ] || { echo "FAIL  libfreeling.so: $n of the 6 marks of the name-class change"; exit 1; }
echo "ok    libfreeling.so has the name-class change"

for f in es/es-cl/dicc.src es/es-cl/historical/dicc.src es/es-cl/probabilitats.dat \
         es/es-cl/locucions.dat es/es-cl/tagset.dat es/es-cl/np.dat es/es-cl/np-speech.dat \
         es/es-cl/quantities.dat common/nec/cities.dat es/nerc/data/gazLOC-c.dat \
         es/nerc/data/gazPER-c.dat es/nerc/data/gazPER-p.dat es/nerc/nec/nec-ab-poor1.dat; do
    want="$(awk -v r="data/$f" '$2 == r {print $1}' SHA256SUMS)"
    have="$(sha256sum "$share/$f" | cut -d' ' -f1)"
    [ -n "$want" ] && [ "$want" = "$have" ] || { echo "FAIL  $share/$f is not the release's"; exit 1; }
done
[ ! -e "$share/common/nec/cities-CL.dat" ] || { echo "FAIL  cities-CL.dat is still installed"; exit 1; }
echo "ok    the 13 Chilean files are the release's"

status=0
out="$(echo "Vos tenís que venir a Arica." | "$prefix/bin/analyze" -f es-cl.cfg --outlv tagged --nonec --nosense 2>&1)" || status=$?
echo "$out"
[ "$status" -eq 0 ] || { echo "FAIL  analyze exited with $status"; exit 1; }
echo "$out" | grep -q "^tenís tener VMIP2SV" || { echo "FAIL  tenís was not read as a voseo form of tener"; exit 1; }
echo "ok    FreeLing reads tenís as a voseo form of tener"
echo "ALL CHECKS PASSED"
