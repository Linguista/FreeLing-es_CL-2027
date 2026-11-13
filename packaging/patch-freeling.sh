#!/usr/bin/env bash
# VERSION 1.2.0
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
#   6    the install: Spanish only. The English and Portuguese data the
#        source tarball carries, the configs of every other language and
#        the Argentine variant (es-ar) are deleted from the source tree,
#        so they are neither built nor installed; the variants are
#        FreeLing Old (es-old, untouched) and es-cl;
#   7    a bug: csr_kb.cc indexed vectors it had only reserved (UKB word
#        sense annotation aborts wherever assertions are on);
#   8    the name classes of the name recognizer and classifier
#        (software/patches/freeling-4.2-np-classes.patch);
#   9    Windows with GCC (MSYS2's UCRT64, the Windows build): each change
#        takes effect only there (under __MINGW32__, or in a Windows-only
#        part of a CMakeLists.txt), so Linux and macOS build exactly as
#        before:
#        9a  crfsuite no longer defines _MSC_VER: with it, MinGW's headers
#            give their inline functions ordinary definitions, and the
#            library does not link (multiple definition of llabs ...);
#        9b  crfsuite's aligned memory uses MinGW's _aligned_malloc and
#            _aligned_free (MinGW has no posix_memalign);
#        9c  libfreeling links ICU's i18n and data libraries under their
#            Windows names too (ICU_IN_LIBRARY, ICU_DT_LIBRARY), without
#            which the collator is not found;
#        9d  the locale: libstdc++ on MinGW knows only "C", so the C runtime
#            gets the UTF-8 locale and the C++ locale stays "C" (FreeLing's
#            locale "eng" stops every program);
#        9e  the standard streams convert UTF-8 themselves, as on macOS,
#            instead of the C runtime's wide mode (_O_U8TEXT), which only
#            MSVC's streams write through: with it nothing is read or
#            written;
#        9f  upper and lower case through ICU (util.cc, dictionary.cc):
#            MinGW's C runtime changes the case of ASCII letters only, so
#            the lowercase form of a capitalized Él, Ángel or Ñuñoa, which
#            FreeLing looks up in the dictionary and gives names as their
#            lemma, kept its capital.
#        Two more Windows fixes are build options, in the Windows job of
#        .github/workflows/packages.yml: Boost linked dynamically, and every
#        symbol of each DLL exported.
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

# 6: Spanish only. The languages and variants built are set in
# CMakeLists.txt; install(DIRECTORY data/ ...) installs every data folder
# there is, so the others are deleted from the tree as well.
grep -q '^SET(languages "as;ca;cs;cy;de;en;es;fr;gl;hr;it;nb;pt;ru;sl")' CMakeLists.txt \
    || fail "CMakeLists.txt: the language list is not FreeLing 4.2's"
grep -q '^SET(variants "es/es-old;es/es-ar;es/es-cl;ca/balear;ca/valencia")' CMakeLists.txt \
    || fail "CMakeLists.txt: the variant list is not FreeLing 4.2's"
sed -i 's|^SET(languages "as;ca;cs;cy;de;en;es;fr;gl;hr;it;nb;pt;ru;sl")|SET(languages "es")|' CMakeLists.txt
sed -i 's|^SET(variants "es/es-old;es/es-ar;es/es-cl;ca/balear;ca/valencia")|SET(variants "es/es-old;es/es-cl")|' CMakeLists.txt
# FreeLing-src-4.2.tar.gz carries the data of English and Portuguese
# besides Spanish (the other languages come in separate tarballs).
for lg in en pt; do
    [ -d "data/$lg" ] || fail "data/$lg: not there"
    rm -rf "data/$lg"
done
[ -d data/es/es-ar ] || fail "data/es/es-ar: not there"
rm -rf data/es/es-ar
for c in as ca ca-balear ca-valencia cs cy de en es-ar fr gl it nb pt ru sl; do
    [ -f "data/config/$c.cfg" ] || fail "data/config/$c.cfg: not there"
    rm -f "data/config/$c.cfg"
done
left="$(LC_ALL=C ls data | tr '\n' ' ')"
[ "$left" = "common config es " ] || fail "data/ holds more than common, config and es: $left"
left="$(LC_ALL=C ls data/config | tr '\n' ' ')"
[ "$left" = "es-cl.cfg es-old.cfg es.cfg ident.cfg " ] || fail "data/config holds other configs: $left"

# 7: reserve() leaves size() at 0; the vectors are then indexed.
grep -q 'edges\.reserve(rels\.size());' src/libfreeling/csr_kb.cc || fail "csr_kb.cc: edges.reserve not found"
grep -q 'first_edge\.reserve(nv); num_edges\.reserve(nv); out_coef\.reserve(nv);' src/libfreeling/csr_kb.cc \
    || fail "csr_kb.cc: first_edge.reserve not found"
sed -i 's/edges\.reserve(rels\.size());/edges.resize(rels.size());/;
        s/first_edge\.reserve(nv); num_edges\.reserve(nv); out_coef\.reserve(nv);/first_edge.resize(nv); num_edges.resize(nv); out_coef.resize(nv);/' \
    src/libfreeling/csr_kb.cc

# 8: the name classes.
patch -p1 --forward --batch < "$np_patch"

# 9: Windows with GCC (MinGW).
c=src/crfsuite/CMakeLists.txt
[ "$(grep -c -- ' -D_MSC_VER=1 )' "$c")" -eq 1 ] || fail "$c: -D_MSC_VER=1 is not there once"
sed -i 's/ -D_MSC_VER=1 )/ )/' "$c"
c=src/crfsuite/crfsuite/crf/vecmath.h
[ "$(grep -c '^#ifdef _MSC_VER$' "$c")" -eq 2 ] || fail "$c: not FreeLing 4.2's"
sed -i -z 's/#ifdef _MSC_VER\n#include <malloc.h>/#if defined(_MSC_VER) || defined(__MINGW32__)\n#include <malloc.h>/' "$c"
[ "$(grep -c '__MINGW32__' "$c")" -eq 1 ] || fail "$c: _aligned_malloc not given to MinGW"
for c in src/crfsuite/crfsuite/lbfgs/arithmetic_sse_double.h src/crfsuite/crfsuite/lbfgs/arithmetic_sse_float.h; do
    [ "$(grep -c '^#if[ \t]*defined(_MSC_VER)[ \t]*$' "$c")" -eq 1 ] || fail "$c: not FreeLing 4.2's"
    sed -i 's/^#if[ \t]*defined(_MSC_VER)[ \t]*$/#if     defined(_MSC_VER) || defined(__MINGW32__)/' "$c"
done
c=src/crfsuite/crfsuite/lbfgs/arithmetic_sse_double.h
sed -i -z 's/#ifdef[ \t]*_MSC_VER\n\([ \t]*_aligned_free\)/#if defined(_MSC_VER) || defined(__MINGW32__)\n\1/' "$c"
[ "$(grep -c '__MINGW32__' "$c")" -eq 2 ] || fail "$c: _aligned_free not given to MinGW"
c=src/libfreeling/CMakeLists.txt
[ "$(grep -c '\${ICU_DATA_LIBRARY}' "$c")" -eq 1 ] || fail "$c: \${ICU_DATA_LIBRARY} is not there once"
sed -i 's/\${ICU_DATA_LIBRARY}/${ICU_DATA_LIBRARY} ${ICU_IN_LIBRARY} ${ICU_DT_LIBRARY}/' "$c"
c=src/libfreeling/util.cc
grep -q '^        current_locale = locale(locale::classic(), lname.c_str(), locale::ctype);$' "$c" || fail "$c: the locale line is not there"
grep -q '^        #if defined MACOSX$' "$c" || fail "$c: the macOS stream conversion is not there"
grep -q '^    std::ios_base::sync_with_stdio(false);$' "$c" || fail "$c: sync_with_stdio is not there"
grep -q '^      setUtf8Mode(stdin, "stdin");$' "$c" || fail "$c: the _O_U8TEXT mode is not there"
sed -i 's/^        current_locale = locale(locale::classic(), lname.c_str(), locale::ctype);$/#if defined __MINGW32__\n        ::setlocale(LC_ALL, ".UTF-8");\n        current_locale = locale::classic();\n#else\n        current_locale = locale(locale::classic(), lname.c_str(), locale::ctype);\n#endif/;
        s/^        #if defined MACOSX$/        #if defined MACOSX || defined __MINGW32__/;
        s/^    std::ios_base::sync_with_stdio(false);$/    std::ios_base::sync_with_stdio(false);\n#if defined __MINGW32__\n    wcin.imbue(current_locale);\n    wcout.imbue(current_locale);\n    wcerr.imbue(current_locale);\n#endif/;
' "$c"
sed -i -z 's/\n    #if defined WIN32 || defined WIN64\n      setUtf8Mode(stdin, "stdin");/\n    #if (defined WIN32 || defined WIN64) \&\& !defined __MINGW32__\n      setUtf8Mode(stdin, "stdin");/' "$c"
[ "$(grep -c '__MINGW32__' "$c")" -eq 4 ] || fail "$c: the Windows changes did not all apply"

# 9f: case changes through ICU on MinGW, in the two files that call towlower
# and towupper. Inserted just before "namespace freeling {", after every
# #include, so that only FreeLing's own calls are renamed.
for c in src/libfreeling/util.cc src/libfreeling/dictionary.cc; do
    [ "$(grep -c '^namespace freeling {' "$c")" -eq 1 ] || fail "$c: not one \"namespace freeling {\""
    grep -q 'towupper' "$c" || fail "$c: no towupper to replace"
    sed -i 's/^namespace freeling {$/#if defined __MINGW32__\n#include <unicode\/uchar.h>\nstatic inline wint_t freeling_towlower(wint_t c) { return (wint_t) u_tolower((UChar32) c); }\nstatic inline wint_t freeling_towupper(wint_t c) { return (wint_t) u_toupper((UChar32) c); }\n#define towlower freeling_towlower\n#define towupper freeling_towupper\n#endif\n\nnamespace freeling {/' "$c"
    [ "$(grep -c 'freeling_towupper' "$c")" -eq 2 ] || fail "$c: the ICU case change did not apply"
done

echo "patch-freeling.sh: every change applied"
