#!/usr/bin/env bash
# VERSION 1.2.0
#
# test-freeling.sh -- checks an installed FreeLing es-CL 2027 package: the
# library has the name-class change, the Chilean files are FreeLing es-CL
# 2027's (their sha256 as in this repository's SHA256SUMS), FreeLing
# analyzes a Chilean sentence with the Chilean dictionary (tenís is a
# voseo form of tener), a 19th-century one with the 19th-century
# dictionary (jente is gente, i is y), and an Old Spanish one with FreeLing
# Old (dixo is decir), whose multiword file is the Chilean one.
#
# Usage, from the repository root: packaging/test-freeling.sh
# PREFIX=DIR names another install prefix than /usr/local (the macOS
# tarballs install into /usr/local/freeling-es-cl-2027); on macOS, GNU
# coreutils and binutils (sha256sum, strings -e L) must come first in PATH.
# On Windows (MSYS2's UCRT64 shell, the Windows build) it runs analyzer.exe
# itself, with FREELINGSHARE set as analyze.bat sets it; the library is
# libfreeling.dll, whose wide strings are 16-bit; es/locucions.dat is a
# copy of es-cl/locucions.dat (Windows has no symbolic links in a zip).

set -euo pipefail
prefix="${PREFIX:-/usr/local}"
lib="$prefix/lib/libfreeling.so"
[ -e "$lib" ] || lib="$prefix/lib/libfreeling.dylib"
[ -e "$lib" ] || lib="$prefix/lib/libfreeling.dll"
share="$prefix/share/freeling"
wide=L
if [ -e "$prefix/bin/analyzer.exe" ]; then
    windows=yes
    wide=l
    export FREELINGSHARE="$(cygpath -m "$share")"
    export PATH="$prefix/bin:$prefix/lib:$PATH"
    analyze() { "$prefix/bin/analyzer.exe" -f "$(cygpath -m "$share/config/$1")" "${@:2}"; }
else
    windows=no
    analyze() { "$prefix/bin/analyze" -f "$@"; }
fi

n=$(strings -e "$wide" "$lib" | grep -c -x -E "DictionaryClasses|FixedClasses|ClassesAtSentenceStart|SentenceStartClasses|ClassShares|keep:" || true)
[ "$n" -eq 6 ] || { echo "FAIL  $lib: $n of the 6 marks of the name-class change"; exit 1; }
echo "ok    $(basename "$lib") has the name-class change"

for f in es/es-cl/dicc.src es/es-cl/historical/dicc.src es/es-cl/historical/probabilitats.dat \
         es/es-cl/historical/locucions.dat es/es-cl/probabilitats.dat \
         es/es-cl/locucions.dat es/es-cl/tagset.dat es/es-cl/np.dat es/es-cl/np-speech.dat \
         es/es-cl/quantities.dat common/nec/cities.dat es/nerc/data/gazLOC-c.dat \
         es/nerc/data/gazPER-c.dat es/nerc/data/gazPER-p.dat es/nerc/nec/nec-ab-poor1.dat \
         config/es-cl.cfg config/es-cl-19th-century.cfg; do
    want="$(awk -v r="data/$f" '$2 == r {print $1}' SHA256SUMS)"
    have="$(sha256sum "$share/$f" | cut -d' ' -f1)"
    [ -n "$want" ] && [ "$want" = "$have" ] || { echo "FAIL  $share/$f is not the release's"; exit 1; }
done
[ ! -e "$share/common/nec/cities-CL.dat" ] || { echo "FAIL  cities-CL.dat is still installed"; exit 1; }
if [ "$windows" = yes ]; then
    cmp -s "$share/es/locucions.dat" "$share/es/es-cl/locucions.dat" || { echo "FAIL  es/locucions.dat is not es-cl/locucions.dat"; exit 1; }
else
    [ "$(readlink "$share/es/locucions.dat")" = "es-cl/locucions.dat" ] || { echo "FAIL  es/locucions.dat is not a link to es-cl/locucions.dat"; exit 1; }
fi
for d in en pt es/es-ar; do
    [ ! -e "$share/$d" ] || { echo "FAIL  $share/$d is installed"; exit 1; }
done
echo "ok    the 17 Chilean files are the release's; only Spanish is installed"

status=0
out="$(echo "Vos tenís que venir a Arica." | analyze es-cl.cfg --outlv tagged --nonec --sense none 2>&1)" || status=$?
echo "$out"
[ "$status" -eq 0 ] || { echo "FAIL  analyze exited with $status"; exit 1; }
echo "$out" | grep -q "^tenís tener VMIP2SV" || { echo "FAIL  tenís was not read as a voseo form of tener"; exit 1; }
echo "ok    FreeLing reads tenís as a voseo form of tener"

out="$(echo "La jente i el rei." | analyze es-cl-19th-century.cfg --outlv tagged --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl-19th-century.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^jente gente NCFS000" && echo "$out" | grep -q "^i y CC" \
    || { echo "FAIL  the 19th-century dictionary did not read jente as gente and i as y"; exit 1; }
echo "ok    the 19th-century dictionary reads jente as gente and i as y"

out="$(echo "Et dixo el rey." | analyze es-old.cfg --outlv tagged --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-old.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^dixo decir VMIS3S0" || { echo "FAIL  FreeLing Old did not read dixo as decir"; exit 1; }
echo "ok    FreeLing Old reads dixo as decir"
echo "ALL CHECKS PASSED"
