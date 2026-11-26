#!/usr/bin/env bash
# VERSION 1.8.0
#
# test-freeling.sh -- checks an installed FreeLing es-CL 2027 package: the
# library has the name-class change, the probability columns and the
# ambiguous-multiwords change, the Chilean files are FreeLing es-CL
# 2027's (their sha256 as in this repository's SHA256SUMS), FreeLing
# analyzes two Chilean sentences with the Chilean dictionary (cachái, soi
# and bañai are voseo forms; voh is vos; no está ni ahí and conchetumare are
# Chilean multiwords), lowercases a capital that is not A to Z (Él is él,
# Ñuñoa ñuñoa), splits reírme into reír + me (the known-roots change of the
# affix analysis), does not read sáltetelo as sal + te + te + lo (the clitic
# rules of afixos.dat), cansá as the participle of cansar with the informal
# dictionary and never with the default one, a 19th-century one with the
# 19th-century dictionary (jente is gente, i is y), and an Old Spanish one
# with FreeLing Old (dixo is decir), which also parses it (its config names
# the parser's files where FreeLing 4.2 has them: change 13 of
# patch-freeling.sh); on Linux and macOS every ICU and Boost library comes
# from FreeLing's own copies in PREFIX/lib/freeling-es-cl (bundle-libraries.sh); with the
# speech config, nn is the hesitation (an interjection) and a stand-in token
# keeps its tag (xxxredactedxxx Fz); the CoNLL columns LEX_PROB and TAG_PROB
# hold a probability for every token (the tag-probabilities change); and a
# multiword marked ambiguous is decided by the tagger (the
# ambiguous-multiwords change): a ver is a + ver in "voy a ver la película"
# and one token in "a ver, dime qué pasó". Every other
# analysis asks for FreeLing's own output format (--output freeling): the
# configs write CoNLL.
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
n=$(strings -e "$wide" "$lib" | grep -c -x -E "LEX_PROB|TAG_PROB" || true)
[ "$n" -eq 2 ] || { echo "FAIL  $lib: no LEX_PROB and TAG_PROB columns (the tag-probabilities change)"; exit 1; }
n=$(strings -e "$wide" "$lib" | grep -c "Invalid weight in ambiguous locution entry" || true)
[ "$n" -ge 1 ] || { echo "FAIL  $lib: multiwords marked ambiguous are not decided by the tagger (the ambiguous-multiwords change)"; exit 1; }
echo "ok    $(basename "$lib") has the probability columns and the ambiguous-multiwords change"

for f in es/es-cl/dicc.src es/es-cl/informal/dicc.src es/es-cl/19th-century/dicc.src es/es-cl/19th-century/probabilitats.dat \
         es/es-cl/19th-century/locucions.dat es/es-cl/probabilitats.dat \
         es/es-cl/locucions.dat es/es-cl/tagset.dat es/es-cl/np.dat es/es-cl/np-speech.dat \
         es/es-cl/quantities.dat es/es-cl/stand-ins.tsv common/nec/cities.dat es/nerc/data/gazLOC-c.dat \
         es/nerc/data/gazPER-c.dat es/nerc/data/gazPER-p.dat es/nerc/nec/nec-ab-poor1.dat \
         es/afixos.dat es/es-cl/usermap/es-cl.dat es/es-cl/usermap/es-cl-informal.dat \
         es/es-cl/usermap/es-cl-speech.dat es/es-cl/usermap/es-cl-19th-century.dat \
         config/es-cl.cfg config/es-cl-informal.cfg config/es-cl-speech.cfg config/es-cl-19th-century.cfg \
         config/es-cl-conll-columns.cfg; do
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
echo "ok    the 27 Chilean files are the release's; only Spanish is installed"

if [ "$windows" = no ]; then
    bdir="$prefix/lib/freeling-es-cl"
    [ -d "$bdir" ] && [ -n "$(ls -A "$bdir")" ] || { echo "FAIL  $bdir: FreeLing's own ICU and Boost are not there"; exit 1; }
    if [ "$(uname -s)" = Darwin ]; then
        bad="$(for f in "$prefix"/bin/* "$prefix"/lib/*.dylib "$bdir"/*; do
                   otool -h "$f" >/dev/null 2>&1 && otool -L "$f" | tail -n +2 | awk '{print $1}'
               done | grep -E '/lib(icu|boost_)' | grep -v "^$bdir/" | sort -u || true)"
    else
        bdir="$(realpath "$bdir")"
        bad="$(for f in "$prefix"/bin/* "$prefix"/lib/*.so "$bdir"/*; do
                   readelf -h "$f" >/dev/null 2>&1 && LD_LIBRARY_PATH= ldd "$f"
               done | awk '$1 ~ /^lib(icu|boost_)/ {print $1, $3}' | while read -r l p; do
                   case "$(realpath -m "$p")" in "$bdir"/*) ;; *) echo "$l => $p" ;; esac
               done | sort -u || true)"
    fi
    [ -z "$bad" ] || { echo "$bad"; echo "FAIL  ICU or Boost not loaded from $bdir"; exit 1; }
    echo "ok    every ICU and Boost library comes from FreeLing's own copies ($(ls "$bdir" | wc -l | tr -d ' ') in $bdir)"
fi

status=0
out="$(echo "Cachái que mi vecina, la Javi, no está ni ahí con voh, conchetumare. Dice que soi cuartero y que no te bañai nunca." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || status=$?
echo "$out"
[ "$status" -eq 0 ] || { echo "FAIL  analyze exited with $status"; exit 1; }
for want in "^Cachái cachar VMIP2SV " "^no_está_ni_ahí no_estar_ni_ahí VMIP3S0 " "^voh vos PP2CS0V " \
            "^conchetumare concha_de_tu_madre I " "^soi ser VSIP2SV " "^bañai bañar VMIP2SV "; do
    echo "$out" | grep -q "$want" || { echo "FAIL  the Chilean sentences: no line matching $want"; exit 1; }
done
echo "ok    FreeLing reads the Chilean sentences: cachái, soi and bañai as voseo, voh as vos, no está ni ahí and conchetumare as Chilean multiwords"

out="$(echo "Él llegó a Ñuñoa." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^Él él P" && echo "$out" | grep -q "^Ñuñoa ñuñoa NP" \
    || { echo "FAIL  a capital other than A to Z was not lowercased (Él, Ñuñoa)"; exit 1; }
echo "ok    FreeLing lowercases accented capitals and Ñ (Él is él, Ñuñoa ñuñoa)"

out="$(echo "Me dio risa reírme." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^reír reír VMN0000" && echo "$out" | grep -q "^me me PP1CS00" \
    || { echo "FAIL  reírme was not read as reír + me (the known-roots change)"; exit 1; }
echo "ok    FreeLing reads reírme as reír + me (the known-roots change)"

out="$(echo "Sáltetelo." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "salir" \
    && { echo "FAIL  sáltetelo was read as sal + te + te + lo (the clitic rules of afixos.dat)"; exit 1; }
echo "ok    FreeLing does not read sáltetelo as sal + te + te + lo (the clitic rules of afixos.dat)"

out="$(echo "Estoy cansá." | analyze es-cl-informal.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl-informal.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^cansá cansar VMP00SF" \
    || { echo "FAIL  the informal dictionary did not read cansá as cansar VMP00SF"; exit 1; }
out="$(echo "Estoy cansá." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^cansá cansar VMP00SF" \
    && { echo "FAIL  the default dictionary read cansá as cansar VMP00SF (the reduced forms are for informal writing only)"; exit 1; }
echo "ok    cansá is cansar VMP00SF with the informal dictionary only"

out="$(echo "La jente i el rei." | analyze es-cl-19th-century.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl-19th-century.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^jente gente NCFS000" && echo "$out" | grep -q "^i y CC" \
    || { echo "FAIL  the 19th-century dictionary did not read jente as gente and i as y"; exit 1; }
echo "ok    the 19th-century dictionary reads jente as gente and i as y"

out="$(echo "Et dixo el rey." | analyze es-old.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-old.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^dixo decir VMIS3S0" || { echo "FAIL  FreeLing Old did not read dixo as decir"; exit 1; }
echo "ok    FreeLing Old reads dixo as decir"

out="$(echo "Et dixo el rey." | analyze es-old.cfg --outlv dep --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  FreeLing Old does not parse (es-old.cfg, --outlv dep)"; exit 1; }
echo "$out"
echo "$out" | grep -q "(dixo decir VMIS3S0" && echo "$out" | grep -q "/dobj/(rey rey NCMS000" \
    || { echo "FAIL  FreeLing Old's parse has no tree with dixo and its object rey"; exit 1; }
echo "ok    FreeLing Old parses (rey is the object of dixo)"

out="$(echo "nn y xxxredactedxxx dijo que no." | analyze es-cl-speech.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl-speech.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^nn nn I" && echo "$out" | grep -q "^xxxredactedxxx xxxredactedxxx Fz" \
    || { echo "FAIL  the speech config did not read nn as the hesitation and xxxredactedxxx as Fz (its user map)"; exit 1; }
echo "ok    the speech config reads nn as the hesitation and the stand-in xxxredactedxxx as Fz"

cols="$(mktemp)"
printf '<Columns>\nID FORM LEMMA TAG LEX_PROB TAG_PROB\n</Columns>\n' > "$cols"
colsarg="$cols"
[ "$windows" = yes ] && colsarg="$(cygpath -m "$cols")"
status=0
out="$(echo "Bueno, yo creo que es bueno." | analyze es-cl.cfg --outlv tagged --output conll --oconll "$colsarg" --nonec --sense none 2>&1)" || status=$?
rm -f "$cols"
echo "$out"
[ "$status" -eq 0 ] || { echo "FAIL  analyze with es-cl.cfg and the probability columns"; exit 1; }
lines=$(echo "$out" | awk 'NF > 0 {n++} END {print n + 0}')
bad=$(echo "$out" | awk 'NF > 0 && (NF != 6 || $5 !~ /^[01](\.[0-9]+)?$/ || $6 !~ /^[01](\.[0-9]+)?$/ || $5 > 1 || $6 > 1) {n++} END {print n + 0}')
[ "$lines" -ge 8 ] && [ "$bad" -eq 0 ] \
    || { echo "FAIL  LEX_PROB and TAG_PROB: $bad of $lines token lines without two probabilities from 0 to 1"; exit 1; }
echo "ok    the CoNLL columns LEX_PROB and TAG_PROB hold a probability for every token"

grep -q "^a_ver a_ver I A" "$share/es/es-cl/locucions.dat" \
    || { echo "FAIL  es/es-cl/locucions.dat: a_ver is not marked ambiguous (a_ver a_ver I A)"; exit 1; }
out="$(echo "Voy a ver la película." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^a a SP" && echo "$out" | grep -q "^ver ver VMN0000" \
    || { echo "FAIL  a ver was not read as a + ver in voy a ver la película (the ambiguous-multiwords change; a_ver is marked A)"; exit 1; }
out="$(echo "A ver, dime qué pasó." | analyze es-cl.cfg --outlv tagged --output freeling --nonec --sense none 2>&1)" || { echo "$out"; echo "FAIL  analyze with es-cl.cfg"; exit 1; }
echo "$out"
echo "$out" | grep -q "^A_ver a_ver I" \
    || { echo "FAIL  a ver before a comma was not kept as the multiword a_ver"; exit 1; }
echo "ok    the tagger decides the ambiguous multiword a ver: a + ver in voy a ver, a_ver in a ver, dime"

grep -q "^CompoundAnalysis=no" "$share/config/es-old.cfg" \
    || { echo "FAIL  es-old.cfg does not have compound analysis off"; exit 1; }
for c in es-cl es-cl-informal es-cl-speech es-cl-19th-century; do
    grep -q "^CompoundAnalysis=no" "$share/config/$c.cfg" \
        || { echo "FAIL  $c.cfg does not have compound analysis off"; exit 1; }
done
echo "ok    compound analysis is off in every config, FreeLing Old's included"
echo "ALL CHECKS PASSED"
