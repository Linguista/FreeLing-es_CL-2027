#!/usr/bin/env bash
# VERSION 1.0.0
#
# patch-freeling.sh -- applies to an unpacked FreeLing 4.2 source tree the
# changes FreeLing es-CL 2027 is built with:
#   1-5  build fixes for current compilers (CMake 4, GCC 15 and later,
#        ICU 77 and later): C++17 instead of C++11, and <cmath> in the five
#        files that use math functions without it (smoothingLD.h only fails
#        with GCC 13, Ubuntu 24.04; the other three build fixes are compiler
#        flags, given by build-freeling.sh);
#   2a   the two errors in templates never instantiated that GCC 15 and
#        later report as warnings, silenced by -Wno-template-body, and
#        GCC 14 (Debian 13) as errors: treeler's ConstantScores assigns to
#        a const member, and the bundled Eigen calls derived() on a
#        Transpose (fixed as Eigen 3.4.1 fixed it);
#   6    the install: only the Spanish variants whose data the source
#        tarball carries (es-old, es-ar, es-cl), not the two Catalan ones;
#   7    a bug: csr_kb.cc indexed vectors it had only reserved (UKB word
#        sense annotation aborts wherever assertions are on);
#   8    the name classes of the name recognizer and classifier
#        (software/patches/freeling-4.2-np-classes.patch).
# Every change must apply exactly as expected, or the script stops.
#
# Usage: patch-freeling.sh FREELING_SOURCE_DIR NP_CLASSES_PATCH

set -euo pipefail
src="${1:?the FreeLing 4.2 source folder}"
np_patch="${2:?the name-class patch}"
cd "$src"

fail() { echo "patch-freeling.sh: $*" >&2; exit 1; }

# The three files the name-class patch changes must be FreeLing 4.2's.
sha256sum -c --quiet - <<'EOF' || fail "not FreeLing 4.2's np.cc, np.h and nec.cc"
2934779917d1041111f9750effb78500a8bfbba9057bfbf43c1cc22cac51a622  src/libfreeling/np.cc
f09274b49e0c72f99ced11ff386c0473dec8a692bed1c29c41e3dd5832550f7b  src/include/freeling/morfo/np.h
1e04d9fafb3423d41803030b3b29a5e14cf80e0f2dc18f1b50d458ba07525a5f  src/libfreeling/nec.cc
EOF

# 4: C++17 (ICU 77's headers need it; a plain set() overrides the cache).
grep -qx 'set(CMAKE_CXX_STANDARD 11)' CMakeLists.txt || fail "CMakeLists.txt: no set(CMAKE_CXX_STANDARD 11)"
sed -i 's/^set(CMAKE_CXX_STANDARD 11)$/set(CMAKE_CXX_STANDARD 17)/' CMakeLists.txt

# 5: <cmath> where math functions are used without it.
for f in src/libfreeling/csr_kb.cc src/libfreeling/coref/relaxcor/relaxcor_fex_dep.cc \
         src/libfreeling/summarizer/summarizer.cc src/libfreeling/numbers/numbers_cs.cc \
         src/include/freeling/morfo/smoothingLD.h; do
    grep -q '#include' "$f" || fail "$f: no #include"
    grep -q '#include <cmath>' "$f" && fail "$f: already includes <cmath>"
    sed -i '0,/#include/s//#include <cmath>\n#include/' "$f"
    grep -q '#include <cmath>' "$f" || fail "$f: <cmath> not added"
done

# 2a: errors in uninstantiated templates (GCC 14 stops on them).
grep -q '^    const double _s; $' src/libtreeler/treeler/base/scores.h || fail "scores.h: no const double _s"
sed -i 's/^    const double _s; $/    double _s; /' src/libtreeler/treeler/base/scores.h
t=src/eigen3/Eigen/src/Core/Transpositions.h
[ "$(grep -c 'AliasFreeProduct>(matrix.derived(), trt.derived());' "$t")" -eq 1 ] || fail "Transpositions.h: the line to fix is not there once"
sed -i 's/AliasFreeProduct>(matrix.derived(), trt.derived());/AliasFreeProduct>(matrix.derived(), trt);/' "$t"

# 6: only the Spanish variants.
grep -q '^SET(variants "es/es-old;es/es-ar;es/es-cl;ca/balear;ca/valencia")' CMakeLists.txt \
    || fail "CMakeLists.txt: the variant list is not FreeLing 4.2's"
sed -i 's|^SET(variants "es/es-old;es/es-ar;es/es-cl;ca/balear;ca/valencia")|SET(variants "es/es-old;es/es-ar;es/es-cl")|' CMakeLists.txt

# 7: reserve() leaves size() at 0; the vectors are then indexed.
grep -q 'edges\.reserve(rels\.size());' src/libfreeling/csr_kb.cc || fail "csr_kb.cc: edges.reserve not found"
grep -q 'first_edge\.reserve(nv); num_edges\.reserve(nv); out_coef\.reserve(nv);' src/libfreeling/csr_kb.cc \
    || fail "csr_kb.cc: first_edge.reserve not found"
sed -i 's/edges\.reserve(rels\.size());/edges.resize(rels.size());/;
        s/first_edge\.reserve(nv); num_edges\.reserve(nv); out_coef\.reserve(nv);/first_edge.resize(nv); num_edges.resize(nv); out_coef.resize(nv);/' \
    src/libfreeling/csr_kb.cc

# 8: the name classes.
patch -p1 --forward --batch < "$np_patch"

echo "patch-freeling.sh: every change applied"
