#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# VERSION 2.8.1
#
# freeling_escl_build.py -- build FreeLing es-CL 2027, the Chilean Spanish
# data for FreeLing 4.2, from FreeLing's own Spanish source files, the CSLD
# grammatical lists and the COSCACH spelling decisions.
#
# It reads (never writes):
#   FreeLing 4.2's Spanish source files, in the FreeLing source tree
#   (default /home/user/build/FreeLing-4.2), each checked against the
#   sha256 of FreeLing 4.2 (a changed file refuses the build):
#       data/es/dictionary/header, data/es/dictionary/entries/MM.*
#                                   the Spanish dictionary, built here
#       data/es/np.dat              the name recognizer's rules
#       data/es/quantities.dat      currencies and measures
#       data/es/tagset.dat          the Spanish tagset (to check the Chilean
#                                   one against)
#       data/es/tagger.dat          the Spanish tagger (only its word
#                                   frequencies are read, to mark in
#                                   NAME-WEIGHTS.tsv the decided names that
#                                   are also common Spanish words)
#       data/es/probabilitats.dat   the Spanish probabilities (only the
#                                   lines of the decided names are read:
#                                   they are the basis of every line the
#                                   build writes for a decided name)
#       data/common/nec/cities.dat  the name classifier's city list, and
#       data/common/nec/cities-CL.dat  FreeLing's own Chilean version of it
#                                   (the world list plus 381 Chilean places)
#       data/es/nerc/data/gazLOC-c.dat  the classifier's list of whole place
#                                   names
#       data/es/nerc/data/gazPER-c.dat  its list of whole person names
#       data/es/nerc/nec/nec-ab-poor1.dat  the classifier's file, to which
#                                   the class shares are added
#       data/es/locucions.dat       FreeLing's general Spanish multiwords,
#                                   merged into the Chilean multiword file
#                                   (decided 261112: FreeLing reads one
#                                   multiword file, and the CSLD configs name
#                                   the Chilean one, so without the merge
#                                   every general multiword is lost)
#   No installed FreeLing file and no archived (deprecated) file is read,
#   and no es-cl.cfg at all: FreeLing's es-cl config, the basis of the
#   release's two configs, is carried in this script (decided 261113).
#   <project root>/linguistic-derived/grammatical-lists/individual/
#       contemporary/freeling-cl/CL.*.GRAM.txt      the Chilean lists
#       contemporary/freeling-cl/metadata/tagset.dat the Chilean tagset
#   <project root>/linguistic-derived/people-names-list/gazPER-p.dat
#                                   the Chilean list of person-name parts
#                                   (merged 291026), which replaces
#                                   FreeLing's
#   <project root>/software/10-Infrastructure/freeling/escl-sources/*.tsv
#                                   the build's own sources: the decisions
#                                   of the COSCACH spelling review that the
#                                   build reads, and the name decisions
#                                   (fixed-name-classes,
#                                   person-name-removals, place-only-forms,
#                                   sentence-start-classes,
#                                   name-class-shares). The real files live
#                                   here; the COSCACH decisions folder holds
#                                   links to them, so there is one copy.
#   the COSCACH decisions folder (LINKED_DECISIONS below), only to check
#                                   the links: every file of a kind the
#                                   build reads must be a link there to its
#                                   file in escl-sources, and every file in
#                                   escl-sources must have its link. Any
#                                   other state refuses the build.
#   the build tree's Chilean data, as deployed
#       /home/user/build/FreeLing-4.2/data/es/es-cl/probabilitats.dat
#       /home/user/build/FreeLing-4.2/data/es/es-cl/locucions.dat
#   FreeLing_es-CL_2027_README.md, the deploy and config tools and their
#   READMEs next to this script, the change to FreeLing's name recognizer
#   and classifier in ../patches/ (the patch, its README and the three
#   changed source files), and
#   /home/user/MyScripts/linguistics/explode-*-4-FreeLing.pl:
#   all copied into the release's software/ folder; the packaging of
#   FreeLing 4.2 with this release for Fedora, Debian and Ubuntu, in
#   ../packaging/ (the scripts and their READMEs into the release's
#   packaging/ folder, packages.yml, the GitHub workflow that builds the
#   packages, into .github/workflows/); every escl-sources
#   file read, and escl-sources/README.md, are copied into its
#   sources/escl-sources/ folder
#
# It writes the release folder (default
#   /home/user/FreeLing_es-CL_2027 ),
# moving a previous build to
#   /home/user/software/deprecated/
#       FreeLing_es-CL_2027.DEPRECATED-YYMMDD[letter]
# Nothing is installed: freeling_escl_deploy.py does that.
#
# THE RELEASE IS PUBLIC (decided 261112). Every file of the release that is
# not data (the READMEs, the build report, the software, the sources) is
# written with the private paths of the privacy file
#   freeling-release-privacy.tsv, in the folder above this script's
# replaced by public ones, and no file of the release, data included, may
# contain a private term of that file: one found, and nothing is written
# (exit 1). The privacy file is private and is never copied into the
# release. The release carries FreeLing's license, the GNU Affero General
# Public License 3.0 (agpl-3.0.txt beside this script), as LICENSE.
#
# TWO DICTIONARIES ARE BUILT (decided 261109):
#   data/es/es-cl/dicc.src             the default: contemporary Chilean
#       Spanish. vos is always voseo (PP2CS0V only), and an -is form with a
#       voseo and a vosotros reading of the same verb and tense keeps the
#       voseo reading only (salis, comis).
#   data/es/es-cl/historical/dicc.src  the 19th-century dictionary, for
#       historical corpora only: vos also keeps its polite reading
#       (PP2CS0P), the -is forms keep both readings (vosotros preferred),
#       and the 19th-century Chilean spellings, the attested old-accent
#       spellings and their multiwords are added, with its own
#       probabilitats.dat and locucions.dat (decided 261112, 261113). Used
#       only when asked for: data/config/es-cl-19th-century.cfg.
#
# What it does, in order (every line-level change goes to CHANGELOG.tsv,
# every decision row to DECISIONS.tsv):
#   1  builds the Spanish dictionary from FreeLing's entries files, exactly
#      as FreeLing's build-dict does
#   2  fixes the Chilean lists (the broken ir lines, erih, vos, habis, veis,
#      dai, the vais/dais/veis/deis voseo readings, capital letters, a bad
#      tag) and removes the voseo forms of erar
#   3  repairs voseo forms of irregular verbs that were conjugated as if
#      regular, checked against the Spanish dictionary's own paradigms
#   4  adds the decided words (CL.additions): names, nouns and adjectives
#      with their other number and gender, adverbs, interjections, and new
#      verbs with their whole paradigm, voseo included, copied from known
#      verbs with the same ending; the verb forms decided one by one
#      (verb-form-readings), with the Chilean imperatives hace, dice, pone
#   5  applies the interjection decisions: lemmas, removals, rare ones
#   6  generates the spelling variants of every voseo form (CL.variants)
#   7  adds the person, place and organization lists (CL.names)
#   8  adds the non-standard forms kept in the text (CL.nonstandard) and the
#      misspelt forms the text corrects, read as their corrections
#      (CL.common-misspellings); withdraws the proper-noun reading of every decided
#      name that is also a common noun or a verb (decided 261110b)
#   9  applies the standard lemmas, and makes every place-only form a
#      place and nothing else (place-only-forms: Arica is never a form of
#      aricar, decided 261110d; Barbados, Chanco, Pirque, decided 261110e)
#   9c adds fué, fuí, dió, vió, á, é, ó, ú with the readings of their
#      modern forms (CL.old-accents)
#   9d adds every accented form written without its accents, when that is
#      not already a word and comes from one form only
#      (CL.common-misspellings)
#  10  builds the two dictionaries (the 19th-century one with its
#      spellings, attested spellings and decided words), the tuteo-tagged
#      one (zipped), and
#      FreeLing's own entries and remove files for both, and checks that
#      FreeLing's build-dict would give the same dictionaries
#  11  writes probabilitats.dat (lemma preferences, the decided names, rare
#      interjections, mm, the 20% future against the imperfect subjunctive,
#      poder over podar, the share of a reading added beside a word's own
#      at the start of a sentence (sentence-start-classes)), locucions.dat
#      (FreeLing's general multiwords merged in, the Chilean entry winning
#      for a key in both; ya_poh, the multiword interjections, the decided
#      multiwords of locutions and locution-removals), quantities.dat (Chilean peso,
#      UF, UTM, euro)
#  11b the names (decided 261110d, 261110e, 261110f, 261110g): the
#      classifier's lists and file, as FreeLing names them, so it reads
#      them in place of its own:
#        common/nec/cities.dat      FreeLing's two city lists merged, plus
#                                   every place name of the Chilean data
#        es/nerc/data/gazLOC-c.dat  FreeLing's place names plus the same
#        es/nerc/data/gazPER-c.dat  FreeLing's person names, minus the
#                                   places it held (Concepción, Lima ...)
#        es/nerc/data/gazPER-p.dat  the Chilean person-name parts
#        es/nerc/nec/nec-ab-poor1.dat  FreeLing's classifier file with the
#                                   class shares of name-class-shares
#                                   (<ClassShares>); FreeLing without the
#                                   name-class change stops on it
#      and the recognizer's two rule files, for FreeLing with the
#      name-class change (../patches/), each with the readings of
#      sentence-start-classes for its kind of text (a form may have one
#      rule for written texts and another for speech, decided 261110g):
#        es-cl/np.dat         written texts: every Chilean locality,
#                             country and continent is a place inside a
#                             sentence; a word that is also a common noun
#                             or an adjective at the start of a sentence
#                             is left to FreeLing (CODICACH)
#        es-cl/np-speech.dat  transcribed speech, where a line is an
#                             utterance: the same at the start of a line
#                             (COSCACH)
#  12  checks the Chilean tagset (by sha256, and against FreeLing's Spanish
#      tagset plus the voseo values only) and decodes every tag of every
#      file written; one tag it cannot decode refuses the build
#
# Executes by default. --dry-run builds and checks in memory and writes
# nothing. Linux. Standard library only.

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import math
import os
import re
import shutil
import sys
import textwrap
import time
import unicodedata
import zipfile
from pathlib import Path

VERSION = "2.8.1"
RELEASE = "FreeLing es-CL 2027"

SOURCE_TREE = Path("/home/user/build/FreeLing-4.2")
BUILD_TREE = Path("/home/user/build/FreeLing-4.2/data/es/es-cl")
OUT = Path("/home/user/software/"
           "FreeLing_es-CL_2027")
GRAM_REL = Path("linguistic-derived/grammatical-lists/individual/"
                "contemporary/freeling-cl")
TAGSET_REL = GRAM_REL / "metadata" / "tagset.dat"
DECISIONS_REL = Path("software/10-Infrastructure/freeling/escl-sources")
# The COSCACH decisions folder, which holds links to the escl-sources files
# (decided 261112: one copy of each file, in the FreeLing tree).
LINKED_DECISIONS = Path("/home/user/corpora/"
                        "050-Spelling-normalized/COSCACH/_processing-records/"
                        "spelling-review/decisions")
# The kinds of decision file the build reads (the part of the name before
# "--"). freeling_escl_sources_move.py moves exactly these.
BUILD_STEMS = (
    "all-corpora-replacements", "correction-lemmas",
    "dictionary-addition-removals", "dictionary-additions",
    "dictionary-words", "historical-attested-spellings",
    "dictionary-additions-all-rounds-standardized", "dictionary-variants",
    "fixed-name-classes", "interjection-removals", "interjections",
    "lemma-standardization", "locution-removals", "locutions",
    "name-class-shares", "person-name-removals",
    "place-only-forms", "sentence-start-classes", "text-correction-removals",
    "text-corrections", "verb-form-readings",
)
# Kinds that are not decisions of the COSCACH spelling review: they live
# only in escl-sources and need no link in the COSCACH decisions folder.
UNLINKED_STEMS = ("locution-removals", "locutions", "dictionary-words",
                  "historical-attested-spellings")
# The hand-edit file of the dictionary (decided 261112): exact dictionary
# lines (form, lemma, tag), applied at every build. It has no round: it is
# edited in place, and its # lines say what goes in it.
HAND_EDITS_NAME = "dictionary-hand-edits.tsv"
GAZPER_P_REL = Path("linguistic-derived/people-names-list/gazPER-p.dat")
README_NAME = "FreeLing_es-CL_2027_README.md"

# FreeLing 4.2's Spanish source files, by sha256 (from FreeLing's own
# repository, tag 4.2). A changed file refuses the build.
FL42 = {
    "data/es/dictionary/header":
        "57bc21e54083bba6c6810743453fa8b62171c3481440fbe91a9a9648009206fd",
    "data/es/dictionary/entries/MM.adj":
        "0bfdce1ec95f3a5128e961b018118da1c5f34b3a3a8b5610642020e526c8f616",
    "data/es/dictionary/entries/MM.adv":
        "38acce505fe58f2a30597d8b949bb57606fbe93d9951a9722784188b6ba99b36",
    "data/es/dictionary/entries/MM.int":
        "bdd6cd33cde58eb0ca4d232515eb7e103a3e7028125eeb8fa274df93703ea5e3",
    "data/es/dictionary/entries/MM.nom":
        "f8115bf4993b26f22369249b039edeffa60656a0b65ec9e9d8d44e12904e78ec",
    "data/es/dictionary/entries/MM.tanc":
        "d7abd54ea3d8f4cdafaadffcbb5a1e63b94a2b12b1f2db525ee8b63a5a1952cb",
    "data/es/dictionary/entries/MM.vaux":
        "7067a5474d942ea3ae32171d0a483b7cb2fe4add8ba298eb22b230c5c797b133",
    "data/es/dictionary/entries/MM.verb":
        "72a0dafe3df20e2d23a6f5b823240aaeb01f4715b9cf373970991da086e18033",
    "data/es/np.dat":
        "85efde501a917a44ffa537847648a828ed96a68c10f4e311a42c60834a2f076e",
    "data/es/quantities.dat":
        "0dae3e3c28ac1a88e6c9219356f1431ec042879e50a4c9ea49ca7abb47ea2c0f",
    "data/es/tagset.dat":
        "5b1faf7e5d74bdf5ff80bbfe16e95af236ebe24433899ce0ef8ad1ce67a8aee2",
    "data/es/tagger.dat":
        "3e86bc15a91e49078d5f7d54cb9da252bc5360451567af95d4a48de6c6caa89c",
    "data/es/probabilitats.dat":
        "f4e598b3e31754781fac5cc81f806d85be1e25af988e40760076c8a589894cd5",
    "data/es/locucions.dat":
        "c4440d93ad51ea4cf3c224cbb69d978aa86fdbb05a9e758b42fa98a46d2d7913",
    "data/common/nec/cities.dat":
        "b29f9221229e86a039bcc1ba09d8889e244b81aab0821391cd30b2448826b585",
    "data/common/nec/cities-CL.dat":
        "cc73038c9b4b8a276e7bfb2d04fec8f8593a9618434431c26e183b22ab6b1cf2",
    "data/es/nerc/data/gazLOC-c.dat":
        "57008ccfe07096d6986556f6c4186529cde239cbe222c2ae9837c63765077909",
    "data/es/nerc/data/gazPER-c.dat":
        "be4817b954e8e062c4dbb9b714effc5b672c45aa9b89e0d7d06a108b90de59bd",
    "data/es/nerc/nec/nec-ab-poor1.dat":
        "4469ae51bf0a0004f293558f93fba6ff54d574b7c12abc2ba1048f67c04e4dc6",
}

# FreeLing 4.2's own es-cl config (data/config/es-cl.cfg, sha256 below),
# the basis of the release's two configs. It is carried here, not read from
# the source tree, so that no es-cl.cfg on this machine is read by the build
# (decided 261113: the CSLD tags only with csld-es-cl.cfg and the configs
# written from it). Trailing spaces are kept out of the text and put back on
# the lines listed, so that the text is FreeLing's byte for byte.
ES_CL_CFG_SHA = ("2934d4320a5690d4fbfb945325a7df20"
                 "cb99d3e0393e8b8d7e6d3ddb37e8a42c")
ES_CL_CFG_TRAILING = (5, 45, 73, 82, 95, 98)
ES_CL_CFG_TEXT = """\
##
#### default configuration file for Spanish analyzer
##

#### General options
Lang=es
Locale=default

### Tagset description file, used by different modules
TagsetFile=$FREELINGSHARE/es/tagset.dat

#### Trace options. Only effective if we have compiled with -DVERBOSE
#
## Possible values for TraceModule (may be OR'ed)
#define SPLIT_TRACE         0x00000001
#define TOKEN_TRACE         0x00000002
#define MACO_TRACE          0x00000004
#define OPTIONS_TRACE       0x00000008
#define NUMBERS_TRACE       0x00000010
#define DATES_TRACE         0x00000020
#define PUNCT_TRACE         0x00000040
#define DICT_TRACE          0x00000080
#define SUFF_TRACE          0x00000100
#define LOCUT_TRACE         0x00000200
#define NP_TRACE            0x00000400
#define PROB_TRACE          0x00000800
#define QUANT_TRACE         0x00001000
#define NEC_TRACE           0x00002000
#define AUTOMAT_TRACE       0x00004000
#define TAGGER_TRACE        0x00008000
#define HMM_TRACE           0x00010000
#define RELAX_TRACE         0x00020000
#define RELAX_TAGGER_TRACE  0x00040000
#define CONST_GRAMMAR_TRACE 0x00080000
#define SENSES_TRACE        0x00100000
#define CHART_TRACE         0x00200000
#define GRAMMAR_TRACE       0x00400000
#define DEP_TRACE           0x00800000
#define UTIL_TRACE          0x01000000

TraceLevel=3
TraceModule=0x0000

## Options to control the applied modules. The input may be partially
## processed, or not a full analysis may me wanted. The specific
## formats are a choice of the main program using the library, as well
## as the responsability of calling only the required modules.
## Valid input/output formats are: plain, token, splitted, morfo, tagged, parsed
InputLevel=text
OutputLevel=tagged

# consider each newline as a sentence end
AlwaysFlush=no

#### Tokenizer options
TokenizerFile=$FREELINGSHARE/es/tokenizer.dat

#### Splitter options
SplitterFile=$FREELINGSHARE/es/splitter.dat

#### Morfo options
AffixAnalysis=yes
CompoundAnalysis=yes
MultiwordsDetection=yes
NumbersDetection=yes
PunctuationDetection=yes
DatesDetection=yes
QuantitiesDetection=yes
DictionarySearch=yes
ProbabilityAssignment=yes
DecimalPoint=,
ThousandPoint=.
LocutionsFile=$FREELINGSHARE/es/es-cl/locucions.dat
QuantitiesFile=$FREELINGSHARE/es/quantities.dat
AffixFile=$FREELINGSHARE/es/afixos.dat
CompoundFile=$FREELINGSHARE/es/compounds.dat
ProbabilityFile=$FREELINGSHARE/es/es-cl/probabilitats.dat
DictionaryFile=$FREELINGSHARE/es/es-cl/dicc.src
PunctuationFile=$FREELINGSHARE/common/punct.dat
ProbabilityThreshold=0.001

# NER options
NERecognition=yes

# config file for "crf" machine learning NERC
# (recognition and classification in a single step)
NPDataFile=$FREELINGSHARE/es/nerc/nerc/nerc.dat

# config file for "basic" rule based NER
#NPDataFile=$FREELINGSHARE/es/np.dat

# config file for "bio" machine learning NER
# NPDataFile=$FREELINGSHARE/es/nerc/ner/ner-ab-poor1.dat
# NPDataFile=$FREELINGSHARE/es/nerc/ner/ner-ab-rich.dat
# "rich" model is trained with rich gazetteer. Offers higher accuracy but
# requires adapting gazetteer files to have high coverage on target corpus.
# "poor1" model is trained with poor gazetteer. Accuracy is splightly lower
# but suffers small accuracy loss the gazetteer has low coverage in target
# corpus. If in doubt, use "poor1" model.

## Phonetic encoding of words.
Phonetics=no
PhoneticsFile=$FREELINGSHARE/es/phonetics.dat

## NEC options. See README in common/nec
NEClassification=no
NECFile=$FREELINGSHARE/es/nerc/nec/nec-ab-poor1.dat
#NECFile=$FREELINGSHARE/es/nerc/nec/nec-ab-rich.dat

## Sense annotation options (none,all,mfs,ukb)
SenseAnnotation=none
SenseConfigFile=$FREELINGSHARE/es/senses.dat
UKBConfigFile=$FREELINGSHARE/es/ukb.dat

#### Tagger options
Tagger=hmm
TaggerHMMFile=$FREELINGSHARE/es/tagger.dat
TaggerRelaxFile=$FREELINGSHARE/es/constr_gram-B.dat
TaggerRelaxMaxIter=500
TaggerRelaxScaleFactor=670.0
TaggerRelaxEpsilon=0.001
TaggerRetokenize=yes
TaggerForceSelect=tagger

#### Parser options
GrammarFile=$FREELINGSHARE/es/chunker/grammar-chunk.dat

#### Dependence Parser options
DependencyParser=txala
DepTxalaFile=$FREELINGSHARE/es/dep_txala/dependences.dat
DepTreelerFile=$FREELINGSHARE/es/treeler/dependences.dat

# Semantic Role Labelling options
SRLTreelerFile=$FREELINGSHARE/es/treeler/srl.dat

#### Coreference Solver options
CorefFile=$FREELINGSHARE/es/coref/relaxcor/relaxcor.dat
SemGraphExtractorFile=$FREELINGSHARE/es/semgraph/semgraph-SRL.dat
"""


def stock_es_cl_cfg() -> str:
    """FreeLing 4.2's es-cl config, exactly as FreeLing ships it."""
    lines = ES_CL_CFG_TEXT.split("\n")[:-1]
    for n in ES_CL_CFG_TRAILING:
        lines[n - 1] += " "
    return "\n".join(lines) + "\n"

# The Spanish dictionary those entries give (FreeLing's installed
# es/dicc.src): the build checks that it rebuilds it byte for byte.
ES_DICC_SHA = "b173f77f9a2d1100f83bbf7f287182579e7a768028529ff7aaa69dbb5c8b35fd"
# The approved Chilean tagset (decided 261109): FreeLing's Spanish tagset
# plus the voseo value on the verb's gender and the pronoun's politeness.
TAGSET_SHA = "4f8def5440de2ffe6b73b11fc309ac8c6817b0f785ddb8ad41f8e5c875f137e8"
TAGSET_CHANGES = [(" polite/P:yes\n", " polite/P:yes;V:voseo\n"),
                  (" gen/F:feminine;M:masculine;C:common\nZ ",
                   " gen/F:feminine;M:masculine;C:common;V:voseo\nZ ")]
# Forms of tu: never a voseo tag (decided 261109).
TU_FORMS = {"tú", "tu", "te", "ti", "contigo"}

# The software that makes the release, copied into its software/ folder.
SOFTWARE_HERE = ["freeling_escl_build.py", "freeling_escl_build_README.md",
                 "freeling_escl_deploy.py", "freeling_escl_deploy_README.md",
                 "freeling_csld_configs.py", "freeling_csld_configs_README.md",
                 "freeling_escl_sources_move.py",
                 "freeling_escl_sources_move_README.md", README_NAME]
# The change to FreeLing's name recognizer (decided 261110d), in
# ../patches/ beside this script's folder, copied into software/patches/.
# The packaging of FreeLing 4.2 with this release for Fedora, Debian and
# Ubuntu (decided 261112), in ../packaging/ beside this script's folder:
# copied into the release's packaging/ folder, and the GitHub workflow that
# builds the packages into .github/workflows/ (the release is the GitHub
# repository).
PACKAGING_FILES = ["patch-freeling.sh", "patch-freeling_README.md",
                   "build-freeling.sh", "build-freeling_README.md",
                   "test-freeling.sh", "test-freeling_README.md",
                   "make-nfpm-config.py", "make-nfpm-config_README.md",
                   "postinstall-deb.sh", "postinstall-deb_README.md",
                   "ldconfig.sh", "ldconfig_README.md",
                   "install-data.sh", "install-data_README.md"]
PACKAGING_WORKFLOW = "packages.yml"
PATCH_FILES = ["freeling-4.2-np-classes.patch",
               "freeling-4.2-np-classes_README.md", "np.cc", "np.h", "nec.cc"]
EXPLODE_DIR = Path("/home/user/MyScripts/linguistics")
EXPLODE_FILES = ["explode-ADJECTIVES-4-FreeLing.pl",
                 "explode-ADVERBS-4-FreeLing.pl",
                 "explode-INTERJECTIONS-4-FreeLing.pl",
                 "explode-NOUNS-ALL-GENDERS-4-FreeLing.pl",
                 "explode-NOUNS-ONLY-PLURALIZE-4-FreeLing.pl",
                 "explode-VERBS-4-FreeLing.pl",
                 "explode-VERBS-4-FreeLing_README.md"]

# The privacy file (private: never copied into the release), in the folder
# above this script's: TAB-separated, header "private<TAB>public"; a row
# with a public text is a replacement, a row without one a term that may
# appear nowhere in the release. Every private text of a replacement is a
# term too. Replacements are made longest first, as written; terms are
# searched for in any case.
PRIVACY_NAME = "freeling-release-privacy.tsv"
# FreeLing 4.2 is under the GNU Affero General Public License, version 3 or
# later; the release, made from its files, is under the same license
# (decided 261112). The text, as the FSF publishes it, beside this script,
# goes into the release as LICENSE.
LICENSE_NAME = "agpl-3.0.txt"
LICENSE_SHA = "0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0"
# The release's data: checked for private terms, never rewritten.
DATA_PARTS = ("data/", "grammatical-lists/", "tuteo-tagged-dictionary/")

HEADER = "<IndexType>\nDB_MAP\n</IndexType>\n<Entries>\n"

# The lists, in the order of the entries files. The verb, auxiliary and
# pronoun lists are read in their voseo-tag version.
LISTS = [("adj", "CL.adj.GRAM.txt"), ("adv", "CL.adv.GRAM.txt"),
         ("demonyms", "CL.demonyms.GRAM.txt"), ("int", "CL.int.GRAM.txt"),
         ("nom", "CL.nom.GRAM.txt"), ("tanc", "CL.tanc.Vos-V.GRAM.txt"),
         ("vaux", "CL.vaux.Vos-V.GRAM.txt"),
         ("verb", "CL.verb.Vos-V.GRAM.txt")]
NAME_LISTS = [("peoplenames", "CL.peoplenames.GRAM.txt"),
              ("orgnames", "CL.orgnames.GRAM.txt"),
              ("cities", "CL.cities.GRAM.txt")]
# Proper-noun classes of the lists (decided 261101).
NAME_TAG = {"peoplenames": "NP00SP0", "cities": "NP00G00"}
LOCUTION_TAG_FIX = {("chuchunco_city", "NPFS000"): "NP00G00",
                    ("*", "AQ0NC00"): "AQ0CN00",
                    # FreeLing's general file tags tal y cual as Fs, a
                    # punctuation mark; it is used as cual is (PI0CS00).
                    ("tal_y_cual", "Fs"): "PI0CS00"}
# The entries files the build writes, in order.
SOURCES = ["adj", "adv", "demonyms", "int", "nom", "tanc", "vaux", "verb",
           "variants", "names", "additions", "nonstandard",
           "common-misspellings", "old-accents", "standard-lemmas"]

# The accented one-syllable forms written before the 1952 reform, in both
# dictionaries (decided 261112): each gets every reading of its modern form.
OLD_ACCENTS = [("fué", "fue"), ("fuí", "fui"), ("dió", "dio"),
               ("vió", "vio"), ("á", "a"), ("é", "e"), ("ó", "o"), ("ú", "u")]
# Common misspellings (decided 261112): every correctly spelled form with
# a written accent or a diaeresis, written without them, when the result
# is not already a word and comes from that one form only.
STRIP_MARKS = str.maketrans("áéíóúü", "aeiouu")
ACCENTS_ONLY = str.maketrans("áéíóú", "aeiou")
# The 19th-century dictionary (the historical one; decided 261112, 261113):
# the spellings of Bello and García del Río (1823), Sarmiento (1843), the
# Chilean orthography of 1844 and the Chilean neographers (1890s to early
# 1900s), generated from every form of the dictionary and given the
# readings of the form they come from. A word may show any combination of
# them; a rule changes every place it applies in a word. The order matters:
# g before e/i becomes j before u is dropped from gue/gui. Accents are
# never dropped (decided 261112).
X_TO_J = {"méxico": "méjico", "mexicano": "mejicano", "mexicana": "mejicana",
          "mexicanos": "mejicanos", "mexicanas": "mejicanas",
          "texas": "tejas", "oaxaca": "oajaca", "ximénez": "jiménez",
          "quixote": "quijote", "xalapa": "jalapa"}
_V = "aeiouáéíóúü"
HIST_RULES = [
    ("g>j", "g before e or i written j (jente, jeneral)",
     lambda w: re.sub(r"g(?=[eiéí])", "j", w)),
    ("x>j", "x for the j sound written j (Méjico, Tejas)",
     lambda w: X_TO_J.get(w, w)),
    ("x>cs", "x before a vowel written cs (ecsamen)",
     lambda w: re.sub(r"x(?=[%s])" % _V, "cs", w)),
    ("x>s", "x before a consonant written s (esplicar, estranjero)",
     lambda w: re.sub(r"x(?=[^%s])" % _V, "s", w)),
    ("y>i", "y as a vowel written i (rei, mui, hoi, i)",
     lambda w: re.sub(r"y(?![%s])" % _V, "i", w)),
    ("c>s", "c before e or i written s (sielo, sienzia)",
     lambda w: re.sub(r"c(?=[eiéí])", "s", w)),
    ("c>z", "c before e or i written z (soziedad, zientífica)",
     lambda w: re.sub(r"c(?=[eiéí])", "z", w)),
    ("z>s", "z written s (sapato)", lambda w: w.replace("z", "s")),
    ("qu>q", "qu written q (qerer, qeso)",
     lambda w: re.sub(r"qu(?=[eiéí])", "q", w)),
    ("qu>k", "qu written k (keso)",
     lambda w: re.sub(r"qu(?=[eiéí])", "k", w)),
    ("c>k", "c for the k sound written k (kasa, elektrizidad)",
     lambda w: re.sub(r"c(?![eiéíh])", "k", w)),
    ("c>q", "c for the k sound written q (qasa, qomerziantes)",
     lambda w: re.sub(r"c(?![eiéíh])", "q", w)),
    ("gu>g", "the silent u of gue, gui dropped (gerra, giso)",
     lambda w: re.sub(r"gu(?=[eiéí])", "g", w)),
    ("h-", "silent h dropped before a vowel (ombre, umano)",
     lambda w: re.sub(r"(?<!c)h(?=[%s])" % _V, "", w)),
    ("v>b", "v written b (bino, Balparaíso)", lambda w: w.replace("v", "b")),
    ("r>rr", "the trill written rr at the start and after n, l, s "
     "(rrazional, Enrrique)",
     lambda w: re.sub(r"(^|(?<=[nls]))r(?!r)", "rr", w)),
]
# The rules the Chilean orthography of 1844 adopted (decided 261113): only
# they may give a spelling that is already a word, and the reading they
# add to it is then nearly impossible on its own in the 19th-century
# probabilitats.dat. A spelling another rule gives that is already a word
# is not added.
BELLO_ADOPTED = ("g>j", "y>i", "x>s")
# Bello spellings that are also other words, decided one by one for the
# 19th-century dictionary (decided 261113). A list gives the readings the
# form keeps, and only those; a word in quotes, the readings of that word;
# "no voseo", its readings without the voseo ones.
HIST_READINGS = {
    "i": [("y", "CC"), ("i", "NCFS000")],   # the conjunction y, 99%
    "rei": [("rey", "NCMS000")],            # never the name Rei
    "lei": [("ley", "NCFS000")],            # never the plural of leu
    "hai": "hay",                           # always hay
    "soi": "no voseo",                      # soy, never voseo
}
# Their probabilities (short tag -> percent), and those of testo.
HIST_PROBS = {"i": {"CC": 99, "NC": 1}, "testo": {"NC": 90, "VMI": 10}}


def hist_variants(word: str, rules):
    """Every spelling the rules give for word, any combination of them,
    in their order; the word itself is left out."""
    out = {word}
    for _, _, f in rules:
        out |= {f(x) for x in out}
    out.discard(word)
    return out


def key_variants(key: str, rules):
    """The same for a multiword key: the <lemma> tokens are left alone."""
    toks = key.split("_")
    plain = [i for i, t in enumerate(toks) if not t.startswith("<")]
    out = {key}
    for _, _, f in rules:
        new = set()
        for k in out:
            t = k.split("_")
            for i in plain:
                t[i] = f(t[i])
            new.add("_".join(t))
        out |= new
    out.discard(key)
    return out


def accent_kind(old: str, modern: str) -> str:
    """How an attested spelling differs from the modern one when both are
    the same letters but for the accents: extra (ménos), moved (ráices) or
    missing (colaboracion)."""
    diff = [i for i, (a, b) in enumerate(zip(old, modern)) if a != b]
    o = any(old[i] in "áéíóú" for i in diff)
    m = any(modern[i] in "áéíóú" for i in diff)
    if o and not m:
        return "extra"
    if m and not o:
        return "missing"
    return "moved"


def write_config(text: str, folder: str, problems, name: str,
                 compounds: bool = True) -> str:
    """FreeLing's es-cl config with the Chilean tagset and quantities and
    the dictionary, probabilities and multiwords of `folder` (es/es-cl or
    es/es-cl/historical). Without compounds, compound analysis is off and
    no compound file is named: FreeLing builds its compound analyzer from
    every form of the dictionary with foma, whose stack holds 2,097,152
    entries, fewer than the 19th-century dictionary has (FreeLing stops
    with "Stack full!")."""
    swaps = [("TagsetFile=$FREELINGSHARE/es/tagset.dat",
              "TagsetFile=$FREELINGSHARE/es/es-cl/tagset.dat"),
             ("QuantitiesFile=$FREELINGSHARE/es/quantities.dat",
              "QuantitiesFile=$FREELINGSHARE/es/es-cl/quantities.dat"),
             ("LocutionsFile=$FREELINGSHARE/es/es-cl/locucions.dat",
              "LocutionsFile=$FREELINGSHARE/%s/locucions.dat" % folder),
             ("ProbabilityFile=$FREELINGSHARE/es/es-cl/probabilitats.dat",
              "ProbabilityFile=$FREELINGSHARE/%s/probabilitats.dat" % folder),
             ("DictionaryFile=$FREELINGSHARE/es/es-cl/dicc.src",
              "DictionaryFile=$FREELINGSHARE/%s/dicc.src" % folder)]
    if not compounds:
        swaps += [("CompoundAnalysis=yes", "CompoundAnalysis=no"),
                  ("CompoundFile=$FREELINGSHARE/es/compounds.dat",
                   "#CompoundFile=$FREELINGSHARE/es/compounds.dat")]
    lines = text.splitlines()
    for old, new in swaps:
        hits = [i for i, x in enumerate(lines) if x.strip() == old]
        if len(hits) != 1:
            problems.append("data/config/es-cl.cfg: %r is not there once "
                            "(for %s)" % (old, name))
            continue
        lines[hits[0]] = new
    return "\n".join(lines) + "\n"

# The ir paradigm, as it stands correct in the build tree (the newest list
# has 53 lines with an empty stem, "a ir VMM03S0" ..., and lacks 50 real
# ones). vais is vosotros only: the voseo form is vai.
IR_LINES = """\
fue VMIS3S0|fuera VMSI1S0|fuera VMSI3S0|fuerai VMSI2SV|fuerais VMSI2P0|\
fueran VMSI3P0|fueras VMSI2S0|fuere VMSF1S0|fuere VMSF3S0|fuereis VMSF2P0|\
fueren VMSF3P0|fueres VMSF2S0|fueron VMIS3P0|fuese VMSI1S0|fuese VMSI3S0|\
fueseis VMSI2P0|fuesen VMSI3P0|fueses VMSI2S0|fui VMIS1S0|fuimos VMIS1P0|\
fuiste VMIS2S0|fuisteis VMIS2P0|fuistes VMIS2SV|fuéramos VMSI1P0|\
fuéremos VMSF1P0|fuésemos VMSI1P0|iba VMII1S0|iba VMII3S0|ibai VMII2SV|\
ibais VMII2P0|iban VMII3P0|ibas VMII2S0|id VMM02P0|ida VMP00SF|\
idas VMP00PF|ido VMP00SM|idos VMP00PM|ir VMN0000|iremos VMIF1P0|\
irá VMIF3S0|irái VMIF2SV|irán VMIF3P0|irás VMIF2S0|iré VMIF1S0|\
iréis VMIF2P0|iría VMIC1S0|iría VMIC3S0|iríai VMIC2SV|iríais VMIC2P0|\
iríamos VMIC1P0|irían VMIC3P0|irías VMIC2S0|va VMIP3S0|vai VMIP2SV|\
vais VMIP2P0|vamos VMIP1P0|vamos VMM01P0|van VMIP3P0|vas VMIP2S0|\
vaya VMM03S0|vaya VMSP1S0|vaya VMSP3S0|vayamos VMM01P0|vayamos VMSP1P0|\
vayan VMM03P0|vayan VMSP3P0|vayas VMSP2S0|vayái VMSP2SV|vayáis VMSP2P0|\
ve VMM02S0|voy VMIP1S0|vái VMIP2SV|yendo VMG0000|íbamos VMII1P0"""
IR = [(f, "ir", t) for f, t in (x.split() for x in IR_LINES.split("|"))]

# ser: the forms the user confirmed (all kept), plus erih and erih with an
# accent, lost from the newest list.
SER_FORMS = {"erai", "eri", "erí", "eris", "erís", "erih", "eríh",
             "fuerai", "fuistes", "seai", "seái", "serái", "seríai", "soi",
             "so", "sos", "soh"}

FIX_ADD = [  # (list, form, lemma, tag, rule)
    ("vaux", "erih", "ser", "VSIP2SV", "ser variant lost from the newest list"),
    ("vaux", "eríh", "ser", "VSIP2SV", "ser variant lost from the newest list"),
    ("vaux", "habís", "haber", "VAIP2SV",
     "habis alternates with hai: the auxiliary reading"),
    ("verb", "veís", "ver", "VMIP2SV", "the voseo present of ver is veis with "
     "an accent"),
    ("verb", "dai", "dar", "VMIP2SV", "the voseo present of dar is dai"),
    ("verb", "deís", "dar", "VMSP2SV", "the voseo subjunctive of dar, as veis "
     "with an accent for ver"),
    ("tanc", "chorrocientos", "chorrocientos", "PI0MP00",
     "the masculine lacked the pronoun reading the feminine has"),
]
FIX_REMOVE = [  # (list, form, lemma, tag, rule)
    ("verb", "vais", "ir", "VMIP2SV", "vais is vosotros only; voseo is vai"),
    ("verb", "dais", "dar", "VMIP2SV", "dais is vosotros only; voseo is dai"),
    ("verb", "veis", "ver", "VMIP2SV", "veis is vosotros only; voseo is veis "
     "with an accent"),
    ("verb", "deis", "dar", "VMSP2SV", "deis is vosotros only; voseo is deis "
     "with an accent"),
]
VOS_TAG = "PP2CS0V"
VOS_POLITE = "PP2CS0P"
# erar's voseo forms collided with ser and are removed (decided 261101).
REMOVE_VOSEO_LEMMAS = {"erar"}
KEEP_ANYWAY = {("dái", "dar"), ("dís", "dar")}
EXEMPT_LEMMAS = {"ser", "haber", "ir"}
PARADIGM_KEEP = {"garuar", "taimar", "apernar"}

# Probabilities.
# (arica over aricar until 261110d: Arica is now a place only, and a
# place-only form loses any lemma preference.)
LEMMA_PREFS = [("hacer", "hacendar"), ("ser", "erar"),
               ("aburrir", "aburrar"), ("vender", "vendar"), ("mío", "miar"),
               ("poder", "podar")]
# hm stays more probable as the interjection (2026 release).
FORMTAG_FIXED = ["hm NC-I NC 1 I 20"]
FUTURE_WEIGHT, SUBJ_WEIGHT = 1, 4          # the unaccented future: 20%
PREFER = [("poder", "podar")]
PREFERRED_WEIGHT, OTHER_WEIGHT = 1000, 1
FORMTAG_REMOVE = {"erai VMI-VSI VMI 1 VSI 1000": "ser over erar: erar's voseo "
                  "forms are removed, so erai is ser only",
                  "erís VMS-VSI VMS 1 VSI 1000": "ser over erar: erar's "
                  "voseo forms are removed, so eris with an accent is ser only",
                  "erarai VMI-VMS VMI 1 VMS 4": "erar's voseo forms are "
                  "removed, so erarai no longer exists"}
# THE DECIDED NAMES (decided 261110). A decided name whose lowercase form is
# also an ordinary word keeps both readings. In probabilitats.dat the proper
# noun gets this share of the word's lexical probability (FormTagFreq), the
# ordinary readings the rest, in the proportions FreeLing already gives
# them:
#   a place (the user's Chilean toponyms): much higher than the ordinary
#       readings
#   a person, an organization or another name: moderate
# The tagger divides each lexical probability by the tag's overall
# frequency (FreeLing's hmm_tagger: P(w|t) = P(t|w) P(w) / P(t)), and a
# proper noun is about 3 times rarer than a common noun in FreeLing's
# training corpus, so these shares already weigh 3 times more against a
# common noun in context.
PLACE_SHARE = 0.80
NAME_SHARE = 0.30
# THE EXEMPTION (decided 261110b): a decided name whose lowercase form is
# also a common noun or a verb gets no proper-noun reading at all; FreeLing's
# name recognizer tags it when it is capitalized. Only names whose ordinary
# readings are of other classes (adjectives, adverbs ...) keep the
# proper-noun reading and the shares above. In probabilitats.dat an
# exempted name gets FreeLing's own Spanish line back, or no line when
# FreeLing has none: the deployed file may hold the line an earlier build
# wrote for it.
EXEMPT_CLASSES = ("NC", "V")
# A decided name counts as a common Spanish word when it occurs at least
# this many times in FreeLing's Spanish training corpus (about 418,000
# words; the word frequencies of FreeLing's tagger.dat). NAME-WEIGHTS.tsv
# marks those for review.
COMMON_COUNT = 20
# RARE interjections and mm (decided 261108): the interjection reading is
# kept but made nearly impossible. Its count is 0, and the other readings
# share at least this many, so FreeLing's smoothing (0.1) leaves it about
# 1 in 100,000.
RARE_TOTAL = 10000

# The name recognizer: every single letter is never a name (decided 261101).
NP_LETTERS = list("abcdefghijklmn") + ["ñ"] + list("opqrstuvwxyz")

# THE NAMES (decided 261110d). The classes of the decisions files, and the
# tag each gives.
NE_CLASS_TAG = {"place": "NP00G00", "person": "NP00SP0",
                "organization": "NP00O00", "other": "NP00V00"}
# Class names as the decision files may spell them (decided 261112: the
# project writes American English; files written before keep the British
# spelling, which is read as the American one).
CLASS_SPELLING = {"organisation": "organization"}


def ne_class(text: str) -> str:
    """A class or reading of a decision file, lower case, American."""
    t = text.strip().lower()
    return CLASS_SPELLING.get(t, t)
# The readings of sentence-start-classes: a class, or "name", a proper noun
# whose class the classifier decides.
START_TAG = dict(NE_CLASS_TAG, name="NP00000")
# Which rule file(s) a sentence-start reading goes to.
START_FILES = {"written": ["np.dat"], "speech": ["np-speech.dat"],
               "both": ["np.dat", "np-speech.dat"]}
# The word classes "keep own readings" may name (instead of yes or no): only
# the word's readings of these classes stay beside the new one at the start
# of a sentence (in np.dat, keep:V,N ...: the first letter of their tags).
KEEP_CLASSES = {"verbs": "V", "nouns": "N", "adjectives": "A",
                "adverbs": "R", "pronouns": "P", "determiners": "D",
                "interjections": "I", "prepositions": "S",
                "conjunctions": "C", "numerals": "Z"}
# The recognizer's <DictionaryClasses>: a one-word name whose dictionary
# entry has one of these tags keeps it, in this order of preference, with
# the dictionary's lemma, and the classifier is not asked.
DICT_CLASSES = ["NP00G00", "NP00SP0", "NP00O00", "NP00V00"]
# The two rule files: (file, <ClassesAtSentenceStart>, what it is for).
NP_FILES = [("np.dat", "no", "written texts (CODICACH): the fixed and "
             "dictionary classes apply inside a sentence; at its start a "
             "word that is also a common noun or an adjective is left to "
             "FreeLing"),
            ("np-speech.dat", "yes", "transcribed speech (COSCACH), where a "
             "line is an utterance: the fixed and dictionary classes apply "
             "at the start of a line too")]
# Words of a multiword name FreeLing writes contracted in the name's lemma
# (del -> de_el, al -> a_el): a fixed name holding one is listed both ways.
NP_CONTRACTIONS = [("del", "de_el"), ("al", "a_el")]

# Locutions.
LOCUTIONS_ADD = ["jeans_day jeans_day NCMS000 I",
                 "jean_day jeans_day NCMS000 I"]
# ya po: the key named a lemma po that no form has, so it never matched;
# po and poh have the lemma poh (decided 261109: "ya po" is "ya poh").
LOCUTION_RENAME = {"ya_<po>": ("ya_<poh>", "ya_poh")}
# The minimal multiword set of the 2026 release (20 expressions), for those
# who prefer it: the build applies the same repairs to it as to the full
# set.
MINIMAL_LOCUTIONS = """\
<TagSetFile>
../tagset.dat
</TagSetFile>
<Multiwords>
concha_de_su_madre concha_de_su_madre AQ0CN00 concha_de_su_madre NCCN000 \
concha_de_su_madre I concha_de_su_madre NCCS000 I
concha_de_su_maire concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
concha_de_su_mare concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
concha_de_tu_madre concha_de_tu_madre I concha_de_tu_madre AQ0CN00 \
concha_de_tu_madre NCCS000 I
concha_de_tu_maire concha_de_tu_madre I concha_de_tu_madre AQ0CN00 \
concha_de_tu_madre NCCS000 I
concha_de_tu_mare concha_de_tu_madre I concha_de_tu_madre AQ0CN00 \
concha_de_tu_madre NCCS000 I
conchas_de_sus_madres concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
conchas_de_sus_maires concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
conchas_de_sus_mares concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
conche_su_madre concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
conche_su_maire concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
conche_su_mare concha_de_su_madre I concha_de_su_madre AQ0CN00 \
concha_de_su_madre NCCS000 I
conche_tu_madre concha_de_tu_madre I concha_de_tu_madre AQ0CN00 \
concha_de_tu_madre NCCS000 I
conche_tu_maire concha_de_tu_madre I concha_de_tu_madre AQ0CN00 \
concha_de_tu_madre NCCS000 I
conche_tu_mare concha_de_tu_madre I concha_de_tu_madre AQ0CN00 \
concha_de_tu_madre NCCS000 I
concho_de_vino concho_de_vino AQ0CN00 concho_de_vino NCCN000 I
con_tutti con_tutti RG I
ya_<po> ya_po I I
jeans_day jeans_day NCMS000 I
jean_day jeans_day NCMS000 I
</Multiwords>
"""

# Quantities (decided 261109): Chilean currency. (pattern, replacement,
# rule); each pattern must occur exactly once in FreeLing's file.
QUANTITY_CHANGES = [
    ("<peso> CUP $1:NC I\n", "<peso> CLP $1:NC I\n",
     "peso alone is the Chilean peso (it was the Cuban one)"),
    ("$ USD NCMN000 I\n", "$ CLP NCMN000 I\n",
     "the sign $ is the Chilean peso (it was the US dollar; US$ is not "
     "affected)"),
    ("€ ECU NCMN000 I\n", "€ EUR NCMN000 I\n",
     "the euro's code is EUR (ECU was its predecessor)"),
    ("<euro> ECU $1:NC I\n", "<euro> EUR $1:NC I\n",
     "the euro's code is EUR"),
    ("<euro>_<europeo> ECU $1:NC I\n", "<euro>_<europeo> EUR $1:NC I\n",
     "the euro's code is EUR"),
]
# Added to <Measure> (codes of currencies) and <MeasureNames>.
QUANTITY_MEASURES = ["$ EUR", "$ UF", "$ UTM"]
QUANTITY_NAMES = ["<unidad>_de_fomento UF $1:NC I",
                  "uf UF NCFN000 I",
                  "<unidad>_tributaria_mensual UTM $1:NC I",
                  "utm UTM NCFN000 I"]

# Unit names removed from <MeasureNames> (decided 261112): the name as the
# first field of its line, which must occur exactly once in the section.
# The unit codes in <Measure> stay: the full words use them (dos días is
# TM_d:2). Abbreviations that are also letters, words or false starts
# before a number, in speech and in writing:
QUANTITY_COLLIDING = {
    "tr": "the letters of a false start (uno tr ...), never a unit",
    "mi": "the possessive mi (uno de mi ..., dos mi ...), not the mile",
    "s": "the letter s or a false start (uno s ..., seis S), not the second",
    "d": "the letter d (sesenta D, tres D), not the day",
    "cd": "CD, the compact disc (los tres cd), not the candela",
    "cl": "a false start (dos cl ... dos tipos), not the centiliter",
    "bu": "a false start (uno bu ...), not the bushel",
    "pk": "the chat spelling of porque, not the peck",
    "in": "the English word in (2 in 1), not the inch",
    "pt": "punto, points (pt, pts), not the pint",
}
# Units not written so in Chile, with their compound forms (decided 261112).
QUANTITY_UNUSED = {
    "ft": ["ft", "ft2", "ft3", "ft_Fh_s", "ft_Fh_h", "ft_Fh_min", "ft_Fh_s2",
           "ft3_Fh_s", "ft3_Fh_min", "ftH2O", "fth2o"],
    "gal": ["gal", "gal_Fh_h", "gal_Fh_min", "gal_Fh_s", "gal_Fh_d",
            "gal_Fh_ac_Fh_d", "gal_Fh_cap_Fh_d", "gal_Fh_ft2", "gal_Fh_ft2_d",
            "gal_Fh_ft2_Fh_min"],
    "lb": ["lb", "lb_Fh_ft2", "lb_Fh_ft3", "lb_Fh_in2", "lb_Fh_milgal", "lbf",
           "lbF"],
    "oz": ["oz", "floz"],
    "ac": ["ac", "ac-ft", "ac·ft"],
    "yd": ["yd", "yd2", "yd3"],
    "qt": ["qt"],
    "in": ["in2", "in3", "in_Fh_s2", "inh20", "inH2O", "inhg", "inHg"],
    "mi": ["mi2", "mi_Fh_h"],
}
QUANTITY_REMOVALS = list(QUANTITY_COLLIDING.items()) + [
    (name, "%s is not written so in Chile (a compound form of it)" % unit
     if name != unit else "%s is not written so in Chile" % unit)
    for unit, names in QUANTITY_UNUSED.items() for name in names]

# Lemmas corrected in the Chilean lists themselves (decided 261112), so the
# corrected lists written back carry them, not only the dictionary: (list,
# wrong lemma, right lemma, forms it applies to, why). Lists already
# corrected (the build's own written-back lists) need nothing; a list in
# which no form it applies to has either lemma refuses the build.
LIST_LEMMA_FIXES = [
    ("nom", "guillatun", "nguillatún", re.compile(r"^nguillat"),
     "the lemma of nguillatún, nguillatun and nguillatunes is nguillatún "
     "(user, 261112); the list gave guillatun"),
]

# Unit codes removed from <Measure> (decided 261112): a code no name uses
# once the names above are gone. The codes of the units kept as full words
# stay (mi for milla, ft for pie, gal for galón ...).
QUANTITY_CODE_REMOVALS = {
    "WG tr": "tr is not a unit: no name uses the code once tr is removed",
}

# Variant rules: (id, old ending, new ending, policy, description).
RULES = [
    ("R1", "ái", "ai", "union", "unaccented -ai (cantai, cantarai)"),
    ("R2", "ís", "is", "new", "unaccented -is (cantis, comis)"),
    ("R3", "íai", "iai", "new", "unaccented -iai (comiai, cantariai)"),
    ("R4", "ís", "íh", "new", "aspirated -ih with accent (cantih)"),
    ("R5", "ís", "ih", "new", "aspirated -ih (cantih)"),
    ("R6", "ái", "ay", "join", "-ay (cantay)"),
    ("R7", "ái", "áy", "join", "-ay with accent (cantay)"),
    ("R8", "ís", "í", "new", "final s dropped (tení, cantí)"),
]
AY_EXCEPT = {"day", "muday"}
CLOSED = set("DPSCRFZW")
FUNCTION = set("DPSC")

VOSEO = re.compile(r"^V..[^0]2SV$")
VOSOTROS = re.compile(r"^V..[^0]2P0$")
TAG_RE = re.compile(r"^[A-Z][A-Z0-9]*$")

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass


def log(*a):
    print(*a, flush=True)


def find_project_root(start: Path) -> Path | None:
    for d in [start, *start.parents]:
        if (d / "PROJECT_ROOT.txt").is_file():
            return d
    return None


def read_privacy(path: Path):
    """([(private, public)] longest first, [term]) from the privacy
    file; ValueError on a malformed file."""
    lines = path.read_text(encoding="utf-8").split("\n")
    if lines[0].rstrip("\r") != "private\tpublic":
        raise ValueError("%s: the first line must be private<TAB>public"
                         % path)
    rows, terms = [], []
    for n, line in enumerate(lines[1:], 2):
        line = line.rstrip("\r")
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) > 2 or not f[0].strip():
            raise ValueError("%s line %d: not private<TAB>public or a term"
                             % (path, n))
        terms.append(f[0])
        if len(f) == 2 and f[1]:
            rows.append((f[0], f[1]))
    if not terms:
        raise ValueError("%s: no private term" % path)
    low = [t.lower() for t in terms]
    for priv, pub in rows:
        if any(t in pub.lower() for t in low):
            raise ValueError("%s: the public text of %s holds a private term"
                             % (path, priv))
    rows.sort(key=lambda r: -len(r[0]))
    return rows, terms


def private_hits(b, terms):
    """[(line number, term)] of every private term in b, in any case."""
    t = (b if isinstance(b, str) else b.decode("utf-8", "replace")).lower()
    low = [(x.lower(), x) for x in terms]
    if not any(x in t for x, _ in low):
        return []
    return [(n, orig) for n, line in enumerate(t.split("\n"), 1)
            for x, orig in low if x in line]


def make_public(rel, b: bytes, rows, terms):
    """(bytes, problems): a file of the release as it is written. A text
    file that is not data gets the replacements of the privacy file; every
    file is then searched for the private terms, and a Python file must
    still compile."""
    if not rel.startswith(DATA_PARTS) and not rel.endswith(".zip"):
        try:
            t = b.decode("utf-8")
        except UnicodeDecodeError:
            t = None
        if t is not None:
            for priv, pub in rows:
                t = t.replace(priv, pub)
            b = t.encode("utf-8")
    problems = ["%s line %d: %s" % (rel, n, term)
                for n, term in private_hits(b, terms)]
    if rel.endswith(".py") and not problems:
        try:
            compile(b.decode("utf-8"), rel, "exec")
        except SyntaxError as exc:
            problems.append("%s: not valid Python after the replacements "
                            "(%s)" % (rel, exc))
    return b, problems


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def strip_accents(s: str) -> str:
    out = []
    for ch in unicodedata.normalize("NFD", s):
        if unicodedata.category(ch) == "Mn" and ch != "̃":
            continue
        out.append(ch)
    return unicodedata.normalize("NFC", "".join(out))


# --------------------------------------------------------------------------
# The tagset

def load_tagset(text: str):
    """(rules, direct): rules maps a category letter to its list of
    (feature name, set of codes), in tag position order; direct is the set
    of tags translated whole (the punctuation). Codes are uppercased, as
    FreeLing's tagset.cc does when it loads them."""
    rules, direct, sec = {}, set(), None
    for line in text.splitlines():
        st = line.strip()
        if not st or st.startswith("#"):
            continue
        if st.startswith("<"):
            sec = st
            continue
        f = st.split()
        if sec == "<DecompositionRules>":
            feats = []
            for spec in f[3:]:
                name, _, vals = spec.partition("/")
                feats.append((name, {v.split(":")[0].upper()
                                     for v in vals.split(";")}))
            rules[f[0]] = (int(f[1]), feats)
        elif sec == "<DirectTranslations>":
            direct.add(f[0])
    return rules, direct


def undecodable(tag: str, tagset) -> str | None:
    """Why the tagset cannot decode a tag, or None if it can. FreeLing
    uppercases a tag before decoding it; 0 is no value."""
    rules, direct = tagset
    if tag in direct:
        return None
    t = tag.upper()
    entry = rules.get(t[0])
    if entry is None:
        return "no category %s" % t[0]
    feats = entry[1]
    if len(t) - 1 > len(feats):
        return "longer than the %d positions of category %s" % (
            len(feats) + 1, t[0])
    for i, ch in enumerate(t[1:]):
        if ch != "0" and ch not in feats[i][1]:
            return "position %d (%s) has %s" % (i + 2, feats[i][0], ch)
    return None


def short_tag(tag: str, tagset) -> str:
    """FreeLing's short tag: the first n characters, n from the tagset
    (2 for nouns and adjectives, 3 for verbs, 1 for interjections); a
    punctuation tag is its own short tag."""
    rules, direct = tagset
    if tag in direct:
        return tag
    entry = rules.get(tag[0])
    if entry is None:
        return tag
    n = entry[0]
    return tag[:n] if n > 0 else tag[:1]


TAG_SHAPE = re.compile(r"^[A-Z][A-Za-z0-9]*$")


def tags_in(text: str, kind: str):
    """(tag, where) for every tag of a dictionary (dicc), probabilities
    (prob), locutions (locu), name recognizer (np) or quantities (quant)
    file. A locution's $n:XX takes the category XX."""
    sec = None
    for line in text.splitlines():
        st = line.strip()
        if st.startswith("<") and (st.endswith(">") and " " not in st):
            sec = st
            continue
        f = st.split()
        if not f:
            continue
        cand = []
        if kind == "dicc" and sec == "<Entries>":
            cand = f[2::2]
        elif kind == "prob" and sec in ("<UnknownTags>", "<SingleTagFreq>"):
            cand = f[:1]
        elif kind == "prob" and sec == "<ClassTagFreq>":
            cand = f[1::2]
        elif kind == "prob" and sec == "<FormTagFreq>":
            cand = f[2::2]
        elif kind == "locu" and sec == "<Multiwords>":
            cand = f[2:-1:2]
        elif kind == "quant" and sec == "<MeasureNames>":
            cand = f[2:3]
        elif kind == "np" and sec == "<NE_Tag>":
            cand = f[:1]
        elif kind == "np" and sec == "<DictionaryClasses>":
            cand = f
        elif kind == "np" and sec == "<FixedClasses>":
            cand = f[1:2]
        elif kind == "np" and sec == "<SentenceStartClasses>":
            cand = f[1:2]
        elif kind == "nec" and sec == "<ClassShares>":
            cand = f[1::2]
        for t in cand:
            m = re.match(r"^\$\d+:(.+)$", t)
            if m:
                t = m.group(1)
            elif not TAG_SHAPE.match(t):
                continue
            yield t, st


def check_chilean_tagset(chilean: str, original: str):
    """Problems if the Chilean tagset is not FreeLing's Spanish tagset with
    exactly the TAGSET_CHANGES."""
    expected = original
    for old, new in TAGSET_CHANGES:
        if expected.count(old) != 1:
            return ["FreeLing's Spanish tagset no longer has exactly one %r; "
                    "the Chilean tagset cannot be checked" % old.strip()]
        expected = expected.replace(old, new)
    if chilean != expected:
        a, b = expected.splitlines(), chilean.splitlines()
        diff = [i + 1 for i in range(max(len(a), len(b)))
                if (a[i] if i < len(a) else None) !=
                (b[i] if i < len(b) else None)]
        return ["the Chilean tagset is not FreeLing's Spanish tagset plus "
                "the voseo values only: it differs on line(s) %s"
                % ", ".join(str(n) for n in diff[:20])]
    return []


def fix_tagset_reference(text: str, name: str, changes, problems):
    """The tagset a probabilities or locutions file names becomes
    ./tagset.dat, the Chilean one beside it. FreeLing's es-cl files name
    ../tagset.dat, the Spanish one."""
    lines = text.splitlines()
    opens = [i for i, x in enumerate(lines)
             if x.strip().lower() == "<tagsetfile>"]
    if len(opens) != 1 or opens[0] + 2 >= len(lines) or \
            lines[opens[0] + 2].strip().lower() != "</tagsetfile>":
        problems.append("%s: expected exactly one tagset section of one line"
                        % name)
        return text
    i = opens[0] + 1
    old = lines[i].strip()
    if old != "./tagset.dat":
        lines[i] = "./tagset.dat"
        changes.append((name, "changed", "tagset reference: the Chilean "
                        "tagset beside it, not the Spanish one", "", "", "",
                        old))
    return "\n".join(lines) + "\n"


def drop_unknown_tags(text: str, tagset, changes):
    """Removes from <UnknownTags> every tag the tagset cannot decode
    (FreeLing's es-cl file has eight adjective degrees the Spanish tagset
    does not have: AQCCN00, AQDFS00 ...)."""
    out, sec = [], None
    for line in text.splitlines():
        st = line.strip()
        if st.startswith("<"):
            sec = st
        elif sec == "<UnknownTags>" and st:
            why = undecodable(st.split()[0], tagset)
            if why:
                changes.append(("probabilitats", "removed", "unknown-word "
                                "tag the tagset cannot decode (%s)" % why,
                                "", "", st.split()[0], st))
                continue
        out.append(line)
    return "\n".join(out) + "\n"


def is_voseo(tag: str) -> bool:
    return bool(VOSEO.match(tag))


def zero(tag: str) -> str:
    """The plain-tag equivalent of a voseo tag: the tuteo tag (VMIP2SV ->
    VMIP2S0; vos PP2CS0V -> PP2CS00, as te and ti). Never the polite tag."""
    if len(tag) == 7 and tag[0] in "VP" and tag[6] == "V":
        return tag[:6] + "0"
    return tag


def tag_class(tag: str) -> str:
    """NP, NC, or the category letter."""
    if tag.startswith(("NP", "NC")):
        return tag[:2]
    return tag[:1]


# --------------------------------------------------------------------------
# Tags in words (for the change log and the variant table)

_G = {"F": "feminine", "M": "masculine", "C": "common gender",
      "V": "voseo"}
_N = {"S": "singular", "P": "plural", "N": "invariable number"}
_P = {"1": "1st person", "2": "2nd person", "3": "3rd person"}
DESCR = {
    "A": ("adjective", [{"O": "ordinal", "Q": "qualifying", "P": "possessive"},
                        {"S": "superlative", "V": "evaluative"}, _G, _N,
                        {k: "possessor " + v for k, v in _P.items()},
                        {k: "possessor " + v for k, v in _N.items()}]),
    "C": ("conjunction", [{"C": "coordinating", "S": "subordinating"}]),
    "D": ("determiner", [{"A": "article", "D": "demonstrative",
                          "I": "indefinite", "P": "possessive",
                          "T": "interrogative", "E": "exclamative"},
                         _P, _G, _N,
                         {k: "possessor " + v for k, v in _N.items()}]),
    "N": ("noun", [{"C": "common", "P": "proper"}, _G, _N,
                   {"S": "person", "G": "place", "O": "organization",
                    "V": "other name"}, {}, {"V": "evaluative"}]),
    "P": ("pronoun", [{"D": "demonstrative", "E": "exclamative",
                       "I": "indefinite", "P": "personal", "R": "relative",
                       "T": "interrogative"}, _P, _G, _N,
                      {"N": "nominative", "A": "accusative", "D": "dative",
                       "O": "oblique"}, {"P": "polite", "V": "voseo"}]),
    "R": ("adverb", [{"N": "negative", "G": "general"}]),
    "S": ("preposition", []),
    "V": ("verb", [{"M": "main", "A": "auxiliary haber/estar", "S": "ser"},
                   {"I": "indicative", "S": "subjunctive", "M": "imperative",
                    "P": "participle", "G": "gerund", "N": "infinitive"},
                   {"P": "present", "I": "imperfect", "F": "future",
                    "S": "preterite", "C": "conditional"}, _P, _N,
                   {"F": "feminine", "M": "masculine", "V": "voseo"}]),
    "Z": ("numeral", []), "W": ("date", []), "I": ("interjection", []),
    "F": ("punctuation", []),
}


def describe(tag: str) -> str:
    """A tag in plain English: VMIP2SV -> verb, main, indicative, present,
    2nd person, singular, voseo."""
    if not tag:
        return ""
    if tag.startswith("$"):
        n, _, rest = tag[1:].partition(":")
        return "category of word %s of the expression: %s" % (n,
                                                              describe(rest))
    if tag[0] not in DESCR:
        return tag
    name, feats = DESCR[tag[0]]
    words = [name]
    for i, ch in enumerate(tag[1:]):
        if i < len(feats) and ch in feats[i]:
            words.append(feats[i][ch])
    return ", ".join(words)


def in_words(pairs) -> str:
    return "; ".join("%s (%s)" % (l, describe(g)) for l, g in pairs)


# --------------------------------------------------------------------------
# Reading

def read_entries_text(text: str):
    """(form, lemma, tag) for every line of an entries file."""
    out = []
    for line in text.splitlines():
        t = line.split()
        if len(t) >= 3:
            out.append((t[0], t[1], t[2]))
    return out


def read_gram(path: Path, problems, changes, name):
    out = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        t = line.split("\t")
        if len(t) != 3 or not all(x.strip() for x in t):
            problems.append("%s line %d is not form<TAB>lemma<TAB>tag: %r"
                            % (path.name, n, line))
            continue
        f, l, g = (x.strip() for x in t)
        if nfc(f) != f or nfc(l) != l:
            changes.append((name, "changed", "made NFC", f, l, g, ""))
            f, l = nfc(f), nfc(l)
        out.append((f, l, g))
    return out


def read_tsv(path: Path):
    """(header, rows) of a decisions file: UTF-8, tab-separated, one header
    line, no quoting. Every cell is NFC-normalized."""
    text = path.read_text(encoding="utf-8")
    rows = list(csv.reader(io.StringIO(text), delimiter="\t",
                           quoting=csv.QUOTE_NONE))
    rows = [[nfc(c) for c in r] for r in rows if any(c.strip() for c in r)]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def np_key(name: str) -> str:
    """A name as FreeLing's recognizer writes a multiword name's form:
    NFC, lower case, words joined by _ (Viña del Mar -> viña_del_mar)."""
    return "_".join(nfc(name).strip().lower().split())


def round_of(path: Path) -> str:
    """The round of a decisions file: the part after the last "--"
    (261103, 261103b ...). Rounds sort as strings."""
    return path.stem.rsplit("--", 1)[-1]


def decision_files(d: Path, stem: str):
    """Every live file of one kind, oldest round first."""
    return sorted(d.glob("%s--*.tsv" % stem), key=round_of)


# --------------------------------------------------------------------------
# The voseo paradigm check

def expected_voseo(lemma, tag, es_by_lt):
    """The voseo forms the Spanish paradigm implies for (lemma, tag), or
    None when the Spanish dictionary cannot say."""
    mt = tag[2:4]
    if mt in ("II", "IC", "IF", "SI"):
        src = es_by_lt.get((lemma, tag[:4] + "2S0"))
        if not src:
            return None
        if mt == "SI":
            src = {f for f in src if f.endswith("ras")}
            if not src:
                return None
        return {f[:-1] + "i" for f in src if f.endswith("s")}
    if mt == "IS":
        src = es_by_lt.get((lemma, tag[:4] + "2S0"))
        return {f + "s" for f in src} if src else None
    if mt in ("IP", "SP"):
        src = es_by_lt.get((lemma, tag[:4] + "2P0"))
        if not src:
            return None
        exp = set()
        for v in src:
            if v.endswith("áis"):
                exp.add(v[:-1])
            elif v.endswith("éis"):
                exp.add(v[:-3] + "ís")
            elif v.endswith("ís"):
                exp.add(v)
            elif v.endswith("eis"):
                exp.add(v[:-3] + "eís")
            elif v.endswith(("ais", "ois")):
                exp.add(v[:-1])
        return exp or None
    return None


def explained_overgeneration(form, lemma, exp):
    """The deliberate overgeneration of the explode scripts: raised e in
    -ear verbs (golpiai, arris) and dropped i in -iar verbs (envis)."""
    cands = []
    if lemma.endswith("ear"):
        s = lemma[:-3]
        if form.startswith(s + "i"):
            cands.append(s + "e" + form[len(s) + 1:])
        if form.startswith(s):
            cands.append(s + "e" + form[len(s):])
    if lemma.endswith("iar"):
        s = lemma[:-3]
        if form.startswith(s):
            cands.append(s + "i" + form[len(s):])
    return any(c in exp for c in cands)


# --------------------------------------------------------------------------
# build-dict, exactly

def build_dict(triples):
    """cat | awk 'NF>0' | LC_ALL=C sort | uniq | unique-key.awk, with the
    header. triples: iterable of (form, lemma, tag)."""
    raw = sorted({("%s %s %s" % t).encode("utf-8") for t in triples})
    out = [HEADER.encode("utf-8")]
    key, data = None, None
    for b in raw:
        k, _, rest = b.partition(b" ")
        if k == key:
            data += b" " + rest
        else:
            if key is not None:
                out.append(key + b" " + data + b"\n")
            key, data = k, rest
    if key is not None:
        out.append(key + b" " + data + b"\n")
    out.append(b"</Entries>\n")
    return b"".join(out)


def simulate_freeling_build(base, remove, entries):
    """FreeLing's own build-dict for a variant (build-dict.cc, as FreeLing's
    install runs it): the Spanish entries, minus the remove folder (applied
    to the Spanish entries only), plus the variant's entries. A form left
    with no analysis would be written bare; it is reported instead."""
    m = collections.defaultdict(set)
    for f, l, g in base:
        m[f].add((l, g))
    for f, l, g in remove:
        if f in m:
            m[f].discard((l, g))
    for f, l, g in entries:
        m[f].add((l, g))
    empty = sorted(f for f, s in m.items() if not s)
    return build_dict((f, l, g) for f, s in m.items() for l, g in s), empty


def voseo_check(dicc: bytes):
    """(vos tags, deis with both readings, -is forms with both readings,
    other forms with both readings)."""
    vos_tags, deis, isf, unexpected = set(), 0, 0, []
    for line in dicc.decode("utf-8").splitlines():
        t = line.split()
        if len(t) < 3 or len(t) % 2 == 0:
            continue
        form, pairs = t[0], [(t[i], t[i + 1]) for i in range(1, len(t), 2)]
        if form == "vos":
            vos_tags = {p[1] for p in pairs if p[0] == "vos"}
            continue
        sv = {(l, g[:4]) for l, g in pairs if VOSEO.match(g)}
        pv = {(l, g[:4]) for l, g in pairs if VOSOTROS.match(g)}
        if sv & pv:
            if form == "deis":
                deis += 1
            else:
                isf += 1
                if not form.endswith(("is", "ís")):
                    unexpected.append(line)
    return vos_tags, deis, isf, unexpected


def contemporary(merged, changes):
    """The default dictionary from the full (historical) one: vos keeps only
    its voseo reading, an -is form with a voseo and a vosotros reading of
    the same verb and tense keeps the voseo one, deis keeps its vosotros
    reading (decided 261109; the rules of the former COSCACH/CODICACH
    copy). Returns (new dict, removed triples)."""
    out, removed = {}, []
    for form, an in merged.items():
        keep = an
        if form == "vos":
            keep = [p for p in an if p[1] != VOS_POLITE]
            why = "vos is always voseo in contemporary Chilean Spanish"
        else:
            sv = {(l, g[:4]) for l, g in an if VOSEO.match(g)}
            pv = {(l, g[:4]) for l, g in an if VOSOTROS.match(g)}
            both = sv & pv
            if both:
                if form == "deis":
                    keep = [p for p in an if not (VOSEO.match(p[1]) and
                                                  (p[0], p[1][:4]) in both)]
                    why = "deis is vosotros only; voseo is deis with an accent"
                else:
                    keep = [p for p in an if not (VOSOTROS.match(p[1]) and
                                                  (p[0], p[1][:4]) in both)]
                    why = ("an -is form is voseo in contemporary Chilean "
                           "Spanish, not vosotros")
        if len(keep) != len(an):
            for p in an:
                if p not in keep:
                    removed.append((form,) + p)
                    changes.append(("contemporary", "removed", why, form,
                                    p[0], p[1], "kept in the historical "
                                    "dictionary"))
        out[form] = keep
    return out, removed


# --------------------------------------------------------------------------
# Spanish word forms (for the decided additions)

VOWELS = set("aeiouáéíóúü")
STRONG = set("aeoáéó")
ACCENT = {"a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"}
UNACCENT = {v: k for k, v in ACCENT.items()}


def nuclei(w: str):
    """The vowel nuclei of a word, as (start, end) pairs: a diphthong is
    one nucleus; two strong vowels, or an accented i or u beside a strong
    vowel, are two. The u of que, qui, gue, gui is not a vowel."""
    out, i = [], 0
    while i < len(w):
        ch = w[i]
        silent_u = (ch == "u" and i > 0 and w[i - 1] in "qg" and
                    i + 1 < len(w) and w[i + 1] in "eiéí")
        if ch in VOWELS and not silent_u:
            j = i + 1
            while j < len(w) and w[j] in VOWELS:
                a, b = w[j - 1], w[j]
                if (a in STRONG and b in STRONG) or \
                        (a in "íú" and b in STRONG) or \
                        (b in "íú" and a in STRONG):
                    break
                j += 1
            out.append((i, j))
            i = j
        else:
            i += 1
    return out


def has_accent(s: str) -> bool:
    return any(c in UNACCENT for c in s)


def accent_nucleus(w: str, nuc) -> str:
    """w with a written accent on the nucleus (start, end): on its strong
    vowel, or on the second of two weak ones."""
    a, b = nuc
    part = w[a:b]
    idx = None
    for k, ch in enumerate(part):
        if ch in "aeo":
            idx = k
    if idx is None:
        idx = len(part) - 1
    ch = part[idx]
    if ch not in ACCENT:
        return w
    return w[:a + idx] + ACCENT[ch] + w[a + idx + 1:]


def pluralize(w: str) -> str | None:
    """The plural of a singular noun or adjective, by the RAE's rules; None
    when the word does not change (crisis, lunes)."""
    if not w:
        return None
    last = w[-1]
    if last in "aeiouáéó":
        return w + "s"
    if last in "íú":
        return w + "es"
    if last == "z":
        return w[:-1] + "ces"
    nuc = nuclei(w)
    if last == "y":
        return w + "es" if len(nuc) <= 1 else w + "s"
    if last in "sx":
        if nuc and has_accent(w[nuc[-1][0]:nuc[-1][1]]):
            return strip_accents(w) + "es"
        if len(nuc) == 1:
            return w + "es"
        return None
    if last in "lrndj":
        if nuc and has_accent(w[nuc[-1][0]:nuc[-1][1]]):
            return strip_accents(w) + "es"
        if last == "n" and not has_accent(w) and len(nuc) >= 2:
            return accent_nucleus(w, nuc[-2]) + "es"
        return w + "es"
    return w + "s"


def singularize(w: str) -> str | None:
    """The singular of a plural, only where it is certain: -as, -os (casas,
    aritos), -is, -us (jipis, otakus), -ces (luces); None otherwise."""
    if w.endswith("ces") and len(w) > 4:
        return w[:-3] + "z"
    if len(w) > 3 and w.endswith("s") and w[-2] in "aoiuáó":
        return w[:-1]
    return None


def looks_plural(form: str, lemma: str) -> bool:
    """A form ending in s is plural when its lemma does not end in s
    (cositos, pantys, flayers); when both do (lentes), when a vowel comes
    before the s."""
    if form == lemma or len(form) < 3 or not form.endswith("s"):
        return False
    if not lemma.endswith("s"):
        return True
    return form[-2] in VOWELS


def evaluative(form: str, lemma: str) -> str:
    """'S' for a superlative (-ísimo), 'V' for a diminutive or augmentative
    (-ito, -cito, -ico, -illo, -ucho, -ote, -azo, -ón) whose lemma is the
    base word, '0' otherwise. A lexicalized diminutive whose lemma has the
    suffix itself (burritos, lemma burrito) is not evaluative."""
    if form == lemma:
        return "0"
    def stem(w):
        if w.endswith("s"):
            w = w[:-1]
        if w and w[-1] in "oae":
            w = w[:-1]
        return w
    fs, ls = stem(form), stem(lemma)
    if fs.endswith("ísim") and not ls.endswith("ísim"):
        return "S"
    for suf in ("it", "ic", "ill", "uch", "ot", "az"):
        if fs.endswith(suf) and not ls.endswith(suf):
            return "V"
    if form.endswith(("ón", "ona", "ones", "onas")) and \
            not lemma.endswith(("ón", "ona")):
        return "V"
    return "0"


def adjective_forms(ms: str):
    """{gender+number: form} of an adjective from its masculine singular:
    four forms, or two when it does not vary for gender."""
    if ms.endswith("o"):
        st = ms[:-1]
        return {"MS": ms, "FS": st + "a", "MP": ms + "s", "FP": st + "as"}
    if ms.endswith("ote"):
        st = ms[:-1]
        return {"MS": ms, "FS": st + "a", "MP": ms + "s", "FP": st + "as"}
    if ms.endswith("or"):
        return {"MS": ms, "FS": ms + "a", "MP": ms + "es", "FP": ms + "as"}
    if ms.endswith(("ón", "án", "ín")):
        b = strip_accents(ms)
        return {"MS": ms, "FS": b + "a", "MP": b + "es", "FP": b + "as"}
    if ms.endswith("és"):
        b = ms[:-2] + "es"
        return {"MS": ms, "FS": b + "a", "MP": b + "es", "FP": b + "as"}
    pl = pluralize(ms)
    out = {"CS": ms}
    if pl:
        out["CP"] = pl
    return out


def adjective_gn(form: str, lemma: str, invariable: bool) -> str:
    if invariable:
        return "C" + ("P" if looks_plural(form, lemma) else "S")
    for end, gn in (("os", "MP"), ("as", "FP"), ("o", "MS"), ("a", "FS"),
                    ("otes", "MP"), ("ote", "MS")):
        if form.endswith(end):
            return gn
    return "C" + ("P" if looks_plural(form, lemma) else "S")


CATEGORY = {
    "proper noun, person": ("NP", "NP00SP0"),
    "proper noun, place": ("NP", "NP00G00"),
    "proper noun, organization or brand": ("NP", "NP00O00"),
    "proper noun, organisation or brand": ("NP", "NP00O00"),
    "proper noun, other": ("NP", "NP00V00"),
    "common noun, masculine": ("NC", "M"),
    "common noun, feminine": ("NC", "F"),
    "common noun, either gender (el/la)": ("NC", "C"),
    "common noun, invariable (same singular and plural)": ("NC", "N"),
    "adjective": ("AQ", ""),
    "adjective, invariable for gender (-e, -l ...)": ("AQ", "C"),
    "adverb": ("RG", "RG"),
    "interjection or discourse marker": ("I", "I"),
    "verb (lemma: the infinitive)": ("V", ""),
    "verb": ("V", ""),
    "foreign word": ("-", ""),
}


def category_of(text: str):
    """(class, detail) of a decision's category, or None."""
    t = text.strip()
    if t in CATEGORY:
        return CATEGORY[t]
    for k, v in CATEGORY.items():
        if t.startswith(k):
            return v
    return None


def lemma_key(lemma: str) -> str:
    """A lemma as the dictionary writes it: spaces become underscores."""
    return lemma.strip().replace(" ", "_")


def word_analyses(form, lemma, category, exists):
    """The (form, lemma, tag) lines a decided word gives, and notes.
    exists(form, lemma) says whether a generated form may be added: it is
    new, or already a form of the same lemma. The decided form itself is
    always added. Verbs are not handled here."""
    cls, detail = category_of(category) or ("?", "")
    out, notes = [], []
    lemma = lemma_key(lemma)

    def gen(f, t, why):
        if f == form:
            out.append((f, lemma, t))
        elif exists(f, lemma):
            out.append((f, lemma, t))
        else:
            notes.append("%s not added: it is another word" % f)

    if cls == "NP":
        out.append((form, lemma, detail))
    elif cls in ("RG", "I"):
        out.append((form, lemma, detail))
    elif cls == "NC":
        g = detail if detail in "MFC" else "C"
        # a feminine form of a masculine lemma is tagged feminine, whatever
        # gender the category gives the lemma (exalumnas, lemma exalumno)
        if g == "M" and ((lemma.endswith("o") and form in (
                lemma[:-1] + "a", lemma[:-1] + "as")) or (
                lemma.endswith("or") and form in (lemma + "a",
                                                   lemma + "as"))):
            g = "F"
            notes.append("tagged feminine: the feminine of %s" % lemma)
        deg = evaluative(form, lemma)
        dv = "V" if deg in "VS" else "0"
        if detail == "N":
            out.append((form, lemma, "NC%sN00%s" % ("C", dv)))
        else:
            plural = looks_plural(form, lemma)
            n = "P" if plural else "S"
            out.append((form, lemma, "NC%s%s00%s" % (g, n, dv)))
            other = singularize(form) if plural else pluralize(form)
            if plural and dv == "0" and lemma_key(lemma) != form and \
                    (pluralize(lemma) == form):
                other = lemma
            if other and other != form:
                gen(other, "NC%s%s00%s" % (g, "S" if plural else "P", dv),
                    "number")
            elif not other:
                notes.append("the %s of %s was not generated (not certain)"
                             % ("singular" if plural else "plural", form))
            # the lemma itself, when the form is its plural or its
            # feminine and the lemma is not yet a word
            if dv == "0" and lemma != form:
                rel = None
                if lemma.endswith("o") and form in (lemma[:-1] + "a",
                                                    lemma[:-1] + "as"):
                    rel = "M"
                elif lemma.endswith("or") and form in (lemma + "a",
                                                       lemma + "as"):
                    rel = "M"
                elif pluralize(lemma) == form:
                    rel = g
                if rel:
                    gen(lemma, "NC%sS000" % rel, "lemma")
                    pl = pluralize(lemma)
                    if pl and pl != form:
                        gen(pl, "NC%sP000" % rel, "lemma plural")
    elif cls == "AQ":
        invariable = detail == "C"
        deg = evaluative(form, lemma)
        forms = None
        if deg in "VS":
            base = form[:-1] if form.endswith("s") else form
            if base.endswith(("o", "a")):
                forms = adjective_forms(base[:-1] + "o")
            elif base.endswith("e"):
                forms = adjective_forms(base)
        else:
            lf = adjective_forms(lemma)
            if form == lemma or form in lf.values():
                forms = lf
            elif form.endswith("o"):
                forms = adjective_forms(form)
        if invariable and forms:
            forms = {("C" + k[1]): v for k, v in forms.items()
                     if k in ("MS", "MP", "CS", "CP")}
        gn = next((k for k, v in (forms or {}).items() if v == form), None) \
            or adjective_gn(form, lemma, invariable)
        out.append((form, lemma, "AQ%s%s00" % (deg, gn)))
        if forms:
            for k, f in forms.items():
                if f != form:
                    gen(f, "AQ%s%s00" % (deg, k), "paradigm")
        else:
            other = singularize(form) if gn[1] == "P" else pluralize(form)
            if other and other != form:
                gen(other, "AQ%s%s%s00" % (deg, gn[0],
                                           "S" if gn[1] == "P" else "P"),
                    "number")
    else:
        notes.append("category %r not added to the dictionary" % category)
    return out, notes


# --------------------------------------------------------------------------
# Verb paradigms for new verbs

# Prefixes a new verb may be made of: a verb made of one of these and a
# known verb is conjugated like that verb (re + programar, auto + valer).
PREFIXES = {"a", "ante", "anti", "auto", "bi", "co", "con", "contra", "de",
            "des", "di", "dis", "em", "en", "entre", "ex", "extra", "hiper",
            "im", "in", "inter", "macro", "micro", "mini", "multi", "p",
            "per", "pos", "post", "pre", "pro", "re", "recontra", "requete",
            "retro", "semi", "sobre", "sub", "super", "tele", "trans",
            "tras", "ultra"}
# ("p" + sicosear: psicosear, the psico- spelling of sico-.)
# (os, the vosotros pronoun, is left out: Chilean Spanish does not use it,
# and taking it off a form makes false bases: cubridos is not cubrid + os.)
CLITICS = sorted(["me", "te", "se", "nos", "lo", "la", "le", "los",
                  "las", "les"], key=len, reverse=True)
INFINITIVE = ("ar", "er", "ir", "ír")


def verb_index(merged):
    """lemma -> sorted list of (form, tag) of its verb readings."""
    idx = collections.defaultdict(set)
    for f, an in merged.items():
        for l, g in an:
            if g.startswith("V"):
                idx[l].add((f, g))
    return {l: sorted(v) for l, v in idx.items()}


class VerbModels:
    """Chooses the verb a new verb is conjugated like, and conjugates it.

    A verb made of a prefix and a known verb is conjugated like that verb
    (desestresar like estresar, sobreexigir like exigir). Any other verb is
    conjugated like the known verbs that share its longest ending (at
    least the consonant before the infinitive ending: -ear, -car, -gir),
    taking the conjugation pattern most of them share, and only if at least
    three share it: so a regular verb never gets a stem change."""

    def __init__(self, vidx):
        self.vidx = vidx
        self.by_end = collections.defaultdict(list)
        for l in vidx:
            if l.endswith(INFINITIVE) and l.isalpha():
                self.by_end[l[-2:]].append(l)
        self.cache = {}

    def table(self, model, k):
        key = (model, k)
        if key not in self.cache:
            stem = model[:-k]
            tb = []
            for f, g in self.vidx[model]:
                if not f.startswith(stem):
                    tb = None
                    break
                tb.append((f[len(stem):], g))
            self.cache[key] = frozenset(tb) if tb else None
        return self.cache[key]

    def choose(self, lemma, allow_prefix=True, min_k=3):
        """(how, model, k, table) or None."""
        if allow_prefix:
            for i in range(1, len(lemma) - 4):
                v = lemma[i:]
                if lemma[:i] not in PREFIXES:
                    continue
                if v in self.vidx and v.endswith(INFINITIVE):
                    tb = self.table(v, len(v))
                    if tb:
                        return ("like %s (%s + %s)" % (v, lemma[:i], v), v,
                                len(v), tb)
        end = lemma[-2:]
        for k in range(len(lemma) - 1, min_k - 1, -1):
            suf = lemma[-k:]
            cands = [m for m in self.by_end.get(end, ())
                     if m.endswith(suf) and m != lemma]
            if len(cands) < 3:
                continue
            groups = collections.Counter()
            members = collections.defaultdict(list)
            for m in cands:
                tb = self.table(m, k)
                if tb:
                    groups[tb] += 1
                    members[tb].append(m)
            if not groups:
                continue
            tb, n = groups.most_common(1)[0]
            if n >= 3:
                ms = sorted(members[tb])
                return ("like %s, %s ... (%d verbs in -%s)"
                        % (ms[0], ms[1], n, suf), ms[0], k, tb)
        return None

    def regular_tags(self, lemma, form):
        """The tags a non-standard form of a known verb has in the pattern
        most verbs of some ending share, from the longest ending down to
        the bare infinitive ending (ponido, ponieron, descubrido: the
        regular -er and -ir patterns). (tags, how) or ([], None)."""
        end = lemma[-2:]
        for k in range(len(lemma) - 1, 1, -1):
            suf = lemma[-k:]
            cands = [m for m in self.by_end.get(end, ())
                     if m.endswith(suf) and m != lemma]
            if len(cands) < 3:
                continue
            groups = collections.Counter()
            members = collections.defaultdict(list)
            for m in cands:
                tb = self.table(m, k)
                if tb:
                    groups[tb] += 1
                    members[tb].append(m)
            if not groups:
                continue
            tb, n = groups.most_common(1)[0]
            if n < 3:
                continue
            stem = lemma[:-k]
            tags = sorted({g for s_, g in tb if stem + s_ == form})
            if tags:
                ms = sorted(members[tb])
                return tags, "like %s, %s ... (%d verbs in -%s)" % (
                    ms[0], ms[1], n, suf)
        return [], None

    def conjugate(self, lemma, choice):
        how, model, k, tb = choice
        stem = lemma[:-k]
        return sorted({(stem + s, lemma, g) for s, g in tb})


def clitic_bases(form):
    """The verb forms a form with attached pronouns may come from
    (empréstame -> empresta, háceme -> hace)."""
    out, w = [], form
    for _ in range(3):
        for c in CLITICS:
            if w.endswith(c) and len(w) > len(c) + 2:
                w = w[:-len(c)]
                out.append(w)
                out.append(strip_accents(w))
                break
        else:
            break
    return out


# --------------------------------------------------------------------------
# The decisions

class Decisions:
    """Every decisions file the build reads, parsed. Later rounds win."""

    def __init__(self, d: Path, problems):
        self.d = d
        self.files = []
        self.problems = problems

        def take(path):
            self.files.append(path)
            return read_tsv(path)

        adds = decision_files(d, "dictionary-additions-all-rounds-"
                                 "standardized")
        rounds = decision_files(d, "dictionary-additions")
        if not adds:
            problems.append("no dictionary-additions-all-rounds-standardized "
                            "file in %s" % d)
            self.additions = []
        else:
            h, rows = take(adds[-1])
            self.additions_file = adds[-1]
            self.additions = [r[:4] for r in rows if len(r) >= 3]
            if rounds and round_of(rounds[-1]) > round_of(adds[-1]):
                problems.append("%s is newer than %s: the all-rounds "
                                "additions file must be regenerated first"
                                % (rounds[-1].name, adds[-1].name))
        # dictionary-words (decided 261113): form, lemma, category, tag,
        # notes. With a tag, the form gets exactly that reading; without
        # one, it gets the category's readings, as a decided addition does
        # (the other number and gender of a noun or an adjective, the whole
        # paradigm of a new verb). Every round is read; a later round wins
        # for the same form and lemma.
        self.words = collections.OrderedDict()
        for p in decision_files(d, "dictionary-words"):
            h, rows = take(p)
            for r in rows:
                if len(r) >= 3 and r[0].strip():
                    r = [nfc(x).strip() for x in r] + ["", ""]
                    self.words[(r[0].lower(), lemma_key(r[1]))] = (
                        r[0].lower(), r[1], r[2], r[3], p.name)
        # the hand-edit file: form, lemma, tag; # lines are comments
        self.hand_edits = []
        hp = d / HAND_EDITS_NAME
        if hp.is_file():
            self.files.append(hp)
            for i, line in enumerate(hp.read_text(encoding="utf-8")
                                     .splitlines(), 1):
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                t = [nfc(x).strip() for x in line.split("\t")]
                if len(t) < 3 or not all(t[:3]):
                    problems.append("%s line %d: form, lemma and tag, "
                                    "separated by tabs" % (hp.name, i))
                    continue
                self.hand_edits.append((t[0].lower(), lemma_key(t[1]), t[2],
                                        i))
        # historical-attested-spellings (decided 261113): spellings attested
        # in historical texts (the CSLD Historic-Word-List and the
        # pre-reform spellings taken out of the contemporary word list).
        self.attested = collections.OrderedDict()
        for p in decision_files(d, "historical-attested-spellings"):
            h, rows = take(p)
            for r in rows:
                if r and r[0].strip():
                    self.attested[nfc(r[0]).strip().lower()] = p.name
        self.addition_removals = set()
        for p in decision_files(d, "dictionary-addition-removals"):
            h, rows = take(p)
            for r in rows:
                self.addition_removals.add((r[0], r[1], r[2]))
        # Every round is read, and a later round wins for the same form
        # (decided 261112: per expression, never a whole file). Something
        # is taken out only by a removals kind, never by leaving it out of
        # a later round.
        by_form = collections.OrderedDict()
        for p in decision_files(d, "interjections"):
            h, rows = take(p)
            for r in rows:
                if r and r[0].strip():
                    by_form[r[0].strip().lower()] = r
        self.interjections = list(by_form.values())
        rm = collections.OrderedDict()
        for p in decision_files(d, "interjection-removals"):
            h, rows = take(p)
            for r in rows:
                if r and r[0].strip():
                    rm[r[0]] = True
        self.interjection_removals = list(rm)
        by_lemma = collections.OrderedDict()
        for p in decision_files(d, "lemma-standardization"):
            h, rows = take(p)
            for r in rows:
                if r and r[0].strip():
                    by_lemma[r[0].strip()] = r
        self.std_rows = list(by_lemma.values())
        # locutions (decided 261112): form, lemma, tag, flag (I always
        # joined, A ambiguous), with any further columns ignored; a later
        # round wins for the same multiword. locution-removals: form, why.
        self.locutions = collections.OrderedDict()
        for p in decision_files(d, "locutions"):
            h, rows = take(p)
            for r in rows:
                if len(r) >= 3 and r[0].strip():
                    self.locutions[multiword_key(r[0])] = (
                        lemma_key(r[1]) or multiword_key(r[0]).replace(
                            "a_el_", "al_").replace("de_el_", "del_"),
                        r[2].strip(),
                        (r[3].strip().upper() if len(r) > 3 else "") or "I",
                        p.name)
        self.locution_removals = collections.OrderedDict()
        for p in decision_files(d, "locution-removals"):
            h, rows = take(p)
            for r in rows:
                if r and r[0].strip():
                    self.locution_removals[multiword_key(r[0])] = p.name
        self.variants = {}
        for p in decision_files(d, "dictionary-variants"):
            h, rows = take(p)
            for r in rows:
                self.variants[r[0]] = (r[1], round_of(p))
        removed = set()
        for p in decision_files(d, "text-correction-removals"):
            h, rows = take(p)
            for r in rows:
                removed.add((r[0], r[1]))
        self.correction_removals = removed
        self.corrections = {}
        for p in decision_files(d, "text-corrections"):
            h, rows = take(p)
            for r in rows:
                if (r[0], r[1]) in removed:
                    continue
                self.corrections[r[0]] = (r[1], r[2], round_of(p))
        self.correction_lemmas = {}
        for p in decision_files(d, "correction-lemmas"):
            h, rows = take(p)
            for r in rows:
                if (r[0], r[1]) in removed:
                    continue
                self.correction_lemmas[r[0]] = (r[1], r[2], r[3],
                                                round_of(p))
        # verb-form-readings: the readings of verb forms the build could
        # not tag by itself (decided 261110b). entry is the dictionary form
        # that gets the tags: the form itself, or the base a form with
        # attached pronouns is built on (hace for háceme); "nearly
        # impossible" makes the reading almost never chosen on its own.
        self.verb_forms = {}
        self.verb_forms_file = ""
        for p in decision_files(d, "verb-form-readings"):
            h, rows = take(p)
            self.verb_forms_file = p.name
            for r in rows:
                if len(r) >= 5 and r[0].strip():
                    self.verb_forms[r[0].strip()] = (
                        lemma_key(r[1]), r[2].strip(),
                        [t.strip() for t in r[3].split(",") if t.strip()],
                        r[4].strip().lower() == "nearly impossible")
        self.replacements = {}
        for p in decision_files(d, "all-corpora-replacements"):
            h, rows = take(p)
            for r in rows:
                if len(r) >= 4 and r[3].strip() == "all":
                    self.replacements[r[0]] = (r[1], r[2], round_of(p))
        # THE NAMES (decided 261110d).
        # fixed-name-classes: name, class (place, person, organization,
        # other, or none: not fixed), source, ruling. The key is the name
        # as the recognizer writes it: lower case, words joined by _.
        self.fixed_names = {}
        for p in decision_files(d, "fixed-name-classes"):
            h, rows = take(p)
            here = {}
            for r in rows:
                if len(r) < 2 or not r[0].strip():
                    continue
                key = np_key(r[0])
                cls = ne_class(r[1])
                if cls != "none" and cls not in NE_CLASS_TAG:
                    problems.append("%s: %s: unknown class %r (place, "
                                    "person, organization, other or none)"
                                    % (p.name, r[0], r[1]))
                    continue
                if key in here and here[key] != cls:
                    problems.append("%s: %s is decided twice, as %s and %s"
                                    % (p.name, r[0], here[key], cls))
                    continue
                here[key] = cls
                self.fixed_names[key] = (cls, r[0].strip(),
                                         r[2].strip() if len(r) > 2 else "",
                                         p.name)
        # person-name-removals: entry, list, ruling.
        self.person_removals = {}
        for p in decision_files(d, "person-name-removals"):
            h, rows = take(p)
            for r in rows:
                if len(r) < 2 or not r[0].strip():
                    continue
                if r[1].strip() != "gazPER-c.dat":
                    problems.append("%s: %s: the list must be gazPER-c.dat, "
                                    "not %r" % (p.name, r[0], r[1]))
                    continue
                self.person_removals[np_key(r[0])] = p.name
        # sentence-start-classes: form, reading (name, place, person,
        # organization, other), keep own readings (yes; no; or word classes,
        # such as verbs: only the readings of those classes stay), share
        # (the reading's percentage among the readings the word has at the
        # start of a sentence, when some of its own stay), files (written,
        # speech, both), ruling. A form may have one rule for written texts
        # (np.dat) and another for speech (np-speech.dat) (decided
        # 261110g): start_classes[form][rule file] = (reading, keep, share,
        # decision file, classes kept). A later file's row replaces the
        # earlier rule for the files it names; two rows of one file for the
        # same form and the same rule file refuse the build.
        self.start_classes = {}
        for p in decision_files(d, "sentence-start-classes"):
            h, rows = take(p)
            here = set()
            for r in rows:
                if len(r) < 5 or not r[0].strip():
                    continue
                form = nfc(r[0]).strip().lower()
                reading, keep = ne_class(r[1]), r[2].strip().lower()
                share, files = r[3].strip(), r[4].strip().lower()
                bad = []
                if " " in form or "_" in form:
                    bad.append("one word only")
                if reading not in START_TAG:
                    bad.append("reading %r is not name, place, person, "
                               "organization or other" % r[1])
                only = ()
                if keep not in ("yes", "no"):
                    names = [x.strip() for x in keep.split(",") if x.strip()]
                    wrong = [x for x in names if x not in KEEP_CLASSES]
                    if not names or wrong:
                        bad.append("keep own readings must be yes, no or "
                                   "word classes (%s)"
                                   % ", ".join(sorted(KEEP_CLASSES)))
                    else:
                        only = tuple(dict.fromkeys(KEEP_CLASSES[x]
                                                   for x in names))
                if files not in START_FILES:
                    bad.append("files must be written, speech or both")
                value = None
                if keep != "no":
                    try:
                        value = float(share) / 100.0
                    except ValueError:
                        value = None
                    if value is None or not 0 < value < 1:
                        bad.append("a reading kept beside the word's own "
                                   "needs a share between 0 and 100")
                elif share:
                    bad.append("a share goes only with keep own readings "
                               "other than no")
                if bad:
                    problems.append("%s: %s: %s" % (p.name, r[0],
                                                    "; ".join(bad)))
                    continue
                twice = [npf for npf in START_FILES[files]
                         if (form, npf) in here]
                if twice:
                    problems.append("%s: %s is decided twice for %s"
                                    % (p.name, r[0], " and ".join(twice)))
                    continue
                for npf in START_FILES[files]:
                    here.add((form, npf))
                    self.start_classes.setdefault(form, {})[npf] = (
                        reading, keep != "no", value, p.name, only)
        # name-class-shares: name, class, share (percent), ruling. The rows
        # of a name in one file are its classes; a later file's rows for
        # the name replace them. Its shares must add up to 100.
        self.class_shares = {}
        for p in decision_files(d, "name-class-shares"):
            h, rows = take(p)
            here = collections.OrderedDict()
            for r in rows:
                if len(r) < 3 or not r[0].strip():
                    continue
                key, cls = np_key(r[0]), ne_class(r[1])
                try:
                    value = float(r[2])
                except ValueError:
                    value = -1
                if cls not in NE_CLASS_TAG or not 0 < value < 100:
                    problems.append("%s: %s: class %r, share %r: the class "
                                    "must be place, person, organization or "
                                    "other, the share between 0 and 100"
                                    % (p.name, r[0], r[1], r[2]))
                    continue
                here.setdefault(key, collections.OrderedDict())[cls] = value
            for key, shares in here.items():
                if abs(sum(shares.values()) - 100) > 1e-6:
                    problems.append("%s: the shares of %s add up to %g, not "
                                    "100" % (p.name, key, sum(shares.values())))
                    continue
                self.class_shares[key] = (shares, p.name)
        # place-only-forms: form, ruling.
        self.place_only = {}
        for p in decision_files(d, "place-only-forms"):
            h, rows = take(p)
            for r in rows:
                if r and r[0].strip():
                    self.place_only[r[0].strip().lower()] = p.name

    def standard_lemmas(self, name_lemmas):
        """(map, classes): lemma -> its standard lemma, with the two sheets
        chained (aylen -> aylén -> ailén); and lemma -> the word classes the
        standardization applies to: those of the decided words and names
        that have that lemma (so the lemma ala of the name Ala becomes alá,
        and the noun ala, wing, is untouched)."""
        sheets = collections.defaultdict(dict)
        for r in self.std_rows:
            if len(r) >= 3 and r[1].strip() and r[0] != r[1]:
                sheets[r[2]][lemma_key(r[0])] = lemma_key(r[1])
        order = ["Accents-Punctuation", "Spelling-Variants"] + sorted(
            s for s in sheets if s not in ("Accents-Punctuation",
                                           "Spelling-Variants"))

        def std(x):
            seen = set()
            while x not in seen:
                seen.add(x)
                y = x
                for s in order:
                    y = sheets[s].get(y, y)
                if y == x:
                    return x
                x = y
            return x
        m = {}
        for s in order:
            for l in sheets[s]:
                t = std(l)
                if t != l:
                    m[l] = t
        cls = collections.defaultdict(set)
        for f, l, c, *_ in self.additions:
            k = category_of(c)
            if k and k[0] not in ("-", "?"):
                c2 = {"AQ": "A", "RG": "R"}.get(k[0], k[0])
                cls[lemma_key(l)].add(c2)
        for r in self.interjections:
            cls[lemma_key(r[1])].add("I")
        for f, (c, l, cat, rd) in self.correction_lemmas.items():
            k = category_of(cat)
            if k and k[0] not in ("-", "?"):
                c2 = {"AQ": "A", "RG": "R"}.get(k[0], k[0])
                cls[lemma_key(l or c)].add(c2)
        for l in name_lemmas:
            cls[l].add("NP")
        classes = {}
        for l, t in m.items():
            classes[l] = cls.get(l, set()) | cls.get(t, set())
        return m, classes


# --------------------------------------------------------------------------
# Locutions

def split_locutions(text: str):
    head, body, tail = [], [], []
    part = 0
    for line in text.splitlines():
        s = line.strip()
        if part == 0:
            head.append(line)
            if s == "<Multiwords>":
                part = 1
        elif part == 1:
            if s == "</Multiwords>":
                tail.append(line)
                part = 2
            elif s:
                body.append(s)
        else:
            tail.append(line)
    return head, body, tail


def covered_by_pattern(key, lemma, entries, lemmas_of):
    """The pattern key (ya_<poh>) of an entry that already gives the
    multiword `key` (ya_po) the same lemma, or None. A <x> token matches
    any form with the lemma x."""
    toks = key.split("_")
    for k, (ps, fl) in entries.items():
        if "<" not in k or not any(l == lemma and g == "I" for l, g in ps):
            continue
        kt = k.split("_")
        if len(kt) != len(toks):
            continue
        ok = True
        for a, b in zip(kt, toks):
            if a.startswith("<") and a.endswith(">"):
                if a[1:-1] not in lemmas_of.get(b, ()):
                    ok = False
                    break
            elif a != b:
                ok = False
                break
        if ok:
            return k
    return None


def process_locutions(text: str, changes, name, interj=None, interj_rm=(),
                      add_new=True, lemmas_of=None, general=None,
                      decided=None, decided_rm=None, tagset=None,
                      problems=None):
    """The repairs of every build (lowercase keys, commas as tokens, lemma
    patterns, tag fixes, duplicate lines merged, jeans_day, ya_poh), then
    the interjection decisions: interj maps a key to (lemma, rare); a key
    in interj_rm loses its interjection reading. With add_new false, only
    the keys already there are changed."""
    head, body, tail = split_locutions(text)
    entries = collections.OrderedDict()
    have = {x.split()[0] for x in body}
    extra = [x for x in LOCUTIONS_ADD if x.split()[0] not in have]
    # FreeLing's general Spanish multiwords (decided 261112): every entry
    # whose key the Chilean file does not have; for a key in both, the
    # Chilean entry wins. They get the same repairs as the Chilean ones.
    gen_lines = []
    if general:
        chilean = {x.split()[0].lower(): x for x in body + extra}
        for s in split_locutions(general)[1]:
            k = s.split()[0].lower()
            if k in chilean:
                # a key already merged by an earlier build is silent; a
                # Chilean entry that differs is logged
                if " ".join(chilean[k].split()[1:]) != " ".join(s.split()[1:]):
                    changes.append((name, "not added", "FreeLing's general "
                                    "multiword: the Chilean entry wins", k,
                                    "", "", s))
                continue
            gen_lines.append(s)
    n_body, n_extra = len(body), len(extra)
    for n_line, s in enumerate(body + extra + gen_lines):
        new_line = n_body <= n_line < n_body + n_extra
        if n_line >= n_body + n_extra:
            t0 = s.split()
            changes.append((name, "added", "FreeLing's general multiword "
                            "(decided 261112)", t0[0].lower(),
                            t0[1] if len(t0) > 1 else "",
                            t0[2] if len(t0) > 2 else "", ""))
        t = s.split()
        form, flag = t[0], t[-1]
        if form != form.lower():
            changes.append((name, "changed", "key lowercased (FreeLing "
                            "matches multiwords in lowercase, so this one "
                            "never matched)", form.lower(), "", "", form))
            form = form.lower()
        if re.search(r"[^_],", form):
            new = re.sub(r"(?<=[^_]),", "_,", form)
            changes.append((name, "changed", "comma made its own token "
                            "(FreeLing splits it off, so this key never "
                            "matched)", new, "", "", form))
            form = new
        mid = t[1:-1]
        if flag not in ("I", "A") or len(mid) % 2:
            if len(t[1:]) % 2 == 0:
                mid, flag = t[1:], "I"
                changes.append((name, "changed", "locution lacked the I/A "
                                "flag; I added", form, "", "", s))
        pairs = []
        for i in range(0, len(mid), 2):
            lem, tag = mid[i], mid[i + 1]
            if "<" in lem or ">" in lem:
                new = lem.replace("<", "").replace(">", "")
                changes.append((name, "changed", "lemma written as a "
                                "pattern", form, new, tag, lem))
                lem = new
            fix = LOCUTION_TAG_FIX.get((form, tag)) or \
                LOCUTION_TAG_FIX.get(("*", tag))
            if fix:
                changes.append((name, "changed", "tag corrected", form, lem,
                                fix, tag))
                tag = fix
            pairs.append((lem, tag))
        if form in LOCUTION_RENAME:
            nf, nl = LOCUTION_RENAME[form]
            changes.append((name, "changed", "ya po: the key named a lemma "
                            "po that no form has; po and poh have the lemma "
                            "poh (decided 261109)", nf, nl, "", form))
            form = nf
            pairs = [(nl, g) for _, g in pairs]
        if form in entries:
            old_pairs, old_flag = entries[form]
            merged = old_pairs + [p for p in pairs if p not in old_pairs]
            changes.append((name, "changed", "duplicate locution lines "
                            "merged (FreeLing keeps only one)", form, "", "",
                            s))
            entries[form] = (merged, "A" if "A" in (old_flag, flag) else "I")
        else:
            if new_line:
                changes.append((name, "added", "multiword noun", form,
                                pairs[0][0], pairs[0][1], ""))
            entries[form] = (pairs, flag)
    # interjection decisions
    for key in sorted(interj_rm):
        if key in entries:
            ps, fl = entries[key]
            keep = [p for p in ps if p[1] != "I"]
            if len(keep) != len(ps):
                changes.append((name, "removed", "interjection reading "
                                "removed (decided 261108)", key, "", "I", ""))
                if keep:
                    entries[key] = (keep, fl)
                else:
                    del entries[key]
    for key, (lemma, rare) in (interj or {}).items():
        flag = "A" if rare else "I"
        if key in entries:
            ps, fl = entries[key]
            new = [p for p in ps if p[1] != "I"]
            had = [p for p in ps if p[1] == "I"]
            new = ([(lemma, "I")] + new) if had and ps[0][1] == "I" else \
                new + [(lemma, "I")]
            if (new, flag) != (ps, fl):
                changes.append((name, "changed", "multiword interjection as "
                                "decided (261108)%s" % (
                                    ", RARE: ambiguous, so its words can "
                                    "stay apart" if rare else ""),
                                key, lemma, "I", " ".join(
                                    [x for p in ps for x in p] + [fl])))
            entries[key] = (new, flag)
        elif add_new:
            pat = covered_by_pattern(key, lemma, entries, lemmas_of or {})
            if pat:
                changes.append((name, "not added", "multiword interjection "
                                "already given by the pattern %s" % pat,
                                key, lemma, "I", ""))
                continue
            entries[key] = ([(lemma, "I")], flag)
            changes.append((name, "added", "multiword interjection "
                            "(decided 261108)%s" % (
                                ", RARE: ambiguous" if rare else ""),
                            key, lemma, "I", ""))
    # the decided multiwords (locutions, locution-removals; decided 261112)
    for key, (lemma, tag, flag, fname) in (decided or {}).items():
        why = undecodable(tag, tagset) if tagset is not None and \
            not re.match(r"^\$\d+:", tag) else None
        if why or flag not in ("I", "A"):
            if problems is not None:
                problems.append("%s: multiword %s: %s" % (
                    fname, key, why or "flag %s is neither I nor A" % flag))
            continue
        old = entries.get(key)
        entries[key] = ([(lemma, tag)], flag)
        changes.append((name, "changed" if old else "added",
                        "multiword as decided (%s)" % fname, key, lemma,
                        tag, " ".join([x for p in old[0] for x in p] +
                                      [old[1]]) if old else ""))
    for key, fname in (decided_rm or {}).items():
        if key in entries:
            ps, fl = entries.pop(key)
            changes.append((name, "removed", "multiword removed as decided "
                            "(%s)" % fname, key, "", "",
                            " ".join([x for p in ps for x in p] + [fl])))
        elif problems is not None:
            problems.append("%s: no multiword %s to remove" % (fname, key))
    lines = [" ".join([f] + [x for p in ps for x in p] + [fl])
             for f, (ps, fl) in entries.items()]
    return "\n".join(head + lines + tail) + "\n", len(body), len(lines)


def multiword_key(form: str) -> str:
    """A decided multiword as FreeLing matches it: the locution key, with
    al and del split into a el and de el (FreeLing splits them before it
    matches multiwords; al tiro is a_el_tiro). A key with a <lemma> pattern
    is taken as written."""
    k = locution_key(form)
    if "<" in k:
        return k
    return "_".join({"al": "a_el", "del": "de_el"}.get(w, w)
                    for w in k.split("_"))


def locution_key(form: str) -> str:
    """A multiword as a locution key: lowercase, words joined by _, a comma
    its own token."""
    k = "_".join(form.lower().split())
    return re.sub(r"(?<=[^_]),", "_,", k)


# --------------------------------------------------------------------------
# Probabilities

def prob_sections(text: str):
    """section name -> (first content line index, end index)."""
    lines = text.splitlines()
    out, cur, start = {}, None, None
    for i, x in enumerate(lines):
        s = x.strip()
        m = re.fullmatch(r"<(/?)([A-Za-z]+)>", s)
        if not m:
            continue
        if not m.group(1):
            cur, start = m.group(2), i + 1
        elif cur == m.group(2):
            out[cur] = (start, i)
            cur = None
    return lines, out


def read_prob_tables(text: str):
    """(class_tags, single_tags, form_tags): the counts FreeLing reads."""
    lines, sec = prob_sections(text)
    cls, single, form = {}, {}, {}
    a, b = sec.get("ClassTagFreq", (0, 0))
    for x in lines[a:b]:
        t = x.split()
        if len(t) >= 3:
            cls[t[0]] = {t[i]: float(t[i + 1]) for i in range(1, len(t) - 1, 2)}
    a, b = sec.get("SingleTagFreq", (0, 0))
    for x in lines[a:b]:
        t = x.split()
        if len(t) >= 2:
            single[t[0]] = float(t[1])
    a, b = sec.get("FormTagFreq", (0, 0))
    for x in lines[a:b]:
        t = x.split()
        if len(t) >= 4:
            form[t[0]] = {t[i]: float(t[i + 1]) for i in range(2, len(t) - 1, 2)}
    return cls, single, form


def formtag_lines(text: str):
    """form -> its FormTagFreq line, as written."""
    lines, sec = prob_sections(text)
    a, b = sec.get("FormTagFreq", (0, 0))
    out = {}
    for x in lines[a:b]:
        st = x.strip()
        if st:
            out[st.split()[0]] = st
    return out


def word_counts(text: str):
    """form -> estimated number of occurrences in FreeLing's Spanish
    training corpus, from the <Word> section of tagger.dat (natural-log
    probabilities; the rarest observed word occurs once)."""
    m, on = {}, False
    for line in text.splitlines():
        s = line.strip()
        if s == "<Word>":
            on = True
            continue
        if s == "</Word>":
            break
        if on:
            t = s.split()
            if len(t) == 2 and not t[0].startswith("<"):
                try:
                    m[t[0]] = float(t[1])
                except ValueError:
                    pass
    if not m:
        return {}
    low = min(m.values())
    return {w: int(round(math.exp(v - low))) for w, v in m.items()}


def managed_line(form, shorts, existing, cls, single, set_np=None,
                 zero=(), share_among=None):
    """A FormTagFreq line for a form whose readings have the short tags
    `shorts` (short tag -> how many readings). The ordinary readings keep
    the proportions FreeLing gives them (the form's own counts, or else its
    ambiguity class, or else the overall tag frequencies), scaled to at
    least RARE_TOTAL when a tag is zeroed; the proper noun gets the share
    set_np; each short tag in `zero` (a rare interjection's I, a Chilean
    imperative's VMM) gets 0. With `share_among` (the short tags of the
    ordinary readings the word keeps at the start of a sentence), set_np is
    the proper noun's share among those and the proper noun only; the
    counts are then scaled up so that those readings add up to at least
    1000, which keeps the share exact. Returns the line, or None when
    nothing needs a line (one reading only)."""
    managed = set()
    if set_np is not None and "NP" in shorts:
        managed.add("NP")
    zeroed = {t for t in zero if t in shorts}
    managed |= zeroed
    zero_i = bool(zeroed)
    others = sorted(t for t in shorts if t not in managed)
    if not managed or (len(shorts) < 2):
        return None
    basis = {}
    if existing:
        basis = {t: existing.get(t, 0.0) for t in others}
    if others and sum(basis.get(t, 0.0) * shorts[t] for t in others) <= 0:
        key = "-".join(others)
        m = cls.get(key) or single
        basis = {t: m.get(t, 0.0) for t in others}
        if sum(basis[t] * shorts[t] for t in others) <= 0:
            basis = {t: 1.0 for t in others}
    from_line = bool(existing) and sum(
        existing.get(t, 0.0) * shorts[t] for t in others) > 0
    total = sum(basis[t] * shorts[t] for t in others)
    # Counts from the form's own line are kept as they are (FreeLing's
    # corpus counts); proportions from the class are scaled to 1000; the
    # other readings of a rare interjection to at least RARE_TOTAL. Run
    # again on its own output, the build gives the same line.
    if zero_i:
        target = RARE_TOTAL if (total < RARE_TOTAL or not from_line) else 0
    else:
        target = 0 if from_line else 1000
    counts = {}
    if others:
        if target:
            f = target / total
            counts = {t: (int(math.ceil(basis[t] * f)) if basis[t] > 0 else 0)
                      for t in others}
        else:
            counts = {t: (int(round(basis[t])) if basis[t] >= 1 or
                          basis[t] == 0 else 1) for t in others}
        total = sum(counts[t] * shorts[t] for t in others)
    if share_among is not None and "NP" in managed and others:
        kept = sum(counts[t] * shorts[t] for t in others if t in share_among)
        if 0 < kept < 1000:
            m = int(math.ceil(1000.0 / kept))
            counts = {t: counts[t] * m for t in others}
        total = sum(counts[t] * shorts[t] for t in others
                    if t in share_among)
    if "NP" in managed:
        if others:
            c = set_np / (1.0 - set_np) * total / shorts["NP"]
            counts["NP"] = max(1, int(round(c)))
        else:
            counts["NP"] = 1000
    for t in zeroed:
        counts[t] = 0
    keys = sorted(counts)
    return "%s %s %s" % (form, "-".join(keys),
                         " ".join("%s %d" % (k, counts[k]) for k in keys))


def process_probabilities(text: str, formtag_new, managed, changes,
                          place_only=()):
    """LemmaPreferences added; old lines of FORMTAG_REMOVE dropped; every
    line of a place-only form dropped (it has one reading only); the
    other new FormTagFreq lines added where the form has none. The managed
    lines (decided names, rare interjections, decided verb readings) replace
    any line of the same form and are written together, sorted, at the end
    of the section (a managed form whose line is None loses its line), so
    the file is the same whichever earlier build the basis comes from."""
    lines = text.splitlines()

    def section(name):
        a = lines.index("<%s>" % name)
        b = lines.index("</%s>" % name)
        return a, b
    a, b = section("LemmaPreferences")
    kept_lp = []
    for x in lines[a + 1:b]:
        f = x.split()[0] if x.split() else ""
        if f in place_only:
            changes.append(("probabilitats", "removed", "a place, never "
                            "another word: no lemma to prefer (decided "
                            "261110d)", f, "", "", x.strip()))
            continue
        kept_lp.append(x)
    lines[a + 1:b] = kept_lp
    a, b = section("LemmaPreferences")
    have = {tuple(x.split()) for x in lines[a + 1:b]}
    add = [p for p in LEMMA_PREFS if p not in have and p[0] not in place_only]
    for p in add:
        changes.append(("probabilitats", "added", "lemma preference",
                        p[0], p[1], "", "prefer %s over %s" % p))
    lines[b:b] = [" ".join(p) for p in add]
    a, b = section("FormTagFreq")
    keep = []
    n_repl = n_added = n_removed = 0
    old_line = {}
    for x in lines[a + 1:b]:
        st = x.strip()
        f = st.split()[0] if st else ""
        if st in FORMTAG_REMOVE:
            changes.append(("probabilitats", "removed", FORMTAG_REMOVE[st],
                            f, "", "", st))
            continue
        if f in place_only and f not in managed:
            changes.append(("probabilitats", "removed", "a place, never "
                            "another word: one reading only (decided "
                            "261110d)", f, "", "", st))
            continue
        if f in managed:
            old_line[f] = st
            continue
        keep.append(x)
    present = {x.split()[0] for x in keep if x.split()}
    present |= {f for f, (new, _) in managed.items() if new is not None}
    add_ft = []
    for entry, rule in [(x, "interjection preferred (from the 2026 tree)")
                        for x in FORMTAG_FIXED] + formtag_new:
        f = entry.split()[0]
        if f in present:
            continue
        present.add(f)
        add_ft.append(entry)
        n_added += 1
        changes.append(("probabilitats", "added", rule, f, "", "", entry))
    for f in sorted(managed):
        new, rule = managed[f]
        st = old_line.get(f)
        if new is None:
            if st is not None:
                n_removed += 1
                changes.append(("probabilitats", "removed", rule, f, "", "",
                                st))
            continue
        add_ft.append(new)
        if st is None:
            n_added += 1
            changes.append(("probabilitats", "added", rule, f, "", "", new))
        elif new != st:
            n_repl += 1
            changes.append(("probabilitats", "changed", rule, f, "", "",
                            "%s  ->  %s" % (st, new)))
    lines[a + 1:b] = keep + add_ft
    return ("\n".join(lines) + "\n", len(add), n_added, n_repl, n_removed)


# --------------------------------------------------------------------------
# The name recognizer and the quantities

def process_np(text: str, changes, problems):
    """Adds every single letter to the Ignore section of np.dat, as "x 1"
    (ignore always)."""
    lines = text.splitlines()
    starts = [i for i, x in enumerate(lines) if x.strip() == "<Ignore>"]
    ends = [i for i, x in enumerate(lines) if x.strip() == "</Ignore>"]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        problems.append("np.dat: expected exactly one <Ignore> ... </Ignore> "
                        "section, found %d opening and %d closing lines"
                        % (len(starts), len(ends)))
        return text
    a, b = starts[0], ends[0]
    listed = {x.split()[0].lower() for x in lines[a + 1:b] if x.split()}
    add = []
    for c in NP_LETTERS:
        if c in listed:
            continue
        add.append("%s 1" % c)
        changes.append(("np", "added", "single letter: never a name (ignore "
                        "always)", c, "", "", "%s 1" % c))
    lines[b:b] = add
    return "\n".join(lines) + "\n"


def list_lines(text: str):
    """The entries of a one-name-per-line list, in order, once each."""
    return list(dict.fromkeys(x.strip() for x in text.splitlines()
                              if x.strip()))


def check_name_list(text: str, name: str, problems):
    """A name list FreeLing reads: NFC, lower case, one name per line, the
    words of a name joined by _."""
    for n, x in enumerate(text.splitlines(), 1):
        st = x.strip()
        if not st:
            continue
        if nfc(st) != st or st != st.lower() or " " in st or "\t" in st:
            problems.append("%s line %d is not one lower-case NFC name with "
                            "its words joined by _: %r" % (name, n, x))
            if len(problems) > 50:
                return


def np_variants(key: str):
    """The name and, when it holds del or al as a word, the same with
    FreeLing's contraction (viña_del_mar and viña_de_el_mar)."""
    g = key
    for short, full in NP_CONTRACTIONS:
        g = re.sub(r"(?:^|(?<=_))%s(?=_)" % short, full, g)
    return [key] if g == key else [key, g]


def process_names(srcb, gazper_p_text, cities_rows, dicc_text, loc_text,
                  np_text, dec, changes, dlog, problems):
    """The name lists of FreeLing's classifier and the recognizer's two
    rule files (decided 261110d). Returns (files, fixed_rows, counts):
    files maps each release path to its text; fixed_rows are the rows of
    NAME-CLASSES.tsv."""
    cities = list_lines(srcb["data/common/nec/cities.dat"].decode("utf-8"))
    ccl = list_lines(srcb["data/common/nec/cities-CL.dat"].decode("utf-8"))
    gl = list_lines(srcb["data/es/nerc/data/gazLOC-c.dat"].decode("utf-8"))
    gpc = list_lines(srcb["data/es/nerc/data/gazPER-c.dat"].decode("utf-8"))
    cities_s, ccl_s, gl_s = set(cities), set(ccl), set(gl)
    check_name_list(gazper_p_text, "gazPER-p.dat", problems)
    clc = {np_key(f) for f, l, g in cities_rows}
    # Every place name of the Chilean data: the Chilean place list, the
    # Chilean places of FreeLing's cities-CL.dat, and every place reading
    # of the default dictionary and of the locutions.
    places = {np_key(l) for f, l, g in cities_rows} | ccl_s
    words = set()
    for line in dicc_text.splitlines():
        p = line.split()
        if len(p) < 3 or len(p) % 2 == 0:
            continue
        pairs = list(zip(p[1::2], p[2::2]))
        places |= {np_key(l) for l, g in pairs if g == "NP00G00"}
        if any(not g.startswith("NP") for _, g in pairs):
            words.add(p[0])
    for line in loc_text.splitlines():
        p = line.split()
        for i in range(1, len(p) - 1):
            if p[i + 1] == "NP00G00":
                places.add(np_key(p[i]))
    # The fixed names: the Chilean places FreeLing's cities-CL.dat adds to
    # its world list, the places of the Chilean list that FreeLing has in
    # neither list (antofa, conce, valpo ...), and the decisions, which win
    # (none: not fixed).
    fixed = {}
    for k in sorted(ccl_s - cities_s):
        fixed[k] = ("place", "FreeLing's cities-CL.dat: a Chilean place it "
                    "adds to the world list", "")
    for k in sorted(clc - cities_s - ccl_s):
        fixed[k] = ("place", "CL.cities.GRAM.txt: a place in neither of "
                    "FreeLing's city lists", "")
    n_none = 0
    for k, (cls, name, source, fn) in sorted(dec.fixed_names.items()):
        if cls == "none":
            if k in fixed:
                del fixed[k]
            n_none += 1
            dlog.append((fn, name, "not a fixed name", "applied",
                         "left to FreeLing's classifier (%s)" % source))
            continue
        fixed[k] = (cls, "%s (%s)" % (fn, source), "")
        dlog.append((fn, name, cls, "applied", "%s: always %s, %s"
                     % (" and ".join(np_variants(k)), NE_CLASS_TAG[cls],
                        source)))
    fixed_places = {k for k, v in fixed.items() if v[0] == "place"}
    # The place names the classifier's lists get: every place name, except
    # a single word that is also an ordinary word of the dictionary (a
    # common noun, a verb ...) and not a fixed place.
    add = {p for p in places
           if "_" in p or p not in words or p in fixed_places}
    loc_out = sorted(gl_s | add)
    cit_out = sorted(cities_s | ccl_s | add)
    for k in sorted(add - gl_s):
        changes.append(("gazLOC-c", "added", "a place name of the Chilean "
                        "data (decided 261110d)", k, k, "", ""))
    for k in sorted((ccl_s | add) - cities_s):
        changes.append(("cities", "added", "a Chilean place of FreeLing's "
                        "cities-CL.dat" if k in ccl_s else "a place name of "
                        "the Chilean data (decided 261110d)", k, k, "", ""))
    rm = dec.person_removals
    per_out = []
    for k in gpc:
        if k in rm:
            m = re.search(r"--(\d{6}[a-z]?)\.tsv$", rm[k])
            changes.append(("gazPER-c", "removed", "not a person: a place "
                            "(decided %s)" % (m.group(1) if m else rm[k]),
                            k, k, "", rm[k]))
            dlog.append((rm[k], k, "removed from gazPER-c.dat", "applied",
                         "FreeLing's classifier no longer reads it as a "
                         "person"))
            continue
        per_out.append(k)
    for k in sorted(set(rm) - set(gpc)):
        dlog.append((rm[k], k, "removed from gazPER-c.dat", "not applied",
                     "not in FreeLing's list"))
    # A name with class shares is decided by the classifier: it cannot
    # also have a fixed class, which would come first.
    for k, (shares, fn) in sorted(dec.class_shares.items()):
        if k in fixed:
            problems.append("%s: %s has class shares and a fixed class (%s): "
                            "decide it as none in fixed-name-classes first"
                            % (fn, k, fixed[k][1]))
    fixed_rows = []
    lines = []
    for k in sorted(fixed):
        cls, source, _ = fixed[k]
        for v in np_variants(k):
            lines.append("%s %s" % (v, NE_CLASS_TAG[cls]))
            fixed_rows.append((v, "fixed class", cls, NE_CLASS_TAG[cls], "",
                               "np.dat, np-speech.dat", source,
                               "" if v == k else "the same, as FreeLing "
                               "writes del and al inside a name"))
    # The readings at the start of a sentence (decided 261110e), by file.
    start_lines = {fn: [] for fn, _, _ in NP_FILES}
    for f, per in sorted(dec.start_classes.items()):
        # the rule files that share one rule, in the order of NP_FILES
        groups = collections.OrderedDict()
        for npf, _, _ in NP_FILES:
            if npf in per:
                groups.setdefault(per[npf], []).append(npf)
        for (reading, keep, share, fn, only), npfs in groups.items():
            tag = START_TAG[reading]
            flag = (" keep:" + ",".join(only)) if only else (
                " keep" if keep else "")
            own = ("its own %s readings" % " and ".join(
                k for k, v in KEEP_CLASSES.items() if v in only)) if only \
                else "its own readings"
            for npf in npfs:
                start_lines[npf].append("%s %s%s" % (f, tag, flag))
            fixed_rows.append((f, "at the start of a sentence", reading, tag,
                               "%g%%" % round(share * 100, 2) if keep else "",
                               ", ".join(npfs), fn,
                               "beside %s only; the tagger chooses" % own
                               if only else
                               "beside its own readings; the tagger chooses"
                               if keep else "its own readings dropped"))
            dlog.append((fn, f, "at the start of a sentence: %s" % reading,
                         "applied", "%s%s, in %s" % (
                             tag, " kept beside %s at %g%%"
                             % (own, round(share * 100, 2)) if keep else
                             ", its own readings dropped",
                             " and ".join(npfs))))
    # The class shares (decided 261110e), for the classifier's file.
    share_lines = []
    for k, (shares, fn) in sorted(dec.class_shares.items()):
        share_lines.append("%s %s" % (k, " ".join(
            "%s %.4f" % (NE_CLASS_TAG[c], v / 100.0)
            for c, v in shares.items())))
        for c, v in shares.items():
            fixed_rows.append((k, "class share", c, NE_CLASS_TAG[c],
                               "%g%%" % v, "nec-ab-poor1.dat", fn, ""))
        dlog.append((fn, k, "class shares", "applied", ", ".join(
            "%s %g%%" % (c, v) for c, v in shares.items())))
    files = {"data/common/nec/cities.dat": "\n".join(cit_out) + "\n",
             "data/es/nerc/data/gazLOC-c.dat": "\n".join(loc_out) + "\n",
             "data/es/nerc/data/gazPER-c.dat": "\n".join(per_out) + "\n",
             "data/es/nerc/data/gazPER-p.dat": gazper_p_text}
    for fn, start, what in NP_FILES:
        sec = ["",
               "## ---------------------------------------------------------"
               "-------------",
               "## FreeLing es-CL 2027: the name classes (decided 261110d).",
               "## Read only by FreeLing 4.2 with the name-class change",
               "## (software/patches/freeling-4.2-np-classes.patch); "
               "FreeLing without it",
               "## skips these sections."] + [
               "## " + x for x in textwrap.wrap("This file: %s." % what, 70)
               ] + ["##",
               "## DictionaryClasses: a one-word name whose dictionary entry "
               "has one of",
               "## these proper-noun tags keeps it, in this order, with the "
               "dictionary's",
               "## lemma; the classifier is not asked.",
               "<DictionaryClasses>",
               " ".join(DICT_CLASSES),
               "</DictionaryClasses>",
               "## ClassesAtSentenceStart: yes, the classes also apply at the "
               "start of a",
               "## sentence (a line of transcribed speech); no, a word there "
               "that is also",
               "## a common noun or an adjective is left to FreeLing.",
               "<ClassesAtSentenceStart>",
               start,
               "</ClassesAtSentenceStart>",
               "## FixedClasses: form tag. The name, in lower case with its "
               "words joined",
               "## by _, always gets this tag, whatever the classifier would "
               "say.",
               "<FixedClasses>"] + lines + ["</FixedClasses>"]
        if start_lines[fn]:
            sec += ["## SentenceStartClasses: form tag [keep[:prefix,...]]. "
                    "At the start of a",
                    "## sentence the one-word name gets this reading, "
                    "whatever the rules above",
                    "## say; with keep its own readings stay beside it and "
                    "the tagger chooses",
                    "## (the odds are in probabilitats.dat); with keep:V only "
                    "those whose tags",
                    "## begin with V (verbs) stay. NP00000: the classifier "
                    "decides the class.",
                    "<SentenceStartClasses>"] + start_lines[fn] + [
                    "</SentenceStartClasses>"]
        files["data/es/es-cl/" + fn] = np_text.rstrip("\n") + "\n" + \
            "\n".join(sec) + "\n"
    nec_text = srcb["data/es/nerc/nec/nec-ab-poor1.dat"].decode("utf-8")
    nec_sec = ["",
               "## ---------------------------------------------------------"
               "-------------",
               "## FreeLing es-CL 2027: the class shares (decided 261110e).",
               "## Read only by FreeLing 4.2 with the name-class change",
               "## (software/patches/freeling-4.2-np-classes.patch); "
               "FreeLing 4.2 without",
               "## it refuses this file.",
               "## ClassShares: form tag share [tag share ...]. The name "
               "takes one of these",
               "## classes: the classifier's weight for each plus half the "
               "log odds of its",
               "## share; the highest wins.",
               "<ClassShares>"] + share_lines + ["</ClassShares>"]
    files["data/es/nerc/nec/nec-ab-poor1.dat"] = nec_text.rstrip("\n") + \
        "\n" + "\n".join(nec_sec) + "\n"
    counts = {"places": len(places), "gazLOC-c added": len(add - gl_s),
              "cities added": len((ccl_s | add) - cities_s),
              "gazPER-c removed": len(gpc) - len(per_out),
              "fixed names": len(fixed), "fixed lines": len(lines),
              "fixed places": len(fixed_places), "not fixed": n_none,
              "gazLOC-c": len(loc_out), "cities": len(cit_out),
              "gazPER-c": len(per_out),
              "gazPER-p": len(list_lines(gazper_p_text)),
              "start np.dat": len(start_lines["np.dat"]),
              "start np-speech.dat": len(start_lines["np-speech.dat"]),
              "shares": len(share_lines)}
    return files, fixed_rows, counts


def process_quantities(text: str, changes, problems):
    """The Chilean currency changes: each pattern must occur exactly once;
    the new codes go to the end of <Measure>, the new names to the end of
    <MeasureNames>."""
    for old, new, rule in QUANTITY_CHANGES:
        n = text.count(old)
        if n != 1:
            problems.append("quantities.dat: %r occurs %d times, not once"
                            % (old.strip(), n))
            continue
        text = text.replace(old, new)
        changes.append(("quantities", "changed", rule, new.split()[0],
                        new.split()[1], "", old.strip()))
    for sec, items in (("Measure", QUANTITY_MEASURES),
                       ("MeasureNames", QUANTITY_NAMES)):
        end = "</%s>\n" % sec
        if text.count(end) != 1:
            problems.append("quantities.dat: no single %s" % end.strip())
            continue
        present = set(text.splitlines())
        add = [x for x in items if x not in present]
        for x in add:
            changes.append(("quantities", "added", "the euro's code"
                            if "EUR" in x else "Chilean currency unit "
                            "(decided 261109)", x.split()[0],
                            x.split()[1], "", x))
        text = text.replace(end, "".join(x + "\n" for x in add) + end)
    # the unit names removed (decided 261112), from <MeasureNames> only
    lines = text.split("\n")
    try:
        a = lines.index("<MeasureNames>")
        b = lines.index("</MeasureNames>", a)
    except ValueError:
        problems.append("quantities.dat: no <MeasureNames> section")
        return text
    drop = set()
    for name, why in QUANTITY_REMOVALS:
        hits = [i for i in range(a + 1, b) if lines[i].split()[:1] == [name]]
        if len(hits) != 1:
            problems.append("quantities.dat: the unit name %r occurs %d times "
                            "in <MeasureNames>, not once" % (name, len(hits)))
            continue
        f = lines[hits[0]].split()
        drop.add(hits[0])
        changes.append(("quantities", "removed", why, f[0],
                        f[1] if len(f) > 1 else "", "", lines[hits[0]].strip()))
    # the unit codes removed (decided 261112), from <Measure> only
    try:
        ma = lines.index("<Measure>")
        mb = lines.index("</Measure>", ma)
    except ValueError:
        problems.append("quantities.dat: no <Measure> section")
        return text
    for code, why in QUANTITY_CODE_REMOVALS.items():
        hits = [i for i in range(ma + 1, mb) if lines[i].strip() == code]
        if len(hits) != 1:
            problems.append("quantities.dat: the unit code %r occurs %d times "
                            "in <Measure>, not once" % (code, len(hits)))
            continue
        users = [lines[i].strip() for i in range(a + 1, b) if i not in drop
                 and lines[i].split()[1:2] == code.split()[1:2]]
        if users:
            problems.append("quantities.dat: the unit code %r is still used "
                            "by %s" % (code, "; ".join(users)))
            continue
        drop.add(hits[0])
        changes.append(("quantities", "removed", why, code.split()[1],
                        code.split()[0], "", code))
    return "\n".join(l for i, l in enumerate(lines) if i not in drop)


def next_free(path: Path) -> Path:
    if not path.exists():
        return path
    for c in "bcdefghijklmnopqrstuvwxyz":
        p = path.with_name(path.name + c)
        if not p.exists():
            return p
    raise SystemExit("REFUSED: too many deprecated builds named %s" % path)


TUTEO_README = """\
# The tuteo-tagged dictionary (dicc-0-tags)

`dicc-0-tags.zip` holds `dicc-0-tags.src`: the default (contemporary)
FreeLing es-CL 2027 dictionary with voseo tagged like tuteo. A voseo verb
form carries the tuteo tag (cantai is tagged as cantas, verb, main,
indicative, present, 2nd person, singular), and vos is tagged like te and
ti (pronoun, personal, 2nd person, common gender, singular, no voseo
value). Voseo and tuteo are then told apart only by their spelling.

It is not used by the CSLD. It exists for anyone who needs FreeLing's
Spanish tags unchanged, for example a tool that rejects the voseo value.

To use it:

1. Unzip it: `unzip dicc-0-tags.zip`
2. Install `dicc-0-tags.src` as `dicc.src` in a FreeLing data folder of its
   own, never over the default dictionary, and point a config at it with
   `DictionaryFile=`.
3. Keep `TagsetFile=` pointing at the Chilean tagset: it decodes both tag
   sets.

It is rebuilt with every release by `freeling_escl_build.py`; the copy here
always matches the release it came with.
"""

# mm keeps the millimeter reading as by far the more probable one; mmm is a
# nearly impossible interjection reading (decided 261108; in COSCACH the
# text itself becomes mmm).
MM_RARE = {"mm"}


def stem_of(name: str) -> str | None:
    """The kind of a decision file: the part before "--" of NAME--ROUND.tsv,
    or None for any other name."""
    if not name.endswith(".tsv") or "--" not in name:
        return None
    return name.split("--", 1)[0]


def check_links(ddir: Path, linked: Path):
    """Problems with the links between escl-sources and the COSCACH decisions
    folder: an ordinary file of a kind the build reads in the COSCACH folder
    (it would never reach the build), a link there that does not lead to its
    file in escl-sources, and an escl-sources file without its link (the
    spelling step would never see it)."""
    out = []
    real = ddir.resolve()
    for p in sorted(linked.iterdir()):
        if stem_of(p.name) not in BUILD_STEMS or \
                stem_of(p.name) in UNLINKED_STEMS:
            continue
        if not p.is_symlink():
            out.append("%s is an ordinary file in the COSCACH decisions "
                       "folder: move it into escl-sources with "
                       "freeling_escl_sources_move.py" % p)
            continue
        target = p.resolve()
        if target != real / p.name or not target.is_file():
            out.append("%s is a link to %s, not to its file in %s"
                       % (p, os.readlink(p), ddir))
    for p in sorted(ddir.iterdir()):
        if stem_of(p.name) not in BUILD_STEMS or \
                stem_of(p.name) in UNLINKED_STEMS:
            continue
        q = linked / p.name
        if not q.is_symlink():
            out.append("%s has no link in %s: run "
                       "freeling_escl_sources_move.py" % (p, linked))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="freeling_escl_build.py",
        description="Build %s. EXECUTES BY DEFAULT." % RELEASE)
    ap.add_argument("--root", default=None, help="project root (default: "
                    "found from this script's location by PROJECT_ROOT.txt)")
    ap.add_argument("--source-tree", default=str(SOURCE_TREE),
                    help="the FreeLing 4.2 source tree (default: %(default)s)")
    ap.add_argument("--build-tree", default=str(BUILD_TREE),
                    help="its deployed es-cl folder (default: %(default)s)")
    ap.add_argument("--decisions", default=None, help="the decisions folder "
                    "(default: <project root>/%s)" % DECISIONS_REL)
    ap.add_argument("--linked-folder", default=str(LINKED_DECISIONS),
                    help="the COSCACH decisions folder, whose links to the "
                    "decisions folder are checked (default: %(default)s)")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--explode-dir", default=str(EXPLODE_DIR))
    ap.add_argument("--patches", default=None, help="the folder of the "
                    "change to FreeLing's name recognizer (default: "
                    "../patches beside this script's folder)")
    ap.add_argument("--packaging", default=None, help="the folder of the "
                    "packaging for Fedora, Debian and Ubuntu (default: "
                    "../packaging beside this script's folder)")
    ap.add_argument("--privacy", default=None, help="the privacy file "
                    "(default: %s in the folder above this script's)"
                    % PRIVACY_NAME)
    ap.add_argument("--dry-run", action="store_true",
                    help="build and check in memory, write nothing")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + VERSION)
    a = ap.parse_args(argv)
    here = Path(__file__).resolve().parent
    root = Path(a.root).resolve() if a.root else find_project_root(here)
    if root is None:
        log("REFUSED: no PROJECT_ROOT.txt above this script; give --root")
        return 2
    gram = root / GRAM_REL
    chilean_tagset = root / TAGSET_REL
    ddir = Path(a.decisions) if a.decisions else root / DECISIONS_REL
    st, bt, out = Path(a.source_tree), Path(a.build_tree), Path(a.out)
    readme = here / README_NAME
    patches = Path(a.patches) if a.patches else here.parent / "patches"
    packaging = Path(a.packaging) if a.packaging else here.parent / "packaging"
    gazper_p = root / GAZPER_P_REL
    privacy = Path(a.privacy) if a.privacy else here.parent / PRIVACY_NAME
    license = here / LICENSE_NAME

    log("=" * 78)
    log("FREELING ES-CL BUILD  %s   (%s)%s" % (VERSION, RELEASE,
                                              "   DRY RUN" if a.dry_run else ""))
    log("=" * 78)
    log("FreeLing 4.2 source : %s" % st)
    log("Chilean tagset      : %s" % chilean_tagset)
    log("Chilean lists       : %s" % gram)
    log("decisions           : %s" % ddir)
    log("links checked in    : %s" % a.linked_folder)
    log("deployed es-cl data : %s" % bt)
    log("person-name parts   : %s" % gazper_p)
    log("name-class change   : %s" % patches)
    log("packaging           : %s" % packaging)
    log("release folder      : %s" % out)
    log("privacy file        : %s" % privacy)
    software = [here / f for f in SOFTWARE_HERE] + \
        [Path(a.explode_dir) / f for f in EXPLODE_FILES]
    patch_files = [patches / f for f in PATCH_FILES]
    packaging_files = [packaging / f for f in PACKAGING_FILES + [PACKAGING_WORKFLOW]]
    needed = [st / r for r in FL42] + packaging_files + [
        chilean_tagset, bt / "probabilitats.dat", bt / "locucions.dat",
        readme, gazper_p, privacy, license] + software + patch_files + \
        [gram / f for _, f in LISTS + NAME_LISTS]
    missing = [str(p) for p in needed if not p.is_file()]
    if not ddir.is_dir():
        missing.append(str(ddir))
    linked = Path(a.linked_folder)
    if not linked.is_dir():
        missing.append(str(linked))
    if missing:
        for m in missing:
            log("REFUSED: not found: %s" % m)
        return 2
    try:
        prows, pterms = read_privacy(privacy)
    except (ValueError, UnicodeDecodeError) as exc:
        log("REFUSED: %s" % exc)
        return 2
    if sha(license.read_bytes()) != LICENSE_SHA:
        log("REFUSED: %s is not the text of the GNU AGPL 3.0 (sha256 %s, "
            "expected %s)" % (license, sha(license.read_bytes()), LICENSE_SHA))
        return 2
    link_problems = check_links(ddir, linked)
    if link_problems:
        for p in link_problems:
            log("REFUSED: %s" % p)
        return 2

    problems, changes, dlog = [], [], []
    srcb = {}
    for rel, h in FL42.items():
        b = (st / rel).read_bytes()
        if sha(b) != h:
            problems.append("%s is not FreeLing 4.2's file (sha256 %s, "
                            "expected %s)" % (st / rel, sha(b), h))
        srcb[rel] = b
    if sha(stock_es_cl_cfg().encode("utf-8")) != ES_CL_CFG_SHA:
        problems.append("the es-cl config carried in this script is not "
                        "FreeLing 4.2's (sha256 %s)"
                        % sha(stock_es_cl_cfg().encode("utf-8")))
    tagset_text = chilean_tagset.read_text(encoding="utf-8")
    if sha(tagset_text.encode("utf-8")) != TAGSET_SHA:
        problems.append("%s is not the approved Chilean tagset (sha256 %s, "
                        "expected %s)" % (chilean_tagset,
                                          sha(tagset_text.encode("utf-8")),
                                          TAGSET_SHA))
    problems += check_chilean_tagset(
        tagset_text, srcb["data/es/tagset.dat"].decode("utf-8"))
    if problems:
        for p in problems:
            log("REFUSED: %s" % p)
        return 2
    tagset = load_tagset(tagset_text)

    # ---- 1  the Spanish dictionary ---------------------------------------
    base = []
    for rel in sorted(r for r in FL42 if "/entries/" in r):
        base += read_entries_text(srcb[rel].decode("utf-8"))
    base = list(dict.fromkeys(base))
    es_dicc = build_dict(base)
    if sha(es_dicc) != ES_DICC_SHA:
        log("REFUSED: the Spanish dictionary built from FreeLing's entries "
            "is not FreeLing's (sha256 %s)" % sha(es_dicc))
        return 2
    es = collections.defaultdict(list)
    for f, l, g in base:
        es[f].append((l, g))
    es_by_lt = collections.defaultdict(set)
    for f, an in es.items():
        for l, g in an:
            es_by_lt[(l, g)].add(f)
    es_tags = {g for an in es.values() for _, g in an}
    base_set = set(base)
    log("")
    log("Spanish dictionary: %d forms, rebuilt byte for byte" % len(es))

    lists = {}
    for name, fn in LISTS + NAME_LISTS:
        lists[name] = read_gram(gram / fn, problems, changes, name)
        log("  %-12s %7d lines   %s" % (name, len(lists[name]), fn))
    if problems:
        for p in problems:
            log("REFUSED: %s" % p)
        return 2

    # ---- 2  fixes of the lists -------------------------------------------
    def drop(name, pred, rule):
        keep = []
        for e in lists[name]:
            if pred(e):
                changes.append((name, "removed", rule) + e + ("",))
            else:
                keep.append(e)
        lists[name] = keep

    def add(name, e, rule):
        if e not in lists[name]:
            lists[name].append(e)
            changes.append((name, "added", rule) + e + ("",))

    ir_set = set(IR)
    drop("verb", lambda e: e[1] == "ir" and e not in ir_set,
         "broken ir line (empty stem) or not in the correct ir paradigm")
    for e in IR:
        add("verb", e, "correct ir paradigm restored")
    for name, f, l, g, rule in FIX_REMOVE:
        drop(name, lambda e, f=f, l=l, g=g: e == (f, l, g), rule)
    for name, f, l, g, rule in FIX_ADD:
        add(name, (f, l, g), rule)
    for name in ("verb", "vaux"):
        drop(name, lambda e: e[1] in REMOVE_VOSEO_LEMMAS
             and e[2].startswith("V") and e[2].endswith("V"),
             "voseo form of erar removed: erar is practically never used and "
             "its voseo forms collided with ser")
    new = []
    for e in lists["tanc"]:
        if e[1] == "vos" and e[2].startswith("PP2CS") and e[2] != VOS_TAG:
            changes.append(("tanc", "changed", "the voseo pronoun tag",
                            e[0], e[1], VOS_TAG, e[2]))
            e = (e[0], e[1], VOS_TAG)
        new.append(e)
    lists["tanc"] = new
    for name, _ in LISTS:
        new = []
        for f, l, g in lists[name]:
            if f != f.lower() and any(t[0] in CLOSED
                                      for _, t in es.get(f.lower(), [])):
                changes.append((name, "removed", "capitalized form whose "
                                "lowercase is a function word (u, the "
                                "conjunction): FreeLing would give the "
                                "function word these readings", f, l, g, ""))
                continue
            if f != f.lower():
                changes.append((name, "changed", "form lowercased (FreeLing "
                                "looks words up in lowercase, so this entry "
                                "was never found)", f.lower(), l, g, f))
                f = f.lower()
            if g == "NCcS000":
                changes.append((name, "changed", "bad tag", f, l, "NCCS000",
                                g))
                g = "NCCS000"
            new.append((f, l, g))
        lists[name] = list(dict.fromkeys(new))
    # wrong lemmas in the lists (decided 261112)
    for name, old, new_l, forms, rule in LIST_LEMMA_FIXES:
        fixed = []
        n = 0
        for f, l, g in lists[name]:
            if l == old and forms.match(f):
                changes.append((name, "changed", rule, f, new_l, g, old))
                fixed.append((f, new_l, g))
                n += 1
            else:
                fixed.append((f, l, g))
        if n == 0 and not any(l == new_l and forms.match(f)
                              for f, l, g in fixed):
            problems.append("CL.%s: no entry with the lemma %s to correct, "
                            "and none with %s" % (name, old, new_l))
        lists[name] = list(dict.fromkeys(fixed))

    # ---- 3  the paradigm checks ------------------------------------------
    for name in ("verb", "vaux"):
        keep = []
        for f, l, g in lists[name]:
            src = es_by_lt.get((l, g))
            if (g.startswith("V") and not g.endswith("V") and src
                    and f not in src and l not in EXEMPT_LEMMAS
                    and l not in PARADIGM_KEEP
                    and not explained_overgeneration(f, l, src)):
                changes.append((name, "removed", "irregular verb conjugated "
                                "as regular; the Spanish dictionary has %s"
                                % "/".join(sorted(src)), f, l, g, ""))
                continue
            keep.append((f, l, g))
        lists[name] = keep
    for name in ("verb", "vaux"):
        keep = []
        for f, l, g in lists[name]:
            if (not g.startswith("V") or not g.endswith("V")
                    or l in EXEMPT_LEMMAS or l in PARADIGM_KEEP
                    or (f, l) in KEEP_ANYWAY):
                keep.append((f, l, g))
                continue
            exp = expected_voseo(l, g, es_by_lt)
            if exp is None or f in exp or explained_overgeneration(f, l, exp):
                keep.append((f, l, g))
                continue
            changes.append((name, "removed", "irregular verb conjugated as "
                            "regular; the Spanish paradigm gives %s"
                            % "/".join(sorted(exp)), f, l, g, ""))
            for c in sorted(exp):
                e = (c, l, g)
                if e not in keep and e not in lists[name]:
                    keep.append(e)
                    changes.append((name, "added", "voseo form derived from "
                                    "the Spanish paradigm", c, l, g,
                                    "replaces %s" % f))
        lists[name] = list(dict.fromkeys(keep))

    es_short = {(f, l) for f, an in es.items() for l, g in an
                if len(f) <= 2 and g.startswith("V")}
    for name, _ in LISTS:
        for f, l, g in lists[name]:
            if not TAG_RE.match(g) or (g not in es_tags
                                       and zero(g) not in es_tags
                                       and not g.startswith("NP")):
                problems.append("%s: unknown tag %s on %s %s" % (name, g, f, l))
            if g.startswith("V") and len(f) <= 2 and (f, l) not in es_short \
                    and (f, l) != ("so", "ser"):
                problems.append("%s: verb form of 2 letters or fewer, not in "
                                "the Spanish dictionary: %s %s %s"
                                % (name, f, l, g))
            if l == "ir" and (f, l, g) not in ir_set:
                problems.append("%s: ir line outside the paradigm: %s %s"
                                % (name, f, g))
            if l == "ser" and g.endswith("V") and f not in SER_FORMS:
                problems.append("%s: voseo ser form not confirmed: %s %s"
                                % (name, f, g))
            if re.search(r"[^a-záéíóúüñàèìòùâêîôûçäëïö\-]", f):
                problems.append("%s: character outside Spanish letters in "
                                "%r" % (name, f))
    if problems:
        for p in problems[:200]:
            log("REFUSED: %s" % p)
        log("Nothing was written.")
        return 2

    src = collections.OrderedDict((n, []) for n in SOURCES)
    for name, _ in LISTS:
        src[name] = list(lists[name])
    base_drop = set()

    def merge():
        m = collections.defaultdict(list)
        for t in base:
            if t not in base_drop:
                m[t[0]].append((t[1], t[2]))
        for name in SOURCES:
            for f, l, g in src[name]:
                if (l, g) not in m[f]:
                    m[f].append((l, g))
        return m
    merged = merge()

    # ---- 4  the decided words --------------------------------------------
    dec = Decisions(ddir, problems)
    if problems:
        for p in problems:
            log("REFUSED: %s" % p)
        return 2
    addf = dec.additions_file.name
    log("")
    log("decisions: %d files; additions from %s (%d rows)"
        % (len(dec.files), addf, len(dec.additions)))

    def exists(f, l):
        return f not in merged or any(x == l for x, _ in merged[f])

    additions = []
    decided_names = collections.defaultdict(set)
    decided_tags = []          # (form, lemma, tag): the decision wins
    verb_rows = collections.OrderedDict()
    verb_file = {}
    for row in dec.additions:
        form, lemma, cat = row[0], row[1], row[2]
        if (form, lemma, cat) in dec.addition_removals:
            dlog.append((addf, form, "%s, %s" % (lemma, cat), "not added",
                         "removed by dictionary-addition-removals"))
            continue
        k = category_of(cat)
        if k is None:
            dlog.append((addf, form, "%s, %s" % (lemma, cat), "not added",
                         "unknown category"))
            continue
        if k[0] == "-":
            dlog.append((addf, form, "%s, %s" % (lemma, cat), "not added",
                         "a foreign word is not a dictionary entry"))
            continue
        if k[0] == "V":
            verb_rows.setdefault(lemma_key(lemma), []).append(form)
            continue
        lines, notes = word_analyses(form, lemma, cat, exists)
        additions += lines
        if k[0] == "NP":
            decided_names[form].add("place" if k[1] == "NP00G00" else "name")
        decided_tags += [t for t in lines if t[0] == form]
        dlog.append((addf, form, "%s, %s" % (lemma, cat), "added",
                     "; ".join(["%s %s" % (f, g) for f, l, g in lines] +
                               notes)))
    # dictionary-words and the hand edits (decided 261112, 261113)
    for (fk, lk_), (form, lemma, cat, tag, wf) in dec.words.items():
        if tag:
            why = undecodable(tag, tagset) if TAG_RE.match(tag) else \
                "not a tag"
            if why:
                problems.append("%s: %s: tag %s: %s" % (wf, form, tag, why))
                continue
            additions.append((form, lemma_key(lemma), tag))
            decided_tags.append((form, lemma_key(lemma), tag))
            dlog.append((wf, form, "%s, %s" % (lemma, tag), "added",
                         "exactly this reading"))
            continue
        k = category_of(cat)
        if k is None or k[0] in ("-", "?"):
            problems.append("%s: %s: unknown category %r" % (wf, form, cat))
            continue
        if k[0] == "V":
            verb_rows.setdefault(lemma_key(lemma), []).append(form)
            verb_file[lemma_key(lemma)] = wf
            continue
        lines, notes = word_analyses(form, lemma, cat, exists)
        additions += lines
        if k[0] == "NP":
            decided_names[form].add("place" if k[1] == "NP00G00" else "name")
        decided_tags += [t for t in lines if t[0] == form]
        dlog.append((wf, form, "%s, %s" % (lemma, cat), "added",
                     "; ".join(["%s %s" % (f, g) for f, l, g in lines] +
                               notes)))
    for form, lemma, tag, i in dec.hand_edits:
        why = undecodable(tag, tagset) if TAG_RE.match(tag) else "not a tag"
        if why:
            problems.append("%s line %d: %s: tag %s: %s"
                            % (HAND_EDITS_NAME, i, form, tag, why))
            continue
        additions.append((form, lemma, tag))
        decided_tags.append((form, lemma, tag))
        dlog.append((HAND_EDITS_NAME, form, "%s, %s" % (lemma, tag), "added",
                     "hand edit, line %d" % i))
    vidx = verb_index(merged)
    models = VerbModels(vidx)
    unresolved = []
    n_paradigms = n_paradigm_lines = 0
    for lk, forms in verb_rows.items():
        addf = verb_file.get(lk, dec.additions_file.name)
        if not lk.endswith(INFINITIVE):
            for form in forms:
                dlog.append((addf, form, "%s, verb" % lk, "not added",
                             "the lemma is not an infinitive"))
            continue
        gen = []
        if lk not in vidx:
            ch = models.choose(lk)
            if ch:
                gen = models.conjugate(lk, ch)
                additions += gen
                n_paradigms += 1
                n_paradigm_lines += len(gen)
                dlog.append((addf, lk, "%s, verb" % lk, "paradigm added",
                             "%d forms, conjugated %s" % (len(gen), ch[0])))
            else:
                dlog.append((addf, lk, "%s, verb" % lk, "no paradigm",
                             "no known verb to conjugate it like"))
        pforms = collections.defaultdict(set)
        for f, g in vidx.get(lk, []):
            pforms[f].add(g)
        for f, l, g in gen:
            pforms[f].add(g)
        for form in forms:
            if form in pforms:
                if lk in vidx or gen:
                    dlog.append((addf, form, "%s, verb" % lk, "in the "
                                 "paradigm", ", ".join(sorted(pforms[form]))))
                continue
            bases = [b for b in clitic_bases(form)
                     if any(g[2] in "MNG" for g in pforms.get(b, ()))]
            if bases:
                dlog.append((addf, form, "%s, verb" % lk, "left to FreeLing",
                             "attached pronouns: FreeLing's affix rules "
                             "analyze it from %s" % bases[0]))
                continue
            tags, how = models.regular_tags(lk, form)
            if tags:
                additions += [(form, lk, g) for g in tags]
                dlog.append((addf, form, "%s, verb" % lk, "added",
                             "a regular form of %s (conjugated %s): %s"
                             % (lk, how, ", ".join(tags))))
                continue
            if form in dec.verb_forms:
                dlog.append((addf, form, "%s, verb" % lk, "decided",
                             "read as decided in %s" % dec.verb_forms_file))
                continue
            unresolved.append((form, lk))
    addf = dec.additions_file.name

    # The verb forms decided one by one (verb-form-readings).
    rare_tags = collections.defaultdict(set)    # entry -> short tags to zero
    for form, (lk, entry, tags, rare) in sorted(dec.verb_forms.items()):
        bad = [t for t in tags if not TAG_RE.match(t) or not t.startswith("V")]
        if bad or not entry or not tags:
            problems.append("%s: %s has no valid verb tags: %s"
                            % (dec.verb_forms_file, form, ", ".join(tags)))
            continue
        additions += [(entry, lk, t) for t in tags]
        if rare:
            for t in tags:
                rare_tags[entry].add(short_tag(t, tagset))
        dlog.append((dec.verb_forms_file, form, "%s, read as %s" % (
            lk, in_words([(lk, t) for t in tags])), "added", (
            "%s gets the reading%s" % (entry, ", nearly impossible on its own "
                                       "(FreeLing's affix rules analyze %s "
                                       "from it)" % form if rare else
                                       " (FreeLing's affix rules analyze %s "
                                       "from it)" % form
                                       if entry != form else ""))))

    # The decision wins: a decided word that has the same tag with another
    # lemma loses that other lemma (in the Spanish dictionary or the lists).
    dt = {(f, g): l for f, l, g in decided_tags}
    for f, l, g in list(base):
        nl = dt.get((f, g))
        if nl is not None and nl != l and (f, l, g) not in base_drop:
            base_drop.add((f, l, g))
            changes.append(("additions", "removed", "the decided lemma "
                            "replaces this one", f, l, g, "now %s" % nl))
    for name, _ in LISTS:
        keep = []
        for f, l, g in src[name]:
            nl = dt.get((f, g))
            if nl is not None and nl != l:
                changes.append((name, "removed", "the decided lemma replaces "
                                "this one", f, l, g, "now %s" % nl))
                continue
            keep.append((f, l, g))
        src[name] = keep

    # ---- 5  interjections ------------------------------------------------
    ijf = dec.files and next((p.name for p in dec.files
                              if p.name.startswith("interjections--")), "")
    interj_single, interj_multi = {}, {}
    for r in dec.interjections:
        form, lemma, prob, multi = r[0], r[1], r[2], r[3]
        rare = prob.strip().upper() == "RARE"
        if multi.strip() == "yes" or " " in form.strip():
            interj_multi[locution_key(form)] = (lemma_key(lemma), rare)
        else:
            interj_single[form.strip().lower()] = (lemma_key(lemma), rare)
    rm_single = {f.strip().lower() for f in dec.interjection_removals
                 if " " not in f.strip()}
    rm_multi = {locution_key(f) for f in dec.interjection_removals
                if " " in f.strip()}
    both = (set(interj_single) & rm_single) | (set(interj_multi) & rm_multi)
    if both:
        problems.append("interjections both kept and removed: %s"
                        % ", ".join(sorted(both)))
    for t in base:
        f, l, g = t
        if g != "I" or t in base_drop:
            continue
        if f in rm_single or (f in interj_single and
                              interj_single[f][0] != l):
            base_drop.add(t)
            changes.append(("interjections", "removed", "interjection "
                            "removed (decided 261108)" if f in rm_single else
                            "interjection lemma as decided (261108)", f, l,
                            g, ""))
    for name in SOURCES:
        keep = []
        for f, l, g in src[name]:
            if g == "I" and (f in rm_single or (
                    f in interj_single and interj_single[f][0] != l)):
                changes.append(("interjections", "removed", "interjection "
                                "removed (decided 261108)" if f in rm_single
                                else "interjection lemma as decided (261108)",
                                f, l, g, name))
                continue
            keep.append((f, l, g))
        src[name] = keep
    additions = [t for t in additions if not (t[2] == "I" and (
        t[0] in rm_single or (t[0] in interj_single and
                              interj_single[t[0]][0] != t[1])))]
    for f, (l, rare) in sorted(interj_single.items()):
        additions.append((f, l, "I"))
        dlog.append((ijf, f, "interjection, lemma %s%s" % (
            l, ", RARE" if rare else ""), "added",
            "single word%s" % ("; nearly impossible in probabilitats.dat"
                               if rare else "")))
    for k, (l, rare) in sorted(interj_multi.items()):
        dlog.append((ijf, k, "interjection, lemma %s%s" % (
            l, ", RARE" if rare else ""), "locution",
            "locucions.dat%s" % (", ambiguous (A)" if rare else "")))
    for f in sorted(rm_single | rm_multi):
        dlog.append((ijf.replace("interjections", "interjection-removals"),
                     f, "interjection removed", "removed", ""))
    src["additions"] = list(dict.fromkeys(additions))
    merged = merge()
    if problems:
        for p in problems:
            log("REFUSED: %s" % p)
        return 2

    # ---- 6  variants -----------------------------------------------------
    standard = sorted(f for f, an in merged.items()
                      if any(is_voseo(g) for _, g in an))
    variants = collections.OrderedDict()
    vrows = []
    skipped = collections.Counter()
    for f in standard:
        an = merged[f]
        sv = {(l, g[:4]) for l, g in an if is_voseo(g)}
        copy = [(l, g) for l, g in an if g.startswith("V")
                and not (VOSOTROS.match(g) and (l, g[:4]) in sv)]
        for rid, old, new, policy, _desc in RULES:
            if not f.endswith(old) or len(f) <= len(old):
                continue
            v = f[:-len(old)] + new
            if len(v) < 3:
                skipped[rid + " too short"] += 1
                continue
            existing = list(merged.get(v, [])) if v in merged else []
            if existing:
                if all(p in existing for p in copy):
                    continue
                if any(g[0] in CLOSED for _, g in existing):
                    skipped[rid + " closed class"] += 1
                    changes.append(("variants", "not added", "%s: %s exists "
                                    "as a closed-class word" % (rid, v), v,
                                    "", "", "from %s" % f))
                    continue
                if policy == "new" or (policy == "union" and not all(
                        is_voseo(g) for _, g in existing)):
                    skipped[rid + " exists"] += 1
                    changes.append(("variants", "not added", "%s: %s already "
                                    "exists with other readings" % (rid, v),
                                    v, "", "", "from %s; has %s" % (
                                        f, in_words(existing))))
                    continue
            if policy == "join" and v in AY_EXCEPT:
                skipped[rid + " exception"] += 1
                changes.append(("variants", "not added", "%s: exception" % rid,
                                v, "", "", "from %s" % f))
                continue
            got = variants.setdefault(v, [])
            for p in copy:
                if p not in got and p not in existing:
                    got.append(p)
            vrows.append((rid, v, f, in_words(copy),
                          "joins existing" if existing else "new form"))
    var_lines = [(v, l, g) for v, an in variants.items() for l, g in an]
    for v, l, g in var_lines:
        changes.append(("variants", "added", "spelling variant", v, l, g, ""))
        if len(v) <= 2:
            problems.append("variant of 2 letters or fewer: %s" % v)
    src["variants"] = var_lines
    merged = merge()

    # ---- 7  names (the lists) --------------------------------------------
    name_lines, name_skip = [], collections.Counter()
    for name in NAME_TAG:
        new = []
        for f, l, g in lists[name]:
            if g != NAME_TAG[name]:
                changes.append((name, "changed", "proper-noun class",
                                f, l, NAME_TAG[name], g))
                g = NAME_TAG[name]
            new.append((f, l, g))
        lists[name] = list(dict.fromkeys(new))
    for name, _ in NAME_LISTS:
        for f, l, g in lists[name]:
            lf = f.lower()
            if not re.fullmatch(r"[^\W\d_]+(?:['\-][^\W\d_]+)*", lf):
                name_skip["not a single word"] += 1
                changes.append((name, "not added", "not a single word", f, l,
                                g, ""))
                continue
            if lf in merged and not all(t.startswith("NP")
                                        for _, t in merged[lf]):
                name_skip["collides with a word"] += 1
                changes.append((name, "not added", "the lowercase form is a "
                                "word of the dictionary; left to the name "
                                "recognizer", lf, l.lower(), g, ""))
                continue
            e = (lf, l.lower(), g)
            if e in name_lines:
                continue
            name_lines.append(e)
    src["names"] = name_lines
    merged = merge()

    # ---- 8  non-standard forms and misspellings --------------------------
    nonstd = []
    for form, (stdf, rd) in sorted(dec.variants.items()):
        fn = "dictionary-variants--%s.tsv" % rd
        f, s = form.strip().lower(), stdf.strip().lower()
        if " " in s or " " in f:
            dlog.append((fn, form, "read as %s" % stdf, "not added",
                         "more than one word"))
            continue
        an = merged.get(s)
        if not an and s.endswith("mente") and len(s) > 7:
            an = [(s, "RG")]
        if not an:
            bases = [b for b in clitic_bases(f)
                     if any(g.startswith("V") and g[2] in "MNG"
                            for _, g in merged.get(b, []))]
            if bases:
                dlog.append((fn, form, "read as %s" % stdf,
                             "left to FreeLing", "attached pronouns: "
                             "FreeLing's affix rules analyze it from %s"
                             % bases[0]))
                continue
            dlog.append((fn, form, "read as %s" % stdf, "not added",
                         "%s is not in the dictionary" % s))
            continue
        new = [(f, l, g) for l, g in an]
        nonstd += new
        dlog.append((fn, form, "read as %s" % stdf, "added",
                     in_words([(l, g) for _, l, g in new])))
    src["nonstandard"] = list(dict.fromkeys(nonstd))
    merged = merge()

    corr = {}
    for f, (c, how, rd) in dec.replacements.items():
        corr[f.strip().lower()] = (c, how, "all-corpora-replacements--%s.tsv"
                                   % rd)
    for f, (c, how, rd) in dec.corrections.items():
        corr[f.strip().lower()] = (c, how, "text-corrections--%s.tsv" % rd)
    missp, corr_add = [], []
    for form in sorted(corr):
        c, how, fn = corr[form]
        c = c.strip().lower()
        h = how.strip()
        if not (h == "replace" or h.startswith("join if")):
            dlog.append((fn, form, "corrected to %s (%s)" % (c, h),
                         "not added", "a split or a join is corrected in the "
                         "text only"))
            continue
        if " " in c or not c:
            dlog.append((fn, form, "corrected to %s" % c, "not added",
                         "more than one word"))
            continue
        if form in merged:
            dlog.append((fn, form, "corrected to %s" % c, "not added",
                         "%s is already a word (%s)" % (
                             form, in_words(merged[form][:4]))))
            continue
        cl = dec.correction_lemmas.get(form)
        readings, how_read = [], ""
        if cl and cl[0].strip().lower() == c and (cl[1].strip() or
                                                  cl[2].strip()):
            lem = lemma_key(cl[1].strip().lower() or c)
            k = category_of(cl[2]) if cl[2].strip() else None
            if k and k[0] == "V":
                readings = [(l, g) for l, g in merged.get(c, [])
                            if l == lem and g.startswith("V")] or \
                    [(l, g) for l, g in merged.get(c, []) if g.startswith("V")]
                how_read = "the verb readings of %s" % c
            elif k and k[0] not in ("-", "?"):
                lines, notes = word_analyses(form, lem, cl[2],
                                             lambda f, l: True)
                readings = [(l, g) for f, l, g in lines if f == form]
                how_read = "%s, %s (correction-lemmas)" % (lem, cl[2])
                if c not in merged:
                    cl_lines, _ = word_analyses(c, lem, cl[2],
                                                lambda f, l: f not in merged)
                    corr_add += [t for t in cl_lines if t[0] == c]
                    dlog.append(("correction-lemmas--%s.tsv" % cl[3], c,
                                 "%s, %s" % (lem, cl[2]), "added",
                                 "the corrected word was not in the "
                                 "dictionary"))
        if not readings:
            readings = list(merged.get(c, []))
            how_read = "the readings of %s" % c
        if not readings and c.endswith("mente") and len(c) > 7:
            # FreeLing derives -mente adverbs by its affix rules; they are
            # not in the dictionary
            readings = [(c, "RG")]
            how_read = "%s, an adverb in -mente" % c
        if not readings:
            dlog.append((fn, form, "corrected to %s" % c, "not added",
                         "the correction %s is not in the dictionary" % c))
            continue
        missp += [(form, l, g) for l, g in readings]
        dlog.append((fn, form, "corrected to %s" % c, "added",
                     "read as %s: %s" % (how_read, in_words(readings[:6]))))
    src["common-misspellings"] = list(dict.fromkeys(missp))
    src["additions"] = list(dict.fromkeys(src["additions"] + corr_add))

    # ---- the exemption (decided 261110b) ---------------------------------
    merged = merge()
    exempted = []
    for f in sorted(decided_names):
        ordinary = [(l, g) for l, g in merged.get(f, [])
                    if not g.startswith("NP")]
        if any(g.startswith(EXEMPT_CLASSES) for _, g in ordinary):
            exempted.append(f)
            dlog.append((addf, f, "proper noun", "exempted", (
                "also %s: no proper-noun reading; FreeLing's name recognizer "
                "tags it when capitalized (decided 261110b)"
                % in_words(ordinary[:3]))))
    ex_set = set(exempted)
    src["additions"] = [t for t in src["additions"]
                        if not (t[0] in ex_set and t[2].startswith("NP"))]
    for f in exempted:
        del decided_names[f]
    merged = merge()
    # The verb forms first left untagged, now read through another decision.
    for form, lk in unresolved:
        an = merged.get(form, [])
        bases = [b for b in clitic_bases(form)
                 if any(l == lk and g.startswith("V") and g[2] in "MNG"
                        for l, g in merged.get(b, []))]
        if any(l == lk for l, _ in an):
            dlog.append((addf, form, "%s, verb" % lk, "read through another "
                         "decision", in_words([p for p in an if p[0] == lk])))
        elif bases:
            dlog.append((addf, form, "%s, verb" % lk, "left to FreeLing",
                         "attached pronouns: FreeLing's affix rules analyze "
                         "it from %s" % bases[0]))
        else:
            dlog.append((addf, form, "%s, verb" % lk, "not added",
                         "no tag could be determined"))

    # ---- 9  standard lemmas ----------------------------------------------
    name_lemmas = {l.lower() for n, _ in NAME_LISTS for _, l, _ in lists[n]}
    std_map, std_cls = dec.standard_lemmas(name_lemmas)

    def std_t(t):
        f, l, g = t
        s = std_map.get(l)
        if s and tag_class(g) in std_cls.get(l, ()):
            return (f, s, g)
        return t
    n_std = collections.Counter()
    stdlem = []
    for t in base:
        if t in base_drop:
            continue
        s = std_t(t)
        if s != t:
            base_drop.add(t)
            stdlem.append(s)
            n_std["spanish"] += 1
            changes.append(("standard-lemmas", "changed", "standard lemma "
                            "(decided 261108)", s[0], s[1], s[2], t[1]))
    for name in SOURCES:
        new = []
        for t in src[name]:
            s = std_t(t)
            if s != t:
                n_std[name] += 1
                changes.append((name, "changed", "standard lemma (decided "
                                "261108)", s[0], s[1], s[2], t[1]))
            new.append(s)
        src[name] = list(dict.fromkeys(new))
    src["standard-lemmas"] = list(dict.fromkeys(stdlem))

    # ---- 9b  the place-only forms (decided 261110d, 261110e) -------------
    # The form is a place and nothing else: every other reading goes, from
    # FreeLing's Spanish dictionary and from the Chilean lists, and the
    # place reading is added when it is missing.
    place_only = dict(dec.place_only)
    for f in sorted(place_only):
        m = re.search(r"--(\d{6}[a-z]?)\.tsv$", place_only[f])
        rule = "a place, never another word (decided %s)" % (
            m.group(1) if m else place_only[f])
        gone = []
        for t_ in base:
            if t_[0] == f and not t_[2].startswith("NP") and \
                    t_ not in base_drop:
                base_drop.add(t_)
                gone.append(t_)
                changes.append(("place-only", "removed", rule, t_[0], t_[1],
                                t_[2], "FreeLing's Spanish dictionary"))
        has_place = False
        for name in SOURCES:
            keep = []
            for t_ in src[name]:
                if t_[0] == f and not t_[2].startswith("NP"):
                    gone.append(t_)
                    changes.append(("place-only", "removed", rule, t_[0],
                                    t_[1], t_[2], "CL.%s" % name))
                    continue
                if t_[0] == f and t_[2] == "NP00G00":
                    has_place = True
                keep.append(t_)
            src[name] = keep
        if not has_place:
            src["names"].append((f, f, "NP00G00"))
            changes.append(("names", "added", rule, f, f, "NP00G00",
                            "place-only form"))
        dlog.append((place_only[f], f, "place only", "applied",
                     "removed %s; the place reading %s" % (
                         in_words([(l, g) for _, l, g in gone]) or "nothing",
                         "kept" if has_place else "added")))

    # ---- 9c  the accented one-syllable forms (decided 261112) -------------
    merged = merge()
    old_acc = []
    for acc, plain_ in OLD_ACCENTS:
        an = merged.get(plain_, [])
        if not an:
            problems.append("%s: %s has no reading to copy" % (acc, plain_))
            continue
        for l, g in an:
            old_acc.append((acc, l, g))
        dlog.append(("old-accents", acc, "the readings of %s" % plain_,
                     "added", in_words(an)))
    src["old-accents"] = list(dict.fromkeys(old_acc))
    merged = merge()

    # ---- 9d  common misspellings (decided 261112) ------------------------
    # Sources: every correctly spelled form, that is, its readings other
    # than those of the misspelt and non-standard forms the text keeps.
    wrong = set(src["common-misspellings"]) | set(src["nonstandard"])
    cand = collections.defaultdict(list)
    for f, an in merged.items():
        if "_" in f:
            continue
        s_ = f.translate(STRIP_MARKS)
        if s_ == f or s_ in merged:
            continue
        ok = [(l, g) for l, g in an if (f, l, g) not in wrong]
        if ok:
            cand[s_].append((f, ok))
    n_miss = collections.Counter()
    miss_new = []
    for s_, srcs in sorted(cand.items()):
        if len(srcs) > 1:
            n_miss["from several accented forms"] += 1
            continue
        f, ok = srcs[0]
        miss_new += [(s_, l, g) for l, g in ok]
        n_miss["added"] += 1
    src["common-misspellings"] = list(dict.fromkeys(
        src["common-misspellings"] + miss_new))
    dlog.append(("common-misspellings", "(generated)", "unaccented forms",
                 "added", "%d forms; %d left out (from several accented "
                 "forms)" % (n_miss["added"],
                             n_miss["from several accented forms"])))

    # ---- 10  the two dictionaries ----------------------------------------
    merged = merge()
    hist = {f: an for f, an in merged.items() if an}
    cont, cont_removed = contemporary(hist, changes)
    # The 19th-century spellings (decided 261112, 261113): generated from
    # every correctly spelled form of the historical dictionary but the
    # proper nouns, into its own entries file.
    wrong = set(src["common-misspellings"]) | set(src["nonstandard"])
    h_new = collections.defaultdict(list)     # new spelling -> readings
    h_coll = collections.defaultdict(list)    # existing word -> readings
    n_hist = collections.Counter()
    for f, an in list(hist.items()):
        if "_" in f:
            continue
        ok = [(l, g) for l, g in an if (f, l, g) not in wrong
              and not g.startswith("NP")]
        if not ok:
            continue
        allv = hist_variants(f, HIST_RULES)
        if not allv:
            continue
        bello = hist_variants(f, [r for r in HIST_RULES
                                  if r[0] in BELLO_ADOPTED])
        for v in allv:
            if v in hist:
                if v not in bello:
                    n_hist["already a word, not a Bello rule"] += 1
                    continue
                for p in ok:
                    if p not in hist[v] and p not in h_coll[v]:
                        h_coll[v].append(p)
            else:
                for p in ok:
                    if p not in h_new[v]:
                        h_new[v].append(p)
    h_coll = {v: ps for v, ps in h_coll.items() if ps}
    h_over = []
    # the spellings attested in historical texts: the readings of the one
    # modern spelling with the same letters, when the attested one has an
    # extra or a moved accent (a missing accent is never added: decided
    # 261112)
    modern_by_key = collections.defaultdict(list)
    for f, an in cont.items():
        if "_" in f:
            continue
        ok = [(l, g) for l, g in an if (f, l, g) not in wrong]
        if ok:
            modern_by_key[f.translate(ACCENTS_ONLY)].append((f, ok))
    h_att = collections.defaultdict(list)
    for a_, fname in dec.attested.items():
        if a_ in hist or a_ in h_new or not re.search("[áéíóú]", a_):
            n_hist["attested: already a word or no accent"] += 1
            continue
        c_ = [m for m in modern_by_key.get(a_.translate(ACCENTS_ONLY), [])
              if m[0] != a_]
        if len(c_) != 1:
            n_hist["attested: %s modern spellings" % (
                "no" if not c_ else "several")] += 1
            continue
        mf, ok = c_[0]
        if accent_kind(a_, mf) == "missing":
            n_hist["attested: missing accent"] += 1
            continue
        h_att[a_] = ok
        n_hist["attested: added"] += 1
    for v, ps in h_new.items():
        for l, g in ps:
            hist.setdefault(v, []).append((l, g))
    for v, ps in h_att.items():
        for l, g in ps:
            if (l, g) not in hist.setdefault(v, []):
                hist[v].append((l, g))
    for v, ps in h_coll.items():
        hist[v] = hist[v] + ps
    for f, spec in HIST_READINGS.items():
        before = list(hist.get(f, []))
        if spec == "no voseo":
            new = [(l, g) for l, g in before if not is_voseo(g)]
        elif isinstance(spec, str):
            new = list(cont.get(spec, []))
        else:
            new = list(spec)
        if not new:
            problems.append("19th century: %s would be left with no reading"
                            % f)
            continue
        hist[f] = new
        h_coll.pop(f, None)
        h_over.extend((f, l, g) for l, g in new)
        dlog.append(("19th-century readings", f, "decided 261113",
                     "set", "%s (was %s)" % (in_words(new), in_words(before))))
    hist_spell = sorted({(v, l, g) for v, ps in h_new.items() for l, g in ps}
                        | {(v, l, g) for v, ps in h_coll.items()
                           for l, g in ps} | set(h_over))
    hist_att = sorted({(v, l, g) for v, ps in h_att.items() for l, g in ps})
    n_hist["new spellings"] = len(h_new)
    n_hist["words given a Bello reading"] = len(h_coll)
    hist_set = {(f, l, g) for f, an in hist.items() for l, g in an}
    cont_set = {(f, l, g) for f, an in cont.items() for l, g in an}
    dicc_h = build_dict(hist_set)
    dicc_c = build_dict(cont_set)
    dicc_0 = build_dict({(f, l, zero(g)) for f, l, g in cont_set})
    # FreeLing's own files for both: the entries files hold the default
    # dictionary's Chilean readings; the readings only the historical one
    # has (the vosotros readings of the -is forms in the Chilean lists) go
    # to historical/dictionary/entries/CL.historical; each remove file
    # lists the Spanish readings its dictionary drops.
    for n in SOURCES:
        src[n] = [t for t in src[n] if t in cont_set]
    entries_c = [t for n in SOURCES for t in src[n]]
    hist_spell = [t for t in hist_spell if t in hist_set]
    hist_extra = set(hist_spell) | set(hist_att)
    hist_only = sorted(hist_set - cont_set - base_set - hist_extra)
    hist_spell = sorted(set(hist_spell) - base_set - cont_set)
    # readings of the Chilean entries files the 19th-century dictionary
    # drops (decided 261113: rei, soi, hai). FreeLing's build-dict applies
    # a remove folder to the Spanish entries only, so these are listed
    # apart, and the check below leaves them out of the Chilean entries.
    remove_h_cl = sorted({t for t in entries_c if t not in hist_set})
    hist_att = sorted(set(hist_att) - base_set - cont_set - set(hist_spell))
    remove_h = sorted(base_set - hist_set)
    remove_c = sorted(base_set - cont_set)
    sim_h, empty_h = simulate_freeling_build(
        base, remove_h, [t for t in entries_c if t in hist_set] + hist_only +
        hist_spell + hist_att)
    sim_c, empty_c = simulate_freeling_build(base, remove_c, entries_c)
    if sim_h != dicc_h:
        problems.append("FreeLing's build-dict would not give the historical "
                        "dictionary from the entries and remove files")
    if sim_c != dicc_c:
        problems.append("FreeLing's build-dict would not give the default "
                        "dictionary from the entries and remove files")
    # A Spanish form whose only reading is removed (the Spanish
    # interjections agur, caray, ole ...) is not in the dictionaries any
    # more: FreeLing guesses it like any unknown word. FreeLing's own
    # build-dict would write it with no analysis, which FreeLing reads the
    # same way.
    emptied = sorted(set(empty_h) | set(empty_c))
    for f in emptied:
        dlog.append(("interjection-removals", f, "interjection removed",
                     "no reading left", "it was only an interjection: "
                     "FreeLing now treats it as an unknown word"))

    # ---- 11  probabilities, locutions, np, quantities --------------------
    base_prob = (bt / "probabilitats.dat").read_text(encoding="utf-8")
    cls_t, single_t, form_t = read_prob_tables(base_prob)
    # The lines of the decided names start from FreeLing's own Spanish
    # lines, never from the deployed file, which may hold the lines an
    # earlier build wrote for them: run on any earlier build, the build
    # gives the same probabilitats.dat.
    es_prob = srcb["data/es/probabilitats.dat"].decode("utf-8")
    _, _, es_form_t = read_prob_tables(es_prob)
    es_lines = formtag_lines(es_prob)
    for f in set(decided_names) | set(exempted):
        if f in es_form_t:
            form_t[f] = es_form_t[f]
        else:
            form_t.pop(f, None)
    corpus_n = word_counts(srcb["data/es/tagger.dat"].decode("utf-8"))
    formtag_new = []
    for f in sorted(cont):
        an = cont[f]
        shorts = sorted({g[:3] for _, g in an})
        mts = {g[2:4] for _, g in an}
        if (len(an) >= 2 and all(g.startswith("V") for _, g in an)
                and len(shorts) == 2 and shorts[0][2] == "I"
                and shorts[1][2] == "S" and mts == {"IF", "SI"}):
            formtag_new.append(("%s %s %s %d %s %d" % (
                f, "-".join(shorts), shorts[0], FUTURE_WEIGHT, shorts[1],
                SUBJ_WEIGHT), "unaccented future against imperfect "
                "subjunctive: future 20%"))
        lemmas = {l for l, _ in an}
        for good, bad in PREFER:
            if lemmas != {good, bad}:
                continue
            gs = {g[:3] for l, g in an if l == good}
            bs = {g[:3] for l, g in an if l == bad}
            if gs & bs:
                continue
            formtag_new.append(("%s %s %s" % (f, "-".join(shorts), " ".join(
                "%s %d" % (t, PREFERRED_WEIGHT if t in gs else OTHER_WEIGHT)
                for t in shorts)), "%s over %s" % (good, bad)))
    rare_forms = {f for f, (l, r) in interj_single.items() if r} | MM_RARE
    managed, wrows = {}, []
    for f in sorted(rare_forms | set(decided_names) | set(rare_tags)):
        an = cont.get(f)
        if not an:
            continue
        shorts = collections.Counter(short_tag(g, tagset) for _, g in an)
        kinds = decided_names.get(f, set())
        share = None
        if kinds and any(not g.startswith("NP") for _, g in an):
            share = PLACE_SHARE if "place" in kinds else NAME_SHARE
        zero_i = f in rare_forms
        zeros = ({"I"} if zero_i else set()) | rare_tags.get(f, set())
        old = form_t.get(f)
        if old and "NP" in shorts and share is not None:
            old = {k: v for k, v in old.items() if k != "NP"}
        if old and zeros:
            old = {k: v for k, v in old.items() if k not in zeros}
        line = managed_line(f, shorts, old, cls_t, single_t,
                            set_np=share, zero=zeros)
        if line is None:
            continue
        rule = []
        if share is not None:
            rule.append("decided %s: the proper noun gets %d%% (decided "
                        "261110)" % ("place" if "place" in kinds else "name",
                                     round(share * 100)))
        if zero_i:
            rule.append("RARE interjection: nearly impossible (decided "
                        "261108)" if f not in MM_RARE else
                        "mm: millimeter by far the more probable, the "
                        "interjection nearly impossible (decided 261108)")
        if rare_tags.get(f):
            rule.append("decided verb reading nearly impossible on its own "
                        "(decided 261110b)")
        managed[f] = (line, "; ".join(rule))
        if share is not None:
            ordinary = [(l, g) for l, g in an if not g.startswith("NP")]
            corpus = corpus_n.get(f, 0)
            wrows.append((f, "place" if "place" in kinds else "name",
                          "%d%%" % round(share * 100), in_words(ordinary),
                          str(corpus),
                          "common word: review" if corpus >= COMMON_COUNT
                          else "", line))
    # An exempted name: FreeLing's own line, or none (decided 261110b).
    for f in exempted:
        if f in managed:
            continue
        managed[f] = (es_lines.get(f), (
            "decided name also a common noun or a verb: no proper-noun "
            "reading, FreeLing's own line (decided 261110b)" if f in es_lines
            else "decided name also a common noun or a verb: no proper-noun "
            "reading, FreeLing has no line for it (decided 261110b)"))
    # A reading given at the start of a sentence beside the word's own
    # (decided 261110e): its share among the readings the word has there
    # (all its own, or only those of the classes named). The proper noun
    # only exists there, so elsewhere the word keeps its own readings with
    # FreeLing's proportions. probabilitats.dat is read with both rule
    # files, so a form that keeps its own readings in both must keep them
    # with the same reading, share and classes (decided 261110g).
    for f, per in sorted(dec.start_classes.items()):
        kept = list(dict.fromkeys(r for r in per.values() if r[1]))
        if not kept:
            continue
        if len({(r[0], r[2], r[4]) for r in kept}) > 1:
            problems.append("%s: %s keeps its own readings at the start of a "
                            "sentence in np.dat and np-speech.dat with a "
                            "different reading, share or word classes; "
                            "probabilitats.dat holds one line for both"
                            % (", ".join(sorted({r[3] for r in kept})), f))
            continue
        reading, keep, share, fn, only = kept[0]
        an = cont.get(f)
        if not an:
            problems.append("%s: %s has no reading in the dictionary to keep"
                            % (fn, f))
            continue
        if f in managed:
            problems.append("%s: %s already has a managed probability line "
                            "(%s)" % (fn, f, managed[f][1]))
            continue
        tag = START_TAG[reading]
        shorts = collections.Counter(short_tag(g, tagset) for _, g in an)
        if short_tag(tag, tagset) in shorts:
            problems.append("%s: %s already has a proper-noun reading" % (fn, f))
            continue
        among = None
        if only:
            among = {short_tag(g, tagset) for _, g in an
                     if any(g.startswith(x) for x in only)}
            if not among:
                problems.append("%s: %s has no reading of the classes to keep "
                                "(%s)" % (fn, f, ", ".join(
                                    k for k, v in KEEP_CLASSES.items()
                                    if v in only)))
                continue
        shorts[short_tag(tag, tagset)] += 1
        line = managed_line(f, shorts, es_form_t.get(f), cls_t, single_t,
                            set_np=share, share_among=among)
        managed[f] = (line, "at the start of a sentence: %s at %g%% beside %s "
                      "(decided 261110e)"
                      % (reading, round(share * 100, 2),
                         ("its own %s readings" % " and ".join(
                             k for k, v in KEEP_CLASSES.items() if v in only))
                         if only else "its own readings"))
    prob_text, n_lp, n_ft, n_repl, n_prm = process_probabilities(
        base_prob, formtag_new, managed, changes, place_only)
    prob_text = fix_tagset_reference(prob_text, "probabilitats", changes,
                                     problems)
    prob_text = drop_unknown_tags(prob_text, tagset, changes)
    lemmas_of = collections.defaultdict(set)
    for f, an in cont.items():
        for l, g in an:
            lemmas_of[f].add(l)
    loc_full, lf_in, lf_out = process_locutions(
        (bt / "locucions.dat").read_text(encoding="utf-8"), changes,
        "locucions", interj_multi, rm_multi, lemmas_of=lemmas_of,
        general=srcb["data/es/locucions.dat"].decode("utf-8"),
        decided=dec.locutions, decided_rm=dec.locution_removals,
        tagset=tagset, problems=problems)
    for key, (lemma, tag, flag, fname) in dec.locutions.items():
        dlog.append((fname, key, "multiword, lemma %s, tag %s, flag %s"
                     % (lemma, tag, flag), "locution", "locucions.dat"))
    for key, fname in dec.locution_removals.items():
        dlog.append((fname, key, "multiword removed", "removed",
                     "locucions.dat"))
    loc_min, lm_in, lm_out = process_locutions(
        MINIMAL_LOCUTIONS, changes, "locucions-MINIMAL", interj_multi,
        rm_multi, add_new=False)
    loc_full = fix_tagset_reference(loc_full, "locucions", changes, problems)
    loc_min = fix_tagset_reference(loc_min, "locucions-MINIMAL", changes,
                                   problems)
    # The 19th-century probabilities (decided 261113): a reading a Bello
    # rule adds to a word that already exists is nearly impossible on its
    # own; the rest is the default probabilitats.dat.
    cls_h, single_h, form_h = read_prob_tables(prob_text)
    managed_h = {}
    n_coll_same = 0
    for v, ps in sorted(h_coll.items()):
        an = hist[v]
        shorts = collections.Counter(short_tag(g, tagset) for _, g in an)
        old_s = {short_tag(g, tagset) for l, g in an if (l, g) not in ps}
        new_s = {short_tag(g, tagset) for _, g in ps} - old_s
        if not new_s:
            n_coll_same += 1
            continue
        line = managed_line(v, shorts, form_h.get(v), cls_h, single_h,
                            zero=new_s)
        if line:
            managed_h[v] = (line, "a 19th-century spelling of %s: nearly "
                            "impossible on its own (decided 261113)"
                            % in_words(ps))
    for f, pct in HIST_PROBS.items():
        an = hist.get(f, [])
        have_s = {short_tag(g, tagset) for _, g in an}
        if set(pct) != have_s:
            problems.append("19th century: %s has the short tags %s, not %s"
                            % (f, " ".join(sorted(have_s)),
                               " ".join(sorted(pct))))
            continue
        keys = sorted(pct)
        managed_h[f] = ("%s %s %s" % (f, "-".join(keys), " ".join(
            "%s %d" % (k, pct[k]) for k in keys)), "decided 261113")
    prob_hist, _, n_ft_h, n_repl_h, _ = process_probabilities(
        prob_text, [], managed_h, [], ())
    # vosotros over voseo (decided 261113): a form with both readings, of
    # the same verb and tense, is read as vosotros, and vos as the polite
    # pronoun. Both readings have the same short tag, so FreeLing's
    # probabilities and tagger cannot tell them apart; the tag preferences
    # (PosPreferences) decide between analyses of equal probability.
    vpref = {(VOS_POLITE, VOS_TAG)}
    for f, an in hist.items():
        sv = {(l, g[:4]): g for l, g in an if VOSEO.match(g)}
        for l, g in an:
            if VOSOTROS.match(g) and (l, g[:4]) in sv:
                vpref.add((g, sv[(l, g[:4])]))
    pl = prob_hist.splitlines()
    a_ = pl.index("<PosPreferences>")
    b_ = pl.index("</PosPreferences>")
    have_p = {tuple(x.split()[:2]) for x in pl[a_ + 1:b_] if x.split()}
    vclash = sorted(p for p in vpref if (p[1], p[0]) in have_p)
    vadd = sorted(p for p in vpref if p not in have_p and p not in vclash)
    if vclash:
        problems.append("19th century: PosPreferences already prefers "
                        "voseo for %s" % ", ".join("%s %s" % p for p in vclash))
    pl[b_:b_] = ["%s %s" % p for p in vadd]
    prob_hist = "\n".join(pl) + "\n"
    n_hist["vosotros over voseo (tag preferences)"] = len(vadd)
    # A reading a Bello rule adds that shares its word class with one the
    # word already has cannot be made improbable by its counts: FreeLing
    # gives both the same probability. The lemma preferences settle it:
    # the word's own lemma wins (FreeLing's probabilities module orders
    # analyses of equal probability by them).
    prefs = set()
    for v, ps in h_coll.items():
        own = [(l, g) for l, g in hist[v] if (l, g) not in ps]
        for l, g in ps:
            for l0, g0 in own:
                if l0 != l and short_tag(g0, tagset) == short_tag(g, tagset):
                    prefs.add((l0, l))
    prefs = sorted(p for p in prefs if (p[1], p[0]) not in prefs)
    pl = prob_hist.splitlines()
    a_ = pl.index("<LemmaPreferences>")
    b_ = pl.index("</LemmaPreferences>")
    have_p = {tuple(x.split()[:2]) for x in pl[a_ + 1:b_] if x.split()}
    clash = [p for p in prefs if (p[1], p[0]) in have_p]
    prefs = [p for p in prefs if p not in have_p and p not in clash]
    pl[b_:b_] = ["%s %s" % p for p in prefs]
    prob_hist = "\n".join(pl) + "\n"
    n_hist["Bello lemmas below the word's own (lemma preferences)"] = \
        len(prefs)
    n_hist["Bello lemma preferences left out (the opposite preference "
           "exists)"] = len(clash)
    n_hist["Bello readings nearly impossible"] = len(managed_h)
    n_hist["Bello readings sharing a word class (no line)"] = n_coll_same
    # The 19th-century multiwords: every multiword in the spellings of the
    # rules, when the key is new (decided 261113).
    head_l, body_l, tail_l = split_locutions(loc_full)
    have_l = {x.split()[0] for x in body_l}
    loc_add = []
    for x in body_l:
        t = x.split()
        for k in sorted(key_variants(t[0], HIST_RULES)):
            if k not in have_l:
                have_l.add(k)
                loc_add.append(" ".join([k] + t[1:]))
    loc_hist = "\n".join(head_l + body_l + loc_add + tail_l) + "\n"
    n_hist["multiwords"] = len(loc_add)
    cfg_base = stock_es_cl_cfg()
    cfg_c = write_config(cfg_base, "es/es-cl", problems, "es-cl.cfg")
    cfg_h = write_config(cfg_base, "es/es-cl/historical", problems,
                         "es-cl-19th-century.cfg", compounds=False)
    # The 19th-century files sit one folder down: their tagset is the
    # Chilean one in the folder above.
    prob_hist = prob_hist.replace("<TagsetFile>\n./tagset.dat\n",
                                  "<TagsetFile>\n../tagset.dat\n", 1)
    loc_hist = loc_hist.replace("<TagSetFile>\n./tagset.dat\n",
                                "<TagSetFile>\n../tagset.dat\n", 1)
    if "../tagset.dat" not in prob_hist or "../tagset.dat" not in loc_hist:
        problems.append("historical probabilitats.dat or locucions.dat: the "
                        "tagset reference could not be pointed at "
                        "../tagset.dat")
    np_text = process_np(srcb["data/es/np.dat"].decode("utf-8"), changes,
                         problems)
    quant_text = process_quantities(
        srcb["data/es/quantities.dat"].decode("utf-8"), changes, problems)

    # ---- 11b  the names (decided 261110d) --------------------------------
    gazper_p_text = gazper_p.read_text(encoding="utf-8")
    name_files, fixed_rows, ncount = process_names(
        srcb, gazper_p_text, lists["cities"], dicc_c.decode("utf-8"),
        loc_full, np_text, dec, changes, dlog, problems)

    # ---- 12  checks ------------------------------------------------------
    for text, kind, nm in ((dicc_c.decode("utf-8"), "dicc", "dicc.src"),
                           (dicc_h.decode("utf-8"), "dicc",
                            "historical/dicc.src"),
                           (dicc_0.decode("utf-8"), "dicc", "dicc-0-tags.src"),
                           (prob_text, "prob", "probabilitats.dat"),
                           (prob_hist, "prob",
                            "historical/probabilitats.dat"),
                           (loc_full, "locu", "locucions.dat"),
                           (loc_hist, "locu", "historical/locucions.dat"),
                           (loc_min, "locu", "locucions-MINIMAL.dat"),
                           (name_files["data/es/es-cl/np.dat"], "np",
                            "np.dat"),
                           (name_files["data/es/es-cl/np-speech.dat"], "np",
                            "np-speech.dat"),
                           (name_files["data/es/nerc/nec/nec-ab-poor1.dat"],
                            "nec", "nec-ab-poor1.dat"),
                           (quant_text, "quant", "quantities.dat")):
        seen = set()
        for tag, where in tags_in(text, kind):
            if tag in seen:
                continue
            seen.add(tag)
            why = undecodable(tag, tagset)
            if why:
                problems.append("%s: tag %s cannot be decoded by the Chilean "
                                "tagset (%s), e.g. in: %s"
                                % (nm, tag, why, where[:120]))
    for dicc, nm, want in ((dicc_c, "dicc.src", {VOS_TAG}),
                           (dicc_h, "historical/dicc.src",
                            {VOS_TAG, VOS_POLITE})):
        for line in dicc.decode("utf-8").splitlines():
            t = line.split()
            if len(t) < 3 or len(t) % 2 == 0:
                continue
            form, pairs = t[0], [(t[i], t[i + 1]) for i in range(1, len(t), 2)]
            for l, g in pairs:
                if g.startswith("P") and len(g) == 7 and g[6] == "V":
                    if form in TU_FORMS:
                        problems.append("%s: %s, a form of tu, has the voseo "
                                        "tag %s" % (nm, form, g))
                    elif l != "vos":
                        problems.append("%s: %s has the voseo pronoun tag %s "
                                        "with the lemma %s, not vos"
                                        % (nm, form, g, l))
        vos_tags, deis, isf, unexpected = voseo_check(dicc)
        if vos_tags != want:
            problems.append("%s: vos must have exactly %s; it has %s"
                            % (nm, " ".join(sorted(want)),
                               " ".join(sorted(vos_tags))))
        if unexpected:
            problems.append("%s: forms not in -is with a voseo and a vosotros "
                            "reading of the same verb: %s"
                            % (nm, "; ".join(unexpected[:10])))
        if nm == "dicc.src" and (isf or deis):
            problems.append("dicc.src: %d -is forms and %d deis keep both "
                            "readings" % (isf, deis))
        if nm == "dicc.src":
            check_c = (vos_tags, deis, isf)
        else:
            check_h = (vos_tags, deis, isf)
    # Every line of the common misspellings must be in the dictionary
    # FreeLing reads, with exactly its readings (decided 261112).
    for dicc, nm in ((dicc_c, "dicc.src"), (dicc_h, "historical/dicc.src")):
        got = set()
        for line in dicc.decode("utf-8").splitlines():
            t = line.split()
            if len(t) >= 3 and len(t) % 2 == 1:
                got.update((t[0], t[i], t[i + 1]) for i in range(1, len(t), 2))
        lost = [x for x in src["common-misspellings"] + src["old-accents"]
                if x not in got]
        if lost:
            problems.append("%s: %d line(s) of CL.common-misspellings and "
                            "CL.old-accents are not in it, e.g. %s"
                            % (nm, len(lost), " ".join(lost[0])))
        if nm == "historical/dicc.src":
            lost = [x for x in hist_spell + hist_att if x not in got]
            if lost:
                problems.append("%s: %d 19th-century line(s) are not in it"
                                % (nm, len(lost)))
    for text, nm in ((loc_full, "locucions.dat"),
                     (loc_hist, "historical/locucions.dat"),
                     (loc_min, "locucions-MINIMAL.dat")):
        _, body, _ = split_locutions(text)
        for st_ in body:
            t = st_.split()
            for g in t[1:-1][1::2]:
                if not (g in es_tags or zero(g) in es_tags or g == "I"
                        or g.startswith(("$", "NP"))):
                    problems.append("%s: unknown tag %s in: %s" % (nm, g, st_))
    if problems:
        log("")
        for p in problems[:200]:
            log("REFUSED: %s" % p)
        if len(problems) > 200:
            log("REFUSED: ... and %d more" % (len(problems) - 200))
        log("Nothing was written.")
        return 2

    # ---- report ----------------------------------------------------------
    kinds = collections.Counter((c[0], c[1]) for c in changes)
    dkinds = collections.Counter((d[0].split("--")[0], d[3]) for d in dlog)
    n_c = dicc_c.count(b"\n") - 5
    n_h = dicc_h.count(b"\n") - 5
    log("")
    log("DECISIONS")
    for (n, k), c in sorted(dkinds.items()):
        log("  %-38s %-18s %6d" % (n, k, c))
    log("  new verbs conjugated: %d (%d forms)" % (n_paradigms,
                                                   n_paradigm_lines))
    log("  standard lemmas applied: %s" % ", ".join(
        "%s %d" % kv for kv in sorted(n_std.items())))
    log("")
    log("CHANGES")
    for (n, k), c in sorted(kinds.items()):
        log("  %-18s %-10s %7d" % (n, k, c))
    log("")
    log("entries: %s" % ", ".join("%s %d" % (n, len(src[n])) for n in SOURCES))
    log("variants: %d forms, %d lines; skipped: %s"
        % (len(variants), len(var_lines), ", ".join(
            "%s %d" % kv for kv in sorted(skipped.items())) or "none"))
    log("names (lists): %d added; skipped: %s" % (len(name_lines), ", ".join(
        "%s %d" % kv for kv in sorted(name_skip.items())) or "none"))
    log("decided names also common nouns or verbs: %d exempted"
        % len(exempted))
    log("decided names with another ordinary reading: %d weighted (%d "
        "marked common)" % (len(wrows), sum(1 for w in wrows if w[5])))
    log("probabilities: %d lemma preferences, %d form lines added, %d "
        "replaced, %d removed" % (n_lp, n_ft, n_repl, n_prm))
    log("locutions: %d lines -> %d entries; minimal %d -> %d"
        % (lf_in, lf_out, lm_in, lm_out))
    log("place-only forms: %s" % (", ".join(sorted(place_only)) or "none"))
    log("names: %d place names in the Chilean data; gazLOC-c.dat %d (+%d), "
        "cities.dat %d (+%d), gazPER-c.dat %d (-%d), gazPER-p.dat %d"
        % (ncount["places"], ncount["gazLOC-c"], ncount["gazLOC-c added"],
           ncount["cities"], ncount["cities added"], ncount["gazPER-c"],
           ncount["gazPER-c removed"], ncount["gazPER-p"]))
    log("fixed names: %d (%d places), %d lines in np.dat and np-speech.dat; "
        "%d decided not fixed" % (ncount["fixed names"],
                                  ncount["fixed places"],
                                  ncount["fixed lines"], ncount["not fixed"]))
    log("sentence start: %d readings in np.dat, %d in np-speech.dat; class "
        "shares: %d names" % (ncount["start np.dat"],
                              ncount["start np-speech.dat"], ncount["shares"]))
    log("default dictionary   : %d forms, %d bytes; vos %s; -is with both "
        "%d" % (n_c, len(dicc_c), " ".join(sorted(check_c[0])), check_c[2]))
    log("historical dictionary: %d forms, %d bytes; vos %s; -is with both "
        "%d" % (n_h, len(dicc_h), " ".join(sorted(check_h[0])), check_h[2]))
    log("FreeLing's build-dict gives both, byte for byte (historical-only "
        "readings %d; forms left with no reading %d)" % (len(hist_only),
                                                         len(emptied)))
    log("common misspellings: %d unaccented forms added, %d left out (from "
        "several accented forms); CL.common-misspellings %d lines, all in "
        "dicc.src" % (n_miss["added"], n_miss["from several accented forms"],
                      len(src["common-misspellings"])))
    log("old accents: %d lines (%s)" % (len(src["old-accents"]), ", ".join(
        a for a, _ in OLD_ACCENTS)))
    log("19th century: %d new spellings (%d lines), %d words given a Bello "
        "reading (%d nearly impossible on their own), %d attested spellings, "
        "%d multiwords" % (n_hist["new spellings"], len(hist_spell),
                           n_hist["words given a Bello reading"],
                           n_hist["Bello readings nearly impossible"],
                           n_hist["attested: added"], n_hist["multiwords"]))
    for k_, v_ in sorted(n_hist.items()):
        log("  %-52s %8d" % (k_, v_))

    # The files of the release that are copied as they are: their privacy
    # is checked here too, so a dry run shows it (the build report and the
    # data are checked when they are written).
    copied = [("README.md", readme), ("LICENSE", license)] + \
        [("software/" + s_.name, s_) for s_ in software] + \
        [("software/patches/" + s_.name, s_) for s_ in patch_files] + \
        [("packaging/" + f, packaging / f) for f in PACKAGING_FILES] + \
        [(".github/workflows/" + PACKAGING_WORKFLOW, packaging / PACKAGING_WORKFLOW)] + \
        [("sources/escl-sources/" + p.name, p)
         for p in sorted(dec.files, key=lambda p: p.name)]
    if (ddir / "README.md").is_file():
        copied.append(("sources/escl-sources/README.md", ddir / "README.md"))
    pre = []
    for rel_, p in copied:
        pre += make_public(rel_, p.read_bytes(), prows, pterms)[1]
    log("privacy: %d replacement(s), %d term(s); %d copied file(s) checked, "
        "%d private line(s) left" % (len(prows), len(pterms), len(copied),
                                     len(pre)))
    for p in pre:
        log("PRIVATE: %s" % p)

    if a.dry_run:
        log("")
        if pre:
            log("DRY RUN -- nothing written. The build would write nothing: "
                "private text is left in %d line(s)." % len(pre))
            return 1
        log("DRY RUN -- nothing written.")
        return 0

    # ---- write -----------------------------------------------------------
    stamp = time.strftime("%y%m%d")
    tmp = out.with_name(out.name + ".part")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    files = {}
    private = []

    def put(rel, data):
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        b = data if isinstance(data, bytes) else data.encode("utf-8")
        b, found = make_public(rel, b, prows, pterms)
        private.extend(found)
        p.write_bytes(b)
        files[rel] = sha(b)

    def lines_of(triples):
        return "".join("%s %s %s\n" % t for t in sorted(set(triples)))

    d = "data/es/es-cl/"
    put(d + "dicc.src", dicc_c)
    put(d + "historical/dicc.src", dicc_h)
    put(d + "dictionary/header", HEADER)
    for n in SOURCES:
        if src[n]:
            put(d + "dictionary/entries/CL." + n, lines_of(src[n]))
    put(d + "remove/CL.removed", lines_of(remove_c))
    put(d + "historical/remove/CL.removed", lines_of(remove_h))
    put(d + "historical/CL.removed-from-chilean-entries",
        lines_of(remove_h_cl))
    put(d + "historical/dictionary/entries/CL.historical",
        lines_of(hist_only))
    put(d + "historical/dictionary/entries/CL.19th-century-spellings",
        lines_of(hist_spell))
    put(d + "historical/dictionary/entries/CL.19th-century-attested",
        lines_of(hist_att))
    put(d + "historical/probabilitats.dat", prob_hist)
    put(d + "historical/locucions.dat", loc_hist)
    put("data/config/es-cl.cfg", cfg_c)
    put("data/config/es-cl-19th-century.cfg", cfg_h)
    put(d + "probabilitats.dat", prob_text)
    put(d + "locucions.dat", loc_full)
    put(d + "locucions-MINIMAL.dat", loc_min)
    put(d + "tagset.dat", tagset_text)
    put(d + "quantities.dat", quant_text)
    for rel_ in sorted(name_files):
        put(rel_, name_files[rel_])
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED,
                         compresslevel=9) as z:
        zi = zipfile.ZipInfo("dicc-0-tags.src", date_time=(2026, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        z.writestr(zi, dicc_0)
    put("tuteo-tagged-dictionary/dicc-0-tags.zip", zbuf.getvalue())
    private.extend("tuteo-tagged-dictionary/dicc-0-tags.zip: dicc-0-tags.src "
                   "line %d: %s" % h for h in private_hits(dicc_0, pterms))
    put("tuteo-tagged-dictionary/dicc-0-tags_README.md", TUTEO_README)

    def tsv(rows):
        return "".join("%s\t%s\t%s\n" % e for e in rows)

    def plain(rows):
        return list(dict.fromkeys((f, l, zero(g)) for f, l, g in rows))
    gl = "grammatical-lists/freeling-cl/"
    for name in NAME_TAG:
        put(gl + "CL.%s.GRAM.txt" % name, tsv(lists[name]))
    ordered = {n: lists[n] for n, _ in LISTS}
    ordered["variants"] = sorted(set(var_lines))
    for name, rows in ordered.items():
        stem = "CL." + name
        if name in ("vaux", "verb", "variants", "tanc"):
            put(gl + "%s.Vos-V.GRAM.txt" % stem, tsv(rows))
            put(gl + "%s.GRAM.txt" % stem, tsv(plain(rows)))
        else:
            put(gl + "%s.GRAM.txt" % stem, tsv(rows))
    put("CHANGELOG.tsv", "list\tchange\trule\tform\tlemma\ttag\t"
        "grammatical information\tdetail\n" +
        "".join("\t".join(c[:6] + (describe(c[5]),) + c[6:]) + "\n"
                for c in changes))
    put("VARIANTS.tsv", "rule\tvariant\tstandard form\tanalyses copied\t"
        "status\n" + "".join("\t".join(r) + "\n" for r in vrows))
    put("DECISIONS.tsv", "decision file\tform\tdecided\toutcome\tdetail\n" +
        "".join("\t".join(r) + "\n" for r in dlog))
    put("NAME-CLASSES.tsv", "form\trule\tclass\ttag\tshare\tfiles\t"
        "source\tnote\n" +
        "".join("\t".join(r) + "\n" for r in fixed_rows))
    put("NAME-WEIGHTS.tsv", "form\tdecided as\tproper noun share\t"
        "ordinary readings\toccurrences in FreeLing's Spanish corpus\t"
        "note\tprobabilitats.dat line\n" +
        "".join("\t".join(r) + "\n" for r in wrows))
    rep = ["# %s -- build report" % RELEASE, "",
           "Built by freeling_escl_build.py %s on %s." % (VERSION, stamp), "",
           "| item | count |", "|---|---|"]
    for (n, k), c in sorted(kinds.items()):
        rep.append("| %s %s | %d |" % (n, k, c))
    for (n, k), c in sorted(dkinds.items()):
        rep.append("| decisions: %s, %s | %d |" % (n, k, c))
    rep += ["| new verbs conjugated | %d |" % n_paradigms,
            "| their forms | %d |" % n_paradigm_lines,
            "| variant forms | %d |" % len(variants),
            "| names added from the lists | %d |" % len(name_lines),
            "| decided names exempted (also a common noun or verb) | %d |"
            % len(exempted),
            "| decided names weighted | %d |" % len(wrows),
            "| lemma preferences added | %d |" % n_lp,
            "| FormTagFreq lines added | %d |" % n_ft,
            "| FormTagFreq lines replaced | %d |" % n_repl,
            "| FormTagFreq lines removed | %d |" % n_prm,
            "| default dicc.src forms | %d |" % n_c,
            "| historical dicc.src forms | %d |" % n_h,
            "| common misspellings added (unaccented forms) | %d |"
            % n_miss["added"],
            "| left out: from several accented forms | %d |"
            % n_miss["from several accented forms"],
            "| CL.common-misspellings lines | %d |"
            % len(src["common-misspellings"]),
            "| CL.old-accents lines | %d |" % len(src["old-accents"]),
            "| 19th century: new spellings | %d |" % n_hist["new spellings"],
            "| 19th century: words given a Bello reading | %d |"
            % n_hist["words given a Bello reading"],
            "| 19th century: Bello readings nearly impossible | %d |"
            % n_hist["Bello readings nearly impossible"],
            "| 19th century: attested spellings added | %d |"
            % n_hist["attested: added"],
            "| 19th century: multiwords added | %d |" % n_hist["multiwords"],
            "| default: -is forms with both readings | %d |" % check_c[2],
            "| historical: -is forms with both readings | %d |" % check_h[2],
            "| place-only forms | %d |" % len(place_only),
            "| place names in the Chilean data | %d |" % ncount["places"],
            "| gazLOC-c.dat: names (added) | %d (%d) |"
            % (ncount["gazLOC-c"], ncount["gazLOC-c added"]),
            "| cities.dat: names (added) | %d (%d) |"
            % (ncount["cities"], ncount["cities added"]),
            "| gazPER-c.dat: names (removed) | %d (%d) |"
            % (ncount["gazPER-c"], ncount["gazPER-c removed"]),
            "| gazPER-p.dat: name parts | %d |" % ncount["gazPER-p"],
            "| fixed names (places) | %d (%d) |"
            % (ncount["fixed names"], ncount["fixed places"]),
            "| FixedClasses lines in each np file | %d |"
            % ncount["fixed lines"],
            "| SentenceStartClasses lines: np.dat, np-speech.dat | %d, %d |"
            % (ncount["start np.dat"], ncount["start np-speech.dat"]),
            "| names with class shares (nec-ab-poor1.dat) | %d |"
            % ncount["shares"],
            "", "## Entries files", ""]
    for n in SOURCES:
        rep.append("- `CL.%s`: %d lines" % (n, len(set(src[n]))))
    rep.append("- `historical/dictionary/entries/CL.historical`: %d lines"
               % len(hist_only))
    rep.append("- `historical/dictionary/entries/CL.19th-century-spellings`: "
               "%d lines" % len(hist_spell))
    rep.append("- `historical/dictionary/entries/CL.19th-century-attested`: "
               "%d lines" % len(hist_att))
    rep.append("- forms left with no reading (Spanish interjections only): "
               "%d" % len(emptied))
    rep += ["", "## Inputs", ""]
    for rel in FL42:
        rep.append("- `%s` %s" % (st / rel, FL42[rel]))
    rep.append("- FreeLing 4.2's `data/config/es-cl.cfg`, carried in this "
               "script %s" % ES_CL_CFG_SHA)
    for p in [chilean_tagset, bt / "probabilitats.dat",
              bt / "locucions.dat", gazper_p] + patch_files + \
            [gram / f for _, f in LISTS + NAME_LISTS] + list(dec.files):
        rep.append("- `%s` %s" % (p, sha(p.read_bytes())))
    put("BUILD-REPORT.md", "\n".join(rep) + "\n")
    # README.md, LICENSE, the software and the build's own sources (so the
    # release can be rebuilt from itself).
    for rel_, p in copied:
        put(rel_, p.read_bytes())
        if rel_.startswith(("software/", "packaging/")) and \
                p.suffix in (".py", ".pl", ".sh"):
            os.chmod(tmp / rel_, 0o755)
    if private:
        log("")
        for p in private:
            log("PRIVATE: %s" % p)
        shutil.rmtree(tmp)
        log("NOT WRITTEN: private text is left in %d line(s) of the release "
            "(listed above); the release folder is unchanged." % len(private))
        return 1
    put("SHA256SUMS", "".join("%s  %s\n" % (h, r)
                              for r, h in sorted(files.items())))
    if out.exists():
        dep = next_free(out.parent / "deprecated" /
                        ("%s.DEPRECATED-%s" % (out.name, stamp)))
        dep.parent.mkdir(parents=True, exist_ok=True)
        os.replace(out, dep)
        log("previous build moved to %s" % dep)
    os.replace(tmp, out)
    log("")
    log("written: %s" % out)
    log("dicc.src sha256            %s" % sha(dicc_c))
    log("historical/dicc.src sha256 %s" % sha(dicc_h))
    log("=" * 78)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log("interrupted")
        sys.exit(130)
