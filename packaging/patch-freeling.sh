#!/usr/bin/env bash
# VERSION 1.6.0
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
#        FreeLing Old (es-old) and es-cl;
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
#        symbol of each DLL exported;
#  10    the known-roots change of the affix analysis
#        (software/patches/freeling-4.2-known-roots.patch, decided 261116):
#        a word read as a dictionary root and a suffix is not also taken
#        apart into a prefix, another root and a suffix, and a root with the
#        accent of a hiatus keeps it when the word is split;
#  11    the probability columns of the CoNLL output
#        (software/patches/freeling-4.2-tag-probabilities.patch, decided
#        261119): LEX_PROB, the probability of the selected reading among
#        the readings of the word, and TAG_PROB, the probability the tagger
#        gives the selected tag in its sentence;
#  12    multiwords marked ambiguous (A) are decided by the tagger
#        (software/patches/freeling-4.2-ambiguous-multiwords.patch, decided
#        261119): FreeLing 4.2 reads the A flag of its multiword file and
#        then never uses it, so every multiword is always joined. Applied
#        after 11, which it builds on.
#  13    FreeLing Old's config (data/config/es-old.cfg) names its parser's
#        files where FreeLing 4.2 has none, es/grammar-dep.dat and
#        es/dep/dependences.dat, so FreeLing Old stops at the parse level
#        ("GRAMMAR: Error opening file"): the two lines name the files
#        FreeLing 4.2 has and es.cfg names, es/chunker/grammar-chunk.dat
#        and es/dep_txala/dependences.dat. Nothing else in FreeLing Old is
#        changed.
# Every change must apply exactly as expected, or the script stops.
#
# Usage: patch-freeling.sh FREELING_SOURCE_DIR NP_CLASSES_PATCH KNOWN_ROOTS_PATCH \
#            TAG_PROBABILITIES_PATCH AMBIGUOUS_MULTIWORDS_PATCH

set -euo pipefail
src="${1:?the FreeLing 4.2 source folder}"
np_patch="$(realpath "${2:?the name-class patch}")"
kr_patch="$(realpath "${3:?the known-roots patch}")"
tp_patch="$(realpath "${4:?the tag-probabilities patch}")"
am_patch="$(realpath "${5:?the ambiguous-multiwords patch}")"
cd "$src"

fail() { echo "patch-freeling.sh: $*" >&2; exit 1; }

# The three files the name-class patch changes must be FreeLing 4.2's.
sha256sum -c --quiet - <<'EOF' || fail "not FreeLing 4.2's np.cc, np.h and nec.cc"
2934779917d1041111f9750effb78500a8bfbba9057bfbf43c1cc22cac51a622  src/libfreeling/np.cc
f09274b49e0c72f99ced11ff386c0473dec8a692bed1c29c41e3dd5832550f7b  src/include/freeling/morfo/np.h
1e04d9fafb3423d41803030b3b29a5e14cf80e0f2dc18f1b50d458ba07525a5f  src/libfreeling/nec.cc
EOF
# The two files the known-roots patch changes must be FreeLing 4.2's.
sha256sum -c --quiet - <<'EOF' || fail "not FreeLing 4.2's suffixes.cc and suffixes.h"
2955d3d544c942772ed71707a4496f66bc9168cd8d2ee17c4c397cc4173f88ac  src/libfreeling/suffixes.cc
7895af5c58a98252466736283c30c9a3ebc005cac0bf3507553d9bfa5fa93d33  src/include/freeling/morfo/suffixes.h
EOF
# The twelve files the tag-probabilities and the ambiguous-multiwords patches
# change must be FreeLing 4.2's.
sha256sum -c --quiet - <<'EOF' || fail "not FreeLing 4.2's tagger, word, multiword and CoNLL files"
3e920ac0cf914aaf0a763c6ad6e9c18efa27c6a22ba9e0c582f1f087f8560695  src/include/freeling/morfo/hmm_tagger.h
a98bc53ffcfa5cef0f332ecf600567adb12296c90e78d7aed149326887e7e3c2  src/include/freeling/morfo/language.h
e436437c78d493f24069adb1a657e253150a721468cb8ff36d1266cc3cab196c  src/include/freeling/morfo/locutions.h
1adca7e4a5a70328d9d96b14ae99f137d584701bb69cefbba3b9a7f16551ab12  src/include/freeling/output/conll_handler.h
c44940523019c65f76c6e031f127ea2d77ce8e92840860935f9bfc522265ccff  src/libfreeling/hmm_tagger.cc
0df9c9db2152627cc3acf1bbdbfbd9d8e1a36799ee0597a663520fd6afe5310f  src/libfreeling/language.cc
3fff73d9a5d9fcf1c3cedea563bad0fda60eab0a8ab11321d535d4f0bffbd40f  src/libfreeling/locutions.cc
fa599770eda1a36b56edbb995985fe6c4717725c36e6d54322d7840cd15b71bf  src/libfreeling/output/conll_handler.cc
4bbe7ee6c0a81f03cad338c461ae3164d468e5f46fe634ea49316c859df79680  src/libfreeling/output/input_conll.cc
06e654f6d7c8582e7a3603bc378f9db8a11c9c03d46e9d0ad785d8a4a9395002  src/libfreeling/output/output_conll.cc
7923f95f77ee956ec7f9866d96bbde83bbebf6ece4b018e273446fbe0a9bce92  src/libfreeling/probabilities.cc
659ac7e2ac65e43ce4763d314726e6dcfdaffa74fb425a98f4156c0f3b7d6d44  src/libfreeling/tagger.cc
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
# FreeLing Old's compound analysis is off as shipped (compound analysis is
# off in every config, decided 261118).
grep -q '^CompoundAnalysis=no$' data/config/es-old.cfg \
    || fail "data/config/es-old.cfg: compound analysis is not off as FreeLing ships it"

# 13: FreeLing Old's parser files, where FreeLing 4.2 has them.
c=data/config/es-old.cfg
echo "dbb29e19b98fc56dcfbd6dc5267b0f4fc3bfa8f61e3212798bac0f840a1a2b7a  $c" | sha256sum -c --quiet - || fail "$c: not FreeLing 4.2's"
[ -f data/es/chunker/grammar-chunk.dat ] && [ -f data/es/dep_txala/dependences.dat ] || fail "FreeLing 4.2's parser files are not where es.cfg names them"
sed -i 's|^GrammarFile=\$FREELINGSHARE/es/grammar-dep\.dat$|GrammarFile=$FREELINGSHARE/es/chunker/grammar-chunk.dat|;
        s|^DepTxalaFile=\$FREELINGSHARE/es/dep/dependences\.dat$|DepTxalaFile=$FREELINGSHARE/es/dep_txala/dependences.dat|' "$c"
echo "4215d956fbd59aea416afce87b677c49a2d519e6bb6f558dbc39d35d3043dc3b  $c" | sha256sum -c --quiet - || fail "$c: the parser lines are not as change 13 makes them"

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

# 10: a known root is not taken apart (the affix analysis).
patch -p1 --forward --batch < "$kr_patch"
sha256sum -c --quiet - <<'EOF' || fail "suffixes.cc and suffixes.h are not as the known-roots patch makes them"
f867ccfd8d00e8abfd2d003b4c3af4456059ca8d47879a20a0476ab1e1d5f99e  src/libfreeling/suffixes.cc
f003ed4307458ffd7f9ea8f9fa7bff02facdb9466c9c406ebd8866152ab02b32  src/include/freeling/morfo/suffixes.h
EOF

# 11 and 12: the probability columns, then the ambiguous multiwords.
patch -p1 --forward --batch < "$tp_patch"
patch -p1 --forward --batch < "$am_patch"
sha256sum -c --quiet - <<'EOF' || fail "the tagger, word, multiword and CoNLL files are not as the two patches make them"
223b224c5f20bd9b9387a6d1b165ab386bc41a7da806deacd030892a8bdb75e2  src/include/freeling/morfo/hmm_tagger.h
c4f4233b9eb74c59772108829906b90c7934e710604243ce86f19aae460cb269  src/include/freeling/morfo/language.h
547da73c035100344842967cfef639f909b10c8f145c733558a14bad7ca5e339  src/include/freeling/morfo/locutions.h
2714c1e553274b7c967c12f538450aa413f20a2c467821d6b7fda38ef65a7d6a  src/include/freeling/output/conll_handler.h
784e9b9106c77fa53841ac004b22f8e8ddefd14cf04891ab37f85ba1c7f45c03  src/libfreeling/hmm_tagger.cc
8733ac79e99a0042b5c6e263a06d631b9bcb6a9b54f4d227c7c1177e20667d4b  src/libfreeling/language.cc
0ffa8faefbf5ce14f9a0f63b72780015f25dc2851bfc581ec9901d9f8137a5f1  src/libfreeling/locutions.cc
9333892e4868c55b984452f9f745b9b58c06fcb8174e47eeaab31057d8aec32e  src/libfreeling/output/conll_handler.cc
2065b9dcf2285944e3770bad1daf2e9b477c1a7678ce5e7050ef3e5eb38f7bed  src/libfreeling/output/input_conll.cc
985a429a175ef470e1eae87055452aa45c8a2f6f137eb7f6f06ef5084d2a5e37  src/libfreeling/output/output_conll.cc
aa0ebeb97a329cf9dd7ad9b26a698cff287f51144fc65ce7f720b98edb5177ab  src/libfreeling/probabilities.cc
ce27745a27d280f2c6995397f7d308963d45c11e9b1ae1a28675d343747e753d  src/libfreeling/tagger.cc
EOF

echo "patch-freeling.sh: every change applied"
